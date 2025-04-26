"""PyP6XER: Parser for XER written in Python.

PyP6XER is a Python library for parsing and working with Primavera P6 XER files.
"""

# PyP6XER
# Copyright (C) 2020, 2021 Hassan Emam <hassan@constology.com>
#
# This file is part of PyP6XER.
#
# PyP6XER library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v2.1 as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyP6XER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>.

from xerparser.model.accounts import Accounts
from xerparser.model.activitiyresources import ActivityResources
from xerparser.model.activitycodes import ActivityCodes
from xerparser.model.acttypes import ActTypes
from xerparser.model.calendars import Calendars
from xerparser.model.currencies import Currencies
from xerparser.model.fintmpls import FinTmpls
from xerparser.model.nonworks import NonWorks
from xerparser.model.obss import OBSs
from xerparser.model.pacttypes import PCatTypes
from xerparser.model.pcatvals import PCatVals
from xerparser.model.predecessors import Predecessors
from xerparser.model.projcats import ProjCats
from xerparser.model.projects import Projects
from xerparser.model.rcattypes import RCatTypes
from xerparser.model.rcatvals import RCatVals
from xerparser.model.resources import Resources
from xerparser.model.rolerates import RoleRates
from xerparser.model.roles import Roles
from xerparser.model.rsrccats import ResourceCategories
from xerparser.model.rsrccurves import ResourceCurves
from xerparser.model.rsrcrates import ResourceRates
from xerparser.model.schedoptions import SchedOptions
from xerparser.model.taskactvs import TaskActvs
from xerparser.model.taskprocs import TaskProcs
from xerparser.model.tasks import Tasks
from xerparser.model.udftypes import UDFTypes
from xerparser.model.udfvalues import UDFValues
from xerparser.model.wbss import WBSs
