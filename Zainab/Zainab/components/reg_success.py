import reflex as rx
from ..states.app_state import NavState, GroupFormState


def success_view():
    return rx.card(
        rx.vstack(
            rx.heading("Group Successfully Created", size="5", align="center", color="green"),
            rx.text(f"Group ID: {GroupFormState.group_id}"),
            rx.text(f"Your User ID: {GroupFormState.admin_user_id}"),
            rx.text(f"Your are the Admin of this group."),
            rx.text("Please save these details somewhere safe."),
            
            rx.link(
                "< Go login",
                on_click=lambda: NavState.set_view("signin"),
                bg="transparent",
                p=2,
                align="center",
                font_size="12px",
                color="#333300"
            ),
            spacing="4",
            width="100%",
            align="center",
        ),
        width="100%",
        
        

        max_width=rx.breakpoints(sm="90%", md="600px"),  # Responsive width: 90% on mobile, 500px on desktop
        padding="40px",
        min_width="420px",
        min_height="150px",
        shadow="lg",  # Optional shadow for styling
        border_radius="lg",  # Optional rounded corners
        bg="rgba(255, 255, 255, 1)",  # Semi-transparent white background
          # Add blur effect
    )