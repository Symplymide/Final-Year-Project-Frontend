import reflex as rx
from ..states.app_state import AppState
from ..states.auth_state import AuthState

def signin_view():
    return rx.card(
        rx.form(
            rx.vstack(
                rx.heading("Sign In", size="5", align="center", color="#333300"),
                rx.input(
                    placeholder="Email",
                    width="100%",
                    height="40px",
                    required=True,
                    variant="surface",
                    color="#333300",
                    color_scheme="brown",
                    # style={"_placeholder": {
                    #         "color": "#333300",
                    #         "font_weight": "500"
                    #     }},
                    value=AuthState.username,
                    on_change=AuthState.set_username,
                ),
                rx.input(
                    placeholder="Password",
                    type="password",
                    width="100%",
                    height="40px",
                    color="#333300",
                    required=True,
                    color_scheme="brown",
                    style={"_placeholder": {
                            "color": "#333300",
                            "font_weight": "500"
                        }},
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                ),
                rx.button(
                    rx.cond(
                        AuthState.loading,
                        rx.spinner(size="2", color="white"),
                        rx.text("Sign In")
                    ),
                    bg="#333300",
                    color="white",
                    width="70%",
                    height="45px",
                    _hover={"bg": "#666633"},
                    on_click=AuthState.login,
                    disabled=AuthState.loading,
                ),
                
                rx.hstack(
                    # rx.link(
                    #     "Forgot Password?",
                    #     on_click=lambda: AppState.set_landing_view("recovery"),
                    #     bg="transparent",
                    #     padding="2",
                    #     font_size="12px",
                    #     color="#333300"
                    # ),
                    rx.link(
                        "Create Account",
                        on_click=lambda: AppState.set_landing_view("signup"),
                        bg="transparent",
                        padding="2",
                        font_size="12px",
                        color="#333300"
                    ),
                ),
                spacing="4",
                width="100%",
                align="center",
            ),
            width="100%",
        ),
        max_width="600px",
        padding=["20px", "40px"],
        min_width="420px",
        min_height="150px",
        shadow="lg",
        border_radius="lg",
        bg="rgba(255, 255, 255, 1)",
    )