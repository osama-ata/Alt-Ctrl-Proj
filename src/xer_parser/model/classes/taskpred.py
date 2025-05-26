from typing import Optional, Any
from pydantic import BaseModel, Field


class TaskPred(BaseModel):
    task_pred_id: Optional[int] = Field(default=None, alias="task_pred_id") # Assuming int ID
    task_id: Optional[int] = Field(default=None, alias="task_id")
    pred_task_id: Optional[int] = Field(default=None, alias="pred_task_id")
    proj_id: Optional[int] = Field(default=None, alias="proj_id")
    pred_proj_id: Optional[int] = Field(default=None, alias="pred_proj_id") # Original used params.get("proj_id")
    pred_type: Optional[str] = Field(default=None, alias="pred_type")
    lag_hr_cnt: Optional[float] = Field(default=None, alias="lag_hr_cnt")
    float_path: Optional[str] = Field(default=None, alias="float_path") # Assuming string, could be int/bool if specific values
    aref: Optional[str] = Field(default=None, alias="aref")
    arls: Optional[str] = Field(default=None, alias="arls")
    comments: Optional[str] = Field(default=None, alias="comments")

    data: Any = Field(default=None, exclude=True)

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        
        # Helper to convert None to empty string and other types to string
        def s(value: Any) -> str:
            return "" if value is None else str(value)

        return [
            "%R",
            s(model_data.get("task_pred_id")),
            s(model_data.get("task_id")),
            s(model_data.get("pred_task_id")),
            s(model_data.get("proj_id")),
            s(model_data.get("pred_proj_id")),
            s(model_data.get("pred_type")),
            s(model_data.get("lag_hr_cnt")),
            s(model_data.get("comments")),
            s(model_data.get("float_path")),
            s(model_data.get("aref")),
            s(model_data.get("arls")),
        ]

    def __repr__(self) -> str:
        pred_id_str = str(self.pred_task_id) if self.pred_task_id is not None else "N/A"
        succ_id_str = str(self.task_id) if self.task_id is not None else "N/A"
        pred_type_str = self.pred_type if self.pred_type is not None else "N/A"
        lag_str = str(self.lag_hr_cnt) if self.lag_hr_cnt is not None else "N/A"
        
        return f"<TaskPred: {pred_id_str} -{pred_type_str}-> {succ_id_str} (Lag: {lag_str}h)>"
