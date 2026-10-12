from fastapi import FastAPI
from models import Task

app = FastAPI()

@app.get("/")
def greet():
    return "Hi"


tasks = [
    Task(id=1,title="Revise Backend concepts", done=False),
    Task(id=2,title="Complete Homework", done=False),
    Task(id=3,title="Pack things", done=True)
]

@app.get("/tasks")
def read_tasks():
    return tasks

@app.get("/tasks/{id}")
def read_tasks_by_id(id:int):
    for task in tasks:
        if task.id == id:
            return task
    return "Task not found"

@app.post("/tasks")
def add_task(task: Task):
    tasks.append(task)
    return task