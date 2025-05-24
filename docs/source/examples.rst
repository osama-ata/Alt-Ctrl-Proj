Examples
========

This section provides practical examples of using Alt-Ctrl-Proj for various tasks related to Primavera P6 project management.

Schedule Health Check
--------------------

This example performs a complete schedule health check using the DCMA 14-point assessment criteria:

.. code-block:: python

    from xer_parser.reader import Reader
    from xer_parser.dcma14.analysis import DCMA14

    # Load the XER file
    xer = Reader("project.xer")

    # Create analyzer with custom thresholds
    analyzer = DCMA14(xer,
                     duration_limit=5,    # Flag activities with duration > 5 days
                     lag_limit=2,         # Flag relationships with lag > 2 days
                     tf_limit=15)         # Flag activities with float > 15 days

    # Run analysis
    results = analyzer.analysis()

    # Print summary
    print("DCMA 14-Point Assessment Results:")
    print("=================================")
    print(f"Total Activities: {results['analysis']['summary']['activity_cnt']}")
    print(f"Total Relationships: {results['analysis']['summary']['relationship_cnt']}")

    # Check missing logic
    successors_pct = results['analysis']['successors']['pct'] * 100
    print(f"Activities missing successors: {successors_pct:.1f}% (threshold: 5%)")

    predecessors_pct = results['analysis']['predecessors']['pct'] * 100
    print(f"Activities missing predecessors: {predecessors_pct:.1f}% (threshold: 5%)")

    # Check high float
    highfloat_pct = results['analysis']['totalfloat']['pct'] * 100
    print(f"Activities with high float: {highfloat_pct:.1f}% (threshold: 5%)")

    # Check negative float
    negfloat_pct = results['analysis']['negativefloat']['pct'] * 100
    print(f"Activities with negative float: {negfloat_pct:.1f}% (threshold: 0%)")

    # Check resources
    no_resources_pct = results['analysis']['resources']['pct'] * 100
    print(f"Activities without resources: {no_resources_pct:.1f}% (threshold: 10%)")

Extracting Critical Path
-----------------------

This example extracts and analyzes the critical path from a project:

.. code-block:: python

    from xer_parser.reader import Reader

    # Load the XER file
    xer = Reader("project.xer")

    # Get all activities
    activities = xer.activities.activities

    # Identify critical activities (zero or negative float)
    critical_activities = [
        activity for activity in activities
        if activity.total_float_hr_cnt is not None and activity.total_float_hr_cnt <= 0
    ]

    # Sort by early start date to see the sequence
    critical_activities.sort(key=lambda x: x.early_start_date if x.early_start_date else datetime.max)

    # Print critical path
    print("Critical Path Analysis:")
    print("======================")
    print(f"Number of critical activities: {len(critical_activities)}")

    for activity in critical_activities:
        # Get predecessors and successors of this critical activity
        predecessors = xer.relations.get_predecessors(activity.task_id)
        successors = xer.relations.get_successors(activity.task_id)

        # Count how many predecessors and successors are also on critical path
        critical_preds = sum(1 for p in predecessors if
                            xer.activities.find_by_id(p.pred_task_id).total_float_hr_cnt is not None and
                            xer.activities.find_by_id(p.pred_task_id).total_float_hr_cnt <= 0)

        critical_succs = sum(1 for s in successors if
                            xer.activities.find_by_id(s.task_id).total_float_hr_cnt is not None and
                            xer.activities.find_by_id(s.task_id).total_float_hr_cnt <= 0)

        # Print activity details
        print(f"\nActivity: {activity.task_code} - {activity.task_name}")
        print(f"  Duration: {activity.duration} days")
        print(f"  Early Start: {activity.early_start_date}")
        print(f"  Early Finish: {activity.early_end_date}")
        print(f"  Float: {activity.total_float_hr_cnt / 8.0 if activity.total_float_hr_cnt else 0} days")
        print(f"  Critical predecessors: {critical_preds}/{len(predecessors)}")
        print(f"  Critical successors: {critical_succs}/{len(successors)}")

Resource Loading Analysis
-----------------------

This example analyzes resource loading across the project timeline:

