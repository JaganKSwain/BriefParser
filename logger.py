"""
logger.py — Centralised logging for the Scrollhouse agent.

Usage:
    from logger import log, log_error
    log("Brief processed: row_001")
    log_error("Pipeline crashed", exc)
"""

import traceback
from datetime import datetime


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str, level: str = "INFO") -> None:
    """Print a timestamped log line to stdout."""
    print(f"[{_ts()}] [{level}] {message}")


def log_info(message: str) -> None:
    log(message, "INFO")


def log_warning(message: str) -> None:
    log(message, "WARN")


def log_error(message: str, exc: Exception = None) -> None:
    """Log an error, optionally with a full traceback."""
    log(message, "ERROR")
    if exc is not None:
        tb = traceback.format_exc()
        if tb.strip() != "NoneType: None":
            print(tb)
