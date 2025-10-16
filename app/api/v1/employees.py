from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse
)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=EmployeeListResponse)
def get_employees(
        skip: int = Query(0, ge=0, description="Número de registros a saltar"),
        limit: int = Query(100, ge=1, le=100, description="Cantidad de registros a retornar"),
        search: Optional[str] = Query(None, description="Buscar por nombre, email, departamento o posición"),
        db: Session = Depends(get_db)
):
    """
    Obtiene la lista de empleados con paginación y búsqueda opcional.
    """
    repo = EmployeeRepository(db)

    if search:
        employees = repo.search(search, skip=skip, limit=limit)
    else:
        employees = repo.get_all(skip=skip, limit=limit)

    total = repo.count()

    return EmployeeListResponse(
        total=total,
        employees=employees,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
        employee_id: int,
        db: Session = Depends(get_db)
):
    """
    Obtiene un empleado por su ID.
    """
    repo = EmployeeRepository(db)
    employee = repo.get_by_id(employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleado con ID {employee_id} no encontrado"
        )

    return employee


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
        employee_data: EmployeeCreate,
        db: Session = Depends(get_db)
):
    """
    Crea un nuevo empleado.
    """
    repo = EmployeeRepository(db)

    # Verificar si el email ya existe
    existing_employee = repo.get_by_email(employee_data.email)
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un empleado con el email {employee_data.email}"
        )

    new_employee = repo.create(employee_data)
    return new_employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
        employee_id: int,
        employee_data: EmployeeUpdate,
        db: Session = Depends(get_db)
):
    """
    Actualiza un empleado existente.
    """
    repo = EmployeeRepository(db)

    # Verificar si el empleado existe
    existing_employee = repo.get_by_id(employee_id)
    if not existing_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleado con ID {employee_id} no encontrado"
        )

    # Si se está actualizando el email, verificar que no exista
    if employee_data.email and employee_data.email != existing_employee.email:
        email_exists = repo.get_by_email(employee_data.email)
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un empleado con el email {employee_data.email}"
            )

    updated_employee = repo.update(employee_id, employee_data)
    return updated_employee


@router.patch("/{employee_id}", response_model=EmployeeResponse)
def partial_update_employee(
        employee_id: int,
        employee_data: EmployeeUpdate,
        db: Session = Depends(get_db)
):
    """
    Actualiza parcialmente un empleado (solo los campos enviados).
    """
    return update_employee(employee_id, employee_data, db)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
        employee_id: int,
        db: Session = Depends(get_db)
):
    """
    Elimina un empleado.
    """
    repo = EmployeeRepository(db)

    deleted = repo.delete(employee_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleado con ID {employee_id} no encontrado"
        )

    return None