from typing import Any

from xer_parser.model.classes.udftype import UDFType

__all__ = ["UDFTypes"]


class UDFTypes:
    def __init__(self) -> None:
        self.index: int = 0
        self._udftypes: list[UDFType] = []

    def add(self, params: dict[str, Any]) -> None:
        self._udftypes.append(UDFType(params))

    def get_tsv(self) -> list[list[str]]:
        tsv: list[list[str]] = []
        if len(self._udftypes) > 0:
            tsv.append(["%T", "UDFTYPE"])
            tsv.append(
                [
                    "%F",
                    "udf_type_id",
                    "table_name",
                    "udf_type_name",
                    "udf_type_label",
                    "logical_data_type",
                    "super_flag",
                    "indicator_expression",
                    "summary_indicator_expression",
                    "export_flag",
                ]
            )
            for udf in self._udftypes:
                tsv.append(udf.get_tsv())
        return tsv

    def find_by_id(self, id: str) -> UDFType | list[UDFType]:
        obj: list[UDFType] = list(
            filter(lambda x: getattr(x, "udf_type_id", None) == id, self._udftypes)
        )
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self) -> int:
        return len(self._udftypes)

    def __len__(self) -> int:
        return len(self._udftypes)

    def __iter__(self) -> "UDFTypes":
        return self

    def __next__(self) -> UDFType:
        if self.index >= len(self._udftypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._udftypes[idx]
