import re
from typing import Dict, Optional

from tradingagents.utils.logging_manager import get_logger

logger = get_logger("instrument_validator")


_EX_SH_PREFIXES = ("10", "11", "113", "110", "118")  # heuristic for SH convertible/bonds
_EX_SZ_PREFIXES = ("12", "123", "127", "128")  # heuristic for SZ convertible/bonds


def normalize_bond_code(code: str) -> Dict[str, Optional[str]]:
    """
    Normalize a China bond/convertible bond code to a standard form.

    Input examples:
    - "123001"
    - "123001.SZ" / "sz123001" / "SZ123001"
    - "110031.SH" / "sh110031" / "SH110031"

    Returns dict:
    - digits: 6-digit numeric code
    - exchange: "SH" | "SZ" | None (unknown)
    - code_std: "{digits}.SH|SZ" if exchange known, else just digits
    """
    if not code:
        return {"digits": None, "exchange": None, "code_std": None}

    s = str(code).strip()

    # Extract exchange hint
    exch: Optional[str] = None
    # dot suffix
    m = re.search(r"\.(SH|SZ)$", s, re.IGNORECASE)
    if m:
        exch = m.group(1).upper()
    # leading prefix sh/sz
    if exch is None:
        m2 = re.match(r"^(SH|SZ)\s*[-_]?\s*(\d{6})$", s, re.IGNORECASE)
        if m2:
            exch = m2.group(1).upper()
            s = m2.group(2)
    # remove non-digits to get digits
    digits = re.sub(r"\D", "", s)
    if len(digits) != 6:
        # Try to capture trailing 6 digits
        m3 = re.search(r"(\d{6})", s)
        if m3:
            digits = m3.group(1)
        else:
            logger.debug(f"normalize_bond_code: invalid code '{code}'")
            return {"digits": None, "exchange": exch, "code_std": None}

    # Heuristic exchange if unknown
    if exch is None:
        if any(digits.startswith(pfx) for pfx in _EX_SH_PREFIXES):
            exch = "SH"
        elif any(digits.startswith(pfx) for pfx in _EX_SZ_PREFIXES):
            exch = "SZ"

    code_std = f"{digits}.{exch}" if exch else digits
    return {"digits": digits, "exchange": exch, "code_std": code_std}
