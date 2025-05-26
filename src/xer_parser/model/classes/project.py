from typing import Optional, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

# Forward reference for WBS, assuming it will be a Pydantic model
# from xer_parser.model.classes.wbs import WBS # Not strictly needed for field defs if using string literal "WBS"


class Project(BaseModel):
    proj_id: Optional[int] = Field(default=None, alias="proj_id")
    fy_start_month_num: Optional[int] = Field(default=None, alias="fy_start_month_num") # Assuming int
    rsrc_self_add_flag: Optional[str] = Field(default=None, alias="rsrc_self_add_flag") # Y/N flag
    allow_complete_flag: Optional[str] = Field(default=None, alias="allow_complete_flag") # Y/N flag
    rsrc_multi_assign_flag: Optional[str] = Field(default=None, alias="rsrc_multi_assign_flag") # Y/N flag
    checkout_flag: Optional[str] = Field(default=None, alias="checkout_flag") # Y/N flag
    project_flag: Optional[str] = Field(default=None, alias="project_flag") # Y/N flag
    step_complete_flag: Optional[str] = Field(default=None, alias="step_complete_flag") # Y/N flag
    cost_qty_recalc_flag: Optional[str] = Field(default=None, alias="cost_qty_recalc_flag") # Y/N flag
    batch_sum_flag: Optional[str] = Field(default=None, alias="batch_sum_flag") # Y/N flag
    name_sep_char: Optional[str] = Field(default=None, alias="name_sep_char")
    def_complete_pct_type: Optional[str] = Field(default=None, alias="def_complete_pct_type")
    proj_short_name: Optional[str] = Field(default=None, alias="proj_short_name")
    acct_id: Optional[int] = Field(default=None, alias="acct_id") # Assuming int
    orig_proj_id: Optional[int] = Field(default=None, alias="orig_proj_id") # Assuming int, though XER might use string for external refs
    source_proj_id: Optional[int] = Field(default=None, alias="source_proj_id") # Assuming int
    base_type_id: Optional[int] = Field(default=None, alias="base_type_id") # Assuming int
    clndr_id: Optional[int] = Field(default=None, alias="clndr_id") # Assuming int
    sum_base_proj_id: Optional[int] = Field(default=None, alias="sum_base_proj_id") # Assuming int
    task_code_base: Optional[int] = Field(default=None, alias="task_code_base") # Assuming int
    task_code_step: Optional[int] = Field(default=None, alias="task_code_step") # Assuming int
    priority_num: Optional[int] = Field(default=None, alias="priority_num") # Assuming int
    wbs_max_sum_level: Optional[int] = Field(default=None, alias="wbs_max_sum_level") # Assuming int
    strgy_priority_num: Optional[int] = Field(default=None, alias="strgy_priority_num") # Assuming int
    last_checksum: Optional[str] = Field(default=None, alias="last_checksum") # Typically a string/hex
    critical_drtn_hr_cnt: Optional[float] = Field(default=None, alias="critical_drtn_hr_cnt") # Assuming float
    def_cost_per_qty: Optional[float] = Field(default=None, alias="def_cost_per_qty") # Assuming float
    last_recalc_date: Optional[datetime] = Field(default=None, alias="last_recalc_date")
    plan_start_date: Optional[datetime] = Field(default=None, alias="plan_start_date")
    plan_end_date: Optional[datetime] = Field(default=None, alias="plan_end_date")
    scd_end_date: Optional[datetime] = Field(default=None, alias="scd_end_date")
    add_date: Optional[datetime] = Field(default=None, alias="add_date")
    last_tasksum_date: Optional[datetime] = Field(default=None, alias="last_tasksum_date")
    fcst_start_date: Optional[datetime] = Field(default=None, alias="fcst_start_date")
    def_duration_type: Optional[str] = Field(default=None, alias="def_duration_type")
    task_code_prefix: Optional[str] = Field(default=None, alias="task_code_prefix")
    guid: Optional[str] = Field(default=None, alias="guid")
    def_qty_type: Optional[str] = Field(default=None, alias="def_qty_type")
    add_by_name: Optional[str] = Field(default=None, alias="add_by_name")
    web_local_root_path: Optional[str] = Field(default=None, alias="web_local_root_path")
    proj_url: Optional[str] = Field(default=None, alias="proj_url")
    def_rate_type: Optional[str] = Field(default=None, alias="def_rate_type")
    add_act_remain_flag: Optional[str] = Field(default=None, alias="add_act_remain_flag") # Y/N flag
    act_this_per_link_flag: Optional[str] = Field(default=None, alias="act_this_per_link_flag") # Y/N flag
    def_task_type: Optional[str] = Field(default=None, alias="def_task_type")
    act_pct_link_flag: Optional[str] = Field(default=None, alias="act_pct_link_flag") # Y/N flag
    critical_path_type: Optional[str] = Field(default=None, alias="critical_path_type")
    task_code_prefix_flag: Optional[str] = Field(default=None, alias="task_code_prefix_flag") # Y/N flag
    def_rollup_dates_flag: Optional[str] = Field(default=None, alias="def_rollup_dates_flag") # Y/N flag
    use_project_baseline_flag: Optional[str] = Field(default=None, alias="use_project_baseline_flag") # Y/N flag
    rem_target_link_flag: Optional[str] = Field(default=None, alias="rem_target_link_flag") # Y/N flag
    reset_planned_flag: Optional[str] = Field(default=None, alias="reset_planned_flag") # Y/N flag
    allow_neg_act_flag: Optional[str] = Field(default=None, alias="allow_neg_act_flag") # Y/N flag
    sum_assign_level: Optional[str] = Field(default=None, alias="sum_assign_level")
    last_fin_dates_id: Optional[int] = Field(default=None, alias="last_fin_dates_id") # Assuming int
    last_baseline_update_date: Optional[datetime] = Field(default=None, alias="last_baseline_update_date") # Note: original used last_fin_dates_id for this
    cr_external_key: Optional[str] = Field(default=None, alias="cr_external_key")
    apply_actuals_date: Optional[datetime] = Field(default=None, alias="apply_actuals_date")
    fintmpl_id: Optional[int] = Field(default=None, alias="fintmpl_id")
    location_id: Optional[int] = Field(default=None, alias="location_id") # Assuming int
    loaded_scope_level: Optional[str] = Field(default=None, alias="loaded_scope_level")
    export_flag: Optional[str] = Field(default=None, alias="export_flag") # Y/N flag
    new_fin_dates_id: Optional[int] = Field(default=None, alias="new_fin_dates_id") # Assuming int
    baselines_to_export: Optional[str] = Field(default=None, alias="baselines_to_export")
    baseline_names_to_export: Optional[str] = Field(default=None, alias="baseline_names_to_export")
    next_data_date: Optional[datetime] = Field(default=None, alias="next_data_date")
    close_period_flag: Optional[str] = Field(default=None, alias="close_period_flag") # Y/N flag
    sum_refresh_date: Optional[datetime] = Field(default=None, alias="sum_refresh_date")
    trsrcsum_loaded: Optional[str] = Field(default=None, alias="trsrcsum_loaded") # Y/N flag
    sumtask_loaded: Optional[str] = Field(default=None, alias="sumtask_loaded") # Y/N flag

    data: Any = Field(default=None, exclude=True)

    @property
    def id(self) -> Optional[int]:
        return self.proj_id

    def get_tsv(self) -> list[Any]:
        model_data = self.model_dump(by_alias=True)
        
        def format_date(dt_val: Any) -> str:
            if isinstance(dt_val, datetime):
                return dt_val.strftime("%Y-%m-%d %H:%M") # Adjust format if XER uses a different one
            elif isinstance(dt_val, str): # If already stringified by model_dump
                return dt_val
            return ""

        return [
            "%R",
            str(model_data.get("proj_id", "")) if model_data.get("proj_id") is not None else "",
            str(model_data.get("fy_start_month_num", "")) if model_data.get("fy_start_month_num") is not None else "",
            model_data.get("rsrc_self_add_flag", "") if model_data.get("rsrc_self_add_flag") is not None else "",
            model_data.get("allow_complete_flag", "") if model_data.get("allow_complete_flag") is not None else "",
            model_data.get("rsrc_multi_assign_flag", "") if model_data.get("rsrc_multi_assign_flag") is not None else "",
            model_data.get("checkout_flag", "") if model_data.get("checkout_flag") is not None else "",
            model_data.get("project_flag", "") if model_data.get("project_flag") is not None else "",
            model_data.get("step_complete_flag", "") if model_data.get("step_complete_flag") is not None else "",
            model_data.get("cost_qty_recalc_flag", "") if model_data.get("cost_qty_recalc_flag") is not None else "",
            model_data.get("batch_sum_flag", "") if model_data.get("batch_sum_flag") is not None else "",
            model_data.get("name_sep_char", "") if model_data.get("name_sep_char") is not None else "",
            model_data.get("def_complete_pct_type", "") if model_data.get("def_complete_pct_type") is not None else "",
            model_data.get("proj_short_name", "") if model_data.get("proj_short_name") is not None else "",
            str(model_data.get("acct_id", "")) if model_data.get("acct_id") is not None else "",
            str(model_data.get("orig_proj_id", "")) if model_data.get("orig_proj_id") is not None else "",
            str(model_data.get("source_proj_id", "")) if model_data.get("source_proj_id") is not None else "",
            str(model_data.get("base_type_id", "")) if model_data.get("base_type_id") is not None else "",
            str(model_data.get("clndr_id", "")) if model_data.get("clndr_id") is not None else "",
            str(model_data.get("sum_base_proj_id", "")) if model_data.get("sum_base_proj_id") is not None else "",
            str(model_data.get("task_code_base", "")) if model_data.get("task_code_base") is not None else "",
            str(model_data.get("task_code_step", "")) if model_data.get("task_code_step") is not None else "",
            str(model_data.get("priority_num", "")) if model_data.get("priority_num") is not None else "",
            str(model_data.get("wbs_max_sum_level", "")) if model_data.get("wbs_max_sum_level") is not None else "",
            str(model_data.get("strgy_priority_num", "")) if model_data.get("strgy_priority_num") is not None else "",
            model_data.get("last_checksum", "") if model_data.get("last_checksum") is not None else "",
            str(model_data.get("critical_drtn_hr_cnt", "")) if model_data.get("critical_drtn_hr_cnt") is not None else "",
            str(model_data.get("def_cost_per_qty", "")) if model_data.get("def_cost_per_qty") is not None else "",
            format_date(model_data.get("last_recalc_date")),
            format_date(model_data.get("plan_start_date")),
            format_date(model_data.get("plan_end_date")),
            format_date(model_data.get("scd_end_date")),
            format_date(model_data.get("add_date")),
            format_date(model_data.get("last_tasksum_date")),
            format_date(model_data.get("fcst_start_date")),
            model_data.get("def_duration_type", "") if model_data.get("def_duration_type") is not None else "",
            model_data.get("task_code_prefix", "") if model_data.get("task_code_prefix") is not None else "",
            model_data.get("guid", "") if model_data.get("guid") is not None else "",
            model_data.get("def_qty_type", "") if model_data.get("def_qty_type") is not None else "",
            model_data.get("add_by_name", "") if model_data.get("add_by_name") is not None else "",
            model_data.get("web_local_root_path", "") if model_data.get("web_local_root_path") is not None else "",
            model_data.get("proj_url", "") if model_data.get("proj_url") is not None else "",
            model_data.get("def_rate_type", "") if model_data.get("def_rate_type") is not None else "",
            model_data.get("add_act_remain_flag", "") if model_data.get("add_act_remain_flag") is not None else "",
            model_data.get("act_this_per_link_flag", "") if model_data.get("act_this_per_link_flag") is not None else "",
            model_data.get("def_task_type", "") if model_data.get("def_task_type") is not None else "",
            model_data.get("act_pct_link_flag", "") if model_data.get("act_pct_link_flag") is not None else "",
            model_data.get("critical_path_type", "") if model_data.get("critical_path_type") is not None else "",
            model_data.get("task_code_prefix_flag", "") if model_data.get("task_code_prefix_flag") is not None else "",
            model_data.get("def_rollup_dates_flag", "") if model_data.get("def_rollup_dates_flag") is not None else "",
            model_data.get("use_project_baseline_flag", "") if model_data.get("use_project_baseline_flag") is not None else "",
            model_data.get("rem_target_link_flag", "") if model_data.get("rem_target_link_flag") is not None else "",
            model_data.get("reset_planned_flag", "") if model_data.get("reset_planned_flag") is not None else "",
            model_data.get("allow_neg_act_flag", "") if model_data.get("allow_neg_act_flag") is not None else "",
            model_data.get("sum_assign_level", "") if model_data.get("sum_assign_level") is not None else "",
            str(model_data.get("last_fin_dates_id", "")) if model_data.get("last_fin_dates_id") is not None else "",
            format_date(model_data.get("last_baseline_update_date")),
            model_data.get("cr_external_key", "") if model_data.get("cr_external_key") is not None else "",
            format_date(model_data.get("apply_actuals_date")),
            str(model_data.get("fintmpl_id", "")) if model_data.get("fintmpl_id") is not None else "",
            str(model_data.get("location_id", "")) if model_data.get("location_id") is not None else "",
            model_data.get("loaded_scope_level", "") if model_data.get("loaded_scope_level") is not None else "",
            model_data.get("export_flag", "") if model_data.get("export_flag") is not None else "",
            str(model_data.get("new_fin_dates_id", "")) if model_data.get("new_fin_dates_id") is not None else "",
            model_data.get("baselines_to_export", "") if model_data.get("baselines_to_export") is not None else "",
            model_data.get("baseline_names_to_export", "") if model_data.get("baseline_names_to_export") is not None else "",
            format_date(model_data.get("next_data_date")),
            model_data.get("close_period_flag", "") if model_data.get("close_period_flag") is not None else "",
            format_date(model_data.get("sum_refresh_date")),
            model_data.get("trsrcsum_loaded", "") if model_data.get("trsrcsum_loaded") is not None else "",
            model_data.get("sumtask_loaded", "") if model_data.get("sumtask_loaded") is not None else "",
        ]

    @property
    def activities(self) -> List["Task"]: # Assuming Task will be a Pydantic model
        """
        Get all activities in this project.
        Relies on self.data being populated with a Data model instance that has a 'tasks' collection.
        """
        if self.data and hasattr(self.data, 'tasks') and hasattr(self.data.tasks, 'get_by_project'):
            return self.data.tasks.get_by_project(self.proj_id)
        return []

    @property
    def wbss(self) -> List["WBS"]: # Assuming WBS will be a Pydantic model
        """
        Get all WBS elements in this project.
        Relies on self.data being populated with a Data model instance that has a 'wbss' collection.
        """
        if self.data and hasattr(self.data, 'wbss') and hasattr(self.data.wbss, 'get_by_project'):
            return self.data.wbss.get_by_project(self.proj_id)
        return []

    def __repr__(self) -> str:
        name = self.proj_short_name if self.proj_short_name is not None else "Unknown Project"
        return f"<{name} (ID: {self.proj_id if self.proj_id is not None else 'N/A'})>"

    class Config:
        arbitrary_types_allowed = True # For self.data: Any
