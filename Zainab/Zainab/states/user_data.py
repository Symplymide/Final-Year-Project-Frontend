import reflex as rx


class UserState(rx.State):
    """Manages user session data after login."""
    user_id: str = rx.LocalStorage("", sync=True)
    group_id: str = rx.LocalStorage("", sync=True)
    name: str = rx.LocalStorage("", sync=True)
    phone: str = rx.LocalStorage("", sync=True)
    email: str = rx.LocalStorage("", sync=True)
    role_name: str = rx.LocalStorage("", sync=True)

    @rx.event
    async def set_user_data(self, data: dict):
        """Store user data in state."""
        self.user_id = data["user_id"]
        self.group_id = data["group_id"]
        self.name = data["name"]
        self.phone = data["phone"]
        self.email = data["email"]
        self.role_name = data["role_name"]
        

    @rx.event
    async def clear_user_data(self):
        """Clear user data when logging out."""
        self.user_id = ""
        self.group_id = ""
        self.name = ""
        self.phone = ""
        self.email = ""
        self.role_name = ""
        