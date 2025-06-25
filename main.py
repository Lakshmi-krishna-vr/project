from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import uuid

app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "obsidian"}
    }
)

# In-memory storage
students: Dict[str, dict] = {}
classes: Dict[str, dict] = {}
registrations: Dict[str, List[str]] = {}

# Pydantic models
class Student(BaseModel):
    name: str
    email: str

class Class(BaseModel):
    title: str
    description: str

# 1. Read Students
@app.get("/students")
def read_students():
    return students

# 2. Create Student
@app.post("/students")
def create_student(student: Student):
    student_id = str(uuid.uuid4())
    students[student_id] = student.dict()
    return {"id": student_id, "message": "Student added"}

# 3. Update Student
@app.put("/students/{student_id}")
def update_student(student_id: str, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = student.dict()
    return {"message": "Student updated"}

# 4. Delete Student
@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted"}

# 5. Get Classes
@app.get("/classes")
def get_classes():
    return classes

# 6. Create Class
@app.post("/classes")
def create_class(new_class: Class):
    class_id = str(uuid.uuid4())
    classes[class_id] = new_class.dict()
    return {"id": class_id, "message": "Class added"}

# 7. Register Student to Class
@app.post("/classes/{class_id}/students/{student_id}")
def register_student(class_id: str, student_id: str):
    if class_id not in classes or student_id not in students:
        raise HTTPException(status_code=404, detail="Invalid student or class ID")
    registrations.setdefault(class_id, []).append(student_id)
    return {"message": "Student registered to class"}

# 8. List Students in Class
@app.get("/classes/{class_id}/students")
def list_students_in_class(class_id: str):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    student_ids = registrations.get(class_id, [])
    return [students[sid] for sid in student_ids if sid in students]

# 9. Delete Class
@app.delete("/classes/{class_id}")
def delete_class(class_id: str):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    del classes[class_id]
    return {"message": "Class deleted"}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
