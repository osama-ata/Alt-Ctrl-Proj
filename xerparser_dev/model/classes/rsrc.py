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


import json
from typing import Any, ClassVar, Dict, List, Optional


class Resource:
    """
    Represents a Primavera P6 resource.

    This class encapsulates all the attributes and functionalities of a resource in Primavera P6,
    including labor and non-labor resources that can be assigned to activities.

    Parameters
    ----------
    params : Dict[str, Any]
        Dictionary of parameters from the XER file

    Attributes
    ----------
    rsrc_id : int
        Unique identifier for the resource
    rsrc_name : str
        Name of the resource
    rsrc_short_name : str
        Short name of the resource
    rsrc_type : str
        Type of resource (Labor, Non-Labor, etc.)
    parent_rsrc_id : int
        ID of the parent resource in a hierarchical structure
    clndr_id : int
        ID of the calendar assigned to this resource
    role_id : int
        ID of the role assigned to this resource
    active_flag : str
        Flag indicating whether the resource is active
    email_addr : str
        Email address of the resource (for labor resources)
    """

    obj_list: ClassVar[List["Resource"]] = []

    def __init__(self, params: Dict[str, Any]) -> None:
        """
        Initialize a Resource object from XER file parameters.

        Parameters
        ----------
        params : Dict[str, Any]
            Dictionary of parameters from the XER file
        """
        self.rsrc_id = (
            int(params.get("rsrc_id").strip()) if params.get("rsrc_id") else None
        )
        self.parent_rsrc_id = (
            int(params.get("parent_rsrc_id").strip())
            if params.get("parent_rsrc_id")
            else None
        )
        self.clndr_id = (
            int(params.get("clndr_id").strip()) if params.get("clndr_id") else None
        )
        self.role_id = (
            int(params.get("role_id").strip()) if params.get("role_id") else None
        )
        self.shift_id = (
            params.get("shift_id").strip() if params.get("shift_id") else None
        )
        self.user_id = params.get("user_id").strip() if params.get("user_id") else None
        self.pobs_id = params.get("pobs_id").strip() if params.get("pobs_id") else None
        self.guid = params.get("guid").strip() if params.get("guid") else None
        self.rsrc_seq_num = (
            params.get("rsrc_seq_num").strip() if params.get("rsrc_seq_num") else None
        )
        self.email_addr = (
            params.get("email_addr").strip() if params.get("email_addr") else None
        )
        self.employee_code = (
            params.get("employee_code").strip() if params.get("employee_code") else None
        )
        self.office_phone = (
            params.get("office_phone").strip() if params.get("office_phone") else None
        )
        self.other_phone = (
            params.get("other_phone").strip() if params.get("other_phone") else None
        )
        self.rsrc_name = (
            params.get("rsrc_name").strip() if params.get("rsrc_name") else None
        )
        self.rsrc_short_name = (
            params.get("rsrc_short_name").strip()
            if params.get("rsrc_short_name")
            else None
        )
        self.rsrc_title_name = (
            params.get("rsrc_title_name").strip()
            if params.get("rsrc_title_name")
            else None
        )
        self.def_qty_per_hr = (
            params.get("def_qty_per_hr").strip()
            if params.get("def_qty_per_hr")
            else None
        )
        self.cost_qty_type = (
            params.get("cost_qty_type").strip() if params.get("cost_qty_type") else None
        )
        self.ot_factor = (
            params.get("ot_factor").strip() if params.get("ot_factor") else None
        )
        self.active_flag = (
            params.get("active_flag").strip() if params.get("active_flag") else None
        )
        self.auto_compute_act_flag = (
            params.get("auto_compute_act_flag").strip()
            if params.get("auto_compute_act_flag")
            else None
        )
        self.def_cost_qty_link_flag = (
            params.get("def_cost_qty_link_flag").strip()
            if params.get("def_cost_qty_link_flag")
            else None
        )
        self.ot_flag = params.get("ot_flag").strip() if params.get("ot_flag") else None
        self.curr_id = (
            int(params.get("curr_id").strip()) if params.get("curr_id") else None
        )
        self.unit_id = (
            int(params.get("unit_id").strip()) if params.get("unit_id") else None
        )
        self.rsrc_type = (
            params.get("rsrc_type").strip() if params.get("rsrc_type") else None
        )
        self.location_id = (
            int(params.get("location_id").strip())
            if params.get("location_id")
            else None
        )
        self.rsrc_notes = (
            params.get("rsrc_notes").strip() if params.get("rsrc_notes") else None
        )
        self.load_tasks_flag = (
            params.get("load_tasks_flag").strip()
            if params.get("load_tasks_flag")
            else None
        )
        self.level_flag = (
            params.get("level_flag").strip() if params.get("level_flag") else None
        )
        self.last_checksum = (
            params.get("level_flag").strip() if params.get("level_flag") else None
        )
        Resource.obj_list.append(self)

    def get_id(self) -> int:
        """
        Get the resource ID.

        Returns
        -------
        int
            The unique identifier for this resource
        """
        return self.rsrc_id

    def get_tsv(self) -> List[Any]:
        """
        Get the resource data in TSV format.

        Returns
        -------
        List[Any]
            Resource data formatted for TSV output
        """
        tsv = [
            "%R",
            self.rsrc_id,
            self.parent_rsrc_id,
            self.clndr_id,
            self.role_id,
            self.shift_id,
            self.user_id,
            self.pobs_id,
            self.guid,
            self.rsrc_seq_num,
            self.email_addr,
            self.employee_code,
            self.office_phone,
            self.other_phone,
            self.rsrc_name,
            self.rsrc_short_name,
            self.rsrc_title_name,
            self.def_qty_per_hr,
            self.cost_qty_type,
            self.ot_factor,
            self.active_flag,
            self.auto_compute_act_flag,
            self.def_cost_qty_link_flag,
            self.ot_flag,
            self.curr_id,
            self.unit_id,
            self.rsrc_type,
            self.location_id,
            self.rsrc_notes,
            self.load_tasks_flag,
            self.level_flag,
            self.last_checksum,
        ]
        return tsv

    @classmethod
    def find_by_id(cls, id: int) -> Optional["Resource"]:
        """
        Find a resource by its ID.

        Parameters
        ----------
        id : int
            The resource ID to search for

        Returns
        -------
        Resource or None
            The resource with the specified ID, or None if not found
        """
        obj = list(filter(lambda x: x.rsrc_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return None

    @property
    def parent(self) -> Optional[int]:
        """
        Get the parent resource ID.

        Returns
        -------
        int or None
            The ID of the parent resource, or None if this is a top-level resource
        """
        return self.parent_rsrc_id

    def __repr__(self) -> str:
        """
        String representation of the resource.

        Returns
        -------
        str
            The resource's name
        """
        return self.rsrc_name

    def __str__(self) -> str:
        """
        String representation of the resource.

        Returns
        -------
        str
            The resource's name
        """
        return self.rsrc_name

    def toJson(self) -> str:
        """
        Convert the resource to a JSON string.

        Returns
        -------
        str
            JSON representation of the resource
        """
        return json.dumps(self, default=lambda o: o.__dict__)
