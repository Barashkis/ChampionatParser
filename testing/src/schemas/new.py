from pydantic import BaseModel, Field, validator

from testing.src.assertions import Assertions


class New(BaseModel):
    title: str = Field(alias="Заголовок")
    href: str = Field(alias="Ссылка")
    tag: str = Field(alias="Тег")
    comments: int = Field(alias="Количество комментариев")
    time: str = Field(alias="Дата публикации")

    @validator("href")
    def validate_href(cls, href):
        Assertions.assert_string_matches_regex(
            href,
            r"https://(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}",
            "Поле href не соответсвует нужному формату"
        )

        return href

    @validator("time")
    def validate_time(cls, time):
        Assertions.assert_string_matches_regex(
            time,
            r"^\d{1,2}:\d{1,2}$",
            "Поле time не соответсвует нужному формату"
        )

        return time
