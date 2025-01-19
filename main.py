from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db import SessionLocal, init_db, store_operation_result

# Initialize FastAPI
app = FastAPI()

# Initialize the database (create tables)
init_db()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI route to perform calculations and store the result
@app.get("/{operation}")
def calculate(num1: float, num2: float, operation: str, db: Session = Depends(get_db)):
    if operation == "sum":
        result = num1 + num2
    elif operation == "sub":
        result = num1 - num2
    elif operation == "mul":
        result = num1 * num2
    elif operation == "Div":
        if num2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed")
        result = num1 / num2
    else:
        raise HTTPException(status_code=404, detail="Operation not found")

    # Store the result in the database
    operation_record = store_operation_result(db, operation, num1, num2, result)
    return {
        "id": operation_record.id,
        "operation": operation,
        "num1": num1,
        "num2": num2,
        "result": result,
    }
