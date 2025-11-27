"""
通用集合导出服务
用于将 MongoDB 集合数据导出为 CSV/Excel/JSON 格式
"""

import io
import logging
import time
from typing import Any, Dict, Optional

import pandas as pd
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger("webapi")


class CollectionExportService:
    """通用集合导出服务类"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def export_to_file(
        self,
        collection_name: str,
        file_format: str = "csv",
        filters: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """
        导出集合数据到文件

        Args:
            collection_name: 集合名称
            file_format: 文件格式 ('csv', 'xlsx', 'json')
            filters: 查询过滤条件

        Returns:
            文件内容（字节）
        """
        t0 = time.perf_counter()
        try:
            collection = self.db.get_collection(collection_name)

            # 查询数据 - 使用 projection 排除 _id 字段
            query = filters or {}
            cursor = collection.find(query, {"_id": 0})
            data = await cursor.to_list(length=None)
            t1 = time.perf_counter()
            logger.info(
                f"[导出] MongoDB 查询完成: {len(data)} 条, 耗时 {t1-t0:.2f}s"
            )

            if not data:
                raise ValueError("没有数据可导出")

            # 转换为DataFrame
            df = pd.DataFrame(data)
            t2 = time.perf_counter()
            logger.info(f"[导出] DataFrame 创建完成, 耗时 {t2-t1:.2f}s")

            # 根据格式导出
            normalized_format = file_format.lower()

            if normalized_format == "csv":
                result = df.to_csv(index=False).encode("utf-8-sig")
                t3 = time.perf_counter()
                logger.info(
                    f"[导出] CSV 生成完成, 耗时 {t3-t2:.2f}s, 总耗时 {t3-t0:.2f}s"
                )
                return result
            elif normalized_format in ("excel", "xlsx"):
                output = io.BytesIO()
                # 使用 xlsxwriter 引擎，比 openpyxl 快 5-10 倍
                df.to_excel(output, index=False, engine="xlsxwriter")
                result = output.getvalue()
                t3 = time.perf_counter()
                logger.info(
                    f"[导出] Excel 生成完成, 耗时 {t3-t2:.2f}s, 总耗时 {t3-t0:.2f}s"
                )
                return result
            elif normalized_format == "json":
                result = df.to_json(orient="records", force_ascii=False).encode(
                    "utf-8"
                )
                t3 = time.perf_counter()
                logger.info(
                    f"[导出] JSON 生成完成, 耗时 {t3-t2:.2f}s, 总耗时 {t3-t0:.2f}s"
                )
                return result
            else:
                raise ValueError(f"不支持的文件格式: {file_format}")

        except Exception as e:
            logger.error(f"导出文件失败: {e}", exc_info=True)
            raise
