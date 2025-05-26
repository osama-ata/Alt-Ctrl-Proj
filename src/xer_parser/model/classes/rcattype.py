from typing import Optional, Any
from pydantic import BaseModel, Field


class RCatType(BaseModel):
    rsrc_catg_type_id: Optional[int] = Field(default=None, alias="rsrc_catg_type_id")
    seq_num: Optional[int] = Field(default=None, alias="seq_num") # Assuming int
    rsrc_catg_short_len: Optional[int] = Field(default=None, alias="rsrc_catg_short_len") # Assuming int
    rsrc_catg_type: Optional[str] = Field(default=None, alias="rsrc_catg_type")

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("rsrc_catg_type_id", "")) if model_data.get("rsrc_catg_type_id") is not None else "",
            str(model_data.get("seq_num", "")) if model_data.get("seq_num") is not None else "",
            str(model_data.get("rsrc_catg_short_len", "")) if model_data.get("rsrc_catg_short_len") is not None else "",
            model_data.get("rsrc_catg_type", "") if model_data.get("rsrc_catg_type") is not None else "",
        ]

    def get_id(self) -> Optional[int]: # Kept for now
        return self.rsrc_catg_type_id

    def __repr__(self) -> str:
        name = self.rsrc_catg_type if self.rsrc_catg_type is not None else "Unknown RCatType"
        return f"<{name} (ID: {self.rsrc_catg_type_id if self.rsrc_catg_type_id is not None else 'N/A'})>"
