"""PyP6XER: Parser for XER written in Python.

PyP6XER is a Python library for parsing and working with Primavera P6 XER files.
"""

# Auto-import model modules
from xerparser_dev.model import (
    accounts,
    activitiyresources,
    activitycodes,
    acttypes,
    calendars,
    currencies,
    fintmpls,
    nonworks,
    obss,
    pacttypes,
    pcatvals,
    predecessors,
    projcats,
    projects,
    rcattypes,
    rcatvals,
    resources,
    rolerates,
    roles,
    rsrccats,
    rsrccurves,
    rsrcrates,
    schedoptions,
    taskactvs,
    taskprocs,
    tasks,
    udftypes,
    udfvalues,
    wbss,
)

# Auto-build __all__
__all__ = []
for module in [
    accounts,
    activitiyresources,
    activitycodes,
    acttypes,
    calendars,
    currencies,
    fintmpls,
    nonworks,
    obss,
    pacttypes,
    pcatvals,
    predecessors,
    projcats,
    projects,
    rcattypes,
    rcatvals,
    resources,
    rolerates,
    roles,
    rsrccats,
    rsrccurves,
    rsrcrates,
    schedoptions,
    taskactvs,
    taskprocs,
    tasks,
    udftypes,
    udfvalues,
    wbss,
]:
    __all__.extend(module.__all__)
