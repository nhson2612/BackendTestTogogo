from fastapi import HTTPException
from datetime import date
from app.model.employee import Employee
from sqlmodel import Session, select


VALID_SHIFTS = {"morning", "afternoon", "full_day"}


class WorkScheduleValidator:

    @staticmethod
    def validate_employee_exists(session: Session, employee_id: int):
        employee = session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=400,
                detail={"employee_id": f"Employee with id {employee_id} does not exist"}
            )
        return employee

    @staticmethod
    def validate_work_day(work_day: str):
        try:
            return date.fromisoformat(work_day)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={"work_day": "Invalid date format. Must be YYYY-MM-DD"}
            )

    @staticmethod
    def validate_shift(shift: str):
        if shift.lower() not in VALID_SHIFTS:
            raise HTTPException(
                status_code=400,
                detail={"shift": f"Shift must be one of {list(VALID_SHIFTS)}"}
            )
        return shift.lower()


