import pytest
from src.tasks import search_tasks

@pytest.mark.parametrize("term,expected_matches", [
    ("coffee", 1),
    ("Food", 1),
    ("work", 2),
    ("fee", 1),
    ("fee for", 0),
    ("description", 0)
])
def test_search_advanced(term, expected_matches):
    task1 = {"id": 1, "title": "Brew Coffee for Work", "description": "Brew some coffee for tomorrow morning before heading off."}
    task2 = {"id": 2, "title": "Prepare Lunch", "description": "Decide what food you'll make to bring to work tomorrow."}
    task3 = {"id": 3, "title": "Test", "description": "Fee fie foe fum for sample text."}
    tasks = [task1, task2, task3]
    filtered_tasks = search_tasks(tasks, term)
    matches = len(filtered_tasks)
    assert matches == expected_matches