import pytest

from xerparser.reader import Reader


def test_reader_initialization(sample_xer_path):
    """Test the initialization of the Reader class"""
    reader = Reader(sample_xer_path)
    assert reader is not None
    assert reader.file == sample_xer_path


def test_projects_property(sample_xer):
    """Test that the projects property returns the correct projects"""
    projects = sample_xer.projects
    assert projects is not None
    # Add more specific assertions based on your sample.xer content


def test_activities_property(sample_xer):
    """Test that the activities property returns the correct activities"""
    activities = sample_xer.activities
    assert activities is not None
    # Add more specific assertions based on your sample.xer content


def test_wbss_property(sample_xer):
    """Test that the wbss property returns the correct WBS elements"""
    wbss = sample_xer.wbss
    assert wbss is not None
    # Add more specific assertions based on your sample.xer content


def test_relations_property(sample_xer):
    """Test that the relations property returns the correct relationships"""
    relations = sample_xer.relations
    assert relations is not None
    # Add more specific assertions based on your sample.xer content
