import reflex as rx
from ..states.auth_state import AuthState
from ..states.user_state import UserDataState

def users_page():
    return rx.fragment(
        rx.center(
            rx.vstack(
                rx.vstack(
                    rx.heading(
                        "All Members",
                        size=rx.breakpoints(initial="5", md="6"),
                        color="#333300",
                        text_align="center",
                    ),
                    rx.cond(
                        UserDataState.loading,
                        rx.spinner(size="3", color="#333300"),
                        rx.grid(
                            rx.foreach(
                                UserDataState.all_users,
                                lambda user: member_card(user["name"], user["user_id"])
                            ),
                            columns=rx.breakpoints(initial="2", sm="3", md="4"),
                            spacing=rx.breakpoints(initial="4", md="7"),
                            width="100%",
                            padding=rx.breakpoints(initial="0.5rem", md="1rem"),
                            max_height="70vh",
                            overflow_y="auto",
                        ),
                    ),
                    spacing="4",
                    width=rx.breakpoints(initial="95%", md="90%"),
                    align="center",
                ),
                align="center",
                width="100%",
                spacing="6",
            ),
            border_radius="10px",
            padding_x=rx.breakpoints(initial="0.5rem", md="2rem"),
            width="100%",
            on_mount=UserDataState.on_mount,
        ),
        user_details_dialog(),
    )

def member_card(name: str, member_id: str):
    return rx.card(
        rx.vstack(
            rx.image(
                src="/user_pics.png",
                width=rx.breakpoints(initial="40%", md="50%"),
                height="auto",
                border_radius="8px",
            ),
            rx.heading(
                name, 
                size=rx.breakpoints(initial="3", md="4"), 
                color="#333300",
                text_align="center"
            ),
            rx.text(f"ID: {member_id}", color="#666633", font_size=rx.breakpoints(initial="10px", md="12px")),
            rx.button(
                "View Profile",
                on_click=lambda: UserDataState.open_dialog(member_id),
                bg="#333300",
                color="white",
                _hover={"bg": "#666633"},
                width="100%",
                size=rx.breakpoints(initial="1", md="2"),
            ),
            spacing="2",
            align="center",
            padding=rx.breakpoints(initial="0.5rem", md="1rem"),
        ),
        width="100%",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    )

def user_details_dialog():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "User Details", 
                color="#333300", 
                margin_bottom="1rem",
                size=rx.breakpoints(initial="4", md="5")
            ),
            rx.flex(
                rx.vstack(
                    rx.image(
                        src="/user_pics.png",
                        width=rx.breakpoints(initial="80px", md="120px"),
                        height="auto",
                        border_radius="8px",
                    ),
                    width=rx.breakpoints(initial="100%", md="40%"),
                    justify="center",
                    align="center",
                    padding_top="1rem",
                ),
                rx.flex(
                    rx.hstack(
                        rx.vstack(
                            rx.text("Name:", color="#333300", font_size="12px", font_weight="bold"),
                            rx.text("ID:", color="#333300", font_size="12px", font_weight="bold"),
                            rx.text("Phone:", color="#333300", font_size="12px", font_weight="bold"),
                            rx.text("Email:", color="#333300", font_size="12px", font_weight="bold"),
                            rx.text("Role:", color="#333300", font_size="12px", font_weight="bold"),
                            rx.text("Status:", color="#333300", font_size="12px", font_weight="bold"),
                            rx.text("Last Login:", color="#333300", font_size="12px", font_weight="bold"),
                            width="100px",
                            align="start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text(UserDataState.selected_user_name, font_size="12px", width="100%"),
                            rx.text(UserDataState.selected_user_id, font_size="12px", width="100%"),
                            rx.text(UserDataState.selected_user_phone, font_size="12px", width="100%"),
                            rx.text(UserDataState.selected_user_email, font_size="12px", width="100%"),
                            rx.text(UserDataState.selected_user_role, font_size="12px", width="100%"),
                            rx.text(rx.cond(UserDataState.selected_user_active, "Active", "Inactive"), font_size="12px", width="100%"),
                            rx.text(f"{UserDataState.selected_user_last_login}", font_size="12px", width="100%"),
                            width="100%",
                            align="start",
                            spacing="1",
                            color="#666633",
                        ),
                    ),
                    direction=rx.breakpoints(initial="column", md="row"),
                    spacing="2",
                ),
                direction=rx.breakpoints(initial="column", md="row"),
                spacing="4",
                width="100%",
            ),
            rx.dialog.close(
                rx.button(
                    "Close",
                    bg="#333300",
                    color="white",
                    _hover={"bg": "#4d4d33"},
                    on_click=UserDataState.close_dialog,
                    size=rx.breakpoints(initial="1", md="2"),
                    width="100%",
                ),
                padding_top="1rem",
                width="100%",
            ),
            padding=rx.breakpoints(initial="1rem", md="2rem"),
            bg="#ffffff",
            width=rx.breakpoints(initial="90vw", md="auto"),
        ),
        open=UserDataState.show_dialog,
    )