import json
from typing import Any

from http_client import get

REQUEST_TIMEOUT = 10


def send_get_by_url() -> None:
    url = input("Введите полный URL для GET запроса: ").strip()
    if not url:
        print("URL не может быть пустым.\n")
        return

    response = get(url, timeout=REQUEST_TIMEOUT)
    if response is not None:
        _print_response(response)


def make_get_country_request(country: str) -> None:
    url = f"https://restcountries.com/v3.1/name/{country}"
    response = get(url, timeout=REQUEST_TIMEOUT)
    if response is None:
        return

    _print_response(response)
    _print_country_info(response.json())


def make_random_dog_request() -> None:
    url = "https://dog.ceo/api/breeds/image/random"
    response = get(url, timeout=REQUEST_TIMEOUT)
    if response is None:
        return

    _print_response(response)
    data = response.json()
    image_url = data.get("message", "N/A") if isinstance(data, dict) else "N/A"
    print(f"Ссылка на изображение: {image_url}\n")


def _print_response(response: Any) -> None:
    print("\n--- Ответ ---")
    print(f"Статус: {response.status_code}")
    print(f"Заголовки: {dict(response.headers)}")
    print("Тело:")
    _print_body(response)
    print("----------------\n")


def _print_body(response: Any) -> None:
    body: Any
    try:
        body = response.json()
        print(json.dumps(body, indent=2, ensure_ascii=False))
    except ValueError:
        print(response.text)


def _print_country_info(data: Any) -> None:
    if not isinstance(data, list) or not data:
        print("Данные по стране не найдены.")
        return

    country_data = data[0]
    if not isinstance(country_data, dict):
        print("Неожиданный формат данных по стране.")
        return

    name = country_data.get("name", {}).get("common", "N/A")
    capital_list = country_data.get("capital", [])
    capital = capital_list[0] if capital_list else "N/A"
    population = country_data.get("population", "N/A")

    print("Ключевые поля:")
    print(f"- name: {name}")
    print(f"- capital: {capital}")
    print(f"- population: {population}\n")


def main() -> None:
    while True:
        print("Выберите действие:")
        print("1 — GET по URL")
        print("2 — Страна")
        print("3 — Случайная собака")
        print("0 — Выход")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            send_get_by_url()
        elif choice == "2":
            country = input("Введите название страны (например, Germany): ").strip()
            if not country:
                print("Название страны не может быть пустым.\n")
                continue
            make_get_country_request(country)
        elif choice == "3":
            make_random_dog_request()
        elif choice == "0":
            print("Пока!")
            break
        else:
            print("Неизвестная опция. Попробуйте снова.\n")


if __name__ == "__main__":
    main()
