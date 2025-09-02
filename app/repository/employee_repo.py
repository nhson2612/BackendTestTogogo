from sqlalchemy import func
from typing import Optional, List, Tuple
from datetime import date

from sqlmodel import Session, select
from app.model.employee import Employee

class EmployeeRepository:
    @staticmethod
    def get_by_email(session: Session, email: str) -> Optional[Employee]:
        return session.exec(select(Employee).where(Employee.email == email)).first()

    @staticmethod
    def create(session: Session, employee: Employee) -> Employee:
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee

    @staticmethod
    def get_by_department_paginated(
            session: Session,
            department: str,
            start_date: Optional[date] = None,
            date_filter: Optional[str] = None,
            order: str = "desc",
            page: int = 0,
            size: int = 10,
    ) -> Tuple[List[Employee], int]:
        query = select(Employee).where(Employee.department == department)

        if start_date:
            if date_filter == "before":
                query = query.where(Employee.start_date < start_date)
            elif date_filter == "after":
                query = query.where(Employee.start_date > start_date)
            else:
                query = query.where(Employee.start_date > start_date)
        count_query = select(func.count()).select_from(query.subquery())
        total_elements = session.exec(count_query).one()

        if order.lower() == "asc":
            query = query.order_by(Employee.start_date.asc())
        else:
            query = query.order_by(Employee.start_date.desc())
        offset = page * size
        items = session.exec(query.offset(offset).limit(size)).all()

        return items, total_elements


