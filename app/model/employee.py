from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

if TYPE_CHECKING:
    from app.model.workschedule import WorkSchedule


class EmployeeBase(SQLModel):
    email: str = Field(index=True, unique=True, nullable=False, max_length=255)
    name: str = Field(nullable=False, max_length=255)
    department: str = Field(nullable=False, max_length=255)
    position: str = Field(nullable=False, max_length=255)
    start_date: date = Field(nullable=False)


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    work_schedules: List["WorkSchedule"] = Relationship(back_populates="employee")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int


class EmployeeUpdate(SQLModel):
    email: Optional[str] = None
    name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[date] = None

class EmployeeResponse(EmployeeRead):
    pass


class PageResponse(SQLModel):
    content: List[EmployeeRead]
    pageNumber: int
    pageSize: int
    totalElements: int
    totalPages: int
    last: bool

