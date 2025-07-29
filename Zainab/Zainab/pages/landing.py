import reflex as rx
from ..components import footer, signin, signup, recovery, register
from ..states.app_state import AppState, GroupFormState, UserSignupFormState

def navbar():
    return rx.box(
        rx.image(src="../thrift_logo.png", height="40px", margin_right="10px", margin_left="1rem"),
        justify_content="start",
        align_items="center",
        padding="1rem",
        width="100%",
        position="fixed",
        top="0",
        z_index="1000",
        background_color="white",
    )

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.image(
            src="../thrift_bg.png",
            height="100vh",
            width="100vw",
            object_fit="cover",
            position="fixed",
            top="0",
            left="0",
            z_index="-1",
        ),
        rx.box(
            height="100vh",
            width="100vw",
            position="fixed",
            top="0",
            left="0",
            bg="rgba(0, 0, 0, 0.6)",
            z_index="0",
        ),
        
        rx.box(
            rx.flex(
                # Left side: Text & Button
                rx.box(
                    rx.vstack(
                        rx.text("Thrift Contribution", 
                               font_size=rx.breakpoints(initial="2rem", md="3rem"),  # Smaller on mobile
                               font_weight="bold", 
                               color="white"),
                        rx.text(
                            "Hello there, welcome to our online contribution platform that helps groups or "
                            "friends come together and make financial goal contributions easily and securely "
                            "in a way that encourages trust, transparency, and fairness.",
                            font_size="md",
                            color="white",
                        ),
                        rx.button(
                            "Create a Group",
                            bg="#333300",
                            color="white",
                            border_radius="md",
                            on_click=lambda: AppState.set_landing_view("create"),
                            padding="4",
                            width=rx.breakpoints(initial="150px", md="200px"),  # Narrower on mobile
                            height="45px",
                            _hover={"bg": "#666633"}
                        ),
                        spacing="4",
                        text_align="left",
                        padding_top=rx.breakpoints(initial="2rem", md="4rem"),  # Less padding on mobile
                    ),
                    width=rx.breakpoints(initial="100%", md="50%"),  # Full width on mobile, half on desktop
                    padding="4",
                    z_index="4",
                ),
                # Right side: Login/Signup Components
                rx.box(
                    rx.vstack(
                        rx.cond(
                            AppState.landing_view == "signin",
                            signin.signin_view(),
                            rx.cond(
                                AppState.landing_view == "signup",
                                signup.signup_view(),
                                rx.cond(
                                    AppState.landing_view == "recovery",
                                    recovery.forgpt_password_view(),
                                    register.new_group()
                                )
                            )
                        ),
                        spacing="5",
                        width="100%",
                        align="center",
                    ),
                    width=rx.breakpoints(initial="100%", md="40%"),  # Full width on mobile, 40% on desktop
                    padding="4",
                ),
                
                direction=rx.breakpoints(initial="column", md="row"),  # Stack vertically on mobile, horizontally on desktop
                spacing="6",
                align="center",
                justify="center",
                width="100%",
                padding="4",
                z_index="2",
                height="calc(100vh - 70px)",
            ),
            width="100%",
            height="100vh",
            padding=rx.breakpoints(initial="2rem", md="4rem"),  # Less padding on mobile
            min_width="0px",  # Remove min-width constraint
            overflow_y="auto",
        ),
        # footer.footer(),
        min_width="0px",  # Remove min-width constraint
        style={
            "scrollbar_width": "thin",
            "scrollbar_color": "#888 transparent",
            "&::-webkit-scrollbar": {
                "width": "10px",
            },
            "&::-webkit-scrollbar-track": {
                "background": "transparent",
            },
            "&::-webkit-scrollbar-thumb": {
                "background_color": "#888",
                "border_radius": "4px",
            },
            "&::-webkit-scrollbar-thumb:hover": {
                "background": "#555",
            },
        },
    )