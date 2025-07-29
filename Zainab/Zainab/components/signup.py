import reflex as rx
from ..states.app_state import UserSignupFormState, AppState
from ..states.auth_state import AuthState

def signup_view():
    return rx.card(
        rx.vstack(
            rx.text("Sign Up", align="center", color="#333300", margin_bottom="15px", font_size="24px", font_weight="bold"),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Group ID",
                        value=UserSignupFormState.group_id,
                        on_change=UserSignupFormState.setvar("group_id"),
                        width="100%",
                        margin_bottom="6px",
                        height="40px",
                        color="#333300",
                    ),
                    rx.input(
                        placeholder="Full Name",
                        value=UserSignupFormState.name,
                        on_change=UserSignupFormState.setvar("name"),
                        width="100%",
                        margin_bottom="6px",
                        height="40px",
                        color="#333300",
                    ),
                    rx.input(
                        placeholder="Phone number",
                        value=UserSignupFormState.phone,
                        on_change=UserSignupFormState.setvar("phone"),
                        width="100%",
                        margin_bottom="6px",
                        height="40px",
                        color="#333300",
                    ),
                    rx.input(
                        placeholder="Email Address",
                        value=UserSignupFormState.email,
                        on_change=UserSignupFormState.setvar("email"),
                        width="100%",
                        margin_bottom="6px",
                        height="40px",
                        color="#333300",
                    ),
                    rx.input(
                        placeholder="Password",
                        type="password",
                        value=UserSignupFormState.password,
                        on_change=UserSignupFormState.setvar("password"),
                        width="100%",
                        margin_bottom="6px",
                        height="40px",
                        color="#333300",
                    ),
                    rx.button(
                        rx.cond(
                            UserSignupFormState.loading,
                            rx.spinner(size="2", color="white"),
                            rx.text("Submit")
                        ),
                        width="70%",
                        align="center",
                        bg="#333300",
                        color="white",
                        height="45px",
                        _hover={"bg": "#666633"},
                        on_click=UserSignupFormState.handle_submit,
                        disabled=UserSignupFormState.loading,
                    ),
                    rx.link(
                        "Sign In Instead",
                        on_click=lambda: AppState.set_landing_view("signin"),
                        bg="transparent",
                        padding="2",
                        font_size="12px",
                        color="#333300"
                    ),
                    spacing="4",
                    width="100%",
                    align="center",
                ),
                width="100%",
            ),
            rx.dialog.root(
                rx.dialog.content(
                    rx.vstack(
                        rx.heading("User Successfully Created!", font_size="26px", align="center", color="green", margin="20px"),
                        rx.text(f"Your User ID: {UserSignupFormState.user_id}", font_size="16px", font_weight="bold"),
                        rx.text("Please save these details somewhere safe.", font_size="16px"),
                        rx.dialog.close(
                            rx.button(
                                "Close",
                                on_click=[UserSignupFormState.setvar("show_dialog", False), AppState.set_landing_view("signin")],
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
                open=UserSignupFormState.show_dialog,
            ),
            spacing="4",
            width="100%",
        ),
        max_width="600px",
        padding="40px",
        min_width="420px",
        min_height="150px",
        shadow="lg",
        border_radius="lg",
        bg="rgba(255, 255, 255, 1)",
    )