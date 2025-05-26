from typing import Optional, Any
from pydantic import BaseModel, Field


class Role(BaseModel):
    role_id: Optional[int] = Field(default=None, alias="role_id")
    parent_role_id: Optional[int] = Field(default=None, alias="parent_role_id")
    seq_num: Optional[int] = Field(default=None, alias="seq_num")
    role_name: Optional[str] = Field(default=None, alias="role_name")
    role_short_name: Optional[str] = Field(default=None, alias="role_short_name")
    pobs_id: Optional[int] = Field(default=None, alias="pobs_id") # Assuming int
    def_cost_qty_link_flag: Optional[str] = Field(default=None, alias="def_cost_qty_link_flag") # Y/N
    cost_qty_type: Optional[str] = Field(default=None, alias="cost_qty_type")
    role_descr: Optional[str] = Field(default=None, alias="role_descr")
    last_checksum: Optional[str] = Field(default=None, alias="last_checksum") # Assuming this was intended to map to 'last_checksum'

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("role_id", "")) if model_data.get("role_id") is not None else "",
            str(model_data.get("parent_role_id", "")) if model_data.get("parent_role_id") is not None else "",
            str(model_data.get("seq_num", "")) if model_data.get("seq_num") is not None else "",
            model_data.get("role_name", "") if model_data.get("role_name") is not None else "",
            model_data.get("role_short_name", "") if model_data.get("role_short_name") is not None else "",
            str(model_data.get("pobs_id", "")) if model_data.get("pobs_id") is not None else "",
            model_data.get("def_cost_qty_link_flag", "") if model_data.get("def_cost_qty_link_flag") is not None else "",
            model_data.get("cost_qty_type", "") if model_data.get("cost_qty_type") is not None else "",
            model_data.get("role_descr", "") if model_data.get("role_descr") is not None else "",
            model_data.get("last_checksum", "") if model_data.get("last_checksum") is not None else "",
        ]

    def __repr__(self) -> str:
        name = self.role_name if self.role_name is not None else "Unknown Role"
        return f"<{name} (ID: {self.role_id if self.role_id is not None else 'N/A'})>"
