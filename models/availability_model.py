import reflex as rx
from sqlmodel import Field

class Availability(rx.Model, table=True):
    employee_id: int = Field(foreign_key="employee.id")
    day_of_week: str
    hour: int

    
