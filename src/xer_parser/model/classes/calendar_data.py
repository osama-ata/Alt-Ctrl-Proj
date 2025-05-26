import datetime
import re
from typing import Optional, Any, List, Dict
from pydantic import BaseModel, Field, model_validator


class CalendarData(BaseModel):
    text: str  # The raw calendar data string from XER
    
    # Parsed components - will be populated in model_post_init
    # Using specific types for better clarity
    parsed_data_map: Dict[str, str] = Field(default_factory=dict)
    working_days_map: Dict[str, bool] = Field(default_factory=dict)
    exception_dates: List[datetime.datetime] = Field(default_factory=list)
    work_pattern_detail: List[Dict[str, Any]] = Field(default_factory=list)

    # Exclude Pydantic's own 'data' if not used, or rename if it conflicts with XER's 'data' field.
    # For this class, we are defining specific parsed fields, so a generic 'data' field is not the primary focus.

    def _parse_internal_data_map(self) -> Dict[str, str]:
        """Helper to parse the initial key-value map from the text."""
        parsed_map = {}
        cal2 = []
        # Regex to find patterns like (d||n() where d is digit, n is number
        cal_matches = re.findall("\\((\\d+)\\|\\|(\\d+)\\(\\)\\)", self.text)
        for match in cal_matches:
            # match[0] is the first digit, match[1] is the number part like '1', '2', etc.
             cal2.append(match[1]) # Store the 'key' part, e.g. '1', '2'

        # Regex to split the text by these patterns. Using a lookbehind/lookahead might be more robust
        # or split by the full pattern match. The original split might be problematic.
        # For simplicity, using the original split logic structure
        # This regex needs to match the full pattern used for splitting.
        val_parts = re.split("\\(\\d\\|\\|\\d+\\(\\)\\)", self.text.strip())
        
        # The first part of val_parts (val_parts[0]) is usually empty or irrelevant before the first pattern.
        # The subsequent parts (val_parts[1:]) correspond to the values for keys in cal2.
        for i, key_from_cal2 in enumerate(cal2):
            if (i + 1) < len(val_parts): # Ensure there's a corresponding value part
                parsed_map[key_from_cal2] = val_parts[i + 1]
            # else:
                # Handle cases where a key might not have a corresponding value part if the split logic is imperfect
                # parsed_map[key_from_cal2] = "" # Or some default
        return parsed_map

    def _xldate_to_datetime(self, xldate: int) -> datetime.datetime:
        temp = datetime.datetime(1899, 12, 30)
        delta = datetime.timedelta(days=xldate)
        return temp + delta

    def _parse_work_pattern(self) -> List[Dict[str, Any]]:
        pattern = r"\(\d\|\|\d\(\)\(" # Matches (0||2()( , (1||3()( etc.
        day_name_map = {
            2: "Monday", 3: "Tuesday", 4: "Wednesday", 5: "Thursday",
            6: "Friday", 7: "Saturday", 1: "Sunday",
        }
        
        # Attempt to isolate the part of the text containing work patterns
        # Original split: tx = self.text.split("(0||VIEW(ShowTotal|Y)())")
        # This assumes "(0||VIEW(ShowTotal|Y)())" is a reliable delimiter
        parts = self.text.split("(0||VIEW(ShowTotal|Y)())", 1)
        work_pattern_text = parts[0] if parts else self.text

        days_data_segments = re.split(pattern, work_pattern_text)
        day_of_week_indicators = re.findall(pattern, work_pattern_text)
        
        parsed_work_pattern = []
        # days_data_segments[0] is the part before the first pattern, usually not a day's data
        for i, segment in enumerate(days_data_segments[1:]):
            if i < len(day_of_week_indicators):
                indicator = day_of_week_indicators[i]
                # Extract day of week number: e.g., from "(0||2()(" -> 2
                dow_match = re.search(r"\|\|(\d)\(\)\(", indicator)
                if not dow_match:
                    continue 
                dow = int(dow_match.group(1))

                starts = re.findall(r"s\|(\d{2}:\d{2})", segment)
                finishes = re.findall(r"f\|(\d{2}:\d{2})", segment)

                day_detail = {"DayOfWeek": day_name_map.get(dow, "Unknown"), "WorkTimes": []}
                for s_time_str, f_time_str in zip(starts, finishes):
                    try:
                        s_time = datetime.datetime.strptime(s_time_str, "%H:%M").time()
                        f_time = datetime.datetime.strptime(f_time_str, "%H:%M").time()
                        day_detail["WorkTimes"].append({"Start": s_time, "Finish": f_time})
                    except ValueError:
                        # Handle or log malformed time strings
                        pass 
                parsed_work_pattern.append(day_detail)
        return parsed_work_pattern

    def _parse_exceptions(self) -> List[datetime.datetime]:
        # Regex to find sequences of 5 or more digits, assumed to be Excel dates
        excep_date_numbers = re.findall(r"\d{5,}", self.text)
        exceptions_list = []
        for date_num_str in excep_date_numbers:
            try:
                date_num = int(date_num_str)
                exceptions_list.append(self._xldate_to_datetime(date_num))
            except ValueError:
                # Handle or log if a found number isn't a valid int
                pass
        return exceptions_list

    def _parse_working_days_map(self) -> Dict[str, bool]:
        # This method depends on self.parsed_data_map being populated
        if not self.parsed_data_map: # Ensure _parse_internal_data_map ran first
             # This condition might be problematic if model_post_init order is not guaranteed
             # or if _parse_internal_data_map itself relies on something not yet set.
             # For now, assume it's available or this method is called after its population.
             # A better approach might be to pass parsed_data_map as an argument if called from model_post_init.
             temp_parsed_map = self._parse_internal_data_map() # Fallback if not set, but be cautious
        else:
             temp_parsed_map = self.parsed_data_map

        days_map = {}
        # The original logic for get_days relied on self.data (now parsed_data_map)
        # and another regex on self.text. This seems complex.
        # Re-evaluating the original get_days:
        # first = re.findall("\\(\\d\\|\\|\\d\\(\\)(.*?)\\)\\)", self.text)
        # This regex seems to be extracting content for each day.
        # Example: (1||1()Day1Content)) (1||2()Day2Content))
        # Let's try to simplify or make it more robust if possible.
        # The keys '1', '2' for days_map seem to come from iteration index, not from parsed_data_map keys directly.
        
        # Simplified interpretation: iterate through expected day keys '1' through '7' (for days of month patterns)
        # This is a guess based on typical calendar structures. The original regex is more general.
        # For now, sticking to a direct adaptation of the original regex from get_days:
        day_content_matches = re.findall(r"\(\d\|\|\d\(\)(.*?)\)\)", self.text)
        for i, content in enumerate(day_content_matches):
            # Original: x = x.replace("(", "").replace(")", "").replace(" ", "").strip()
            # Original: days[str(i + 1)] = len(x) > 0 if len(x) > 1 else False
            # This logic is a bit opaque, "len(x) > 1" for True.
            # Assuming non-empty relevant content means it's a working day variant.
            cleaned_content = content.replace("(", "").replace(")", "").replace(" ", "").strip()
            days_map[str(i + 1)] = bool(cleaned_content) # Simplified: any content means true. Original was len(cleaned_content) > 1
        return days_map

    def model_post_init(self, __context: Any) -> None:
        """Populate parsed fields after model initialization."""
        super().model_post_init(__context)
        self.parsed_data_map = self._parse_internal_data_map()
        self.working_days_map = self._parse_working_days_map() # Depends on parsed_data_map
        self.exception_dates = self._parse_exceptions()
        self.work_pattern_detail = self._parse_work_pattern()

    def __repr__(self) -> str:
        return f"<CalendarData text='{self.text[:50]}...' " \
               f"parsed_days={len(self.working_days_map)} " \
               f"exceptions={len(self.exception_dates)} " \
               f"patterns={len(self.work_pattern_detail)}>"
