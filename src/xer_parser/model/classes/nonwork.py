from typing import Optional, Any
from pydantic import BaseModel, Field


class NonWork(BaseModel):
    nonwork_type_id: Optional[int] = Field(default=None, alias="nonwork_type_id") # Assuming int
    seq_num: Optional[int] = Field(default=None, alias="seq_num") # Assuming int
    nonwork_code: Optional[str] = Field(default=None, alias="nonwork_code")
    nonwork_type: Optional[str] = Field(default=None, alias="nonwork_type")

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_id(self): # Kept for now
        return self.nonwork_type_id

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("nonwork_type_id", "")) if model_data.get("nonwork_type_id") is not None else "",
            str(model_data.get("seq_num", "")) if model_data.get("seq_num") is not None else "",
            model_data.get("nonwork_code", "") if model_data.get("nonwork_code") is not None else "",
            model_data.get("nonwork_type", "") if model_data.get("nonwork_type") is not None else "",
        ]

    def __repr__(self):
        type_id = str(self.nonwork_type_id) if self.nonwork_type_id is not None else "N/A"
        ntype = self.nonwork_type if self.nonwork_type is not None else "Unknown"
        return f"NonWorkType (ID: {type_id} -> {ntype})"
