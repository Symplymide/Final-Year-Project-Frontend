import reflex as rx
import httpx
from datetime import datetime, timezone
from .auth_state import AuthState

BACKEND_URL = "http://localhost:8001"


def format_timestamp(date_string: str) -> str:
    # Ensure input is a string
    date_str = str(date_string)
    
    # Try parsing the ISO 8601 format with T
    try:
        
        dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        formatted_date = dt.strftime('%A, %d %B %Y')
        return formatted_date
    except ValueError as e:
        # print(f"Format %Y-%m-%dT%H:%M:%S.%f%z failed: {str(e)}")
        
        # Fallback to other common formats if needed
        possible_formats = [
            '%Y-%m-%d %H:%M:%S.%f%z',  # e.g., "2025-03-21 21:02:27.465894+01"
            '%Y-%m-%d %H:%M:%S%z',     # e.g., "2025-03-21 21:02:27+01"
            '%Y-%m-%d',                # e.g., "2025-03-21"
            '%Y-%m-%d %H:%M:%S',       # e.g., "2025-03-21 21:02:27"
        ]
        for fmt in possible_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                formatted_date = dt.strftime('%A, %d %B %Y')
                return formatted_date
            except ValueError as e:
                continue
        
        # Final fallback if all formats fail
        return date_str

class NotificationState(rx.State):
    recipients_type: list[str] = ["All Members", "Yet to Contribute", "General"]
    loading: bool = False
    view_history: bool = False
    message_count: int = 0
    message_title: str = ""
    message_content: str = ""
    reminder_date: str = ""
    recipient: str = ""
    message_type: str = "Notification"
    delivery_type: str = "In_app"
    notifications: list[dict] = []
    current_page: int = 1
    items_per_page: int = 5
    paginated_notification: list[dict] = []

    selected_notification: dict = {}
    show_dialog: bool = False

    @rx.var
    def selected_title(self) -> str:
        return self.selected_notification.get('title') or 'N/A'

    @rx.var
    def selected_content(self) -> str:
        return self.selected_notification.get('content') or 'N/A'

    @rx.var
    def selected_date(self) -> str:
        return format_timestamp(self.selected_notification.get('created_at')) or 'N/A'

    @rx.var
    def selected_message_type(self) -> str:
        return self.selected_notification.get('message_type') or 'N/A'

    # Preprocess paginated notifications with formatted timestamps
    @rx.var
    def formatted_paginated_notifications(self) -> list[dict]:
        return [
            {   "message_id": n.get("message_id"),
                "title": n.get("title", ""),
                "message_type": n.get("message_type", ""),
                "content": n.get("content", ""),
                "created_at": format_timestamp(n.get("created_at", ""))
            }
            for n in self.paginated_notification
        ]

    async def set_message_title(self, value: str):
        self.message_title = value

    async def set_message_content(self, value: str):
        self.message_content = value

    async def set_reminder_date(self, value: str):
        self.reminder_date = value

    async def set_recipients(self, value: str):
        self.recipient = value

    async def set_message_type(self, value: str):
        self.message_type = value

    async def set_delivery_type(self, value: str):
        self.delivery_type = value

    async def create_notification(self):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token

        # Validation checks
        if not self.message_title:
            yield rx.toast.error("Message title is required.", position="top-right")
            return

        if not self.message_content:
            yield rx.toast.error("Message content is required.", position="top-right")
            return

        if not self.message_type:
            yield rx.toast.error("Message type is required.", position="top-right")
            return

        if not self.delivery_type:
            yield rx.toast.error("Delivery type is required.", position="top-right")
            return

        if not self.recipient:
            yield rx.toast.error("Recipient type is required.", position="top-right")
            return

        if self.recipient not in self.recipients_type:
            yield rx.toast.error("Invalid recipient type.", position="top-right")
            return
        
        formatted_date = datetime.strptime(self.reminder_date, "%Y-%m-%d").date()

        self.loading = True
        yield  # Ensure the UI updates before making the request

        try:
            payload = {
                "group_id": auth_state.group_id,
                "title": self.message_title,
                "content": self.message_content,
                "message_type": self.message_type,
                "delivery_type": self.delivery_type,
                "reminder_date": str(formatted_date),  
                "recipient_type": self.recipient,
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{BACKEND_URL}/notification/create-notifications/",
                    headers={"Authorization": f"Bearer {token}"},
                    json=payload,
                )

                response.raise_for_status()
                self.reset_fields()
                yield rx.toast.success("Notification created successfully!", position="top-right")
        except Exception as e:
            yield rx.toast.error(f"Failed to create notification: {str(e)}", position="top-right")
        finally:
            self.loading = False
            yield  # Ensure the UI updates after the request

    def reset_fields(self):
        self.message_title = ""
        self.message_content = ""
        self.reminder_date = ""
        self.recipient = ""
        self.message_type = ""
        self.delivery_type = ""

    async def fetch_notification(self):
        auth_state = await self.get_state(AuthState)
        token = auth_state.token

        self.loading = True
        yield  # Ensure the UI updates before making the request

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BACKEND_URL}/notification/messages/",
                    headers={"Authorization": f"Bearer {token}"},
                )
                response.raise_for_status()
                self.notifications = response.json()
                # print(self.notifications)
                self.update_pagination()
        except Exception as e:
            yield rx.toast.error(f"Failed to fetch notifications: {str(e)}", position="top-right")
        finally:
            self.loading = False
            yield  # Ensure the UI updates after the request

    async def toggle_view(self):
        self.view_history = not self.view_history
        if self.view_history:
            async for event in self.fetch_notification():
                if event:
                    yield event

    def next_page(self):
        if (self.current_page * self.items_per_page) < self.notification_length:
            self.current_page += 1
            self.update_pagination()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def update_pagination(self):
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        self.paginated_notification = self.notifications[start:end]


    def open_dialog(self, message_id: int):
        self.show_dialog = True
        notific = next((message for message in self.notifications if str(message["message_id"]) == str(message_id)), None)
        if notific:
            self.selected_notification = notific
            self.show_dialog = True
            yield  # Ensure UI updates
        else:
            yield rx.toast.error(f"No user found for user_id: {message_id}", position="top-right")
            print(f"No user found for user_id: {message_id}")

    def close_dialog(self):
        self.show_dialog = False