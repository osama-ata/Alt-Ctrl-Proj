from typing import Optional, Any
from pydantic import BaseModel, Field

# Import all collection classes
from ..accounts import Accounts
from ..activitycodes import ActivityCodes
from ..activityresources import ActivityResources
from ..acttypes import ActTypes
from ..calendars import Calendars
from ..currencies import Currencies
from ..fintmpls import FinTmpls
from ..nonworks import NonWorks
from ..obss import OBSs
from ..pacttypes import PCatTypes
from ..pcatvals import PCatVals
from ..predecessors import Predecessors
from ..projcats import ProjCats
from ..projects import Projects
from ..rcattypes import RCatTypes
from ..rcatvals import RCatVals
from ..resources import Resources
from ..rolerates import RoleRates
from ..roles import Roles
from ..rsrccats import ResourceCategories
from ..rsrccurves import ResourceCurves
from ..rsrcrates import ResourceRates
from ..schedoptions import SchedOptions
from ..taskactvs import TaskActvs
from ..taskprocs import TaskProcs
from ..tasks import Tasks
from ..udftypes import UDFTypes
from ..udfvalues import UDFValues
from ..wbss import WBSs


class Data(BaseModel):
    _xer_file_path: Optional[str] = Field(default=None, exclude=True) # To store file path

    accounts: Accounts = Field(default_factory=Accounts)
    activitycodes: ActivityCodes = Field(default_factory=ActivityCodes)
    activityresources: ActivityResources = Field(default_factory=ActivityResources)
    acttypes: ActTypes = Field(default_factory=ActTypes)
    calendars: Calendars = Field(default_factory=Calendars)
    currencies: Currencies = Field(default_factory=Currencies)
    fintmpls: FinTmpls = Field(default_factory=FinTmpls)
    nonworks: NonWorks = Field(default_factory=NonWorks)
    obss: OBSs = Field(default_factory=OBSs)
    pcattypes: PCatTypes = Field(default_factory=PCatTypes)
    pcatvals: PCatVals = Field(default_factory=PCatVals)
    predecessors: Predecessors = Field(default_factory=Predecessors)
    projcats: ProjCats = Field(default_factory=ProjCats)
    projects: Projects = Field(default_factory=Projects)
    rcattypes: RCatTypes = Field(default_factory=RCatTypes)
    rcatvals: RCatVals = Field(default_factory=RCatVals)
    resources: Resources = Field(default_factory=Resources)
    rolerates: RoleRates = Field(default_factory=RoleRates)
    roles: Roles = Field(default_factory=Roles)
    rsrccats: ResourceCategories = Field(default_factory=ResourceCategories)
    rsrccurves: ResourceCurves = Field(default_factory=ResourceCurves)
    rsrcrates: ResourceRates = Field(default_factory=ResourceRates)
    schedoptions: SchedOptions = Field(default_factory=SchedOptions)
    taskactvs: TaskActvs = Field(default_factory=TaskActvs)
    taskprocs: TaskProcs = Field(default_factory=TaskProcs)
    tasks: Tasks = Field(default_factory=Tasks)
    udftypes: UDFTypes = Field(default_factory=UDFTypes)
    udfvalues: UDFValues = Field(default_factory=UDFValues)
    wbss: WBSs = Field(default_factory=WBSs)

    def model_post_init(self, __context: Any = None) -> None:
        super().model_post_init(__context)
        
        collection_field_names = [
            "accounts", "activitycodes", "activityresources", "acttypes", "calendars",
            "currencies", "fintmpls", "nonworks", "obss", "pcattypes", "pcatvals",
            "predecessors", "projcats", "projects", "rcattypes", "rcatvals",
            "resources", "rolerates", "roles", "rsrccats", "rsrccurves", "rsrcrates",
            "schedoptions", "taskactvs", "taskprocs", "tasks", "udftypes", "udfvalues", "wbss"
        ]
        
        for field_name in collection_field_names:
            collection_instance = getattr(self, field_name, None)
            # All collection classes are expected to have __init__(self, data_context: Optional[Any] = None)
            # and store it as self.data_context.
            # The default_factory will call their __init__ without arguments.
            # So, we set data_context here.
            if collection_instance is not None:
                 if hasattr(collection_instance, 'data_context'):
                    collection_instance.data_context = self
                 # For instances within the collection that might need direct access to Data
                 # This is generally handled by the collection's add method passing its data_context
                 # to the item's .data field.
                 # However, if items are somehow added before data_context is set on collection,
                 # this ensures they get it.
                 if hasattr(collection_instance, '_collection'): # Common pattern for internal list
                     for item in getattr(collection_instance, '_collection', []):
                         if hasattr(item, 'data') and item.data is None:
                             item.data = self # Pass the Data instance to each item

    class Config:
        arbitrary_types_allowed = True
