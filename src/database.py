"""
Simple in-memory database for Task Manager API
"""
import re
from datetime import datetime
from typing import Dict, List, Optional
from src.models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority


class TaskDatabase:
    """In-memory task database"""

    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task"""
        now = datetime.utcnow()
        task = Task(
            id=self.next_id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            created_at=now,
            updated_at=now
        )
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return list(self.tasks.values())

    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description"""
        # Sanitize input by removing non-alphanumeric characters except spaces
        sanitized_query = re.sub(r'[^\w\s]', '', query).lower().strip()

        # Return empty list if sanitized query is empty to avoid matching all tasks
        if not sanitized_query:
            return []

        results = []
        for task in self.tasks.values():
            title_lower = task.title.lower()
            description_lower = task.description.lower() if task.description else ""

            if sanitized_query in title_lower or sanitized_query in description_lower:
                results.append(task)
        return results

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update an existing task"""
        task = self.tasks.get(task_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False


# Global database instance
db = TaskDatabase()
