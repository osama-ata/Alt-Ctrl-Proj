# PyP6Xer Python Primavera P6 XER parser

![Tests](https://github.com/osama-ata/PyP6Xer-dev/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/osama-ata/PyP6Xer-dev/branch/master/graph/badge.svg?token=YOUR-TOKEN-HERE)](https://codecov.io/gh/osama-ata/PyP6Xer-dev)

PyXer is an open source project to parse Primavera xer files in python. The project is work in progress and open for community contributions.

In order to install a copy in your system you can use pip package manager as follows:

```bash
pip install PyP6XER-dev
```

The usage of the library is fairly simple and the import examples can be:

```python
from xerparser.reader import Reader
```

Here are some examples of reading and parsing xer files:

```python
xer = Reader("<filename>") # this returns a reader object  
```

to read all projects in file as one xer file may have multiple projects stored into it:

```python
for project in xer.projects:
  print(project)
```

## XER Explorer Tool

PyP6Xer now includes an XER Explorer tool that helps you quickly analyze the contents of XER files. The tool generates a concise report with key information about the file, including projects, calendars, WBS elements, and more.

### Command-line Usage

After installing PyP6Xer, you can use the explorer directly from the command line:

```bash
# Basic usage
xer-explorer path/to/your/file.xer

# Specify custom output file
xer-explorer path/to/your/file.xer -o custom_report.txt

# Include large collections (which are skipped by default)
xer-explorer path/to/your/file.xer --include-large
```

### Programmatic Usage

You can also use the Explorer in your Python code:

```python
from xerparser.tools import explore_xer_file

# Generate a report with default settings
explore_xer_file("path/to/your/file.xer", "output_report.txt")
```

For more advanced usage and examples, see the [documentation](https://pyp6xer.readthedocs.io/).
