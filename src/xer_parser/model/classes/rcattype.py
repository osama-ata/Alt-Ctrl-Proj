from __future__ import annotations

from typing import Any, ClassVar


class RCatType:
    obj_list: ClassVar[list[RCatType]] = []

    def __init__(self, params: dict[str, Any]) -> None:
        self.rsrc_catg_type_id: int | None = (
            int(params["rsrc_catg_type_id"].strip())
            if params.get("rsrc_catg_type_id") is not None
            else None
        )
        self.seq_num: str | None = (
            str(params["seq_num"].strip())
            if params.get("seq_num") is not None
            else None
        )
        self.rsrc_catg_short_len: str | None = (
            str(params["rsrc_catg_short_len"].strip())
            if params.get("rsrc_catg_short_len") is not None
            else None
        )
        self.rsrc_catg_type: str | None = (
            str(params["rsrc_catg_type"].strip())
            if params.get("rsrc_catg_type") is not None
            else None
        )
        RCatType.obj_list.append(self)

    def get_tsv(self) -> list[str | int | None]:
        return [
            "%R",
            self.rsrc_catg_type_id,
            self.seq_num,
            self.rsrc_catg_short_len,
            self.rsrc_catg_type,
        ]

    def get_id(self) -> int | None:
        return self.rsrc_catg_type_id

    @classmethod
    def find_by_id(cls, id: int) -> RCatType | list[RCatType]:
        obj = [x for x in cls.obj_list if getattr(x, "rsrc_catg_type_id", None) == id]
        if obj:
            return obj[0]
        return obj

    def __repr__(self) -> str:
        return str(self.rsrc_catg_type) if self.rsrc_catg_type is not None else ""
