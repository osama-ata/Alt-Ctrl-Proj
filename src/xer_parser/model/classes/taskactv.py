from typing import Optional, Any
from pydantic import BaseModel, Field


class TaskActv(BaseModel):
    task_id: Optional[int] = Field(default=None, alias="task_id")
    actv_code_type_id: Optional[int] = Field(default=None, alias="actv_code_type_id") # Assuming this is an int ID
    actv_code_id: Optional[int] = Field(default=None, alias="actv_code_id")
    proj_id: Optional[int] = Field(default=None, alias="proj_id")

    data: Any = Field(default=None, exclude=True) # To store a reference to the main Data object if needed later

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("task_id", "")) if model_data.get("task_id") is not None else "",
            str(model_data.get("actv_code_type_id", "")) if model_data.get("actv_code_type_id") is not None else "",
            str(model_data.get("actv_code_id", "")) if model_data.get("actv_code_id") is not None else "",
            str(model_data.get("proj_id", "")) if model_data.get("proj_id") is not None else "",
        ]

    def __repr__(self) -> str:
        task_id_str = str(self.task_id) if self.task_id is not None else "N/A"
        actv_code_id_str = str(self.actv_code_id) if self.actv_code_id is not None else "N/A"
        return f"<TaskActv task_id={task_id_str} -> actv_code_id={actv_code_id_str}>"
