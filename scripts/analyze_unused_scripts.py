#!/usr/bin/env python3
"""
分析 scripts 文件夹中未被项目引用的脚本

检查方式：
1. 扫描 scripts 文件夹中的所有 .py 文件
2. 在项目其他位置搜索对这些脚本的引用（import, 文件名引用等）
3. 排除 scripts 目录自身的引用
4. 输出未被使用的脚本列表
"""

import argparse
import json
import logging
import os
import pickle
import random
import re
import sys
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed


LOGGER_NAME = Path(__file__).name if '__file__' in globals() else 'analyze_unused_scripts.py'
LOG_FORMAT = '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
LOG_TIME_FORMAT = '%H:%M:%S'
logger = logging.getLogger(LOGGER_NAME)


def _configure_logger(log_file: Optional[Path] = None):
    formatter = logging.Formatter(LOG_FORMAT, LOG_TIME_FORMAT)

    # Console handler（只配置一次）
    if not any(isinstance(h, logging.StreamHandler) and getattr(h, '_from_analyze_unused', False)
               for h in logger.handlers):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        handler._from_analyze_unused = True  # type: ignore[attr-defined]
        logger.addHandler(handler)

    # File handler（可多次调用，确保唯一）
    if log_file is not None:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        if not any(isinstance(h, logging.FileHandler) and Path(getattr(h, 'baseFilename', '')) == log_file
                   for h in logger.handlers):
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    logger.setLevel(logging.INFO)
    logger.propagate = False


_configure_logger()


WORKER_SCRIPT_IDENTIFIERS: Dict[str, Set[str]] = {}


def _init_worker(script_identifiers: Dict[str, Set[str]]):
    global WORKER_SCRIPT_IDENTIFIERS
    WORKER_SCRIPT_IDENTIFIERS = script_identifiers


def _process_file_for_references(file_path_str: str) -> List[Tuple[str, str, str, str]]:
    file_path = Path(file_path_str)
    results: List[Tuple[str, str, str, str]] = []
    for script_key, identifiers in WORKER_SCRIPT_IDENTIFIERS.items():
        refs = search_references_in_file(file_path, identifiers)
        for identifier, locations in refs.items():
            for loc in locations:
                results.append((script_key, identifier, str(file_path), loc))
    return results


class AnalysisTimeoutError(RuntimeError):
    """Raised when the analysis exceeds the allowed runtime."""


# 需要分析的脚本扩展名
SCRIPT_EXTENSIONS = {'.py', '.sh', '.ps1', '.bat'}
MAX_RUNTIME_SECONDS = 60
DEFAULT_LOG_FILENAME = 'analyze_unused_scripts.log'
DEFAULT_STATE_FILENAME = 'analyze_unused_scripts.json'
DEFAULT_FILE_CACHE = 'analyze_unused_scripts.pkl'
DEFAULT_UNUSED_STATE_FILENAME = 'analyze_unused_scripts_true.json'
SINGLE_MODE = 'single'
ALL_MODE = 'all'


TimeChecker = Optional[Callable[[], None]]


def get_all_scripts(scripts_dir: Path, check_runtime: TimeChecker = None) -> List[Path]:
    """获取 scripts 目录下所有的脚本文件（.py, .sh, .ps1, .bat）"""
    scripts = []
    for root, dirs, files in os.walk(scripts_dir):
        if check_runtime:
            check_runtime()
        # 跳过 __pycache__ 目录
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            if check_runtime:
                check_runtime()
            if Path(file).suffix.lower() in SCRIPT_EXTENSIONS:
                scripts.append(Path(root) / file)
    return scripts


def log(msg: str, level: int = logging.INFO):
    """输出日志"""
    logger.log(level, msg)


def _load_used_scripts_state(state_path: Path) -> Set[str]:
    try:
        if not state_path.exists():
            return set()
        with open(state_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            entries = data.get('used_scripts', [])
        elif isinstance(data, list):
            entries = data
        else:
            entries = []
        return {str(item) for item in entries if isinstance(item, str)}
    except Exception as exc:
        log(f"读取 {state_path} 失败，忽略并重建: {exc}", logging.WARNING)
        return set()


def _save_used_scripts_state(state_path: Path, used_scripts: Set[str]) -> None:
    try:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            'used_scripts': sorted(used_scripts),
            'updated_at': __import__('datetime').datetime.now().isoformat(),
        }
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as exc:
        log(f"写入 {state_path} 失败: {exc}", logging.ERROR)


