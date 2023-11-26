from src.core.messages import *


def input_nickname():
    """
    Функция-хелпер для ввода никнейма с проверкой валидности.

    Пользователь вводит никнейм, который проверяется на соответствие длине от 1 до 15 символов.
    Если введенный никнейм равен 'exit', функция завершает выполнение программы.
    При вводе недопустимого никнейма выводится соответствующее сообщение и запрашивается повторный ввод.

    :return: Валидный никнейм пользователя.
    """
    while True:
        nickname = input(NICKNAME_INPUT_MSG).strip()

        if nickname.lower() == "exit":
            exit()

        if not 1 <= len(nickname) <= 15:
            print(NICKNAME_LEN_REQUIRED)
            continue

        return nickname
