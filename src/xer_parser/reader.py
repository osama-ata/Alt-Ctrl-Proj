"""
This file starts the process of reading and parsing xer files

This module provides functionality to read and parse Primavera P6 XER files,
transforming the tabular data into Python objects.
"""

# Standard library imports
import codecs
import csv
import logging
import mmap
from typing import Any, ClassVar, Dict

# Local imports
from xer_parser.model.classes.data import Data
# Collection class imports are no longer needed here for instantiation,
# but might be needed for type hints in properties if not fully refactored to use Data.
from xer_parser.model.accounts import Accounts
from xer_parser.model.activitycodes import ActivityCodes # Used by a property
from xer_parser.model.activityresources import ActivityResources
from xer_parser.model.acttypes import ActTypes
from xer_parser.model.calendars import Calendars
from xer_parser.model.currencies import Currencies
from xer_parser.model.fintmpls import FinTmpls
from xer_parser.model.nonworks import NonWorks
from xer_parser.model.obss import OBSs
from xer_parser.model.pacttypes import PCatTypes
from xer_parser.model.pcatvals import PCatVals
from xer_parser.model.predecessors import Predecessors
from xer_parser.model.projcats import ProjCats
from xer_parser.model.projects import Projects
from xer_parser.model.rcattypes import RCatTypes
from xer_parser.model.rcatvals import RCatVals
from xer_parser.model.resources import Resources
from xer_parser.model.rolerates import RoleRates
from xer_parser.model.roles import Roles
from xer_parser.model.rsrccats import ResourceCategories
from xer_parser.model.rsrccurves import ResourceCurves
from xer_parser.model.rsrcrates import ResourceRates
from xer_parser.model.schedoptions import SchedOptions
from xer_parser.model.taskactvs import TaskActvs
from xer_parser.model.taskprocs import TaskProcs # Used by a property
from xer_parser.model.tasks import Tasks
from xer_parser.model.udftypes import UDFTypes
from xer_parser.model.udfvalues import UDFValues
from xer_parser.model.wbss import WBSs

