from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ResourceRate(BaseModel):
    rsrc_rate_id: Optional[int] = Field(default=None, alias="rsrc_rate_id")
    rsrc_id: Optional[int] = Field(default=None, alias="rsrc_id")
    max_qty_per_hr: Optional[float] = Field(default=None, alias="max_qty_per_hr")
    cost_per_qty: Optional[float] = Field(default=None, alias="cost_per_qty")
    start_date: Optional[datetime] = Field(default=None, alias="start_date")
    shift_period_id: Optional[int] = Field(default=None, alias="shift_period_id")
    cost_per_qty2: Optional[float] = Field(default=None, alias="cost_per_qty2")
    cost_per_qty3: Optional[float] = Field(default=None, alias="cost_per_qty3")
    cost_per_qty4: Optional[float] = Field(default=None, alias="cost_per_qty4")
    cost_per_qty5: Optional[float] = Field(default=None, alias="cost_per_qty5")

    data: Any = Field(default=None, exclude=True)

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)

        start_date_str = ""
        if model_data.get("start_date"):
            dt_obj = self.start_date
            if isinstance(dt_obj, datetime):
                start_date_str = dt_obj.strftime("%Y-%m-%d %H:%M")
            elif isinstance(dt_obj, str): # If model_dump already stringified it
                start_date_str = dt_obj
        
        return [
            "%R",
            str(model_data.get("rsrc_rate_id", "")) if model_data.get("rsrc_rate_id") is not None else "",
            str(model_data.get("rsrc_id", "")) if model_data.get("rsrc_id") is not None else "",
            str(model_data.get("max_qty_per_hr", "")) if model_data.get("max_qty_per_hr") is not None else "",
            str(model_data.get("cost_per_qty", "")) if model_data.get("cost_per_qty") is not None else "",
            start_date_str,
            str(model_data.get("shift_period_id", "")) if model_data.get("shift_period_id") is not None else "",
            str(model_data.get("cost_per_qty2", "")) if model_data.get("cost_per_qty2") is not None else "",
            str(model_data.get("cost_per_qty3", "")) if model_data.get("cost_per_qty3") is not None else "",
            str(model_data.get("cost_per_qty4", "")) if model_data.get("cost_per_qty4") is not None else "",
            str(model_data.get("cost_per_qty5", "")) if model_data.get("cost_per_qty5") is not None else "",
        ]

    def __repr__(self) -> str:
        rate_id = str(self.rsrc_rate_id) if self.rsrc_rate_id is not None else "N/A"
        res_id = str(self.rsrc_id) if self.rsrc_id is not None else "N/A"
        return f"<ResourceRate ID: {rate_id} (Resource ID: {res_id})>"
