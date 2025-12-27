import reflex as rx
from states.employee_state import employeeState

def index() -> rx.Component:
    return rx.container(
        rx.toast.provider(),
        rx.flex(
            rx.link(rx.button('Availability >'), href='availability', style={'margin-left': 'auto'}),
        ),
        rx.vstack(
            
            #Header
            rx.heading("Add New Employee", size="9", width="100%", text_align="center"),

            #Name Box
            rx.input(
                value=employeeState.new_employee_name,
                placeholder="Enter Employee's Name",
                on_change=employeeState.change_name,
                width="100%",
            ),

            #Add Employee Button
            rx.button(
                "Add Employee",
                color_scheme="blue",
                on_click=employeeState.add_employee,
                width="100%",
            ),


            align_items="start",
        ),

            #Divider between buttons and table.
            rx.divider(),
            rx.heading("Current Staff:", size="5", padding_y="1em"),
            #Table area
            rx.vstack(
                rx.foreach(

                #Employee Table
                employeeState.employees,
                lambda emp: rx.hstack(
                    rx.badge(f"ID: {emp['id']}", variant="outline", color_scheme="red"),
                    rx.text(emp['name']),

                    #Delete button.
                    rx.button(
                    rx.icon("trash-2"),
                    on_click=lambda: employeeState.delete_employee(emp.id),
                    color_scheme="red",
                    variant="ghost",
                ),

                    justify="between",
                    align_items="center",
                    padding_y="2",
                    border_bottom="1px solid #eaeaea",
                ),
                ),
            spacing="5",
            width="100%",
        ),
        padding_top="2em"
    )
