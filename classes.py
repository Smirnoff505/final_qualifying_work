import csv
import json
import re

import requests
from tqdm import tqdm


class GoldenAppleAPI:
    base_url = 'https://goldapple.ru/front/api/'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
    }

    def count(self):
        """Возвращает полное количество товаров"""

        params = {
            'categoryId': '1000000007',
            'cityId': '4ffcde97-05e9-4a6e-bd51-3a984b41b7bd',
            'pageNumber': 1
        }

        url = f'{self.base_url}catalog/plp'
        response = requests.get(url=url, params=params, headers=self.headers)
        count = response.json()['data']['products']['count']

        return count

    def get_all_id(self, page_number):
        """Возвращает список всех ID карточек расположенных на странице с номером page_number"""

        all_ld = []

        params = {
            'categoryId': '1000000007',
            'cityId': '4ffcde97-05e9-4a6e-bd51-3a984b41b7bd',
            'pageNumber': page_number
        }

        url = f'{self.base_url}catalog/plp'
        response = requests.get(url=url, params=params, headers=self.headers)
        data = response.json()['data']['products']['products']

        response.raise_for_status()

        for item in data:
            card_id = item['itemId']
            all_ld.append(card_id)

        return all_ld

    @staticmethod
    def get_rating(card_id):
        """Получает рейтинг"""

        params = {
            'pageNumber': 1,
            'itemId': int(card_id),
            'cityId': '0c5b2444-70a0-4932-980c-b4dc0d3f02b5',
            'hasMedia': False
        }

        url = f'https://goldapple.ru/front/api/review/listing'
        response = requests.get(url=url, params=params)
        response.raise_for_status()

        try:
            rating = response.json()['data']['statistic']['rating']
        except:
            rating = 'Данный товар еще никто не оценил'

        return rating

    def get_products_info_and_save_json(self, cards_id: list):
        """Принимает список ID карточек и сохраняет необходимую информацию в json-файл"""

        products_data = []

        for card in tqdm(cards_id):

            params = {
                'itemId': int(card),
                'cityId': '4ffcde97-05e9-4a6e-bd51-3a984b41b7bd',
                'customerGroupId': 0

            }

            url = f'{self.base_url}catalog/product-card'
            response = requests.get(url=url, params=params, headers=self.headers)
            product_info = response.json()

            product_url = product_info['data']['variants'][0]['url']
            product_title = product_info['data']['productDescription'][0]['title']

            product_description = product_info['data']['productDescription'][0]['content']
            product_description = re.sub(r'\s*\n\s*', '', product_description).replace('<br>', ' ')

            price = product_info['data']['variants'][0]['price']['actual']['amount']

            try:
                price_loyalty = product_info['data']['variants'][0]['price']['loyalty']['amount']
            except:
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
                    # 'Рейтинг': self.get_rating(card),
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
