from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.nonwork import NonWork # Corrected relative import

__all__ = ["NonWorks"]


class NonWorks:
    _nonworks: List[NonWork] # Changed attribute name to lowercase

    def __init__(self, data_context: Optional[Any] = None) -> None:
        self.index: int = 0
        self._nonworks: List[NonWork] = [] # Changed attribute name to lowercase
        self.data_context: Optional[Any] = data_context # Store if needed for NonWork instances

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds a NonWork to the collection.
        The params dictionary is validated into a NonWork Pydantic model.
        """
        nonwork_instance = NonWork.model_validate(params)
        if self.data_context: # Though NonWork may not use it now, good for consistency
            nonwork_instance.data = self.data_context
        self._nonworks.append(nonwork_instance) # Changed attribute name to lowercase

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._nonworks: # Changed attribute name to lowercase
            return []
            
        tsv_data: list[list[str]] = [["%T", "NONWORK"]]
        header = ["%F", "nonwork_type_id", "seq_num", "nonwork_code", "nonwork_type"]
        tsv_data.append(header)
        for nw in self._nonworks: # Changed attribute name to lowercase
            tsv_data.append(nw.get_tsv())
        return tsv_data

    def find_by_id(self, nonwork_type_id: int) -> Optional[NonWork]: # Corrected parameter name and return type
        """Finds a non-work type by its nonwork_type_id."""
        # Original filter was x.fintmpl_id == id, corrected to x.nonwork_type_id
        return next((nw for nw in self._nonworks if nw.nonwork_type_id == nonwork_type_id), None)

    @property
    def count(self) -> int:
        return len(self._nonworks) # Changed attribute name to lowercase

    def __len__(self) -> int:
        return len(self._nonworks) # Changed attribute name to lowercase

    def __iter__(self) -> Iterator[NonWork]: # Corrected return type
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> NonWork:
        if self.index < len(self._nonworks): # Changed attribute name to lowercase
            result = self._nonworks[self.index] # Changed attribute name to lowercase
            self.index += 1
            return result
        else:
            raise StopIteration
