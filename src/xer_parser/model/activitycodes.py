from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.activitycode import ActivityCode

__all__ = ["ActivityCodes"]


class ActivityCodes:
    _activitycodes: List[ActivityCode]

    def __init__(self) -> None:
        self.index: int = 0
        self._activitycodes: List[ActivityCode] = []
        # self.data_context: Optional[Any] = None # Placeholder if a main data context is needed

    def add(self, params: Dict[str, Any]) -> None:
        activity_code_instance = ActivityCode.model_validate(params)
        # if self.data_context: # If a central data object is used for relations
        #     activity_code_instance.data = self.data_context
        self._activitycodes.append(activity_code_instance)

    def count(self) -> int:
        return len(self._activitycodes)

    def get_tsv(self) -> list:
        if not self._activitycodes:
            return []
            
        tsv_data = [["%T", "ACTVCODE"]]
        header = [
            "%F",
            "actv_code_id",
            "parent_actv_code_id",
            "actv_code_type_id",
            "actv_code_name",
            "short_name",
            "seq_num",
            "color",
            "total_assignments",
        ]
        tsv_data.append(header)
        for code in self._activitycodes:
            tsv_data.append(code.get_tsv())
        return tsv_data

    def find_by_id(self, code_id: int) -> Optional[ActivityCode]:
        for code in self._activitycodes:
            if code.actv_code_id == code_id:
                return code
        return None

    def find_by_type_id(self, type_id: int) -> List[ActivityCode]:
        return [code for code in self._activitycodes if code.actv_code_type_id == type_id]

    def __len__(self) -> int:
        return len(self._activitycodes)

    def __iter__(self) -> Iterator[ActivityCode]:
        self.index = 0 # Reset index for each new iteration
        return self

    def __next__(self) -> ActivityCode:
        if self.index < len(self._activitycodes):
            result = self._activitycodes[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
