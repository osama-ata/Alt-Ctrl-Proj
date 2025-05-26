from typing import Optional, Any
from pydantic import BaseModel, Field


class TaskProc(BaseModel):
    proc_id: Optional[int] = Field(default=None, alias="proc_id")
    task_id: Optional[int] = Field(default=None, alias="task_id")
    proj_id: Optional[int] = Field(default=None, alias="proj_id")
    seq_num: Optional[int] = Field(default=None, alias="seq_num")
    proc_name: Optional[str] = Field(default=None, alias="proc_name")
    complete_flag: Optional[str] = Field(default=None, alias="complete_flag") # Y/N
    proc_wt: Optional[float] = Field(default=None, alias="proc_wt")
    complete_pct: Optional[float] = Field(default=None, alias="complete_pct")
    proc_descr: Optional[str] = Field(default=None, alias="proc_descr")

    data: Any = Field(default=None, exclude=True)

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        
        # Helper to convert None to empty string and other types to string
        def s(value: Any) -> str:
            return "" if value is None else str(value)

        return [
            "%R",
            s(model_data.get("proc_id")),
            s(model_data.get("task_id")),
            s(model_data.get("proj_id")),
            s(model_data.get("seq_num")),
            s(model_data.get("proc_name")),
            s(model_data.get("complete_flag")),
            s(model_data.get("proc_wt")),
            s(model_data.get("complete_pct")),
            s(model_data.get("proc_descr")),
        ]

    def __repr__(self) -> str:
        proc_id_str = str(self.proc_id) if self.proc_id is not None else "N/A"
        task_id_str = str(self.task_id) if self.task_id is not None else "N/A"
        return f"<TaskProc proc_id={proc_id_str} -> task_id={task_id_str}>"
