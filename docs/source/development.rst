Development
===========

This section provides guidelines for those who want to contribute to the PyP6XER-dev library.

Setting Up Development Environment
---------------------------------

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/osama-ata/PyP6Xer-dev.git
       cd PyP6Xer-dev

2. Create and activate a virtual environment:

   .. code-block:: bash

       python -m venv venv
       # On Windows
       venv\Scripts\activate
       # On Unix or MacOS
       source venv/bin/activate

3. Install development dependencies:

   .. code-block:: bash

       pip install -e ".[dev]"

Project Structure
----------------

The repository is organized as follows:

- ``xerparser_dev/``: Main package directory
  - ``model/``: Contains data models for XER entities
    - ``classes/``: Individual entity classes (Task, Resource, etc.)
  - ``dcma14/``: DCMA 14-point schedule assessment implementation
  - ``reader.py``: Core functionality for parsing XER files
  - ``write.py``: Functionality for writing to XER format

- ``tests/``: Test suite
  - ``fixtures/``: Test data including sample XER files
  - ``test_*.py``: Test modules

- ``docs/``: Documentation

Development Workflow
-------------------

1. Create a feature branch:

   .. code-block:: bash

       git checkout -b feature/your-feature-name

2. Make your changes, following coding standards.

3. Add tests for your changes in the ``tests/`` directory.

4. Run the test suite:

   .. code-block:: bash

       pytest

5. Check code quality:

   .. code-block:: bash

       mypy xerparser_dev
       ruff check xerparser_dev

6. Update documentation if necessary.

7. Submit a pull request.

Coding Standards
--------------

- Follow PEP 8 style guidelines.
- Add type hints to all functions and methods.
- Write NumPy-style docstrings for all modules, classes, functions, and methods.
- Write tests for new functionality.

Example NumPy-style Docstring
----------------------------

.. code-block:: python

    def example_function(param1: int, param2: str) -> bool:
        """
        Brief description of the function.

        Extended description with more details about what
        the function does, how it works, etc.

        Parameters
        ----------
        param1 : int
            Description of param1
        param2 : str
            Description of param2

        Returns
        -------
        bool
            Description of return value

        Raises
        ------
        ValueError
            When param1 is negative

        Examples
        --------
        >>> example_function(1, "test")
        True
        """
        # Function implementation here

Documentation
------------

Documentation is built using Sphinx with the Napoleon extension for NumPy-style docstrings.

To build the documentation:

.. code-block:: bash

    cd docs
    make html

The generated HTML documentation will be in ``docs/build/html/``.

Release Process
-------------

1. Update the version number in ``pyproject.toml``.

2. Update ``CHANGELOG.md`` following the Keep a Changelog format.

3. Create a new Git tag:

   .. code-block:: bash

       git tag -a v1.x.x -m "Version 1.x.x"
       git push origin v1.x.x

4. Build and upload the package to PyPI:

   .. code-block:: bash

       python -m build
       python -m twine upload dist/*