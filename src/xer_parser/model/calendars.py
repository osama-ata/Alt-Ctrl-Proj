from typing import Any

from xer_parser.model.classes.calendar import Calendar

__all__ = ["Calendars"]


class Calendars:
    def __init__(self) -> None:
        self.index: int = 0
        self._calendars: list[Calendar] = []

    def add(self, params: Any) -> None:
        self._calendars.append(Calendar(params))

    def get_tsv(self) -> list[list[str]]:
        if len(self._calendars) > 0:
            tsv: list[list[str]] = []
            tsv.append(["%T", "CALENDAR"])
            tsv.append(
                [
                    "%F",
                    "clndr_id",
                    "default_flag",
                    "clndr_name",
                    "proj_id",
                    "base_clndr_id",
                    "last_chng_date",
                    "clndr_type",
                    "day_hr_cnt",
                    "week_hr_cnt",
                    "month_hr_cnt",
                    "year_hr_cnt",
                    "rsrc_private",
                    "clndr_data",
                ]
            )
            for cal in self._calendars:
                tsv.append(cal.get_tsv())
            return tsv
        return []

    def find_by_id(self, id: Any) -> Calendar | list[Calendar]:
        obj: list[Calendar] = list(filter(lambda x: x.clndr_id == id, self._calendars))
        if len(obj) > 0:
            return obj[0]
        return obj

    def count(self) -> int:
        return len(self._calendars)

    def __len__(self) -> int:
        return len(self._calendars)

    def __iter__(self) -> "Calendars":
        return self

    def __next__(self) -> Calendar:
        if self.index >= len(self._calendars):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._calendars[idx]
