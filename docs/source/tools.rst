Tools Reference
==============

This section covers the utility tools provided by Alt-Ctrl-Proj for common operations when working with XER files.

XER Explorer
------------

The XER Explorer is a utility for exploring and summarizing the contents of XER files. It provides both a command-line interface and a programmatic API.

Overview
~~~~~~~~

When working with XER files, especially large ones, it can be difficult to quickly understand what data is contained within the file. The XER Explorer tool generates a concise report that summarizes the key elements in an XER file, including:

- File statistics and collection sizes
- Project details
- Calendar information
- WBS elements
- Resources
- And optionally activities and relationships (if not too large)

Command-Line Usage
~~~~~~~~~~~~~~~~~~

The XER Explorer can be used directly from the command line after installing Alt-Ctrl-Proj. The CLI entry point is installed as `xer-explorer`:

.. code-block:: bash

    # Basic usage
    xer-explorer path/to/your/file.xer

    # Specify custom output file
    xer-explorer path/to/your/file.xer -o custom_report.txt

    # Include large collections (which are skipped by default)
    xer-explorer path/to/your/file.xer --include-large

Options:

* ``-o, --output``: Specify the output file path (default: xer_exploration.txt)
* ``--include-large``: Include detailed exploration of large collections
* ``--threshold``: Set the threshold for what is considered a large collection (default: 1000)

> **Note:** The `xer-explorer` command is available after installing the package. The script in `scripts/xer_explorer.py` is for development or manual use only.

API Reference
~~~~~~~~~~~~~

.. py:class:: xerparser_dev.tools.XerExplorer(xer_path)

   A class for exploring and summarizing XER files.

   :param str xer_path: Path to the XER file to explore

   .. py:method:: parse_file()

      Parse the XER file using the Reader class.

      :return: True if successful, False otherwise
      :rtype: bool

   .. py:method:: collect_data()

      Collect data from all collections in the XER file.

      :return: Dictionary of collection names and their data
      :rtype: dict

   .. py:method:: generate_report(output_file, skip_large_collections=True, large_threshold=1000)

      Generate a report of the XER file contents.

      :param str output_file: Path to the output file
      :param bool skip_large_collections: Whether to skip detailed exploration of large collections
      :param int large_threshold: Threshold for what is considered a large collection
      :return: True if successful, False otherwise
      :rtype: bool

.. py:function:: xerparser_dev.tools.explore_xer_file(xer_path, output_file, skip_large=True, large_threshold=1000)

   Explore a XER file and generate a report.

   :param str xer_path: Path to the XER file
   :param str output_file: Path to the output file
   :param bool skip_large: Whether to skip detailed exploration of large collections
   :param int large_threshold: Threshold for what is considered a large collection
   :return: True if successful, False otherwise
   :rtype: bool

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

    from xerparser_dev.tools import XerExplorer, explore_xer_file

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
