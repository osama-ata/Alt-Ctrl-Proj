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
from typing import Any, ClassVar

# Local imports
from xer_parser.model.accounts import Accounts
from xer_parser.model.activitycodes import ActivityCodes
from xer_parser.model.activityresources import ActivityResources
from xer_parser.model.acttypes import ActTypes
from xer_parser.model.calendars import Calendars
from xer_parser.model.classes.data import Data
from xer_parser.model.classes.fintmpl import FinTmpl
from xer_parser.model.classes.nonwork import NonWork
from xer_parser.model.classes.projcat import ProjCat
from xer_parser.model.classes.taskpred import TaskPred
from xer_parser.model.classes.taskproc import TaskProc
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
from xer_parser.model.taskprocs import TaskProcs
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

    This class reads an XER file and parses its contents into various Python objects
    representing projects, tasks, resources, and other Primavera P6 entities.

    Parameters
    ----------

    filename : str
        Path to the XER file to be parsed

    Attributes
    ----------

    file : str
        Path to the XER file
    projects : Projects
        Collection of projects in the XER file
    activities : Tasks
        Collection of activities/tasks in the XER file
    wbss : WBSs
        Collection of Work Breakdown Structure elements in the XER file
    relations : Predecessors
        Collection of relationships between activities in the XER file

    Examples
    --------

    >>> from xer_parser.reader import Reader
    >>> xer = Reader("myproject.xer")
    >>> for project in xer.projects:
    ...     print(project)
    """

    current_table: str = ""
    current_headers: ClassVar[list[str]] = []

    def write(self, filename: str | None = None) -> None:
        """
        Write the parsed data back to an XER file.

        Parameters
        ----------

        filename : str, optional
            Path to the output XER file. If None, an exception is raised.

        Raises
        ------

        Exception
            If filename is None

        Returns
        -------

        None
        """
        if filename is None:
            raise ValueError("You have to provide the filename")
        writeXER(self, filename)

    def create_object(self, object_type: str, params: dict[str, Any]) -> None:
        """
        Create appropriate objects based on the record type.

        This method creates and adds objects to their respective collections
        based on the type of record found in the XER file.

        Parameters
        ----------

        object_type : str
            The type of record in the XER file
        params : dict
            The parameters parsed from the record

        Returns
        -------

        None
        """
        if object_type.strip() == "CURRTYPE":
            self._currencies.add(params)
        elif object_type.strip() == "ROLES":
            self._roles.add(params)
        elif object_type.strip() == "ACCOUNT":
            self._accounts.add(params)
        elif object_type.strip() == "ROLERATE":
            self._rolerates.add(params)
        elif object_type.strip() == "OBS":
            self._obss.add(params)
        elif object_type.strip() == "RCATTYPE":
            self._rcattypes.add(params)
        elif object_type.strip() == "UDFTYPE":
            self._udftypes.add(params)
        elif object_type.strip() == "RCATVAL":
            self._rcatvals.add(params)
        elif object_type.strip() == "PROJECT":
            self._projects.add(params, self._data)
        elif object_type.strip() == "CALENDAR":
            self._calendars.add(params)
        elif object_type.strip() == "SCHEDOPTIONS":
            self._schedoptions.add(params)
        elif object_type.strip() == "PROJWBS":
            self._wbss.add(params, self._data)
        elif object_type.strip() == "RSRC":
            self._resources.add(params)
        elif object_type.strip() == "RSRCCURVDATA":
            self._rsrcurves.add(params)
        elif object_type.strip() == "ACTVTYPE":
            self._acttypes.add(params)
        elif object_type.strip() == "PCATTYPE":
            self._pcattypes.add(params)
        elif object_type.strip() == "PROJPCAT":
            self._projpcats.add(params)
        elif object_type.strip() == "PCATVAL":
            self._pcatvals.add(params)
        elif object_type.strip() == "RSRCRATE":
            self._rsrcrates.add(params)
        elif object_type.strip() == "RSRCRCAT":
            self._rsrccats.add(params)
        elif object_type.strip() == "TASK":
            self._tasks.add(params, self._data)
        elif object_type.strip() == "ACTVCODE":
            self._actvcodes.add(params)
        elif object_type.strip() == "TASKPRED":
            self._predecessors.add(params)
        elif object_type.strip() == "TASKRSRC":
            self._activityresources.add(params, self._data)
        elif object_type.strip() == "TASKPROC":
            self._taskprocs.add(params)
        elif object_type.strip() == "TASKACTV":
            self._activitycodes.add(params, self._data)
        elif object_type.strip() == "UDFVALUE":
            self._udfvalues.add(params)
        elif object_type.strip() == "FINTMPL":
            self._fintmpls.add(params)
        elif object_type.strip() == "NONWORK":
            self._nonworks.add(params)

    def summary(self) -> None:
        """
        Log a summary of the parsed XER file.

        Displays the number of activities and relationships in the parsed file.

        Returns
        -------

        None
        """
        logger.info("Number of activities: %d", self.activities.count)
        logger.info("Number of relationships: %d", len(TaskPred.obj_list))

    @property
    def projects(self) -> Projects:
        """
        Get all projects in the XER file.

        Returns
        -------

        Projects
            Collection of all projects contained in the XER file
        """
        return self._projects

    @property
    def activities(self) -> Tasks:
        """
        Get all tasks/activities in the XER file.

        Returns
        -------

        Tasks
            Collection of all tasks contained in the XER file
        """
        return self._tasks

    @property
    def wbss(self) -> WBSs:
        """
        Get all Work Breakdown Structure elements in the XER file.

        Returns
        -------

        WBSs
            Collection of all WBS elements in the XER file
        """
        return self._wbss

    @property
    def relations(self) -> Predecessors:
        """
        Get all relationships between activities in the XER file.

        Returns
        -------

        Predecessors
            Collection of all relationships in the XER file
        """
        return self._predecessors

    @property
    def resources(self) -> Resources:
        """
        Get all resources in the XER file.

        Returns
        -------

        Resources
            Collection of all resources in the XER file
        """
        return self._resources

    @property
    def accounts(self) -> Accounts:
        """
        Get all accounts in the XER file.

        Returns
        -------

        Accounts
            Collection of all accounts in the XER file
        """
        return self._accounts

    @property
    def activitycodes(self) -> ActivityCodes:
        """
        Get all activity codes in the XER file.

        Returns
        -------

        ActivityCodes
            Collection of all activity codes in the XER file
        """
        return self._activitycodes

    @property
    def actvcodes(self) -> TaskActvs:
        """
        Get all activity code values in the XER file.

        Returns
        -------

        TaskActvs
            Collection of all activity code values in the XER file
        """
        return self._actvcodes

    @property
    def acttypes(self) -> ActTypes:
        """
        Get all activity types in the XER file.

        Returns
        -------

        ActTypes
            Collection of all activity types in the XER file
        """
        return self._acttypes

    @property
    def calendars(self) -> Calendars:
        """
        Get all calendars in the XER file.

        Returns
        -------

        Calendars
            Collection of all calendars in the XER file
        """
        return self._calendars

    @property
    def currencies(self) -> Currencies:
        """
        Get all currencies in the XER file.

        Returns
        -------

        Currencies
            Collection of all currencies in the XER file
        """
        return self._currencies

    @property
    def obss(self) -> OBSs:
        """
        Get all OBS elements in the XER file.

        Returns
        -------

        OBSs
            Collection of all OBS elements in the XER file
        """
        return self._obss

    @property
    def rcattypes(self) -> RCatTypes:
        """
        Get all resource category types in the XER file.

        Returns
        -------

        RCatTypes
            Collection of all resource category types in the XER file
        """
        return self._rcattypes

    @property
    def rcatvals(self) -> RCatVals:
        """
        Get all resource category values in the XER file.

        Returns
        -------

        RCatVals
            Collection of all resource category values in the XER file
        """
        return self._rcatvals

    @property
    def rolerates(self) -> RoleRates:
        """
        Get all role rates in the XER file.

        Returns
        -------

        RoleRates
            Collection of all role rates in the XER file
        """
        return self._rolerates

    @property
    def roles(self) -> Roles:
        """
        Get all roles in the XER file.

        Returns
        -------

        Roles
            Collection of all roles in the XER file
        """
        return self._roles

    @property
    def resourcecurves(self) -> ResourceCurves:
        """
        Get all resource curves in the XER file.

        Returns
        -------

        ResourceCurves
            Collection of all resource curves in the XER file
        """
        return self._rsrcurves

    @property
    def resourcerates(self) -> ResourceRates:
        """
        Get all resource rates in the XER file.

        Returns
        -------

        ResourceRates
            Collection of all resource rates in the XER file
        """
        return self._rsrcrates

    @property
    def resourcecategories(self) -> ResourceCategories:
        """
        Get all resource categories in the XER file.

        Returns
        -------

        ResourceCategories
            Collection of all resource categories in the XER file
        """
        return self._rsrccats

    @property
    def scheduleoptions(self) -> SchedOptions:
        """
        Get all schedule options in the XER file.

        Returns
        -------

        SchedOptions
            Collection of all schedule options in the XER file
        """
        return self._schedoptions

    @property
    def activityresources(self) -> ActivityResources:
        """
        Get all activity resources in the XER file.

        Returns
        -------

        ActivityResources
            Collection of all activity resources in the XER file
        """
        return self._activityresources

    @property
    def udfvalues(self) -> UDFValues:
        """
        Get all UDF values in the XER file.

        Returns
        -------

        UDFValues
            Collection of all UDF values in the XER file
        """
        return self._udfvalues

    @property
    def udftypes(self) -> UDFTypes:
        """
        Get all UDF types in the XER file.

        Returns
        -------

        UDFTypes
            Collection of all UDF types in the XER file
        """
        return self._udftypes

    @property
    def pcattypes(self) -> list[PCatTypes]:
        """
        Get all project category types in the XER file.

        Returns
        -------

        list[PCatTypes]
            Collection of all project category types in the XER file
        """
        return self._pcattypes

    @property
    def pcatvals(self) -> list[PCatVals]:
        """
        Get all project category values in the XER file.

        Returns
        -------

        list[PCatVals]
            Collection of all project category values in the XER file
        """
        return self._pcatvals

    @property
    def projpcats(self) -> list[ProjCat]:
        """
        Get all project categories in the XER file.

        Returns
        -------

        list[ProjCat]
            Collection of all project categories in the XER file
        """
        return self._projpcats

    @property
    def taskprocs(self) -> list[TaskProc]:
        """
        Get all task procedures in the XER file.

        Returns
        -------

        list[TaskProc]
            Collection of all task procedures in the XER file
        """
        return self._taskprocs

    @property
    def fintmpls(self) -> list[FinTmpl]:
        """
        Get all financial templates in the XER file.

        Returns
        -------

        list[FinTmpl]
            Collection of all financial templates in the XER file
        """
        return self._fintmpls

    @property
    def nonworks(self) -> list[NonWork]:
        """
        Get all non-work periods in the XER file.

        Returns
        -------

        list[NonWork]
            Collection of all non-work periods in the XER file
        """
        return self._nonworks

    def __init__(self, filename: str) -> None:
        self.file = filename
        self._tasks = Tasks()
        self._predecessors = Predecessors()
        self._projects = Projects()
        self._wbss = WBSs()
        self._resources = Resources()
        self._accounts = Accounts()
        self._actvcodes = ActivityCodes()
        self._activitycodes = TaskActvs()
        self._acttypes = ActTypes()
        self._calendars = Calendars()
        self._currencies = Currencies()
        self._obss = OBSs()
        self._rcatvals = RCatVals()
        self._rcattypes = RCatTypes()
        self._rolerates = RoleRates()
        self._roles = Roles()
        self._rsrcurves = ResourceCurves()
        self._rsrcrates = ResourceRates()
        self._rsrccats = ResourceCategories()
        self._schedoptions = SchedOptions()
        self._activityresources = ActivityResources()
        self._udftypes = UDFTypes()
        self._udfvalues = UDFValues()
        self._pcattypes = PCatTypes()
        self._pcatvals = PCatVals()
        self._projpcats = ProjCats()
        self._taskprocs = TaskProcs()
        self._fintmpls = FinTmpls()
        self._nonworks = NonWorks()
        self._data = Data()
        self._data.projects = self._projects
        self._data.wbss = self._wbss
        self._data.tasks = self._tasks
        self._data.resources = self._resources
        self._data.taskresource = self._activityresources
        self._data.taskactvcodes = self._activitycodes
        self._data.predecessors = self._predecessors
        with codecs.open(filename, encoding="utf-8", errors="ignore") as tsvfile:
            stream = csv.reader(tsvfile, delimiter="\t")
            for row in stream:
                if row[0] == "%T":
                    current_table = row[1]
                elif row[0] == "%F":
                    current_headers = [r.strip() for r in row[1:]]
                elif row[0] == "%R":
                    zipped_record = dict(zip(current_headers, row[1:], strict=False))
                    self.create_object(current_table, zipped_record)

        # for line in content:
        #     line_lst = line.split('\t')
        #     if line_lst[0] == "%T":
        #         current_table = line_lst[1]
        #     elif line_lst[0] == "%R":
        #         self.create_object(current_table, line_lst[1:])

    def get_num_lines(self, file_path: str) -> int:
        """
        Get the number of lines in a file.

        Parameters
        ----------

        file_path : str
            Path to the file

        Returns
        -------

        int
            Number of lines in the file
        """
        with open(file_path, "r+", encoding="utf-8", errors="ignore") as fp:
            buf = mmap.mmap(fp.fileno(), 0)
            lines = 0
            while buf.readline():
                lines += 1
        return lines
