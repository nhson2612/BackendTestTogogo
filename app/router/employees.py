from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.model.employee import EmployeeRead, EmployeeCreate, EmployeeResponse
from app.service.employee_service import EmployeeService
from app.service.shift_service import WorkScheduleService
from app.validator.employee_validator import EmployeeValidator

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=EmployeeResponse)
def create_employee(employee_data: EmployeeCreate, session: Session = Depends(get_session)):
    return EmployeeService.create_employee(session, employee_data)

@router.get("")
def get_employees(
        params: tuple = Depends(EmployeeValidator.validate_params),
        db: Session = Depends(get_session)
):
    department, start_date, date_filter, order, page, size = params

    result = EmployeeService.get_employees_paginated(
        db, department, start_date, date_filter, order, page, size
    )

    if result is None:
        raise HTTPException(status_code=204, detail="No Content")
    return result

@router.post("/{employee_id}/shift")
def assign_shift(
        employee_id: int,
        payload: dict,
        session: Session = Depends(get_session),
):
    result, is_update = WorkScheduleService.assign_or_update_shift(
        session,
        employee_id=employee_id,
        work_day=payload.get("work_day"),
        shift=payload.get("shift")
    )

    if is_update:
        return {"status": status.HTTP_200_OK, "detail": result["message"]}
    else:
        return {"status": status.HTTP_201_CREATED, "detail": result["message"]}

