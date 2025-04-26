Getting Started
===============

This guide will walk you through the basic usage of PyP6XER to parse, analyze, and manipulate Primavera P6 XER files.

Loading an XER File
------------------

The first step is to load an XER file using the ``Reader`` class:

.. code-block:: python

    from xerparser_dev.reader import Reader
    
    # Load an XER file
    xer = Reader("project.xer")
    
    # Access basic project information
    for project in xer.projects:
        print(f"Project: {project.proj_short_name}")
        print(f"Start Date: {project.start_date}")
        print(f"Finish Date: {project.finish_date}")

Accessing Tasks
--------------

You can access all tasks/activities in the project:

.. code-block:: python

    # Get all tasks
    tasks = xer.activities
    
    # Print task information
    for task in tasks:
        print(f"Task: {task.task_name}")
        print(f"Duration: {task.duration}")
        print(f"Start: {task.early_start_date}")
        print(f"Finish: {task.early_end_date}")
    
    # Filter tasks by specific criteria
    critical_tasks = [task for task in tasks if task.total_float_hr_cnt <= 0]
    print(f"Number of critical tasks: {len(critical_tasks)}")

Working with the WBS (Work Breakdown Structure)
----------------------------------------------

You can access the Work Breakdown Structure elements:

.. code-block:: python

    # Get all WBS elements
    wbs_elements = xer.wbss
    
    # Print WBS hierarchy
    for wbs in wbs_elements:
        print(f"WBS: {wbs.wbs_name}")
        print(f"Level: {wbs.wbs_level}")
        
        # Find tasks belonging to this WBS
        wbs_tasks = [task for task in xer.activities if task.wbs_id == wbs.wbs_id]
        print(f"Number of tasks: {len(wbs_tasks)}")

Analyzing Relationships
---------------------

You can examine the relationships (dependencies) between tasks:

.. code-block:: python

    # Get all relationships
    relationships = xer.relations
    
    # Examine relationship types
    fs_count = len(relationships.finish_to_start)
    ss_count = len([r for r in relationships if r.pred_type == 'PR_SS'])
    ff_count = len([r for r in relationships if r.pred_type == 'PR_FF'])
    sf_count = len([r for r in relationships if r.pred_type == 'PR_SF'])
    
    print(f"Finish-to-Start: {fs_count}")
    print(f"Start-to-Start: {ss_count}")
    print(f"Finish-to-Finish: {ff_count}")
    print(f"Start-to-Finish: {sf_count}")
    
    # Find tasks with no predecessors
    tasks_without_predecessors = xer.activities.has_no_predecessor
    print(f"Tasks with no predecessors: {len(tasks_without_predecessors)}")

DCMA 14-Point Schedule Analysis
------------------------------

PyP6XER includes built-in support for the DCMA 14-point schedule assessment:

.. code-block:: python

    from xerparser_dev.dcma14.analysis import DCMA14
    
    # Create a DCMA14 analyzer
    analyzer = DCMA14(xer)
    
    # Run the analysis
    results = analyzer.analysis()
    
    # Print analysis results
    print(f"Missing logic - activities without successors: {results['analysis']['successors']['pct']:.2%}")
    print(f"Missing logic - activities without predecessors: {results['analysis']['predecessors']['pct']:.2%}")
    print(f"High float activities: {results['analysis']['totalfloat']['pct']:.2%}")
    print(f"Negative float activities: {results['analysis']['negativefloat']['pct']:.2%}")
    print(f"High duration activities: {results['analysis']['duration']['pct']:.2%}")

Modifying and Writing Back to XER
--------------------------------

You can modify the project data and write it back to XER format:

.. code-block:: python

    # Get a specific task by ID
    task = xer.activities.find_by_id(12345)
    
    # Modify the task
    task.task_name = "Updated Task Name"
    task.duration = 10
    
    # Write changes back to a new XER file
    xer.write("modified_project.xer")

Next Steps
---------

After mastering these basics, you can explore:

- Working with resources and resource assignments
- Manipulating calendars and non-work periods
- Advanced filtering and reporting techniques
- Integration with other Python libraries for analysis and visualization