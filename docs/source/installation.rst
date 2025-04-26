Installation
============

PyP6XER is available on PyPI and can be installed using pip. The library is compatible with Python 3.6 and above.

Basic Installation
-----------------

To install the latest stable release of PyP6XER:

.. code-block:: bash

    pip install pyp6xer

Development Installation
-----------------------

To install the development version directly from GitHub:

.. code-block:: bash

    pip install git+https://github.com/HassanEmam/PyP6Xer.git

Dependencies
-----------

PyP6XER has minimal dependencies:

- Python 3.6+

Optional Dependencies
-------------------

For running tests or contributing to development:

- pytest
- pytest-cov
- mypy
- ruff

You can install development dependencies with:

.. code-block:: bash

    pip install pyp6xer[dev]

Or manually:

.. code-block:: bash

    pip install pytest pytest-cov mypy ruff

Verification
-----------

To verify the installation, you can run:

.. code-block:: python

    import xerparser
    print(xerparser.__version__)