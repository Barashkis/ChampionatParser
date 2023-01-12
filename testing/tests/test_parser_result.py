import os
import random

import pytest

from championat_parser import get_data
from testing.src.assertions import Assertions
from testing.src.models.result import Result


@pytest.fixture(params=[
    [sport, random.randint(1, 15)]
    for sport in ["/", "/football/", "/hockey/", "/boxing/", "/tennis/", "/figureskating/"]
])
def parsing_result(request):
    get_data(*request.param)

    yield os.path.abspath("news.json"), *request.param

    if os.path.exists("news.json"):
        os.remove("news.json")


class TestParserResult:
    def test_file_exists(self, parsing_result):
        result_file_path, sport, pages_amount = parsing_result

        Assertions.assert_path_exists(
            result_file_path,
            f"Файл с данными не был создан, вид спорта - {sport}, количество страниц - {pages_amount}"
        )

    def test_result_format(self, parsing_result):
        result_file_path, sport, pages_amount = parsing_result

        news = Assertions.assert_result_format(
            result_file_path,
            f"Содержимое файла {result_file_path} не соответствует формату JSON, "
            f"вид спорта - {sport}, количество страниц - {pages_amount}"
        )

        Result(news).validate()

    def test_result_news_count(self, parsing_result):
        result_file_path, sport, pages_amount = parsing_result

        news = Assertions.assert_result_format(
            result_file_path,
            f"Содержимое файла {result_file_path} не соответствует формату JSON, "
            f"вид спорта - {sport}, количество страниц - {pages_amount}"
        )
        Assertions.assert_news_count(
            news,
            pages_amount,
            f"Парсер не записал в файл следующее количество новостей: {50 * pages_amount - len(news)}, "
            f"вид спорта - {sport}, количество страниц - {pages_amount}"
        )
