from typing import List, Iterator, Any, Dict, Optional
from ..model.classes.calendar import Calendar

__all__ = ["Calendars"]


class Calendars:
    _calendars: List[Calendar]

    def __init__(self, data_context: Optional[Any] = None) -> None:
        self.index: int = 0
        self._calendars: List[Calendar] = []
        self.data_context: Optional[Any] = data_context # Store if needed for Calendar instances

    def add(self, params: Dict[str, Any]) -> None:
        """
        Adds a Calendar to the collection.
        The params dictionary is validated into a Calendar Pydantic model.
        """
        calendar_instance = Calendar.model_validate(params)
        if self.data_context: # Pass the main Data object to the instance if available and needed
            calendar_instance.data = self.data_context
        self._calendars.append(calendar_instance)

    def get_tsv(self) -> list: # Return type changed to list for consistency
        if not self._calendars:
            return []
            
        tsv_data: list[list[str]] = [["%T", "CALENDAR"]]
        header = [
            "%F",
            "clndr_id", "default_flag", "clndr_name", "proj_id", "base_clndr_id",
            "last_chng_date", "clndr_type", "day_hr_cnt", "week_hr_cnt", 
            "month_hr_cnt", "year_hr_cnt", "rsrc_private", "clndr_data",
        ]
        tsv_data.append(header)
        for cal in self._calendars:
            tsv_data.append(cal.get_tsv())
        return tsv_data

    def find_by_id(self, clndr_id: int) -> Optional[Calendar]:
        """Finds a calendar by its clndr_id."""
        return next((cal for cal in self._calendars if cal.clndr_id == clndr_id), None)

    def count(self) -> int:
        return len(self._calendars)

    def __len__(self) -> int:
        return len(self._calendars)

    def __iter__(self) -> Iterator[Calendar]:
        self.index = 0  # Reset index for each new iteration
        return self

    def __next__(self) -> Calendar:
        if self.index < len(self._calendars):
            result = self._calendars[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
