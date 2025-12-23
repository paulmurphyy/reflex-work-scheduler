import reflex as rx
from .base_state import State
from models import Availability, Employee
from typing import List, Dict, Any, TypedDict


class availabilityState(State):
    """
    Controls availability across all employees.
    """
    cur_id: int = 1
    cur_name: str = ''
    cur_aval: Dict[str, List[int]] = {}
    days: list[str] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    h_blocks: list[int] = [9, 10, 11, 12, 13, 14, 15, 16]

    def next_employee(self):
        """
        Moves to the next employee in the database.
        """
        self.cur_id += 1
        self.load_employee_name()

    def prev_employee(self):
        """
        Moves to the previous employee in the database.
        """
        if self.cur_id > 1:
            self.cur_id -= 1
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
    
    def load_employee_name(self):
        """
        Pulls the employee's name via the employee id.
        """
        with rx.session() as session:
            #Get the name.
            employee = session.get(Employee, self.cur_id)
            if employee:
                self.cur_name = employee.name
            session.commit()
        #Refresh the grid.
        self.get_employee_week(self.cur_id)

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