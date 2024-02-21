from uuid import UUID
from fastapi import FastAPI, status, HTTPException


app = FastAPI()


class Student:
   def __init__(self, name: str, age: int, sex: str, height: float): 
        self.id = None
        self.name = name
        self.age = age
        self.sex = sex
        self.height = height




students = []

@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "Hello, from the student API!"}


@app.get("/students", status_code=status.HTTP_200_OK)
async def get_all_students():
    return students


@app.get("/student/{id}", status_code=status.HTTP_200_OK)
async def get_a_student(id: str):  
    for student in students:
        if student.id == id:
            return student.__dict__
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

@app.get("/students/filtered", status_code=status.HTTP_200_OK)
async def get_many_students_fiter_age(min_age: int, max_age: int, limit: int = None, offset: int = 0):


    filtered_students = students


    if min_age is not None and max_age is not None:  
        filtered_students = [student for student in students if min_age <= student.age <= max_age]

    if limit is not None:
        if limit > len(students):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit cannot exceed the total number of students")
        filtered_students = filtered_students[offset:offset + limit]
    else:
        filtered_students = filtered_students[offset:]
    return filtered_students


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(name: str, age: int, sex: str, height: float):
    sex_lower = sex.lower()
    if sex_lower not in ["male", "female"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sex must be either'male' or 'female'",
        )
    new_id = str(UUID(int=len(students) + 1))
    new_student = Student(name=name, age=age, sex=sex_lower, height=height)
    new_student.id = new_id 
    students.append(new_student)
    return {"message": "Student successfully created.", "data":new_student.__dict__}


@app.get("/students/sex", status_code=status.HTTP_200_OK)
async def get_students_by_sex(sex: str):
    sex_lower = sex.lower()
    if sex_lower not in ["male", "female"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sex must be either'male' or 'female'",
        )
    return [student.__dict__ for student in students if student.sex == sex_lower]


@app.put("/students/{id}", status_code=status.HTTP_200_OK)
async def update_students(id: str, name: str, age: int, sex: str, height: float):
    sex_lower = sex.lower()
    if sex_lower not in ["male", "female"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sex must be either a 'male' or 'female'",
        )
    for student in students:
        if student.id == id:
            student.name = name
            student.age = age
            student.sex = sex_lower
            student.height = height
            return {"message": "Student successfully updated.", "data":student.__dict__}
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )


@app.delete("/students/{id}", status_code=status.HTTP_200_OK)
async def delete_student(id: str):
    for student in students:
        if student.id == id:
            students.remove(student)
            return {"message": "Student successfully deleted."}
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )