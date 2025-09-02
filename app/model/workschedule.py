from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint, Column, String
from datetime import date
from enum import Enum

if TYPE_CHECKING:
    from .employee import Employee


class ShiftEnum(str, Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    FULL_DAY = "FULL_DAY"


class WorkScheduleBase(SQLModel):
    work_day: date = Field(nullable=False)
    shift: ShiftEnum = Field(sa_column=Column(String(20), nullable=False))


class WorkSchedule(WorkScheduleBase, table=True):
    __tablename__ = "work_schedule"
    __table_args__ = (
        UniqueConstraint("employee_id", "work_day", name="uix_employee_workday"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", nullable=False)
    employee: Optional["Employee"] = Relationship(back_populates="work_schedules")


class WorkScheduleCreate(WorkScheduleBase):
    employee_id: int


class WorkScheduleRead(WorkScheduleBase):
    id: int
    employee_id: int


class WorkScheduleUpdate(SQLModel):
    work_day: Optional[date] = None
    shift: Optional[ShiftEnum] = None
