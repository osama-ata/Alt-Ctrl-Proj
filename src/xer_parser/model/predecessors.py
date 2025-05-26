from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.taskpred import TaskPred

__all__ = ["Predecessors"]


class Predecessors:
    """
    Container class for managing relationships between activities in Primavera P6.
    This class provides functionality to store, retrieve, and manipulate
    relationship objects (TaskPred).
    """
    _task_preds: List[TaskPred] # Renamed for convention

    def __init__(self, data_context: Optional[Any] = None) -> None:
        """
        Initialize an empty Predecessors container.
        """
        self.index: int = 0
        self._task_preds: List[TaskPred] = [] # Renamed for convention
        self.data_context: Optional[Any] = data_context

    def find_by_id(self, task_pred_id: int) -> Optional[TaskPred]: # Corrected param name
        """
        Find a relationship by its task_pred_id.
        """
        return next((pred for pred in self._task_preds if pred.task_pred_id == task_pred_id), None)

    def get_tsv(self) -> list: # Return type changed to list for consistency
        """
        Get all relationships in TSV format.
        """
        if not self._task_preds:
            return []
            
        tsv_data: list[list[Any]] = [["%T", "TASKPRED"]]
        header = [
            "%F", "task_pred_id", "task_id", "pred_task_id", "proj_id", "pred_proj_id",
            "pred_type", "lag_hr_cnt", "comments", "float_path", "aref", "arls",
        ]
        tsv_data.append(header)
        for pred in self._task_preds:
            tsv_data.append(pred.get_tsv())
        return tsv_data

    def add(self, params: Dict[str, Any]) -> None:
        """
        Add a new relationship to the container.
        The params dictionary is validated into a TaskPred Pydantic model.
        """
        task_pred_instance = TaskPred.model_validate(params)
        if self.data_context:
             task_pred_instance.data = self.data_context
        self._task_preds.append(task_pred_instance)

    @property
    def relations(self) -> List[TaskPred]: # Type hint updated
        """
        Get all relationships.
        """
        return self._task_preds

    @property
    def leads(self) -> List[TaskPred]: # Type hint updated
        """
        Get all relationships with lead time (negative lag).
        """
        return [
            pred for pred in self._task_preds if pred.lag_hr_cnt is not None and pred.lag_hr_cnt < 0
        ]

    @property
    def finish_to_start(self) -> List[TaskPred]: # Type hint updated
        """
        Get all Finish-to-Start relationships.
        """
        return [pred for pred in self._task_preds if pred.pred_type == "PR_FS"]

    def get_successors(self, act_id: int) -> List[TaskPred]: # Type hint updated
        """
        Get all successor relationships for a given activity.
        """
        return [pred for pred in self._task_preds if pred.pred_task_id == act_id]

    def get_predecessors(self, act_id: int) -> List[TaskPred]: # Type hint updated
        """
        Get all predecessor relationships for a given activity.
        """
        return [pred for pred in self._task_preds if pred.task_id == act_id]

    def count(self) -> int:
        """
        Get the number of relationships.
        """
        return len(self._task_preds)

    def __len__(self) -> int:
        """
        Get the number of relationships.
        """
        return len(self._task_preds)

    def __iter__(self) -> Iterator[TaskPred]: # Corrected return type
        """
        Make Predecessors iterable.
        """
        self.index = 0 # Reset index for each new iteration
        return self

    def __next__(self) -> TaskPred:
        """
        Get the next relationship in the iteration.
        """
        if self.index < len(self._task_preds):
            result = self._task_preds[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
