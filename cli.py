from typing import Any

from api_client import get_currency_rates
from storage import is_cache_fresh, read_from_file, save_to_file

DATA_FILE = "currency_rate.json"
TARGET_CURRENCIES = ("RUB", "EUR", "GBP")
CACHE_MAX_AGE_SECONDS = 24 * 60 * 60


def get_rates_with_cache(base: str, path: str = DATA_FILE) -> dict[str, Any]:
    base = base.upper()
    cached_data = read_from_file(path)

    if is_cache_fresh(path, CACHE_MAX_AGE_SECONDS):
        cached_rates = cached_data.get(base)
        if isinstance(cached_rates, dict):
            return cached_rates

    fresh_rates = get_currency_rates(base)
    if not fresh_rates:
        return {}

    if not isinstance(cached_data, dict):
        cached_data = {}
    cached_data[base] = fresh_rates
    save_to_file(cached_data, path)
    return fresh_rates


def get_available_currency_codes(rates_data: dict[str, Any]) -> set[str]:
    rates = rates_data.get("rates")
    if not isinstance(rates, dict):
        return set()
    return {str(code).upper() for code in rates.keys()}


def print_selected_rates(base: str, rates_data: dict[str, Any]) -> None:
    rates = rates_data.get("rates")
    if not isinstance(rates, dict):
        print("В ответе API нет блока rates.")
        return

    print(f"\nКурсы для базовой валюты {base}:")
    for code in TARGET_CURRENCIES:
        value = rates.get(code)
        if value is None:
            print(f"- {code}: нет данных")
        else:
            print(f"- {code}: {value}")


def convert_currency(amount: float, from_currency: str, to_currency: str, rates: dict[str, Any]) -> float | None:
    from_rate = rates.get(from_currency)
    to_rate = rates.get(to_currency)
    if from_rate is None:
        print(f"Код валюты '{from_currency}' не найден.")
        return None
    if to_rate is None:
        print(f"Код валюты '{to_currency}' не найден.")
        return None

    try:
        return amount * (float(to_rate) / float(from_rate))
    except (TypeError, ValueError, ZeroDivisionError):
        print("Некорректные значения курсов в ответе API.")
        return None


def convert_amount(from_currency: str, to_currency: str, amount: float) -> float | None:
    rates_data = get_rates_with_cache(from_currency, DATA_FILE)
    if not rates_data:
        print(f"Не удалось получить курсы для {from_currency}.")
        return None

    rates = rates_data.get("rates")
    if not isinstance(rates, dict):
        print("В ответе API нет блока rates.")
        return None

    return convert_currency(amount, from_currency, to_currency, rates)


def main() -> None:
    base = input("Введите базовую валюту (например, USD): ").strip().upper()
    if not base:
        print("Базовая валюта не может быть пустой.")
        return

    rates_data = get_rates_with_cache(base, DATA_FILE)
    if not rates_data:
        print("Не удалось получить курсы.")
        return

    available_codes = get_available_currency_codes(rates_data)
    if not available_codes:
        print("Не удалось получить список кодов валют (rates.keys()).")
        return

    print_selected_rates(base, rates_data)

    print("\nКонвертер суммы:")
    from_currency = input("Из валюты (например, USD): ").strip().upper()
    to_currency = input("В валюту (например, EUR): ").strip().upper()
    amount_raw = input("Сумма: ").strip().replace(",", ".")

    if not from_currency or not to_currency:
        print("Коды валют не могут быть пустыми.")
        return
    if from_currency not in available_codes:
        print(f"Код валюты '{from_currency}' не найден. Доступные коды: {', '.join(sorted(available_codes))}")
        return
    if to_currency not in available_codes:
        print(f"Код валюты '{to_currency}' не найден. Доступные коды: {', '.join(sorted(available_codes))}")
        return

    try:
        amount = float(amount_raw)
    except ValueError:
        print("Сумма должна быть числом.")
        return

    result = convert_amount(from_currency, to_currency, amount)
    if result is None:
        return
    print(f"{amount:.4f} {from_currency} = {result:.4f} {to_currency}")
