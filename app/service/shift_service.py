from sqlmodel import Session
from app.repository.workschedule_repo import WorkScheduleRepository
from app.validator.shift_validator import WorkScheduleValidator
from app.model.workschedule import WorkSchedule


class WorkScheduleService:

    @staticmethod
    def assign_or_update_shift(session: Session, employee_id: int, work_day: str, shift: str):
        WorkScheduleValidator.validate_employee_exists(session, employee_id)
        valid_day = WorkScheduleValidator.validate_work_day(work_day)
        valid_shift = WorkScheduleValidator.validate_shift(shift)

        existing_schedule = WorkScheduleRepository.get_by_employee_and_day(
            session, employee_id, valid_day
        )

        if existing_schedule:
            existing_schedule.shift = valid_shift
            WorkScheduleRepository.save(session, existing_schedule)
            return {"message": "Shift updated successfully"}, True
        else:
            new_schedule = WorkSchedule(
                employee_id=employee_id,
                work_day=valid_day,
                shift=valid_shift
            )
            WorkScheduleRepository.save(session, new_schedule)
            return {"message": "Shift assigned successfully"}, False





