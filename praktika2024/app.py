import json
import csv
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
import sys


def is_unique_combination(entities, attributes):
    """
    Проверяет, является ли комбинация атрибутов уникальной для всех сущностей.

    :param entities: список сущностей
    :param attributes: комбинация атрибутов
    :return: True, если комбинация уникальна, иначе False
    """
    seen = set()
    for entity in entities:
        identifier = tuple(entity.get(attr, None) for attr in attributes)
        if identifier in seen:
            return False
        seen.add(identifier)
    return True


def calculate_information_gain(entities, attribute):
    """
    Вычисляет количество уникальных значений для данного атрибута.

    :param entities: список сущностей
    :param attribute: атрибут
    :return: количество уникальных значений
    """
    unique_values = set(entity.get(attribute, None) for entity in entities)
    return len(unique_values)


def check_combination(entities, combination):
    """
    Проверяет, является ли данная комбинация атрибутов уникальной.

    :param entities: список сущностей
    :param combination: комбинация атрибутов
    :return: комбинация, если она уникальна, иначе None
    """
    return combination if is_unique_combination(entities, combination) else None


def find_minimal_unique_combination(entities):
    """
    Находит минимальную уникальную комбинацию атрибутов для идентификации сущностей.

    :param entities: список сущностей
    :return: минимальная уникальная комбинация атрибутов
    """
    if not entities:
        return []

    attributes = list(entities[0].keys())

    # Calculate information gain for each attribute
    info_gain = {attr: calculate_information_gain(entities, attr) for attr in attributes}

    # Sort attributes by their information gain
    sorted_attributes = sorted(attributes, key=lambda x: info_gain[x], reverse=True)

    for r in range(1, len(sorted_attributes) + 1):
        combinations_list = list(combinations(sorted_attributes, r))
        with ThreadPoolExecutor() as executor:
            results = executor.map(lambda combo: check_combination(entities, combo), combinations_list)
            minimal_combination = next((result for result in results if result is not None), None)
            if minimal_combination:
                return list(minimal_combination)

    return []


def main(json_data):
    """
    Основная функция, которая принимает JSON-строку и возвращает CSV-строку.

    :param json_data: JSON-строка с исходными данными
    :return: CSV-строка с минимальной уникальной комбинацией атрибутов
    """
    entities = json.loads(json_data)
    minimal_combination = find_minimal_unique_combination(entities)

    output = StringIO()
    writer = csv.writer(output, lineterminator='\n')
    for attribute in minimal_combination:
        writer.writerow([attribute])

    return output.getvalue()


# Unit-тесты
import unittest


class TestUniqueCombination(unittest.TestCase):

    def setUp(self):
        self.json_data = json.dumps([
            {"фамилия": "Смирнов", "имя": "Евгений", "отчество": "Александрович", "класс": "6"},
            {"фамилия": "Смирнов", "имя": "Евгений", "отчество": "Александрович", "класс": "7"},
            {"фамилия": "Петров", "имя": "Иван", "отчество": "Сергеевич", "класс": "7"}
        ])
        self.entities = json.loads(self.json_data)

    def test_is_unique_combination(self):
        self.assertTrue(is_unique_combination(self.entities, ["фамилия", "имя", "отчество", "класс"]))
        self.assertFalse(is_unique_combination(self.entities, ["фамилия", "имя", "отчество"]))

    def test_calculate_information_gain(self):
        self.assertEqual(calculate_information_gain(self.entities, "фамилия"), 2)
        self.assertEqual(calculate_information_gain(self.entities, "класс"), 2)

    def test_find_minimal_unique_combination(self):
        self.assertEqual(find_minimal_unique_combination(self.entities), ["фамилия", "класс"])

    def test_main(self):
        expected_csv = "фамилия\nкласс\n"
        self.assertEqual(main(self.json_data), expected_csv)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_input = sys.argv[1]
        result_csv = main(json_input)
        print(result_csv)
    else:
        unittest.main()
