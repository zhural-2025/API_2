import json
import time
from pathlib import Path
from typing import Any


def save_to_file(data: dict[str, Any], path: str = "currency_rate.json") -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_from_file(path: str = "currency_rate.json") -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        return {}
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def is_cache_fresh(path: str = "currency_rate.json", max_age_seconds: int = 24 * 60 * 60) -> bool:
    file_path = Path(path)
    if not file_path.exists():
        return False
    age_seconds = time.time() - file_path.stat().st_mtime
    return age_seconds < max_age_seconds
