import reflex as rx
import httpx
from datetime import datetime, timezone
from .auth_state import AuthState

BACKEND_URL = "http://localhost:8001"

class AccessLogState(rx.State):
    loading: bool = False
    logs: list[dict] = []
    current_page: int = 1
    items_per_page: int = 5
    paginated_logs: list[dict] = []


    @rx.var(cache=True)
    def log_length(self) -> int:
        return len(self.logs)
    
    async def fetch_logs(self):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token

        self.loading = True
        yield  # Ensure the UI updates before making the request

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/access/logs/",
                    headers={"Authorization": f"Bearer {token}"},
                )
                response.raise_for_status()
                self.logs = response.json()  # Update logs
                self.update_pagination()  # Update paginated logs
        except Exception as e:
            yield rx.toast.error(f"Failed to fetch logs: {str(e)}", position="top-right")
        finally:
            self.loading = False
            yield  # Ensure the UI updates after the request


    def next_page(self):
        if (self.current_page * self.items_per_page) < self.log_length:
            self.current_page += 1
            self.update_pagination()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def update_pagination(self):
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        self.paginated_logs = self.logs[start:end]

    async def on_mount(self):
        yield
        async for _ in self.fetch_logs():
            pass  # Iterate over the generator to execute it

