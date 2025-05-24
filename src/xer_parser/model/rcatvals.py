from typing import Any

from xer_parser.model.classes.rcatval import RCatVal

__all__ = ["RCatVals"]


class RCatVals:
    def __init__(self) -> None:
        self.index: int = 0
        self._rcatvals: list[RCatVal] = []

    def add(self, params: dict[str, Any]) -> None:
        self._rcatvals.append(RCatVal(params))

    def get_tsv(self) -> list[list[str]]:
        tsv: list[list[str]] = []
        if len(self._rcatvals) > 0:
            tsv.append(["%T", "RCATVAL"])
            tsv.append(
                [
                    "%F",
                    "rsrc_catg_id",
                    "rsrc_catg_type_id",
                    "rsrc_catg_short_name",
                    "rsrc_catg_name",
                    "parent_rsrc_catg_id",
                ]
            )
            for rc in self._rcatvals:
                tsv.append(rc.get_tsv())
        return tsv

    def find_by_id(self, id: str) -> RCatVal | list[RCatVal]:
        obj: list[RCatVal] = list(
            filter(lambda x: getattr(x, "rsrc_catg_id", None) == id, self._rcatvals)
        )
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self) -> int:
        return len(self._rcatvals)

    def __len__(self) -> int:
        return len(self._rcatvals)

    def __iter__(self) -> "RCatVals":
        return self

    def __next__(self) -> RCatVal:
        if self.index >= len(self._rcatvals):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rcatvals[idx]
