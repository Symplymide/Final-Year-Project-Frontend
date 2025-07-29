import reflex as rx
from ..states.auth_state import AuthState
from ..states.schedule_withdrawal_state import ScheduleWithdrawalState

def schedule_withdrawal_page():
    return rx.center(
        rx.vstack(
            rx.cond(
                ScheduleWithdrawalState.view_history,
                rx.cond(
                    AuthState.is_authenticated,
                    rx.vstack(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID"),
                                    rx.table.column_header_cell("Name"),
                                    rx.table.column_header_cell("Start"),
                                    rx.table.column_header_cell("End"),
                                    rx.table.column_header_cell("Target(NGN)"),
                                    rx.table.column_header_cell("Amount(NGN)"),
                                    rx.table.column_header_cell("Status"),
                                ),
                                background_color="#333300",
                                color="white",
                                font_size="12px",
                            ),
                            rx.table.body(
                                rx.foreach(
                                    ScheduleWithdrawalState.paginated_schedules,
                                    lambda w: rx.table.row(
                                        rx.table.cell(rx.cond(w["schedule_id"], f"{w['schedule_id']}", "N/A")),
                                        rx.table.cell(rx.cond(w["schedule_name"], f"{w['schedule_name']}", "N/A")),
                                        rx.table.cell(rx.cond(w["start_date"], f"{w['start_date']}", "N/A")),
                                        rx.table.cell(rx.cond(w["end_date"], f"{w['end_date']}", "N/A")),
                                        rx.table.cell(rx.cond(w["total_target_amount"], f"{w['total_target_amount']}", "N/A")),
                                        rx.table.cell(rx.cond(w["aggregate_contribution_amount"], f"{w['aggregate_contribution_amount']}", "N/A")),
                                        rx.table.cell(rx.cond(w["status"], f"{w['status']}", "N/A")),
                                        style={"color": "#333300"},
                                    ),
                                ),
                                font_size="12px",
                            ),
                            variant="ghost",
                            width="100%",
                        ),
                        rx.hstack(
                            rx.button("Previous", on_click=ScheduleWithdrawalState.prev_page, disabled=ScheduleWithdrawalState.current_page == 1, background_color="#333300"),
                            rx.text(f"Page {ScheduleWithdrawalState.current_page}", color="#333300"),
                            rx.button(
                                "Next",
                                on_click=ScheduleWithdrawalState.next_page,
                                disabled=(ScheduleWithdrawalState.current_page * ScheduleWithdrawalState.items_per_page) >= ScheduleWithdrawalState.schedule_length,
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
                rx.vstack(
                    rx.heading(
                        "Create Withdrawal Schedule",
                        size="6",
                        color="#333300",
                        margin_top="2rem",
                        text_align="center",
                    ),
                    rx.cond(
                        AuthState.role_name == "Moderator",
                        rx.vstack(
                            rx.cond(
                                ScheduleWithdrawalState.active_schedule,
                                rx.text(f"{ScheduleWithdrawalState.active_schedule} is currently active!.", color="green"),
                            ),
                            rx.input(
                                placeholder="Schedule Name",
                                value=ScheduleWithdrawalState.schedule_name,
                                on_change=ScheduleWithdrawalState.set_schedule_name,
                                width="100%",
                                height="40px",
                                color="white",
                                bg="#333333",
                                variant="surface",
                                border_color="#333300",
                                _hover={"border_color": "#4d4d33"},
                            ),
                            rx.input(
                                type_="date",
                                placeholder="Start Date",
                                value=ScheduleWithdrawalState.start_date,
                                on_change=ScheduleWithdrawalState.set_start_date,
                                width="100%",
                                height="40px",
                                color="white",
                                bg="#333333",
                                variant="surface",
                                border_color="#333300",
                                _hover={"border_color": "#4d4d33"},
                            ),
                            rx.input(
                                type_="date",
                                placeholder="End Date",
                                value=ScheduleWithdrawalState.end_date,
                                on_change=ScheduleWithdrawalState.set_end_date,
                                width="100%",
                                height="40px",
                                color="white",
                                bg="#333333",
                                variant="surface",
                                border_color="#333300",
                                _hover={"border_color": "#4d4d33"},
                            ),
                            rx.input(
                                placeholder="Total Target Amount (NGN)",
                                value=ScheduleWithdrawalState.total_target_amount,
                                on_change=ScheduleWithdrawalState.set_total_target_amount,
                                width="100%",
                                height="40px",
                                color="white",
                                bg="#333333",
                                variant="surface",
                                border_color="#333300",
                                _hover={"border_color": "#4d4d33"},
                            ),
                            spacing="4",
                            width="70%",
                            align="center",
                        ),
                        rx.text("Only Moderators can create withdrawal schedules.", color="#333300"),
                    ),
                    spacing="4",
                    width="70%",
                    align="center",
                ),
            ),
            rx.flex(
                rx.button(
                    rx.cond(ScheduleWithdrawalState.view_history, 
                            "Back to Form", 
                            "View Schedules"),
                    bg="#333300",
                    color="white",
                    border_radius="md",
                    padding="2",
                    width="180px",
                    height="45px",
                    _hover={"bg": "#4d4d33"},
                    on_click=ScheduleWithdrawalState.toggle_view,
                ),
                rx.cond(
                    ScheduleWithdrawalState.view_history,
                    rx.fragment(),
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.button(
                            "Create Schedules",
                            bg="#CCCC33",
                            color="white",
                            border_radius="md",
                            padding="2",
                            width="180px",
                            height="45px",
                            _hover={"bg": "#4d4d33"},
                            on_click=ScheduleWithdrawalState.create_schedule,
                            disabled=(~ScheduleWithdrawalState.is_form_valid | ScheduleWithdrawalState.loading),
                        ),
                        rx.text("Please log in to withdraw.", color="#333300"),
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
    )


def dialog():
    return rx.dialog.root(
        rx.dialog.trigger(rx.fragment()),  # No visible trigger; controlled by state
        rx.dialog.content(
            rx.dialog.title("Confirm Deactivation", color="#333300"),
            rx.dialog.description(
                f'Are you sure you want to deactivate schedule "{ScheduleWithdrawalState.selected_schedule_id}"?',
                color="#333300",
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        bg="#333300",
                        color="white",
                        _hover={"bg": "#4d4d33"},
                        on_click=ScheduleWithdrawalState.close_deactivate_dialog,
                    )
                ),
                rx.button(
                    "Confirm",
                    bg="#CCCC33",
                    color="white",
                    _hover={"bg": "#4d4d33"},
                    on_click=ScheduleWithdrawalState.confirm_deactivate,
                ),
                spacing="2",
                justify="end",
                margin_top="1rem",
            ),
            bg="#ffffff",
        ),
        open=ScheduleWithdrawalState.is_deactivate_dialog_open,
    ),