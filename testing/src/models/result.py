import json

from testing.src.schemas.new import New


class Result:
    def __init__(self, news):
        self.news = news

    def validate(self):
        for new in self.news:
            New.parse_obj(new)
