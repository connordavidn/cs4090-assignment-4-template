import pytest
import os
from src.tasks import DEFAULT_TASKS_FILE, save_tasks, load_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, search_tasks

def test_save_load_tasks(tmp_path):
    file = tmp_path / DEFAULT_TASKS_FILE
    task1 = {"id": 1, "title": "Task 1", "category": "Testing", "completed": False}
    task2 = {"id": 2, "title": "Task 2", "category": "Assignment", "completed": False}
    tasks = [task1, task2]
    save_tasks(tasks, file)
    loaded_tasks = load_tasks(file)
    assert loaded_tasks == tasks

def test_load_nonexistent_task_file(tmp_path):
    file = tmp_path / f"__nonexistent__{DEFAULT_TASKS_FILE}"
    loaded_tasks = load_tasks(file)
    assert loaded_tasks == []

def test_load_corrupted_JSON(tmp_path):
    file = tmp_path / f"__nonexistent__{DEFAULT_TASKS_FILE}"
    file.write_text("This is invalid JSON data.")
    loaded_tasks = load_tasks(file)
    assert loaded_tasks == []

def test_generate_initial_id():
    tasks = []
    first_id = generate_unique_id(tasks)
    assert first_id == 1

def test_generate_ids():
    task1 = {"id": 1, "title": "Test"}
    task4 = {"id": 4, "title": "Test"}
    task2 = {"id": 2, "title": "Test"}
    tasks = [task1, task4, task2]
    next_id = generate_unique_id(tasks)
    assert next_id == 5

def test_filter_tasks_by_priority():
    task1 = {"id": 1, "title": "Test", "priority": "Medium"}
    task2 = {"id": 2, "title": "Test", "priority": "High"}
    task3 = {"id": 3, "title": "Test", "priority": "Low"}
    task4 = {"id": 4, "title": "Test", "priority": "High"}
    tasks = [task1, task2, task3, task4]
    filtered_tasks = filter_tasks_by_priority(tasks, "High")
    high_priority = [task2, task4]
    assert filtered_tasks == high_priority

def test_filter_tasks_by_priority_unmatched():
    task1 = {"id": 1, "title": "Test", "priority": "Medium"}
    tasks = [task1]
    filtered_tasks = filter_tasks_by_priority(tasks, "High")
    assert filtered_tasks == []

def test_filter_tasks_by_category():
    task1 = {"id": 1, "title": "Test", "category": "Work"}
    task2 = {"id": 2, "title": "Test", "category": "Personal"}
    task3 = {"id": 3, "title": "Test", "category": "Work"}
    task4 = {"id": 4, "title": "Test", "category": "Personal"}
    tasks = [task1, task2, task3, task4]
    filtered_tasks = filter_tasks_by_category(tasks, "Work")
    work_category = [task1, task3]
    assert filtered_tasks == work_category

def test_filter_tasks_by_category_unmatched():
    task1 = {"id": 1, "title": "Test", "category": "Work"}
    tasks = [task1]
    filtered_tasks = filter_tasks_by_category(tasks, "School")
    assert filtered_tasks == []

def test_filter_tasks_by_completion():
    task1 = {"id": 1, "title": "Test", "completed": True}
    task2 = {"id": 2, "title": "Test", "completed": False}
    task3 = {"id": 3, "title": "Test", "completed": True}
    tasks = [task1, task2, task3]
    filtered_tasks = filter_tasks_by_completion(tasks, True)
    completed = [task1, task3]
    assert filtered_tasks == completed

def test_filter_tasks_by_completion_unmatched():
    task2 = {"id": 2, "title": "Test", "completed": False}
    tasks = [task2]
    filtered_tasks = filter_tasks_by_completion(tasks, True)
    assert filtered_tasks == []

def test_search_titles_and_descriptions():
    task1 = {"id": 1, "title": "Brew Coffee for Work", "description": "Brew some coffee for tomorrow morning before heading off."}
    task2 = {"id": 2, "title": "Prepare Lunch", "description": "Decide what food you'll make to bring to work tomorrow."}
    task3 = {"id": 3, "title": "Test", "description": "Sample text."}
    tasks = [task1, task2, task3]
    filtered_tasks = search_tasks(tasks, "work")
    work = [task1, task2]
    assert filtered_tasks == work

def test_search_tasks_unmatched():
    task1 = {"id": 1, "title": "Test", "description": "Sample text."}
    tasks = [task1]
    filtered_tasks = search_tasks(tasks, "work")
    assert filtered_tasks == []