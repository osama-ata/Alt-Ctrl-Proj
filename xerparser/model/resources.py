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


from typing import Any, Dict, List, Optional, Tuple

from xerparser.model.classes.rsrc import Resource


class Resources:
    """
    Container class for managing Primavera P6 resources.

    This class provides functionality to store, retrieve, and manipulate
    Resource objects, supporting both individual resource operations and
    hierarchical resource structures.

    Attributes
    ----------
    _rsrcs : List[Resource]
        Internal list of Resource objects
    index : int
        Current index for iterator functionality
    """

    def __init__(self) -> None:
        """
        Initialize an empty Resources container.
        """
        self.index = 0
        self._rsrcs = []

    def add(self, params: Dict[str, Any]) -> None:
        """
        Add a new resource to the container.

        Parameters
        ----------
        params : Dict[str, Any]
            Dictionary of parameters from the XER file to create a new Resource
        """
        rsrc = Resource(params)
        self._rsrcs.append(rsrc)

    def get_resource_by_id(self, id: int) -> Optional[Resource]:
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
        rsrc = list(filter(lambda x: x.rsrc_id == id, self._rsrcs))
        if len(rsrc) > 0:
            rsrc = rsrc[0]
        else:
            rsrc = None
        return rsrc

    def get_parent(self, id: int) -> Optional[Resource]:
        """
        Find the parent resource of a given resource.

        Parameters
        ----------
        id : int
            The resource ID for which to find the parent

        Returns
        -------
        Resource or None
            The parent resource, or None if the resource has no parent or is not found
        """
        rsrc = list(filter(lambda x: x.rsrc_id == id, self._rsrcs))
        if len(rsrc) > 0:
            rsrc = rsrc[0]
        else:
            rsrc = None
        return rsrc

    def __iter__(self) -> "Resources":
        """
        Make Resources iterable.

        Returns
        -------
        Resources
            Self reference for iterator
        """
        return self

    def __next__(self) -> Resource:
        """
        Get the next resource in the iteration.

        Returns
        -------
        Resource
            The next resource in the collection

        Raises
        ------
        StopIteration
            When there are no more resources to iterate
        """
        if self.index >= len(self._rsrcs):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rsrcs[idx]

    def _get_list(self) -> List[Tuple[int, Optional[int]]]:
        """
        Get a list of resource ID and parent resource ID pairs.

        Returns
        -------
        List[Tuple[int, Optional[int]]]
            List of tuples containing (resource_id, parent_resource_id)
        """
        resor = []
        for res in self._rsrcs:
            resor.append((res.rsrc_id, res.parent_rsrc_id))
        return resor

    def get_tsv(self) -> List[List[Any]]:
        """
        Get all resources in TSV format.

        Returns
        -------
        List[List[Any]]
            Resources data formatted for TSV output
        """
        tsv = []
        if len(self._rsrcs) > 0:
            tsv.append(["%T", "RSRC"])
            tsv.append(
                [
                    "%F",
                    "rsrc_id",
                    "parent_rsrc_id",
                    "clndr_id",
                    "role_id",
                    "shift_id",
                    "user_id",
                    "pobs_id",
                    "guid",
                    "rsrc_seq_num",
                    "email_addr",
                    "employee_code",
                    "office_phone",
                    "other_phone",
                    "rsrc_name",
                    "rsrc_short_name",
                    "rsrc_title_name",
                    "def_qty_per_hr",
                    "cost_qty_type",
                    "ot_factor",
                    "active_flag",
                    "auto_compute_act_flag",
                    "def_cost_qty_link_flag",
                    "ot_flag",
                    "curr_id",
                    "unit_id",
                    "rsrc_type",
                    "location_id",
                    "rsrc_notes",
                    "load_tasks_flag",
                    "level_flag",
                    "last_checksum",
                ]
            )
            for rsr in self._rsrcs:
                tsv.append(rsr.get_tsv())
        return tsv

    def build_tree(self) -> List[Dict[int, Any]]:
        """
        Build a hierarchical tree structure of resources.

        This method organizes resources into their hierarchical structure based on
        parent-child relationships. Resources without parents form the roots of separate
        trees in the resulting forest.

        Returns
        -------
        List[Dict[int, Any]]
            A forest of resource trees, where each tree represents a hierarchical
            structure of resources
        """
        # pass 1: create nodes dictionary
        a = self._get_list()
        nodes = {}
        for i in a:
            id, parent_id = i
            nodes[id] = {id: self.get_resource_by_id(id)}
        # a = a[1:]
        # pass 2: create trees and parent-child relations
        forest = []
        for i in a:
            id, parent_id = i
            node = nodes[id]
            # either make the node a new tree or link it to its parent
            if parent_id is None or nodes.get(parent_id) is None:
                # start a new tree in the forest
                forest.append(node)
            else:
                # add new_node as child to parent
                parent = nodes.get(parent_id)

                if "children" not in parent:
                    # ensure parent has a 'children' field
                    parent["children"] = []
                children = parent["children"]
                children.append(node)
        return forest
