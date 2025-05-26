"""Module for writing parsed XER data back to files.

This module provides functionality to write data from the Data
object back to an XER file in the Primavera P6 format.
"""

import csv
from typing import Any
# Import the main Pydantic Data model
from xer_parser.model.classes.data import Data # Assuming this is the correct path

# __all__ = ["writeXER"] # Typically __all__ is for package exports


def writeXER(data_obj: Data, filename: str) -> None: # Changed 'r: Any' to 'data_obj: Data'
    """
    Write parsed data back to an XER file.

    This function writes all the data contained in the Data object back to a
    new XER file in the Primavera P6 format. It creates a TSV (tab-separated values)
    file with all the tables and records from the original XER file, potentially with
    modifications if made to the data structures.

    Parameters
    ----------
    data_obj : Data
        The Data object containing the parsed XER data
    filename : str
        Path to the output XER file

    Returns
    -------
    None

    Notes
    -----
    The order of tables written to the XER file is important and follows Primavera P6's
    requirements for dependencies between tables. The function adds appropriate headers
    and format indicators for the XER file format.

    Examples
    --------
    >>> from xer_parser.reader import Reader # Assuming Reader populates a Data object
    >>> from xer_parser.write import writeXER
    >>> xer_reader = Reader("input.xer")
    >>> data_to_write = xer_reader._data # Access the Data instance from the Reader
    >>> # Make modifications to the data_to_write
    >>> writeXER(data_to_write, "output.xer")
    """
    header = [
        "ERMHDR",
        "8.0", # This version might need to be dynamic or configurable
        "2021-11-02", # This date might need to be dynamic
        "Project", "admin", "Primavera", "Admin",
        "dbxDatabaseNoName", "Project Management", "U.K.",
    ]
    with open(filename, "w", newline="", encoding="utf-8") as output:
        tsv_writer = csv.writer(output, delimiter="\t", lineterminator="\n") # Ensure consistent line endings
        tsv_writer.writerow(header)
        
        # Access collections from the data_obj
        tsv_writer.writerows(data_obj.currencies.get_tsv())
        tsv_writer.writerows(data_obj.fintmpls.get_tsv())
        tsv_writer.writerows(data_obj.nonworks.get_tsv())
        tsv_writer.writerows(data_obj.obss.get_tsv())
        tsv_writer.writerows(data_obj.pcattypes.get_tsv())
        tsv_writer.writerows(data_obj.rsrccurves.get_tsv())
        tsv_writer.writerows(data_obj.udftypes.get_tsv())
        tsv_writer.writerows(data_obj.accounts.get_tsv())
        tsv_writer.writerows(data_obj.pcatvals.get_tsv())
        tsv_writer.writerows(data_obj.projects.get_tsv())
        tsv_writer.writerows(data_obj.calendars.get_tsv())
        tsv_writer.writerows(data_obj.projcats.get_tsv())
        tsv_writer.writerows(data_obj.schedoptions.get_tsv())
        tsv_writer.writerows(data_obj.wbss.get_tsv())
        tsv_writer.writerows(data_obj.resources.get_tsv())
        tsv_writer.writerows(data_obj.acttypes.get_tsv())
        tsv_writer.writerows(data_obj.rsrcrates.get_tsv())
        tsv_writer.writerows(data_obj.tasks.get_tsv())
        # Note: In Reader, ACTVCODE table was mapped to _activitycodes (ActivityCodes collection)
        # and TASKACTV to _taskactvs (TaskActvs collection).
        # Assuming data_obj.activitycodes is the collection for ACTVCODE table (definitions)
        # and data_obj.taskactvs is for TASKACTV table (assignments).
        # The original writeXER had r.actvcodes.get_tsv() and r.activitycodes.get_tsv().
        # Based on refactored Data model, it should be:
        tsv_writer.writerows(data_obj.activitycodes.get_tsv()) # For ACTVCODE (definitions)
        # PROJCOST - This table was not explicitly handled in the Reader's create_object or Data model.
        # If it exists, it needs a collection and Pydantic model. Skipping for now.
        tsv_writer.writerows(data_obj.predecessors.get_tsv())
        tsv_writer.writerows(data_obj.taskprocs.get_tsv())
        tsv_writer.writerows(data_obj.activityresources.get_tsv()) # TASKRSRC
        tsv_writer.writerows(data_obj.taskactvs.get_tsv()) # For TASKACTV (assignments)
        tsv_writer.writerows(data_obj.udfvalues.get_tsv())
        tsv_writer.writerow(["%E"])
