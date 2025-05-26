import locale
from typing import Optional, Any
from pydantic import BaseModel, Field


class RoleRate(BaseModel):
    role_rate_id: Optional[int] = Field(default=None, alias="role_rate_id")
    role_id: Optional[int] = Field(default=None, alias="role_id")
    cost_per_qty: Optional[float] = Field(default=None, alias="cost_per_qty")
    cost_per_qty2: Optional[float] = Field(default=None, alias="cost_per_qty2")
    cost_per_qty3: Optional[float] = Field(default=None, alias="cost_per_qty3")
    cost_per_qty4: Optional[float] = Field(default=None, alias="cost_per_qty4")
    cost_per_qty5: Optional[float] = Field(default=None, alias="cost_per_qty5")

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("role_rate_id", "")) if model_data.get("role_rate_id") is not None else "",
            str(model_data.get("role_id", "")) if model_data.get("role_id") is not None else "",
            str(model_data.get("cost_per_qty", "")) if model_data.get("cost_per_qty") is not None else "",
            str(model_data.get("cost_per_qty2", "")) if model_data.get("cost_per_qty2") is not None else "",
            str(model_data.get("cost_per_qty3", "")) if model_data.get("cost_per_qty3") is not None else "",
            str(model_data.get("cost_per_qty4", "")) if model_data.get("cost_per_qty4") is not None else "",
            str(model_data.get("cost_per_qty5", "")) if model_data.get("cost_per_qty5") is not None else "",
        ]

    def __repr__(self) -> str:
        return f"<RoleRate ID: {self.role_rate_id if self.role_rate_id is not None else 'N/A'}>"
