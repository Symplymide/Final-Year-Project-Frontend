import reflex as rx
from ..states.auth_state import AuthState
from ..states.withdrawal_state import WithdrawalState

def withdraw_page():
    return rx.center(
        rx.vstack(
            rx.cond(
                WithdrawalState.view_history,
                rx.cond(
                    AuthState.is_authenticated,
                    rx.vstack(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID"),
                                    rx.table.column_header_cell("Amount (NGN)"),
                                    rx.table.column_header_cell("Date"),
                                    rx.table.column_header_cell("Status"),
                                ),
                                background_color="#333300",
                                color="white",
                            ),
                            rx.table.body(
                                rx.foreach(
                                    WithdrawalState.paginated_withdrawals,
                                    lambda w: rx.table.row(
                                        rx.table.cell(rx.cond(w["transaction_id"], f"{w['transaction_id']}", "N/A")),
                                        rx.table.cell(rx.cond(w["amount"], f"{w['amount']}", "N/A")),
                                        rx.table.cell(rx.cond(w["created_at"], f"{w['created_at']}", "N/A")),
                                        rx.table.cell(rx.cond(w["transaction_status"], f"{w['transaction_status']}", "N/A")),
                                        style={"color": "#333300"},
                                    ),
                                ),
                            ),
                            variant="ghost",
                            width="100%",
                        ),
                        rx.hstack(
                            rx.button("Previous", on_click=WithdrawalState.prev_page, disabled=WithdrawalState.current_page == 1, background_color="#333300"),
                            rx.text(f"Page {WithdrawalState.current_page}", color="#333300"),
                            rx.button(
                                "Next",
                                on_click=WithdrawalState.next_page,
                                disabled=(WithdrawalState.current_page * WithdrawalState.items_per_page) >= WithdrawalState.withdrawals_length,
                                background_color="#333300",
                            ),
                            spacing="2",
                            justify="between",
                            width="100%",
                            margin_top="1rem",
                        ),
                        width="100%",
                        padding=["1rem", "2rem"],  # Smaller padding on mobile
                        height="100%",
                        border_radius="md",
                    ),
                    rx.text("Please log in to view withdrawals.", color="#333300"),
                ),
                rx.vstack(
                    rx.cond(
                        WithdrawalState.is_payout,
                        rx.vstack(
                            rx.text(f"Amount Receivable{WithdrawalState.payout_date}", color="#333300", weight="bold", font_size=["16px", "18px"]),
                            rx.heading(f"NGN {WithdrawalState.amount_receivable:,}", color="green", text_align="center", weight="bold", font_size=["20px", "25px"]),

                            rx.text(f"Your withdrawal date", color="#333300", text_align="center", weight="bold", font_size=["16px", "18px"]),
                            rx.heading(f"{WithdrawalState.payout_date}", color="green", text_align="center", weight="bold", font_size=["20px", "25px"]),

                            rx.text(f"You have {WithdrawalState.days_remaining} days and {WithdrawalState.hours_remaining} hours remaining ", color="#333300", text_align="center", font_size=["12px", "14px"]),
                            
                            align="center",
                            padding=["1rem", "2rem"],  # Smaller padding on mobile
                            spacing="3"
                        ),

                        rx.vstack(
                            rx.heading(
                                "Withdraw Contributions",
                                size=rx.breakpoints(initial="5", md="6"),  # Smaller size on mobile
                                color="#333300",
                                margin_top=["1rem", "2rem"],  # Less margin on mobile
                                text_align="center",
                            ),
                            rx.heading(
                                f"Available Balance (NGN): {WithdrawalState.balance:,}",
                                size=rx.breakpoints(initial="2", md="2"),  # Smaller size on mobile
                                color="#333300",
                                margin_top="1rem",
                                text_align="center",
                            ),

                            rx.text(
                                f"Amount Receivable: {WithdrawalState.amount_receivable:,} NGN on {WithdrawalState.payout_date}",
                                color="#333300",
                                font_size=["12px", "14px"],  # Smaller font on mobile
                                weight="bold",
                            ),
                            rx.select(
                                WithdrawalState.banks,
                                placeholder="Select Bank",
                                value=WithdrawalState.bank,
                                on_change=WithdrawalState.set_bank,
                                width="100%",
                                height="40px",
                                color="white",
                                bg="white",
                                variant="surface",
                                border_color="#333300",
                                _hover={"border_color": "#4d4d33"},
                            ),
                            rx.input(
                                placeholder="Account Number",
                                value=WithdrawalState.account_number,
                                on_change=WithdrawalState.set_account_number,
                                width="100%",
                                height="40px",
                                color="white",
                                bg="#333333",
                                variant="surface",
                                border_color="#333300",
                                _hover={"border_color": "#4d4d33"},
                            ),

                            rx.hstack(
                                rx.cond(
                                    WithdrawalState.account_loading,
                                    rx.spinner(size="2", color="green"),
                                ),
                                rx.text(
                                    f"{WithdrawalState.account_name}",
                                    color="green",
                                    font_size=["10px", "12px"],  # Smaller font on mobile
                                    weight="bold",
                                    text_align="left",
                                ),
                                justify_content="start",
                            ),

                            rx.input(
                                placeholder="Amount to Withdraw",
                                value=WithdrawalState.amount,
                                on_change=WithdrawalState.set_amount,
                                width="100%",
                                height="40px",
                                color="white",
                                bg="#333333",
                                variant="surface",
                                border_color="#333300",
                                _hover={"border_color": "#4d4d33"},
                            ),
                            width="100%",
                            align="center"
                        ),
                        
                    ),
                    
                    width=["100%", "60%"],  # Wider on mobile, narrower on desktop
                    align="center",
                    spacing="4",
                ),
            ),
            rx.flex(
                rx.button(
                    rx.cond(WithdrawalState.view_history, "Back to Form", "View History"),
                    bg="#333300",
                    color="white",
                    border_radius="md",
                    padding="2",
                    width=["150px", "180px"],  # Narrower buttons on mobile
                    height="45px",
                    _hover={"bg": "#4d4d33"},
                    on_click=WithdrawalState.toggle_view,
                ),
                rx.cond(
                    WithdrawalState.view_history,
                    rx.fragment(),
                    rx.cond(
                        AuthState.is_authenticated & ~WithdrawalState.is_payout,
                        rx.button(
                            "Withdraw Money",
                            bg="#CCCC33",
                            color="white",
                            border_radius="md",
                            padding="2",
                            width=["150px", "180px"],  # Narrower buttons on mobile
                            height="45px",
                            _hover={"bg": "#4d4d33"},
                            on_click=WithdrawalState.withdraw,
                            disabled=(WithdrawalState.amount == "" | ~WithdrawalState.is_amount_valid | WithdrawalState.loading),
                        ),
                    ),
                ),
                width="100%",
                justify="center",
                align="center",
                spacing="4",
                padding="0.3rem",
                margin_bottom="1.5rem",
                wrap="wrap",
            ),
            align="center",
            width=rx.breakpoints(initial="100%", md="80%"),  # Wider on mobile, narrower on desktop
            padding=rx.breakpoints(initial="1rem", md="4rem"),  # Less padding on mobile
            spacing="6",
            bg="rgba(255, 255, 255, 0.9)",
            border_radius="10px",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        ),
        border_radius="10px",
        padding=rx.breakpoints(initial="1rem", md="2rem"),  # Smaller padding on mobile
        width="100%",
        on_mount=WithdrawalState.on_mount,
    )