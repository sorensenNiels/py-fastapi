"""
This is a simple example of using FastAPI with Jinja2
"""

from fastapi import Depends, FastAPI, Form, Request, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()


def get_db():
    """This function initializes and returns a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    """Get all available Todos"""
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse(
        "base.html", {"request": request, "todo_list": todos}
    )


@app.post("/add")
def add(_request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    """Add a Todo"""
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/update/{todo_id}")
def update(_request: Request, todo_id: int, db: Session = Depends(get_db)):
    """Update a Todo"""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.get("/delete/{todo_id}")
def delete(_request: Request, todo_id: int, db: Session = Depends(get_db)):
    """Delete a Todo"""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
