import reflex as rx
from datetime import datetime
from ..states.auth_state import AuthState
from ..states.notification_state import NotificationState


def notification_page():
    return rx.center(
        rx.vstack(
            rx.cond(
                NotificationState.view_history,
                rx.cond(
                    AuthState.is_authenticated,
                    rx.vstack(
                        rx.heading(
                            "All Notification / Reminder",
                            size=rx.breakpoints(initial="5", md="6"),  # Smaller on mobile
                            color="#333300",
                            text_align="center",
                        ),
                        rx.cond(
                            NotificationState.loading,
                            rx.spinner(size="3", color="#333300"),
                            rx.box(
                                rx.grid(
                                    rx.foreach(
                                        NotificationState.formatted_paginated_notifications,
                                        lambda message: rx.card(
                                            rx.vstack(
                                                rx.hstack(
                                                    rx.text(
                                                        f"{message['title']}", 
                                                        font_weight="bold", 
                                                        color="#333300",
                                                        font_size=["12px", "14px"]  # Smaller on mobile
                                                    ),
                                                    rx.hstack(
                                                        rx.text(f"{message['message_id']}", color="white", font_size="10px"),
                                                        rx.text(f"{message['is_active']}", color="orange", font_size="10px"),
                                                        rx.text(
                                                            f"{message['message_type']}", 
                                                            color="#333300", 
                                                            font_size=["10px", "12px"]  # Smaller on mobile
                                                        ),
                                                        spacing="2",  # Reduced spacing on mobile
                                                    ),
                                                    justify="between",
                                                    width="100%",
                                                ),
                                                spacing="1",  # Reduced spacing on mobile
                                            ),
                                            width="100%",
                                            padding=["1rem", "2rem"],  # Less padding on mobile
                                            border_radius="md",
                                            cursor="pointer",
                                            on_click=NotificationState.open_dialog(message['message_id']),
                                            _hover={
                                                "background": "rgba(255, 255, 255, 0.05)",
                                                "transform": "translateY(-2px)",
                                                "transition": "all 0.2s ease-in-out"
                                            },
                                        ),
                                    ),
                                    columns="1",
                                    spacing="3",  # Reduced spacing on mobile
                                    width="100%",
                                    padding_bottom="0.2rem",
                                ),
                                max_height="50vh",
                                overflow_y="auto",
                                width="100%",
                            ),
                        ),
                        width="100%",
                        padding=["1rem", "2rem"],  # Less padding on mobile
                        padding_bottom="0.2rem",
                        height="100%",
                        border_radius="md",
                        align="center",
                    ),
                    rx.text("Please log in to view Notifications", color="#333300"),
                ),
                rx.vstack(
                    rx.heading(
                        "Create Notification / Reminder",
                        size=rx.breakpoints(initial="5", md="6"),  # Smaller on mobile
                        color="#333300",
                        margin_top=["1rem", "2rem"],  # Less margin on mobile
                        text_align="center",
                    ),
                    rx.cond(
                        AuthState.role_name == "Moderator",
                        rx.vstack(
                            rx.data_list.root(
                                rx.data_list.item(
                                    rx.data_list.label(
                                        "Message Type:", 
                                        color="#333300", 
                                        text_align="right",
                                        font_size=["12px", "14px"]  # Smaller on mobile
                                    ),
                                    rx.data_list.value(
                                        rx.radio_group(
                                            ["Notification", "Reminder"],
                                            spacing="3",  # Reduced spacing on mobile
                                            direction=rx.breakpoints(initial="column", md="row"),  # Stack vertically on mobile
                                            color="#333300",
                                            value=NotificationState.message_type,
                                            on_change=NotificationState.set_message_type,
                                        ),
                                    ),
                                    spacing="3",  # Reduced spacing on mobile
                                ),
                                rx.data_list.item(
                                    rx.data_list.label(
                                        "Message Title:", 
                                        color="#333300", 
                                        text_align="right",
                                        font_size=["12px", "14px"]  # Smaller on mobile
                                    ),
                                    rx.data_list.value(
                                        rx.input(
                                            placeholder="Message Title",
                                            value=NotificationState.message_title,
                                            on_change=NotificationState.set_message_title,
                                            width="100%",
                                            height="40px",
                                            color="white",
                                            bg="#333333",
                                            variant="surface",
                                            border_color="#333300",
                                            _hover={"border_color": "#4d4d33"},
                                        ),
                                    ),
                                    spacing="3",  # Reduced spacing on mobile
                                ),
                                rx.data_list.item(
                                    rx.data_list.label(
                                        "Message Content:", 
                                        color="#333300", 
                                        text_align="right",
                                        font_size=["12px", "14px"]  # Smaller on mobile
                                    ),
                                    rx.data_list.value(
                                        rx.text_area(
                                            placeholder="Message Content",
                                            value=NotificationState.message_content,
                                            on_change=NotificationState.set_message_content,
                                            width="100%",
                                            height="80px",
                                            color="white",
                                            bg="#333333",
                                            variant="surface",
                                            border_color="#333300",
                                            _hover={"border_color": "#4d4d33"},
                                        ),
                                    ),
                                    spacing="3",  # Reduced spacing on mobile
                                ),
                                rx.data_list.item(
                                    rx.data_list.label(
                                        "Delivery Type:", 
                                        color="#333300", 
                                        text_align="right",
                                        font_size=["12px", "14px"]  # Smaller on mobile
                                    ),
                                    rx.data_list.value(
                                        rx.radio_group(
                                            ["In_app", "Email"],
                                            spacing="3",  # Reduced spacing on mobile
                                            direction=rx.breakpoints(initial="column", md="row"),  # Stack vertically on mobile
                                            color="#333300",
                                            value=NotificationState.delivery_type,
                                            on_change=NotificationState.set_delivery_type,
                                        ),
                                    ),
                                    spacing="3",  # Reduced spacing on mobile
                                ),
                                rx.data_list.item(
                                    rx.data_list.label(
                                        "Reminder Date:", 
                                        color="#333300", 
                                        text_align="right",
                                        font_size=["12px", "14px"]  # Smaller on mobile
                                    ),
                                    rx.data_list.value(
                                        rx.input(
                                            type="date",
                                            placeholder="Reminder Date",
                                            value=NotificationState.reminder_date,
                                            on_change=NotificationState.set_reminder_date,
                                            width="100%",
                                            height="40px",
                                            color="white",
                                            bg="#333333",
                                            variant="surface",
                                            border_color="#333300",
                                            _hover={"border_color": "#4d4d33"},
                                        ),
                                    ),
                                    spacing="3",  # Reduced spacing on mobile
                                ),
                                align="center",
                                width="100%",
                            ),
                            rx.select(
                                NotificationState.recipients_type,
                                placeholder="Select Recipient Type",
                                value=NotificationState.recipient,
                                on_change=NotificationState.set_recipients,
                                width="100%",
                                height="40px",
                                color="white",
                                bg="white",
                                variant="surface",
                                border_color="#333300",
                                _hover={"border_color": "#4d4d33"},
                            ),
                            spacing="3",  # Reduced spacing on mobile
                            width=rx.breakpoints(initial="90%", md="70%"),  # Wider on mobile
                            align="center",
                        ),
                        rx.text("Only Moderators can create notifications.", color="#333300"),
                    ),
                    spacing="3",  # Reduced spacing on mobile
                    width=rx.breakpoints(initial="90%", md="70%"),  # Wider on mobile
                    align="center",
                ),
            ),
            rx.flex(
                rx.button(
                    rx.cond(NotificationState.view_history, "Back to Form", "View Notifications"),
                    bg="#333300",
                    color="white",
                    border_radius="md",
                    padding="2",
                    width=rx.breakpoints(initial="150px", md="180px"),  # Narrower on mobile
                    height="45px",
                    _hover={"bg": "#4d4d33"},
                    on_click=NotificationState.toggle_view,
                ),
                rx.cond(
                    NotificationState.view_history,
                    rx.fragment(),
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.button(
                            "Save Notifications",
                            bg="#CCCC33",
                            color="white",
                            border_radius="md",
                            padding="2",
                            width=rx.breakpoints(initial="150px", md="180px"),  # Narrower on mobile
                            height="45px",
                            _hover={"bg": "#4d4d33"},
                            on_click=NotificationState.create_notification,
                            disabled=(NotificationState.loading),
                        ),
                    ),
                ),
                width="100%",
                justify_content="center",
                align_items="center",
                spacing="3",  # Reduced spacing on mobile
                padding="0.3rem",
                margin_bottom="1.5rem",
            ),
            align="center",
            width=rx.breakpoints(initial="95%", md="80%"),  # Wider on mobile
            padding=rx.breakpoints(initial="3", md="6"),  # Less padding on mobile
            spacing="4",  # Reduced spacing on mobile
            bg="rgba(255, 255, 255, 0.9)",
            border_radius="10px",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
            overflow_y="auto",
        ),
        nofication_dialog(),
        border_radius="10px",
        padding=rx.breakpoints(initial="1rem", md="2rem"),  # Less padding on mobile
        width="100%",
        overflow="hidden",
    )


