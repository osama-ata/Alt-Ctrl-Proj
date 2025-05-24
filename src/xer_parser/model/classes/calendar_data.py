import datetime
import re
from typing import ClassVar


class CalendarData:
    working_days: ClassVar[dict] = {}
    exceptions: ClassVar[list] = []

    def __init__(self, text):
        self.text = text
        cal2 = []
        cal = re.findall("\\(\\d\\|\\|\\d+\\(\\)", text)
        for c in cal:
            c2 = c.split("||")[1]
            cal2.append(c2.split("()")[0])
        val = re.split("\\(\\d\\|\\|\\d+\\(\\)", text.strip())

        self.data = {}
        for i, c in enumerate(cal2):
            self.data[c] = val[i + 1] if i >= 1 else ""

        self.exceptions = self.get_exceptions()
        self.working_days = self.get_days()

    def xldate_to_datetime(self, xldate):
        temp = datetime.datetime(1899, 12, 30)
        delta = datetime.timedelta(days=xldate)
        return temp + delta

    def get_work_pattern(self):
        pattern = r"\(\d\|\|\d\(\)\("
        day_name = {
            2: "Monday",
            3: "Tuesday",
            4: "Wednesday",
            5: "Thursday",
            6: "Friday",
            7: "Saturday",
            1: "Sunday",
        }
        tx = self.text.split("(0||VIEW(ShowTotal|Y)())")
        days = re.split(pattern, tx[0])
        dys = re.findall(pattern, self.text)
        lst_dow = []
        for day, d in zip(days[1:], dys, strict=True):
            dow = int(d.replace("(0||", "").replace(")", "").replace("(", ""))
            starts = re.findall("s\\|\\d\\d\\:\\d\\d", day)
            finishes = re.findall("f\\|\\d\\d\\:\\d\\d", day)

            day_dict = {"DayOfWeek": day_name[dow], "WorkTimes": [], "ifc": None}
            for s, f in zip(starts, finishes, strict=True):
                s_c = datetime.datetime.strptime(s.replace("s|", ""), "%H:%M").time()
                f_c = datetime.datetime.strptime(f.replace("f|", ""), "%H:%M").time()
                day_dict["WorkTimes"].append({"Start": s_c, "Finish": f_c})
            lst_dow.append(day_dict)
        return lst_dow

    def get_exceptions(self):
        base_datetime = datetime.datetime(1899, 12, 30)
        excep_dates = re.findall(r"\d{5,}", self.text)
        exceptions = []
        for exc in excep_dates:
            exc = int(exc)
            delta = datetime.timedelta(exc)
            exc_date = base_datetime + delta
            exceptions.append(exc_date)
        return exceptions

    def get_days(self):
        if not self.data:
            return None
        first = re.findall("\\(\\d\\|\\|\\d\\(\\)(.*?)\\)\\)", self.text)
        days = {}
        for i, x in enumerate(first):
            x = x.replace("(", "").replace(")", "").replace(" ", "").strip()
            days[str(i + 1)] = len(x) > 0 if len(x) > 1 else False
        self.working_days = days
        return self.working_days