def _load_unused_scripts_state(state_path: Path) -> Set[str]:
    try:
        if not state_path.exists():
            return set()
        with open(state_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            entries = data.get('unused_scripts', [])
        elif isinstance(data, list):
            entries = data
        else:
            entries = []
        return {str(item) for item in entries if isinstance(item, str)}
    except Exception as exc:
        log(f"读取 {state_path} 失败，忽略并重建: {exc}", logging.WARNING)
        return set()


def _save_unused_scripts_state(state_path: Path, unused_scripts: Set[str]) -> None:
    try:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            'unused_scripts': sorted(unused_scripts),
            'updated_at': __import__('datetime').datetime.now().isoformat(),
        }
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as exc:
        log(f"写入 {state_path} 失败: {exc}", logging.ERROR)


def _ensure_state_file(state_path: Path) -> None:
    if not state_path.exists():
        _save_used_scripts_state(state_path, set())


def _ensure_unused_state_file(state_path: Path) -> None:
    if not state_path.exists():
        _save_unused_scripts_state(state_path, set())


def _load_project_files_cache(cache_path: Path, project_root: Path) -> Optional[List[Path]]:
    try:
        if not cache_path.exists():
            return None
        with open(cache_path, 'rb') as f:
            data = pickle.load(f)
        if not isinstance(data, dict):
            return None
        if data.get('project_root') != str(project_root):
            return None
        rel_files = data.get('files', [])
        if not isinstance(rel_files, list):
            return None
        return [project_root / Path(rel) for rel in rel_files]
    except Exception as exc:
        log(f"读取文件缓存失败，将重新扫描: {exc}", logging.WARNING)
        return None


def _save_project_files_cache(cache_path: Path, project_root: Path, files: List[Path]) -> None:
    try:
        rel_files = []
        for file_path in files:
            try:
                rel_files.append(str(file_path.relative_to(project_root)))
            except ValueError:
                # 如果无法相对化，跳过缓存该文件
                continue
        cache_data = {
            'project_root': str(project_root),
            'files': rel_files,
            'updated_at': __import__('datetime').datetime.now().isoformat(),
        }
        with open(cache_path, 'wb') as f:
            pickle.dump(cache_data, f)
        log(f"项目文件缓存已更新: {cache_path} (共 {len(rel_files)} 个文件)")
    except Exception as exc:
        log(f"写入文件缓存失败: {exc}", logging.WARNING)


def _scan_project_files(
    project_dir: Path,
    scripts_dir: Path,
    check_runtime: TimeChecker = None,
) -> List[Path]:
    """扫描项目文件列表（不含 scripts 目录）"""
    search_extensions = {'.py', '.md', '.txt', '.yml', '.yaml', '.json', '.sh', '.ps1', '.bat', '.rst', '.toml'}
    exclude_dirs = {
        '__pycache__', '.git', 'node_modules', '.venv', 'venv', 'env',
        '.pytest_cache', '.mypy_cache', 'dist', 'build', '.idea', '.vscode',
    }
    docs_dir = project_dir / 'docs'
    files_to_search: List[Path] = []

    for root, dirs, files in os.walk(project_dir):
        if check_runtime:
            check_runtime()
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        root_path = Path(root)

        # 跳过 scripts 目录自身
        try:
            root_path.relative_to(scripts_dir)
            continue
        except ValueError:
            pass

        for file in files:
            file_path = root_path / file
            suffix = file_path.suffix.lower()

            # 排除 docs 目录中的 Markdown 文档
            if suffix == '.md':
                try:
                    file_path.relative_to(docs_dir)
                    continue
                except ValueError:
                    pass

            if suffix in search_extensions:
                if check_runtime:
                    check_runtime()
                files_to_search.append(file_path)

    return files_to_search


