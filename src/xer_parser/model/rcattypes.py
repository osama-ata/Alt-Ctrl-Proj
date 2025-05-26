from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.rcattype import RCatType

__all__ = ["RCatTypes"]


class RCatTypes:
    _rcattypes: List[RCatType]

    def __init__(self, data_context: Optional[Any] = None) -> None:
        self.index: int = 0
        self._rcattypes: List[RCatType] = []
        self.data_context: Optional[Any] = data_context

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds an RCatType to the collection.
        The params dictionary is validated into an RCatType Pydantic model.
        """
        rcattype_instance = RCatType.model_validate(params)
        if self.data_context: # Though RCatType may not use it now, good for consistency
            rcattype_instance.data = self.data_context
        self._rcattypes.append(rcattype_instance)

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._rcattypes:
            return []
            
        tsv_data: list[list[str | int | None]] = [["%T", "RCATTYPE"]]
        header = [
            "%F",
            "rsrc_catg_type_id", "seq_num", "rsrc_catg_short_len", "rsrc_catg_type",
        ]
        tsv_data.append(header)
        for rcat_type in self._rcattypes:
            tsv_data.append(rcat_type.get_tsv())
        return tsv_data

    def find_by_id(self, rsrc_catg_type_id: int) -> Optional[RCatType]: # Corrected parameter name and return type
        """Finds a resource category type by its rsrc_catg_type_id."""
        return next((rcat_type for rcat_type in self._rcattypes if rcat_type.rsrc_catg_type_id == rsrc_catg_type_id), None)

    @property
    def count(self) -> int:
        return len(self._rcattypes)

    def __len__(self) -> int:
        return len(self._rcattypes)

    def __iter__(self) -> Iterator[RCatType]: # Corrected return type
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> RCatType:
        if self.index < len(self._rcattypes):
            result = self._rcattypes[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
