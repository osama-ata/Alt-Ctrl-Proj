from typing import Optional, Any
from pydantic import BaseModel, Field


class PCatType(BaseModel):
    proj_catg_type_id: Optional[int] = Field(default=None, alias="proj_catg_type_id")
    seq_num: Optional[int] = Field(default=None, alias="seq_num")
    proj_catg_short_len: Optional[str] = Field(default=None, alias="proj_catg_short_len") # Kept as str
    proj_catg_type: Optional[str] = Field(default=None, alias="proj_catg_type")
    export_flag: Optional[int] = Field(default=None, alias="export_flag") # Could be bool if only 0/1

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_id(self) -> Optional[int]: # Kept for now
        return self.proj_catg_type_id

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("proj_catg_type_id", "")) if model_data.get("proj_catg_type_id") is not None else "",
            str(model_data.get("seq_num", "")) if model_data.get("seq_num") is not None else "",
            model_data.get("proj_catg_short_len", "") if model_data.get("proj_catg_short_len") is not None else "",
            model_data.get("proj_catg_type", "") if model_data.get("proj_catg_type") is not None else "",
            str(model_data.get("export_flag", "")) if model_data.get("export_flag") is not None else "",
        ]

    def __repr__(self) -> str:
        name = self.proj_catg_type if self.proj_catg_type is not None else "Unknown PCatType"
        return f"<{name} (ID: {self.proj_catg_type_id if self.proj_catg_type_id is not None else 'N/A'})>"
