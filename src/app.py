import streamlit as st
import pandas as pd
from datetime import datetime
from tasks import *
import subprocess
from os import path

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title and datetime.now().date() <= task_due_date:
            new_task = {
                "id": generate_unique_id(tasks),
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with col3:
        sorting_option = st.selectbox("Sorting:", ["Default", "Upcoming Due Date", "Title", "Highest Priority"])
    
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        completed_tasks = filter_tasks_by_completion(filtered_tasks, True)
        filtered_tasks = [task for task in filtered_tasks if not task in completed_tasks]
    if sorting_option == "Upcoming Due Date":
        filtered_tasks = sort_tasks_by_due_date_upcoming(filtered_tasks)
    if sorting_option == "Title":
        filtered_tasks = sort_tasks_by_title(filtered_tasks)
    if sorting_option == "Highest Priority":
        filtered_tasks = sort_tasks_by_high_priority(filtered_tasks)
    
    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

    st.sidebar.header("Testing & Analysis")
    directory = path.dirname(path.dirname(path.abspath(__file__)))
    directory = directory if directory else "../"
    print(directory)

    if st.sidebar.button("Unit Tests"):
        with st.spinner("Running unit tests..."):
            result = subprocess.run(
                [".venv/bin/python", "-m", "pytest", "tests/test_basic.py", "-v"],
                cwd=directory, capture_output=True, text=True
            )
            st.code(result.stdout)

    if st.sidebar.button("Parameterized Tests"):
        with st.spinner("Running parameterized tests..."):
            result = subprocess.run(
                [".venv/bin/python", "-m", "pytest", "tests/test_advanced.py", "-v"],
                cwd=directory, capture_output=True, text=True
            )
            st.code(result.stdout)

    if st.sidebar.button("Full Coverage Report"):
        with st.spinner("Running all tests and generating coverage report..."):
            result = subprocess.run(
                [".venv/bin/python", "-m", "pytest", "tests/", "--cov=src.tasks", "--cov-report=term-missing", "--cov-report=html"],
                cwd=directory, capture_output=True, text=True
            )
            st.code(result.stdout)

    if st.sidebar.button("TDD Tests"):
        with st.spinner("Running TDD tests..."):
            result = subprocess.run(
                [".venv/bin/python", "-m", "pytest", "tests/test_tdd.py", "-v"],
                cwd=directory, capture_output=True, text=True
            )
            st.code(result.stdout)

    if st.sidebar.button("BDD Tests"):
        with st.spinner("Running BDD tests..."):
            result = subprocess.run(
                [".venv/bin/python", "-m", "pytest", "tests/feature", "-v"],
                cwd=directory, capture_output=True, text=True
            )
            st.code(result.stdout)

if __name__ == "__main__":
    main()