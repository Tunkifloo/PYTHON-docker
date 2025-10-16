from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository:
    """Repositorio para operaciones CRUD de empleados"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Obtiene todos los empleados con paginación"""
        return self.db.query(Employee).offset(skip).limit(limit).all()

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """Obtiene un empleado por ID"""
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def get_by_email(self, email: str) -> Optional[Employee]:
        """Obtiene un empleado por email"""
        return self.db.query(Employee).filter(Employee.email == email).first()

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Busca empleados por nombre, email o departamento"""
        search_filter = or_(
            Employee.first_name.ilike(f"%{query}%"),
            Employee.last_name.ilike(f"%{query}%"),
            Employee.email.ilike(f"%{query}%"),
            Employee.department.ilike(f"%{query}%"),
            Employee.position.ilike(f"%{query}%")
        )
        return self.db.query(Employee).filter(search_filter).offset(skip).limit(limit).all()

    def count(self) -> int:
        """Cuenta el total de empleados"""
        return self.db.query(Employee).count()

    def create(self, employee_data: EmployeeCreate) -> Employee:
        """Crea un nuevo empleado"""
        db_employee = Employee(**employee_data.model_dump())
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def update(self, employee_id: int, employee_data: EmployeeUpdate) -> Optional[Employee]:
        """Actualiza un empleado existente"""
        db_employee = self.get_by_id(employee_id)
        if not db_employee:
            return None

        # Actualiza solo los campos que fueron enviados
        update_data = employee_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_employee, field, value)

        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def delete(self, employee_id: int) -> bool:
        """Elimina un empleado"""
        db_employee = self.get_by_id(employee_id)
        if not db_employee:
            return False

        self.db.delete(db_employee)
        self.db.commit()
        return True