from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.projcat import ProjCat

__all__ = ["ProjCats"]


class ProjCats:
    _projcats: List[ProjCat] # Renamed for convention

    def __init__(self, data_context: Optional[Any] = None) -> None:
        self.index: int = 0
        self._projcats: List[ProjCat] = [] # Renamed for convention
        self.data_context: Optional[Any] = data_context

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds a ProjCat to the collection.
        The params dictionary is validated into a ProjCat Pydantic model.
        """
        projcat_instance = ProjCat.model_validate(params)
        if self.data_context: # Pass the main Data object to the instance if available and needed
            projcat_instance.data = self.data_context
        self._projcats.append(projcat_instance) # Renamed for convention

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._projcats: # Renamed for convention
            return []
            
        tsv_data: list[list[str | int | None]] = [["%T", "PROJPCAT"]]
        header = ["%F", "proj_id", "proj_catg_type_id", "proj_catg_id"]
        tsv_data.append(header)
        for projcat_item in self._projcats: # Renamed for convention
            tsv_data.append(projcat_item.get_tsv())
        return tsv_data

    def find_by_id(self, proj_id: int, proj_catg_id: int) -> Optional[ProjCat]:
        """Finds a project category assignment by its composite key."""
        # Assuming proj_id and proj_catg_id together form a key
        for projcat in self._projcats:
            if projcat.proj_id == proj_id and projcat.proj_catg_id == proj_catg_id:
                return projcat
        return None

    @property
    def count(self) -> int:
        return len(self._projcats) # Renamed for convention

    def __len__(self) -> int:
        return len(self._projcats) # Renamed for convention

    def __iter__(self) -> Iterator[ProjCat]: # Corrected return type
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> ProjCat:
        if self.index < len(self._projcats): # Renamed for convention
            result = self._projcats[self.index] # Renamed for convention
            self.index += 1
            return result
        else:
            raise StopIteration
