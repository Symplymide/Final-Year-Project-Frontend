import reflex as rx
from ..states.app_state import AppState, GroupFormState, SignupFormState
from . import signin, signup, recovery, register, reg_success
# from .signin import signin_view



def login_page() -> rx.Component:
    return rx.flex(
            # Left side: Text & Button

            rx.box(
                rx.desktop_only(
                    rx.vstack(
                    rx.text("Thrift Contribution", font_size="3rem", font_weight="bold", color="white",),
                    
                    
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
                        width="200px", 
                        height="45px"),
                    ),
                ),
                
                width="50%",
                padding="4",
                text_align="left",
                spacing="4",

            ),

            # Right side: Login Form
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

                                rx.cond(
                                    AppState.landing_view == "create",
                                    register.new_group(),
                                ),
                            ),
                        ),
                    ),
                    
                    
                    
                    
                    spacing="5",
                
                ),
            ),
            alert(),
            user_alert(),

            spacing="8",
            direction=rx.breakpoints(sm="column", md="row"),  # Column layout on mobile, row on larger screens
            align="center",
            justify="center",
            wrap="wrap",
            width="100%",
            padding="4",
            z_index="2"
        )

# def alert():
#     return rx.box(
#         rx.alert_dialog.root(
#             rx.alert_dialog.content(
#                 rx.alert_dialog.title("Success"),
#                 rx.alert_dialog.description("Your request was successful"),
#                 rx.alert_dialog.action(
#                     rx.button("OK", on_click=GroupFormState.setvar("show_dialog", False))
#                 ),
#             ),
#             open=GroupFormState.show_dialog,
#         ),
#     )

def user_alert():
    return rx.box(
        rx.dialog.root(
            rx.dialog.content(
                rx.vstack(
                    rx.heading(
                        "User Successfully Created!",
                        font_size="26px",
                        align="center", 
                        color="green",
                        margin="20px",
                    ),
                    rx.text(f"Your User ID: {SignupFormState.user_id}", font_size="16px"),
                    rx.text("Please save these details somewhere safe.", font_size="14px"),
                    rx.dialog.close(
                        rx.button(
                            "Close", 
                            on_click=[SignupFormState.setvar("show_dialog", False), AppState.set_landing_view("signin")],
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
            open=SignupFormState.show_dialog,
        )
    )






def alert():
    return rx.box(
        rx.dialog.root(
            rx.dialog.content(
                rx.vstack(
                    rx.heading(
                        "Group Successfully Created!",
                        font_size="26px",
                        align="center", 
                        color="green",
                        margin="20px",
                    ),
                    rx.text(f"Group ID: {GroupFormState.group_id}", font_size="16px"),
                    rx.text(f"Your User ID: {GroupFormState.admin_user_id}", font_size="16px"),
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
        )
    )



