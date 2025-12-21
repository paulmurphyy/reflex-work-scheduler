import reflex as rx
from states import availabilityState

def availability() -> rx.Component:
    return rx.container(
        #Title
        rx.vstack(
            rx.text("Add Availability", size="9", padding="2em", width="100%", text_align="center"),
        ),

        #Employee Name Subheader
        rx.hstack(
            rx.button("<", on_click=availabilityState.prev_employee),
            rx.text(availabilityState.selected_employee_name, size="5", width="100%", text_align="center"),
            rx.button(">", on_click=availabilityState.next_employee),
            justify="center",
            spacing="4",
            padding="1em",
        ),

        #Availability Grid
        rx.grid(
            #Header
            rx.text("Time", font_weight="bold"),
            rx.foreach(availabilityState.days, lambda day: rx.text(day[:3], font_weight="bold")),

            #Body
            rx.foreach(
                availabilityState.hours_blocks, 
                lambda hour: rx.fragment(
                    rx.text(f"{hour}:00"),
                    rx.foreach(
                        availabilityState.days,
                        lambda day: rx.button(
                            "",
                            size="1",
                            variant="outline",
                            width="25px",
                            on_click=lambda: availabilityState.set_employee_availability(
                                availabilityState.selected_employee_id, 
                                day, 
                                hour,
                            ),
                        )
                    )
                )
            ),
            columns="8",
            spacing="2",
            width="100%",
        ),
        padding="2em",
    )
