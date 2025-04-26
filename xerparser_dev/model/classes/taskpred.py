# PyP6XER
# Copyright (C) 2020, 2021 Hassan Emam <hassan@constology.com>
#
# This file is part of PyP6XER.
#
# PyP6XER library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v2.1 as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyP6XER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>.

from typing import Any, ClassVar, Dict, List, Optional, Union


class TaskPred:
    """
    Represents a relationship between two activities in Primavera P6.

    This class encapsulates a logical connection between two activities, defining
    how they are related in time. Relationships are directional, having a predecessor
    and a successor activity, a relationship type, and an optional lag or lead time.

    Parameters
    ----------
    params : Dict[str, Any]
        Dictionary of parameters from the XER file

    Attributes
    ----------
    task_pred_id : str
        Unique identifier for the relationship
    task_id : int
        ID of the successor task
    pred_task_id : int
        ID of the predecessor task
    pred_type : str
        Type of relationship: 'PR_FS' (Finish-to-Start), 'PR_SS' (Start-to-Start),
        'PR_FF' (Finish-to-Finish), or 'PR_SF' (Start-to-Finish)
    lag_hr_cnt : float
        Lag time in hours between the predecessor and successor
        Positive values represent lag (delay), negative values represent lead (acceleration)
    proj_id : int
        Project ID to which the successor task belongs
    pred_proj_id : int
        Project ID to which the predecessor task belongs
    float_path : str
        Float path indicator
    comments : str
        Comments associated with the relationship

    Notes
    -----
    Relationship types in Primavera P6 are defined as:
    - Finish-to-Start (PR_FS): The successor cannot start until the predecessor finishes
    - Start-to-Start (PR_SS): The successor cannot start until the predecessor starts
    - Finish-to-Finish (PR_FF): The successor cannot finish until the predecessor finishes
    - Start-to-Finish (PR_SF): The successor cannot finish until the predecessor starts
    """

    obj_list: ClassVar[List["TaskPred"]] = []

    def __init__(self, params: Dict[str, Any]) -> None:
        """
        Initialize a TaskPred object from XER file parameters.

        Parameters
        ----------
        params : Dict[str, Any]
            Dictionary of parameters from the XER file
        """
        self.task_pred_id = (
            params.get("task_pred_id").strip() if params.get("task_pred_id") else None
        )
        self.task_id = int(params.get("task_id")) if params.get("task_id") else None
        self.pred_task_id = (
            int(params.get("pred_task_id")) if params.get("pred_task_id") else None
        )
        self.proj_id = (
            int(params.get("proj_id").strip()) if params.get("proj_id") else None
        )
        self.pred_proj_id = (
            int(params.get("proj_id").strip()) if params.get("pred_proj_id") else None
        )
        self.pred_type = (
            params.get("pred_type").strip() if params.get("pred_type") else None
        )
        self.lag_hr_cnt = (
            float(params.get("lag_hr_cnt").strip())
            if params.get("lag_hr_cnt")
            else None
        )
        self.float_path = (
            params.get("float_path").strip() if params.get("float_path") else None
        )
        self.aref = params.get("aref").strip() if params.get("aref") else None
        self.arls = params.get("arls").strip() if params.get("arls") else None
        self.comments = (
            params.get("comments").strip() if params.get("comments") else None
        )
        TaskPred.obj_list.append(self)

    def get_id(self) -> str:
        """
        Get the relationship ID.

        Returns
        -------
        str
            The unique identifier for this relationship
        """
        return self.task_pred_id

    def get_tsv(self) -> List[Any]:
        """
        Get the relationship data in TSV format.

        Returns
        -------
        List[Any]
            Relationship data formatted for TSV output
        """
        tsv = [
            "%R",
            self.task_pred_id,
            self.task_id,
            self.pred_task_id,
            self.proj_id,
            self.pred_proj_id,
            self.pred_type,
            self.lag_hr_cnt,
            self.comments,
            self.float_path,
            self.aref,
            self.arls,
        ]
        return tsv

    def __repr__(self) -> str:
        """
        String representation of the relationship.

        Returns
        -------
        str
            A string representing the relationship in the format:
            "predecessor_id - relationship_type -> successor_id lag: lag_value"
        """
        return (
            str(self.pred_task_id)
            + "- "
            + self.pred_type
            + " ->"
            + str(self.task_id)
            + " lag: "
            + str(self.lag_hr_cnt)
        )
