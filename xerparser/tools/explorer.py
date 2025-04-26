"""
XER Explorer utility for PyP6Xer.

This module provides functionality to explore and summarize XER files,
giving a concise overview of the file contents.
"""

import os
import sys
from datetime import datetime

from xerparser.reader import Reader


class XerExplorer:
    """Class for exploring and summarizing XER files."""

    def __init__(self, xer_path):
        """
        Initialize the XER Explorer with a path to an XER file.

        Args:
            xer_path (str): Path to the XER file to explore
        """
        self.xer_path = xer_path
        self.reader = None
        self.collection_data = {}

    def parse_file(self):
        """
        Parse the XER file using the Reader class.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.reader = Reader(self.xer_path)
            return True
        except Exception as e:
            print(f"Error parsing XER file: {str(e)}")
            return False

    def collect_data(self):
        """
        Collect data from all collections in the XER file.

        Returns:
            dict: Dictionary of collection names and their data
        """
        if not self.reader:
            if not self.parse_file():
                return {}

        # List potential collections
        potential_collections = [
            "projects",
            "wbss",
            "activities",
            "relations",
            "calendars",
            "resources",
            "activitycodes",
            "task_predecessors",
        ]

        for name in potential_collections:
            if hasattr(self.reader, name):
                try:
                    collection_data = list(getattr(self.reader, name))
                    self.collection_data[name] = collection_data
                except Exception:
                    # Skip collections that can't be accessed
                    pass

        return self.collection_data

    def generate_report(
        self, output_file, skip_large_collections=True, large_threshold=1000
    ):
        """
        Generate a report of the XER file contents.

        Args:
            output_file (str): Path to the output file
            skip_large_collections (bool): Whether to skip detailed exploration of large collections
            large_threshold (int): Threshold for what is considered a large collection

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.reader and not self.parse_file():
            return False

        if not self.collection_data:
            self.collect_data()

        # Open the output file for writing
        with open(output_file, "w") as f:
            f.write(f"PyP6Xer Exploration Results\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"XER File: {os.path.basename(self.xer_path)}\n")
            f.write("=" * 80 + "\n\n")

            # Collection Statistics
            f.write("FILE STATISTICS\n")
            f.write("=" * 80 + "\n")

            f.write("Collections found in this XER file:\n")
            large_collections = []

            for name, data in self.collection_data.items():
                count = len(data)
                f.write(f"  {name}: {count} items\n")

                # Track large collections
                if skip_large_collections and count > large_threshold:
                    large_collections.append((name, count))

            if skip_large_collections and large_collections:
                f.write("\nSkipping detailed exploration of large collections:\n")
                for name, count in large_collections:
                    f.write(f"  - {name} (too large - {count} items)\n")

            f.write("\n" + "-" * 80 + "\n\n")

            # Project Summary
            self._write_project_summary(f)
            f.write("-" * 80 + "\n\n")

            # Calendar Summary
            self._write_calendar_summary(f)
            f.write("\n" + "-" * 80 + "\n\n")

            # WBS Summary
            self._write_wbs_summary(f)
            f.write("\n" + "-" * 80 + "\n\n")

            # Resources Summary
            self._write_resource_summary(f)
            f.write("\n" + "-" * 80 + "\n\n")

            # Activities Summary (if not skipped)
            if "activities" in self.collection_data and not (
                skip_large_collections
                and len(self.collection_data["activities"]) > large_threshold
            ):
                self._write_activity_summary(f)
                f.write("\n" + "-" * 80 + "\n\n")

            # Relationships Summary (if not skipped)
            if "relations" in self.collection_data and not (
                skip_large_collections
                and len(self.collection_data["relations"]) > large_threshold
            ):
                self._write_relationship_summary(f)
                f.write("\n" + "-" * 80 + "\n\n")

            # Report Summary
            f.write("EXPLORATION SUMMARY\n")
            f.write("=" * 80 + "\n")
            f.write("The XER file has been successfully explored.\n")
            f.write(
                "This report provides a high-level overview of the key elements in the file.\n"
            )
            if skip_large_collections and large_collections:
                f.write("Large collections were skipped for brevity.\n")
            f.write(
                "To explore the data in more detail, you can use the PyP6Xer library in your own code.\n"
            )

        return True

    def _write_project_summary(self, file_obj):
        """Write project summary to file."""
        file_obj.write("1. PROJECT SUMMARY\n")
        file_obj.write("=" * 80 + "\n")

        if "projects" in self.collection_data and self.collection_data["projects"]:
            projects = self.collection_data["projects"]
            file_obj.write(f"Found {len(projects)} project(s)\n\n")

            for i, project in enumerate(projects, 1):
                file_obj.write(f"Project #{i}:\n")

                # Key project attributes
                key_attrs = [
                    "proj_id",
                    "proj_short_name",
                    "proj_name",
                    "lastupdate",
                    "clndr_id",
                    "proj_start_date",
                    "proj_finish_date",
                    "plan_start_date",
                    "plan_end_date",
                    "status_code",
                ]

                for attr in key_attrs:
                    if hasattr(project, attr):
                        try:
                            value = getattr(project, attr)
                            file_obj.write(f"  {attr}: {value}\n")
                        except Exception:
                            file_obj.write(f"  {attr}: Unable to access\n")

                file_obj.write("\n")
        else:
            file_obj.write("No projects found in this XER file.\n\n")

    def _write_calendar_summary(self, file_obj):
        """Write calendar summary to file."""
        file_obj.write("2. CALENDAR SUMMARY\n")
        file_obj.write("=" * 80 + "\n")

        if "calendars" in self.collection_data and self.collection_data["calendars"]:
            calendars = self.collection_data["calendars"]
            file_obj.write(f"Total calendars: {len(calendars)}\n\n")

            if calendars:
                file_obj.write("Calendar listing:\n")
                for i, calendar in enumerate(calendars, 1):
                    try:
                        cal_id = getattr(calendar, "clndr_id", "N/A")
                        cal_name = getattr(calendar, "clndr_name", "N/A")
                        file_obj.write(f"  {i}. ID: {cal_id}, Name: {cal_name}\n")
                    except Exception:
                        file_obj.write(f"  {i}. Unable to access calendar details\n")
        else:
            file_obj.write("No calendars found in this XER file.\n")

    def _write_wbs_summary(self, file_obj):
        """Write WBS summary to file."""
        file_obj.write("3. WBS SUMMARY\n")
        file_obj.write("=" * 80 + "\n")

        if "wbss" in self.collection_data and self.collection_data["wbss"]:
            wbss_list = self.collection_data["wbss"]
            file_obj.write(f"Total WBS elements: {len(wbss_list)}\n\n")

            if wbss_list:
                # Sample of WBS elements
                max_display = 10
                file_obj.write(f"Sample WBS elements (showing first {max_display}):\n")
                for i, wbs in enumerate(wbss_list[:max_display], 1):
                    try:
                        wbs_id = getattr(wbs, "wbs_id", "N/A")
                        wbs_name = getattr(wbs, "wbs_name", "N/A")
                        file_obj.write(f"  {i}. ID: {wbs_id}, Name: {wbs_name}\n")
                    except Exception:
                        file_obj.write(f"  {i}. Unable to access WBS details\n")

                if len(wbss_list) > max_display:
                    file_obj.write(f"  ... and {len(wbss_list) - max_display} more\n")
        else:
            file_obj.write("No WBS elements found in this XER file.\n")

    def _write_resource_summary(self, file_obj):
        """Write resource summary to file."""
        file_obj.write("4. RESOURCES SUMMARY\n")
        file_obj.write("=" * 80 + "\n")

        if "resources" in self.collection_data and self.collection_data["resources"]:
            resources_list = self.collection_data["resources"]
            file_obj.write(f"Total resources: {len(resources_list)}\n\n")

            if resources_list:
                file_obj.write("Resources listing:\n")
                for i, resource in enumerate(resources_list, 1):
                    try:
                        rsrc_id = getattr(resource, "rsrc_id", "N/A")
                        rsrc_name = getattr(resource, "rsrc_name", "N/A")
                        file_obj.write(f"  {i}. ID: {rsrc_id}, Name: {rsrc_name}\n")

                        # Add more resource details if available
                        for attr in ["rsrc_short_name", "rsrc_type", "parent_rsrc_id"]:
                            if hasattr(resource, attr):
                                value = getattr(resource, attr)
                                if value:  # Only print if there's a value
                                    file_obj.write(f"     {attr}: {value}\n")

                        file_obj.write("\n")
                    except Exception:
                        file_obj.write(f"  {i}. Unable to access resource details\n\n")
        else:
            file_obj.write("No resources found in this XER file.\n")

    def _write_activity_summary(self, file_obj):
        """Write activity summary to file."""
        file_obj.write("5. ACTIVITY SUMMARY\n")
        file_obj.write("=" * 80 + "\n")

        if "activities" in self.collection_data and self.collection_data["activities"]:
            activities_list = self.collection_data["activities"]
            file_obj.write(f"Total activities: {len(activities_list)}\n\n")

            if activities_list:
                # Sample of activities
                max_display = 5
                file_obj.write(f"Sample activities (showing first {max_display}):\n")
                for i, activity in enumerate(activities_list[:max_display], 1):
                    try:
                        task_id = getattr(activity, "task_code", "N/A")
                        task_name = getattr(activity, "task_name", "N/A")
                        file_obj.write(f"  {i}. ID: {task_id}, Name: {task_name}\n")
                    except Exception:
                        file_obj.write(f"  {i}. Unable to access activity details\n")

                if len(activities_list) > max_display:
                    file_obj.write(
                        f"  ... and {len(activities_list) - max_display} more\n"
                    )
        else:
            file_obj.write("No activities found in this XER file.\n")

    def _write_relationship_summary(self, file_obj):
        """Write relationship summary to file."""
        file_obj.write("6. RELATIONSHIP SUMMARY\n")
        file_obj.write("=" * 80 + "\n")

        if "relations" in self.collection_data and self.collection_data["relations"]:
            relations_list = self.collection_data["relations"]
            file_obj.write(f"Total relationships: {len(relations_list)}\n\n")

            if relations_list:
                # Sample of relationships
                max_display = 5
                file_obj.write(f"Sample relationships (showing first {max_display}):\n")
                for i, relation in enumerate(relations_list[:max_display], 1):
                    try:
                        pred_task = getattr(relation, "pred_task_id", "N/A")
                        succ_task = getattr(relation, "task_id", "N/A")
                        rel_type = getattr(relation, "pred_type", "N/A")
                        file_obj.write(f"  {i}. {pred_task} {rel_type} {succ_task}\n")
                    except Exception:
                        file_obj.write(
                            f"  {i}. Unable to access relationship details\n"
                        )

                if len(relations_list) > max_display:
                    file_obj.write(
                        f"  ... and {len(relations_list) - max_display} more\n"
                    )
        else:
            file_obj.write("No relationships found in this XER file.\n")


def explore_xer_file(xer_path, output_file, skip_large=True, large_threshold=1000):
    """
    Explore a XER file and generate a report.

    Args:
        xer_path (str): Path to the XER file
        output_file (str): Path to the output file
        skip_large (bool): Whether to skip detailed exploration of large collections
        large_threshold (int): Threshold for what is considered a large collection

    Returns:
        bool: True if successful, False otherwise
    """
    explorer = XerExplorer(xer_path)
    if not explorer.parse_file():
        return False

    explorer.collect_data()
    return explorer.generate_report(output_file, skip_large, large_threshold)


def main():
    """Command-line interface for XER Explorer."""
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

    print(f"Exploring XER file: {args.xer_file}")
    success = explore_xer_file(
        args.xer_file, args.output, not args.include_large, args.threshold
    )

    if success:
        print(f"Exploration complete! Results saved to {args.output}")
    else:
        print("Exploration failed!")
        sys.exit(1)


# Command-line interface
if __name__ == "__main__":
    main()
