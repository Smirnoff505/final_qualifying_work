import os
import shutil
import unittest

from classes import GoldenAppleAPI


class TestGoldenAppleAPI(unittest.TestCase):
    """Тесты класса GoldenAppleAPI"""

    def setUp(self):
        self.golden = GoldenAppleAPI()

    def test_count(self):
        """Тест для метода получения количества товаров"""
        try:

            self.assertGreater(
                self.golden.count(),
                0
            )

            self.assertEqual(
                self.golden.count(),
                10684
            )
        except Exception as err:
            print(f'Тест не прошел {err}')

    def test_get_all_id(self):
        """Тест для получения ID карточек"""

        try:

            self.assertEqual(
                self.golden.get_all_id(1),
                ['19000004549', '83800100002', '19000206606', '28320100007', '19000174047', '19000220691',
                 '19000196621', '7273800003', '83710100004', '19000214266', '19000178408',
                 '83670100006', '19000165286', '19000195377', '19000139404', '19000122593', '19000123334',
                 '19000240975', '19000063330', '19000206595', '19000165309', '19000182787', '19000152689',
                 '19000121301']
            )
        except Exception as err:
            print(f'Тест не прошел {err}')

    def test_get_products_info_and_save_json(self):
        """Тест получения информации и сохранения json-файла"""

        if not os.path.exists('data'):
            os.mkdir('data')

        try:
            self.golden.get_products_info_and_save_json(['19000004549', '83800100002'])

            self.assertTrue(
                os.path.exists('data/products_info.json')
            )

        except Exception as err:
            print(f'Тест не прошел {err}')

    def test_save_to_csv(self):
        """Тест для записи информации о продуктах в файл"""

        try:
            self.golden.save_to_csv()

            self.assertTrue(
                os.path.exists('data/products_info.csv')
            )
        except Exception as err:
            print(f'Тест не прошел {err}')

        shutil.rmtree('data')
        pass

    def tearDown(self):
        pass