from xer_parser.write import writeXER

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Reader:
    """
    Main parser class for Primavera P6 XER files.
    """

    current_table: str = ""
    current_headers: ClassVar[list[str]] = []
    _data: Data # Main data container

    def __init__(self, filename: str) -> None:
        self.file = filename # Keep original filename if needed for metadata
        self._data = Data(_xer_file_path=filename) # Instantiate the main Data Pydantic model

        # The Data model's model_post_init will set self._data as data_context for all collections
        
        with codecs.open(filename, encoding="utf-8", errors="ignore") as tsvfile:
            stream = csv.reader(tsvfile, delimiter="\t")
            for row in stream:
                if not row:  # Skip empty rows
                    continue
                row_type = row[0]
                if row_type == "%T":
                    self.current_table = row[1]
                elif row_type == "%F":
                    self.current_headers = [r.strip() for r in row[1:]]
                elif row_type == "%R":
                    # Ensure current_headers is set before processing rows
                    if not self.current_headers:
                        logger.warning(f"Skipping row in table {self.current_table} due to missing headers: {row}")
                        continue
                    zipped_record = dict(zip(self.current_headers, row[1:], strict=False))
                    self.create_object(self.current_table, zipped_record)


    def write(self, filename: str | None = None) -> None:
        if filename is None:
            raise ValueError("You have to provide the filename")
        # writeXER function would need to be adapted to work with the Pydantic Data model
        writeXER(self._data, filename) # Pass the Data object

    def create_object(self, object_type: str, params: Dict[str, Any]) -> None:
        """
        Adds parsed data to the appropriate collection within the Data object.
        """
        ot = object_type.strip()
        # The collection's add method now handles Pydantic model validation
        # and setting the .data attribute on the model instance if needed.
        # The data_context for the collection itself is set by Data.model_post_init.
        if ot == "CURRTYPE":
            self._data.currencies.add(params)
        elif ot == "ROLES":
            self._data.roles.add(params)
        elif ot == "ACCOUNT":
            self._data.accounts.add(params)
        elif ot == "ROLERATE":
            self._data.rolerates.add(params)
        elif ot == "OBS":
            self._data.obss.add(params)
        elif ot == "RCATTYPE":
            self._data.rcattypes.add(params)
        elif ot == "UDFTYPE":
            self._data.udftypes.add(params)
        elif ot == "RCATVAL":
            self._data.rcatvals.add(params)
        elif ot == "PROJECT":
            self._data.projects.add(params) # data_context is set by Data's post_init
        elif ot == "CALENDAR":
            self._data.calendars.add(params)
        elif ot == "SCHEDOPTIONS":
            self._data.schedoptions.add(params)
        elif ot == "PROJWBS":
            self._data.wbss.add(params)
        elif ot == "RSRC":
            self._data.resources.add(params)
        elif ot == "RSRCCURVDATA":
            self._data.rsrccurves.add(params)
        elif ot == "ACTVTYPE":
            self._data.acttypes.add(params)
        elif ot == "PCATTYPE":
            self._data.pcattypes.add(params)
        elif ot == "PROJPCAT":
            self._data.projcats.add(params)
        elif ot == "PCATVAL":
            self._data.pcatvals.add(params)
        elif ot == "RSRCRATE":
            self._data.rsrcrates.add(params)
        elif ot == "RSRCRCAT":
            self._data.rsrccats.add(params)
        elif ot == "TASK":
            self._data.tasks.add(params)
        elif ot == "ACTVCODE": # This is for ActivityCode definitions
            self._data.activitycodes.add(params)
        elif ot == "TASKPRED":
            self._data.predecessors.add(params)
        elif ot == "TASKRSRC":
            self._data.activityresources.add(params)
        elif ot == "TASKPROC":
            self._data.taskprocs.add(params)
        elif ot == "TASKACTV": # This is for assignments of ActivityCodes to Tasks
            self._data.taskactvs.add(params)
        elif ot == "UDFVALUE":
            self._data.udfvalues.add(params)
        elif ot == "FINTMPL":
            self._data.fintmpls.add(params)
        elif ot == "NONWORK":
            self._data.nonworks.add(params)
        # else:
            # logger.debug(f"Unknown object type: {ot}")


    def summary(self) -> None:
        logger.info("Number of activities: %d", self.activities.count)
        logger.info("Number of relationships: %d", self.relations.count) # Changed from TaskPred.obj_list

    # Properties now access collections from self._data
    @property
    def projects(self) -> Projects:
        return self._data.projects

    @property
    def activities(self) -> Tasks:
        return self._data.tasks

    @property
    def wbss(self) -> WBSs:
        return self._data.wbss

    @property
    def relations(self) -> Predecessors:
        return self._data.predecessors

    @property
    def resources(self) -> Resources:
        return self._data.resources

    @property
    def accounts(self) -> Accounts:
        return self._data.accounts

    @property
    def activitycodes(self) -> ActivityCodes: # Collection of ActivityCode definitions
        return self._data.activitycodes

    @property
    def actvcodes(self) -> TaskActvs: # Collection of TaskActv (assignments)
        return self._data.taskactvs # Corrected to point to taskactvs

    @property
    def acttypes(self) -> ActTypes:
        return self._data.acttypes

    @property
    def calendars(self) -> Calendars:
        return self._data.calendars

    @property
    def currencies(self) -> Currencies:
        return self._data.currencies

    @property
    def obss(self) -> OBSs:
        return self._data.obss

    @property
    def rcattypes(self) -> RCatTypes:
        return self._data.rcattypes

    @property
    def rcatvals(self) -> RCatVals:
        return self._data.rcatvals

    @property
    def rolerates(self) -> RoleRates:
        return self._data.rolerates

    @property
    def roles(self) -> Roles:
        return self._data.roles

    @property
    def resourcecurves(self) -> ResourceCurves: # Corrected property name casing
        return self._data.rsrccurves

    @property
    def resourcerates(self) -> ResourceRates: # Corrected property name casing
        return self._data.rsrcrates

    @property
    def resourcecategories(self) -> ResourceCategories: # Corrected property name casing
        return self._data.rsrccats

    @property
    def scheduleoptions(self) -> SchedOptions: # Corrected property name casing
        return self._data.schedoptions

    @property
    def activityresources(self) -> ActivityResources: # Corrected property name casing
        return self._data.activityresources

    @property
    def udfvalues(self) -> UDFValues:
        return self._data.udfvalues

    @property
    def udftypes(self) -> UDFTypes:
        return self._data.udftypes
    
    @property
    def pcattypes(self) -> PCatTypes: # Corrected return type
        return self._data.pcattypes

    @property
    def pcatvals(self) -> PCatVals: # Corrected return type
        return self._data.pcatvals

    @property
    def projpcats(self) -> ProjCats: # Corrected return type
        return self._data.projcats

    @property
    def taskprocs(self) -> TaskProcs: # Corrected return type
        return self._data.taskprocs

    @property
    def fintmpls(self) -> FinTmpls: # Corrected return type
        return self._data.fintmpls

    @property
    def nonworks(self) -> NonWorks: # Corrected return type
        return self._data.nonworks


    def get_num_lines(self, file_path: str) -> int:
        with open(file_path, "r+", encoding="utf-8", errors="ignore") as fp:
            buf = mmap.mmap(fp.fileno(), 0)
            lines = 0
            while buf.readline():
                lines += 1
        return lines
