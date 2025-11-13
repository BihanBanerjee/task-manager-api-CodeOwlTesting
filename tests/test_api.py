"""
Test cases for Task Manager API
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from src.database import db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test"""
    db.tasks.clear()
    db.next_id = 1
    yield


def test_root_endpoint():
    """Test the root health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task():
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "todo",
        "priority": "high"
    }
    response = client.post("/api/tasks", json=task_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"
    assert response.json()["id"] == 1


def test_get_all_tasks():
    """Test getting all tasks"""
    # Create a task first
    client.post("/api/tasks", json={"title": "Task 1"})
    client.post("/api/tasks", json={"title": "Task 2"})

    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["metadata"]["total"] == 2


def test_get_task_by_id():
    """Test getting a specific task"""
    # Create a task first
    create_response = client.post("/api/tasks", json={"title": "Test Task"})
    task_id = create_response.json()["id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_get_nonexistent_task():
    """Test getting a task that doesn't exist"""
    response = client.get("/api/tasks/999")
    assert response.status_code == 404


def test_update_task():
    """Test updating a task"""
    # Create a task first
    create_response = client.post("/api/tasks", json={"title": "Original Title"})
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {"title": "Updated Title", "status": "completed"}
    response = client.put(f"/api/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["status"] == "completed"


def test_delete_task():
    """Test deleting a task"""
    # Create a task first
    create_response = client.post("/api/tasks", json={"title": "To Delete"})
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404


def test_pagination_basic():
    """Test basic pagination"""
    # Create 5 tasks
    for i in range(5):
        client.post("/api/tasks", json={"title": f"Task {i+1}"})

    # Get first 2 tasks
    response = client.get("/api/tasks?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["metadata"]["total"] == 5
    assert data["metadata"]["skip"] == 0
    assert data["metadata"]["limit"] == 2
    assert data["metadata"]["has_next"] is True
    assert data["metadata"]["has_prev"] is False


def test_pagination_skip():
    """Test pagination with skip parameter"""
    # Create 5 tasks
    for i in range(5):
        client.post("/api/tasks", json={"title": f"Task {i+1}"})

    # Skip first 2 tasks
    response = client.get("/api/tasks?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["metadata"]["has_next"] is True
    assert data["metadata"]["has_prev"] is True


def test_pagination_negative_values():
    """Test pagination with negative values"""
    client.post("/api/tasks", json={"title": "Task 1"})

    response = client.get("/api/tasks?skip=-1&limit=-1")
    assert response.status_code == 200
