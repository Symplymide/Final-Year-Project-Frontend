import httpx
import asyncio
import reflex as rx
from datetime import datetime
from ..states.auth_state import AuthState

BACKEND_URL = "http://localhost:8001"

class DashboardState(rx.State):
    loading: bool = False
    group_details: dict = {}  # Store group details
    show_details: bool = False  # Control visibility of the dialog
    due_date: str = ""
    receiveable: str = "0"

    total_members: int = 0
    active_members: int = 0
    total_schedules: int = 0
    total_contributions: int = 0
    
    group_balance: str = "0"
    total_contributed: str = "0"
    total_withdrawal: str = "0"
    my_contributions: str = "0"
    active_target_amount: str = "0"
    amount_realised: str = "0"
    percentage: float = 0.0

    async def fetch_group_details(self):
        """Fetch group details from /group-details/."""
        auth_state = await self.get_state(AuthState)
        token = auth_state.token

        self.loading = True
        yield  # Ensure UI updates before making requests

        headers = {"Authorization": f"Bearer {token}"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{BACKEND_URL}/dashboard/group-details/", headers=headers)
                response.raise_for_status()
                self.group_details = response.json()
        except httpx.HTTPStatusError as e:
            yield rx.toast.error(f"Failed to fetch group details: {e.response.text}", position="top-right")
        except Exception as e:
            yield rx.toast.error(f"An error occurred: {str(e)}", position="top-right")
        finally:
            self.loading = False
            yield  # Ensure UI updates after completion

    async def fetch_other_details(self):
        """Fetch other dashboard stats from /dashboard/others/."""
        auth_state = await self.get_state(AuthState)
        token = auth_state.token

        self.loading = True
        yield  # Ensure UI updates before making requests

        headers = {"Authorization": f"Bearer {token}"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{BACKEND_URL}/dashboard/others/", headers=headers)
                response.raise_for_status()
                details = response.json()
                try:
                    response2 = await client.get(f"{BACKEND_URL}/dashboard/group-details/", headers=headers)
                    response2.raise_for_status()
                    self.group_details = response2.json()
                except Exception as e:
                    yield rx.toast.error(f"Failed to fetch group details: {str(e)}", position="top-right")
                    self.group_details = {}

                # Assign values with formatting
                self.total_members = details.get("total_members", 0)
                self.active_members = details.get("active_members", 0)
                self.total_schedules = details.get("total_schedules", 0)
                self.total_contributions = details.get("total_contributions", 0)
                self.group_balance = f'{details.get("group_balance", 0):,}'
                self.total_contributed = f'{details.get("total_contributed", 0):,}'
                self.total_withdrawal = f'{details.get("total_withdrawal", 0):,}'
                self.my_contributions = f'{details.get("my_contributions", 0):,}'
                self.active_target_amount = f'{details.get("active_target_amount", 0):,}'
                self.amount_realised = f'{details.get("amount_realised", 0):,}'
                self.percentage = details.get("percentage", 0)

                # Format due_date if present in the response
                if "due_date" in details:
                    self.format_date(details["due_date"])
        except httpx.HTTPStatusError as e:
            yield rx.toast.error(f"Failed to fetch other details: {e.response.text}", position="top-right")
        except Exception as e:
            yield rx.toast.error(f"An error occurred: {str(e)}", position="top-right")
        finally:
            self.loading = False
            yield  # Ensure UI updates after completion

    async def show_group_details(self):
        """Fetch and display group details."""
        self.loading = True
        # yield
        # async for _ in self.fetch_group_details():
        #     pass  # Iterate over the async generator to execute it
        self.show_details = True  # Open the dialog

    def close_details(self):
        """Close the group details dialog."""
        self.show_details = False

    def format_date(self, date_string: str) -> None:
        """Format a date string and store it in due_date."""
        try:
            dt = datetime.strptime(date_string, '%Y-%m-%d')
            self.due_date = dt.strftime('%A, %d %B %Y')
        except ValueError:
            self.due_date = date_string  # Fallback to original string if parsing fails

    async def on_mount(self):
        yield
        async for _ in self.fetch_other_details():
            pass



