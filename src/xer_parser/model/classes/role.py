from typing import Any, ClassVar


class Role:
    obj_list: ClassVar[list["Role"]] = []

    def __init__(self, params: dict[str, Any]) -> None:
        try:
            self.role_id: int | None = (
                int(params["role_id"])
                if params.get("role_id") not in (None, "")
                else None
            )
        except Exception:
            self.role_id = None
        try:
            self.parent_role_id: int | None = (
                int(params["parent_role_id"])
                if params.get("parent_role_id") not in (None, "")
                else None
            )
        except Exception:
            self.parent_role_id = None
        try:
            self.seq_num: int | None = (
                int(params["seq_num"])
                if params.get("seq_num") not in (None, "")
                else None
            )
        except Exception:
            self.seq_num = None
        self.role_name: str | None = (
            str(params["role_name"]) if params.get("role_name") is not None else None
        )
        self.role_short_name: str | None = (
            str(params["role_short_name"])
            if params.get("role_short_name") is not None
            else None
        )
        self.pobs_id: Any = (
            params.get("pobs_id") if params.get("pobs_id") is not None else None
        )
        self.def_cost_qty_link_flag: Any = (
            params.get("def_cost_qty_link_flag")
            if params.get("def_cost_qty_link_flag") is not None
            else None
        )
        self.cost_qty_type: Any = (
            params.get("cost_qty_type")
            if params.get("cost_qty_type") is not None
            else None
        )
        self.role_descr: str | None = (
            str(params["role_descr"]) if params.get("role_descr") is not None else None
        )
        self.last_checksum: str | None = (
            str(params["role_descr"]) if params.get("role_descr") is not None else None
        )

        Role.obj_list.append(self)

    def get_tsv(self) -> list[str | int | None]:
        tsv: list[str | int | None] = [
            "%R",
            self.role_id,
            self.parent_role_id,
            self.seq_num,
            self.role_name,
            self.role_short_name,
            self.pobs_id,
            self.def_cost_qty_link_flag,
            self.cost_qty_type,
            self.role_descr,
            self.last_checksum,
        ]
        return tsv

    def __repr__(self) -> str:
        return str(self.role_name) if self.role_name is not None else ""
