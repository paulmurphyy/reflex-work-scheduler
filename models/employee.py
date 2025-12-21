import reflex as rx


class Employee(rx.Model, table=True):
    name: str
    employee_id: int #Maybe be unneccessary depending on the primary key of the database.
    #Shifts - how should we represent this? List of str and you choose from a dropdown? Morning/Mid/Closing?
    