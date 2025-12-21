import reflex as rx
from states import availabilityState

def availability() -> rx.Component:
    return rx.container(
        # Title
        rx.vstack(
            rx.text("Add Availability", size="9", padding="2em", width="100%", text_align="center"),
        ),

        # Employee Name Subheader with Navigation
        rx.hstack(
            rx.button("<", on_click=availabilityState.prev_employee),
            rx.text(availabilityState.selected_employee_name, size="5", width="100%", text_align="center"),
            rx.button(">", on_click=availabilityState.next_employee),
            justify="center",
            spacing="4",
            padding="1em",
        ),

        # Availability Grid
        rx.grid(
            # Header Row
            rx.text("Time", font_weight="bold"),
            rx.foreach(availabilityState.days, lambda day: rx.text(day[:3], font_weight="bold")),

            # Body Rows
            rx.foreach(
                availabilityState.hours_list, 
                lambda h_data: rx.fragment(
                    # Display the 12-hour label (e.g., "1:00 PM")
                    rx.text(h_data["label"], white_space="nowrap"),
                    rx.foreach(
                        availabilityState.days,
                        lambda day: rx.center(
                            rx.checkbox(
                                # Use h_data["hour"] (the integer) for logic and state tracking
                                is_checked=availabilityState.active_slots.contains(
                                    day + "-" + h_data["hour"].to_string()
                                ),
                                # When clicked, it triggers the database logic with the correct integer hour
                                on_change=lambda _: availabilityState.set_employee_availability(
                                    availabilityState.selected_employee_id, 
                                    day, 
                                    h_data["hour"]
                                ),
                                color_scheme="green",
                                size="3",
                            ),
                            width="25px",
                        )
                    )
                )
            ),
            columns="8",
            spacing="4",
            width="100%",
        ),
        padding="2em",
    )