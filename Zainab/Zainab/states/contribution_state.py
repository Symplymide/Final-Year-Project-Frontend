import reflex as rx
import httpx
from datetime import datetime, timezone, timedelta
from .auth_state import AuthState

BACKEND_URL = "http://localhost:8001"

class ContributionState(rx.State):
    """Manages contribution-related logic."""
    amount: str = ""
    status: str = "Pending"
    transaction_reference: str = ""
    contributions: list[dict] = []
    view_history: bool = False
    current_page: int = 1
    items_per_page: int = 5
    paginated_contributions: list[dict] = []
    expected_amount: float = 0.0  # New: Expected contribution amount
    frequency: str = ""  # New: Contribution frequency
    payment_loading: bool = False
    current_month: str = ""
    days_remaining: int = ""
    contribution_current_month: int = ""
    contribution_status: str = ""
    current_year_month: str = ""
    

    @rx.var(cache=False)
    def is_amount_valid(self) -> bool:
        try:
            amount = float(self.amount)
            return amount >= self.expected_amount and amount > 0
        except ValueError:
            return False

    @rx.var(cache=True)
    def contributions_length(self) -> int:
        return len(self.contributions)

    def set_amount(self, value: str):
        self.amount = str(value) if value is not None else ""

    
    async def fetch_expected_amount(self):
        auth_state = await self.get_state(AuthState)  # Get the AuthState instance
        token = auth_state.token
        self.get_current_date()

        yield  # Ensure the UI updates before making the request

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/contribution/expected-amount/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()  # Raise an exception for HTTP errors
                data = response.json()

                # Update state with the fetched data
                self.expected_amount = data["expected_amount"]
                self.frequency = data["frequency"]
                self.contribution_current_month = data["current_month"]
                self.contribution_status = data["contribution_status"]
                self.current_year_month = data["current_calendar_month"]

        except Exception as e:
            # Handle errors and update state
            self.expected_amount = 0.0
            self.frequency = ""
            yield rx.toast.error(f"Failed to fetch expected amount: {str(e)}", position="top-right")  # Use yield for toast

        finally:
            yield  # Ensure the UI updates

    async def initiate_contribution(self):
        auth_state = await self.get_state(AuthState)
        user_id = auth_state.user_id
        group_id = auth_state.group_id
        token = auth_state.token

        # amount_str = str(self.amount)
        # try:
        #     amount_float = float(amount_str)
        #     if not amount_str or amount_float <= 0:
        #         self.status = "Error. Enter a valid amount"
        #         yield rx.toast.error("Please enter a valid amount", position="top-right")  # Use yield
        #         return  # Exit early
        #     if amount_float < self.expected_amount:
        #         self.status = f"Error: Amount must be at least {self.expected_amount} NGN"
        #         yield rx.toast.error(f"Amount must be at least {self.expected_amount} NGN for {self.frequency} contribution", position="top-right")  # Use yield
        #         return  # Exit early
        # except ValueError:
        #     self.status = "Error: Invalid amount format"
        #     yield rx.toast.error("Please enter a numeric amount", position="top-right")  # Use yield
        #     return  # Exit early

        amount_float = float(self.expected_amount)
        if not user_id or not group_id or not token:
            self.status = "Error: Authentication data missing"
            yield rx.toast.error("Authentication error: Missing user_id, group_id, or token", position="top-right")  # Use yield
            return  # Exit early

        self.payment_loading = True
        yield  # Ensure the UI updates before making the request

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{BACKEND_URL}/contribution/create/",
                    json={
                        "user_id": user_id,
                        "group_id": group_id,
                        "amount": amount_float,
                        "contribution_date": datetime.now(timezone.utc).isoformat(),
                        "status": "Pending",
                        "operation": "Create"
                    },
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                data = response.json()
                self.transaction_reference = data["transaction_reference"]
                self.status = "Initiated"
                yield rx.redirect(data["authorization_url"])  # Use yield for redirect

        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: Status {e.response.status_code}, Content: {e.response.text}")
            try:
                error_detail = e.response.json().get("detail", "Unknown error")
            except ValueError:
                error_detail = e.response.text or "Unknown error"
            self.status = f"Failed: {error_detail}"
            yield rx.toast.error(f"Payment initiation failed: {error_detail}", position="top-right")  # Use yield

        except Exception as e:
            self.status = f"Failed: {str(e)}"
            yield rx.toast.error(f"Unexpected error: {str(e)}", position="top-right")  # Use yield

        finally:
            self.payment_loading = False
            yield  # Ensure the UI updates

    async def verify_payment(self, reference: str = None):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token
        if reference:
            self.transaction_reference = reference
        if not self.transaction_reference:
            self.status = "Error: No transaction reference"
            return rx.toast.error("No transaction reference available", position="top-right")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/contribution/verify-payment/{self.transaction_reference}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                data = response.json()
                print(f"Verification response: {data}")
                self.status = "Payment processed successfully!" if data["transaction_status"] == "Completed" else f"Verification Failed: {data['transaction_status']}"
                await self.fetch_contributions()
                return rx.redirect("/home")
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: Status {e.response.status_code}, Content: {e.response.text}")
            try:
                error_detail = e.response.json().get("detail", "Unknown error")
            except ValueError:
                error_detail = e.response.text or "Unknown error"
            self.status = f"Verification Failed: {error_detail}"
            return rx.toast.error(f"Error: {error_detail}", position="top-right")
        except Exception as e:
            self.status = f"Verification Failed: {str(e)}"
            return rx.toast.error(f"Error: {str(e)}", position="top-right")

    async def fetch_contributions(self):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/contribution/get-contributions/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                self.contributions = response.json()
                self.update_pagination()
        except Exception as e:
            self.contributions = [{"error": f"Failed to fetch: {str(e)}"}]
            self.update_pagination()
            return rx.toast.error(f"Error: {str(e)}", position="top-right")

    async def toggle_view(self):
        self.view_history = not self.view_history
        if self.view_history and not self.contributions:
            await self.fetch_contributions()

    def next_page(self):
        if (self.current_page * self.items_per_page) < self.contributions_length:
            self.current_page += 1
            self.update_pagination()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def update_pagination(self):
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        self.paginated_contributions = self.contributions[start:end]

    # async def on_mount(self):
    #     await self.fetch_expected_amount()

    async def on_mount(self):
        yield
        async for _ in self.fetch_expected_amount():
            pass  # Iterate over the generator to execute it



    def get_current_date(self):
        now = datetime.now()
        current_month = now.strftime("%B")
        if now.month == 12:
            next_month = now.replace(year=now.year + 1, month=1, day=1)
        else:
            next_month = now.replace(month=now.month + 1, day=1)
        last_day_of_month = next_month - timedelta(days=1)
        days_remaining = (last_day_of_month - now).days

        self.current_month = current_month
        self.days_remaining = days_remaining