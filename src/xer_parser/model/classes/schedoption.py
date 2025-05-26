from typing import Optional, Any
from pydantic import BaseModel, Field


class SchedOption(BaseModel):
    schedoptions_id: Optional[int] = Field(default=None, alias="schedoptions_id") # Assuming int
    proj_id: Optional[int] = Field(default=None, alias="proj_id") # Assuming int

    sched_outer_depend_type: Optional[str] = Field(default=None, alias="sched_outer_depend_type")
    sched_open_critical_flag: Optional[str] = Field(default=None, alias="sched_open_critical_flag") # Y/N
    sched_lag_early_start_flag: Optional[str] = Field(default=None, alias="sched_lag_early_start_flag") # Y/N
    sched_retained_logic: Optional[str] = Field(default=None, alias="sched_retained_logic") # Y/N
    sched_setplantoforecast: Optional[str] = Field(default=None, alias="sched_setplantoforecast") # Y/N
    sched_float_type: Optional[str] = Field(default=None, alias="sched_float_type")
    sched_calendar_on_relationship_lag: Optional[str] = Field(default=None, alias="sched_calendar_on_relationship_lag") # Y/N
    sched_use_expect_end_flag: Optional[str] = Field(default=None, alias="sched_use_expect_end_flag") # Y/N
    sched_progress_override: Optional[str] = Field(default=None, alias="sched_progress_override") # Y/N
    
    level_float_thrs_cnt: Optional[int] = Field(default=None, alias="level_float_thrs_cnt") # Assuming int
    level_outer_assign_flag: Optional[str] = Field(default=None, alias="level_outer_assign_flag") # Y/N
    level_outer_assign_priority: Optional[str] = Field(default=None, alias="level_outer_assign_priority") # Assuming string, could be int if it's a numeric priority
    level_over_alloc_pct: Optional[float] = Field(default=None, alias="level_over_alloc_pct") # Assuming float for percentage
    level_within_float_flag: Optional[str] = Field(default=None, alias="level_within_float_flag") # Y/N
    level_keep_sched_date_flag: Optional[str] = Field(default=None, alias="level_keep_sched_date_flag") # Y/N
    level_all_rsrc_flag: Optional[str] = Field(default=None, alias="level_all_rsrc_flag") # Y/N
    
    sched_use_project_end_date_for_float: Optional[str] = Field(default=None, alias="sched_use_project_end_date_for_float") # Y/N
    enable_multiple_longest_path_calc: Optional[str] = Field(default=None, alias="enable_multiple_longest_path_calc") # Y/N
    limit_multiple_longest_path_calc: Optional[str] = Field(default=None, alias="limit_multiple_longest_path_calc") # Y/N
    max_multiple_longest_path: Optional[int] = Field(default=None, alias="max_multiple_longest_path") # Assuming int
    use_total_float_multiple_longest_paths: Optional[str] = Field(default=None, alias="use_total_float_multiple_longest_paths") # Y/N
    key_activity_for_multiple_longest_paths: Optional[int] = Field(default=None, alias="key_activity_for_multiple_longest_paths") # Assuming int (activity ID)
    
    LevelPriorityList: Optional[str] = Field(default=None, alias="LevelPriorityList") # Often a comma-separated string

    data: Any = Field(default=None, exclude=True)

    def get_tsv(self) -> list:
        model_data = self.model_dump(by_alias=True)
        return [
            "%R",
            str(model_data.get("schedoptions_id", "")) if model_data.get("schedoptions_id") is not None else "",
            str(model_data.get("proj_id", "")) if model_data.get("proj_id") is not None else "",
            model_data.get("sched_outer_depend_type", "") if model_data.get("sched_outer_depend_type") is not None else "",
            model_data.get("sched_open_critical_flag", "") if model_data.get("sched_open_critical_flag") is not None else "",
            model_data.get("sched_lag_early_start_flag", "") if model_data.get("sched_lag_early_start_flag") is not None else "",
            model_data.get("sched_retained_logic", "") if model_data.get("sched_retained_logic") is not None else "",
            model_data.get("sched_setplantoforecast", "") if model_data.get("sched_setplantoforecast") is not None else "",
            model_data.get("sched_float_type", "") if model_data.get("sched_float_type") is not None else "",
            model_data.get("sched_calendar_on_relationship_lag", "") if model_data.get("sched_calendar_on_relationship_lag") is not None else "",
            model_data.get("sched_use_expect_end_flag", "") if model_data.get("sched_use_expect_end_flag") is not None else "",
            model_data.get("sched_progress_override", "") if model_data.get("sched_progress_override") is not None else "",
            str(model_data.get("level_float_thrs_cnt", "")) if model_data.get("level_float_thrs_cnt") is not None else "",
            model_data.get("level_outer_assign_flag", "") if model_data.get("level_outer_assign_flag") is not None else "",
            model_data.get("level_outer_assign_priority", "") if model_data.get("level_outer_assign_priority") is not None else "",
            str(model_data.get("level_over_alloc_pct", "")) if model_data.get("level_over_alloc_pct") is not None else "",
            model_data.get("level_within_float_flag", "") if model_data.get("level_within_float_flag") is not None else "",
            model_data.get("level_keep_sched_date_flag", "") if model_data.get("level_keep_sched_date_flag") is not None else "",
            model_data.get("level_all_rsrc_flag", "") if model_data.get("level_all_rsrc_flag") is not None else "",
            model_data.get("sched_use_project_end_date_for_float", "") if model_data.get("sched_use_project_end_date_for_float") is not None else "",
            model_data.get("enable_multiple_longest_path_calc", "") if model_data.get("enable_multiple_longest_path_calc") is not None else "",
            model_data.get("limit_multiple_longest_path_calc", "") if model_data.get("limit_multiple_longest_path_calc") is not None else "",
            str(model_data.get("max_multiple_longest_path", "")) if model_data.get("max_multiple_longest_path") is not None else "",
            model_data.get("use_total_float_multiple_longest_paths", "") if model_data.get("use_total_float_multiple_longest_paths") is not None else "",
            str(model_data.get("key_activity_for_multiple_longest_paths", "")) if model_data.get("key_activity_for_multiple_longest_paths") is not None else "",
            model_data.get("LevelPriorityList", "") if model_data.get("LevelPriorityList") is not None else "",
        ]

    def __repr__(self) -> str:
        opt_id = str(self.schedoptions_id) if self.schedoptions_id is not None else "N/A"
        p_id = str(self.proj_id) if self.proj_id is not None else "N/A"
        return f"<SchedOption ID: {opt_id} (Project ID: {p_id})>"
