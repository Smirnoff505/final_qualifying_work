import csv
import json
import re

import requests
from tqdm import tqdm


class GoldenAppleAPI:

    def __init__(self):
        self.base_url = 'https://goldapple.ru/front/api/'

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
        }

        self.params = {
            'cityId': '4ffcde97-05e9-4a6e-bd51-3a984b41b7bd',
        }

    def count(self) -> int:
        """Возвращает полное количество товаров"""

        self.params.update({
            'categoryId': '1000000007',
            'pageNumber': 1
        })

        url = f'{self.base_url}catalog/plp'
        response = requests.get(url=url, params=self.params, headers=self.headers)
        count = response.json()['data']['products']['count']

        return count

    def get_all_id(self, page_number: int) -> list:
        """Возвращает список всех ID карточек расположенных на странице с номером page_number"""

        all_ld = []

        self.params.update({
            'categoryId': '1000000007',
            'pageNumber': page_number
        })

        url = f'{self.base_url}catalog/plp'
        response = requests.get(url=url, params=self.params, headers=self.headers)
        data = response.json()['data']['products']['products']

        response.raise_for_status()

        for item in data:
            card_id = item['itemId']
            all_ld.append(card_id)

        return all_ld

    def get_products_info_and_save_json(self, cards_id: list) -> None:
        """Принимает список ID карточек и сохраняет необходимую информацию в json-файл"""

        products_data = []

        for card in tqdm(cards_id):

            self.params.update({
                'itemId': card,
                'customerGroupId': 0
            })

            url = f'{self.base_url}catalog/product-card'
            response = requests.get(url=url, params=self.params, headers=self.headers)
            product_info = response.json()

            product_url = product_info['data']['variants'][0]['url']
            product_title = product_info['data']['productDescription'][0]['title']

            product_description = product_info['data']['productDescription'][0]['content']
            product_description = re.sub(r'\s*\n\s*', '', product_description).replace('<br>', ' ')

            price = product_info['data']['variants'][0]['price']['actual']['amount']

            try:
                price_loyalty = product_info['data']['variants'][0]['price']['loyalty']['amount']
            except Exception:
                price_loyalty = 'Скидка отсутствует'

            product_instruction = ''
            for item in product_info['data']['productDescription']:
                if item['text'].lower() == 'применение':
                    product_instruction = item['content']
                    product_instruction = re.sub(r'\s*\n\s*', '', product_instruction).replace('<br>', ' ')

            product_country = ''
            for item in product_info['data']['productDescription']:
                if item['text'].lower() == 'дополнительная информация':
                    product_country = item['content'].split('<br>')[1]

            products_data.append(
                {
                    'Ссылка на продукт': f"https://goldapple.ru{product_url}",
                    'Наименование': product_title,
                    'Описание продукта': product_description,
                    'Цена без скидки': price,
                    'Цена со скидкой': price_loyalty,
                    'Инструкция по применению': product_instruction,
                    'Страна - производитель': product_country
                }
            )

        with open('data/products_info.json', 'a', encoding='utf-8') as file:
            json.dump(products_data, file, indent=4, ensure_ascii=False)

    def save_to_csv(self) -> None:
        """Создает файл-csv"""

        try:
            with open('data/products_info.json') as file_json:
                data = json.load(file_json)

            titles = list(data[0].keys())  # Получаем ключи первого элемента для заголовков

            with open('data/products_info.csv', 'w', newline='') as file_csv:
                writer = csv.writer(file_csv)
                writer.writerow(titles)

                for item in tqdm(data):
                    values = list(item.values())
                    writer.writerow(values)

        except FileNotFoundError as err:
            print(err, 'Не найден файл products_info.json')
