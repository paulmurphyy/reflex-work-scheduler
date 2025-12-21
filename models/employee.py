import reflex as rx
from .base_model import SimpleModel
import sqlmodel

class Employee(SimpleModel, table=True):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    name: str