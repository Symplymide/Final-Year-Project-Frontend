import reflex as rx
import httpx
from datetime import datetime
from .auth_state import AuthState

BACKEND_URL = "http://localhost:8001"

class TransactionState(rx.State):
    loading: bool = False
    transactions: list[dict] = []
    current_page: int = 1
    items_per_page: int = 5
    paginated_transactions: list[dict] = []

    @rx.var(cache=True)
    def transaction_length(self) -> int:
        return len(self.transactions)

    async def fetch_transactions(self):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token

        self.loading = True
        yield  # Ensure the UI updates before making the request

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/transactions/read-transactions/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()

                if response.status_code == 200:
                    self.transactions = response.json()
                    self.update_pagination()
                elif response.status_code == 401:
                    raise Exception("Token expired, please login again")

        except Exception as e:
            self.transactions = [{"error": f"Failed to fetch: {str(e)}"}]
            self.update_pagination()
            yield rx.toast.error(f"Error: {str(e)}", position="top-right")  # Use yield for toast

        finally:
            self.loading = False
            yield  # Ensure the UI updates

    async def refresh_view(self):
        async for _ in self.fetch_transactions():
            pass  # Iterate over the generator to execute it

    def next_page(self):
        if (self.current_page * self.items_per_page) < self.transaction_length:
            self.current_page += 1
            self.update_pagination()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def update_pagination(self):
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        self.paginated_transactions = self.transactions[start:end]

    async def on_mount(self):
        yield
        async for _ in self.fetch_transactions():
            pass  # Iterate over the generator to execute it