"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from states import employeeState, availabilityState, calendarState
from pages.index import index
from pages.availability import availability
from pages.calendar import calendar
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
app.add_page(availability, route="/availability", on_load=availabilityState.on_load)
app.add_page(calendar, on_load=calendarState.update_heatmap)