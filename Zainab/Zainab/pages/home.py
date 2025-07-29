import reflex as rx
from ..components import footer, nav, side_nav, icon_side_nav
from . import dashboard, contributions, withdrawal, schedule, transactions, notification, logs, users
from ..states.app_state import AppState
from ..states.auth_state import AuthState
from ..states.contribution_state import ContributionState
from ..states.dashboard_state import DashboardState

def home_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            nav.navbar(),
            rx.mobile_and_tablet(
                rx.cond(
                    AppState.is_menu,
                    icon_side_nav.side_navbar(),
                ),
                width="100%",
                height="100%",
            ),
            rx.hstack(
                rx.desktop_only(
                    rx.hstack(
                        side_nav.side_navbar(),
                        width="100%",
                        height="100%",
                        background_color="#333300",
                    ),
                    width="240px",
                    height="calc(100vh - 70px)",
                    position="fixed",
                    top="70px",
                    left="0",
                ),
                
                rx.box(
                    rx.hstack(
                        rx.hstack(
                            rx.desktop_only(rx.text("Group ID:", font_size="18px")),
                            rx.text(f"{AuthState.group_id}", font_size=rx.breakpoints(initial="14px", md="18px"), font_weight="bold"),
                            rx.cond(DashboardState.loading, rx.spinner(size="2", color="green"), rx.icon("circle-arrow-right", size=14)),
                            color="#333300",
                            align="center",
                            cursor="pointer",
                            on_click=DashboardState.show_group_details,
                            _hover={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "transform": "translateY(-2px)",
                                "transition": "all 0.2s ease-in-out"
                            }
                        ),
                        rx.hstack(
                            rx.desktop_only(rx.text("Active Contribution:", font_size="12px")),
                            rx.text(f"{DashboardState.group_details['group_name']}", font_size=rx.breakpoints(initial="14px", md="16px"), font_weight="bold"),
                            color="#333300",
                            align="center",
                            cursor="pointer",
                        ),
                        rx.hstack(
                            rx.text(f"{AuthState.today}", font_size=rx.breakpoints(initial="12px", md="14px")),
                            color="#333300",
                            align="center",
                        ),
                        border_bottom="2px solid rgba(51, 51, 0, 0.1)",
                        justify="between",
                        align_items="center",
                        padding="1rem",
                        padding_y="0.7rem",
                        width="100%",
                        box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 4px",
                    ),
                    rx.box(
                        rx.match(
                            AppState.current_page,
                            ("Dashboard", dashboard.dashboard_page()),
                            ("Members", users.users_page()),
                            ("Contribution", contributions.contribution_page()),
                            ("Withdrawal", withdrawal.withdraw_page()),
                            ("Schedule", schedule.schedule_withdrawal_page()),
                            ("Transactions", transactions.transaction_page()),
                            ("Notification", notification.notification_page()),
                            ("Activity Logs", logs.activity_log_page()),
                            (dashboard.dashboard_page()),  # 
                        ),
                        align="center",
                        spacing="4",
                        padding=[".5rem", "1rem","2rem"],
                        overflow_y="auto",  # This enables vertical scrolling when content overflows
                        height="calc(100vh - 140px)",  # Adjusted height to account for navbar and header
                        width="100%",
                    ),
                    padding_left=rx.breakpoints(initial="0", md="240px", lg="240px"),
                    margin_top="70px",
                    width="100%",
                    height="calc(100vh - 70px)",
                    min_width="450px",
                    flex="1",
                    background_color="#e6e6e6",
                    align="center",
                    justify="center",
                    style={
                        "scrollbar_width": "thin",
                        "scrollbar_color": "#888 transparent",
                        "&::-webkit-scrollbar": {
                            "width": "10px",
                        },
                        "&::-webkit-scrollbar-track": {
                            "background": "transparent",
                        },
                        "&::-webkit-scrollbar-thumb": {
                            "background_color": "#888",
                            "border_radius": "4px",
                        },
                        "&::-webkit-scrollbar-thumb:hover": {
                            "background": "#555",
                        },
                    },
                ),
                width="100%",
            ),
            width="100%",
            height="100vh",
            spacing="0",
        ),
        confirm_logout(),
        thrift_details(),
        width="100vw",
        height="100vh",
        background_color="#ffffff",
    )


