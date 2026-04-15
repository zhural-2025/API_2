from typing import Any

import requests
from requests import Response


def get(url: str, params: dict[str, Any] | None = None, timeout: int = 10) -> Response | None:
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.RequestException as error:
        print(f"Ошибка GET запроса: {error}")
        return None
