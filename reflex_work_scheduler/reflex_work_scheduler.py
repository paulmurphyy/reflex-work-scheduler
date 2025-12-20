"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from typing import List


class Employee(rx.Model, table=True):
    employee_id: int
    name: str
    # availability: list[str]

class State(rx.State):
    employee_id: int = 0
    name: str = ""
    # availability: list[str] = []

    def set_name(self, value: str):
        self.name = value

    def set_employee_id(self, value: str):
        self.employee_id = int(value) if value.isdigit() else 0

    # def set_availability(self, value: str):
    #     # comma-separated input → list
    #     self.availability = [v.strip() for v in value.split(",")]

    def add_employee(self):
        with rx.session() as session:
            session.add(
                Employee(
                    employee_id=self.employee_id,
                    name=self.name,
                    # availability=self.availability,
                )
            )
            session.commit()

        # reset inputs
        self.employee_id = 0
        self.name = ""
        # self.availability = []


# config = rx.Config(
#     app_name="my_app",
#     # db_url="sqlite:///reflex.db",
# )

def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Employee Entry", size="9"),

            rx.input(
                value=State.name,
                placeholder="Enter name",
                on_change=State.set_name,
            ),

            rx.input(
                value=State.employee_id,
                placeholder="Enter employee ID",
                on_change=State.set_employee_id,
            ),

            # rx.input(
            #     placeholder="Availability (comma separated)",
            #     on_change=State.set_availability,
            # ),

            rx.button(
                "Add employee to database",
                on_click=State.add_employee,
            ),

            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )



app = rx.App()
app.add_page(index)
