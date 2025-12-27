import reflex as rx
from states import calendarState
from .availability import h_label


def calendar() -> rx.Component:
    return rx.container(

        #Nav:
         rx.flex(
            rx.link(rx.button('< Availability'), href='/availability', variant="soft"),
            rx.spacer(),
            rx.link(rx.button('Employees >'), href='/', variant="soft"),
            width="100%",
            margin_bottom="1em",
        ),

        #Title
        rx.text("Shift Calendar", size="9", font_weight="bold", margin_bottom="1em"),

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
                lambda hour: rx.fragment(
                    # Column 1: The Hour Label
                    rx.text(f"{hour}:00", white_space="nowrap", padding_top="0.5em"),

                    # Columns 2-8: The heatmap cells for that hour
                    rx.foreach(
                        calendarState.days,
                        lambda day: rx.center(
                            rx.text(calendarState.heatmap[day][hour].to_string()),
                            bg="green",

                            #Styling for each of the cells:
                            border="1px solid white",
                            border_radius="4px",
                            height="3em",
                            width="100%",

                            #Opacity adjusts with the number of employees working: (cur_count/max_count). Darker color means more people are working.
                            opacity=rx.cond(
                                calendarState.heatmap[day][hour] > 0,
                                calendarState.heatmap[day][hour] / calendarState.max_emp_count,
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
        ),
        padding="2em",
    )