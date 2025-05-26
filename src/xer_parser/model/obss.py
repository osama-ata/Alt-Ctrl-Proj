from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.obs import OBS

__all__ = ["OBSs"]


class OBSs:
    _obss: List[OBS]

    def __init__(self, data_context: Optional[Any] = None) -> None:
        self.index: int = 0
        self._obss: List[OBS] = []
        self.data_context: Optional[Any] = data_context

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds an OBS to the collection.
        The params dictionary is validated into an OBS Pydantic model.
        """
        obs_instance = OBS.model_validate(params)
        if self.data_context: # Pass the main Data object to the instance if available and needed
            obs_instance.data = self.data_context
        self._obss.append(obs_instance)

    def find_by_id(self, obs_id: int) -> Optional[OBS]: # Corrected parameter name and return type
        """Finds an OBS entry by its obs_id."""
        return next((obs for obs in self._obss if obs.obs_id == obs_id), None)

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._obss:
            return []
            
        tsv_data: list[list[str]] = [["%T", "OBS"]]
        header = [
            "%F",
            "obs_id", "parent_obs_id", "guid", "seq_num", "obs_name", "obs_descr",
        ]
        tsv_data.append(header)
        for obs_item in self._obss:
            tsv_data.append(obs_item.get_tsv())
        return tsv_data

    @property
    def count(self) -> int:
        return len(self._obss)

    def __len__(self) -> int:
        return len(self._obss)

    def __iter__(self) -> Iterator[OBS]: # Corrected return type
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> OBS:
        if self.index < len(self._obss):
            result = self._obss[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
