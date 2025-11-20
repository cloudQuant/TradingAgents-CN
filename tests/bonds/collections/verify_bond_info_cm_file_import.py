"""
验证 bond_info_cm CSV/Excel 文件导入功能

检查以下内容：
1. 后端 bonds 路由已新增 /collections/{collection_name}/import 接口，并使用 UploadFile 接收文件
2. 前端 bondsApi 中已新增 importCollectionData 方法，调用上述接口
3. 前端 Bonds Collection 页面更新数据对话框中已添加文件上传区域和导入按钮
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
    print("验证 bond_info_cm 文件导入功能")
    print("=" * 70)

    # 1. 检查后端路由
    print("\n[检查1] 验证后端 bonds 路由导入接口")
    bonds_router_path = os.path.join(root_dir, "app", "routers", "bonds.py")
    if not os.path.exists(bonds_router_path):
        print(f"  [FAILED] 找不到 bonds 路由文件: {bonds_router_path}")
        sys.exit(1)

    router_content = _read_file(bonds_router_path)

    # 1.1 确认导入 UploadFile, File
    if "UploadFile" in router_content and "File(" in router_content:
        print("  [OK] 已导入 UploadFile 和 File")
    else:
        print("  [FAILED] bonds.py 未导入 UploadFile 或 File（需要用于文件上传）")
        sys.exit(1)

    # 1.2 确认存在 import 接口装饰器
    import_marker = '@router.post("/collections/{collection_name}/import")'
    pos = router_content.find(import_marker)
    if pos < 0:
        print("  [FAILED] 找不到 /collections/{collection_name}/import 路由定义")
        sys.exit(1)

    print("  [OK] 找到 collections import 路由装饰器")

    snippet = router_content[pos : pos + 2500]

    # 1.3 检查函数签名中包含 UploadFile 参数
    if "def import_collection_data" not in snippet:
        print("  [FAILED] import_collection_data 函数未找到")
        sys.exit(1)

    if "file: UploadFile = File(" in snippet:
        print("  [OK] import_collection_data 使用 UploadFile = File(...) 接收文件")
    else:
        print("  [FAILED] import_collection_data 未正确使用 UploadFile = File(...)")
        sys.exit(1)

    # 1.4 简单检查实现中提到 bond_info_cm
    if "bond_info_cm" in snippet:
        print("  [OK] 导入接口中包含 bond_info_cm 处理逻辑")
    else:
        print("  [WARN] 导入接口中未显式出现 bond_info_cm，请确认逻辑是否覆盖该集合")

    # 2. 检查前端 bondsApi
    print("\n[检查2] 验证前端 bondsApi.importCollectionData 方法")
    bonds_api_path = os.path.join(root_dir, "frontend", "src", "api", "bonds.ts")
    if not os.path.exists(bonds_api_path):
        print(f"  [FAILED] 找不到前端 bonds API 文件: {bonds_api_path}")
        sys.exit(1)

    api_content = _read_file(bonds_api_path)

    if "importCollectionData" not in api_content:
        print("  [FAILED] bondsApi 中未找到 importCollectionData 方法")
        sys.exit(1)

    # 粗略检查请求路径
    if "/api/bonds/collections/" in api_content and "/import" in api_content:
        print("  [OK] importCollectionData 使用 /api/bonds/collections/{collectionName}/import 路径")
    else:
        print("  [WARN] importCollectionData 的请求路径可能不符合预期，请人工检查")

    # 3. 检查前端 Collection.vue 中的上传区域
    print("\n[检查3] 验证 Bonds Collection 页面文件上传区域")
    collection_view_path = os.path.join(root_dir, "frontend", "src", "views", "Bonds", "Collection.vue")
    if not os.path.exists(collection_view_path):
        print(f"  [FAILED] 找不到 Bonds Collection 视图文件: {collection_view_path}")
        sys.exit(1)

    view_content = _read_file(collection_view_path)

    # 3.1 检查模板中是否包含 el-upload 且与 bond_info_cm 条件相关
    if "<el-upload" in view_content and "bond_info_cm" in view_content:
        print("  [OK] Collection.vue 中存在针对 bond_info_cm 的 el-upload 上传区域")
    else:
        print("  [FAILED] 未在 Collection.vue 中找到针对 bond_info_cm 的文件上传区域")
        sys.exit(1)

    # 3.2 检查脚本中是否有导入相关处理函数
    handler_checks = [
        "handleImportFile",
        "handleImportFileChange",
        "handleImportFileRemove",
    ]
    missing_handlers = [h for h in handler_checks if h not in view_content]
    if missing_handlers:
        print(f"  [FAILED] Collection.vue 中缺少处理函数: {', '.join(missing_handlers)}")
        sys.exit(1)
    else:
        print("  [OK] Collection.vue 中已实现文件导入相关处理函数")

    # 3.3 检查上传组件是否支持多文件
    upload_item_marker = "<el-form-item v-if=\"collectionName === 'bond_info_cm'\" label=\"文件导入\""
    upload_start = view_content.find(upload_item_marker)
    if upload_start >= 0:
        upload_end = view_content.find("</el-form-item>", upload_start)
        upload_section = view_content[upload_start:upload_end if upload_end > upload_start else None]
    else:
        upload_section = ""

    if "multiple" in upload_section:
        print("  [OK] el-upload 已启用多文件选择")
    else:
        print("  [FAILED] el-upload 未启用多文件选择（需要支持多文件导入）")
        sys.exit(1)

    # 4. 检查导入成功后是否关闭对话框
    if "handleImportFile" in view_content:
        idx = view_content.find("const handleImportFile")
        snippet2 = view_content[idx : idx + 1500] if idx >= 0 else ""
        if "refreshDialogVisible.value = false" in snippet2 or "refreshDialogVisible.value=false" in snippet2:
            print("  [OK] 导入成功后包含关闭更新对话框的逻辑")
        else:
            print("  [FAILED] 未在导入处理逻辑中找到关闭更新对话框的代码")
            sys.exit(1)

    print("\n" + "=" * 70)
    print("[SUCCESS] bond_info_cm 文件导入功能相关代码检查通过（或存在仅警告项）")
    print("=" * 70)


if __name__ == "__main__":
    main()
