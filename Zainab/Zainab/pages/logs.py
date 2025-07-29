import reflex as rx
from ..states.auth_state import AuthState
from ..states.log_state import AccessLogState

def activity_log_page():
    return rx.center(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Member Access Logs",
                    size="6",
                    color="#333300",
                    margin_top="2rem",
                    text_align="center",
                ),
                rx.vstack(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("ID"),
                                rx.table.column_header_cell("User ID"),
                                rx.table.column_header_cell("Log In"),
                                rx.table.column_header_cell("Log Out"),
                                rx.table.column_header_cell("IP Address"),
                            ),
                            background_color="#333300",
                            color="white",
                        ),
                        rx.table.body(
                            rx.foreach(
                                AccessLogState.paginated_logs,
                                lambda w, idx: rx.table.row(
                                    rx.table.cell(rx.cond(w["log_id"], idx+1, "N/A")),
                                    rx.table.cell(rx.cond(w["user_id"], w["user_id"], "N/A")),
                                    rx.table.cell(rx.cond(w["login_time"], w["login_time"], "N/A")),
                                    rx.table.cell(rx.cond(w["logout_time"], w["logout_time"], "N/A")),
                                    rx.table.cell(rx.cond(w["ip_address"], w["ip_address"], "N/A")),
                                    style={
                                        "background_color": rx.cond(
                                            idx % 2 == 0,
                                            "#f0f0f0",  # Light gray for even rows
                                            "#ffffff",  # White for odd rows
                                        ),
                                        "color": "#333300",
                                        "font_size": "14px",
                                        "padding": "10px",
                                    },
                                ),
                            ),
                        ),
                        variant="ghost",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            "Previous",
                            on_click=AccessLogState.prev_page,
                            disabled=AccessLogState.current_page == 1,
                            background_color="#333300",
                            color="white",
                            _hover={"bg": "#4d4d33"},
                        ),
                        rx.text(f"Page {AccessLogState.current_page}", color="#333300"),
                        rx.button(
                            "Next",
                            on_click=AccessLogState.next_page,
                            disabled=(AccessLogState.current_page * AccessLogState.items_per_page) >= AccessLogState.log_length,
                            background_color="#333300",
                            color="white",
                            _hover={"bg": "#4d4d33"},
                        ),
                        spacing="2",
                        justify="between",
                        width="100%",
                        margin_top="1rem",
                    ),
                    width="100%",
                    padding="1rem",
                    height="100%",
                    border_radius="md",
                ),
                spacing="4",
                width="90%",
                align="center",
            ),
            
            rx.flex(
                rx.button(
                    "Refresh",
                    bg="#333300",
                    color="white",
                    border_radius="md",
                    padding="2",
                    width="180px",
                    height="45px",
                    _hover={"bg": "#4d4d33"},
                    on_click=AccessLogState.fetch_logs,
                ),
                width="100%",
                justify_content="center",
                align_items="center",
                spacing="4",
                padding="0.3rem",
                margin_bottom="1.5rem",
            ),
            align="center",
            width="80%",
            padding="6",
            spacing="6",
            bg="rgba(255, 255, 255, 0.9)",
            border_radius="10px",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
            overflow_y="auto",
        ),
        border_radius="10px",
        padding="2rem",
        width="100%",
        overflow="hidden",
        on_mount=AccessLogState.on_mount,
    )