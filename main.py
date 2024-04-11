import datetime
import os

from classes import GoldenAppleAPI

if __name__ == '__main__':
    goldenapple = GoldenAppleAPI()

    if not os.path.exists('data'):
        os.mkdir('data')

    # goldenapple.save_to_csv()

    # id_p = goldenapple.get_all_id(5)
    # goldenapple.get_products_info_and_save_json(id_p)

    # Получение времени начала работы
    cur_time = datetime.datetime.now()

    # получение количества товаров
    count = goldenapple.count()

    cards_id = []
    page_number = 1
    print(f'Получение списка ID-карточек:')

    while True:
        # добавление ID-карточек в список cards_id
        cards_id.extend(goldenapple.get_all_id(page_number))
        print(f'Прошло итераций {page_number} из {(count // 24) + 1}')
        page_number += 1
        if len(cards_id) >= count:
            break

    # получение информации о продукте и запись его в json файл
    goldenapple.get_products_info_and_save_json(cards_id)

    # запись информации в файл csv
    goldenapple.save_to_csv()

    # вычисление времени работы программы
    end_time = datetime.datetime.now() - cur_time
    print(end_time)
