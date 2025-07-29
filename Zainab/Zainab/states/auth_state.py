import reflex as rx
import httpx
from datetime import datetime

BACKEND_URL = "http://localhost:8001"

class AuthState(rx.State):
    """Handles authentication and user data."""
    is_authenticated: bool = rx.SessionStorage("false") == "true"
    token: str = rx.SessionStorage("")
    user_id: str = rx.LocalStorage("", sync=True)
    group_id: str = rx.LocalStorage("", sync=True)
    name: str = rx.LocalStorage("", sync=True)
    phone: str = rx.LocalStorage("", sync=True)
    email: str = rx.LocalStorage("", sync=True)
    role_name: str = rx.LocalStorage("", sync=True)
    confirm_dialog: bool = False
    today: str = ""

    username: str = user_id if user_id else ""  # Form fields
    password: str = ""
    loading: bool = False

    async def login(self):
        """Handle login and store user data."""
        if not (self.username and self.password):
            yield rx.toast("Please provide credentials!", position="top-right")
            return  # Exit the function early
        
        # Set loading to True and yield to ensure the UI updates
        self.loading = True
        yield  # This ensures the state is updated before proceeding

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{BACKEND_URL}/auth/",
                    data={"username": self.username, "password": self.password}
                )

                data = response.json()
                if response.status_code == 200 and data.get("access_token"):
                    self.token = data["access_token"]
                    self.user_id = data["user_id"]
                    self.group_id = data["group_id"]
                    self.name = data["name"]
                    self.phone = data["phone"]
                    self.email = data["email"]
                    self.role_name = data["role_name"]
                    self.is_authenticated = True
                    self.loading = False
                    self.today = await self.get_todays_date()
                    yield rx.redirect("/home")  # Use yield instead of return
                else:
                    raise Exception("Invalid credentials")
        except Exception as e:
            self.loading = False
            yield rx.toast(f"Login failed: {str(e)}", position="top-right")  # Use yield instead of return
        

    async def logout(self):
        """Clear auth state and redirect."""
        try:
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{BACKEND_URL}/auth/logout",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                # raise Exception("Invalid credentials")
        except Exception as e:
            self.loading = False
            # return rx.toast(f"Login failed: {str(e)}", position="top-right")
        
        self.is_authenticated = False
        self.token = ""
        self.user_id = ""
        self.group_id = ""
        self.name = ""
        self.phone = ""
        self.email = ""
        self.role_name = ""
        self.username = ""
        self.password = ""
        return rx.redirect("/")
    

    def set_username(self, value: str):
        self.username = value

    def set_password(self, value: str):
        self.password = value

    def open_dialog(self):
        self.confirm_dialog = True

    async def continue_logout(self):
        self.confirm_dialog = False
        await self.logout()

    def close_dialog(self):
        self.confirm_dialog = False

    async def get_todays_date(self):
        today = datetime.today()
        formatted_date = today.strftime("%A, %d %B %Y")
        
        return formatted_date


    @staticmethod
    def require_auth(page_func):
        """Protect pages from unauthenticated access."""
        def wrapper(*args, **kwargs):
            return rx.cond(
                AuthState.is_authenticated,
                page_func(*args, **kwargs),
                rx.fragment(rx.script("window.location.href = '/'"))
            )
        wrapper.__name__ = page_func.__name__  # Preserve the original function name
        return wrapper
    
    