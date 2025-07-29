import reflex as rx
import httpx
from .auth_state import AuthState

BACKEND_URL = "http://localhost:8001"

class AppState(rx.State):
    """Manages navigation for landing and home pages."""
    landing_view: str = "signin"  # Controls landing page component
    current_page: str = "Dashboard"  # Controls home page section
    is_menu: bool = False

    def set_landing_view(self, view: str):
        self.landing_view = view

    def set_home_page(self, page: str):
        self.current_page = page

    def toggle_menu(self):
        """Toggle the visibility of the side menu."""
        self.is_menu = not self.is_menu

class UserSignupFormState(rx.State):
    """Handles user signup form."""
    user_id: str = ""
    group_id: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    password: str = ""
    loading: bool = False
    show_dialog: bool = False

    async def handle_submit(self):
        # self.loading = True
        if not all([self.group_id, self.name, self.phone, self.email, self.password]):
            self.loading = False
            yield rx.toast("All fields are required!", position="top-right")
            return

        payload = {
            "group_id": self.group_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            "role_name": "Member",
            "operation": "Create"
        }

        self.loading = True
        yield  # This ensures the state is updated before proceeding

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{BACKEND_URL}/users/create-user/", json=payload)
                if response.status_code == 201:
                    data = response.json()
                    self.user_id = data["user_id"]
                    self.loading = False
                    self.show_dialog = True
        
                    yield rx.toast.success("User created successfully!", position="top-right")
                else:
                    raise Exception("Signup failed")
        except Exception as e:
            self.loading = False
            yield rx.toast.error(f"Error: {str(e)}", position="top-right")
        

class GroupFormState(rx.State):
    """Handles group creation form."""
    user_id: str = ""
    group_id: str = ""
    group_name: str = ""
    group_description: str = ""
    admin_name: str = ""
    admin_phone: str = ""
    admin_mail: str = ""
    password: str = ""
    confirm_password: str = ""
    loading: bool = False
    show_dialog: bool = False

    # @rx.event
    async def handle_submit(self):
        # self.loading = True
        if self.password != self.confirm_password:
            # self.loading = False
            yield rx.toast("Passwords do not match!", position="top-right")
            return
        if not all([self.group_name, self.group_description, self.admin_name, self.admin_phone, self.admin_mail, self.password]):
            # self.loading = False
            yield rx.toast("All fields are required!", position="top-right")
            return

        payload = {
            "group_name": self.group_name,
            "group_description": self.group_description,
            "admin_name": self.admin_name,
            "admin_phone": self.admin_phone,
            "admin_mail": self.admin_mail,
            "password": self.password,
            "role_name": "Moderator",
            "operation": "Create"
        }

        self.loading = True
        yield

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{BACKEND_URL}/groups/create-group/", json=payload)
                data = response.json()
                if response.status_code == 201:
                    
                    self.user_id = data["group_admin"]
                    self.group_id = data["group_id"]
                    self.loading = False
                    self.show_dialog = True
                    
                    yield rx.toast.success("Group created successfully!", position="top-right")
                else:
                    raise Exception("Group creation failed")
        except Exception as e:
            self.loading = False
            yield rx.toast.error(f"Error: {str(e)}", position="top-right")
            
        
