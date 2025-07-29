import reflex as rx
import httpx
from datetime import datetime
from .auth_state import AuthState
from .contribution_state import ContributionState
from .withdrawal_state import WithdrawalState

BACKEND_URL = "http://localhost:8001"

class ScheduleWithdrawalState(rx.State):
    schedule_name: str = ""
    start_date: str = datetime.now().strftime("%Y-%m-%d")
    end_date: str = (datetime.now().replace(month=(datetime.now().month % 12) + 1)).strftime("%Y-%m-%d")
    total_target_amount: str = ""
    loading: bool = False
    view_history: bool = False
    schedules: list[dict] = []
    current_page: int = 1
    items_per_page: int = 5
    paginated_schedules: list[dict] = []
    active_schedule: str = ""

    @rx.var(cache=True)
    def schedule_length(self) -> int:
        return len(self.schedules)

    @rx.var(cache=False)
    def is_form_valid(self) -> bool:
        
        try:
            target = float(self.total_target_amount)
            start = datetime.strptime(self.start_date, "%Y-%m-%d")
            end = datetime.strptime(self.end_date, "%Y-%m-%d")
            return (
                self.schedule_name and
                target > 0 and
                start < end
            )
        except ValueError:
            return False

    def set_schedule_name(self, value: str):
        self.schedule_name = value

    def set_start_date(self, value: str):
        self.start_date = value

    def set_end_date(self, value: str):
        self.end_date = value

    def set_total_target_amount(self, value: str):
        self.total_target_amount = value

    async def create_schedule(self):
        auth_state = await self.get_state(AuthState)
        contribution_state = await self.get_state(ContributionState)
        withdrawal_state = await self.get_state(WithdrawalState)

        # Check if there is an active schedule (commented out for now)
        # if self.active_schedule:
        #     yield rx.toast("There is still a Schedule", position="top-right")
        #     return

        # Check if the user is a moderator
        if auth_state.role_name != "Moderator":
            yield rx.toast.error("Only Moderators can create schedules", position="top-right")  # Use yield
            return  

        # Validate form fields
        if not self.is_form_valid:
            yield rx.toast.error("Please fill all fields correctly", position="top-right")  # Use yield
            return  

        self.loading = True
        yield  # Ensure the UI updates before making the request

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{BACKEND_URL}/withdraw/schedule/create/",
                    json={
                        "group_id": auth_state.group_id,
                        "schedule_name": self.schedule_name,
                        "start_date": self.start_date,
                        "end_date": self.end_date,
                        "total_target_amount": float(self.total_target_amount)
                    },
                    headers={"Authorization": f"Bearer {auth_state.token}"}
                )
                response.raise_for_status()
                data = response.json()

                
                async for _ in contribution_state.fetch_expected_amount():
                    pass  
                async for _ in withdrawal_state.fetch_balance():
                    pass  
                async for _ in withdrawal_state.fetch_payout():
                    pass  
                async for _ in self.fetch_schedules():
                    pass  

                yield rx.toast.success("Withdrawal schedule created successfully!", position="top-right")  # Use yield

        except httpx.HTTPStatusError as e:
            try:
                error_detail = e.response.json().get("detail", "Unknown error")
            except ValueError:
                error_detail = e.response.text or "Unknown error"
            yield rx.toast.error(f"Failed to create schedule: {error_detail}", position="top-right")  # Use yield

        except Exception as e:
            yield rx.toast.error(f"Unexpected error: {str(e)}", position="top-right")  # Use yield

        finally:
            self.loading = False
            yield  

    async def fetch_schedules(self):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token
        self.loading = True
        yield
        try:
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/withdraw/schedules/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                schedules_data = response.json()
                self.schedules = schedules_data
                self.update_pagination()
                # Set active schedule name
                self.active_schedule = ""
                for schedule in schedules_data:
                    if schedule.get("status") == "Active":
                        self.active_schedule = schedule.get("schedule_name", "")
                        break
        except Exception as e:
            self.schedules = [{"error": f"Failed to fetch: {str(e)}"}]
            self.update_pagination()
            yield rx.toast.error(f"Error: {str(e)}", position="top-right")
        finally:
            self.loading = False
            yield

    async def toggle_view(self):
        self.view_history = not self.view_history
        if self.view_history:
            async for event in self.fetch_schedules():
                print("Event yielded:", event)
                if event:
                    yield event

    def next_page(self):
        if (self.current_page * self.items_per_page) < self.schedule_length:
            self.current_page += 1
            self.update_pagination()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def update_pagination(self):
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        self.paginated_schedules = self.schedules[start:end]
        
