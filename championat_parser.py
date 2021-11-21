import json
import random
from time import sleep
import os
import shutil

from bs4 import BeautifulSoup
import requests


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

    count = 1

    for sport in kinds_of_sport.keys():
        print(sport)
        count += 1

    while True:
        try:
            input_sport = int(input("Из предложенного списка ведите число, это будет вид спорта, который мы будем "
                                    "парсить с сайта championat.com: "))

            if not (0 < input_sport < 7):
                raise Exception

            dict_key = list(kinds_of_sport.keys())[input_sport - 1]
            parsed_sport = kinds_of_sport[dict_key]

            break
        except Exception:
            print("Вы ввели неправильное число, попробуйте снова.")

    while True:
        try:
            pages_amount = int(input("Сколько страниц с новостями будем просматривать? "
                                     "Введите целое число (от 1 до 100): "))
            if not (0 < pages_amount < 101):
                raise Exception

            break
        except Exception:
            print("Введите, пожалуйста, число в пределах от 1 до 100.")

    return parsed_sport, pages_amount


# Функция создания папки data
def data_folder():
    if os.path.exists("data"):
        shutil.rmtree("data")
    os.mkdir("data")


# Функция извлечения информации о комментариях
def extract_comments(soup):
    all_comments = soup.find_all("span", class_="js-comments-count")
    json_url = f"https://c.rambler.ru/api/app/5/comments-count?"

    # Через цикл генерируем ссылку обращения к серверу для получения json файла с необходимой информацией
    for comment in all_comments:
        json_url += "xid=" + comment.get("data-id") + "&"

    json_data = requests.get(headers=headers, url=json_url).text
    json_obj = json.loads(json_data)

    return json_obj["xids"]


# Функция, которая парсит страницы
def get_data(parsed_sport, pages_amount):
    news_info = []

    iteration_count = pages_amount
    count = 0
    print(f"Всего итераций: {iteration_count}")

    # Проходим по каждой странице с новостями
    for page_number in range(1, pages_amount + 1):
        url = f"https://www.championat.com/news{parsed_sport}{page_number}.html"

        req = requests.get(url, headers=headers)
        src = req.text

        with open(f"data/page_{page_number}.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open(f"data/page_{page_number}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_news = soup.find_all("div", class_="news-item")

        comments_dict = extract_comments(soup)

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
                comments = None

            news_info.append({
                "Заголовок": title,
                "Ссылка": href,
                "Тег": tag,
                "Количество комментариев": comments,
                "Дата публикации": time
            })

        count += 1
        print(f"# Новости со страницы {count} записаны...")

        iteration_count -= 1

        if iteration_count == 0:
            print("Работа завершена")
            break

        print(f"Осталось итераций: {iteration_count}")

        sleep(random.randint(2, 4))

    with open(f"news.json", "w", encoding="utf-8") as file:
        json.dump(news_info, file, indent=4, ensure_ascii=False)


# Сначала создаем папку data, затем получаем пользовательские вводные данные и на основе их парсим новости определенного
# вида спорта и количества страниц
def main():
    data_folder()
    parsed_sport, pages_amount = main_prompt()
    get_data(parsed_sport, pages_amount)


if __name__ == "__main__":
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
           Chrome/95.0.4638.69 Safari/537.36"
    }
    main()
