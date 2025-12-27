import reflex as rx
from .base_state import State
from models import Availability, Employee
from typing import List, Dict, Any, TypedDict


class availabilityState(State):
    """
    Controls availability across all employees.
    """
    all_employees: List[Employee] = []
    cur_index: int = 0
    cur_id: int = 0
    cur_name: str = 'No Employees Found'
    cur_aval: Dict[str, List[int]] = {}
    days: list[str] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    h_blocks: list[int] = [9, 10, 11, 12, 13, 14, 15, 16]


    #Computed properties: 
    @rx.var
    def is_at_start(self) -> bool:
        return self.cur_index == 0 
    
    @rx.var
    def is_at_end(self) -> bool:
        return self.cur_index >= len(self.all_employees) - 1

    #Functions:
    def next_employee(self):
        """
        Moves to the next employee in the employee list.
        """
        if not self.is_at_end:
            self.cur_index += 1
            self.load_employee_name()

    def prev_employee(self):
        """
        Moves to the previous employee in the employee list.
        """
        if not self.is_at_start:
            self.cur_index -= 1
            self.load_employee_name()

    def add_aval(self, id, day, h_block):
        """
        Sets the employee's available hours for the given day.
        """
        print(f"--DB TRIGGERED: {id}, {day}, {h_block}")
        # id = int(id)
        h_block = int(h_block)

        with rx.session() as session:
            existing = session.scalars(Availability.select().where(Availability.employee_id == id)).first()

            if not existing:
                session.add(
                    Availability(
                        employee_id=id, availability={day: [h_block]}
                    )
                )
            else:
                result = dict(existing.availability)
                hours = set(result.get(day, []))
                hours.add(h_block)
                result[day] = list(hours)
                existing.availability = result

            session.commit()

        self.get_employee_week(id)

    def rem_aval(self, id, day, h_block):
        """
        Sets the employee's available hours for the given day.
        """
        print(f"--DB TRIGGERED: {id}, {day}, {h_block}")
        # id = int(id)
        h_block = int(h_block)

        with rx.session() as session:
            existing = session.scalars(Availability.select().where(Availability.employee_id == id)).first()

            if existing:
                result = dict(existing.availability)
                hours = set(result.get(day, []))
                hours.remove(h_block)
                result[day] = list(hours)
                existing.availability = result
            else: print('error')

            session.commit()

        self.get_employee_week(id)

    def on_load(self):
        """
        Initializes the employee list on page load.
        """
        with rx.session() as session:
            self.all_employees = session.scalars(Employee.select()).all()
            if self.all_employees:
                self.cur_index = 0
                self.load_employee_name() 
            else:
                self.cur_name = 'No Employees Found'
                self.cur_aval = {}    
        
    def load_employee_name(self):
        """
        Pulls the employee's name via the current list index.
        """
        #Wipe current view.
        self.cur_aval = {}

        #If no employees are in the database:
        if not self.all_employees:
            self.cur_name = "No Employees Found"
            return

        #Pull employee via index:
        target = self.all_employees[self.cur_index]
        self.cur_id = target.id
        self.cur_name = target.name

        #Pull availability:
        with rx.session() as session:
            emp_aval = session.scalars(
                Availability.select().where(Availability.employee_id == self.cur_id)
            ).first()
            if emp_aval and emp_aval.availability:
                self.cur_aval = emp_aval.availability

    def get_employee_week(self, id):
        with rx.session() as session:
            emp = session.scalars(
                Availability.select().where(Availability.employee_id == id)
            ).first()
           
            if emp and emp.availability:
                self.cur_aval = emp.availability
            else:
                self.cur_aval = {}
            # Query your models
            employees = session.scalars(Availability.select()).all()
            for employee in employees:
                print(employee.employee_id, employee.availability)
            print(self.cur_aval)
            session.commit()