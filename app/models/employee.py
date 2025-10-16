from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    position = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    hire_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Employee(id={self.id}, name={self.first_name} {self.last_name}, position={self.position})>"