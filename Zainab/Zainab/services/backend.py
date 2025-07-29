import httpx

BASE_URL = "http://127.0.0.1:8001"


async def create_group(payload):
    """
    Registers a student.

    Args:
        payload (dict): A dictionary containing the student's details.

    Returns:
        dict: A dictionary containing the student's details if successful, or an error message.
    """

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BASE_URL}/groups/create-group/", json=payload)
            response.raise_for_status()  # Raise an error for bad status codes
            return response
        except Exception as exc:
            
            return f"Error: {exc}"


async def user_signin(user_id, password):
    """
    Validates student credentials.

    Args:
        matriculation_number (str): The student's matriculation number.
        password (str): The student's password.

    Returns:
        dict: A dictionary containing the student's details if successful, or an error message.
    """
    async with httpx.AsyncClient() as client:

        try:
            response = await client.post(
                f"{BASE_URL}/login/",
                data={"username": user_id, "password": password}
            )
            response.raise_for_status()  
            return response
        except Exception as exc:
            return f"Error: {exc}"


async def user_signup(payload):
    """
    Registers a student.

    Args:
        payload (dict): A dictionary containing the student's details.

    Returns:
        dict: A dictionary containing the student's details if successful, or an error message.
    """

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BASE_URL}/users/create-user/", json=payload)
            response.raise_for_status()  # Raise an error for bad status codes
            return response
        except Exception as exc:
            return f"Error: {exc}"
