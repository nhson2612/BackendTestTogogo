from sqlmodel import Session, select
from app.model.workschedule import WorkSchedule


class WorkScheduleRepository:

    @staticmethod
    def get_by_employee_and_day(session: Session, employee_id: int, work_day):
        statement = select(WorkSchedule).where(
            WorkSchedule.employee_id == employee_id,
            WorkSchedule.work_day == work_day
        )
        return session.exec(statement).first()

    @staticmethod
    def save(session: Session, schedule: WorkSchedule):
        session.add(schedule)
        session.commit()
        session.refresh(schedule)
        return schedule
