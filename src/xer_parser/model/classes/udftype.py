from typing import Any


class UDFType:
    udf_type_id: str | None = None
    table_name: str | None = None
    udf_type_name: str | None = None
    udf_type_label: str | None = None
    logical_data_type: str | None = None
    super_flag: str | None = None
    indicator_expression: str | None = None
    summary_indicator_expression: str | None = None
    export_flag: str | None = None

    def __init__(self, params: dict[str, Any]) -> None:
        self.udf_type_id = (
            str(params.get("udf_type_id")).strip()
            if params.get("udf_type_id") is not None
            else None
        )
        self.table_name = (
            str(params.get("table_name")).strip()
            if params.get("table_name") is not None
            else None
        )
        self.udf_type_name = (
            str(params.get("udf_type_name")).strip()
            if params.get("udf_type_name") is not None
            else None
        )
        self.udf_type_label = (
            str(params.get("udf_type_label")).strip()
            if params.get("udf_type_label") is not None
            else None
        )
        self.logical_data_type = (
            str(params.get("logical_data_type")).strip()
            if params.get("logical_data_type") is not None
            else None
        )
        self.super_flag = (
            str(params.get("super_flag")).strip()
            if params.get("super_flag") is not None
            else None
        )
        self.indicator_expression = (
            str(params.get("indicator_expression")).strip()
            if params.get("indicator_expression") is not None
            else None
        )
        self.summary_indicator_expression = (
            str(params.get("summary_indicator_expression")).strip()
            if params.get("summary_indicator_expression") is not None
            else None
        )
        self.export_flag = (
            str(params.get("export_flag")).strip()
            if params.get("export_flag") is not None
            else None
        )

    def get_id(self) -> str | None:
        return self.udf_type_id

    def get_tsv(self) -> list[str]:
        tsv: list[str] = [
            "%R",
            str(self.udf_type_id) if self.udf_type_id is not None else "",
            str(self.table_name) if self.table_name is not None else "",
            str(self.udf_type_name) if self.udf_type_name is not None else "",
            str(self.udf_type_label) if self.udf_type_label is not None else "",
            str(self.logical_data_type) if self.logical_data_type is not None else "",
            str(self.super_flag) if self.super_flag is not None else "",
            str(self.indicator_expression)
            if self.indicator_expression is not None
            else "",
            str(self.summary_indicator_expression)
            if self.summary_indicator_expression is not None
            else "",
            str(self.export_flag) if self.export_flag is not None else "",
        ]
        return tsv

    def __repr__(self) -> str:
        return self.udf_type_name or ""
