import tempfile
import unittest
from pathlib import Path

from cli import convert_currency
from storage import read_from_file, save_to_file


class CurrencyTests(unittest.TestCase):
    def test_save_and_read_with_custom_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "rates.json"
            payload = {"base_code": "USD", "rates": {"USD": 1, "EUR": 0.85}}

            save_to_file(payload, path=str(file_path))
            loaded = read_from_file(path=str(file_path))

            self.assertEqual(payload, loaded)

    def test_convert_currency_success(self) -> None:
        rates = {"USD": 1.0, "EUR": 0.85, "RUB": 75.0}
        result = convert_currency(100, "USD", "EUR", rates)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result, 85.0, places=6)

    def test_convert_currency_unknown_code(self) -> None:
        rates = {"USD": 1.0}
        result = convert_currency(10, "USD", "EUR", rates)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
