import reflex as rx
import sqlmodel
import sqlalchemy
from .base_model import SimpleModel
from typing import Optional, Dict
from .employee import Employee


class Availability(SimpleModel, table=True):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)

    employee_id: int = sqlmodel.Field(
        foreign_key="employee.id",
        index=True,
    )
    # day_of_week: str
    # hour: int
    availability: Dict = sqlmodel.Field(
        default_factory=Dict, 
        sa_column=sqlalchemy.Column(
            'availability',
            sqlalchemy.JSON
        )
    )

    employee: Optional[Employee] = sqlmodel.Relationship(
        sa_relationship_kwargs={"lazy": "select"}
    )