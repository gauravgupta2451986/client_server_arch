from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection string for MySQL
DATABASE_URL = "mysql+mysqlconnector://fastapi_user:password@localhost/operations_db"

# Create the database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Define the table schema for storing operation results
class OperationResult(Base):
    __tablename__ = "operation_results"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    num1 = Column(Float, nullable=False)
    num2 = Column(Float, nullable=False)
    result = Column(Float, nullable=False)

# Function to initialize the database and create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Function to store an operation result in the database
def store_operation_result(db, operation, num1, num2, result):
    operation_result = OperationResult(operation=operation, num1=num1, num2=num2, result=result)
    db.add(operation_result)
    db.commit()
    db.refresh(operation_result)
    return operation_result
