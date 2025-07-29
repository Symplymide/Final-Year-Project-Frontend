import reflex as rx
from ..states.app_state import AppState
from ..states.auth_state import AuthState



# Define the navbar component with a logo
def navbar():
    return rx.box(
        rx.hstack(
            rx.image(src="../thrift_logo2.png", height="40px", margin_right="10px", margin_left="1rem"),  # Add your logo
            rx.hstack(
                rx.hstack(
                    rx.desktop_only(
                        rx.vstack(
                            rx.text(f"{AuthState.name}", font_size="14px", color="#CCCC33", text_align="right"),
                            rx.text(f"{AuthState.role_name}", font_size="12px", color="#666633", text_align="right"),
                            spacing="0",
                            align="end",
                        ),
                    ),
                    
                    rx.desktop_only(
                        rx.image(
                            src="../user_pics.png",
                            width="40px",
                        ),
                    ),
                    rx.mobile_and_tablet(
                        rx.icon(
                            "menu", 
                            size=30, 
                            color=rx.cond(AppState.is_menu, "#FFFFFF", "#CCCC33"),
                            text_align="right",
                            cursor="pointer",
                            on_click=AppState.toggle_menu,
                            _hover={
                                "color": "#FFFFFF",
                                "transition": "color 0.2s ease-in-out",
                            },
                        ),
                    ),
                    spacing="2",
                    align="center",
                ),
                spacing="6",  
                margin_right=[".5rem", ".5rem", "1rem"],  
                align="center",
            ),

            justify_content="space-between",  
            align_items="center",  
            padding="1rem",
            width="100%",
            position="fixed",
            top="0",
            z_index="1000",
            background_color="#333300",
        ),
    )
