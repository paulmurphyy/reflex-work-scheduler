import reflex as rx
from states import calendarState
from .availability import h_label

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

def calendar() -> rx.Component:
    return rx.container(

        #Nav:
        rx.flex(
            rx.link(rx.button('< Availability'), href='/availability', variant="soft"),
            width="100%",
            margin_bottom="1em",
        ),

        #Title
        rx.heading("Shift Calendar", size="9"),

        #Grid layout for calendar: 
        rx.grid(
            # Column 1, Row 1: space for the time column
            rx.text("Time", font_weight="bold"),

            # Columns 2-8, Row 1: day headers
            rx.foreach(
                calendarState.days,
                lambda day: rx.text(day[0:3], font_weight="bold", text_align="center")
            ),

            rx.foreach(
                calendarState.hours, 
                lambda h: rx.fragment(
                    # Column 1: The Hour Label
                    rx.text(h_label(h), white_space="nowrap", padding_top="0.5em"),

                    # Columns 2-8: The heatmap cells for that hour
                    rx.foreach(
                        calendarState.days,
                        lambda day: rx.center(
                            rx.text(calendarState.heatmap[day][h].to_string()),
                            bg="green",

                            #Styling for each of the cells:
                            border="1px solid white",
                            border_radius="4px",
                            height="3em",
                            width="100%",

                            #Opacity adjusts with the number of employees working: (cur_count/max_count). Darker color means more people are working.
                            opacity=rx.cond(
                                calendarState.heatmap[day][h] > 0,
                                calendarState.heatmap[day][h] / calendarState.max_emp_count,
                                #If no-one is working on the day, the cell is transparent:
                                0.05,
                            ),
                            padding="0.5em",
                        )
                    )
                )
            ),
            columns="8", 
            spacing="2",
            width="100%",
            padding_top='1em',
        ),
        padding="2em",
    )