import reflex as rx
from typing import List
from models import Employee
from .base_state import State

class employeeState(State):

    new_employee_name: str = ""
    new_employee_id: str = "" #Initially kept as a string to allow the employee_id textbox to be empty.
    employees: List[Employee] = []

    def change_name(self, name:str):
        self.new_employee_name = name

    def change_id(self, id:str):
        #Only capture numbers or spaces. Letters will be omitted. Note: You will see the letters in the box, but they won't be recorded.
        if id.isdigit() or id == "":
            self.new_employee_id = id

    def get_employees(self):
        with rx.session() as session:
            #Fetch all employees from the database.
            self.employees = session.exec(Employee.select()).all() #type: ignore

    def delete_employee(self, emp_id: int):
        with rx.session() as session:
            employee = session.exec(
                Employee.select().where(Employee.id == emp_id)
            ).first()
            if employee:
                session.delete(employee)
                session.commit()

        #Refresh employee list after deletion.
        self.get_employees()

    def add_employee(self):

        #Validate that both fields are entered:
        if self.new_employee_id == "" or self.new_employee_name == "":
            return rx.toast.error("Both Name and ID are required!")
        
        #If entered id is not a number:
        if not self.new_employee_id.isdigit():
            return rx.toast.error("ID must be a number!")

        #if checks pass, add employee.
        with rx.session() as session:
            session.add(
                Employee(
                    name=self.new_employee_name,
                    employee_id=int(self.new_employee_id) #ID is converted back to an int when added to the database.
                )
            )
            session.commit()

            #Copy employee name.
            employee_name = self.new_employee_name

            #Reset for next entry.
            self.new_employee_name = ""
            self.new_employee_id = ""

            #Refresh the list of users.
            self.get_employees()

            #Success message to let users new the employee has been added. 
            return rx.toast.success(f"Added {employee_name}!")

