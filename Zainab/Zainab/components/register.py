import reflex as rx
from ..states.app_state import AppState, GroupFormState
from ..states.auth_state import AuthState

def new_group():
    return rx.card(
        rx.form(
            rx.vstack(
                rx.heading("Create New Thrift Group", size="5", align="center", color="#333300", margin_bottom="15px"),
                rx.input(
                    placeholder="Enter Group Name",
                    value=GroupFormState.group_name,
                    on_change=GroupFormState.setvar("group_name"),
                    width="100%",
                    margin_bottom="6px",
                    height="40px",
                    color="#333300",
                ),
                rx.input(
                    placeholder="Enter Group Descriptions",
                    value=GroupFormState.group_description,
                    on_change=GroupFormState.setvar("group_description"),
                    width="100%",
                    margin_bottom="6px",
                    height="40px",
                    color="#333300",
                ),
                rx.input(
                    placeholder="Admin Name",
                    value=GroupFormState.admin_name,
                    on_change=GroupFormState.setvar("admin_name"),
                    width="100%",
                    margin_bottom="6px",
                    height="40px",
                    color="#333300",
                ),
                rx.input(
                    placeholder="Phone",
                    value=GroupFormState.admin_phone,
                    on_change=GroupFormState.setvar("admin_phone"),
                    width="100%",
                    margin_bottom="6px",
                    height="40px",
                    color="#333300",
                ),
                rx.input(
                    placeholder="Email",
                    value=GroupFormState.admin_mail,
                    on_change=GroupFormState.setvar("admin_mail"),
                    width="100%",
                    margin_bottom="6px",
                    height="40px",
                    color="#333300",
                ),
                rx.input(
                    placeholder="Password",
                    type="password",
                    value=GroupFormState.password,
                    on_change=GroupFormState.setvar("password"),
                    width="100%",
                    margin_bottom="6px",
                    height="40px",
                    color="#333300",
                ),
                rx.input(
                    placeholder="Confirm Password",
                    type="password",
                    value=GroupFormState.confirm_password,
                    on_change=GroupFormState.setvar("confirm_password"),
                    width="100%",
                    margin_bottom="6px",
                    height="40px",
                    color="#333300",
                ),
                rx.button(
                    rx.cond(
                        GroupFormState.loading,
                        rx.spinner(size="2", color="white"),
                        rx.text("Submit")
                    ),
                    bg="#333300",
                    color="white",
                    width="70%",
                    height="45px",
                    _hover={"bg": "#CC9933"},
                    on_click=GroupFormState.handle_submit,
                    disabled=GroupFormState.loading,
                ),
                rx.link(
                    "< Go Back",
                    on_click=lambda: AppState.set_landing_view("signin"),
                    bg="transparent",
                    padding="2",
                    font_size="12px",
                    color="#333300"
                ),
                spacing="2",
                width="100%",
                align="center",
            ),
            width="100%",
        ),
        rx.dialog.root(
            rx.dialog.content(
                rx.vstack(
                    rx.heading("Group Successfully Created!", font_size="26px", align="center", color="green", margin="20px"),
                    rx.text(f"Group ID: {GroupFormState.group_id}", font_size="16px"),
                    rx.text(f"Your User ID: {GroupFormState.user_id}", font_size="16px"),
                    rx.text("You are the Admin of this group.", font_size="14px"),
                    rx.text("Please save these details somewhere safe.", font_size="14px"),
                    rx.dialog.close(
                        rx.button(
                            "Close",
                            on_click=[GroupFormState.setvar("show_dialog", False), AppState.set_landing_view("signin")],
                            bg="#333300",
                            color="white",
                            border_radius="md",
                            padding="4",
                            width="200px",
                            height="45px"
                        ),
                    ),
                    spacing="2",
                    width="100%",
                    align="center",
                ),
            ),
            open=GroupFormState.show_dialog,
        ),
        max_width=rx.breakpoints(sm="90%", md="600px"),
        padding=["20px", "40px"],
        min_width="420px",
        min_height="150px",
        shadow="lg",
        border_radius="lg",
        bg="rgba(255, 255, 255, 1)",
    )