def _search_single_script_references(
    script: Path,
    identifiers: Set[str],
    project_files: List[Path],
    project_root: Path,
    check_runtime: TimeChecker = None,
) -> Dict[str, List[Tuple[Path, str]]]:
    """在项目文件中搜索单个脚本的引用"""
    refs: Dict[str, List[Tuple[Path, str]]] = defaultdict(list)
    total_files = len(project_files)
    
    for idx, file_path in enumerate(project_files):
        if check_runtime:
            check_runtime()
        
        # 每处理100个文件输出一次进度
        if (idx + 1) % 500 == 0 or idx == total_files - 1:
            pct = ((idx + 1) / total_files * 100) if total_files else 100
            print(f"\r    搜索进度: {idx + 1}/{total_files} ({pct:.1f}%)", end='', flush=True)
        
        found = search_references_in_file(file_path, identifiers, check_runtime)
        for identifier, locations in found.items():
            for loc in locations:
                refs[identifier].append((file_path, loc))
    
    print()  # 换行
    return refs


def get_script_identifiers(script_path: Path, scripts_dir: Path) -> Set[str]:
    """
    获取脚本的各种可能被引用的标识符
    - 文件名（不含扩展名）
    - 完整文件名
    - 相对路径中的模块形式
    """
    identifiers = set()
    
    # 文件名（不含扩展名）
    stem = script_path.stem
    identifiers.add(stem)
    
    # 完整文件名
    identifiers.add(script_path.name)
    
    # 相对路径（用于 import 语句，仅 .py 文件）
    if script_path.suffix.lower() == '.py':
        try:
            rel_path = script_path.relative_to(scripts_dir)
            # scripts.xxx.yyy 形式
            module_path = str(rel_path.with_suffix('')).replace(os.sep, '.')
            identifiers.add(module_path)
            identifiers.add(f"scripts.{module_path}")
        except ValueError:
            pass
    
    return identifiers


def search_references_in_file(
    file_path: Path,
    identifiers: Set[str],
    check_runtime: TimeChecker = None,
) -> Dict[str, List[str]]:
    """在单个文件中搜索对脚本的引用"""
    found_refs = defaultdict(list)
    
    try:
        if check_runtime:
            check_runtime()
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        for identifier in identifiers:
            if check_runtime:
                check_runtime()
            # 构建搜索模式
            patterns = [
                # import 语句
                rf'\bimport\s+.*\b{re.escape(identifier)}\b',
                rf'\bfrom\s+.*\b{re.escape(identifier)}\b',
                # 文件名引用（字符串形式）
                rf'["\'].*{re.escape(identifier)}.*\.py["\']',
                # 命令行调用
                rf'python\s+.*{re.escape(identifier)}',
                rf'python3\s+.*{re.escape(identifier)}',
                # subprocess 调用
                rf'subprocess.*{re.escape(identifier)}',
                # 文档引用
                rf'\b{re.escape(identifier)}\.py\b',
            ]
            
            for i, line in enumerate(lines, 1):
                if check_runtime:
                    check_runtime()
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        found_refs[identifier].append(f"L{i}: {line.strip()[:100]}")
                        break
                        
    except Exception as e:
        pass
    
    return found_refs


