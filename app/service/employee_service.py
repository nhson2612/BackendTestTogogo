import math
from typing import Optional
from datetime import date
from sqlmodel import Session
from app.model.employee import EmployeeCreate, Employee
from app.repository.employee_repo import EmployeeRepository
from app.validator.employee_validator import EmployeeValidator

class EmployeeService:
    @staticmethod
    def create_employee(session: Session, employee_data: EmployeeCreate) -> Employee:
        EmployeeValidator.validate_employee(session, employee_data)
        new_employee = Employee(
            email=employee_data.email,
            name=employee_data.name,
            department=employee_data.department,
            position=employee_data.position,
            start_date=employee_data.start_date
        )
        return EmployeeRepository.create(session, new_employee)

    @staticmethod
    def get_employees_paginated(
            session: Session,
            department: str,
            start_date: Optional[date],
            date_filter: Optional[str],
            order: str,
            page: int,
            size: int,
    ):
        employees, total_elements = EmployeeRepository.get_by_department_paginated(
            session, department, start_date, date_filter, order, page, size
        )
        if total_elements == 0:
            return None
        return {
            "content": employees,
            "pageNumber": page,
            "pageSize": size,
            "totalElements": total_elements,
            "totalPages": math.ceil(total_elements / size),
            "last": (page + 1) * size >= total_elements,
        }

