import json
import asyncio
import random

import aiohttp

from bs4 import BeautifulSoup
from faker import Faker

news_info = []


def main_prompt():
    kinds_of_sport = {
        "Все новости": "/",
        "Футбол": "/football/",
        "Хоккей": "/hockey/",
        "Бокс": "/boxing/",
        "Теннис": "/tennis/",
        "Фигурное катание": "/figureskating/"
    }

    for sport in enumerate(kinds_of_sport.keys(), start=1):
        print(f"{sport[0]}. {sport[1]}")

    input_sport = input("Из предложенного списка ведите число, это будет вид спорта, который мы будем "
                        "парсить с сайта championat.com: ")
    while True:
        try:
            input_sport = int(input_sport)
        except ValueError:
            input_sport = input("Вы ввели не число, попробуйте снова: ")

            continue

        if not 0 < input_sport < len(kinds_of_sport):
            input_sport = input("Вы ввели неправильное число, попробуйте снова: ")

            continue

        try:
            dict_key = list(kinds_of_sport.keys())[input_sport - 1]
            parsed_sport = kinds_of_sport[dict_key]
        except IndexError:
            input_sport = input("Вы ввели неправильное число, попробуйте снова: ")

            continue

        break

    pages_amount = input("Сколько страниц с новостями будем просматривать? "
                         "Введите целое число (от 1 до 100): ")
    while True:
        try:
            pages_amount = int(pages_amount)
        except ValueError:
            pages_amount = input("Введите, пожалуйста, число в пределах от 1 до 100 (было введено не число): ")

            continue

        if not (0 < pages_amount < 101):
            pages_amount = input("Введите, пожалуйста, число в пределах от 1 до 100 "
                                 "(было введено число не из этого диапазона): ")

            continue

        break

    return parsed_sport, pages_amount


async def extract_comments(session, all_comments, headers):
    url = f"https://c.rambler.ru/api/app/5/comments-count?"

    for comment in all_comments:
        url += "xid=" + comment.get("data-id") + "&"

    async with session.get(url=url, headers=headers) as response:
        json_data = await response.text()

    json_obj = json.loads(json_data)

    return json_obj["xids"]


async def get_page_data(session, page, parsed_sport):
    Faker.seed(random.randint(0, 100))
    fake = Faker()

    headers = {
        "Accept": "*/*",
        "User-Agent": fake.chrome()
    }

    url = f"https://www.championat.com/news{parsed_sport}{page}.html"

    async with session.get(url=url, headers=headers) as response:
        src = await response.text()
        soup = BeautifulSoup(src, "lxml")
        all_news = soup.find_all("div", class_="news-item")

        all_comments = soup.find_all("span", class_="js-comments-count")
        comments_dict = await extract_comments(session, all_comments, headers)

        for new in all_news:
            new_time = new.find("div", class_="news-item__time")
            new_content = new.find("div", class_="news-item__content")

            title = new_content.find_all("a")[0].text
            href = "https://www.championat.com" + new_content.find_all("a")[0].get("href")
            tag = new.find("a", class_="news-item__tag").text
            date = new_time.text

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
                "Дата публикации": date
            })

        print(f"[INFO] Обработана страница {page}")


async def gather_data(pages_amount, parsed_sport):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for page in range(1, pages_amount + 1):
            task = asyncio.create_task(get_page_data(session, page, parsed_sport))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    parsed_sport, pages_amount = main_prompt()
    asyncio.run(gather_data(pages_amount, parsed_sport))

    with open(f"news.json", "w", encoding="utf-8") as file:
        json.dump(news_info, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
