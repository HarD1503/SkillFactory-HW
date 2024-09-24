import requests
import  json
from config import exchanges


class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_symb = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_symb = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_symb == quote_symb:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = round(float(amount))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get('https://www.cbr-xml-daily.ru/latest.js')
        resp = json.loads(r.content)

        rates = {}
        for i in exchanges.values():
            if i == 'RUB':
                rates[i] = 1
            else:
                rates[i] = resp['rates'][i]
        price = round((rates[quote_symb]/rates[base_symb]) * amount,3)
        message = f'Цена {str(amount)} {base} в {quote} : {price}'
        return message