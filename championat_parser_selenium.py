import json
import os
import shutil
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service


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
            page_number = int(input("Какую страницу с новостями будем просматривать? "
                                    "Введите целое число (от 1 до 100): "))
            if not (0 < page_number < 100):
                raise Exception

            break
        except Exception:
            print("Введите, пожалуйста, число в пределах от 1 до 100.")

    return parsed_sport, page_number


def data_folder():
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


def get_data(url, parsed_sport, page_number):
    news_info = []

    options = webdriver.ChromeOptions()
    useragent = UserAgent()
    options.add_argument(f"user-agent={useragent.random}")
    options.add_argument('headless')
    service = Service(str(Path(str(Path.cwd()), "chromedriver.exe")))

    browser = webdriver.Chrome(
        options=options,
        service=service
    )

    print(f"Переходим на страницу новостей №{page_number}")

    if parsed_sport == "/":
        parsed_sport = "/all/"

    try:
        browser.get(url=url)
        src = browser.page_source

        with open(f"data/{parsed_sport[1:-1]}_{page_number}.html", "w", encoding="utf-8") as file:
            file.write(src)

    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()

    with open(f"data/{parsed_sport[1:-1]}_{page_number}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    all_news = soup.find_all("div", class_="news-item")

    for new in all_news:
        new_time = new.find("div", class_="news-item__time")
        new_content = new.find("div", class_="news-item__content")

        title = new_content.find_all("a")[0].text
        href = "https://www.championat.com" + new_content.find_all("a")[0].get("href")
        theme = new_content.find("a", class_="news-item__tag").text
        time = new_time.text

        try:
            comments = new_content.find("span", class_="js-comments-count").text
            if not comments:
                comments = "0"
        except AttributeError:
            comments = "0"

        news_info.append({
            "Заголовок": title,
            "Ссылка": href,
            "Тема": theme,
            "Количество комментариев": comments,
            "Дата публикации": time
        })

    print(f"# Новости со страницы записаны...")

    with open(f"data/{parsed_sport[1:-1]}.json", "a+", encoding="utf-8") as file:
        json.dump(news_info, file, indent=4, ensure_ascii=False)

    print("Работа завершена")


def main():
    data_folder()
    parsed_sport, page_number = main_prompt()
    url = f"https://www.championat.com/news{parsed_sport}{page_number}.html"
    get_data(url, parsed_sport, page_number)


if __name__ == "__main__":
    main()
