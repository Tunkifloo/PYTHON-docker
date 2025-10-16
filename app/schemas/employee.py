from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class EmployeeBase(BaseModel):
    """Schema base con campos comunes"""
    first_name: str = Field(..., min_length=1, max_length=50, description="Nombre del empleado")
    last_name: str = Field(..., min_length=1, max_length=50, description="Apellido del empleado")
    email: EmailStr = Field(..., description="Email del empleado")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono del empleado")
    position: str = Field(..., min_length=1, max_length=100, description="Cargo del empleado")
    department: str = Field(..., min_length=1, max_length=100, description="Departamento")
    salary: float = Field(..., gt=0, description="Salario del empleado")
    hire_date: datetime = Field(..., description="Fecha de contratación")


class EmployeeCreate(EmployeeBase):
    """Schema para crear un empleado"""
    pass


class EmployeeUpdate(BaseModel):
    """Schema para actualizar un empleado (todos los campos opcionales)"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    salary: Optional[float] = Field(None, gt=0)
    hire_date: Optional[datetime] = None


class EmployeeResponse(EmployeeBase):
    """Schema para respuesta (incluye campos generados por la BD)"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EmployeeListResponse(BaseModel):
    """Schema para lista de empleados con paginación"""
    total: int
    employees: list[EmployeeResponse]
    page: int
    page_size: int