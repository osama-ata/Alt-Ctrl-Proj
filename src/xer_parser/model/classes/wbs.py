import logging
from typing import Optional, Any, List, TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .task import Task # Assuming Task is already/will be a Pydantic model
    # from .data import Data # For self.data type hint if available

# Initialize logger
logger = logging.getLogger(__name__)


class WBS(BaseModel):
    wbs_id: Optional[int] = Field(default=None, alias="wbs_id")
    proj_id: Optional[int] = Field(default=None, alias="proj_id")
    obs_id: Optional[int] = Field(default=None, alias="obs_id") # Assuming int ID
    seq_num: Optional[int] = Field(default=None, alias="seq_num") # Assuming int
    est_wt: Optional[float] = Field(default=None, alias="est_wt") # Assuming float
    proj_node_flag: Optional[str] = Field(default=None, alias="proj_node_flag") # Y/N
    sum_data_flag: Optional[str] = Field(default=None, alias="sum_data_flag") # Y/N
    status_code: Optional[str] = Field(default=None, alias="status_code")
    wbs_short_name: Optional[str] = Field(default=None, alias="wbs_short_name")
    wbs_name: Optional[str] = Field(default=None, alias="wbs_name")
    phase_id: Optional[int] = Field(default=None, alias="phase_id") # Assuming int ID
    parent_wbs_id: Optional[int] = Field(default=None, alias="parent_wbs_id")
    ev_user_pct: Optional[float] = Field(default=None, alias="ev_user_pct") # Assuming float
    ev_etc_user_value: Optional[float] = Field(default=None, alias="ev_etc_user_value") # Assuming float
    orig_cost: Optional[float] = Field(default=None, alias="orig_cost") # Assuming float
    indep_remain_total_cost: Optional[float] = Field(default=None, alias="indep_remain_total_cost") # Assuming float
    ann_dscnt_rate_pct: Optional[float] = Field(default=None, alias="ann_dscnt_rate_pct") # Assuming float
    dscnt_period_type: Optional[str] = Field(default=None, alias="dscnt_period_type")
    indep_remain_work_qty: Optional[float] = Field(default=None, alias="indep_remain_work_qty") # Assuming float
    anticip_start_date: Optional[datetime] = Field(default=None, alias="anticip_start_date")
    anticip_end_date: Optional[datetime] = Field(default=None, alias="anticip_end_date")
    ev_compute_type: Optional[str] = Field(default=None, alias="ev_compute_type")
    ev_etc_compute_type: Optional[str] = Field(default=None, alias="ev_etc_compute_type")
    guid: Optional[str] = Field(default=None, alias="guid")
    tmpl_guid: Optional[str] = Field(default=None, alias="tmpl_guid")
    plan_open_state: Optional[str] = Field(default=None, alias="plan_open_state")

    data: Any = Field(default=None, exclude=True)

    def _format_date_for_tsv(self, dt_val: Any) -> str:
        if dt_val is None: return ""
        if isinstance(dt_val, datetime): return dt_val.strftime("%Y-%m-%d %H:%M")
        return str(dt_val)

    def get_tsv(self) -> list[Any]:
        model_data = self.model_dump(by_alias=True)
        def s(value: Any) -> str:
            return "" if value is None else str(value)

        return [
            "%R",
            s(model_data.get("wbs_id")),
            s(model_data.get("proj_id")),
            s(model_data.get("obs_id")),
            s(model_data.get("seq_num")),
            s(model_data.get("est_wt")),
            s(model_data.get("proj_node_flag")),
            s(model_data.get("sum_data_flag")),
            s(model_data.get("status_code")),
            s(model_data.get("wbs_short_name")),
            s(model_data.get("wbs_name")),
            s(model_data.get("phase_id")),
            s(model_data.get("parent_wbs_id")),
            s(model_data.get("ev_user_pct")),
            s(model_data.get("ev_etc_user_value")),
            s(model_data.get("orig_cost")),
            s(model_data.get("indep_remain_total_cost")),
            s(model_data.get("ann_dscnt_rate_pct")),
            s(model_data.get("dscnt_period_type")),
            s(model_data.get("indep_remain_work_qty")),
            self._format_date_for_tsv(self.anticip_start_date),
            self._format_date_for_tsv(self.anticip_end_date),
            s(model_data.get("ev_compute_type")),
            s(model_data.get("ev_etc_compute_type")),
            s(model_data.get("guid")),
            s(model_data.get("tmpl_guid")),
            s(model_data.get("plan_open_state")),
        ]

    @property
    def activities(self) -> List["Task"]: # Type hint to List["Task"]
        if self.data and hasattr(self.data, 'tasks') and self.data.tasks is not None and self.wbs_id is not None:
            # Assuming self.data.tasks is a list of Pydantic Task models
            return [task for task in self.data.tasks if hasattr(task, 'wbs_id') and task.wbs_id == self.wbs_id]
        return []

    def __repr__(self) -> str:
        return self.wbs_name if self.wbs_name is not None else "WBS Element"

    class Config:
        arbitrary_types_allowed = True