def nofication_dialog():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                NotificationState.selected_title, 
                color="#333300", 
                magin_bottom="2rem",
                font_size=["14px", "16px"]  # Smaller on mobile
            ),
            rx.vstack(
                rx.vstack(
                    rx.text(
                        NotificationState.selected_content, 
                        font_size=["12px", "14px"],  # Smaller on mobile
                        color="#333300"
                    ),
                    spacing="1",
                    justify="center",
                ),
                rx.hstack(
                    rx.text(
                        NotificationState.selected_message_type, 
                        color="#333300",  
                        font_weight="bold", 
                        font_size=["12px", "14px"]  # Smaller on mobile
                    ),
                    rx.text(
                        NotificationState.selected_date, 
                        font_size=["12px", "14px"],  # Smaller on mobile
                        color="#333300"
                    ),
                    justify="between",
                    width="100%",
                    padding_top=["1rem", "2rem"],  # Less padding on mobile
                ),
                spacing="2",
                padding=["1rem", "2rem"]  # Less padding on mobile
            ),
            rx.dialog.close(
                rx.button(
                    "Close",
                    bg="#333300",
                    color="white",
                    _hover={"bg": "#4d4d33"},
                    on_click=NotificationState.close_dialog,
                ),
                padding=["0.5rem", "1rem"]  # Less padding on mobile
            ),
            padding=["1rem", "2rem"],  # Less padding on mobile
            bg="#ffffff",
        ),
        open=NotificationState.show_dialog,
    )