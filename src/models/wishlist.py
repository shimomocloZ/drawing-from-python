# -*- coding: utf-8 -*-
import dataclasses


@dataclasses.dataclass
class Wishlist:
    id: int = 0
    priority: list[str] = None
    number_of_buy: list[int] = None

    def __post_init__(self):
        self.id = int(self.id)
        self.priority = self.convert_priority(self.priority)
        self.number_of_buy = self.convert_buy_of_number(self.number_of_buy)

    def convert_priority(self, values: str) -> None:
        if type(values) == str and ';' in values:
            return values.split(';')
        # it is array or single string.
        else:
            return values

    def convert_buy_of_number(self, values: str) -> None:
        if type(values) == str:
            if ';' in values:
                return [int(i) for i in values.split(';')]
            # it is single str
            else:
                return [int(values)]
        # it is array.
        else:
            return values
