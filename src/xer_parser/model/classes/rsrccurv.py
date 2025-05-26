import locale
from typing import Optional, Any, List
from pydantic import BaseModel, Field


class ResourceCurve(BaseModel):
    curv_id: Optional[int] = Field(default=None, alias="curv_id")
    curv_name: Optional[str] = Field(default=None, alias="curv_name") # Corrected original conditional
    default_flag: Optional[str] = Field(default=None, alias="default_flag") # Y/N

    # Percentage usage fields (0-20)
    pct_usage_0: Optional[float] = Field(default=None, alias="pct_usage_0")
    pct_usage_1: Optional[float] = Field(default=None, alias="pct_usage_1")
    pct_usage_2: Optional[float] = Field(default=None, alias="pct_usage_2")
    pct_usage_3: Optional[float] = Field(default=None, alias="pct_usage_3")
    pct_usage_4: Optional[float] = Field(default=None, alias="pct_usage_4")
    pct_usage_5: Optional[float] = Field(default=None, alias="pct_usage_5")
    pct_usage_6: Optional[float] = Field(default=None, alias="pct_usage_6")
    pct_usage_7: Optional[float] = Field(default=None, alias="pct_usage_7")
    pct_usage_8: Optional[float] = Field(default=None, alias="pct_usage_8")
    pct_usage_9: Optional[float] = Field(default=None, alias="pct_usage_9")
    pct_usage_10: Optional[float] = Field(default=None, alias="pct_usage_10")
    pct_usage_11: Optional[float] = Field(default=None, alias="pct_usage_11")
    pct_usage_12: Optional[float] = Field(default=None, alias="pct_usage_12")
    pct_usage_13: Optional[float] = Field(default=None, alias="pct_usage_13")
    pct_usage_14: Optional[float] = Field(default=None, alias="pct_usage_14")
    pct_usage_15: Optional[float] = Field(default=None, alias="pct_usage_15")
    pct_usage_16: Optional[float] = Field(default=None, alias="pct_usage_16")
    pct_usage_17: Optional[float] = Field(default=None, alias="pct_usage_17")
    pct_usage_18: Optional[float] = Field(default=None, alias="pct_usage_18")
    pct_usage_19: Optional[float] = Field(default=None, alias="pct_usage_19")
    pct_usage_20: Optional[float] = Field(default=None, alias="pct_usage_20")

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        # Construct the list of pct_usage values in order
        pct_usages = [
            str(model_data.get(f"pct_usage_{i}", "")) if model_data.get(f"pct_usage_{i}") is not None else ""
            for i in range(21) # 0 to 20
        ]
        
        return [
            "%R",
            str(model_data.get("curv_id", "")) if model_data.get("curv_id") is not None else "",
            model_data.get("curv_name", "") if model_data.get("curv_name") is not None else "",
            model_data.get("default_flag", "") if model_data.get("default_flag") is not None else "",
            *pct_usages, # Unpack the list of pct_usage strings
        ]

    def __repr__(self) -> str:
        name = self.curv_name if self.curv_name is not None else "Unknown ResourceCurve"
        return f"<{name} (ID: {self.curv_id if self.curv_id is not None else 'N/A'})>"

    class Config:
        # If locale.atof was essential and input values might not be standard floats,
        # custom validators might be needed. For now, assuming Pydantic's float coercion is sufficient.
        pass
