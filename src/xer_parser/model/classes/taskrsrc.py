from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class TaskRsrc(BaseModel):
    taskrsrc_id: Optional[int] = Field(default=None, alias="taskrsrc_id")
    task_id: Optional[int] = Field(default=None, alias="task_id")
    proj_id: Optional[int] = Field(default=None, alias="proj_id") # Assuming int ID
    cost_qty_link_flag: Optional[str] = Field(default=None, alias="cost_qty_link_flag") # Y/N
    role_id: Optional[int] = Field(default=None, alias="role_id") # Assuming int ID
    acct_id: Optional[int] = Field(default=None, alias="acct_id") # Assuming int ID
    rsrc_id: Optional[int] = Field(default=None, alias="rsrc_id")
    pobs_id: Optional[int] = Field(default=None, alias="pobs_id") # Assuming int ID
    skill_level: Optional[int] = Field(default=None, alias="skill_level") # Assuming int
    remain_qty: Optional[float] = Field(default=None, alias="remain_qty")
    target_qty: Optional[float] = Field(default=None, alias="target_qty")
    remain_qty_per_hr: Optional[float] = Field(default=None, alias="remain_qty_per_hr")
    target_lag_drtn_hr_cnt: Optional[float] = Field(default=None, alias="target_lag_drtn_hr_cnt")
    target_qty_per_hr: Optional[float] = Field(default=None, alias="target_qty_per_hr") # Was string, assuming float
    act_ot_qty: Optional[float] = Field(default=None, alias="act_ot_qty") # Was string, assuming float
    act_reg_qty: Optional[float] = Field(default=None, alias="act_reg_qty") # Was string, assuming float
    relag_drtn_hr_cnt: Optional[float] = Field(default=None, alias="relag_drtn_hr_cnt") # Was string, assuming float
    ot_factor: Optional[float] = Field(default=None, alias="ot_factor") # Was string, assuming float
    cost_per_qty: Optional[float] = Field(default=None, alias="cost_per_qty") # Was string, assuming float
    target_cost: Optional[float] = Field(default=None, alias="target_cost") # Was string, assuming float
    act_reg_cost: Optional[float] = Field(default=None, alias="act_reg_cost")
    act_ot_cost: Optional[float] = Field(default=None, alias="act_ot_cost") # Was string, assuming float
    remain_cost: Optional[float] = Field(default=None, alias="remain_cost") # Was string, assuming float
    act_start_date: Optional[datetime] = Field(default=None, alias="act_start_date")
    act_end_date: Optional[datetime] = Field(default=None, alias="act_end_date")
    restart_date: Optional[datetime] = Field(default=None, alias="restart_date")
    reend_date: Optional[datetime] = Field(default=None, alias="reend_date")
    target_start_date: Optional[datetime] = Field(default=None, alias="target_start_date")
    target_end_date: Optional[datetime] = Field(default=None, alias="target_end_date")
    rem_late_start_date: Optional[datetime] = Field(default=None, alias="rem_late_start_date")
    rem_late_end_date: Optional[datetime] = Field(default=None, alias="rem_late_end_date")
    rollup_dates_flag: Optional[str] = Field(default=None, alias="rollup_dates_flag") # Y/N
    target_crv: Optional[str] = Field(default=None, alias="target_crv") # Curve name or ID?
    remain_crv: Optional[str] = Field(default=None, alias="remain_crv") # Curve name or ID?
    actual_crv: Optional[str] = Field(default=None, alias="actual_crv") # Curve name or ID?
    ts_pend_act_end_flag: Optional[str] = Field(default=None, alias="ts_pend_act_end_flag") # Y/N
    guid: Optional[str] = Field(default=None, alias="guid")
    rate_type: Optional[int] = Field(default=None, alias="rate_type") # Assuming int, (e.g. 1 for Price / Unit, 2 for Price / Unit 2 etc)
    act_this_per_cost: Optional[float] = Field(default=None, alias="act_this_per_cost") # Was string, assuming float
    act_this_per_qty: Optional[float] = Field(default=None, alias="act_this_per_qty") # Corrected from act_this_per_cost
    curv_id: Optional[int] = Field(default=None, alias="curv_id") # Assuming int ID
    rsrc_type: Optional[str] = Field(default=None, alias="rsrc_type")
    cost_per_qty_source_type: Optional[str] = Field(default=None, alias="cost_per_qty_source_type")
    create_user: Optional[str] = Field(default=None, alias="create_user")
    create_date: Optional[datetime] = Field(default=None, alias="create_date")
    cbs_id: Optional[int] = Field(default=None, alias="cbs_id") # Assuming int ID
    has_rsrchours: Optional[str] = Field(default=None, alias="has_rsrchours") # Y/N
    taskrsrc_sum_id: Optional[int] = Field(default=None, alias="taskrsrc_sum_id") # Assuming int ID

    data: Any = Field(default=None, exclude=True)

    def _format_date_for_tsv(self, dt_val: Any) -> str:
        if dt_val is None: return ""
        if isinstance(dt_val, datetime): return dt_val.strftime("%Y-%m-%d %H:%M")
        return str(dt_val)

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        def s(value: Any) -> str:
            return "" if value is None else str(value)

        return [
            "%R",
            s(model_data.get("taskrsrc_id")), s(model_data.get("task_id")), s(model_data.get("proj_id")),
            s(model_data.get("cost_qty_link_flag")), s(model_data.get("role_id")), s(model_data.get("acct_id")),
            s(model_data.get("rsrc_id")), s(model_data.get("pobs_id")), s(model_data.get("skill_level")),
            s(model_data.get("remain_qty")), s(model_data.get("target_qty")), s(model_data.get("remain_qty_per_hr")),
            s(model_data.get("target_lag_drtn_hr_cnt")), s(model_data.get("target_qty_per_hr")),
            s(model_data.get("act_ot_qty")), s(model_data.get("act_reg_qty")), s(model_data.get("relag_drtn_hr_cnt")),
            s(model_data.get("ot_factor")), s(model_data.get("cost_per_qty")), s(model_data.get("target_cost")),
            s(model_data.get("act_reg_cost")), s(model_data.get("act_ot_cost")), s(model_data.get("remain_cost")),
            self._format_date_for_tsv(self.act_start_date), self._format_date_for_tsv(self.act_end_date),
            self._format_date_for_tsv(self.restart_date), self._format_date_for_tsv(self.reend_date),
            self._format_date_for_tsv(self.target_start_date), self._format_date_for_tsv(self.target_end_date),
            self._format_date_for_tsv(self.rem_late_start_date), self._format_date_for_tsv(self.rem_late_end_date),
            s(model_data.get("rollup_dates_flag")), s(model_data.get("target_crv")), s(model_data.get("remain_crv")),
            s(model_data.get("actual_crv")), s(model_data.get("ts_pend_act_end_flag")), s(model_data.get("guid")),
            s(model_data.get("rate_type")), s(model_data.get("act_this_per_cost")), s(model_data.get("act_this_per_qty")),
            s(model_data.get("curv_id")), s(model_data.get("rsrc_type")), s(model_data.get("cost_per_qty_source_type")),
            s(model_data.get("create_user")), self._format_date_for_tsv(self.create_date),
            s(model_data.get("cbs_id")), s(model_data.get("has_rsrchours")), s(model_data.get("taskrsrc_sum_id")),
        ]

    @property
    def resource(self) -> Any: # Should be Optional["Resource"] once Resource is Pydantic
        if self.data and hasattr(self.data, 'resources') and self.data.resources is not None and self.rsrc_id is not None:
            # Assuming self.data.resources is a list of Pydantic Resource models
            for res in self.data.resources:
                if hasattr(res, 'rsrc_id') and res.rsrc_id == self.rsrc_id:
                    return res
        return None

    def __repr__(self) -> str:
        task_id_str = str(self.task_id) if self.task_id is not None else "N/A"
        rsrc_id_str = str(self.rsrc_id) if self.rsrc_id is not None else "N/A"
        target_qty_str = str(self.target_qty) if self.target_qty is not None else "N/A"
        return f"<TaskRsrc task_id={task_id_str} -> rsrc_id={rsrc_id_str} (Target Qty: {target_qty_str})>"
