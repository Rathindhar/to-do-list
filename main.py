from fastapi import FastAPI, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import Task, TaskCreate, TaskUpdate
from database import session

app = FastAPI()


# Handle invalid request data with HTTP 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )


# Root endpoint
@app.get("/")
def greet():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}


# In-memory task storage
tasks = [
    Task(id=1, title="Revise Backend concepts", done=False),
    Task(id=2, title="Complete Homework", done=False),
    Task(id=3, title="Pack things", done=True)
]


# Read all tasks
@app.get("/tasks")
def read_tasks():
    db = session()
    db.query()
    return tasks


# Read one task
@app.get("/tasks/{id}")
def read_task_by_id(id: int):
    for task in tasks:
        if task.id == id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )


# Create a task
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def add_task(task: TaskCreate):
    title = task.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    next_id = max((t.id for t in tasks), default=0) + 1

    new_task = Task(
        id=next_id,
        title=title,
        done=False
    )

    tasks.append(new_task)
    return new_task


# Update a task
@app.put("/tasks/{id}")
def update_task(id: int, task: TaskUpdate):
    if task.title is None and task.done is None:
        raise HTTPException(
            status_code=400,
            detail="Provide title or done to update"
        )

    for i, existing_task in enumerate(tasks):
        if existing_task.id == id:
            updated_data = existing_task.model_dump()

            if task.title is not None:
                title = task.title.strip()

                if not title:
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )

                updated_data["title"] = title

            if task.done is not None:
                updated_data["done"] = task.done

            tasks[i] = Task(**updated_data)
            return tasks[i]

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )


# Delete a task
@app.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(id: int):
    for i, task in enumerate(tasks):
        if task.id == id:
            del tasks[i]
            return Response(
                status_code=status.HTTP_204_NO_CONTENT
            )

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )
