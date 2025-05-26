from typing import Optional, Any
from pydantic import BaseModel, Field


class PCatVal(BaseModel):
    proj_catg_id: Optional[int] = Field(default=None, alias="proj_catg_id")
    proj_catg_type_id: Optional[int] = Field(default=None, alias="proj_catg_type_id")
    seq_num: Optional[int] = Field(default=None, alias="seq_num")
    proj_catg_short_name: Optional[str] = Field(default=None, alias="proj_catg_short_name")
    parent_proj_catg_id: Optional[int] = Field(default=None, alias="parent_proj_catg_id")
    proj_catg_name: Optional[str] = Field(default=None, alias="proj_catg_name")

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_id(self) -> Optional[int]: # Kept for now
        return self.proj_catg_id

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("proj_catg_id", "")) if model_data.get("proj_catg_id") is not None else "",
            str(model_data.get("proj_catg_type_id", "")) if model_data.get("proj_catg_type_id") is not None else "",
            str(model_data.get("seq_num", "")) if model_data.get("seq_num") is not None else "",
            model_data.get("proj_catg_short_name", "") if model_data.get("proj_catg_short_name") is not None else "",
            str(model_data.get("parent_proj_catg_id", "")) if model_data.get("parent_proj_catg_id") is not None else "",
            model_data.get("proj_catg_name", "") if model_data.get("proj_catg_name") is not None else "",
        ]

    def __repr__(self) -> str:
        name = self.proj_catg_name if self.proj_catg_name is not None else "Unknown PCatVal"
        return f"<{name} (ID: {self.proj_catg_id if self.proj_catg_id is not None else 'N/A'})>"
