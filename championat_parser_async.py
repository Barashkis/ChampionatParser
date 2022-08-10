import json
import asyncio
import aiohttp

from bs4 import BeautifulSoup

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
       Chrome/95.0.4638.69 Safari/537.36"
}
news_info = []


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


async def extract_comments(session, soup):
    all_comments = soup.find_all("span", class_="js-comments-count")
    url = f"https://c.rambler.ru/api/app/5/comments-count?"

    for comment in all_comments:
        url += "xid=" + comment.get("data-id") + "&"

    async with session.get(url=url, headers=headers) as response:
        json_data = await response.text()

    json_obj = json.loads(json_data)

    return json_obj["xids"]


async def get_page_data(session, page, parsed_sport):
    url = f"https://www.championat.com/news{parsed_sport}{page}.html"

    async with session.get(url=url, headers=headers) as response:
        src = await response.text()
        soup = BeautifulSoup(src, "lxml")
        all_news = soup.find_all("div", class_="news-item")

        comments_dict = await extract_comments(session, soup)

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

        for page in range(1, pages_amount):
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
