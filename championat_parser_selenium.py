import json
import os
import shutil
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service


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
            page_number = int(input("Какую страницу с новостями будем просматривать? "
                                    "Введите целое число (от 1 до 100): "))
            if not (0 < page_number < 100):
                raise Exception

            break
        except Exception:
            print("Введите, пожалуйста, число в пределах от 1 до 100.")

    return parsed_sport, page_number


# Функция создания папки data
def data_folder():
    if os.path.exists("data"):
        shutil.rmtree("data")
    os.mkdir("data")


# Функция, которая парсит страницы
def get_data(parsed_sport, page_number):
    url = f"https://www.championat.com/news{parsed_sport}{page_number}.html"

    news_info = []

    # Создаем экземпляр браузера Chrome
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

    # Извлекаем код нужной страницы с новостями
    try:
        browser.get(url=url)
        src = browser.page_source

        with open(f"data/page_{page_number}.html", "w", encoding="utf-8") as file:
            file.write(src)

    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()

    with open(f"data/page_{page_number}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    all_news = soup.find_all("div", class_="news-item")

    # Проходим по каждой новости из этой страницы и после записываем всю информацию о них в json файл
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
            "Количество комментариев": int(comments),
            "Дата публикации": time
        })

    print(f"# Новости со страницы записаны...")

    with open(f"news.json", "w", encoding="utf-8") as file:
        json.dump(news_info, file, indent=4, ensure_ascii=False)

    print("Работа завершена")


# Сначала создаем папку data, затем получаем пользовательские вводные данные и на основе их парсим новости определенного
# вида спорта определенной страницы
def main():
    data_folder()
    parsed_sport, page_number = main_prompt()
    get_data(parsed_sport, page_number)


if __name__ == "__main__":
    main()
