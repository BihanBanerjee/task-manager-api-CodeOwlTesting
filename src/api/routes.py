"""
API routes for Task Manager
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from src.models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from src.database import db

router = APIRouter()


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """Create a new task"""
    return db.create_task(task)


@router.get("/tasks", response_model=List[Task])
async def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by task priority")
):
    """Get all tasks with optional filtering by status and priority"""
    tasks = db.get_all_tasks()

    if status:
        tasks = [task for task in tasks if task.status == status]

    if priority:
        tasks = [task for task in tasks if task.priority == priority]

    return tasks


@router.get("/tasks/search", response_model=List[Task])
async def search_tasks(q: str = Query(..., min_length=1, max_length=255, description="Search query")):
    """Search tasks by title or description"""
    return db.search_tasks(q)


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    task = db.update_task(task_id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    """Delete a task"""
    success = db.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
