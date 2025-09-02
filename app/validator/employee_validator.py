import re
from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status, Query
from sqlmodel import Session
from datetime import date
from app.repository.employee_repo import EmployeeRepository
from app.model.employee import EmployeeCreate


class EmployeeValidator:
    @staticmethod
    def validate_email_format(email: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"field": "email", "message": "Email không hợp lệ"},
            )

    @staticmethod
    def validate_start_date(start_date: str) -> date:
        try:
            parsed_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            return parsed_date
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"field": "start_date", "message": "Định dạng ngày phải là YYYY-MM-DD"},
            )

    @staticmethod
    def validate_unique_email(session: Session, email: str):
        if EmployeeRepository.get_by_email(session, email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"field": "email", "message": "Email đã tồn tại"},
            )

    @classmethod
    def validate_employee(cls, session: Session, employee_data: EmployeeCreate):
        cls.validate_email_format(employee_data.email)
        cls.validate_unique_email(session, employee_data.email)

    @staticmethod
    def validate_params(
            department: str = Query(...),
            start_date: Optional[date] = Query(None),
            date_filter: Optional[str] = Query(None),
            order: str = Query("desc", description="asc|desc"),
            page: int = Query(0, ge=0),
            size: int = Query(10, gt=0),
    ):
        if date_filter and date_filter not in ("before", "after"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"field": "date_filter", "message": "only before or after allowed"},
            )
        if order not in ("asc", "desc"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"field": "order", "message": "Only asc or desc allowed"},
            )

        if size > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"field": "size", "message": "Size must not be greater than 100"},
            )

        return department, start_date, date_filter, order, page, size

