from typing import Any

from xer_parser.model.classes.udfvalue import UDFValue

__all__ = ["UDFValues"]


class UDFValues:
    def __init__(self) -> None:
        self.index: int = 0
        self._udfvalues: list[UDFValue] = []

    def add(self, params: Any) -> None:
        self._udfvalues.append(UDFValue(params))

    def get_tsv(self) -> list[list[str]]:
        if len(self._udfvalues) > 0:
            tsv: list[list[str]] = []
            tsv.append(["%T", "UDFVALUE"])
            tsv.append(
                [
                    "%F",
                    "udf_type_id",
                    "fk_id",
                    "proj_id",
                    "udf_date",
                    "udf_number",
                    "udf_text",
                    "udf_code_id",
                ]
            )
            for udfval in self._udfvalues:
                tsv.append(udfval.get_tsv())
            return tsv
        return []

    def find_by_id(self, id: Any) -> UDFValue | list[UDFValue]:
        obj: list[UDFValue] = list(
            filter(lambda x: getattr(x, "udf_type_id", None) == id, self._udfvalues)
        )
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self) -> int:
        return len(self._udfvalues)

    def __len__(self) -> int:
        return len(self._udfvalues)

    def __iter__(self) -> "UDFValues":
        return self

    def __next__(self) -> UDFValue:
        if self.index >= len(self._udfvalues):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._udfvalues[idx]
