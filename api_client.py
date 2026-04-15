from typing import Any

import requests


def get_currency_rates(base: str) -> dict[str, Any]:
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as error:
        print(f"Ошибка запроса для {base}: {error}")
        return {}

    if response.status_code != 200:
        print(f"Не удалось получить курсы для {base}. Код ответа: {response.status_code}")
        return {}

    data: dict[str, Any] = response.json()
    if data.get("result") != "success":
        print(f"API вернул ошибку для {base}: {data.get('error-type', 'unknown')}")
        return {}
    return data
