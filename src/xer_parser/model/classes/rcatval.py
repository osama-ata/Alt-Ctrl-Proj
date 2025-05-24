from __future__ import annotations

from typing import Any, ClassVar


class RCatVal:
    obj_list: ClassVar[list[RCatVal]] = []
    rsrc_catg_id: str | None
    rsrc_catg_type_id: str | None
    rsrc_catg_short_name: str | None
    rsrc_catg_name: str | None
    parent_rsrc_catg_id: str | None

    def __init__(self, params: dict[str, Any]) -> None:
        self.rsrc_catg_id = (
            str(params.get("rsrc_catg_id")).strip()
            if params.get("rsrc_catg_id") is not None
            else None
        )
        self.rsrc_catg_type_id = (
            str(params.get("rsrc_catg_type_id")).strip()
            if params.get("rsrc_catg_type_id") is not None
            else None
        )
        self.rsrc_catg_short_name = (
            str(params.get("rsrc_catg_short_name")).strip()
            if params.get("rsrc_catg_short_name") is not None
            else None
        )
        self.rsrc_catg_name = (
            str(params.get("rsrc_catg_name")).strip()
            if params.get("rsrc_catg_name") is not None
            else None
        )
        self.parent_rsrc_catg_id = (
            str(params.get("parent_rsrc_catg_id")).strip()
            if params.get("parent_rsrc_catg_id") is not None
            else None
        )
        RCatVal.obj_list.append(self)

    def get_id(self) -> str | None:
        return self.rsrc_catg_id

    def get_tsv(self) -> list[str]:
        return [
            "%R",
            str(self.rsrc_catg_id) if self.rsrc_catg_id is not None else "",
            str(self.rsrc_catg_type_id) if self.rsrc_catg_type_id is not None else "",
            str(self.rsrc_catg_short_name)
            if self.rsrc_catg_short_name is not None
            else "",
            str(self.rsrc_catg_name) if self.rsrc_catg_name is not None else "",
            str(self.parent_rsrc_catg_id)
            if self.parent_rsrc_catg_id is not None
            else "",
        ]

    @classmethod
    def find_by_id(cls, id: str) -> RCatVal | list[RCatVal]:
        obj: list[RCatVal] = list(
            filter(lambda x: getattr(x, "rsrc_catg_id", None) == id, cls.obj_list)
        )
        if len(obj) > 0:
            return obj[0]
        return obj

    def __repr__(self) -> str:
        return self.rsrc_catg_name or ""
