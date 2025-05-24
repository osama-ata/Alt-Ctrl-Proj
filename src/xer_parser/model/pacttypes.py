from typing import Any

from xer_parser.model.classes.pcattype import PCatType

__all__ = ["PCatTypes"]


class PCatTypes:
    def __init__(self) -> None:
        self.index: int = 0
        self._pcattypes: list[PCatType] = []

    def add(self, params: dict[str, Any]) -> None:
        self._pcattypes.append(PCatType(params))

    def find_by_id(self, id: int) -> PCatType | list[PCatType]:
        obj = [
            x for x in self._pcattypes if getattr(x, "proj_catg_type_id", None) == id
        ]
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self) -> list[list[str | int | None]]:
        if len(self._pcattypes) > 0:
            tsv: list[list[str | int | None]] = []
            tsv.append(["%T", "PCATTYPE"])
            tsv.append(
                [
                    "%F",
                    "proj_catg_type_id",
                    "seq_num",
                    "proj_catg_short_len",
                    "proj_catg_type",
                    "export_flag",
                ]
            )
            for acttyp in self._pcattypes:
                tsv.append(acttyp.get_tsv())
            return tsv
        return []

    def count(self) -> int:
        return len(self._pcattypes)

    def __len__(self) -> int:
        return len(self._pcattypes)

    def __iter__(self) -> "PCatTypes":
        return self

    def __next__(self) -> PCatType:
        if self.index >= len(self._pcattypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._pcattypes[idx]
