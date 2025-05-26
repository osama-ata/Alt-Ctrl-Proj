from typing import Optional, Any
from pydantic import BaseModel, Field


class ResourceCat(BaseModel):
    rsrc_id: Optional[int] = Field(default=None, alias="rsrc_id")
    rsrc_catg_type_id: Optional[int] = Field(default=None, alias="rsrc_catg_type_id")
    rsrc_catg_id: Optional[int] = Field(default=None, alias="rsrc_catg_id") # Assuming param key is "rsrc_catg_id"

    data: Any = Field(default=None, exclude=True)

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("rsrc_id", "")) if model_data.get("rsrc_id") is not None else "",
            str(model_data.get("rsrc_catg_type_id", "")) if model_data.get("rsrc_catg_type_id") is not None else "",
            str(model_data.get("rsrc_catg_id", "")) if model_data.get("rsrc_catg_id") is not None else "",
        ]

    def __repr__(self) -> str:
        r_id = str(self.rsrc_id) if self.rsrc_id is not None else "N/A"
        rc_id = str(self.rsrc_catg_id) if self.rsrc_catg_id is not None else "N/A"
        return f"<ResourceCat rsrc_id={r_id} rsrc_catg_id={rc_id}>"
