import reflex as rx
from ..states.app_state import AuthState
from ..states.user_data import UserState
from ..states.dashboard_state import DashboardState


def dashboard_page():
    return rx.box(
        rx.vstack(
            rx.box(
                rx.vstack(
                    # ===================================================================================
                    #               User Info Section (4 cards - 2 per row on mobile)
                    # ===================================================================================
                    rx.box(
                        rx.flex(
                            # Card 1
                            rx.vstack(
                                rx.vstack(
                                    rx.heading(f"{DashboardState.total_members}", color="#ffffff"),
                                    rx.text("Total Members", font_size="14px", color="#ffffff"),
                                    padding="1rem",
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("More info", font_size="14px", color="#ffffff"),
                                    rx.icon("circle-arrow-right", size=14, color="#ffffff"), 
                                    align="center",
                                    justify="center",
                                    overflow="hidden",
                                    width="100%",
                                    height="40px",
                                    background_color="rgba(0, 0, 0, 0.1)",
                                    cursor="pointer",
                                    _hover={
                                        "transform": "translateY(-2px)",
                                        "transition": "all 0.2s ease-in-out",
                                        "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                                    },
                                ),
                                min_width="200px",
                                height="150px",
                                spacing="4",
                                background_color="#660287",
                                border_radius="5px",
                                width=rx.breakpoints(initial="48%", md="23%"),  # 2 per row on mobile
                            ),

                            # Card 2
                            rx.vstack(
                                rx.vstack(
                                    rx.heading(f"{DashboardState.active_members}", color="#ffffff"),
                                    rx.text("Active Members", font_size="14px", color="#ffffff"),
                                    padding="1rem",
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("More info", font_size="14px", color="#ffffff"),
                                    rx.icon("circle-arrow-right", size=14, color="#ffffff"), 
                                    align="center",
                                    justify="center",
                                    overflow="hidden",
                                    width="100%",
                                    height="40px",
                                    background_color="rgba(0, 0, 0, 0.1)",
                                    cursor="pointer",
                                    _hover={
                                        "transform": "translateY(-2px)",
                                        "transition": "all 0.2s ease-in-out",
                                        "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                                    },
                                ),
                                min_width="200px",
                                height="150px",
                                spacing="4",
                                background_color="#FF9933",
                                border_radius="5px",
                                width=rx.breakpoints(initial="48%", md="23%"),  # 2 per row on mobile
                            ),

                            # Card 3
                            rx.vstack(
                                rx.vstack(
                                    rx.heading(f"{DashboardState.total_contributions}", color="#ffffff"),
                                    rx.text("Total Contributions", font_size="14px", color="#ffffff"),
                                    padding="1rem",
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("More info", font_size="14px", color="#ffffff"),
                                    rx.icon("circle-arrow-right", size=14, color="#ffffff"), 
                                    align="center",
                                    justify="center",
                                    overflow="hidden",
                                    width="100%",
                                    height="40px",
                                    background_color="rgba(0, 0, 0, 0.1)",
                                    cursor="pointer",
                                    _hover={
                                        "transform": "translateY(-2px)",
                                        "transition": "all 0.2s ease-in-out",
                                        "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                                    },
                                ),
                                min_width="200px",
                                height="150px",
                                spacing="4",
                                background_color="#0A708A",
                                border_radius="5px",
                                width=rx.breakpoints(initial="48%", md="23%"),  # 2 per row on mobile
                            ),

                            # Card 4
                            rx.vstack(
                                rx.vstack(
                                    rx.heading(f"{DashboardState.total_schedules}", color="#ffffff"),
                                    rx.text("Total Schedules", font_size="14px", color="#ffffff"),
                                    padding="1rem",
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("More info", font_size="14px", color="#ffffff"),
                                    rx.icon("circle-arrow-right", size=14, color="#ffffff"), 
                                    align="center",
                                    justify="center",
                                    overflow="hidden",
                                    width="100%",
                                    height="40px",
                                    background_color="rgba(0, 0, 0, 0.1)",
                                    cursor="pointer",
                                    _hover={
                                        "transform": "translateY(-2px)",
                                        "transition": "all 0.2s ease-in-out",
                                        "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
                                    },
                                    
                                ),
                                min_width="200px",
                                height="150px",
                                spacing="4",
                                background_color="#663333",
                                border_radius="5px",
                                width=rx.breakpoints(initial="48%", md="23%"),  # 2 per row on mobile
                            ),
                           
                            justify="between",
                            align="center",
                            spacing="3",
                            direction=rx.breakpoints(initial="row", md="row"),
                            wrap="wrap",  # Allow items to wrap on smaller screens
                            width="100%",
                        ),
                        padding_y="1rem",
                        width="100%",
                    ),

                    # ===================================================================================
                    #               Withdrawal Schedule Section (column on mobile)
                    # ===================================================================================
                    rx.flex(
                        rx.hstack(
                            rx.vstack(
                                rx.heading("Withdrawal Schedule", size="5", color="#333300"),
                                rx.text(f"{DashboardState.due_date}", font_size="16px", color="#333300"),
                            ),
                            rx.icon("arrow-right", size=18, color="#333300"),
                            padding="2rem",
                            padding_y="3rem",
                            bg_color="#ffffff",
                            spacing="3",
                            width=rx.breakpoints(initial="100%", md="40%"),  # Full width on mobile
                            align="center",
                            justify="center",
                            border_radius="5px",
                            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                        ),

                        rx.vstack(
                            rx.heading("Amount Receivable", size=rx.breakpoints(initial="4", md="5"), color="#333300"),
                            rx.text(f"₦ {DashboardState.receiveable:,}", font_size=rx.breakpoints(initial="14px", md="16px"), color="#333300"),
                            padding="2rem",
                            padding_y="3rem",
                            bg_color="#ffffff",
                            spacing="3",
                            width=rx.breakpoints(initial="100%", md="40%"),  # Full width on mobile
                            align="center",
                            justify="center",
                            border_radius="5px",
                            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                        ),
                        width="100%",
                        justify_content="space-around",
                        align_items="center",
                        spacing="4",
                        direction=rx.breakpoints(initial="column", md="row"),  # Column on mobile
                        wrap="wrap",
                    ),

                    # ===================================================================================
                    #               Breakdown section (2 per row on mobile with dividers between pairs)
                    # ===================================================================================
                    rx.flex(
                        # First pair
                        rx.flex(
                            rx.vstack(
                                rx.heading(f"₦ {DashboardState.my_contributions:,}", size="5", color="#333300"),
                                rx.text("My Contributions", font_size="16px", color="#333300"),
                                padding="1rem",
                                border_radius="5px",
                                spacing="4",
                                align="center",
                                width="100%",
                            ),

                            rx.divider(
                                orientation="vertical", 
                                height="80px", 
                                background_color="rgba(51, 51, 0, 0.7)", 
                                style={'width':'2px'}
                                ),

                            rx.vstack(
                                rx.heading(f"₦ {DashboardState.total_contributed}", size="5", color="#333300"),
                                rx.text("Total Contributed", font_size="16px", color="#333300"),
                                padding="1rem",
                                border_radius="5px",
                                spacing="2",
                                align="center",
                                width="100%",
                            ),
                            width="100%",
                            justify_content="space-between",
                            align_items="center",
                            spacing="4",
                            direction="row",
                        ),
                        rx.desktop_only(
                            rx.divider(
                                orientation="vertical", 
                                height="70%", 
                                background_color="rgba(51, 51, 0, 0.2)", 
                                style={'width':'2px'}
                                ),
                        ),

                        # Second pair
                        rx.flex(
                            rx.vstack(
                                rx.heading(f"₦ {DashboardState.total_withdrawal}", size="5", color="#333300"),
                                rx.text("Total Withdrawn", font_size="16px", color="#333300"),
                                padding="1rem",
                                border_radius="5px",
                                spacing="2",
                                align="center",
                                width="100%",
                            ),
                            rx.divider(
                                orientation="vertical", 
                                height="70%", 
                                background_color="rgba(51, 51, 0, 0.2)", 
                                style={'width':'2px'}
                                ),
                            rx.vstack(
                                rx.heading(f"₦ {DashboardState.group_balance}", size="5", color="#333300"),
                                rx.text("Total Savings", font_size="16px", color="#333300"),
                                padding="1rem",
                                border_radius="5px",
                                spacing="2",
                                align="center",
                                width="100%",
                            ),
                            width="100%",
                            justify_content="space-between",
                            align_items="center",
                            spacing="4",
                            direction="row",
                        ),
                        
                        width="100%",
                        justify_content="space-between",
                        align_items="center",
                        border_radius="5px",
                        height="auto",
                        spacing="4",
                        padding="0.5rem",
                        background_color="#ffff",
                        direction=rx.breakpoints(initial="column", md="row"),  # Stack pairs vertically on mobile
                        margin_top="1rem",
                    ),

                    spacing="3",
                    width="100%",
                ),
                width="100%",
                padding_right=".4rem",  
            ),      
        ),  
        width="100%",
        on_mount=DashboardState.on_mount,  
    )




