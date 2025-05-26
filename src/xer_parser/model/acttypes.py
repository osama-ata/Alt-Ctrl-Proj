from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.acttype import ActType

__all__ = ["ActTypes"]


class ActTypes:
    _activitytypes: List[ActType]

    def __init__(self) -> None:
        self.index: int = 0
        self._activitytypes: List[ActType] = []
        # self.data_context: Optional[Any] = None # Main Data object if needed for relations in ActType

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds an ActType to the collection.
        The params dictionary is validated into an ActType Pydantic model.
        """
        acttype_instance = ActType.model_validate(params)
        # if self.data_context: # If ActType instances need a reference to the main Data object
        #     acttype_instance.data = self.data_context
        self._activitytypes.append(acttype_instance)

    def find_by_id(self, type_id: int) -> Optional[ActType]:
        """Finds an activity code type by its actv_code_type_id."""
        for act_type in self._activitytypes:
            if act_type.actv_code_type_id == type_id:
                return act_type
        return None

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._activitytypes:
            return []
            
        tsv_data: list[list[str]] = [["%T", "ACTVTYPE"]]
        header = [
            "%F",
            "actv_code_type_id",
            "actv_short_len",
            "seq_num",
            "actv_code_type",
            "proj_id",
            "wbs_id",
            "actv_code_type_scope",
        ]
        tsv_data.append(header)
        for acttyp in self._activitytypes:
            tsv_data.append(acttyp.get_tsv())
        return tsv_data

    def count(self) -> int:
        return len(self._activitytypes)

    def __len__(self) -> int:
        return len(self._activitytypes)

    def __iter__(self) -> Iterator[ActType]:
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> ActType:
        if self.index < len(self._activitytypes):
            result = self._activitytypes[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
