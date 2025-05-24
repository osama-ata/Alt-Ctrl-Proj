from typing import Any

from xer_parser.model.classes.pcatval import PCatVal

__all__ = ["PCatVals"]


class PCatVals:
    def __init__(self) -> None:
        self.index: int = 0
        self._PCatVals: list[PCatVal] = []

    def add(self, params: dict[str, Any]) -> None:
        self._PCatVals.append(PCatVal(params))

    def get_tsv(self) -> list[list[str]]:
        tsv: list[list[str]] = []
        if len(self._PCatVals) > 0:
            tsv.append(["%T", "PCATVAL"])
            tsv.append(
                [
                    "%F",
                    "proj_catg_id",
                    "proj_catg_type_id",
                    "seq_num",
                    "proj_catg_short_name",
                    "parent_proj_catg_id",
                    "proj_catg_name",
                ]
            )
            for pcatval in self._PCatVals:
                tsv.append(pcatval.get_tsv())
        return tsv

    def find_by_id(self, id: str) -> PCatVal | list[PCatVal]:
        obj: list[PCatVal] = list(
            filter(lambda x: getattr(x, "proj_catg_id", None) == id, self._PCatVals)
        )
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self) -> int:
        return len(self._PCatVals)

    def __len__(self) -> int:
        return len(self._PCatVals)

    def __iter__(self) -> "PCatVals":
        return self

    def __next__(self) -> PCatVal:
        if self.index >= len(self._PCatVals):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._PCatVals[idx]
