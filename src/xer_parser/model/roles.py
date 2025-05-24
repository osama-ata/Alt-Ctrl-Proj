from typing import Any

from xer_parser.model.classes.role import Role

__all__ = ["Roles"]


class Roles:
    def __init__(self) -> None:
        self.index: int = 0
        self._roles: list[Role] = []

    def get_tsv(self) -> list[list[str | int | None]]:
        if len(self._roles) > 0:
            tsv: list[list[str | int | None]] = []
            tsv.append(["%T", "ROLE"])
            tsv.append(
                [
                    "%F",
                    "role_id",
                    "parent_role_id",
                    "seq_num",
                    "role_name",
                    "role_short_name",
                    "pobs_id",
                    "def_cost_qty_link_flag",
                    "cost_qty_type",
                    "role_descr",
                    "last_checksum",
                ]
            )
            for role in self._roles:
                tsv.append(role.get_tsv())
            return tsv
        return []

    def add(self, params: dict[str, Any]) -> None:
        self._roles.append(Role(params))

    def find_by_id(self, id: int) -> Role | list[Role]:
        obj = [x for x in self._roles if getattr(x, "role_id", None) == id]
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self) -> int:
        return len(self._roles)

    def __len__(self) -> int:
        return len(self._roles)

    def __iter__(self) -> "Roles":
        return self

    def __next__(self) -> Role:
        if self.index >= len(self._roles):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._roles[idx]
