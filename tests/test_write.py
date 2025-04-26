import os

import pytest

from xerparser.reader import Reader
from xerparser.write import writeXER


def test_write_xer(sample_xer, fixtures_dir):
    """Test writing an XER file"""
    output_file = os.path.join(fixtures_dir, "output_test.xer")

    # Write the XER file
    writeXER(sample_xer, output_file)

    # Check that the file was created
    assert os.path.exists(output_file)

    # Read the written file to verify structure
    new_reader = Reader(output_file)

    # Verify key components were preserved - just check that we can read the file back in
    assert new_reader is not None
    assert hasattr(new_reader, "projects")

    # Clean up the test file
    os.remove(output_file)


def test_reader_write_method(sample_xer, fixtures_dir):
    """Test the write method of the Reader class"""
    output_file = os.path.join(fixtures_dir, "output_reader_test.xer")

    # Use the Reader's write method
    sample_xer.write(output_file)

    # Check that the file was created
    assert os.path.exists(output_file)

    # Clean up the test file
    os.remove(output_file)
