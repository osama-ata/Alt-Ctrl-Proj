from typing import Any

from xer_parser.model.classes.acttype import ActType

__all__ = ["ActTypes"]


class ActTypes:
    def __init__(self) -> None:
        self.index: int = 0
        self._activitytypes: list[ActType] = []

    def add(self, params: Any) -> None:
        self._activitytypes.append(ActType(params))

    def find_by_id(self, id: Any) -> ActType | list[ActType]:
        obj: list[ActType] = list(
            filter(lambda x: x.actv_code_type_id == id, self._activitytypes)
        )
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self) -> list[list[str]]:
        if len(self._activitytypes) > 0:
            tsv: list[list[str]] = []
            tsv.append(["%T", "ACTVTYPE"])
            tsv.append(
                [
                    "%F",
                    "actv_code_type_id",
                    "actv_short_len",
                    "seq_num",
                    "actv_code_type",
                    "proj_id",
                    "wbs_id",
                    "actv_code_type_scope",
                ]
            )
            for acttyp in self._activitytypes:
                tsv.append(acttyp.get_tsv())
            return tsv
        return []

    def count(self) -> int:
        return len(self._activitytypes)

    def __len__(self) -> int:
        return len(self._activitytypes)

    def __iter__(self) -> "ActTypes":
        return self

    def __next__(self) -> ActType:
        if self.index >= len(self._activitytypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._activitytypes[idx]
