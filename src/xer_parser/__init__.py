"""Parser for XER written in Python.

PyP6XER is a Python library for parsing and working with Primavera P6 XER files.
"""

import importlib
import os

# Version information
__version__ = "1.0.0"  # Add version info if not already defined elsewhere

# Initialize __all__ as empty list (keep only this definition)
__all__: list[str] = []


def _get_model_modules() -> list[str]:
    """Dynamically discover all model modules.

    Returns:
        List of module names in the model package.
    """

    return [
        "accounts",
        "activityresources",
        "acttypes",
        "calendars",
        "currencies",
        "fintmpls",
        "nonworks",
        "obss",
        "pacttypes",
        "pcatvals",
        "predecessors",
        "projcats",
        "projects",
        "rcattypes",
        "rcatvals",
        "resources",
        "rolerates",
        "roles",
        "rsrccats",
        "rsrccurves",
        "rsrcrates",
        "schedoptions",
        "taskactvs",
        "taskprocs",
        "tasks",
        "udftypes",
        "udfvalues",
        "wbss",
    ]


def _lazy_import_models():
    """Lazily import all model modules and build __all__.

    This approach delays imports until actually needed, improving startup time.
    """
    global __all__
    if __all__:  # Already initialized
        return

    __all__ = []
    model_modules = _get_model_modules()

    for module_name in model_modules:
        try:
            module = importlib.import_module(f"xer_parser.model.{module_name}")
            if hasattr(module, "__all__"):
                __all__.extend(module.__all__)
        except ImportError as e:
            # Log warning but don't fail completely
            import warnings

            warnings.warn(
                f"Failed to import model module {module_name}: {e}", stacklevel=2
            )


# Lazy loading approach - only import when __all__ is accessed
def __getattr__(name: str):
    """Implement lazy loading for module attributes."""
    if name == "__all__" and not __all__:
        _lazy_import_models()
        return __all__

    # Try to import from model modules
    model_modules = _get_model_modules()
    for module_name in model_modules:
        try:
            module = importlib.import_module(f"xer_parser.model.{module_name}")
            if hasattr(module, name):
                return getattr(module, name)
        except ImportError:
            continue

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# For backwards compatibility, provide explicit imports
# This can be removed if lazy loading is preferred
def _import_all_models():
    """Import all model modules explicitly for backwards compatibility."""
    # Import modules locally to avoid circular dependencies
    import xer_parser.model.accounts as accounts
    import xer_parser.model.activityresources as activityresources
    import xer_parser.model.acttypes as acttypes
    import xer_parser.model.calendars as calendars
    import xer_parser.model.currencies as currencies
    import xer_parser.model.fintmpls as fintmpls
    import xer_parser.model.nonworks as nonworks
    import xer_parser.model.obss as obss
    import xer_parser.model.pacttypes as pacttypes
    import xer_parser.model.pcatvals as pcatvals
    import xer_parser.model.predecessors as predecessors
    import xer_parser.model.projcats as projcats
    import xer_parser.model.projects as projects
    import xer_parser.model.rcattypes as rcattypes
    import xer_parser.model.rcatvals as rcatvals
    import xer_parser.model.resources as resources
    import xer_parser.model.rolerates as rolerates
    import xer_parser.model.roles as roles
    import xer_parser.model.rsrccats as rsrccats
    import xer_parser.model.rsrccurves as rsrccurves
    import xer_parser.model.rsrcrates as rsrcrates
    import xer_parser.model.schedoptions as schedoptions
    import xer_parser.model.taskactvs as taskactvs
    import xer_parser.model.taskprocs as taskprocs
    import xer_parser.model.tasks as tasks
    import xer_parser.model.udftypes as udftypes
    import xer_parser.model.udfvalues as udfvalues
    import xer_parser.model.wbss as wbss

    # Build __all__ from imported modules
    global __all__
    __all__ = []

    modules = [
        accounts,
        activityresources,
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
    ]

    for module in modules:
        if hasattr(module, "__all__"):
            __all__.extend(module.__all__)


# Choose import strategy based on environment variable or default to lazy loading
if os.getenv("XER_PARSER_EAGER_IMPORT", "false").lower() == "true":
    _import_all_models()
else:
    # Use lazy loading by default
    pass

# __all__ is defined only once at the top, no duplicates present.
