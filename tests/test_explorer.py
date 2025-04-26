"""
Test module for the xerparser.tools.explorer module.
"""

import os
import tempfile

import pytest

from xerparser.tools.explorer import XerExplorer, explore_xer_file


class TestXerExplorer:
    """Test class for the XerExplorer functionality."""

    @pytest.fixture
    def sample_xer_path(self):
        """Return the path to a sample XER file."""
        return os.path.join("tests", "fixtures", "sample.xer")

    @pytest.fixture
    def output_file(self):
        """Create a temporary file to store the output."""
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    def test_explorer_initialization(self, sample_xer_path):
        """Test XerExplorer class initialization."""
        explorer = XerExplorer(sample_xer_path)
        assert explorer.xer_path == sample_xer_path
        assert explorer.reader is None
        assert explorer.collection_data == {}

    def test_parse_file(self, sample_xer_path):
        """Test parsing the XER file."""
        explorer = XerExplorer(sample_xer_path)
        result = explorer.parse_file()
        assert result is True
        assert explorer.reader is not None

    def test_collect_data(self, sample_xer_path):
        """Test collecting data from the XER file."""
        explorer = XerExplorer(sample_xer_path)
        explorer.parse_file()
        data = explorer.collect_data()
        assert isinstance(data, dict)
        # At minimum, we expect projects and activities collections in sample.xer
        assert "projects" in data
        assert len(data["projects"]) > 0

    def test_generate_report(self, sample_xer_path, output_file):
        """Test generating a report from the XER file."""
        explorer = XerExplorer(sample_xer_path)
        explorer.parse_file()
        explorer.collect_data()
        result = explorer.generate_report(output_file)
        assert result is True
        assert os.path.exists(output_file)

        # Verify report content
        with open(output_file, "r") as f:
            content = f.read()
            assert "PyP6Xer Exploration Results" in content
            assert "PROJECT SUMMARY" in content
            assert "CALENDAR SUMMARY" in content
            assert "WBS SUMMARY" in content

    def test_explore_xer_file_function(self, sample_xer_path, output_file):
        """Test the explore_xer_file function."""
        result = explore_xer_file(sample_xer_path, output_file)
        assert result is True
        assert os.path.exists(output_file)

        # Verify report content
        with open(output_file, "r") as f:
            content = f.read()
            assert "PyP6Xer Exploration Results" in content

    def test_invalid_file_path(self, output_file):
        """Test handling of invalid file paths."""
        explorer = XerExplorer("non_existent_file.xer")
        result = explorer.parse_file()
        assert result is False
