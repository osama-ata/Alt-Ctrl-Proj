from typing import Optional, Any
from pydantic import BaseModel, Field


class ProjCat(BaseModel):
    # %F	proj_id	proj_catg_type_id	proj_catg_id
    proj_id: Optional[int] = Field(default=None, alias="proj_id") # Assuming int
    proj_catg_type_id: Optional[int] = Field(default=None, alias="proj_catg_type_id") # Assuming int
    proj_catg_id: Optional[int] = Field(default=None, alias="proj_catg_id") # Assuming int

    data: Any = Field(default=None, exclude=True) # Standard data field

    def get_id(self) -> Optional[int]: # Kept for now
        return self.proj_id

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("proj_id", "")) if model_data.get("proj_id") is not None else "",
            str(model_data.get("proj_catg_type_id", "")) if model_data.get("proj_catg_type_id") is not None else "",
            str(model_data.get("proj_catg_id", "")) if model_data.get("proj_catg_id") is not None else "",
        ]

    def __repr__(self) -> str:
        p_id = str(self.proj_id) if self.proj_id is not None else "N/A"
        pc_id = str(self.proj_catg_id) if self.proj_catg_id is not None else "N/A"
        return f"<ProjCat project_id={p_id} category_id={pc_id}>"
