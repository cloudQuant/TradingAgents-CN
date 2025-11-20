"""
验证 bond_info_cm 远程同步功能

检查以下内容：
1. 后端 bonds 路由已新增 /collections/{collection_name}/sync-remote 接口，并包含远程连接参数
   （包括远程主机、数据库类型、批量大小、远程集合名、远程用户名和密码等）
2. BondDataService 中新增远程同步方法
3. 前端 bondsApi 中已新增 syncCollectionFromRemote 方法，调用上述接口
4. 前端 Bonds Collection 页面更新数据对话框中已添加远程同步区域和按钮
"""

import os
import re
import sys


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main() -> None:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

    print("=" * 70)
    print("验证 bond_info_cm 远程同步功能")
    print("=" * 70)

    # 1. 检查后端路由
    print("\n[检查1] 验证后端 bonds 路由远程同步接口")
    bonds_router_path = os.path.join(root_dir, "app", "routers", "bonds.py")
    if not os.path.exists(bonds_router_path):
        print(f"  [FAILED] 找不到 bonds 路由文件: {bonds_router_path}")
        sys.exit(1)

    router_content = _read_file(bonds_router_path)

    sync_marker = '@router.post("/collections/{collection_name}/sync-remote")'
    pos = router_content.find(sync_marker)
    if pos < 0:
        print("  [FAILED] 找不到 /collections/{collection_name}/sync-remote 路由定义")
        sys.exit(1)

    print("  [OK] 找到 collections sync-remote 路由装饰器")

    snippet = router_content[pos : pos + 3000]

    if "def sync_collection_from_remote" not in snippet:
        print("  [FAILED] sync_collection_from_remote 函数未找到")
        sys.exit(1)

    required_params = [
        "remote_host",
        "db_type",
        "batch_size",
        "remote_collection",
        "remote_username",
        "remote_password",
    ]
    missing_params = [p for p in required_params if p not in snippet]
    if missing_params:
        print(f"  [FAILED] sync_collection_from_remote 缺少参数: {', '.join(missing_params)}")
        sys.exit(1)
    else:
        print(f"  [OK] sync_collection_from_remote 包含参数: {', '.join(required_params)}")

    # 1.2 检查服务层方法
    print("\n[检查2] 验证 BondDataService 远程同步方法")
    service_path = os.path.join(root_dir, "app", "services", "bond_data_service.py")
    if not os.path.exists(service_path):
        print(f"  [FAILED] 找不到 BondDataService 文件: {service_path}")
        sys.exit(1)

    service_content = _read_file(service_path)

    if "async def sync_collection_from_remote_mongo" in service_content:
        print("  [OK] 找到 BondDataService.sync_collection_from_remote_mongo 方法")
    else:
        print("  [FAILED] 未找到 BondDataService.sync_collection_from_remote_mongo 方法")
        sys.exit(1)

    # 2. 检查前端 bondsApi
    print("\n[检查3] 验证前端 bondsApi.syncCollectionFromRemote 方法")
    bonds_api_path = os.path.join(root_dir, "frontend", "src", "api", "bonds.ts")
    if not os.path.exists(bonds_api_path):
        print(f"  [FAILED] 找不到前端 bonds API 文件: {bonds_api_path}")
        sys.exit(1)

    api_content = _read_file(bonds_api_path)

    if "syncCollectionFromRemote" not in api_content:
        print("  [FAILED] bondsApi 中未找到 syncCollectionFromRemote 方法")
        sys.exit(1)

    if "/api/bonds/collections/" in api_content and "/sync-remote" in api_content:
        print("  [OK] syncCollectionFromRemote 使用 /api/bonds/collections/{collectionName}/sync-remote 路径")
    else:
        print("  [WARN] syncCollectionFromRemote 的请求路径可能不符合预期，请人工检查")

    # 3. 检查前端 Collection.vue 中的远程同步区域
    print("\n[检查4] 验证 Bonds Collection 页面远程同步区域")
    collection_view_path = os.path.join(root_dir, "frontend", "src", "views", "Bonds", "Collection.vue")
    if not os.path.exists(collection_view_path):
        print(f"  [FAILED] 找不到 Bonds Collection 视图文件: {collection_view_path}")
        sys.exit(1)

    view_content = _read_file(collection_view_path)

    # 3.1 检查模板中是否包含“远程同步”字段/按钮
    if "远程同步" in view_content and "remoteSyncHost" in view_content:
        print("  [OK] Collection.vue 中存在远程同步相关表单/文案")
    else:
        print("  [FAILED] 未在 Collection.vue 中找到远程同步相关表单/文案")
        sys.exit(1)

    # 3.2 检查脚本中是否有远程同步处理函数
    handler_checks = [
        "remoteSyncHost",
        "remoteSyncDbType",
        "remoteSyncBatchSize",
        "remoteSyncCollection",
        "remoteSyncUsername",
        "remoteSyncPassword",
        "handleRemoteSync",
    ]
    missing_handlers = [h for h in handler_checks if h not in view_content]
    if missing_handlers:
        print(f"  [FAILED] Collection.vue 中缺少远程同步相关状态/方法: {', '.join(missing_handlers)}")
        sys.exit(1)
    else:
        print("  [OK] Collection.vue 中已实现远程同步相关状态和处理函数")

    print("\n" + "=" * 70)
    print("[SUCCESS] bond_info_cm 远程同步功能相关代码检查通过（或存在仅警告项）")
    print("=" * 70)


if __name__ == "__main__":
    main()
