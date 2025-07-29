import reflex as rx
from ..states.app_state import AppState

class RecoveryFormState(rx.State):
    email: str = ""
    loading: bool = False

    def set_email(self, value: str):
        self.email = value

    async def handle_reset(self):
        self.loading = True
        # Placeholder for reset logic (e.g., API call to send reset email)
        await rx.sleep(1)  # Simulate async operation
        self.loading = False
        return rx.toast("Password reset email sent (placeholder)!", position="top-right")

def forgpt_password_view():
    return rx.card(
        rx.form(
            rx.vstack(
                rx.heading("Forgot Password", size="5", align="center", color="#333300"),
                rx.input(
                    placeholder="Email",
                    value=RecoveryFormState.email,
                    on_change=RecoveryFormState.set_email,
                    width="100%",
                    height="40px",
                    color="#333300",
                ),
                rx.button(
                    rx.cond(
                        RecoveryFormState.loading,
                        rx.spinner(size="2", color="white"),
                        rx.text("Reset Password")
                    ),
                    bg="#333300",
                    color="white",
                    width="70%",
                    height="45px",
                    _hover={"bg": "#CC9933"},
                    on_click=RecoveryFormState.handle_reset,
                    disabled=RecoveryFormState.loading,
                ),
                rx.link(
                    "< Go Back",
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
        max_width=rx.breakpoints(sm="90%", md="600px"),
        padding="40px",
        min_width="420px",
        min_height="150px",
        shadow="lg",
        border_radius="lg",
        bg="rgba(255, 255, 255, 1)",
    )