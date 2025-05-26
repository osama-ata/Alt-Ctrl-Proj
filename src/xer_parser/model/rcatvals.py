from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.rcatval import RCatVal

__all__ = ["RCatVals"]


class RCatVals:
    _rcatvals: List[RCatVal]

    def __init__(self, data_context: Optional[Any] = None) -> None:
        self.index: int = 0
        self._rcatvals: List[RCatVal] = []
        self.data_context: Optional[Any] = data_context

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds an RCatVal to the collection.
        The params dictionary is validated into an RCatVal Pydantic model.
        """
        rcatval_instance = RCatVal.model_validate(params)
        if self.data_context: # Though RCatVal may not use it now, good for consistency
            rcatval_instance.data = self.data_context
        self._rcatvals.append(rcatval_instance)

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._rcatvals:
            return []
            
        tsv_data: list[list[str | int | None]] = [["%T", "RCATVAL"]] # Type hint for tsv_data
        header = [
            "%F",
            "rsrc_catg_id", "rsrc_catg_type_id", "rsrc_catg_short_name", 
            "rsrc_catg_name", "parent_rsrc_catg_id",
        ]
        # Note: The RCatVal model has an optional seq_num, but it's not in the original get_tsv header.
        # If it needs to be included, the header and RCatVal.get_tsv() should be updated.
        tsv_data.append(header)
        for rcatval_item in self._rcatvals:
            tsv_data.append(rcatval_item.get_tsv())
        return tsv_data

    def find_by_id(self, rsrc_catg_id: int) -> Optional[RCatVal]: # Corrected parameter name and return type
        """Finds a resource category value by its rsrc_catg_id."""
        return next((rcatval for rcatval in self._rcatvals if rcatval.rsrc_catg_id == rsrc_catg_id), None)

    @property
    def count(self) -> int:
        return len(self._rcatvals)

    def __len__(self) -> int:
        return len(self._rcatvals)

    def __iter__(self) -> Iterator[RCatVal]: # Corrected return type
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> RCatVal:
        if self.index < len(self._rcatvals):
            result = self._rcatvals[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
