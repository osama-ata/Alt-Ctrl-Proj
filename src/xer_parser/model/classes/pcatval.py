from typing import Any


class PCatVal:
    proj_catg_id: str | None
    proj_catg_type_id: str | None
    seq_num: str | None
    proj_catg_short_name: str | None
    parent_proj_catg_id: str | None
    proj_catg_name: str | None

    def __init__(self, params: dict[str, Any]) -> None:
        # %F	proj_catg_id	proj_catg_type_id	seq_num	proj_catg_short_name	parent_proj_catg_id	proj_catg_name
        self.proj_catg_id = (
            str(params.get("proj_catg_id")).strip()
            if params.get("proj_catg_id") is not None
            else None
        )
        self.proj_catg_type_id = (
            str(params.get("proj_catg_type_id")).strip()
            if params.get("proj_catg_type_id") is not None
            else None
        )
        self.seq_num = (
            str(params.get("seq_num")).strip()
            if params.get("seq_num") is not None
            else None
        )
        self.proj_catg_short_name = (
            str(params.get("proj_catg_short_name")).strip()
            if params.get("proj_catg_short_name") is not None
            else None
        )
        self.parent_proj_catg_id = (
            str(params.get("parent_proj_catg_id")).strip()
            if params.get("parent_proj_catg_id") is not None
            else None
        )
        self.proj_catg_name = (
            str(params.get("proj_catg_name")).strip()
            if params.get("proj_catg_name") is not None
            else None
        )

    def get_id(self) -> str | None:
        return self.proj_catg_id

    def get_tsv(self) -> list[str]:
        tsv: list[str] = [
            "%R",
            str(self.proj_catg_id) if self.proj_catg_id is not None else "",
            str(self.proj_catg_type_id) if self.proj_catg_type_id is not None else "",
            str(self.seq_num) if self.seq_num is not None else "",
            str(self.proj_catg_short_name)
            if self.proj_catg_short_name is not None
            else "",
            str(self.parent_proj_catg_id)
            if self.parent_proj_catg_id is not None
            else "",
            str(self.proj_catg_name) if self.proj_catg_name is not None else "",
        ]
        return tsv

    def __repr__(self) -> str:
        return self.proj_catg_name or ""
