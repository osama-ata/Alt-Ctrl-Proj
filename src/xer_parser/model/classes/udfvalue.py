from typing import Any


class UDFValue:
    udf_code_id: str | None = None
    udf_type_id: str | None = None
    fk_id: str | None = None
    proj_id: str | None = None
    udf_number: str | None = None
    udf_text: str | None = None
    udf_date: str | None = None

    def __init__(self, params: dict[str, Any]) -> None:
        self.udf_type_id = (
            str(params.get("udf_type_id")).strip()
            if params.get("udf_type_id") is not None
            else None
        )
        self.fk_id = (
            str(params.get("fk_id")).strip()
            if params.get("fk_id") is not None
            else None
        )
        self.proj_id = (
            str(params.get("proj_id")).strip()
            if params.get("proj_id") is not None
            else None
        )
        self.udf_date = (
            str(params.get("udf_date")).strip()
            if params.get("udf_date") is not None
            else None
        )
        self.udf_number = (
            str(params.get("udf_number")).strip()
            if params.get("udf_number") is not None
            else None
        )
        self.udf_text = (
            str(params.get("udf_text")).strip()
            if params.get("udf_text") is not None
            else None
        )
        self.udf_code_id = (
            str(params.get("udf_code_id")).strip()
            if params.get("udf_code_id") is not None
            else None
        )

    def get_id(self) -> str | None:
        return self.udf_type_id

    def get_tsv(self) -> list[str]:
        tsv: list[str] = [
            "%R",
            str(self.udf_type_id) if self.udf_type_id is not None else "",
            str(self.fk_id) if self.fk_id is not None else "",
            str(self.proj_id) if self.proj_id is not None else "",
            str(self.udf_date) if self.udf_date is not None else "",
            str(self.udf_number) if self.udf_number is not None else "",
            str(self.udf_text) if self.udf_text is not None else "",
            str(self.udf_code_id) if self.udf_code_id is not None else "",
        ]
        return tsv

    @staticmethod
    def find_by_id(code_id: str, activity_code_dict: dict[str, Any]) -> dict[str, Any]:
        return {
            k: v
            for k, v in activity_code_dict.items()
            if getattr(v, "actv_code_id", None) == code_id
        }

    def __repr__(self) -> str:
        return f"{self.udf_text or ''}->{self.udf_code_id or ''}"
