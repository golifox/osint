import requests
import httpx

print("Система поиска по никнейму")

nick = input("Введите никнейм: ")

print("Введен никнейм " + nick + " пожалуйста, ожидайте")


def osint(list):
    file = open(list)

    for line in file:
        name = line.split(" ")[0]
        site = line.split(" ")[1]

        site = site.rstrip("\n")
        url = site + nick

        try:
            r = requests.get(url)

            if r.status_code == 200:
                print("найдено " + name + ": " + url)
            else:
                print(+name + " не найдено")
        except:
            print("ошибка запроса для " + name)

    file.close()


print("Социальный сети и мессенджеры:")
osint("social.txt")

print("Видеохостинги:")
osint("vh.txt")

print("Игры:")
osint("games.txt")

print("Форумы: ")
osint("forums.txt")

print("Деньги: ")
osint("money.txt")

print("Другие сайты: ")
osint("other.txt")

print("Поиск завершён!")
