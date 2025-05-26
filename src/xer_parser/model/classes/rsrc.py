import json
from typing import Optional, Any
from pydantic import BaseModel, Field


class Resource(BaseModel):
    rsrc_id: Optional[int] = Field(default=None, alias="rsrc_id")
    parent_rsrc_id: Optional[int] = Field(default=None, alias="parent_rsrc_id")
    clndr_id: Optional[int] = Field(default=None, alias="clndr_id")
    role_id: Optional[int] = Field(default=None, alias="role_id")
    shift_id: Optional[int] = Field(default=None, alias="shift_id") # Assuming int
    user_id: Optional[int] = Field(default=None, alias="user_id") # Assuming int
    pobs_id: Optional[int] = Field(default=None, alias="pobs_id") # Assuming int
    guid: Optional[str] = Field(default=None, alias="guid")
    rsrc_seq_num: Optional[int] = Field(default=None, alias="rsrc_seq_num") # Assuming int
    email_addr: Optional[str] = Field(default=None, alias="email_addr")
    employee_code: Optional[str] = Field(default=None, alias="employee_code")
    office_phone: Optional[str] = Field(default=None, alias="office_phone")
    other_phone: Optional[str] = Field(default=None, alias="other_phone")
    rsrc_name: Optional[str] = Field(default=None, alias="rsrc_name")
    rsrc_short_name: Optional[str] = Field(default=None, alias="rsrc_short_name")
    rsrc_title_name: Optional[str] = Field(default=None, alias="rsrc_title_name")
    def_qty_per_hr: Optional[float] = Field(default=None, alias="def_qty_per_hr") # Assuming float
    cost_qty_type: Optional[str] = Field(default=None, alias="cost_qty_type")
    ot_factor: Optional[float] = Field(default=None, alias="ot_factor") # Assuming float
    active_flag: Optional[str] = Field(default=None, alias="active_flag") # Y/N
    auto_compute_act_flag: Optional[str] = Field(default=None, alias="auto_compute_act_flag") # Y/N
    def_cost_qty_link_flag: Optional[str] = Field(default=None, alias="def_cost_qty_link_flag") # Y/N
    ot_flag: Optional[str] = Field(default=None, alias="ot_flag") # Y/N
    curr_id: Optional[int] = Field(default=None, alias="curr_id")
    unit_id: Optional[int] = Field(default=None, alias="unit_id") # Assuming int
    rsrc_type: Optional[str] = Field(default=None, alias="rsrc_type")
    location_id: Optional[int] = Field(default=None, alias="location_id")
    rsrc_notes: Optional[str] = Field(default=None, alias="rsrc_notes")
    load_tasks_flag: Optional[str] = Field(default=None, alias="load_tasks_flag") # Y/N
    level_flag: Optional[str] = Field(default=None, alias="level_flag") # Y/N
    last_checksum: Optional[str] = Field(default=None, alias="last_checksum") # Original was assigned level_flag

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_id(self) -> Optional[int]:
        return self.rsrc_id

    def get_tsv(self) -> list[Any]:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("rsrc_id", "")) if model_data.get("rsrc_id") is not None else "",
            str(model_data.get("parent_rsrc_id", "")) if model_data.get("parent_rsrc_id") is not None else "",
            str(model_data.get("clndr_id", "")) if model_data.get("clndr_id") is not None else "",
            str(model_data.get("role_id", "")) if model_data.get("role_id") is not None else "",
            str(model_data.get("shift_id", "")) if model_data.get("shift_id") is not None else "",
            str(model_data.get("user_id", "")) if model_data.get("user_id") is not None else "",
            str(model_data.get("pobs_id", "")) if model_data.get("pobs_id") is not None else "",
            model_data.get("guid", "") if model_data.get("guid") is not None else "",
            str(model_data.get("rsrc_seq_num", "")) if model_data.get("rsrc_seq_num") is not None else "",
            model_data.get("email_addr", "") if model_data.get("email_addr") is not None else "",
            model_data.get("employee_code", "") if model_data.get("employee_code") is not None else "",
            model_data.get("office_phone", "") if model_data.get("office_phone") is not None else "",
            model_data.get("other_phone", "") if model_data.get("other_phone") is not None else "",
            model_data.get("rsrc_name", "") if model_data.get("rsrc_name") is not None else "",
            model_data.get("rsrc_short_name", "") if model_data.get("rsrc_short_name") is not None else "",
            model_data.get("rsrc_title_name", "") if model_data.get("rsrc_title_name") is not None else "",
            str(model_data.get("def_qty_per_hr", "")) if model_data.get("def_qty_per_hr") is not None else "",
            model_data.get("cost_qty_type", "") if model_data.get("cost_qty_type") is not None else "",
            str(model_data.get("ot_factor", "")) if model_data.get("ot_factor") is not None else "",
            model_data.get("active_flag", "") if model_data.get("active_flag") is not None else "",
            model_data.get("auto_compute_act_flag", "") if model_data.get("auto_compute_act_flag") is not None else "",
            model_data.get("def_cost_qty_link_flag", "") if model_data.get("def_cost_qty_link_flag") is not None else "",
            model_data.get("ot_flag", "") if model_data.get("ot_flag") is not None else "",
            str(model_data.get("curr_id", "")) if model_data.get("curr_id") is not None else "",
            str(model_data.get("unit_id", "")) if model_data.get("unit_id") is not None else "",
            model_data.get("rsrc_type", "") if model_data.get("rsrc_type") is not None else "",
            str(model_data.get("location_id", "")) if model_data.get("location_id") is not None else "",
            model_data.get("rsrc_notes", "") if model_data.get("rsrc_notes") is not None else "",
            model_data.get("load_tasks_flag", "") if model_data.get("load_tasks_flag") is not None else "",
            model_data.get("level_flag", "") if model_data.get("level_flag") is not None else "",
            model_data.get("last_checksum", "") if model_data.get("last_checksum") is not None else "",
        ]

    @property
    def parent(self) -> Optional[int]:
        return self.parent_rsrc_id

    def __repr__(self) -> str:
        name = self.rsrc_name if self.rsrc_name is not None else "Unknown Resource"
        return f"<{name} (ID: {self.rsrc_id if self.rsrc_id is not None else 'N/A'})>"

    def __str__(self) -> str:
        return self.rsrc_name if self.rsrc_name is not None else super().__str__()

    def toJson(self) -> str: # Note: Pydantic models have .model_dump_json()
        return self.model_dump_json(by_alias=True)

    class Config:
        arbitrary_types_allowed = True
