"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from states import employeeState, availabilityState
from pages.index import index
from pages.availability import availability
# from typing import List


# config = rx.Config(
#     app_name="my_app",
#     # db_url="sqlite:///reflex.db",
# )


app = rx.App(
    theme=rx.theme(
        appearance="inherit",
        has_background=True,
        radius="large",
    )
)
app.add_page(index, on_load=employeeState.get_employees)
app.add_page(availability, route="/availability", on_load=lambda: availabilityState.load_employee_name(1))
