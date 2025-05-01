from pytest_bdd import scenarios, given, when, then, parsers
from src.tasks import load_tasks, save_tasks, generate_unique_id, search_tasks, filter_tasks_by_category

scenarios("../add_task.feature")

tasks = []
search_results = []
filtered_tasks_by_category = []

@given("the task list is empty")
def clear_tasks():
    tasks.clear()

@when(parsers.parse('I add a task with title "{title}" and description "{description}" and priority "{priority}" and category "{category}"'))
def add_task(title, description, priority, category):
    task = {
        "id": generate_unique_id(tasks),
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "completed": False
    }
    tasks.append(task)

@then(parsers.parse("the task list contains exactly 1 task"))
def check_for_one_task():
    assert len(tasks) == 1

@then(parsers.parse('the task titled "{title}" has description "{description}"'))
def check_for_description(title, description):
    filtered_tasks = [task for task in tasks if task["title"] == title]
    task = filtered_tasks[-1]
    assert task["description"] == description

@then(parsers.parse('the task titled "{title}" has priority "{priority}"'))
def check_for_priority(title, priority):
    filtered_tasks = [task for task in tasks if task["title"] == title]
    task = filtered_tasks[-1]
    assert task["priority"] == priority

@then(parsers.parse('the task titled "{title}" has category "{category}"'))
def check_for_category(title, category):
    filtered_tasks = [task for task in tasks if task["title"] == title]
    task = filtered_tasks[-1]
    assert task["category"] == category

@then(parsers.parse('the task titled "{title}" is not marked as complete'))
def check_for_not_complete(title):
    filtered_tasks = [task for task in tasks if task["title"] == title]
    task = filtered_tasks[-1]
    assert task["completed"] is False


@then(parsers.parse('the task titled "{title}" has ID 1'))
def check_for_id_one(title):
    filtered_tasks = [task for task in tasks if task["title"] == title]
    task = filtered_tasks[-1]
    assert task["id"] == "1"


@given(parsers.parse('I add a task (with title "{title1}" and ID {id1}) and another task (with title "{title2}" and ID {id2}) and another task (with title "{title3}" and ID {id3})'))
def add_three_tasks_with_ids(title1, id1, title2, id2, title3, id3):
    tasks.append({"id": int(id1), "title": title1})
    tasks.append({"id": int(id2), "title": title2})
    tasks.append({"id": int(id3), "title": title3})

@when(parsers.parse('I add a new task with title "{title}" and generate a unique ID for it'))
def add_new_task(title):
    tasks.append({"id": generate_unique_id(tasks), "title": title})

@then(parsers.parse('the task titled "{title}" has ID {id1}'))
def check_for_id(title, id1):
    filtered_tasks = [task for task in tasks if task["title"] == title]
    task = filtered_tasks[-1]
    assert task["id"] == int(id1)


@given(parsers.parse('the task list contains a task with title "{title}"'))
def add_one_task(title):
    tasks.append({"id": generate_unique_id(tasks), "title": title})

@when(parsers.parse('I mark the task titled "{title}" as complete'))
def mark_task_as_complete(title):
    filtered_tasks = [task for task in tasks if task["title"] == title]
    task = filtered_tasks[-1]
    task["completed"] = True

@then(parsers.parse('the task titled "{title}" is marked as complete'))
def check_for_marked_task_as_complete(title):
    filtered_tasks = [task for task in tasks if task["title"] == title]
    task = filtered_tasks[-1]
    assert task["completed"] is True


@given(parsers.parse('the task list contains a task with title "{title}" and description "{description}"'))
def add_one_task_with_description(title, description):
    tasks.append({
        "id": generate_unique_id(tasks),
        "title": title,
        "description": description
    })

@when(parsers.parse('I search tasks using the query "{query}"'))
def search_for_task(query):
    global search_results
    search_results = search_tasks(tasks, query)

@then(parsers.parse('the search results contain a task titled "{title}"'))
def check_for_title(title):
    assert [task for task in search_results if task["title"] == title]


@given(parsers.parse('the task list contains a task (with title "{title1}" and category "{category1}") and another task (with title "{title2}" and category "{category2}") and another task (with title "{title3}" and category "{category3}")'))
def add_three_tasks_with_categories(title1, category1, title2, category2, title3, category3):
    tasks.append({
        "id": generate_unique_id(tasks),
        "title": title1,
        "category": category1
    })
    tasks.append({
        "id": generate_unique_id(tasks),
        "title": title2,
        "category": category2
    })
    tasks.append({
        "id": generate_unique_id(tasks),
        "title": title3,
        "category": category3
    })

@when(parsers.parse('I filter tasks using the category "{category}"'))
def filter_by_category(category):
    global filtered_tasks_by_category
    filtered_tasks_by_category = filter_tasks_by_category(tasks, category)

@then(parsers.parse('only tasks titled "{title1}" and "{title2}" are visible'))
def check_for_two_titles(title1, title2):
    tasks_other_than_desired = [not(task["title"] == title1) and not(task["title"] == title2) for task in filtered_tasks_by_category]
    assert not any(tasks_other_than_desired)
    assert any([task["title"] == title1 for task in filtered_tasks_by_category])
    assert any([task["title"] == title2 for task in filtered_tasks_by_category])