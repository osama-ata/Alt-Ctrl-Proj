from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class UDFValue(BaseModel):
    udf_type_id: Optional[int] = Field(default=None, alias="udf_type_id")
    fk_id: Optional[int] = Field(default=None, alias="fk_id") # Foreign key to another table's record
    proj_id: Optional[int] = Field(default=None, alias="proj_id") # Project ID, if UDF is project-specific
    udf_date: Optional[datetime] = Field(default=None, alias="udf_date")
    udf_number: Optional[float] = Field(default=None, alias="udf_number")
    udf_text: Optional[str] = Field(default=None, alias="udf_text")
    udf_code_id: Optional[int] = Field(default=None, alias="udf_code_id") # FK to UDFCode if data_type is Code

    data: Any = Field(default=None, exclude=True)

    def _format_date_for_tsv(self, dt_val: Any) -> str:
        if dt_val is None: return ""
        # Assuming XER dates are like "2000-12-31 00:00"
        if isinstance(dt_val, datetime): return dt_val.strftime("%Y-%m-%d %H:%M") 
        return str(dt_val)

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        
        def s(value: Any) -> str:
            return "" if value is None else str(value)

        return [
            "%R",
            s(model_data.get("udf_type_id")),
            s(model_data.get("fk_id")),
            s(model_data.get("proj_id")),
            self._format_date_for_tsv(self.udf_date), # Use instance attribute for formatting
            s(model_data.get("udf_number")),
            s(model_data.get("udf_text")),
            s(model_data.get("udf_code_id")),
        ]

    def __repr__(self) -> str:
        parts = []
        if self.udf_text is not None:
            parts.append(f"text='{self.udf_text}'")
        if self.udf_number is not None:
            parts.append(f"number={self.udf_number}")
        if self.udf_date is not None:
            parts.append(f"date='{self.udf_date.strftime('%Y-%m-%d') if self.udf_date else 'N/A'}'")
        if self.udf_code_id is not None:
            parts.append(f"code_id={self.udf_code_id}")
        
        value_str = ", ".join(parts)
        return f"<UDFValue type_id={self.udf_type_id or 'N/A'} fk_id={self.fk_id or 'N/A'} ({value_str})>"
