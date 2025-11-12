# Task Manager API

A simple REST API for managing tasks and todos, built with FastAPI.

## Features

- Create, read, update, and delete tasks
- Task priorities (low, medium, high)
- Task statuses (todo, in_progress, completed)
- In-memory database (no external dependencies)
- Full test coverage

## Project Structure

```
task-manager-api/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── src/
│   ├── models.py       # Pydantic data models
│   ├── database.py     # In-memory database
│   ├── utils.py        # Utility functions
│   └── api/
│       └── routes.py   # API endpoints
└── tests/
    └── test_api.py     # API tests
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## API Endpoints

### Health Check
- `GET /` - Health check endpoint

### Tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task

## Example Usage

### Create a Task
```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "status": "todo",
    "priority": "high"
  }'
```

### Get All Tasks
```bash
curl "http://localhost:8000/api/tasks"
```

### Update a Task
```bash
curl -X PUT "http://localhost:8000/api/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

## Running Tests

```bash
pytest tests/
```

For detailed test output:
```bash
pytest -v tests/
```

## Development Roadmap

- [ ] Add task filtering by status and priority
- [ ] Add task search functionality
- [ ] Add user authentication
- [ ] Add task categories/tags
- [ ] Add due dates and reminders
- [ ] Persist data to SQLite/PostgreSQL

## License

MIT
