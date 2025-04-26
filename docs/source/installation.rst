Installation
============

PyP6Xer-dev is available on PyPI and can be installed using pip. The library is compatible with Python 3.6 and above.

Basic Installation
-----------------

To install the latest stable release of PyP6Xer-dev:

.. code-block:: bash

    pip install pyp6xer-dev

Development Installation
-----------------------

To install the development version directly from GitHub:

.. code-block:: bash

    pip install git+https://github.com/osama-ata/PyP6Xer-dev.git

Dependencies
-----------

PyP6Xer-dev has minimal dependencies:

- Python 3.8+

Optional Dependencies
-------------------

For running tests or contributing to development:

- pytest
- pytest-cov
- mypy
- ruff

You can install development dependencies with:

.. code-block:: bash

    pip install pyp6xer-dev[dev]

Or manually:

.. code-block:: bash

    pip install pytest pytest-cov mypy ruff

Verification
-----------

To verify the installation, you can run:

.. code-block:: python

    import xerparser_dev
    print(xerparser_dev.__version__)