import json
import os
import re


class Assertions:
    @staticmethod
    def assert_number_validation(actual_value, expected_value, error_message):
        assert actual_value is expected_value, error_message

    @staticmethod
    def assert_result_format(file_path, error_message):
        try:
            with open(file_path, encoding="utf-8") as file:
                result = json.load(file)
        except json.JSONDecodeError:
            assert False, error_message

        return result

    @staticmethod
    def assert_path_exists(path_to_file, error_message):
        assert os.path.exists(path_to_file), error_message

    @staticmethod
    def assert_news_count(news, pages_amount, error_message):
        assert len(news) == 50 * pages_amount, error_message

    @staticmethod
    def assert_string_matches_regex(string, regexp, error_message):
        assert re.match(regexp, string), error_message
