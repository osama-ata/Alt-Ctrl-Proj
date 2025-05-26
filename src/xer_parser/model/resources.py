from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.rsrc import Resource # Corrected relative import

__all__ = ["Resources"]


class Resources:
    """
    Container class for managing Primavera P6 resources.
    This class provides functionality to store, retrieve, and manipulate
    Resource objects, supporting both individual resource operations and
    hierarchical resource structures.
    """
    _rsrcs: List[Resource]

    def __init__(self, data_context: Optional[Any] = None) -> None:
        """
        Initialize an empty Resources container.
        """
        self.index: int = 0
        self._rsrcs: List[Resource] = []
        self.data_context: Optional[Any] = data_context

    def add(self, params: Dict[str, Any]) -> None:
        """
        Add a new resource to the container.
        The params dictionary is validated into a Resource Pydantic model.
        """
        resource_instance = Resource.model_validate(params)
        if self.data_context:
            resource_instance.data = self.data_context
        self._rsrcs.append(resource_instance)

    def get_resource_by_id(self, rsrc_id: int) -> Optional[Resource]: # Parameter name changed for clarity
        """
        Find a resource by its rsrc_id.
        """
        return next((rsrc for rsrc in self._rsrcs if rsrc.rsrc_id == rsrc_id), None)

    def get_parent(self, rsrc_id: int) -> Optional[Resource]: # Parameter name changed
        """
        Find the parent resource of a given resource.
        """
        resource = self.get_resource_by_id(rsrc_id)
        if resource and resource.parent_rsrc_id is not None:
            return self.get_resource_by_id(resource.parent_rsrc_id)
        return None

    def __iter__(self) -> Iterator[Resource]: # Corrected return type
        """
        Make Resources iterable.
        """
        self.index = 0 # Reset index for each new iteration
        return self

    def __next__(self) -> Resource:
        """
        Get the next resource in the iteration.
        """
        if self.index < len(self._rsrcs):
            result = self._rsrcs[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def _get_list(self) -> list[tuple[Optional[int], Optional[int]]]: # Adjusted type hint
        """
        Get a list of resource ID and parent resource ID pairs.
        """
        return [(res.rsrc_id, res.parent_rsrc_id) for res in self._rsrcs]


    def get_tsv(self) -> list: # Return type changed to list for consistency
        """
        Get all resources in TSV format.
        """
        if not self._rsrcs:
            return []
            
        tsv_data: list[list[Any]] = [["%T", "RSRC"]]
        header = [
            "%F", "rsrc_id", "parent_rsrc_id", "clndr_id", "role_id", "shift_id", "user_id", 
            "pobs_id", "guid", "rsrc_seq_num", "email_addr", "employee_code", "office_phone", 
            "other_phone", "rsrc_name", "rsrc_short_name", "rsrc_title_name", "def_qty_per_hr", 
            "cost_qty_type", "ot_factor", "active_flag", "auto_compute_act_flag", 
            "def_cost_qty_link_flag", "ot_flag", "curr_id", "unit_id", "rsrc_type", 
            "location_id", "rsrc_notes", "load_tasks_flag", "level_flag", "last_checksum",
        ]
        tsv_data.append(header)
        for rsrc_item in self._rsrcs:
            tsv_data.append(rsrc_item.get_tsv())
        return tsv_data

    def build_tree(self) -> list[dict[Optional[int], Any]]: # Adjusted type hint for dict key
        """
        Build a hierarchical tree structure of resources.
        """
        nodes: Dict[int, Dict[Optional[int], Any]] = {} # Adjusted type hint
        for rsrc in self._rsrcs:
            if rsrc.rsrc_id is not None: # Ensure rsrc_id is not None before using as key
                 nodes[rsrc.rsrc_id] = {"node_obj": rsrc, "children": []}

        forest = []
        for rsrc in self._rsrcs:
            if rsrc.rsrc_id is None: continue # Skip if rsrc_id is None
            
            node_dict_entry = nodes[rsrc.rsrc_id]
            
            # Re-structure node to be {rsrc_id: node_obj, children: []} if needed by consumer
            # For now, using a simpler structure for the list items in forest
            # Current node_dict_entry is already {"node_obj": rsrc, "children": []}

            if rsrc.parent_rsrc_id is None or rsrc.parent_rsrc_id not in nodes:
                forest.append(node_dict_entry) 
            else:
                parent_node_dict_entry = nodes[rsrc.parent_rsrc_id]
                parent_node_dict_entry["children"].append(node_dict_entry)
        return forest

    @property
    def count(self) -> int:
        return len(self._rsrcs)

    def __len__(self) -> int:
        return len(self._rsrcs)
