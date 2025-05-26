from typing import Optional, Any
from pydantic import BaseModel, Field


class FinTmpl(BaseModel):
    fintmpl_id: Optional[int] = Field(default=None, alias="fintmpl_id") # Assuming int from context
    fintmpl_name: Optional[str] = Field(default=None, alias="fintmpl_name")
    default_flag: Optional[str] = Field(default=None, alias="default_flag") # 'Y'/'N'

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_id(self): # Kept for now
        return self.fintmpl_id

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("fintmpl_id", "")) if model_data.get("fintmpl_id") is not None else "",
            model_data.get("fintmpl_name", "") if model_data.get("fintmpl_name") is not None else "",
            model_data.get("default_flag", "") if model_data.get("default_flag") is not None else "",
        ]

    def __repr__(self):
        name = self.fintmpl_name if self.fintmpl_name is not None else "Unknown FinTmpl"
        return f"<{name} (ID: {self.fintmpl_id if self.fintmpl_id is not None else 'N/A'})>"
