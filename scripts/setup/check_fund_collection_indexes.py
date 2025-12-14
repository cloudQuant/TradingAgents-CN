#!/usr/bin/env python3
"""
检查并修复基金（funds）相关 MongoDB 集合的唯一索引脚本

设计目标：
- 只关注 funds 模块中的集合（即由 fund providers 定义的集合）
- 对每个集合：
  - 读取 provider 中声明的 unique_keys
  - 检查 MongoDB 中是否已经存在「字段顺序完全一致、并且 unique=True」的联合索引
  - 如果已经存在，则跳过
  - 如果不存在，则创建对应的联合唯一索引
- 不会删除任何已有索引，只做“补充”和“修复缺失”的工作

用法（在项目根目录执行）：

  python scripts/setup/check_fund_collection_indexes.py

也支持通过环境变量配置 MongoDB 连接信息（与其他脚本保持一致）：

  MONGODB_HOST / MONGODB_PORT / MONGODB_DATABASE / MONGODB_USERNAME / MONGODB_PASSWORD / MONGODB_AUTH_SOURCE
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List, Tuple

from pymongo import MongoClient, ASCENDING

# ---------------------------------------------------------------------------
# 确保可以从项目根目录导入 app 包
# ---------------------------------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]  # .../云子量化
if str(PROJECT_ROOT) not in sys.path:
  sys.path.insert(0, str(PROJECT_ROOT))

# 依赖应用内部的 provider 注册机制
from app.services.data_sources.funds.provider_registry import get_registered_fund_providers
from app.services.data_sources.base_provider import BaseProvider


def build_mongo_uri() -> str:
  """根据环境变量构造 MongoDB 连接 URI（与 init_mongodb_indexes 脚本保持风格一致）"""
  host = os.getenv("MONGODB_HOST", "localhost")
  port = int(os.getenv("MONGODB_PORT", "27017"))
  db = os.getenv("MONGODB_DATABASE", "tradingagents")
  user = os.getenv("MONGODB_USERNAME", "")
  pwd = os.getenv("MONGODB_PASSWORD", "")
  auth_src = os.getenv("MONGODB_AUTH_SOURCE", "admin")

  if user and pwd:
    return f"mongodb://{user}:{pwd}@{host}:{port}/{db}?authSource={auth_src}"
  return f"mongodb://{host}:{port}/{db}"


def index_matches_unique_keys(
  index_def: dict,
  unique_keys: List[str],
) -> bool:
  """
  判断一个现有索引是否与目标 unique_keys 完全一致（字段及顺序相同，且 unique=True）
  """
  if not index_def.get("unique"):
    return False

  index_keys: List[Tuple[str, int]] = index_def.get("key", [])
  target_keys: List[Tuple[str, int]] = [(field, ASCENDING) for field in unique_keys]

  if len(index_keys) != len(target_keys):
    return False

  for (ik, iv), (tk, tv) in zip(index_keys, target_keys):
    if ik != tk or iv != tv:
      return False

  return True


def ensure_unique_index_for_collection(db, provider_cls: type[BaseProvider]) -> None:
  """
  确保某个基金集合的唯一索引存在且字段与 provider.unique_keys 一致
  """
  collection_name = getattr(provider_cls, "collection_name", "") or provider_cls.collection_name
  unique_keys: List[str] = getattr(provider_cls, "unique_keys", []) or provider_cls().get_unique_keys()

  if not collection_name:
    print("⚠️  跳过一个未定义 collection_name 的 Provider:", provider_cls.__name__)
    return

  if not unique_keys:
    # 没有声明 unique_keys 的集合直接忽略
    print(f"ℹ️  集合 {collection_name} 未配置 unique_keys，跳过")
    return

  coll = db[collection_name]

  try:
    index_info = coll.index_information()
  except Exception as e:
    print(f"❌ 无法获取集合 {collection_name} 的索引信息: {e}")
    return

  # 检查是否已有完全匹配的唯一索引
  for name, info in index_info.items():
    if index_matches_unique_keys(info, unique_keys):
      print(f"✅ 集合 {collection_name} 已存在匹配的唯一索引: {name} -> {unique_keys}")
      return

  # 没有找到匹配的唯一索引，则创建一个新的
  index_name = f"uniq_{collection_name}_" + "_".join(unique_keys)
  index_keys = [(field, ASCENDING) for field in unique_keys]

  try:
    coll.create_index(index_keys, unique=True, name=index_name)
    print(f"🛠️  为集合 {collection_name} 创建唯一索引 {index_name}: {unique_keys}")
  except Exception as e:
    print(f"❌ 为集合 {collection_name} 创建唯一索引失败: {e}")


def main() -> None:
  uri = build_mongo_uri()
  dbname = os.getenv("MONGODB_DATABASE", "tradingagents")

  print(f"🔗 连接 MongoDB: {uri}")
  client = MongoClient(uri)
  db = client[dbname]

  print("🔍 扫描基金 Provider 列表...")
  providers = get_registered_fund_providers()
  print(f"✅ 共发现 {len(providers)} 个基金 Provider")

  for provider_cls in providers:
    ensure_unique_index_for_collection(db, provider_cls)

  print("🎉 基金集合唯一索引检查/修复完成")


if __name__ == "__main__":
  main()


