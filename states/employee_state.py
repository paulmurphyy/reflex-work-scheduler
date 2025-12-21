import reflex as rx
from typing import Sequence
from models import Employee
from .base_state import State

class employeeState(State):

    new_employee_name: str = ""
    new_employee_id: str = ""
    employees: Sequence[Employee] = []

    def change_name(self, name: str):
        self.new_employee_name = name

    def change_id(self, id: str):
        if id.isdigit() or id == "":
            self.new_employee_id = id

    def _get_employees(self):
        with rx.session() as session:
            self.employees = session.scalars(Employee.select()).all()

    def get_employees(self):
        self._get_employees()

    def delete_employee(self, emp_id: int):
        with rx.session() as session:
            employee = session.scalars(
                Employee.select().where(Employee.id == emp_id)
            ).first()
            if employee:
                session.delete(employee)
            session.commit()

        self._get_employees()
        return rx.toast.success("Employee deleted")

    def add_employee(self):
        if self.new_employee_id == "" or self.new_employee_name == "":
            return rx.toast.error("Both Name and ID are required!")

        if not self.new_employee_id.isdigit():
            return rx.toast.error("ID must be a number!")

        with rx.session() as session:
            session.add(Employee(
                name=self.new_employee_name,
                id=int(self.new_employee_id)
            ))
            session.commit()

        employee_name: str = self.new_employee_name
        self.new_employee_name = ""
        self.new_employee_id = ""

        self._get_employees()
        return rx.toast.success(f"Added {employee_name}!")