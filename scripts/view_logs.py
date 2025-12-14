#!/usr/bin/env python3
"""
日志查看工具 - 美化显示日志内容
"""
import sys
import re
from pathlib import Path
import argparse
from datetime import datetime, timedelta


def colorize_level(level):
    """为日志级别添加颜色"""
    colors = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
    }
    reset = '\033[0m'
    return f"{colors.get(level, '')}{level}{reset}"


def colorize_module(module):
    """为模块名添加颜色"""
    if 'error' in module.lower():
        return f"\033[31m{module}\033[0m"  # 红色
    elif 'webapi' in module.lower():
        return f"\033[34m{module}\033[0m"  # 蓝色
    elif 'app' in module.lower():
        return f"\033[32m{module}\033[0m"  # 绿色
    else:
        return f"\033[37m{module}\033[0m"  # 白色


def parse_log_line(line):
    """解析日志行"""
    # 匹配格式: 时间 | 模块 | 级别 | 消息 | trace=xxx
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| trace=([^|]*)'
    match = re.match(pattern, line.strip())
    
    if match:
        timestamp, module, level, message, trace_id = match.groups()
        return {
            'timestamp': timestamp.strip(),
            'module': module.strip(),
            'level': level.strip(),
            'message': message.strip(),
            'trace_id': trace_id.strip(),
            'raw': line
        }
    return None


def format_log_entry(entry, colorize=True):
    """格式化日志条目"""
    if not entry:
        return ""
    
    timestamp = entry['timestamp']
    module = colorize_module(entry['module']) if colorize else entry['module']
    level = colorize_level(entry['level']) if colorize else entry['level']
    message = entry['message']
    trace_id = entry['trace_id']
    
    # 格式化输出
    if trace_id and trace_id != '-':
        trace_part = f" 🔗 {trace_id[:8]}..."
    else:
        trace_part = ""
    
    return f"{timestamp} | {module:<25} | {level:<7} | {message}{trace_part}"


def filter_logs(lines, level_filter=None, module_filter=None, time_filter=None):
    """过滤日志"""
    filtered = []
    
    for line in lines:
        entry = parse_log_line(line)
        if not entry:
            continue
        
        # 级别过滤
        if level_filter and entry['level'] not in level_filter:
            continue
        
        # 模块过滤
        if module_filter and not any(mod in entry['module'] for mod in module_filter):
            continue
        
        # 时间过滤
        if time_filter:
            try:
                log_time = datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S')
                if log_time < time_filter:
                    continue
            except:
                pass
        
        filtered.append(entry)
    
    return filtered


def main():
    parser = argparse.ArgumentParser(description='查看和分析TradingAgents日志')
    parser.add_argument('--file', '-f', default='backend.log', help='日志文件路径')
    parser.add_argument('--lines', '-n', type=int, default=50, help='显示行数')
    parser.add_argument('--level', '-l', nargs='+', help='过滤日志级别 (DEBUG, INFO, WARNING, ERROR)')
    parser.add_argument('--module', '-m', nargs='+', help='过滤模块名')
    parser.add_argument('--since', '-s', help='显示指定时间之后的日志 (如: 10m, 1h, 2d)')
    parser.add_argument('--follow', action='store_true', help='实时跟踪日志')
    parser.add_argument('--no-color', action='store_true', help='禁用颜色输出')
    parser.add_argument('--stats', action='store_true', help='显示日志统计信息')
    
    args = parser.parse_args()
    
    log_file = Path(args.file)
    if not log_file.exists():
        print(f"❌ 日志文件不存在: {log_file}")
        sys.exit(1)
    
    # 解析时间过滤器
    time_filter = None
    if args.since:
        try:
            if args.since.endswith('m'):
                minutes = int(args.since[:-1])
                time_filter = datetime.now() - timedelta(minutes=minutes)
            elif args.since.endswith('h'):
                hours = int(args.since[:-1])
                time_filter = datetime.now() - timedelta(hours=hours)
            elif args.since.endswith('d'):
                days = int(args.since[:-1])
                time_filter = datetime.now() - timedelta(days=days)
        except:
            print(f"❌ 无效的时间格式: {args.since}")
            sys.exit(1)
    
    # 读取日志文件
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ 读取日志文件失败: {e}")
        sys.exit(1)
    
    # 获取最后N行
    if args.lines > 0:
        lines = lines[-args.lines:]
    
    # 过滤日志
    entries = filter_logs(lines, args.level, args.module, time_filter)
    
    if args.stats:
        # 显示统计信息
        level_counts = {}
        module_counts = {}
        
        for entry in entries:
            level_counts[entry['level']] = level_counts.get(entry['level'], 0) + 1
            module_counts[entry['module']] = module_counts.get(entry['module'], 0) + 1
        
        print("📊 日志统计信息")
        print("=" * 50)
        print("📈 按级别统计:")
        for level, count in sorted(level_counts.items()):
            print(f"  {level:<10}: {count:>5}")
        
        print("\n📈 按模块统计 (前10):")
        for module, count in sorted(module_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {module:<25}: {count:>5}")
        
        print(f"\n📊 总计: {len(entries)} 条日志")
        return
    
    # 显示日志
    colorize = not args.no_color
    print(f"📋 显示日志: {log_file} (最近 {len(entries)} 条)")
    print("=" * 80)
    
    for entry in entries:
        print(format_log_entry(entry, colorize))
    
    if args.follow:
        print("\n👀 实时跟踪日志 (Ctrl+C 退出)...")
        try:
            import time
            with open(log_file, 'r', encoding='utf-8') as f:
                f.seek(0, 2)  # 移到文件末尾
                while True:
                    line = f.readline()
                    if line:
                        entry = parse_log_line(line)
                        if entry:
                            print(format_log_entry(entry, colorize))
                    else:
                        time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n👋 停止跟踪")


if __name__ == '__main__':
    main()