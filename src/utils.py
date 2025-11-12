"""
Utility functions for Task Manager API
"""
from datetime import datetime
from typing import List
from src.models import Task, TaskStatus


def filter_tasks_by_status(tasks: List[Task], status: TaskStatus) -> List[Task]:
    """Filter tasks by status"""
    return [task for task in tasks if task.status == status]


def sort_tasks_by_priority(tasks: List[Task], reverse: bool = True) -> List[Task]:
    """Sort tasks by priority (high to low by default)"""
    priority_order = {"high": 3, "medium": 2, "low": 1}
    return sorted(
        tasks,
        key=lambda task: priority_order.get(task.priority.value, 0),
        reverse=reverse
    )


def format_task_summary(task: Task) -> str:
    """Format a task as a summary string"""
    return f"[{task.priority.value.upper()}] {task.title} - {task.status.value}"
