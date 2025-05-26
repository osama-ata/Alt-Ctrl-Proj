from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.taskrsrc import TaskRsrc

__all__ = ["ActivityResources"]


class ActivityResources:
    _taskrsrc: List[TaskRsrc]

    def __init__(self) -> None:
        self.index: int = 0
        self._taskrsrc: List[TaskRsrc] = []
        # self.data_context: Optional[Any] = None # Main Data object, if this collection is part of it

    def add(self, params: Dict[str, Any], data_context: Optional[Any] = None) -> None:
        """
        Adds a TaskRsrc to the collection.
        The params dictionary is validated into a TaskRsrc Pydantic model.
        The data_context (main Data object) is passed to the instance for relationship navigation.
        """
        task_rsrc_instance = TaskRsrc.model_validate(params)
        if data_context:
            task_rsrc_instance.data = data_context
        self._taskrsrc.append(task_rsrc_instance)

    def find_by_id(self, taskrsrc_id: int) -> Optional[TaskRsrc]:
        for rsrc_assignment in self._taskrsrc:
            if rsrc_assignment.taskrsrc_id == taskrsrc_id:
                return rsrc_assignment
        return None

    def get_tsv(self) -> list:
        if not self._taskrsrc:
            return []
            
        tsv_data = [["%T", "TASKRSRC"]]
        header = [
            "%F", "taskrsrc_id", "task_id", "proj_id", "cost_qty_link_flag", "role_id", 
            "acct_id", "rsrc_id", "pobs_id", "skill_level", "remain_qty", "target_qty", 
            "remain_qty_per_hr", "target_lag_drtn_hr_cnt", "target_qty_per_hr", 
            "act_ot_qty", "act_reg_qty", "relag_drtn_hr_cnt", "ot_factor", "cost_per_qty", 
            "target_cost", "act_reg_cost", "act_ot_cost", "remain_cost", "act_start_date", 
            "act_end_date", "restart_date", "reend_date", "target_start_date", 
            "target_end_date", "rem_late_start_date", "rem_late_end_date", 
            "rollup_dates_flag", "target_crv", "remain_crv", "actual_crv", 
            "ts_pend_act_end_flag", "guid", "rate_type", "act_this_per_cost", 
            "act_this_per_qty", "curv_id", "rsrc_type", "cost_per_qty_source_type", 
            "create_user", "create_date", "cbs_id", "has_rsrchours", "taskrsrc_sum_id",
        ]
        tsv_data.append(header)
        for taskrsrc_item in self._taskrsrc:
            tsv_data.append(taskrsrc_item.get_tsv())
        return tsv_data

    def find_by_rsrc_id(self, rsrc_id: int) -> List[TaskRsrc]:
        return [r for r in self._taskrsrc if r.rsrc_id == rsrc_id]

    def find_by_activity_id(self, task_id: int) -> List[TaskRsrc]:
        # Original filtered also on x.rsrc_id existing, which is implicit if it's an int/Optional[int]
        return [r for r in self._taskrsrc if r.task_id == task_id]

    @property
    def count(self) -> int:
        return len(self._taskrsrc)

    def __len__(self) -> int:
        return len(self._taskrsrc) # Corrected from ActivityResources._taskrsrc

    def __iter__(self) -> Iterator[TaskRsrc]:
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> TaskRsrc:
        if self.index < len(self._taskrsrc):
            result = self._taskrsrc[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
