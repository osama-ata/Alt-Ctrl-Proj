from typing import Any

from xer_parser.model.classes.taskpred import TaskPred

__all__ = ["Predecessors"]


class Predecessors:
    """
    Container class for managing relationships between activities in Primavera P6.

    This class provides functionality to store, retrieve, and manipulate
    relationship objects (TaskPred), which represent logical connections between
    activities in a project schedule.

    Attributes
    ----------
    task_pred : List[TaskPred]
        Internal list of TaskPred objects representing activity relationships
    index : int
        Current index for iterator functionality

    Notes
    -----
    In Primavera P6, relationships can be of four types:
    - Finish-to-Start (FS): The successor activity cannot start until the predecessor finishes
    - Start-to-Start (SS): The successor activity cannot start until the predecessor starts
    - Finish-to-Finish (FF): The successor activity cannot finish until the predecessor finishes
    - Start-to-Finish (SF): The successor activity cannot finish until the predecessor starts

    Relationships can also have lag (positive value) or lead (negative value) time.
    """

    def __init__(self) -> None:
        """
        Initialize an empty Predecessors container.
        """
        self.index = 0
        self.task_pred = []

    def find_by_id(self, code_id: int) -> TaskPred | None:
        """
        Find a relationship by its ID.

        Parameters
        ----------
        code_id : int
            The relationship ID to search for

        Returns
        -------
        TaskPred or None
            The relationship with the specified ID, or None if not found
        """
        obj = list(filter(lambda x: x.task_pred_id == code_id, self.task_pred))
        if len(obj) > 0:
            return obj[0]
        return None

    def get_tsv(self) -> list[list[Any]]:
        """
        Get all relationships in TSV format.

        Returns
        -------
        list[list[Any]]
            Relationship data formatted for TSV output
        """
        tsv = []
        if len(self.task_pred) > 0:
            tsv.append(["%T", "TASKPRED"])
            tsv.append(
                [
                    "%F",
                    "task_pred_id",
                    "task_id",
                    "pred_task_id",
                    "proj_id",
                    "pred_proj_id",
                    "pred_type",
                    "lag_hr_cnt",
                    "comments",
                    "float_path",
                    "aref",
                    "arls",
                ]
            )
            for pred in self.task_pred:
                tsv.append(pred.get_tsv())
        return tsv

    def add(self, params: dict[str, Any]) -> None:
        """
        Add a new relationship to the container.

        Parameters
        ----------
        params : dict[str, Any]
            Dictionary of parameters from the XER file to create a new TaskPred
        """
        pred = TaskPred(params)
        self.task_pred.append(pred)

    @property
    def relations(self) -> list[TaskPred]:
        """
        Get all relationships.

        Returns
        -------
        list[TaskPred]
            List of all relationships in the container
        """
        return self.task_pred

    @property
    def leads(self) -> list[TaskPred]:
        """
        Get all relationships with lead time (negative lag).

        Returns
        -------
        list[TaskPred]
            List of relationships with negative lag values
        """
        return list(
            filter(lambda x: x.lag_hr_cnt < 0 if x.lag_hr_cnt else None, self.task_pred)
        )

    @property
    def finish_to_start(self) -> list[TaskPred]:
        """
        Get all Finish-to-Start relationships.

        Returns
        -------
        list[TaskPred]
            List of Finish-to-Start relationships
        """
        return list(filter(lambda x: x.pred_type == "PR_FS", self.task_pred))

    def get_successors(self, act_id: int) -> list[TaskPred]:
        """
        Get all successor relationships for a given activity.

        Parameters
        ----------
        act_id : int
            The activity ID for which to find successors

        Returns
        -------
        list[TaskPred]
            List of relationships where the specified activity is a predecessor
        """
        succ = list(filter(lambda x: x.pred_task_id == act_id, self.task_pred))
        return succ

    def get_predecessors(self, act_id: int) -> list[TaskPred]:
        """
        Get all predecessor relationships for a given activity.

        Parameters
        ----------
        act_id : int
            The activity ID for which to find predecessors

        Returns
        -------
        list[TaskPred]
            List of relationships where the specified activity is a successor
        """
        succ = list(filter(lambda x: x.task_id == act_id, self.task_pred))
        return succ

    def count(self) -> int:
        """
        Get the number of relationships.

        Returns
        -------
        int
            The number of relationships in the container
        """
        return len(self.task_pred)

    def __len__(self) -> int:
        """
        Get the number of relationships.

        Returns
        -------
        int
            The number of relationships in the container
        """
        return len(self.task_pred)

    def __iter__(self) -> "Predecessors":
        """
        Make Predecessors iterable.

        Returns
        -------
        Predecessors
            Self reference for iterator
        """
        return self

    def __next__(self) -> TaskPred:
        """
        Get the next relationship in the iteration.

        Returns
        -------
        TaskPred
            The next relationship in the collection

        Raises
        ------
        StopIteration
            When there are no more relationships to iterate
        """
        if self.index >= len(self.task_pred):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self.task_pred[idx]
