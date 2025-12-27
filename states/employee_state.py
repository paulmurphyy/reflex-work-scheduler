import reflex as rx
from typing import Dict, Any, List
from models import Employee, Availability
import sqlmodel

class employeeState(rx.State):

    new_employee_name: str = ""
    new_employee_id: str = ""
    employees: List[Dict[str, Any]]

    def change_name(self, name: str):
        self.new_employee_name = name

    def change_id(self, id: str):
        if id.isdigit() or id == "":
            self.new_employee_id = id

    def get_employees(self):
        with rx.session() as session:
            self.employees = [
                {
                    "id": emp.id,
                    "name": emp.name,
                }
                for emp in session.scalars(Employee.select()).all()
            ]
    
    def clear_employees(self):
        with rx.session() as session:
            for emp in session.scalars(Employee.select()).all():
                session.delete(emp)
            for aval in session.scalars(Availability.select()).all():
                session.delete(aval)
            session.commit()
        self.get_employees()
    
    def delete_employee(self, emp_id: int):
        with rx.session() as session:
            employee = session.scalars(
                Employee.select().where(Employee.id == emp_id)
            ).first()
            aval = session.scalars(Availability.select().where(Availability.employee_id == emp_id)).first()
            if aval:
                session.delete(aval)
            if employee:
                session.delete(employee)
            session.commit()

        self.get_employees()
        return rx.toast.success("Employee deleted")

    def add_employee(self):
        if self.new_employee_name == "":
            return rx.toast.error("Name is required!")

        with rx.session() as session:
            session.add(Employee(
                name = self.new_employee_name
            ))
            session.commit()

        employee_name: str = self.new_employee_name
        self.new_employee_name = ""

        self.get_employees()
        return rx.toast.success(f"Added {employee_name}!")