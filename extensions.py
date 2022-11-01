'" Файл с классами для обработки исключений и проведения конвертации валют"'
import requests
import json
from config import currencies

# класс для обработки исключений
class APIException(Exception):
    pass

# класс для проведения конвертации
class Convert():
    @staticmethod
    def get_price(quote, base, amount):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        d = json.loads(r.content)

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f"Невозможно выполнить конвертацию валюты {quote}")

        try:
            base_ticker =  currencies[base]
        except KeyError:
            raise APIException(f"Невозможно выполнить конвертацию валюты {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f" Неверно введено количество валюты {amount}")
        if amount <= 0:
            raise APIException('Количество валюты должно быть больше 0')

        if quote == 'рубль':
            return (amount) / ((float)(d['Valute'][base_ticker]['Value']))
        if base == 'рубль':
            return ((float)(d['Valute'][quote_ticker]['Value'])) * amount

        return ((float)(d['Valute'][quote_ticker]['Value']) / (float)(d['Valute'][base_ticker]['Value'])) * amount
