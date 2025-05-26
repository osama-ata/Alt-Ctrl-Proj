import locale
from datetime import datetime
from typing import Optional, Any, List, TYPE_CHECKING
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .calendar import Calendar # Assuming Calendar is already/will be a Pydantic model
    # from .wbs import WBS # Assuming WBS is already/will be a Pydantic model
    # from .taskproc import TaskProc # Assuming TaskProc is already/will be a Pydantic model
    # from .taskpred import TaskPred # For successors/predecessors if they return Task objects
    # from .taskrsrc import TaskRsrc
    # from .taskactv import TaskActv # For activitycodes
    # from .data import Data # For self.data access


class Task(BaseModel):
    task_id: Optional[int] = Field(default=None, alias="task_id")
    proj_id: Optional[int] = Field(default=None, alias="proj_id")
    wbs_id: Optional[int] = Field(default=None, alias="wbs_id")
    clndr_id: Optional[int] = Field(default=None, alias="clndr_id")
    phys_complete_pct: Optional[float] = Field(default=None, alias="phys_complete_pct")
    rev_fdbk_flag: Optional[str] = Field(default=None, alias="rev_fdbk_flag")
    est_wt: Optional[float] = Field(default=None, alias="est_wt")
    lock_plan_flag: Optional[str] = Field(default=None, alias="lock_plan_flag")
    auto_compute_act_flag: Optional[str] = Field(default=None, alias="auto_compute_act_flag")
    complete_pct_type: Optional[str] = Field(default=None, alias="complete_pct_type")
    task_type: Optional[str] = Field(default=None, alias="task_type")
    duration_type: Optional[str] = Field(default=None, alias="duration_type")
    status_code: Optional[str] = Field(default=None, alias="status_code")
    task_code: Optional[str] = Field(default=None, alias="task_code")
    task_name: Optional[str] = Field(default=None, alias="task_name")
    rsrc_id: Optional[int] = Field(default=None, alias="rsrc_id") # This might be a primary resource, not a list
    total_float_hr_cnt: Optional[float] = Field(default=None, alias="total_float_hr_cnt")
    free_float_hr_cnt: Optional[float] = Field(default=None, alias="free_float_hr_cnt")
    remain_drtn_hr_cnt: Optional[float] = Field(default=0.0, alias="remain_drtn_hr_cnt") # Original defaulted to 0
    act_work_qty: Optional[float] = Field(default=None, alias="act_work_qty")
    remain_work_qty: Optional[float] = Field(default=None, alias="remain_work_qty")
    target_work_qty: Optional[float] = Field(default=None, alias="target_work_qty")
    target_drtn_hr_cnt: Optional[float] = Field(default=None, alias="target_drtn_hr_cnt")
    target_equip_qty: Optional[float] = Field(default=None, alias="target_equip_qty")
    act_equip_qty: Optional[float] = Field(default=None, alias="act_equip_qty")
    remain_equip_qty: Optional[float] = Field(default=None, alias="remain_equip_qty")
    cstr_date: Optional[datetime] = Field(default=None, alias="cstr_date")
    act_start_date: Optional[datetime] = Field(default=None, alias="act_start_date")
    act_end_date: Optional[datetime] = Field(default=None, alias="act_end_date")
    late_start_date: Optional[datetime] = Field(default=None, alias="late_start_date")
    late_end_date: Optional[datetime] = Field(default=None, alias="late_end_date")
    expect_end_date: Optional[datetime] = Field(default=None, alias="expect_end_date")
    early_start_date: Optional[datetime] = Field(default=None, alias="early_start_date")
    early_end_date: Optional[datetime] = Field(default=None, alias="early_end_date")
    restart_date: Optional[datetime] = Field(default=None, alias="restart_date")
    reend_date: Optional[datetime] = Field(default=None, alias="reend_date")
    target_start_date: Optional[datetime] = Field(default=None, alias="target_start_date")
    target_end_date: Optional[datetime] = Field(default=None, alias="target_end_date")
    rem_late_start_date: Optional[datetime] = Field(default=None, alias="rem_late_start_date")
    rem_late_end_date: Optional[datetime] = Field(default=None, alias="rem_late_end_date")
    cstr_type: Optional[str] = Field(default=None, alias="cstr_type")
    priority_type: Optional[str] = Field(default=None, alias="priority_type")
    suspend_date: Optional[datetime] = Field(default=None, alias="suspend_date")
    resume_date: Optional[datetime] = Field(default=None, alias="resume_date")
    int_path: Optional[str] = Field(default=None, alias="int_path") # Keep as str, could be int if it's numeric
    int_path_order: Optional[int] = Field(default=None, alias="int_path_order") # Assuming int
    guid: Optional[str] = Field(default=None, alias="guid")
    tmpl_guid: Optional[str] = Field(default=None, alias="tmpl_guid")
    cstr_date2: Optional[datetime] = Field(default=None, alias="cstr_date2")
    cstr_type2: Optional[str] = Field(default=None, alias="cstr_type2")
    driving_path_flag: Optional[str] = Field(default=None, alias="driving_path_flag")
    act_this_per_work_qty: Optional[float] = Field(default=None, alias="act_this_per_work_qty")
    act_this_per_equip_qty: Optional[float] = Field(default=None, alias="act_this_per_equip_qty")
    external_early_start_date: Optional[datetime] = Field(default=None, alias="external_early_start_date")
    external_late_end_date: Optional[datetime] = Field(default=None, alias="external_late_end_date")
    create_date: Optional[datetime] = Field(default=None, alias="create_date")
    update_date: Optional[datetime] = Field(default=None, alias="update_date")
    create_user: Optional[str] = Field(default=None, alias="create_user")
    update_user: Optional[str] = Field(default=None, alias="update_user")
    location_id: Optional[int] = Field(default=None, alias="location_id") # Assuming int

    data: Any = Field(default=None, exclude=True)
    logic_missing: bool = Field(default=False, exclude=True) # From original __init__

    # calendar: Optional["Calendar"] = None # This would be populated post-init

    def _format_date_for_tsv(self, dt_val: Optional[datetime]) -> str:
        if dt_val is None:
            return ""
        # Pydantic v2 might pass datetime objects directly if not stringified by model_dump
        if isinstance(dt_val, datetime):
            return dt_val.strftime("%Y-%m-%d %H:%M")
        elif isinstance(dt_val, str): # If already string from model_dump
            return dt_val 
        return ""


    def get_tsv(self) -> list[Any]:
        model_data = self.model_dump(by_alias=True, exclude_none=False) # exclude_none=False might not be needed if we handle each field
        
        # Helper to get value as string or "" if None/missing
        def s(key: str) -> str:
            val = model_data.get(key)
            if val is None: return ""
            if isinstance(val, (int, float)): return str(val)
            return str(val) # Should already be string for str fields

        return [
            "%R",
            s("task_id"), s("proj_id"), s("wbs_id"), s("clndr_id"),
            s("phys_complete_pct"), s("rev_fdbk_flag"), s("est_wt"), s("lock_plan_flag"),
            s("auto_compute_act_flag"), s("complete_pct_type"), s("task_type"), s("duration_type"),
            s("status_code"), s("task_code"), s("task_name"), s("rsrc_id"),
            s("total_float_hr_cnt"), s("free_float_hr_cnt"), s("remain_drtn_hr_cnt"),
            s("act_work_qty"), s("remain_work_qty"), s("target_work_qty"),
            s("target_drtn_hr_cnt"), s("target_equip_qty"), s("act_equip_qty"), s("remain_equip_qty"),
            self._format_date_for_tsv(self.cstr_date),
            self._format_date_for_tsv(self.act_start_date),
            self._format_date_for_tsv(self.act_end_date),
            self._format_date_for_tsv(self.late_start_date),
            self._format_date_for_tsv(self.late_end_date),
            self._format_date_for_tsv(self.expect_end_date),
            self._format_date_for_tsv(self.early_start_date),
            self._format_date_for_tsv(self.early_end_date),
            self._format_date_for_tsv(self.restart_date),
            self._format_date_for_tsv(self.reend_date),
            self._format_date_for_tsv(self.target_start_date),
            self._format_date_for_tsv(self.target_end_date),
            self._format_date_for_tsv(self.rem_late_start_date),
            self._format_date_for_tsv(self.rem_late_end_date),
            s("cstr_type"), s("priority_type"),
            self._format_date_for_tsv(self.suspend_date),
            self._format_date_for_tsv(self.resume_date),
            s("int_path"), s("int_path_order"), s("guid"), s("tmpl_guid"),
            self._format_date_for_tsv(self.cstr_date2),
            s("cstr_type2"), s("driving_path_flag"),
            s("act_this_per_work_qty"), s("act_this_per_equip_qty"),
            self._format_date_for_tsv(self.external_early_start_date),
            self._format_date_for_tsv(self.external_late_end_date),
            self._format_date_for_tsv(self.create_date),
            self._format_date_for_tsv(self.update_date),
            s("create_user"), s("update_user"), s("location_id"),
        ]

    @property
    def id(self) -> Optional[int]:
        return self.task_id

    @property
    def totalint(self) -> Optional[float]: # Original name was total_int_hr_cnt, but XER field is total_float_hr_cnt
        if self.total_float_hr_cnt is not None: # Use the actual Pydantic field name
            # Assuming 8 hours per day, adjust if needed
            return float(self.total_float_hr_cnt) / 8.0 
        return None

    @property
    def resources(self) -> List["TaskRsrc"]:
        if self.data and hasattr(self.data, 'taskrsrcs') and self.data.taskrsrcs is not None:
            return [r for r in self.data.taskrsrcs if r.task_id == self.task_id]
        return []

    @property
    def steps(self) -> List["TaskProc"]:
        if self.data and hasattr(self.data, 'taskprocs') and self.data.taskprocs is not None:
             return [s for s in self.data.taskprocs if s.task_id == self.task_id]
        return []
    
    @property
    def activitycodes(self) -> List["TaskActv"]:
        if self.data and hasattr(self.data, 'taskactvs') and self.data.taskactvs is not None:
            return [ac for ac in self.data.taskactvs if ac.task_id == self.task_id]
        return []

    @property
    def calendar(self) -> Optional["Calendar"]:
        if self.data and hasattr(self.data, 'calendars') and self.data.calendars is not None and self.clndr_id is not None:
            for cal in self.data.calendars:
                if cal.clndr_id == self.clndr_id:
                    return cal
        return None

    @property
    def duration(self) -> float:
        dur = 0.0
        if self.target_drtn_hr_cnt is not None:
            current_calendar = self.calendar
            if current_calendar and current_calendar.day_hr_cnt and current_calendar.day_hr_cnt > 0:
                dur = self.target_drtn_hr_cnt / current_calendar.day_hr_cnt
            else: # Default to 8 hours if calendar or day_hr_cnt is not available/valid
                dur = self.target_drtn_hr_cnt / 8.0
        return dur

    @property
    def constraints(self) -> Optional[dict[str, Any]]:
        if self.cstr_type is None or self.cstr_date is None:
            return None
        # Corrected key name from "ConstrintDate" to "ConstraintDate"
        return {"ConstraintType": self.cstr_type, "ConstraintDate": self.cstr_date}


    @property
    def start_date(self) -> Optional[datetime]:
        if self.act_start_date:
            return self.act_start_date
        return self.target_start_date

    @property
    def end_date(self) -> Optional[datetime]:
        if self.act_end_date:
            return self.act_end_date
        return self.target_end_date

    @property
    def successors(self) -> List["TaskPred"]:
        if self.data and hasattr(self.data, 'taskpreds') and self.data.taskpreds is not None:
            return [p for p in self.data.taskpreds if p.pred_task_id == self.task_id]
        return []

    @property
    def predecessors(self) -> List["TaskPred"]:
        if self.data and hasattr(self.data, 'taskpreds') and self.data.taskpreds is not None:
            return [p for p in self.data.taskpreds if p.task_id == self.task_id]
        return []
        
    def __repr__(self) -> str:
        return self.task_name if self.task_name is not None else super().__repr__()

    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (ClassVar,) # To handle ClassVar if any were left (obj_list is removed)