.. code-block:: python

    from xer_parser.reader import Reader
    from collections import defaultdict
    from datetime import datetime, timedelta

    # Load the XER file
    xer = Reader("project.xer")

    # Get resources and resource assignments
    resources = xer.resources
    assignments = xer.activityresources

    # Create a dictionary to track resource loading by day
    resource_loading = defaultdict(lambda: defaultdict(float))

    # Process all activities with assigned resources
    for activity in xer.activities.activities:
        # Skip activities without dates
        if not activity.early_start_date or not activity.early_end_date:
            continue

        # Get resource assignments for this activity
        activity_assignments = assignments.find_by_activity_id(activity.task_id)

        if not activity_assignments:
            continue

        # Calculate daily resource units
        start_date = activity.early_start_date
        end_date = activity.early_end_date
        duration_days = (end_date - start_date).days + 1

        if duration_days <= 0:
            continue

        # Process each assignment
        for assignment in activity_assignments:
            resource_id = assignment.rsrc_id
            units_per_day = float(assignment.remain_qty) / duration_days if assignment.remain_qty else 0

            # Distribute units across all days of the activity
            current_date = start_date
            while current_date <= end_date:
                # Skip weekends (simplistic approach)
                if current_date.weekday() < 5:  # 0-4 are Monday to Friday
                    resource_loading[resource_id][current_date] += units_per_day

                current_date += timedelta(days=1)

    # Print resource loading
    print("Resource Loading Analysis:")
    print("=========================")

    for resource_id, daily_loading in resource_loading.items():
        resource = resources.find_by_id(resource_id)
        if not resource:
            continue

        print(f"\nResource: {resource.rsrc_name}")

        # Find peak loading
        peak_date = max(daily_loading.items(), key=lambda x: x[1], default=(None, 0))
        if peak_date[0]:
            print(f"Peak loading: {peak_date[1]:.2f} units on {peak_date[0]}")

        # Calculate average loading
        avg_loading = sum(daily_loading.values()) / len(daily_loading) if daily_loading else 0
        print(f"Average loading: {avg_loading:.2f} units")

        # Get total assigned units
        total_units = sum(daily_loading.values())
        print(f"Total assigned units: {total_units:.2f}")

XER Explorer Tool
----------------

This example demonstrates how to use the XER Explorer tool to generate a summary report of a P6 XER file:

Command-Line Usage
~~~~~~~~~~~~~~~~~

The Explorer tool can be used directly from the command line after installing Alt-Ctrl-Proj:

.. code-block:: bash

    # Basic usage
    xer-explorer path/to/your/file.xer

    # Specify custom output file
    xer-explorer path/to/your/file.xer -o custom_report.txt

    # Include large collections (which are skipped by default)
    xer-explorer path/to/your/file.xer --include-large

    # Set custom threshold for what's considered a "large" collection
    xer-explorer path/to/your/file.xer --threshold 2000

Programmatic Usage
~~~~~~~~~~~~~~~~

The Explorer can also be used programmatically in your Python code:

.. code-block:: python

    from xer_parser.tools import XerExplorer, explore_xer_file

    # Simple function approach
    explore_xer_file("path/to/your/file.xer", "output_report.txt")

    # Object-oriented approach for more control
    explorer = XerExplorer("path/to/your/file.xer")
    explorer.parse_file()
    explorer.collect_data()
    explorer.generate_report("output_report.txt",
                            skip_large_collections=True,
                            large_threshold=1000)

    # Access the collected data directly
    project_data = explorer.collection_data.get("projects", [])
    for project in project_data:
        print(f"Project: {project.proj_short_name}")

Example Output
~~~~~~~~~~~~

The Explorer generates a concise report with information about the XER file contents:

.. code-block:: text

    Alt-Ctrl-Proj Exploration Results
    Generated on: 2025-04-14 15:45:30
    XER File: sample2.xer
    ================================================================================

    FILE STATISTICS
    ================================================================================
    Collections found in this XER file:
      projects: 1 items
      wbss: 837 items
      activities: 3397 items
      relations: 7474 items
      calendars: 12 items
      resources: 2 items
      activitycodes: 15655 items

    Skipping detailed exploration of large collections:
      - activities (too large - 3397 items)
      - relations (too large - 7474 items)
      - activitycodes (too large - 15655 items)

    --------------------------------------------------------------------------------

    1. PROJECT SUMMARY
    ================================================================================
    Found 1 project(s)

    Project #1:
      proj_id: 4015
      proj_short_name: SA06C1_BL_Rev_F_10042025
      clndr_id: 639
      plan_start_date: 2020-12-31 00:00
      plan_end_date: None

    // ... additional sections ...

This makes it easy to get a quick overview of an XER file's contents without having to write custom code to explore each part of the file.
