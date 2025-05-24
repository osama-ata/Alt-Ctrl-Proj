# Alt-Ctrl-Proj Python Primavera P6 XER parser

![Tests](https://github.com/osama-ata/Alt-Ctrl-Proj/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/osama-ata/Alt-Ctrl-Proj/branch/master/graph/badge.svg?token=YOUR-TOKEN-HERE)](https://codecov.io/gh/osama-ata/Alt-Ctrl-Proj)
[![Publish Python 🐍 package](https://github.com/osama-ata/Alt-Ctrl-Proj/actions/workflows/publish.yml/badge.svg)](https://github.com/osama-ata/Alt-Ctrl-Proj/actions/workflows/publish.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15287707.svg)](https://doi.org/10.5281/zenodo.15287707)

Alt-Ctrl-Proj is an actively maintained fork of PyP6Xer, an open-source project for parsing Primavera XER files in Python. The project is a work in progress and open for community contributions.

In order to install a copy in your system you can use pip package manager as follows:

```bash
pip install Alt-Ctrl-Proj
```

The usage of the library is fairly simple and the import examples can be:

```python
from xer_parser.reader import Reader
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

Alt-Ctrl-Proj now includes an XER Explorer tool that helps you quickly analyze the contents of XER files. The tool generates a concise report with key information about the file, including projects, calendars, WBS elements, and more.

### Command-line Usage

After installing Alt-Ctrl-Proj, you can use the XER Explorer tool directly from the command line using the provided entry point:

```bash
# Basic usage
xer-explorer path/to/your/file.xer

# Specify custom output file
xer-explorer path/to/your/file.xer -o custom_report.txt

# Include large collections (which are skipped by default)
xer-explorer path/to/your/file.xer --include-large
```

> **Note:** The `xer-explorer` command is available after installing the package via pip. The script in `scripts/xer_explorer.py` is for development or manual use only.

### Programmatic Usage

You can also use the Explorer in your Python code:

```python
from xer_parser.tools import explore_xer_file

# Generate a report with default settings
explore_xer_file("path/to/your/file.xer", "output_report.txt")
```

For more advanced usage and examples, see the [documentation](https://alt-ctrl-proj.readthedocs.io/).
