import reflex as rx
from ..states.app_state import AppState
from ..states.auth_state import AuthState
from ..states.notification_state import NotificationState


nav_style = dict(
    padding=".5em",
    text_align="center",
    cursor="pointer",
    width="100%",
    box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",  # Adding shadow for better UI
)

active_style = dict(
    **nav_style,
    background_color=rx.color("accent", 8),  # Using Reflex color system
)

def nav_item(text: str, message: int=None) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(text),
            rx.text(
                rx.cond(message != None, f'{message}', ""),
                margin_left="3rem",
                ),
            spacing="3",
            justify="start",
            width="100%",
        ),
        color=rx.cond(
            AppState.current_page == text,
            "gray.200", 
            "#CCCC33"
        ),
        background=rx.cond(
            AppState.current_page == text,
            "rgba(255, 255, 255, 0.1)",
            "transparent"
        ),
        on_click=[AppState.set_home_page(text), AppState.toggle_menu],
        style=nav_style,
        _hover={
            "background": "rgba(255, 255, 255, 0.05)",
            "transform": "translateY(-2px)",
            "transition": "all 0.2s ease-in-out"
        },
        _active={
            "transform": "scale(0.98)",
            "transition": "all 0.1s ease-in-out"
        },
    )


def sign_out_nav(text: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(text),
            spacing="3",
            justify="start",
            width="100%",
        ),
        color=rx.cond(
            AppState.current_page == text,
            "gray.200", 
            "#CCCC33"
        ),
        background=rx.cond(
            AppState.current_page == text,
            "rgba(255, 255, 255, 0.1)",
            "transparent"
        ),
        on_click=AuthState.open_dialog(),
        style=nav_style,
        _hover={
            "background": "rgba(255, 255, 255, 0.05)",
            "transform": "translateY(-2px)",
            "transition": "all 0.2s ease-in-out"
        },
        _active={
            "transform": "scale(0.98)",
            "transition": "all 0.1s ease-in-out"
        },
    )


def side_navbar():
    return rx.box(
        rx.vstack(
            # Navigation items group
            rx.vstack(
                nav_item("Dashboard"),
                nav_item("Members"),
                nav_item("Contribution"),
                nav_item("Withdrawal"),
                nav_item("Schedule"),
                nav_item("Transactions"),
                nav_item("Notification", f"{NotificationState.message_count}"),
                nav_item("Activity Logs"),
                sign_out_nav("Logout"),
                spacing="0",
                width="100%",
            ),
            
            height="100%",  # Take full height
            width="100%",
            spacing="0",
        ),
        position="fixed",
        # height="30vh",
        width="50vw",
        right="0",
        top="0",
        padding="1rem",
        border_radius="15px",
        padding_top="4rem",
        background_color="#333300",
        z_index="1000",  # Ensure it is above other content
        
    )
