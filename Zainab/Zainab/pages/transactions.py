import reflex as rx
from ..states.auth_state import AuthState
from ..states.transaction_state import TransactionState

def transaction_page():
    return rx.center(
        rx.vstack(
            rx.cond(
                AuthState.is_authenticated,
                rx.vstack(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("ID"),
                                rx.table.column_header_cell("Amount (NGN)"),
                                rx.table.column_header_cell("Ref."),
                                rx.table.column_header_cell("Type"),
                                rx.table.column_header_cell("Date"),
                                rx.table.column_header_cell("Status"),
                            ),
                            background_color="#333300",
                            color="white",
                        ),
                        rx.table.body(
                            rx.foreach(
                                TransactionState.paginated_transactions,
                                lambda w, idx: rx.table.row(
                                    rx.table.cell(rx.cond(w["transaction_id"], idx+1, "N/A")),
                                    rx.table.cell(rx.cond(w["amount"], f"{w['amount']}", "N/A")),
                                    rx.table.cell(rx.cond(w["transaction_reference"], f"{w['transaction_reference']}", "N/A")),
                                    rx.table.cell(rx.cond(w["transaction_type"], f"{w['transaction_type']}", "N/A")),
                                    rx.table.cell(rx.cond(w["created_at"], f"{w['created_at']}", "N/A")),
                                    rx.table.cell(rx.cond(w["transaction_status"], f"{w['transaction_status']}", "N/A")),
                                    style={
                                        "background_color": rx.cond(
                                            idx % 2 == 0,
                                            "#f0f0f0",  
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
                        rx.button("Previous", on_click=TransactionState.prev_page, disabled=TransactionState.current_page == 1, background_color="#333300"),
                        rx.text(f"Page {TransactionState.current_page}", color="#333300"),
                        rx.button(
                            "Next",
                            on_click=TransactionState.next_page,
                            disabled=(TransactionState.current_page * TransactionState.items_per_page) >= TransactionState.transaction_length,
                            background_color="#333300",
                        ),
                        spacing="2",
                        justify="between",
                        width="100%",
                        margin_top="1rem",
                    ),
                    width="100%",
                    padding="2rem",
                    height="100%",
                    border_radius="md",
                ),
                rx.text("Please log in to view withdrawals.", color="#333300"),
            ),
            
            rx.flex(
                rx.button(
                    "Refresh Data",
                    bg="#333300",
                    color="white",
                    border_radius="md",
                    padding="2",
                    width="180px",
                    height="45px",
                    _hover={"bg": "#4d4d33"},
                    on_click=TransactionState.refresh_view,
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
        ),
        border_radius="10px",
        padding="2rem",
        width="100%",
        on_mount=TransactionState.on_mount,
    )