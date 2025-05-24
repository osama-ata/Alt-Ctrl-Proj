from __future__ import annotations

from typing import Any, ClassVar


class PCatType:
    obj_list: ClassVar[list[PCatType]] = []

    def __init__(self, params: dict[str, Any]) -> None:
        self.proj_catg_type_id: int | None = (
            int(params["proj_catg_type_id"].strip())
            if params.get("proj_catg_type_id") is not None
            else None
        )
        self.seq_num: int | None = (
            int(params["seq_num"].strip())
            if params.get("seq_num") is not None
            else None
        )
        self.proj_catg_short_len: str | None = (
            str(params["proj_catg_short_len"].strip())
            if params.get("proj_catg_short_len") is not None
            else None
        )
        self.proj_catg_type: str | None = (
            str(params["proj_catg_type"].strip())
            if params.get("proj_catg_type") is not None
            else None
        )
        self.export_flag: int | None = (
            int(params["export_flag"])
            if params.get("export_flag") is not None
            else None
        )
        PCatType.obj_list.append(self)

    def get_id(self) -> int | None:
        return self.proj_catg_type_id

    def get_tsv(self) -> list[str | int | None]:
        tsv: list[str | int | None] = [
            "%R",
            self.proj_catg_type_id,
            self.seq_num,
            self.proj_catg_short_len,
            self.proj_catg_type,
            self.export_flag,
        ]
        return tsv

    @classmethod
    def find_by_id(cls, id: int) -> PCatType | list[PCatType]:
        obj = [x for x in cls.obj_list if getattr(x, "proj_catg_type_id", None) == id]
        if obj:
            return obj[0]
        return obj

    def __repr__(self) -> str:
        return str(self.proj_catg_type) if self.proj_catg_type is not None else ""
