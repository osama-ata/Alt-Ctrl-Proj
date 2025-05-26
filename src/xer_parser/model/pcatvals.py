from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.pcatval import PCatVal

__all__ = ["PCatVals"]


class PCatVals:
    _pcatvals: List[PCatVal] # Changed attribute name to lowercase

    def __init__(self, data_context: Optional[Any] = None) -> None:
        self.index: int = 0
        self._pcatvals: List[PCatVal] = [] # Changed attribute name to lowercase
        self.data_context: Optional[Any] = data_context

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds a PCatVal to the collection.
        The params dictionary is validated into a PCatVal Pydantic model.
        """
        pcatval_instance = PCatVal.model_validate(params)
        if self.data_context: # Though PCatVal may not use it now, good for consistency
            pcatval_instance.data = self.data_context
        self._pcatvals.append(pcatval_instance) # Changed attribute name to lowercase

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._pcatvals: # Changed attribute name to lowercase
            return []
            
        tsv_data: list[list[str | int | None]] = [["%T", "PCATVAL"]] # Type hint for tsv_data
        header = [
            "%F",
            "proj_catg_id", "proj_catg_type_id", "seq_num", 
            "proj_catg_short_name", "parent_proj_catg_id", "proj_catg_name",
        ]
        tsv_data.append(header)
        for pcatval_item in self._pcatvals: # Changed attribute name to lowercase
            tsv_data.append(pcatval_item.get_tsv())
        return tsv_data

    def find_by_id(self, proj_catg_id: int) -> Optional[PCatVal]: # Corrected parameter name and return type
        """Finds a project category value by its proj_catg_id."""
        # Original filter used getattr, direct attribute access is fine with Pydantic
        return next((pcatval for pcatval in self._pcatvals if pcatval.proj_catg_id == proj_catg_id), None)

    @property
    def count(self) -> int:
        return len(self._pcatvals) # Changed attribute name to lowercase

    def __len__(self) -> int:
        return len(self._pcatvals) # Changed attribute name to lowercase

    def __iter__(self) -> Iterator[PCatVal]: # Corrected return type
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> PCatVal:
        if self.index < len(self._pcatvals): # Changed attribute name to lowercase
            result = self._pcatvals[self.index] # Changed attribute name to lowercase
            self.index += 1
            return result
        else:
            raise StopIteration
