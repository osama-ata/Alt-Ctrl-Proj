from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.project import Project # Corrected relative import

__all__ = ["Projects"]


class Projects:
    _projects: List[Project]

    def __init__(self, data_context: Optional[Any] = None) -> None:
        self.index: int = 0
        self._projects: List[Project] = []
        self.data_context: Optional[Any] = data_context

    def add(self, params: Dict[str, Any]) -> None: # Removed data argument, will use self.data_context
        """
        Adds a Project to the collection.
        The params dictionary is validated into a Project Pydantic model.
        The main Data object context is passed to the Project instance.
        """
        project_instance = Project.model_validate(params)
        if self.data_context:
            project_instance.data = self.data_context
        self._projects.append(project_instance)

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._projects:
            return []
            
        tsv_data: list[list[Any]] = [["%T", "PROJECT"]]
        # Header matches fields in Project.get_tsv()
        header = [
            "%F", "proj_id", "fy_start_month_num", "rsrc_self_add_flag", "allow_complete_flag", 
            "rsrc_multi_assign_flag", "checkout_flag", "project_flag", "step_complete_flag", 
            "cost_qty_recalc_flag", "batch_sum_flag", "name_sep_char", "def_complete_pct_type", 
            "proj_short_name", "acct_id", "orig_proj_id", "source_proj_id", "base_type_id", 
            "clndr_id", "sum_base_proj_id", "task_code_base", "task_code_step", "priority_num", 
            "wbs_max_sum_level", "strgy_priority_num", "last_checksum", "critical_drtn_hr_cnt", 
            "def_cost_per_qty", "last_recalc_date", "plan_start_date", "plan_end_date", 
            "scd_end_date", "add_date", "last_tasksum_date", "fcst_start_date", 
            "def_duration_type", "task_code_prefix", "guid", "def_qty_type", "add_by_name", 
            "web_local_root_path", "proj_url", "def_rate_type", "add_act_remain_flag", 
            "act_this_per_link_flag", "def_task_type", "act_pct_link_flag", "critical_path_type", 
            "task_code_prefix_flag", "def_rollup_dates_flag", "use_project_baseline_flag", 
            "rem_target_link_flag", "reset_planned_flag", "allow_neg_act_flag", 
            "sum_assign_level", "last_fin_dates_id", "last_baseline_update_date", 
            "cr_external_key", "apply_actuals_date", "fintmpl_id", "location_id", 
            "loaded_scope_level", "export_flag", "new_fin_dates_id", "baselines_to_export", 
            "baseline_names_to_export", "next_data_date", "close_period_flag", 
            "sum_refresh_date", "trsrcsum_loaded", "sumtask_loaded",
        ]
        tsv_data.append(header)
        for proj in self._projects:
            tsv_data.append(proj.get_tsv())
        return tsv_data

    def find_by_id(self, proj_id: int) -> Optional[Project]: # Corrected parameter name and return type
        """Finds a project by its proj_id."""
        return next((proj for proj in self._projects if proj.proj_id == proj_id), None)

    def __repr__(self) -> str:
        return f"<Projects count={len(self._projects)}>"

    def __len__(self) -> int:
        return len(self._projects) # Corrected: was super().__len__() which is wrong if not inheriting

    def __iter__(self) -> Iterator[Project]: # Corrected return type
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> Project:
        if self.index < len(self._projects):
            result = self._projects[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
