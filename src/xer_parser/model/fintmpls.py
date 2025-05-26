from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.fintmpl import FinTmpl

__all__ = ["FinTmpls"]


class FinTmpls:
    _fintmpls: List[FinTmpl] # Corrected attribute name casing for consistency

    def __init__(self, data_context: Optional[Any] = None) -> None:
        self.index: int = 0
        self._fintmpls: List[FinTmpl] = [] # Corrected attribute name casing
        self.data_context: Optional[Any] = data_context

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds a FinTmpl to the collection.
        The params dictionary is validated into a FinTmpl Pydantic model.
        """
        fintmpl_instance = FinTmpl.model_validate(params)
        if self.data_context: # Though FinTmpl may not use it now, good for consistency
            fintmpl_instance.data = self.data_context
        self._fintmpls.append(fintmpl_instance) # Corrected attribute name casing

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._fintmpls: # Corrected attribute name casing
            return []
            
        tsv_data: list[list[str]] = [["%T", "FINTMPL"]]
        header = ["%F", "fintmpl_id", "fintmpl_name", "default_flag"]
        tsv_data.append(header)
        for fin_tmpl in self._fintmpls: # Corrected attribute name casing
            tsv_data.append(fin_tmpl.get_tsv())
        return tsv_data

    def find_by_id(self, fintmpl_id: int) -> Optional[FinTmpl]:
        """Finds a financial template by its fintmpl_id."""
        return next((ft for ft in self._fintmpls if ft.fintmpl_id == fintmpl_id), None) # Corrected attribute name casing

    @property
    def count(self) -> int:
        return len(self._fintmpls) # Corrected attribute name casing

    def __len__(self) -> int:
        return len(self._fintmpls) # Corrected attribute name casing

    def __iter__(self) -> Iterator[FinTmpl]:
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> FinTmpl:
        if self.index < len(self._fintmpls): # Corrected attribute name casing
            result = self._fintmpls[self.index] # Corrected attribute name casing
            self.index += 1
            return result
        else:
            raise StopIteration
