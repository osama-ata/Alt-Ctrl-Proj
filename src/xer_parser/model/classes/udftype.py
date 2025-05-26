from typing import Optional, Any
from pydantic import BaseModel, Field


class UDFType(BaseModel):
    udf_type_id: Optional[int] = Field(default=None, alias="udf_type_id") # Assuming int ID
    table_name: Optional[str] = Field(default=None, alias="table_name")
    udf_type_name: Optional[str] = Field(default=None, alias="udf_type_name")
    udf_type_label: Optional[str] = Field(default=None, alias="udf_type_label")
    logical_data_type: Optional[str] = Field(default=None, alias="logical_data_type")
    super_flag: Optional[str] = Field(default=None, alias="super_flag") # Y/N
    indicator_expression: Optional[str] = Field(default=None, alias="indicator_expression")
    summary_indicator_expression: Optional[str] = Field(default=None, alias="summary_indicator_expression")
    export_flag: Optional[str] = Field(default=None, alias="export_flag") # Y/N

    data: Any = Field(default=None, exclude=True)

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        
        def s(value: Any) -> str:
            return "" if value is None else str(value)

        return [
            "%R",
            s(model_data.get("udf_type_id")),
            s(model_data.get("table_name")),
            s(model_data.get("udf_type_name")),
            s(model_data.get("udf_type_label")),
            s(model_data.get("logical_data_type")),
            s(model_data.get("super_flag")),
            s(model_data.get("indicator_expression")),
            s(model_data.get("summary_indicator_expression")),
            s(model_data.get("export_flag")),
        ]

    def __repr__(self) -> str:
        return self.udf_type_name if self.udf_type_name is not None else "UDFType"
