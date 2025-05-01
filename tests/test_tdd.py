import pytest
from src.tasks import *
from datetime import datetime, timedelta

@pytest.fixture
def sample_tasks():
    todays_date = datetime.now().date()
    return [
        {
            "id": 1,
            "title": "Old Task",
            "priority": "Low",
            "due_date": (todays_date - timedelta(days=2)).strftime("%Y-%m-%d")
        },
        {
            "id": 2,
            "title": "Today's Task",
            "priority": "High",
            "due_date": todays_date.strftime("%Y-%m-%d")
        },
        {
            "id": 3,
            "title": "New Upcoming Task",
            "priority": "Medium",
            "due_date": (todays_date + timedelta(days=2)).strftime("%Y-%m-%d"),
        },
        {
            "id": 4,
            "title": "Upcoming Exam",
            "priority": "High",
            "due_date": (todays_date + timedelta(days=30)).strftime("%Y-%m-%d"),
        },
        {
            "id": 5,
            "title": "Upcoming Exam 2",
            "priority": "Low",
            "due_date": (todays_date + timedelta(days=31)).strftime("%Y-%m-%d"),
        },
    ]

def test_sort_tasks_by_due_date_upcoming(sample_tasks):
    by_upcoming = sort_tasks_by_due_date_upcoming(sample_tasks.copy())
    todays_date = datetime.now().date().strftime("%Y-%m-%d")
    max_day = datetime.max.date().strftime("%Y-%m-%d")
    assert all(task["due_date"] >= todays_date for task in by_upcoming)
    for i in range(len(by_upcoming)):
        earlier_task = by_upcoming[i]["due_date"]
        later_task = by_upcoming[i + 1]["due_date"] if i + 1 < len(by_upcoming) else max_day
        assert earlier_task <= later_task


def test_sort_tasks_by_title(sample_tasks):
    #TODO
    by_title = sort_tasks_by_title(sample_tasks.copy())
    assert by_title[0] == sample_tasks[2]
    assert by_title[1] == sample_tasks[0]
    assert by_title[2] == sample_tasks[1]
    assert by_title[3] == sample_tasks[3]
    assert by_title[4] == sample_tasks[4]



def test_sort_tasks_by_high_priority(sample_tasks):
    #TODO
    by_priority = sort_tasks_by_high_priority(sample_tasks.copy())

    high_priority = [sample_tasks[1], sample_tasks[3]]
    medium_priority = [sample_tasks[2]]
    low_priority = [sample_tasks[0], sample_tasks[4]]

    guess_high = [by_priority[0], by_priority[1]]
    guess_medium = [by_priority[2]]
    guess_low = [by_priority[3], by_priority[4]]

    assert guess_high == high_priority or guess_high == high_priority[::-1]
    assert guess_medium == medium_priority
    assert guess_low == low_priority or guess_low == low_priority[::-1]