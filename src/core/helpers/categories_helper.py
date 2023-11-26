from prettytable import PrettyTable

from src.core.messages import *
from src.db.models import Category


def input_category(categories: list[Category]):
    """
    Функция для получения пользовательского ввода ID категорий.

    Отображает доступные категории и предлагает пользователю ввести один или несколько ID категорий, разделенных запятыми.
    Если пользователь вводит 'exit', функция завершает выполнение программы.
    Проверяет, что все введенные значения являются цифрами, и возвращает список целочисленных ID категорий.
    В случае неверного ввода выводится сообщение об ошибке и запрашивается повторный ввод.

    :return: Список ID выбранных категорий.
    """
    pretty_print_categories(categories)

    while True:
        suggested_categories = input(CATEGORIES_INPUT_MSG).strip()
        if suggested_categories.lower() == "exit":
            exit()

        category_ids_str = [uuid.strip() for uuid in suggested_categories.split(",")]

        if all(uuid.isdigit() for uuid in category_ids_str):
            category_ids = [int(uuid) for uuid in category_ids_str]
            return category_ids
        else:
            print(CATEGORIES_ERROR_MSG)


def pretty_print_categories(categories):
    """
    Функция для получения пользовательского ввода ID категорий.

    Отображает доступные категории и предлагает пользователю ввести один или несколько ID категорий, разделенных запятыми.
    Если пользователь вводит 'exit', функция завершает выполнение программы.
    Проверяет, что все введенные значения являются цифрами, и возвращает список целочисленных ID категорий.
    В случае неверного ввода выводится сообщение об ошибке и запрашивается повторный ввод.

    :return: Список ID выбранных категорий.
    """
    table = PrettyTable()
    table.field_names = [CATEGORY_ID, CATEGORY_NAME]
    table.align[CATEGORY_ID] = "l"
    table.align[CATEGORY_NAME] = "l"

    for category in categories:
        table.add_row([category.id, category.name])

    print(AVAILABLE_CATEGORIES)
    print(table)
