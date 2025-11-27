# -*- coding: utf-8 -*-
import ast
import json
from pathlib import Path
from typing import Dict, List, Optional

PROVIDERS_DIR = Path("app/services/data_sources/funds/providers")

METADATA_FIELDS = [
    {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    {"name": "更新人", "type": "string", "description": "数据更新人"},
    {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
    {"name": "创建人", "type": "string", "description": "数据创建人"},
]

DATE_KEYWORDS = [
    "净值日期",
    "公告日期",
    "报告日期",
    "统计日期",
    "发布日期",
    "交易日期",
    "日期",
    "时间",
    "Date",
    "date",
    "report_date",
    "trade_date",
]
QUARTER_KEYWORDS = ["季度", "期间", "年度", "年份", "year", "quarter"]
CODE_KEYWORDS = ["基金代码", "股票代码", "债券代码", "代码", "code", "Code", "symbol", "Symbol"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_block(text: str, anchor: str) -> Optional[Dict[str, int]]:
    idx = text.find(anchor)
    if idx == -1:
        return None
    start_bracket = text.find("[", idx)
    if start_bracket == -1:
        return None
    depth = 0
    for pos in range(start_bracket, len(text)):
        char = text[pos]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return {"start": idx, "value_start": start_bracket, "end": pos + 1}
    return None


def parse_list(text: str) -> List:
    return ast.literal_eval(text)


def format_field_info(indent: str, fields: List[Dict[str, str]]) -> str:
    lines = [f"{indent}field_info = ["]
    for field in fields:
        entry = (
            f'{{"name": {json.dumps(field["name"], ensure_ascii=False)}, '
            f'"type": {json.dumps(field["type"], ensure_ascii=False)}, '
            f'"description": {json.dumps(field.get("description", ""), ensure_ascii=False)}}}'
        )
        lines.append(f"{indent}    {entry},")
    lines.append(f"{indent}]")
    return "\n".join(lines)


def format_unique_keys(indent: str, keys: List[str]) -> str:
    entries = ", ".join(json.dumps(key, ensure_ascii=False) for key in keys)
    return f"{indent}unique_keys = [{entries}]"


def find_name(field_names: List[str], keywords: List[str]) -> Optional[str]:
    for kw in keywords:
        for name in field_names:
            if kw in name:
                return name
    return None


def infer_unique_keys(field_names: List[str]) -> List[str]:
    code_field = find_name(field_names, CODE_KEYWORDS)
    date_field = find_name(field_names, DATE_KEYWORDS)
    quarter_field = find_name(field_names, QUARTER_KEYWORDS)
    if code_field and date_field:
        return [code_field, date_field]
    if code_field and quarter_field:
        return [code_field, quarter_field]
    if code_field:
        return [code_field]
    if date_field:
        return [date_field]
    return field_names[:1] if field_names else []


def extract_indent(text: str, index: int) -> str:
    line_start = text.rfind("\n", 0, index)
    if line_start == -1:
        return ""
    line_start += 1
    return text[line_start:index]


def extract_field_names(field_list: List[Dict[str, str]]) -> List[str]:
    return [str(item.get("name", "")) for item in field_list]


def extract_ak_func(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("akshare_func"):
            _, _, value = stripped.partition("=")
            return value.strip().strip("\"'")
    return ""


def safe_replace(text: str, block: Dict[str, int], new_block: str) -> str:
    start_line = text.rfind("\n", 0, block["start"])
    if start_line == -1:
        start_line = 0
    else:
        start_line += 1
    return text[:start_line] + new_block + text[block["end"]:]


def update_file(path: Path) -> bool:
    if path.name == "__init__.py":
        return False
    text = read_text(path)
    original_text = text
    changed = False

    ak_func = extract_ak_func(text)

    block = find_block(text, "field_info")
    if block:
        value_str = text[block["value_start"]:block["end"]]
        field_list = parse_list(value_str)
        field_names = extract_field_names(field_list)
        for meta in METADATA_FIELDS:
            if meta["name"] not in field_names:
                field_list.append(meta.copy())
                field_names.append(meta["name"])
                changed = True
        source_desc = f"来源接口: {ak_func}"
        if "来源" not in field_names:
            field_list.append({"name": "来源", "type": "string", "description": source_desc})
            changed = True
        else:
            for item in field_list:
                if item.get("name") == "来源" and item.get("description") != source_desc:
                    item["description"] = source_desc
                    changed = True
        indent = extract_indent(text, block["start"])
        text = safe_replace(text, block, format_field_info(indent, field_list))

    block = find_block(text, "unique_keys")
    if block:
        value_str = text[block["value_start"]:block["end"]]
        current_keys = parse_list(value_str)
        if not current_keys:
            field_block = find_block(text, "field_info")
            if field_block:
                field_list = parse_list(text[field_block["value_start"]:field_block["end"]])
                field_names = extract_field_names(field_list)
            else:
                field_names = []
            inferred = infer_unique_keys(field_names)
            if inferred:
                indent = extract_indent(text, block["start"])
                text = safe_replace(text, block, format_unique_keys(indent, inferred))
                changed = True

    if changed and text != original_text:
        path.write_text(text, encoding="utf-8")
    return changed


def main():
    updated = 0
    for file in sorted(PROVIDERS_DIR.glob("*.py")):
        try:
            if update_file(file):
                updated += 1
        except Exception as exc:
            print(f"Error processing {file}: {exc}")
            raise
    print(f"Updated {updated} provider files")


if __name__ == "__main__":
    main()
