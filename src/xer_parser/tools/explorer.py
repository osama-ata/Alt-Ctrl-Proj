"""
XER Explorer utility for PyP6Xer.

This module provides functionality to explore and summarize XER files,
giving a concise overview of the file contents.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Any, TextIO, List # Added List for type hinting

from xer_parser.reader import Reader
# Import Pydantic models for type checking if needed, or for explicit attribute access understanding
# from xer_parser.model.classes.project import Project
# from xer_parser.model.classes.calendar import Calendar
# from xer_parser.model.classes.wbs import WBS
# from xer_parser.model.classes.rsrc import Resource
# from xer_parser.model.classes.task import Task
# from xer_parser.model.classes.taskpred import TaskPred


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XerExplorer:
    """Class for exploring and summarizing XER files."""

    def __init__(self, xer_path: str):
        """
        Initialize the XER Explorer with a path to an XER file.

        Args:
            xer_path (str): Path to the XER file to explore
        """
        self.xer_path = xer_path
        self.reader: Optional[Reader] = None # Type hint Reader
        self.collection_data: dict[str, list[Any]] = {}

    def parse_file(self) -> bool:
        """
        Parse the XER file using the Reader class.
        The Reader now populates its internal self._data (Pydantic Data model).
        """
        try:
            self.reader = Reader(self.xer_path)
            return True
        except Exception as e:
            logger.error(f"Error parsing XER file: {e!s}")
            return False

    def collect_data(self) -> dict[str, list[Any]]:
        """
        Collect data from all relevant collections via the Reader's properties.
        """
        if not self.reader:
            if not self.parse_file():
                return {}

        # Updated list of potential collections based on Reader properties
        potential_collections = [
            "projects", "wbss", "activities", "relations", "calendars", "resources",
            "accounts", "activitycodes", "actvcodes", "acttypes", "currencies",
            "fintmpls", "nonworks", "obss", "pcattypes", "pcatvals", "projpcats",
            "rcattypes", "rcatvals", "rolerates", "roles", "resourcecurves",
            "resourcerates", "resourcecategories", "scheduleoptions", "activityresources",
            "taskprocs", "udftypes", "udfvalues"
            # Note: 'relations' maps to 'predecessors' in Reader._data
            # 'activities' maps to 'tasks' in Reader._data
        ]
        
        # Correct mapping from explorer terms to Reader property names
        collection_map = {
            "activities": "activities", # reader.activities -> reader._data.tasks
            "relations": "relations",   # reader.relations -> reader._data.predecessors
            # Add other mappings if explorer uses different names than Reader properties
        }


        for name in potential_collections:
            explorer_name = name # Name used in explorer's collection_data and reports
            reader_attr_name = collection_map.get(name, name) # Get actual reader property name

            if hasattr(self.reader, reader_attr_name):
                try:
                    # Reader properties now directly return the collection objects which are iterable
                    collection_instance = getattr(self.reader, reader_attr_name)
                    # The items in these collections are Pydantic models
                    self.collection_data[explorer_name] = list(collection_instance) 
                except Exception as e:
                    logger.warning(f"Could not collect data for '{explorer_name}': {e}")
                    self.collection_data[explorer_name] = []
            else:
                logger.warning(f"Reader does not have attribute '{reader_attr_name}' for explorer collection '{explorer_name}'")
                self.collection_data[explorer_name] = []
        
        # Specific handling for 'task_predecessors' if it was meant to be 'relations'
        if "task_predecessors" in self.collection_data and not self.collection_data["task_predecessors"]:
            if "relations" in self.collection_data:
                 self.collection_data["task_predecessors"] = self.collection_data["relations"]


        return self.collection_data

    def generate_report(
        self,
        output_file: str,
        skip_large_collections: bool = True,
        large_threshold: int = 1000,
    ) -> bool:
        if not self.reader and not self.parse_file(): # Ensures reader and self.reader._data are populated
            return False

        if not self.collection_data: # Ensure data is collected
            self.collect_data()

        with open(output_file, "w", encoding='utf-8') as f: # Added encoding
            f.write("PyP6Xer Exploration Results\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"XER File: {os.path.basename(self.xer_path)}\n")
            f.write("=" * 80 + "\n\n")

            f.write("FILE STATISTICS\n")
            f.write("=" * 80 + "\n")
            f.write("Collections found in this XER file:\n")
            large_collections = []

            for name, data_list in self.collection_data.items():
                count = len(data_list)
                f.write(f"  {name}: {count} items\n")
                if skip_large_collections and count > large_threshold:
                    large_collections.append((name, count))
            
            if skip_large_collections and large_collections:
                f.write("\nSkipping detailed exploration of large collections:\n")
                for name, count in large_collections:
                    f.write(f"  - {name} (too large - {count} items)\n")
            f.write("\n" + "-" * 80 + "\n\n")

            self._write_project_summary(f)
            f.write("-" * 80 + "\n\n")
            self._write_calendar_summary(f)
            f.write("\n" + "-" * 80 + "\n\n")
            self._write_wbs_summary(f)
            f.write("\n" + "-" * 80 + "\n\n")
            self._write_resource_summary(f)
            f.write("\n" + "-" * 80 + "\n\n")

            if not (skip_large_collections and "activities" in self.collection_data and len(self.collection_data["activities"]) > large_threshold):
                self._write_activity_summary(f)
                f.write("\n" + "-" * 80 + "\n\n")
            
            # Ensure 'relations' is used for the check, matching the reader's property name
            relations_key = "relations" if "relations" in self.collection_data else "task_predecessors"
            if not (skip_large_collections and relations_key in self.collection_data and len(self.collection_data[relations_key]) > large_threshold):
                self._write_relationship_summary(f) # This method uses self.collection_data["relations"] or "task_predecessors"
                f.write("\n" + "-" * 80 + "\n\n")

            f.write("EXPLORATION SUMMARY\n")
            f.write("=" * 80 + "\n")
            f.write("The XER file has been successfully explored.\n")
            f.write("This report provides a high-level overview of the key elements in the file.\n")
            if skip_large_collections and large_collections:
                f.write("Large collections were skipped for brevity.\n")
            f.write("To explore the data in more detail, you can use the PyP6Xer library in your own code.\n")
        return True

    def _format_value(self, value: Any, is_date: bool = False) -> str:
        if value is None:
            return "N/A"
        if is_date and isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return str(value)

    def _write_project_summary(self, file_obj: TextIO) -> None:
        file_obj.write("1. PROJECT SUMMARY\n")
        file_obj.write("=" * 80 + "\n")
        projects = self.collection_data.get("projects")
        if projects:
            file_obj.write(f"Found {len(projects)} project(s)\n\n")
            for i, project in enumerate(projects, 1): # project is now a Pydantic model
                file_obj.write(f"Project #{i}:\n")
                key_attrs = [
                    "proj_id", "proj_short_name", "proj_name", "clndr_id",
                    "status_code", "update_date", # Using update_date instead of lastupdate
                    "plan_start_date", "plan_end_date", 
                    "scd_end_date", "add_date", "last_recalc_date", "fcst_start_date"
                ]
                for attr in key_attrs:
                    value = getattr(project, attr, None)
                    is_date = "date" in attr 
                    file_obj.write(f"  {attr}: {self._format_value(value, is_date)}\n")
                file_obj.write("\n")
        else:
            file_obj.write("No projects found in this XER file.\n\n")

    def _write_calendar_summary(self, file_obj: TextIO) -> None:
        file_obj.write("2. CALENDAR SUMMARY\n")
        file_obj.write("=" * 80 + "\n")
        calendars = self.collection_data.get("calendars")
        if calendars:
            file_obj.write(f"Total calendars: {len(calendars)}\n\n")
            if calendars:
                file_obj.write("Calendar listing:\n")
                for i, calendar in enumerate(calendars, 1): # calendar is Pydantic model
                    cal_id = self._format_value(calendar.clndr_id)
                    cal_name = self._format_value(calendar.clndr_name)
                    file_obj.write(f"  {i}. ID: {cal_id}, Name: {cal_name}\n")
        else:
            file_obj.write("No calendars found in this XER file.\n")

    def _write_wbs_summary(self, file_obj: TextIO) -> None:
        file_obj.write("3. WBS SUMMARY\n")
        file_obj.write("=" * 80 + "\n")
        wbss_list = self.collection_data.get("wbss")
        if wbss_list:
            file_obj.write(f"Total WBS elements: {len(wbss_list)}\n\n")
            if wbss_list:
                max_display = 10
                file_obj.write(f"Sample WBS elements (showing first {max_display}):\n")
                for i, wbs in enumerate(wbss_list[:max_display], 1): # wbs is Pydantic model
                    wbs_id = self._format_value(wbs.wbs_id)
                    wbs_name = self._format_value(wbs.wbs_name)
                    file_obj.write(f"  {i}. ID: {wbs_id}, Name: {wbs_name}\n")
                if len(wbss_list) > max_display:
                    file_obj.write(f"  ... and {len(wbss_list) - max_display} more\n")
        else:
            file_obj.write("No WBS elements found in this XER file.\n")

    def _write_resource_summary(self, file_obj: TextIO) -> None:
        file_obj.write("4. RESOURCES SUMMARY\n")
        file_obj.write("=" * 80 + "\n")
        resources_list = self.collection_data.get("resources")
        if resources_list:
            file_obj.write(f"Total resources: {len(resources_list)}\n\n")
            if resources_list:
                file_obj.write("Resources listing (sample):\n")
                for i, resource in enumerate(resources_list[:10], 1): # resource is Pydantic model
                    rsrc_id = self._format_value(resource.rsrc_id)
                    rsrc_name = self._format_value(resource.rsrc_name)
                    file_obj.write(f"  {i}. ID: {rsrc_id}, Name: {rsrc_name}\n")
                    for attr in ["rsrc_short_name", "rsrc_type", "parent_rsrc_id"]:
                        value = getattr(resource, attr, None)
                        if value is not None:
                            file_obj.write(f"     {attr}: {self._format_value(value)}\n")
                    file_obj.write("\n")
                if len(resources_list) > 10:
                     file_obj.write(f"  ... and {len(resources_list) - 10} more\n")
        else:
            file_obj.write("No resources found in this XER file.\n")

    def _write_activity_summary(self, file_obj: TextIO) -> None:
        file_obj.write("5. ACTIVITY SUMMARY\n")
        file_obj.write("=" * 80 + "\n")
        activities_list = self.collection_data.get("activities")
        if activities_list:
            file_obj.write(f"Total activities: {len(activities_list)}\n\n")
            if activities_list:
                max_display = 5
                file_obj.write(f"Sample activities (showing first {max_display}):\n")
                for i, activity in enumerate(activities_list[:max_display], 1): # activity is Pydantic model
                    task_code = self._format_value(activity.task_code)
                    task_name = self._format_value(activity.task_name)
                    file_obj.write(f"  {i}. Code: {task_code}, Name: {task_name}\n")
                if len(activities_list) > max_display:
                    file_obj.write(f"  ... and {len(activities_list) - max_display} more\n")
        else:
            file_obj.write("No activities found in this XER file.\n")

    def _write_relationship_summary(self, file_obj: TextIO) -> None:
        file_obj.write("6. RELATIONSHIP SUMMARY\n")
        file_obj.write("=" * 80 + "\n")
        # Use 'relations' if available, otherwise fallback to 'task_predecessors'
        relations_key = "relations" if "relations" in self.collection_data else "task_predecessors"
        relations_list = self.collection_data.get(relations_key)

        if relations_list:
            file_obj.write(f"Total relationships: {len(relations_list)}\n\n")
            if relations_list:
                max_display = 5
                file_obj.write(f"Sample relationships (showing first {max_display}):\n")
                for i, relation in enumerate(relations_list[:max_display], 1): # relation is Pydantic model
                    pred_task = self._format_value(relation.pred_task_id)
                    succ_task = self._format_value(relation.task_id)
                    rel_type = self._format_value(relation.pred_type)
                    lag = self._format_value(relation.lag_hr_cnt)
                    file_obj.write(f"  {i}. Pred: {pred_task}, Succ: {succ_task}, Type: {rel_type}, Lag: {lag}h\n")
                if len(relations_list) > max_display:
                    file_obj.write(f"  ... and {len(relations_list) - max_display} more\n")
        else:
            file_obj.write("No relationships found in this XER file.\n")


def explore_xer_file(
    xer_path: str,
    output_file: str,
    skip_large: bool = True,
    large_threshold: int = 1000,
) -> bool:
    explorer = XerExplorer(xer_path)
    # parse_file() is called by collect_data() if reader is not initialized
    explorer.collect_data() # This will also parse the file if not already done
    if not explorer.reader: # Check if parsing was successful
        return False
    return explorer.generate_report(output_file, skip_large, large_threshold)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Explore and summarize XER files")
    parser.add_argument("xer_file", help="Path to the XER file to explore")
    parser.add_argument(
        "-o",
        "--output",
        default="xer_exploration.txt",
        help="Path to the output file (default: xer_exploration.txt)",
    )
    parser.add_argument(
        "--include-large",
        action="store_true",
        help="Include detailed exploration of large collections",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=1000,
        help="Threshold for what is considered a large collection (default: 1000)",
    )

    args = parser.parse_args()

    logger.info(f"Exploring XER file: {args.xer_file}")
    success = explore_xer_file(
        args.xer_file, args.output, not args.include_large, args.threshold
    )

    if success:
        logger.info(f"Exploration complete! Results saved to {args.output}")
    else:
        logger.error("Exploration failed!")
        sys.exit(1)


# Command-line interface
if __name__ == "__main__":
    main()
