import json
import random

import requests

from faker import Faker
from tqdm import tqdm
from bs4 import BeautifulSoup

from time import sleep


# Класс исключения, вызывающегося, если число не входит в определенный диапазон
class RangeError(Exception):
    def __init__(self, number, end_range):
        self.number = number
        self.end_range = end_range

    def __str__(self):
        return f"Ошибка: число должно быть в пределах от 1 до {self.end_range} включительно." \
               f"Было введено число: {self.number}"


# Функция валидации переданного числа
def is_valid_number(number, range_end):
    try:
        if not (1 <= int(number) <= range_end):
            raise RangeError(number, range_end)
    except ValueError:
        print("Вы ввели не число. Пожалуйста, повторите попытку.")
    except RangeError:
        print(f"Число должно быть в пределах от 1 до {range_end} включительно. "
              "Пожалуйста, повторите попытку.")
    else:
        return True

    return False


# Функция опроса пользователя
def poll_user(poll_text, end_range):
    while True:
        number = input(poll_text)
        if is_valid_number(number, end_range):
            break

    return int(number)


# Функция отображения информации для пользователя
def main_prompt():
    kinds_of_sport = {
        "1. Все новости": "/",
        "2. Футбол": "/football/",
        "3. Хоккей": "/hockey/",
        "4. Бокс": "/boxing/",
        "5. Теннис": "/tennis/",
        "6. Фигурное катание": "/figureskating/"
    }

    list(map(print, list(kinds_of_sport.keys())))

    input_sport = poll_user(
        "Из предложенного списка ведите число, это будет вид спорта, который мы будем парсить с сайта championat.com: ",
        len(kinds_of_sport)
    )

    dict_key = list(kinds_of_sport.keys())[input_sport - 1]
    parsed_sport = kinds_of_sport[dict_key]

    pages_amount = poll_user(
        "Сколько страниц с новостями будем просматривать? Введите целое число (от 1 до 100): ",
        100
    )

    return parsed_sport, pages_amount


# Функция извлечения информации о комментариях
def extract_comments(all_comments, headers):
    json_url = f"https://c.rambler.ru/api/app/5/comments-count?"

    # Через цикл генерируем ссылку обращения к серверу для получения json файла с необходимой информацией
    for comment in all_comments:
        json_url += "xid=" + comment.get("data-id") + "&"

    data = requests.get(headers=headers, url=json_url).json()

    return data["xids"]


# Функция, которая парсит страницы
def get_data(parsed_sport, pages_amount):
    news_info = []

    # Проходим по каждой странице с новостями
    for page_number in tqdm(range(1, pages_amount + 1)):
        Faker.seed(random.randint(0, 100))
        fake = Faker()

        headers = {
            "Accept": "*/*",
            "User-Agent": fake.chrome()
        }

        url = f"https://www.championat.com/news{parsed_sport}{page_number}.html"

        req = requests.get(url, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")
        all_news = soup.find_all("div", class_="news-item")

        all_comments = soup.find_all("span", class_="js-comments-count")
        comments_dict = extract_comments(all_comments, headers)

        # В каждой новости на странице находим все сведения о ней
        for new in all_news:
            new_time = new.find("div", class_="news-item__time")
            new_content = new.find("div", class_="news-item__content")

            title = new_content.find_all("a")[0].text
            href = "https://www.championat.com" + new_content.find_all("a")[0].get("href")
            tag = new.find("a", class_="news-item__tag").text
            time = new_time.text

            try:
                new_comments_class = new.find("span", class_="js-comments-count").get("data-id")
                comments = comments_dict[new_comments_class]
            except Exception:
                comments = 0

            news_info.append({
                "Заголовок": title,
                "Ссылка": href,
                "Тег": tag,
                "Количество комментариев": comments,
                "Дата публикации": time
            })

        sleep(random.randint(2, 4))

    with open(f"news.json", "w", encoding="utf-8") as file:
        json.dump(news_info, file, indent=4, ensure_ascii=False)

    print("Работа завершена!")


# Получаем пользовательские вводные данные и на основе их парсим новости определенного
# вида спорта и количества страниц
def main():
    parsed_sport, pages_amount = main_prompt()
    get_data(parsed_sport, pages_amount)


if __name__ == "__main__":
    main()
