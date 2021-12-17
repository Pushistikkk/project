import unittest
from tetris_game import get_record, set_record, check_borders
import os

class Test_Get_Records(unittest.TestCase):
    """тесты для функции получения рекорда"""
    def test_get_record(self):
        """проверяем, считывает ли функция из файла record верное значение, и что не считывает не верное"""

        with open('record') as f:  # считываем предыдущее значение
            get = f.readline()  # заносим значение в переменную

        write = "123"  # вписываем любое значение
        not_write = "1"

        with open('record', 'w') as f:
            f.write(write)
        gets = get_record() # выводим результат работы функции get_record
        with open('record', 'w') as f:
            f.write(get)  # возвращаем предыдущее значение в файл
        self.assertEqual(gets, write)  # сравниваем результат работы функции get_record с ожидаемым
        self.assertNotEqual(gets, not_write) # проверяем, что не считывает любое другое, кроме write
    def test_get_record_file(self):
        """Проверяем, что при отсутствии файла record он автоматом создается со значением 0"""
        try:  # если изначально файл создан, удаляем его
            with open('record') as f:  # считываем предыдущее значение
                gett = f.readline()  # заносим значение в переменную
            os.remove("record")
            gets = get_record()
            get = get_record()
            with open('record', 'w') as f:
                f.write(gett)  # возвращаем предыдущее значение в файл
            self.assertEqual(get, "0")
        except FileNotFoundError:  # если файла изначально нет
            gets = get_record()
            get = get_record()
            self.assertEqual(get, "0")

class Test_Set_Records(unittest.TestCase):
    """тесты для функции записи рекорда"""
    def test_set_record_score(self):
        """функция, которая проверяет, что если набранных очков больше, чем предыдущий рекорд,
        в файл record записывается значение score"""
        with open('record') as f:  # считываем предыдущее значение
            gets = f.readline()  # заносим значение в переменную
        score = 700
        record = 400  # придумываем новые значения, чтобы значение record было меньше
        set_record(record, score)  # применяем функцию к новым значениям
        with open('record') as f:
            get = int(f.readline())  # считываем из файла значение, которое туда записала примененная функция
        with open('record', 'w') as f:
            f.write(gets)  # возвращаем в файл значение, которое в нем было до теста
        self.assertEqual(get, score)  # сравниваем, правильно ли записалось новое значение в файл
    def test_set_record_record(self):
        """функция, которая проверяет, что если набранных очков меньше, чем предыдущий рекорд,
        в файл record записывается значение record"""
        with open('record') as f:
            gets = f.readline()
        score = 100
        record = 400
        set_record(record, score)
        with open('record') as f:
            get = int(f.readline())
        with open('record', 'w') as f:
            f.write(gets)
        self.assertEqual(get, record)
    def test_set_record_middle(self):
        """функция, которая проверяет, что если score и record равны,
                в файл record записывается значение record(score)"""
        with open('record') as f:
            gets = f.readline()
        score = 300
        record = 300
        set_record(record, score)
        with open('record') as f:
            get = int(f.readline())
        with open('record', 'w') as f:
            f.write(gets)
        self.assertEqual(get, record)
        self.assertEqual(get, score)

class Test_Check_Borders(unittest.TestCase):
    """Тесты для функции проверки границ"""
    def test_check_borders(self):
        check1 = check_borders(10, 18, map)  # если по х зашел за правую границу, а по у нет
        self.assertEqual(check1, False)
        check2 = check_borders(-1, 18, map)  # если по х зашел за левую границу, а по у нет
        self.assertEqual(check2, False)
        check3 = check_borders(8, 20, map)  # если по у достиг дна, а по х не зашел за границы
        self.assertEqual(check3, False)
        check4 = check_borders(10, 20, map)  # если зашел за границу по х и достиг дна по у
        self.assertEqual(check4, False)

if __name__ == "__main__":
    unittest.main()


