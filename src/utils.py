import datetime
import os

from src.golden_apple import GoldenAppleAPI


def main():
    goldenapple = GoldenAppleAPI()

    if not os.path.exists('data'):
        os.mkdir('data')

    try:
        # Получение времени начала работы
        current_time = datetime.datetime.now()

        # получение количества товаров
        count_goods = goldenapple.count()

        cards_id = []
        page_number = 1
        print('Получение списка ID-карточек:')

        while True:
            # добавление ID-карточек в список cards_id
            cards_id.extend(goldenapple.get_all_id(page_number))
            print(f'Прошло итераций {page_number} из {(count_goods // 24) + 1}')
            page_number += 1
            if len(cards_id) >= count_goods:
                break

        # получение информации о продукте и запись его в json файл
        goldenapple.get_products_info_and_save_json(cards_id)

        # запись информации в файл csv
        goldenapple.save_to_csv()

        # вычисление времени работы программы
        end_time = datetime.datetime.now() - current_time
        print(end_time)

    except KeyboardInterrupt:
        print('[INFO] Программа остановлена принудительно!')

    except ConnectionError as err:
        print(f'[INFO] {err} Проблемы с сетью.')
