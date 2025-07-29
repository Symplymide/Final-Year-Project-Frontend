# user_state.py
import httpx
import reflex as rx
from .auth_state import AuthState

BACKEND_URL = "http://localhost:8001"

class UserDataState(rx.State):
    all_users: list[dict] = []
    loading: bool = False
    selecte3d_user: dict = {}
    show_dialog: bool = False

    @rx.var
    def selected_user_name(self) -> str:
        return self.selected_user.get('name') or 'N/A'

    @rx.var
    def selected_user_id(self) -> str:
        return self.selected_user.get('user_id') or 'N/A'

    @rx.var
    def selected_user_phone(self) -> str:
        return self.selected_user.get('phone') or 'N/A'

    @rx.var
    def selected_user_email(self) -> str:
        return self.selected_user.get('email') or 'N/A'

    @rx.var
    def selected_user_role(self) -> str:
        return self.selected_user.get('role_name') or 'N/A'

    @rx.var
    def selected_user_active(self) -> bool:
        return self.selected_user.get('is_active', False)

    @rx.var
    def selected_user_last_login(self) -> str:
        return self.selected_user.get('last_login') or 'N/A'

    @rx.var
    def selected_user_created_at(self) -> str:
        return self.selected_user.get('created_at') or 'N/A'

    async def fetch_all_users(self):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token
        self.loading = True
        yield
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/users/read-user/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                data = response.json()
                self.all_users = data
        except httpx.HTTPStatusError as e:
            error_detail = e.response.json().get("detail", "Unknown error") if e.response else "Unknown error"
            print(f"HTTP error: {error_detail}")
            yield rx.toast.error(f"Failed to fetch user data: {error_detail}", position="top-right")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            yield rx.toast.error(f"Unexpected error: {str(e)}", position="top-right")
        finally:
            self.loading = False
            yield

    def open_dialog(self, user_id: str):
        self.show_dialog = True
        user = next((user for user in self.all_users if str(user["user_id"]) == str(user_id)), None)
        if user:
            self.selected_user = user
            self.show_dialog = True
            yield  # Ensure UI updates
        else:
            yield rx.toast.error(f"No user found for user_id: {user_id}", position="top-right")
            print(f"No user found for user_id: {user_id}")

    def close_dialog(self):
        self.show_dialog = False

    async def on_mount(self):
        yield
        async for _ in self.fetch_all_users():
            pass