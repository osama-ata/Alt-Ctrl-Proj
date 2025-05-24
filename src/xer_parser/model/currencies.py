from typing import Any

from xer_parser.model.classes.currency import Currency

__all__ = ["Currencies"]


class Currencies:
    def __init__(self) -> None:
        self.index: int = 0
        self._currencies: list[Currency] = []

    def add(self, params: Any) -> None:
        self._currencies.append(Currency(params))

    def find_by_id(self, id: Any) -> Currency | list[Currency]:
        obj: list[Currency] = list(filter(lambda x: x.curr_id == id, self._currencies))
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self) -> list[list[str]]:
        if len(self._currencies) > 0:
            tsv: list[list[str]] = []
            tsv.append(["%T", "CURRTYPE"])
            tsv.append(
                [
                    "%F",
                    "curr_id",
                    "decimal_digit_cnt",
                    "curr_symbol",
                    "decimal_symbol",
                    "digit_group_symbol",
                    "pos_curr_fmt_type",
                    "neg_curr_fmt_type",
                    "curr_type",
                    "curr_short_name",
                    "group_digit_cnt",
                    "base_exch_rate",
                ]
            )
            for cur in self._currencies:
                tsv.append(cur.get_tsv())
            return tsv
        return []

    @property
    def count(self) -> int:
        return len(self._currencies)

    def __len__(self) -> int:
        return len(self._currencies)

    def __iter__(self) -> "Currencies":
        return self

    def __next__(self) -> Currency:
        if self.index >= len(self._currencies):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._currencies[idx]
