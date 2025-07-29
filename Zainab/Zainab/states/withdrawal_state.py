import reflex as rx
import httpx
from datetime import datetime, timezone

from .auth_state import AuthState
from .dashboard_state import DashboardState

BACKEND_URL = "http://localhost:8001"

class WithdrawalState(rx.State):
    bank: str = ""
    banks: list[str] = [
        "Access Bank", "Citi Bank", "Diamond Bank", "Ecobank Nigeria", "Fidelity Bank", "First Bank of Nigeria", "First City Monument Bank",
        "Guaranty Trust Bank", "Heritage Bank", "Keystone Bank", "Mainstreet Bank", "Polaris Bank", "Providus Bank", "Rand Merchant Bank",
        "Stanbic IBTC Bank", "Standard Chartered Bank", "Sterling Bank", "Suntrust Bank", "Union Bank of Nigeria", "United Bank for Africa",
        "Unity Bank", "Wema Bank", "Zenith Bank", "Kuda Bank", "Opay", "PalmPay", "FairMoney", "VFD Microfinance Bank",
        "Alat by Wema", "Sparkle Microfinance Bank"
    ]
    account_number: str = ""
    account_name: str = ""
    amount: str = ""
    balance: float = 0.0
    amount_receivable: float = 0.0
    payout_date: str = ""
    is_payout: bool = False
    view_history: bool = False
    withdrawals: list[dict] = []
    current_page: int = 1
    items_per_page: int = 5
    paginated_withdrawals: list[dict] = []
    loading: bool = False
    account_loading: bool = False
    days_remaining: int = 0
    hours_remaining: int = 0

    @rx.var(cache=True)
    def withdrawals_length(self) -> int:
        return len(self.withdrawals)

    @rx.var(cache=False)
    def is_amount_valid(self) -> bool:
        try:
            amount = float(self.amount)
            return amount > 0 and amount <= self.balance and amount <= self.amount_receivable
        except ValueError:
            return False

    def set_bank(self, value: str):
        self.bank = value

    async def set_account_number(self, value: str):
        self.account_number = value
        if len(self.account_number) == 10 and self.bank:
            async for _ in self.validate_account():
                pass  
        else:
            self.account_name = ""
        

    def set_amount(self, value: str):
        self.amount = str(value) if value is not None else ""

    async def fetch_balance(self):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token

        self.loading = True
        yield  # Ensure the UI updates before making the request

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/withdraw/balance/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                self.balance = response.json()["balance"]

        except Exception as e:
            self.balance = 0.0
            yield rx.toast.error(f"Failed to fetch balance: {str(e)}", position="top-right")  # Use yield for toast

        finally:
            self.loading = False
            yield  # Ensure the UI updates

    

    def time_until_target_date(target_date_str):
        # Convert the target date string to a datetime object
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
        
        # Get the current date and time
        current_date = datetime.now()
        
        # Calculate the time difference
        time_difference = target_date - current_date
        
        # Extract days and hours from the time difference
        days_remaining = time_difference.days
        hours_remaining = time_difference.seconds // 3600  # Convert seconds to hours
        
        return days_remaining, hours_remaining

    # Example usage
    # target_date_str = "2025-04-01"
    # days, hours = time_until_target_date(target_date_str)

    # print(f"Days remaining: {days}")
    # print(f"Hours remaining: {hours}")


    async def fetch_payout(self):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token

        dashboard = await self.get_state(DashboardState)
        

        self.loading = True
        yield  # Ensure the UI updates before making the request

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/withdraw/payouts/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                payouts = response.json()
                active_payout = next((p for p in payouts if p["status"] == "Pending"), None)
                if active_payout:
                    self.amount_receivable = active_payout["amount_payable"]
                    self.payout_date = active_payout["payout_date"]
                    data = dashboard.format_date(active_payout["payout_date"])
                    dashboard.receiveable = f'{int(active_payout["amount_payable"]):,}'
                    target_date = datetime.strptime(active_payout["payout_date"], "%Y-%m-%d")
                    current_date = datetime.now()
                    self.is_payout = target_date > current_date
                    time_difference = target_date - current_date
        
                    # Extract days and hours from the time difference
                    self.days_remaining = time_difference.days
                    self.hours_remaining = time_difference.seconds // 3600  # Convert seconds to hours

                else:
                    self.amount_receivable = 0.0
                    self.payout_date = ""

        except Exception as e:
            self.amount_receivable = 0.0
            self.payout_date = ""
            yield rx.toast.error(f"Failed to fetch payout: {str(e)}", position="top-right")  # Use yield for toast

        finally:
            self.loading = False
            yield  # Ensure the UI updates


    async def validate_account(self):
        if len(self.account_number) == 10 and self.bank:  # Ensure account number and bank are valid
            auth_state = await self.get_state(AuthState)
            token = auth_state.token

            self.account_loading = True
            yield  # Ensure the UI updates before making the request

            try:
                print(f"account_loading: {self.account_loading}")
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{BACKEND_URL}/withdraw/get-account-name/",
                        headers={"Authorization": f"Bearer {token}"},
                        params={"account_number": self.account_number, "bank": self.bank}
                    )
                    response.raise_for_status()
                    self.account_name = response.json()  # Set the account name from the response
                    yield rx.toast.success("Account validated successfully!", position="top-right")  # Notify the user

            except httpx.HTTPStatusError as e:
                try:
                    error_detail = e.response.json().get("detail", "Invalid account details")
                except ValueError:
                    error_detail = e.response.text or "Invalid account details"
                self.account_name = f"Error: {error_detail}"
                yield rx.toast.error(f"Validation failed: {error_detail}", position="top-right")  # Notify the user

            except Exception as e:
                self.account_name = f"Error: {str(e)}"
                yield rx.toast.error(f"Unexpected error: {str(e)}", position="top-right")  # Notify the user

            finally:
                self.account_loading = False
                yield  # Ensure the UI updates
        else:
            self.account_name = ""  


    async def withdraw(self):
        auth_state = await self.get_state(AuthState)
        user_id = auth_state.user_id
        group_id = auth_state.group_id
        token = auth_state.token

        if self.payout_date > datetime.now(timezone.utc).isoformat():
            yield rx.toast.error("Withdrawal not allowed: Payout date is in the future", position="top-right")  # Use yield
            return  # Exit early

        amount_str = str(self.amount)
        try:
            amount_float = float(amount_str)
            if not amount_str or amount_float <= 0:
                yield rx.toast.error("Please enter a valid amount", position="top-right")  # Use yield
                return  # Exit early
        except ValueError:
            yield rx.toast.error("Please enter a numeric amount", position="top-right")  # Use yield
            return  # Exit early

        if not user_id or not group_id or not token:
            yield rx.toast.error("Authentication error: Missing user_id, group_id, or token", position="top-right")  # Use yield
            return  # Exit early

        if not self.bank or not self.account_number:
            yield rx.toast.error("Please provide bank and account number", position="top-right")  # Use yield
            return  # Exit early

        self.loading = True
        yield  # Ensure the UI updates before making the request

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{BACKEND_URL}/withdraw/create/",
                    json={
                        "group_id": group_id,
                        "user_id": user_id,
                        "amount": amount_float,
                        "transaction_type": "Withdrawal",
                        "operation": "Create",
                        "bank": self.bank,
                        "account_number": self.account_number
                    },
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                data = response.json()

                # Fetch updated data after withdrawal
                async for _ in self.fetch_balance():
                    pass  # Iterate over the generator
                async for _ in self.fetch_withdrawals():
                    pass  # Iterate over the generator
                async for _ in self.fetch_payout():
                    pass  # Iterate over the generator

                yield rx.toast.success("Withdrawal initiated successfully!", position="top-right")  # Use yield

        except httpx.HTTPStatusError as e:
            try:
                error_detail = e.response.json().get("detail", "Unknown error")
            except ValueError:
                error_detail = e.response.text or "Unknown error"
            yield rx.toast.error(f"Withdrawal failed: {error_detail}", position="top-right")  # Use yield

        except Exception as e:
            yield rx.toast.error(f"Unexpected error: {str(e)}", position="top-right")  # Use yield

        finally:
            self.loading = False
            yield  # Ensure the UI updates

    async def fetch_withdrawals(self):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token

        self.loading = True
        yield  # Ensure the UI updates before making the request

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/withdraw/withdrawals/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                self.withdrawals = response.json()
                self.update_pagination()

        except Exception as e:
            self.withdrawals = [{"error": f"Failed to fetch: {str(e)}"}]
            self.update_pagination()
            yield rx.toast.error(f"Error: {str(e)}", position="top-right")  # Use yield

        finally:
            self.loading = False
            yield  # Ensure the UI updates

    async def toggle_view(self):
        self.view_history = not self.view_history
        if self.view_history and not self.withdrawals:
            async for _ in self.fetch_withdrawals():
                pass  # Iterate over the generator

    def next_page(self):
        if (self.current_page * self.items_per_page) < self.withdrawals_length:
            self.current_page += 1
            self.update_pagination()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def update_pagination(self):
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        self.paginated_withdrawals = self.withdrawals[start:end]

    async def on_mount(self):
        yield
        async for _ in self.fetch_balance():
            pass  # Iterate over the generator
        async for _ in self.fetch_payout():
            pass  # Iterate over the generator