Feature: Task List Management

  Scenario: Adding a new task
    Given the task list is empty
    When I add a task with title "Finish Unit Testing" and description "Write out BDD and TDD unit tests." and priority "High" and category "School"
    Then the task list contains exactly 1 task
    And the task titled "Finish Unit Testing" has description "Write out BDD and TDD unit tests."
    And the task titled "Finish Unit Testing" has priority "High"
    And the task titled "Finish Unit Testing" has category "School"
    And the task titled "Finish Unit Testing" is not marked as complete
    And the task titled "Finish Unit Testing" has ID 1

  Scenario: Generating a unique ID for a task
    Given the task list is empty
    And I add a task (with title "Finish Unit Testing" and ID 1) and another task (with title "Prepare Lunch" and ID 4) and another task (with title "Astronomy Homework 10" and ID 2)
    When I add a new task with title "Brew Coffee for Work" and generate a unique ID for it
    Then the task titled "Brew Coffee for Work" has ID 5

  Scenario: Marking a task as complete
    Given the task list contains a task with title "Astronomy Homework 10"
    When I mark the task titled "Astronomy Homework 10" as complete
    Then the task titled "Astronomy Homework 10" is marked as complete

  Scenario: Searching for a task
    Given the task list contains a task with title "Prepare Lunch" and description "Decide what food you'll make to bring to work tomorrow."
    When I search tasks using the query "food"
    Then the search results contain a task titled "Prepare Lunch"

  Scenario: Filtering tasks by category
    Given the task list contains a task (with title "Finish Unit Testing" and category "School") and another task (with title "Prepare Lunch" and category "Personal") and another task (with title "Astronomy Homework 10" and category "School")
    When I filter tasks using the category "School"
    Then only tasks titled "Finish Unit Testing" and "Astronomy Homework 10" are visible