def search_references_in_project(
    project_dir: Path, 
    scripts_dir: Path,
    script_identifiers: Dict[Path, Set[str]],
    check_runtime: TimeChecker = None,
    file_cache_path: Optional[Path] = None,
) -> Dict[Path, Dict[str, List[Tuple[Path, str]]]]:
    """在整个项目中搜索对脚本的引用"""
    
    # 需要搜索的文件扩展名
    search_extensions = {'.py', '.md', '.txt', '.yml', '.yaml', '.json', '.sh', '.ps1', '.bat', '.rst', '.toml'}
    
    # 要排除的目录
    exclude_dirs = {
        '__pycache__', 
        '.git', 
        'node_modules', 
        '.venv', 
        'venv', 
        'env',
        '.pytest_cache',
        '.mypy_cache',
        'dist',
        'build',
        '.idea',
        '.vscode',
    }
    
    docs_dir = project_dir / 'docs'
    files_to_search: List[Path] = []

    # 优先尝试读取缓存
    if file_cache_path:
        cached_files = _load_project_files_cache(file_cache_path, project_dir)
        if cached_files:
            files_to_search = cached_files
            log(f"使用文件缓存，共 {len(files_to_search)} 个候选文件")

    if not files_to_search:
        log("未命中文件缓存，开始遍历项目文件...")
        for root, dirs, files in os.walk(project_dir):
            if check_runtime:
                check_runtime()
            # 排除指定目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            root_path = Path(root)
            
            # 跳过 scripts 目录自身
            try:
                root_path.relative_to(scripts_dir)
                continue
            except ValueError:
                pass
            
            for file in files:
                file_path = root_path / file
                suffix = file_path.suffix.lower()

                # 排除 docs 目录中的 Markdown 文档
                if suffix == '.md':
                    try:
                        file_path.relative_to(docs_dir)
                        continue
                    except ValueError:
                        pass

                if suffix in search_extensions:
                    if check_runtime:
                        check_runtime()
                    files_to_search.append(file_path)

        # 保存缓存
        if file_cache_path:
            _save_project_files_cache(file_cache_path, project_dir, files_to_search)
    
    # 搜索引用
    script_references = {script: defaultdict(list) for script in script_identifiers}
    
    total_files = len(files_to_search)
    processed = 0
    start_scan = time.monotonic()

    script_path_map = {str(script): script for script in script_identifiers.keys()}
    worker_identifiers = {str(script): identifiers for script, identifiers in script_identifiers.items()}

    with ProcessPoolExecutor(max_workers=10, initializer=_init_worker, initargs=(worker_identifiers,)) as executor:
        futures = {executor.submit(_process_file_for_references, str(fp)): fp for fp in files_to_search}
        try:
            for future in as_completed(futures):
                if check_runtime:
                    check_runtime()
                processed += 1
                current_file = futures.get(future)
                percent = (processed / total_files * 100) if total_files else 100.0
                elapsed = time.monotonic() - start_scan
                avg_per_file = elapsed / processed if processed else 0
                remaining = avg_per_file * (total_files - processed)
                eta = time.strftime('%H:%M:%S', time.gmtime(elapsed + remaining))
                current_desc = str(current_file.relative_to(project_dir)) if current_file else "<unknown>"
                log(f"[扫描进度] {processed}/{total_files} 文件 ({percent:.1f}%)，最近完成: {current_desc}，已用 {elapsed:.1f}s，预计完成时间 {eta}")
                print(f"\r    处理进度: {processed}/{total_files} 文件 ({percent:.1f}%)，当前: {current_desc}", end='', flush=True)

                try:
                    results = future.result()
                    for script_key, identifier, file_path_str, loc in results:
                        script = script_path_map.get(script_key)
                        if script is None:
                            continue
                        file_path = Path(file_path_str)
                        script_references[script][identifier].append((file_path, loc))
                except AnalysisTimeoutError:
                    for f in futures:
                        f.cancel()
                    raise
                except Exception:
                    pass
        finally:
            for future in futures:
                future.cancel()

    print()  # 换行
    return script_references


def _make_time_checker(start_time: float, max_seconds: Optional[int]) -> Callable[[], None]:
    if max_seconds is None or max_seconds <= 0:
        def no_op() -> None:
            return None
        return no_op

    def check():
        elapsed = time.monotonic() - start_time
        if elapsed > max_seconds:
            raise AnalysisTimeoutError(f"运行已超过 {max_seconds} 秒，终止分析")

    return check


