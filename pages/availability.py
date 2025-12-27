import reflex as rx
from states import availabilityState


def h_label(h):
    """
    Transforms military hours into a list of dictionaries with 12-hour labels.
    >>>
    {'hour': 13, 'label': '1:00 PM'}
    """
    return rx.cond(
        h == 0,
        "12:00 AM",
        rx.cond(
            h < 12,
            rx.text(f"{h}:00 AM"),
            rx.cond(
                h == 12,
                "12:00 PM",
                f"{h - 12}:00 PM",
            ),
        ),
    )

def availability() -> rx.Component:
    return rx.container(
        # Title
        rx.flex(
            rx.link(rx.button('< Employees'), href='../', style={'margin-right': 'auto'}),
        ),
        rx.vstack(
            rx.text("Add Availability", size="9", width="100%", text_align="center"),
        ),

        # Employee Name Subheader with Navigation
        rx.hstack(
            rx.button("<", 
                      on_click=availabilityState.prev_employee,
                      #"Previous" arrow is disabled if the current index is 0.
                      is_disabled=availabilityState.is_at_start,
                      opacity=rx.cond(availabilityState.is_at_start, 0.3, 1.0),
                      cursor=rx.cond(availabilityState.is_at_start, "not-allowed", "pointer"),
                      ),
            rx.text(availabilityState.cur_name, size="5", width="100%", text_align="center"),
            rx.button(">", 
                      on_click=availabilityState.next_employee,
                      #"Next" arrow is disabled if end of list is reached.
                      is_disabled=availabilityState.is_at_end,
                      opacity=rx.cond(availabilityState.is_at_end, 0.3, 1.0),
                      cursor=rx.cond(availabilityState.is_at_end, "not-allowed", "pointer"),
                      ),
            justify="center",
            # spacing="4",
            padding="1em",
        ),

        # Availability Grid
        rx.grid(
            # Header Row
            rx.text("Time", font_weight="bold"),
            rx.foreach(availabilityState.days, lambda day: rx.text(day[:3], font_weight="bold")),
            rx.foreach(
                availabilityState.h_blocks,
                lambda hour: rx.fragment(
                    rx.text(h_label(hour), white_space="nowrap"),
                    rx.foreach(
                        availabilityState.days,
                        lambda day: rx.center(
                            rx.cond(
                                availabilityState.cur_aval.contains(day) & availabilityState.cur_aval[day].contains(hour),
                                rx.checkbox(
                                    checked=True, 
                                    on_change=lambda *_: availabilityState.rem_aval(
                                        availabilityState.cur_id,
                                        day,
                                        hour,
                                    ),
                                ),
                                rx.checkbox(
                                    checked=False, 
                                    on_change=lambda *_: availabilityState.add_aval(
                                        availabilityState.cur_id,
                                        day,
                                        hour,
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            columns="8",
            spacing="4",
            width="100%",
        ),
        padding="2em",
    )