import pytest
from pydantic import ValidationError
from datetime import datetime
import os

from xer_parser.reader import Reader
from xer_parser.model.classes.project import Project
from xer_parser.model.classes.task import Task
from xer_parser.model.classes.wbs import WBS
from xer_parser.model.classes.taskpred import TaskPred
from xer_parser.model.classes.calendar import Calendar # Assuming for task.calendar check
from xer_parser.model.projects import Projects
from xer_parser.model.tasks import Tasks
from xer_parser.model.wbss import WBSs
from xer_parser.model.predecessors import Predecessors


def test_reader_initialization(sample_xer_path):
    """Test the initialization of the Reader class and main data object."""
    reader = Reader(sample_xer_path)
    assert reader is not None
    assert reader.file == sample_xer_path
    assert reader._data is not None
    assert reader._data._xer_file_path == sample_xer_path


def test_projects_collection(sample_xer):
    """Test that the projects property returns a Projects collection of Project models."""
    projects_collection = sample_xer.projects
    assert isinstance(projects_collection, Projects)
    if projects_collection.count > 0:
        project = list(projects_collection)[0]
        assert isinstance(project, Project)
        assert isinstance(project.proj_id, int)
        assert isinstance(project.proj_short_name, (str, type(None)))
        assert isinstance(project.add_date, (datetime, type(None)))
        # Example: Check if data context is passed (if project has properties needing it)
        # assert project.data is sample_xer._data # This might be true if collections pass it down


def test_tasks_collection(sample_xer):
    """Test that the activities property returns a Tasks collection of Task models."""
    tasks_collection = sample_xer.activities # reader.activities maps to reader._data.tasks
    assert isinstance(tasks_collection, Tasks)
    if tasks_collection.count > 0:
        task = list(tasks_collection)[0]
        assert isinstance(task, Task)
        assert isinstance(task.task_id, int)
        assert isinstance(task.task_code, (str, type(None)))
        assert isinstance(task.target_drtn_hr_cnt, (float, type(None)))
        assert isinstance(task.status_code, (str, type(None)))
        assert isinstance(task.act_start_date, (datetime, type(None)))
        assert isinstance(task.act_end_date, (datetime, type(None)))
        assert isinstance(task.early_start_date, (datetime, type(None)))
        assert isinstance(task.early_end_date, (datetime, type(None)))
        assert isinstance(task.target_start_date, (datetime, type(None)))
        assert isinstance(task.target_end_date, (datetime, type(None)))
        
        # Check if related objects are accessible and of correct type (if loaded)
        if task.calendar: # Task.calendar property
             assert isinstance(task.calendar, Calendar)
        # Check if task.data points to the main Data object
        assert task.data is sample_xer._data
        # Check task.predecessors and task.successors (lists of TaskPred)
        assert isinstance(task.predecessors, list)
        if task.predecessors:
            assert isinstance(task.predecessors[0], TaskPred)
        assert isinstance(task.successors, list)
        if task.successors:
            assert isinstance(task.successors[0], TaskPred)


def test_wbss_collection(sample_xer):
    """Test that the wbss property returns a WBSs collection of WBS models."""
    wbss_collection = sample_xer.wbss
    assert isinstance(wbss_collection, WBSs)
    if wbss_collection.count > 0:
        wbs_item = list(wbss_collection)[0]
        assert isinstance(wbs_item, WBS)
        assert isinstance(wbs_item.wbs_id, int)
        assert isinstance(wbs_item.wbs_name, (str, type(None)))
        # Check if wbs_item.data points to the main Data object
        assert wbs_item.data is sample_xer._data


def test_relations_collection(sample_xer):
    """Test that the relations property returns a Predecessors collection of TaskPred models."""
    relations_collection = sample_xer.relations
    assert isinstance(relations_collection, Predecessors)
    if relations_collection.count > 0:
        relation = list(relations_collection)[0]
        assert isinstance(relation, TaskPred)
        assert isinstance(relation.task_pred_id, int)
        assert isinstance(relation.pred_task_id, (int, type(None)))
        assert isinstance(relation.task_id, (int, type(None)))
        assert isinstance(relation.pred_type, (str, type(None)))
        assert isinstance(relation.lag_hr_cnt, (float, type(None)))
        # Check if relation.data points to the main Data object
        assert relation.data is sample_xer._data


def test_pydantic_validation_error_on_malformed_xer(tmp_path):
    """Test that Pydantic ValidationError is raised for malformed XER data."""
    malformed_content = """%T\tPROJECT
%F\tproj_id\tproj_short_name\tadd_date
%R\tnot_an_int\tTestProject\t2023-01-01 00:00
%E
"""
    malformed_xer_file = tmp_path / "malformed.xer"
    malformed_xer_file.write_text(malformed_content)

    with pytest.raises(ValidationError) as excinfo:
        Reader(str(malformed_xer_file))
    
    # Check if the error messages contain relevant information (optional)
    # Example: Check that the error is about 'proj_id' and its type
    assert "proj_id" in str(excinfo.value).lower()
    assert "int" in str(excinfo.value).lower()

    malformed_content_task = """%T\tTASK
%F\ttask_id\ttask_code\ttarget_drtn_hr_cnt
%R\t1\tA100\tnot_a_float
%E
"""
    malformed_xer_file_task = tmp_path / "malformed_task.xer"
    malformed_xer_file_task.write_text(malformed_content_task)
    with pytest.raises(ValidationError):
        Reader(str(malformed_xer_file_task))

def test_task_specific_attributes(sample_xer):
    """Test specific attributes and relationships of a Task model."""
    tasks_collection = sample_xer.activities
    if tasks_collection.count > 0:
        task = list(tasks_collection)[0] # Get a sample task
        # Assuming Task model has 'predecessors' and 'resources' properties
        # that return lists of related Pydantic models
        assert isinstance(task.predecessors, list)
        if len(task.predecessors) > 0:
            assert isinstance(task.predecessors[0], TaskPred)
            assert task.predecessors[0].data is sample_xer._data # Check context propagation

        assert isinstance(task.resources, list)
        # TaskRsrc model would need to be imported if we check instance type here
        # For now, just checking it's a list.
        # if len(task.resources) > 0:
        #     from xer_parser.model.classes.taskrsrc import TaskRsrc
        #     assert isinstance(task.resources[0], TaskRsrc)
        #     assert task.resources[0].data is sample_xer._data
        
        # Test calendar property
        if task.calendar: # Assuming task.calendar can be None
            assert isinstance(task.calendar, Calendar)
            assert task.calendar.data is sample_xer._data


def test_empty_xer_file(tmp_path):
    """Test handling of an empty or minimal XER file."""
    empty_content = "%T\tVERSION\n%F\tversion\n%R\t8.0\n%E\n" # Minimal valid XER
    empty_xer_file = tmp_path / "empty.xer"
    empty_xer_file.write_text(empty_content)
    
    reader = Reader(str(empty_xer_file))
    assert reader.projects.count == 0
    assert reader.activities.count == 0

def test_reader_summary_method(sample_xer, caplog):
    """ Test the summary method of the reader """
    import logging
    caplog.set_level(logging.INFO)
    sample_xer.summary() # Call the summary method
    
    # Check if the log messages contain the expected counts
    # These counts depend on the content of sample.xer
    # Example:
    # assert f"Number of activities: {sample_xer.activities.count}" in caplog.text
    # assert f"Number of relationships: {sample_xer.relations.count}" in caplog.text
    # For now, just check if it runs without error
    assert "Number of activities:" in caplog.text
    assert "Number of relationships:" in caplog.text
