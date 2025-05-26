from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.pcattype import PCatType # Corrected relative import

__all__ = ["PCatTypes"]


class PCatTypes:
    _pcattypes: List[PCatType]

    def __init__(self, data_context: Optional[Any] = None) -> None:
        self.index: int = 0
        self._pcattypes: List[PCatType] = []
        self.data_context: Optional[Any] = data_context # Store if needed for PCatType instances

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds a PCatType to the collection.
        The params dictionary is validated into a PCatType Pydantic model.
        """
        pcat_type_instance = PCatType.model_validate(params)
        if self.data_context: # Though PCatType may not use it now, good for consistency
            pcat_type_instance.data = self.data_context
        self._pcattypes.append(pcat_type_instance)

    def find_by_id(self, proj_catg_type_id: int) -> Optional[PCatType]: # Corrected parameter name and return type
        """Finds a project category type by its proj_catg_type_id."""
        return next((ptype for ptype in self._pcattypes if ptype.proj_catg_type_id == proj_catg_type_id), None)

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._pcattypes:
            return []
            
        tsv_data: list[list[str | int | None]] = [["%T", "PCATTYPE"]] # Type hint for tsv_data
        header = [
            "%F",
            "proj_catg_type_id", "seq_num", "proj_catg_short_len", 
            "proj_catg_type", "export_flag",
        ]
        tsv_data.append(header)
        for pcat_type in self._pcattypes:
            tsv_data.append(pcat_type.get_tsv())
        return tsv_data

    def count(self) -> int:
        return len(self._pcattypes)

    def __len__(self) -> int:
        return len(self._pcattypes)

    def __iter__(self) -> Iterator[PCatType]: # Corrected return type
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> PCatType:
        if self.index < len(self._pcattypes):
            result = self._pcattypes[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
