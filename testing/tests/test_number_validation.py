import pytest

from championat_parser import is_valid_number
from testing.src.assertions import Assertions


class TestNumberValidation:
    @pytest.mark.parametrize("number", list(map(str, [i for i in range(1, 11)])))
    def test_number_validation_positive(self, number):
        Assertions.assert_number_validation(
            is_valid_number(number, 10),
            True,
            f"Валидное число {number} не прошло проверку"
        )

    @pytest.mark.parametrize("number", ["-6", "0", "13", "tiger", "2G"])
    def test_number_validation_negative(self, number):
        Assertions.assert_number_validation(
            is_valid_number(number, 10),
            False,
            f"Не валидное число {number} прошло проверку"
        )
