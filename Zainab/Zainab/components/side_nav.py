import reflex as rx
from ..states.app_state import AppState
from ..states.auth_state import AuthState
from ..states.notification_state import NotificationState


nav_style = dict(
    padding="1em",
    text_align="left",
    cursor="pointer",
    width="100%",
    box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",  # Adding shadow for better UI
)

active_style = dict(
    **nav_style,
    background_color=rx.color("accent", 8),  # Using Reflex color system
)

def nav_item(text: str, icon: str, message: int=None) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(icon),
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
        on_click=AppState.set_home_page(text),
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


def sign_out_nav(text: str, icon: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(icon),
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
                nav_item("Dashboard", "home"),
                nav_item("Members", "users"),
                nav_item("Contribution", "coins"),
                nav_item("Withdrawal", "hand-coins"),
                nav_item("Schedule", "calendar"),
                nav_item("Transactions", "arrow-left-right"),
                nav_item("Notification", "bell", f"{NotificationState.message_count}"),
                nav_item("Activity Logs", "activity"),
                sign_out_nav("Logout", "log_out"),
                spacing="0",
                width="100%",
            ),
            # Footer group
            rx.spacer(),  # This pushes the footer to the bottom
            rx.box(
                rx.text(
                    "© 2024 - 2025, Quoin-lab Technology",
                    color="white",
                    font_size="12px",
                ),
                padding="1em",
                width="100%",
                text_align="center",
            ),
            height="100%",  # Take full height
            width="100%",
            spacing="0",
        ),
        position="fixed",
        height="100vh",
        width="240px",
        left="0",
        top="0",
        padding_top="6em",
        
    )




    