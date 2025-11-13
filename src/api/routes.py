"""
API routes for Task Manager
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from src.models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority, PaginatedResponse, PaginationMetadata
from src.database import db

router = APIRouter()


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """Create a new task"""
    return db.create_task(task)


@router.get("/tasks", response_model=PaginatedResponse[Task])
async def get_tasks(
    skip: int = Query(0, description="Number of tasks to skip"),
    limit: int = Query(100, description="Maximum number of tasks to return"),
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by task priority")
):
    """Get all tasks with optional filtering by status and priority, with pagination"""
    # Get all tasks from database with pagination
    tasks = db.get_all_tasks(skip=skip, limit=limit)

    # Apply filters
    filtered_tasks = [
        task for task in tasks
        if (status is None or task.status == status)
        and (priority is None or task.priority == priority)
    ]

    # Get total count
    total = db.count_tasks()

    # Create pagination metadata
    metadata = PaginationMetadata(
        total=total,
        skip=skip,
        limit=limit,
        has_next=skip + limit < total,
        has_prev=skip > 0
    )

    return PaginatedResponse(items=filtered_tasks, metadata=metadata)


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
