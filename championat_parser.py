import json
import random
from time import sleep
import os
import shutil

from bs4 import BeautifulSoup
import lxml
import requests


def main():
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
            if not (0 < pages_amount < 100):
                raise Exception

            break
        except Exception:
            print("Введите, пожалуйста, число в пределах от 1 до 100.")

    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/95.0.4638.69 Safari/537.36"
    }
    news_info = []

    if not os.path.exists("data"):
        os.mkdir("data")
    else:
        folder = 'data'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    iteration_count = pages_amount
    count = 0
    print(f"Всего итераций: {iteration_count}")

    for page_number in range(1, pages_amount + 1):
        url = f"https://www.championat.com/news{parsed_sport}{page_number}.html"

        req = requests.get(url, headers=headers)
        src = req.text

        if parsed_sport == "/":
            parsed_sport = "/all/"

        with open(f"data/{parsed_sport[1:-1]}_{page_number}.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open(f"data/{parsed_sport[1:-1]}_{page_number}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_news = soup.find_all("div", class_="news-item")

        for new in all_news:
            new_time = new.find("div", class_="news-item__time")
            new_content = new.find("div", class_="news-item__content")

            title = new_content.find_all("a")[0].text
            href = "https://www.championat.com" + new_content.find_all("a")[0].get("href")
            time = new_time.text

            news_info.append({
                "Заголовок": title,
                "Сслыка": href,
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

    with open(f"data/{parsed_sport[1:-1]}.json", "a+", encoding="utf-8") as file:
        json.dump(news_info, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