def analyze_unused_scripts(
    project_root: str = None,
    max_runtime_seconds: int = MAX_RUNTIME_SECONDS,
    script_filter: Optional[str] = None,
    log_file: Optional[str] = None,
    mode: str = ALL_MODE,
):
    """主分析函数"""
    
    start_time = time.monotonic()

    if project_root is None:
        # 获取项目根目录
        project_root = Path(__file__).parent.parent
    else:
        project_root = Path(project_root)
    
    scripts_dir = project_root / 'scripts'
    mode = (mode or ALL_MODE).lower()
    if mode not in {ALL_MODE, SINGLE_MODE}:
        raise ValueError(f"未知检测模式: {mode}，可选值: {ALL_MODE}/{SINGLE_MODE}")
    if mode == ALL_MODE:
        # 批量模式允许长时间运行，禁用超时检查
        time_checker = _make_time_checker(start_time, None)
        log("批量模式: 已禁用 60 秒超时限制，直到分析完成才结束")
    else:
        time_checker = _make_time_checker(start_time, max_runtime_seconds)

    state_path = scripts_dir / DEFAULT_STATE_FILENAME
    unused_state_path = scripts_dir / DEFAULT_UNUSED_STATE_FILENAME
    # 确保两个状态文件都存在
    _ensure_state_file(state_path)
    _ensure_unused_state_file(unused_state_path)

    # 组装日志文件路径
    if log_file:
        log_path = Path(log_file)
    else:
        log_path = scripts_dir / DEFAULT_LOG_FILENAME
    _configure_logger(log_path)
    
    log("=" * 80)
    log("Scripts 文件夹未使用脚本分析")
    log("=" * 80)
    log(f"项目根目录: {project_root}")
    log(f"Scripts 目录: {scripts_dir}")
    log(f"日志写入: {log_path}")
    log(f"检测模式: {mode}")
    log(f"分析的脚本类型: {', '.join(SCRIPT_EXTENSIONS)}")
    
    # 1. 获取所有脚本
    log("[1/4] 扫描 scripts 目录中的脚本文件...")
    all_scripts = get_all_scripts(scripts_dir, time_checker)
    time_checker()
    
    # 加载已记录的脚本状态
    used_script_records = _load_used_scripts_state(state_path)
    unused_script_records = _load_unused_scripts_state(unused_state_path)
    already_analyzed = used_script_records | unused_script_records
    log(f"已记录为【已使用】的脚本: {len(used_script_records)} 个")
    log(f"已记录为【未使用】的脚本: {len(unused_script_records)} 个")

    
    # 按类型统计
    ext_count = defaultdict(int)
    for s in all_scripts:
        ext_count[s.suffix.lower()] += 1
    log(f"找到 {len(all_scripts)} 个脚本文件")
    for ext, count in sorted(ext_count.items()):
        log(f"  - {ext}: {count} 个")
    
    # 过滤掉已经分析过的脚本
    scripts_to_analyze = []
    for script in all_scripts:
        rel = str(script.relative_to(scripts_dir)).replace('\\', '/')
        if rel not in already_analyzed:
            scripts_to_analyze.append(script)
    
    log(f"需要分析的脚本: {len(scripts_to_analyze)} 个（跳过已记录的 {len(already_analyzed)} 个）")
    
    selected_script_path: Optional[Path] = None

    # SINGLE 模式且未指定脚本时，从未分析的脚本中选择
    if mode == SINGLE_MODE and not script_filter:
        if not scripts_to_analyze:
            log("所有脚本都已分析完成！")
            return {
                'total': len(all_scripts),
                'used': len(used_script_records),
                'unused': len(unused_script_records),
                'unused_scripts': list(unused_script_records),
                'used_scripts': list(used_script_records),
            }
        selected_script_path = random.choice(scripts_to_analyze)
        script_filter = str(selected_script_path.relative_to(scripts_dir)).replace('\\', '/')
        log(f"随机选择脚本进行检测: {script_filter}")

    # 仅分析指定脚本
    if script_filter:
        normalized = script_filter.replace('\\', '/').strip()
        log(f"仅分析指定脚本: {normalized}")
        matched_scripts = []
        for script in all_scripts:
            time_checker()
            rel = str(script.relative_to(scripts_dir)).replace('\\', '/')
            if rel == normalized or script.name == normalized or script.stem == normalized:
                matched_scripts.append(script)
        if not matched_scripts:
            raise FileNotFoundError(f"未在 scripts 目录中找到脚本: {script_filter}")
        if len(matched_scripts) > 1:
            choices = ', '.join(str(s.relative_to(scripts_dir)) for s in matched_scripts)
            raise ValueError(f"找到多个匹配脚本 ({choices})，请使用相对路径精确指定")
        scripts_to_analyze = matched_scripts
        selected_script_path = scripts_to_analyze[0]
        log(f"匹配脚本: {selected_script_path.relative_to(scripts_dir)}")

    # 准备文件缓存
    file_cache_path = scripts_dir / DEFAULT_FILE_CACHE
    
    # 加载项目文件列表（只加载一次）
    log("[2/4] 加载项目文件列表...")
    cached_files = _load_project_files_cache(file_cache_path, project_root)
    if not cached_files:
        log("未命中文件缓存，开始扫描项目文件...")
        cached_files = _scan_project_files(project_root, scripts_dir, time_checker)
        _save_project_files_cache(file_cache_path, project_root, cached_files)
    log(f"项目文件总数: {len(cached_files)} 个")
    
    # 3. 逐个分析脚本
    total_scripts = len(scripts_to_analyze)
    log(f"[3/4] 开始逐个分析脚本 (共 {total_scripts} 个)...")
    
    used_scripts = []
    unused_scripts = []
    
    for script_idx, script in enumerate(scripts_to_analyze, 1):
        time_checker()
        rel_path = str(script.relative_to(scripts_dir)).replace('\\', '/')
        
        # 显示总体进度
        progress_pct = (script_idx / total_scripts * 100) if total_scripts else 100
        log(f"")
        log(f"{'='*60}")
        log(f"[脚本进度] {script_idx}/{total_scripts} ({progress_pct:.1f}%) - 正在分析: {rel_path}")
        log(f"{'='*60}")
        print(f"\n>>> [{script_idx}/{total_scripts}] 分析脚本: {rel_path}")
        
        # 生成标识符
        identifiers = get_script_identifiers(script, scripts_dir)
        log(f"  标识符: {identifiers}")
        
        # 在项目文件中搜索引用
        script_refs = _search_single_script_references(
            script, identifiers, cached_files, project_root, time_checker
        )
        
        # 判断是否被使用
        is_used = any(script_refs.values())
        
        if is_used:
            used_scripts.append((script, script_refs))
            # 立即保存到 used 记录
            used_script_records.add(rel_path)
            _save_used_scripts_state(state_path, used_script_records)
            ref_count = sum(len(locs) for locs in script_refs.values())
            log(f"  [已使用] ({ref_count} 处引用) -> 已记录到 {state_path.name}")
            print(f"    [+] 已使用 ({ref_count} 处引用)")
        else:
            unused_scripts.append(script)
            # 立即保存到 unused 记录
            unused_script_records.add(rel_path)
            _save_unused_scripts_state(unused_state_path, unused_script_records)
            log(f"  [未使用] -> 已记录到 {unused_state_path.name}")
            print(f"    [-] 未使用")
    
    time_checker()
    
    # 4. 汇总结果
    log(f"")
    log("[4/4] 分析完成，汇总结果...")
    
    # 按子目录分组
    def get_relative_path(script: Path) -> str:
        try:
            return str(script.relative_to(scripts_dir))
        except ValueError:
            return str(script)
    
    # 输出结果
    print("\n" + "=" * 80)
    print("分析结果")
    print("=" * 80)
    
    log(f"总脚本数: {len(all_scripts)}")
    log(f"被引用的脚本: {len(used_scripts)}")
    log(f"未被引用的脚本: {len(unused_scripts)}")
    
    # 按目录分组未使用的脚本
    unused_by_dir = defaultdict(list)
    for script in unused_scripts:
        rel_path = get_relative_path(script)
        if os.sep in rel_path or '/' in rel_path:
            dir_name = rel_path.split(os.sep)[0] if os.sep in rel_path else rel_path.split('/')[0]
        else:
            dir_name = '(根目录)'
        unused_by_dir[dir_name].append(rel_path)
    
    print("\n" + "-" * 80)
    print("未被引用的脚本列表（按目录分组）:")
    print("-" * 80)
    
    for dir_name in sorted(unused_by_dir.keys()):
        scripts = unused_by_dir[dir_name]
        print(f"\n## {dir_name} ({len(scripts)} 个)")
        for script in sorted(scripts):
            print(f"    - {script}")
    
    # 输出被使用的脚本（可选）
    print("\n" + "-" * 80)
    print("被引用的脚本列表:")
    print("-" * 80)
    
    for script, refs in sorted(used_scripts, key=lambda x: get_relative_path(x[0])):
        rel_path = get_relative_path(script)
        ref_count = sum(len(locs) for locs in refs.values())
        print(f"\n## {rel_path} ({ref_count} 处引用)")
        for identifier, locations in refs.items():
            for file_path, loc in locations:
                try:
                    ref_file = file_path.relative_to(project_root)
                except ValueError:
                    ref_file = file_path
                print(f"    - [{identifier}] {ref_file}: {loc}")
    
    # 生成报告内容
    timestamp = __import__('datetime').datetime.now()
    report_lines: List[str] = []
    report_lines.append("Scripts 文件夹未使用脚本分析报告")
    report_lines.append("=" * 80)
    report_lines.append("")
    report_lines.append(f"生成时间: {timestamp}")
    report_lines.append(f"项目根目录: {project_root}")
    report_lines.append(f"Scripts 目录: {scripts_dir}")
    report_lines.append("")
    report_lines.append(f"总脚本数: {len(all_scripts)}")
    report_lines.append(f"被引用的脚本: {len(used_scripts)}")
    report_lines.append(f"未被引用的脚本: {len(unused_scripts)}")
    report_lines.append("")
    report_lines.append("-" * 80)
    report_lines.append("未被引用的脚本列表:")
    report_lines.append("-" * 80)
    report_lines.append("")
    for dir_name in sorted(unused_by_dir.keys()):
        scripts = unused_by_dir[dir_name]
        report_lines.append(f"## {dir_name} ({len(scripts)} 个)")
        for script in sorted(scripts):
            report_lines.append(f"    {script}")
        report_lines.append("")
    report_lines.append("-" * 80)
    report_lines.append("被引用的脚本列表:")
    report_lines.append("-" * 80)
    report_lines.append("")
    for script, refs in sorted(used_scripts, key=lambda x: get_relative_path(x[0])):
        rel_path = get_relative_path(script)
        ref_count = sum(len(locs) for locs in refs.values())
        report_lines.append(f"{rel_path} ({ref_count} 处引用)")
        for identifier, locations in refs.items():
            for file_path, loc in locations:
                try:
                    ref_file = file_path.relative_to(project_root)
                except ValueError:
                    ref_file = file_path
                report_lines.append(f"    [{identifier}] {ref_file}: {loc}")
        report_lines.append("")

    # 同步写入日志
    log("分析报告内容（同步写入日志）:")
    for line in report_lines:
        log(line)

    log("分析报告仅写入日志（不再生成 scripts/unused_scripts_report.txt）")
    log(f"日志已保存到: {log_path}")

    # 输出最终统计
    log(f"")
    log(f"{'='*60}")
    log(f"本次分析完成！")
    log(f"  - 本次分析脚本数: {len(scripts_to_analyze)}")
    log(f"  - 本次发现已使用: {len(used_scripts)}")
    log(f"  - 本次发现未使用: {len(unused_scripts)}")
    log(f"  - 累计已使用记录: {len(used_script_records)}")
    log(f"  - 累计未使用记录: {len(unused_script_records)}")
    log(f"{'='*60}")

    return {
        'total': len(all_scripts),
        'used': len(used_scripts),
        'unused': len(unused_scripts),
        'unused_scripts': [get_relative_path(s) for s in unused_scripts],
        'used_scripts': [get_relative_path(s) for s, _ in used_scripts],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='分析 scripts 目录中的未使用脚本')
    parser.add_argument('--project-root', type=str, default=None, help='项目根目录（默认：脚本上级目录）')
    parser.add_argument('--script', type=str, default=None, help='仅分析指定脚本（支持文件名/相对路径）')
    parser.add_argument('--max-seconds', type=int, default=MAX_RUNTIME_SECONDS, help='运行超时时间（秒）')
    parser.add_argument('--log-file', type=str, default=None, help='日志文件路径（默认：scripts/analyze_unused_scripts.log）')
    parser.add_argument('--mode', type=str, default=ALL_MODE, choices=[ALL_MODE, SINGLE_MODE], help='检测模式：all（全部）或 single（随机单个）')
    args = parser.parse_args()

    try:
        result = analyze_unused_scripts(
            project_root=args.project_root,
            max_runtime_seconds=args.max_seconds,
            script_filter=args.script,
            log_file=args.log_file,
            mode=args.mode,
        )
    except AnalysisTimeoutError as exc:
        log(str(exc), logging.ERROR)
        sys.exit(1)
    
    print("\n\n" + "=" * 80)
    print("摘要")
    print("=" * 80)
    print(f"未使用脚本占比: {result['unused'] / result['total'] * 100:.1f}%")