def confirm_logout():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Are you sure to logout?", color="#333300", text_align="center", margin_y="2rem"),
            rx.hstack(
                rx.button(
                    "Confirm",
                    bg="#333300",
                    color="white",
                    _hover={"bg": "#4d4d33"},
                    on_click=AuthState.continue_logout,
                ),

                rx.button(
                    "Cancel",
                    bg="#333300",
                    color="white",
                    _hover={"bg": "#4d4d33"},
                    on_click=AuthState.close_dialog,
                ),
                justify="center",
                align="center",
                spacing="3",
            ),
            
            padding="2rem",
            bg="#ffffff",
        ),
        open=AuthState.confirm_dialog,
    )

def thrift_details():
    
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Group Details", color="#333300", magin_bottom="2rem"),
            rx.vstack(
                rx.vstack(
                    rx.text("Group ID", color="#333300",  font_size="12px"),
                    rx.text(DashboardState.group_details["group_id"], font_size="14px", font_weight="bold", color="#333300"),
                    spacing="1",
                    justify="start",
                ),
                rx.vstack(
                    rx.text("Group Name", color="#333300",  font_size="12px"),
                    rx.text(DashboardState.group_details["group_name"], font_size="14px", font_weight="bold", color="#333300"),
                    spacing="1",
                    justify="start",
                ),
                rx.vstack(
                    rx.text("Group Descriptions", color="#333300",  font_size="12px"),
                    rx.text(DashboardState.group_details["description"], font_size="14px", font_weight="bold", color="#333300"),
                    spacing="1",
                    justify="start",
                ),
                rx.vstack(
                    rx.text("Group Admin ID", color="#333300",  font_size="12px"),
                    rx.text(DashboardState.group_details["group_admin"], font_size="14px", font_weight="bold", color="#333300"),
                    spacing="1",
                    justify="start",
                ),
                rx.vstack(
                    rx.text("Group Status", color="#333300",  font_size="12px"),
                    rx.text(rx.cond(DashboardState.group_details["is_active"], "Active", "Inactive"), font_size="14px", font_weight="bold", color="#333300"),
                    spacing="1",
                    justify="start",
                ),               
                spacing="2",
                padding="2rem"

            ),
            
            rx.dialog.close(
                rx.button(
                    "Close",
                    bg="#333300",
                    color="white",
                    _hover={"bg": "#4d4d33"},
                    on_click=DashboardState.close_details,
                ),
                padding="1rem"
            ),
            padding="2rem",
            bg="#ffffff",
        ),
        open=DashboardState.show_details,
    )


class CallbackState(rx.State):
    """State for the callback page."""
    @rx.var
    def reference(self) -> str:
        """Get the 'reference' query parameter from the URL."""
        return self.router.page.params.get("reference", "")

    async def verify_on_mount(self):
        """Trigger payment verification on page load."""
        if self.reference:
            contrib_state = await self.get_state(ContributionState)
            await contrib_state.verify_payment(self.reference)

def payment_callback():
    return rx.vstack(
        rx.center(
            rx.vstack(
                rx.heading("Payment Status", color="#333300", margin_top="2rem", margin_bottom="1rem"),
                rx.spinner("loader", size="3", color="green", margin_bottom="1rem"),
                rx.text(
                    rx.cond(
                        ContributionState.status != "Payment processed successfully!",
                        "Verifying payment...", 
                        "Verifying completed!",
                    ),
                    
                    color="#333300",
                ),
                rx.text(f"Status: {ContributionState.status}", color="#333300"),
                # rx.button(
                #     "Back to Contributions",
                #     bg="#333300",
                #     color="white",
                #     border_radius="md",
                #     padding="2",
                #     width="200px",
                #     height="45px",
                #     _hover={"bg": "#4d4d33"},
                #     href="/home",
                #     margin_top="1rem", 
                #     margin_bottom="2rem"
                # ),
                

                rx.cond(
                    ContributionState.status == "Payment processed successfully!",
                    rx.link(
                        "Back to Contributions", 
                        href="/home", 
                        color="#333300",
                        padding="2",
                        margin_top="1rem", 
                        margin_bottom="2rem",
                        font_weight="bold",
                    ),
                    
                ),
                

                align="center",
                justify="center",
                width="40%",
                padding="4",
                spacing="2",
                bg="rgba(255, 255, 255, 0.9)",
                border_radius="10px",
                box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
            ),
            width="100%",
            height="100vh",
            # align="center",
            # justify="center"
            
        ),
        
        width="100vw",
        height="100vh",
        background_color="#e6e6e6",
        on_mount=CallbackState.verify_on_mount,
    )