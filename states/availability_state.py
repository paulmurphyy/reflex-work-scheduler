import reflex as rx
from .base_state import State
from models import Availability, Employee
from typing import Sequence


class availabilityState(State):
    """
    Controls availability across all employees.
    """
    selected_employee_id: int = 1
    selected_employee_name: str = "Select an Employee"
    days: list[str] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours_blocks: list[int] = [9, 10, 11, 12, 13, 14, 15, 16]
    working_now: Sequence[Availability] = []
    my_shifts: Sequence[Availability] = []
    my_week: Sequence[Availability] = []


    @rx.var
    def active_slots(self) -> list[str]:
        #Returns a list of str like: ["Monday-9"]
        return [f"{row.day_of_week}-{row.hour}" for row in self.my_week]
    
    @rx.var
    def hours_list(self) -> list[dict[str, int | str]]:
        """
        Transforms military hours into a list of dictionaries with 12-hour labels.
        >>>
        {'hour': 13, 'label': '1:00 PM'}
        """
        data = []
        for h in self.hours_blocks:
            if h == 0:
                label = "12:00 AM"
            elif h < 12: 
                label = f"{h}:00 AM"
            elif h == 12: 
                label = "12:00 PM"
            else:
                label = f"{h-12}:00 PM"
            data.append({"hour": h, "label": label})
        return data

    def next_employee(self):
        """
        Moves to the next employee in the database.
        """
        self.selected_employee_id += 1
        self.load_employee_name(self.selected_employee_id)

    def prev_employee(self):
        """
        Moves to the previous employee in the database.
        """
        if self.selected_employee_id >1:
            self.selected_employee_id -= 1
            self.load_employee_name(self.selected_employee_id)

    def set_employee_availability(self, id, day, hour_block):
        """
        Sets the employee's available hours for the given day.
        """
        print(f"--DB TRIGGERED: {id}, {day}, {hour_block}")
        emp_id = int(id)
        h_block = int(hour_block)

        with rx.session() as session:

            existing = session.exec(
                Availability.select().where(
                    (Availability.employee_id == emp_id) &
                    (Availability.day_of_week == day) &
                    (Availability.hour == h_block)
                )
            ).first()

            if existing:
                #If shift exists for this employee, delete it.
                session.delete(existing)

            else:
                session.add(
                    Availability(
                        employee_id=emp_id, day_of_week=day, hour=h_block
                    )
                )
            #Commit changes.
            session.commit()

        #Refresh so the checkbox lights up.
        self.get_employee_week(id)

    def load_employee_name(self, id):
        """
        Pulls the employee's name via the employee id.
        """
        self.selected_employee_id = id
        with rx.session() as session:
            #Get the name.
            employee = session.get(Employee, id)
            if employee:
                self.selected_employee_name = employee.name

            #Refresh the grid.
            self.get_employee_week(id)

    def get_employee_day(self, id, day):
        """
        Returns employee's availability for shift(s) for the given day.
        """
        with rx.session() as session:
            results = session.exec(
                Availability.select().where(
                    (Availability.employee_id == id) &
                    (Availability.day_of_week == day)
                )
            ).all()
        self.my_shifts = results

    def get_employee_week(self, id):
        """
        Returns employee's availability for the entire week.
        """
        with rx.session() as session:
            results = session.exec(
                Availability.select().where(
                    (Availability.employee_id == id)
                )
            ).all()
        self.my_week = results

    def get_day_hour_status(self, day, hour):
        """
        Returns everyone who is available for shifts on the given day and hour.
        """
        with rx.session() as session:
            results = session.exec(
                Availability.select().where(
                (Availability.day_of_week == day) &
                (Availability.hour == hour)
                )
            ).all()
            self.working_now = results
            
    def get_day_status(self, day):
        """
        Returns everyone who is available on the given day.
        """
        with rx.session() as session:
            results = session.exec(
                Availability.select().where(
                    (Availability.day_of_week == day)
                )
            ).all()
        self.working_now = results

