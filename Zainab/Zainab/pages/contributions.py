import reflex as rx
from ..states.auth_state import AuthState
from ..states.contribution_state import ContributionState

def contribution_page():
    return rx.center(
        rx.vstack(
            rx.cond(
                ContributionState.view_history,
                rx.cond(
                    AuthState.is_authenticated,
                    rx.vstack(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID"),
                                    rx.table.column_header_cell("Amount"),
                                    rx.table.column_header_cell("Date"),
                                    rx.table.column_header_cell("Status"),
                                ),
                                background_color="#333300",
                                color="white",
                            ),
                            rx.table.body(
                                rx.foreach(
                                    ContributionState.paginated_contributions,
                                    lambda c: rx.table.row(
                                        rx.table.cell(rx.cond(c["contribution_id"], f"{c['contribution_id']}", "N/A")),
                                        rx.table.cell(rx.cond(c["amount"], f"₦{c['amount']:,}", "N/A")),
                                        rx.table.cell(rx.cond(c["contribution_date"], f"{c['contribution_date']}", "N/A")),
                                        rx.table.cell(rx.cond(c["status"], f"{c['status']}", "N/A")),
                                        style={"color": "#333300"},
                                    ),
                                ),
                            ),
                            variant="ghost",
                            width="100%",
                            overflow_x=rx.breakpoints(initial="auto", md="hidden"),
                        ),
                        rx.hstack(
                            rx.button(
                                "Previous", 
                                on_click=ContributionState.prev_page, 
                                disabled=ContributionState.current_page == 1, 
                                background_color="#333300",
                                size=rx.breakpoints(initial="1", md="2"),
                            ),
                            rx.text(f"Page {ContributionState.current_page}", color="#333300"),
                            rx.button(
                                "Next",
                                on_click=ContributionState.next_page,
                                disabled=(ContributionState.current_page * ContributionState.items_per_page) >= ContributionState.contributions_length,
                                background_color="#333300",
                                size=rx.breakpoints(initial="1", md="2"),
                            ),
                            spacing="2",
                            justify="between",
                            width="100%",
                            margin_top="1rem",
                        ),
                        width="100%",
                        padding=rx.breakpoints(initial="1rem", md="2rem"),
                        height="100%",
                        border_radius="md",
                    ),
                    rx.text("Please log in to view contributions.", color="#333300"),
                ),
                rx.vstack(
                    rx.cond(
                        ContributionState.contribution_status == "Completed",
                        rx.vstack(
                            rx.image(
                                src="/confirm.png",
                                width=rx.breakpoints(initial="80px", md="120px"),
                                height="auto",
                                border_radius="8px",
                            ),
                            rx.text(
                                "No pending contributions", 
                                color="green", 
                                text_align="center", 
                                weight="bold", 
                                font_size=rx.breakpoints(initial="14px", md="18px")
                            ),
                            rx.text(
                                f"Contributions for {ContributionState.current_year_month} completed",
                                color="#333300", 
                                text_align="center", 
                                weight="bold", 
                                font_size=rx.breakpoints(initial="12px", md="14px")
                            ),
                            align="center",
                            padding=rx.breakpoints(initial="1rem", md="2rem"),
                            spacing="3"
                        ),
                        rx.vstack(
                            rx.heading(
                                "Make Contributions",
                                size=rx.breakpoints(initial="5", md="6"),
                                color="#333300",
                                margin_top=rx.breakpoints(initial="1rem", md="2rem"),
                                text_align="center",
                            ),
                            rx.grid(
                                rx.text("Member ID:", color="#333300", text_align="right", weight="bold", 
                                       font_size=rx.breakpoints(initial="12px", md="14px")),
                                rx.text(f"{AuthState.user_id}", color="#333300", 
                                       font_size=rx.breakpoints(initial="12px", md="14px")),
                                rx.text("Member Name:", color="#333300", text_align="right", weight="bold", 
                                       font_size=rx.breakpoints(initial="12px", md="14px")),
                                rx.text(f"{AuthState.name}", color="#333300", 
                                       font_size=rx.breakpoints(initial="12px", md="14px")),
                                padding="2",
                                width="100%",
                                columns="2",
                                spacing_x="4",
                                spacing_y="2",
                            ),
                            rx.text(
                                f"{ContributionState.days_remaining} days left for {ContributionState.current_month} contributions",
                                color="#333300",
                                font_size=rx.breakpoints(initial="14px", md="16px"),
                                weight="bold",
                                text_align="center",
                            ),
                            rx.heading(
                                f"₦{ContributionState.expected_amount:,}",
                                size=rx.breakpoints(initial="6", md="8"),
                                color="red",
                                text_align="center",
                            ),
                            rx.text(
                                f"Status: {ContributionState.status}",
                                color="#333300",
                                font_size=rx.breakpoints(initial="14px", md="16px"),
                                text_align="center",
                            ),
                            spacing="4",
                            width="100%",
                            align="center",
                        ),
                    ),
                    width=rx.breakpoints(initial="90%", sm="80%", md="70%"),
                    align="center",
                ),
            ),
            rx.flex(
                rx.button(
                    rx.cond(ContributionState.view_history, "Back to Form", "View History"),
                    bg="#333300",
                    color="white",
                    border_radius="md",
                    padding="2",
                    width=rx.breakpoints(initial="140px", md="180px"),
                    height="45px",
                    _hover={"bg": "#4d4d33"},
                    on_click=ContributionState.toggle_view,
                    size=rx.breakpoints(initial="1", md="2"),
                ),
                rx.cond(
                    ContributionState.view_history,
                    rx.fragment(),
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.cond(
                            ContributionState.contribution_status == "Pending",
                            rx.button(
                                rx.cond(
                                    ContributionState.payment_loading,
                                    rx.spinner(size="2", color="white"),
                                    rx.text("Make Payment")
                                ),
                                bg="#CCCC33",
                                color="white",
                                border_radius="md",
                                padding="2",
                                width=rx.breakpoints(initial="140px", md="180px"),
                                height="45px",
                                _hover={"bg": "#4d4d33"},
                                on_click=ContributionState.initiate_contribution,
                                disabled=(ContributionState.amount == "" | ~ContributionState.is_amount_valid),
                                size=rx.breakpoints(initial="1", md="2"),
                            ),
                        ),
                        rx.text("Please log in to make payment", color="#333300"),
                    ),
                ),
                width="100%",
                justify_content="center",
                align_items="center",
                spacing="4",
                padding="0.3rem",
                margin_bottom="1.5rem",
            ),
            align="center",
            width=rx.breakpoints(initial="95%", sm="90%", md="80%"),
            padding=rx.breakpoints(initial="3", md="6"),
            spacing="6",
            bg="rgba(255, 255, 255, 0.9)",
            border_radius="10px",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        ),
        border_radius="10px",
        padding=rx.breakpoints(initial="1rem", md="2rem"),
        width="100%",
        on_mount=ContributionState.on_mount,
    )