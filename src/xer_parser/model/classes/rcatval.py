from typing import Optional, Any
from pydantic import BaseModel, Field


class RCatVal(BaseModel):
    rsrc_catg_id: Optional[int] = Field(default=None, alias="rsrc_catg_id")
    rsrc_catg_type_id: Optional[int] = Field(default=None, alias="rsrc_catg_type_id")
    rsrc_catg_short_name: Optional[str] = Field(default=None, alias="rsrc_catg_short_name")
    rsrc_catg_name: Optional[str] = Field(default=None, alias="rsrc_catg_name")
    parent_rsrc_catg_id: Optional[int] = Field(default=None, alias="parent_rsrc_catg_id")
    # seq_num is often present in such tables, but not in original __init__. Added based on common pattern.
    # If not in XER, it can be removed. For now, assuming it might be relevant.
    seq_num: Optional[int] = Field(default=None, alias="seq_num") 

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_id(self) -> Optional[int]: # Kept for now
        return self.rsrc_catg_id

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        # Original get_tsv order: rsrc_catg_id, rsrc_catg_type_id, rsrc_catg_short_name, rsrc_catg_name, parent_rsrc_catg_id
        # Adding seq_num at a logical place if it were present, e.g., after type_id or at end.
        # For now, keeping original fields and order from file. If seq_num is confirmed, order needs adjustment.
        # The provided file did not have seq_num in its __init__ or get_tsv.
        return [
            "%R",
            str(model_data.get("rsrc_catg_id", "")) if model_data.get("rsrc_catg_id") is not None else "",
            str(model_data.get("rsrc_catg_type_id", "")) if model_data.get("rsrc_catg_type_id") is not None else "",
            model_data.get("rsrc_catg_short_name", "") if model_data.get("rsrc_catg_short_name") is not None else "",
            model_data.get("rsrc_catg_name", "") if model_data.get("rsrc_catg_name") is not None else "",
            str(model_data.get("parent_rsrc_catg_id", "")) if model_data.get("parent_rsrc_catg_id") is not None else "",
            # str(model_data.get("seq_num", "")) if model_data.get("seq_num") is not None else "", # If seq_num is added
        ]

    def __repr__(self) -> str:
        name = self.rsrc_catg_name if self.rsrc_catg_name is not None else "Unknown RCatVal"
        return f"<{name} (ID: {self.rsrc_catg_id if self.rsrc_catg_id is not None else 'N/A'})>"
