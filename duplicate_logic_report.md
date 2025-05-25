# Report: Duplicate Logic Findings in Alt-Ctrl-Proj Repository

The primary areas with noticeable duplicate or highly similar logic are found within the data model classes in `src/xer_parser/model/` and in the DCMA14 analysis module.

**1. Data Model Collection Classes (e.g., `Accounts`, `ActivityCodes`, `Calendars` in `src/xer_parser/model/`)**

A significant number of classes responsible for managing collections of XER entities exhibit a recurring structural pattern and method implementations. This includes:

*   **Initialization (`__init__`)**: Most collection classes (e.g., `Accounts`, `ActivityCodes`, `ActTypes`, `Calendars`, `Currencies`, `FinTmpls`, `NonWorks`, `OBSs`, `PCatTypes`, `PCatVals`, `Predecessors`, `ProjCats`, `Projects`, `RCatTypes`, `RCatVals`, `Resources`, `RoleRates`, `Roles`, `ResourceCategories`, `ResourceCurves`, `ResourceRates`, `SchedOptions`, `TaskActvs`, `TaskProcs`, `Tasks`, `UDFTypes`, `UDFValues`, `WBSs`) initialize an internal list to store objects and an `index` variable for iteration in a virtually identical manner.
    *   *Example*: `self.index = 0; self._accounts = []` in `accounts.py`.
*   **`add(params, ...)` Method**: The method for adding new items to the collection, where an object is instantiated from `params` and appended to the internal list, is highly similar across these classes.
    *   *Example*: `self._accounts.append(Account(params))` in `accounts.py`.
*   **Iterator Implementation (`__iter__`, `__next__`)**: The standard Python iterator protocol is implemented identically across most of these collection classes.
    *   *Example*: Present in `accounts.py`, `activitycodes.py`, `calendars.py`, etc.
*   **`count()` or `__len__()` Methods**: Methods to return the size of the collection are implemented consistently.
    *   *Example*: `def count(self): return len(self._accounts)` in `accounts.py`.
*   **`get_tsv()` Method**: This is a major area of duplication. The logic to generate a Tab-Separated Values (TSV) representation of the collection typically involves:
    1.  Checking if the collection is empty.
    2.  Initializing a list for TSV rows.
    3.  Appending a table identifier row (e.g., `["%T", "TABLE_NAME"]`).
    4.  Appending a header row with field names (e.g., `["%F", "field1", "field2", ...]`).
    5.  Iterating over the items in the collection, calling `item.get_tsv()` for each, and appending the result.
    6.  Returning the list of TSV rows or an empty list.
    *   *Files Affected*: `accounts.py`, `activitycodes.py`, `acttypes.py`, `calendars.py`, `currencies.py`, `fintmpls.py`, `nonworks.py`, `obss.py`, `pacttypes.py`, `pcatvals.py`, `projcats.py`, `projects.py`, `rcattypes.py`, `rcatvals.py`, `roles.py`, `rsrccats.py`, `rsrccurves.py`, `rsrcrates.py`, `schedoptions.py`, `taskactvs.py`, `taskprocs.py`, `tasks.py`, `udftypes.py`, `udfvalues.py`, `wbss.py`.
*   **`find_by_id(id)` Method**: Many collection classes have a method to find an item by its unique identifier. The core filtering logic is the same, though the specific ID attribute name (e.g., `acct_id`, `clndr_id`) and the name of the internal list vary.
    *   *Example*: `obj = list(filter(lambda x: x.clndr_id == id, self._calendars))` in `calendars.py`.
    *   *Files Affected*: `activitycodes.py`, `acttypes.py`, `calendars.py`, `currencies.py`, `fintmpls.py`, `obss.py`, `pacttypes.py`, `pcatvals.py`, `projects.py`, `rcattypes.py`, `rcatvals.py`, `roles.py`, `rolerates.py`, `rsrccurves.py`, `rsrcrates.py`, `schedoptions.py`, `taskactvs.py`, `taskprocs.py`, `tasks.py`, `udftypes.py`, `udfvalues.py`.

**2. Individual Data Item Classes (e.g., `Account`, `ActivityCode` in `src/xer_parser/model/classes/`)**

The classes representing individual data entities also show some repetition:

*   **Initialization (`__init__`)**: The parsing of parameters from the input `params` dictionary often follows a pattern of `self.attribute = type_conversion(params.get("key").strip()) if params.get("key") else None`.
    *   *Example*: `self.acct_id = int(params.get("acct_id").strip()) if params.get("acct_id") else None` in `account.py`.
*   **`get_tsv()` Method**: These methods consistently return a list starting with `"%R"` followed by the object's attributes, prepared for TSV output.
    *   *Example*: `return ["%R", self.acct_id, ...]` in `account.py`.

**3. DCMA14 Analysis (`src/xer_parser/dcma14/analysis.py`)**

Within the `DCMA14.analysis()` method, there's a repetitive pattern for conducting each of the 14 checks:

*   **Filtering Data**: A list of activities or relations is filtered based on specific criteria for the check.
*   **Counting Results**: The number of items passing the filter is counted.
*   **Storing Results**: The count, a list of the identified items (often processed by `self.get_activity()`), and the percentage are stored in the `self.results["analysis"]` dictionary under a specific key for that check.
    *   *Example*: The logic for handling "successors", "predecessors", "lags", "leads", "constraints", "totalfloat", "negativefloat", and "duration" all follow this structure closely.
