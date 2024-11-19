#!/usr/bin/env python3
"""
End-to-end integration test for user authentication service
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a new user
    """
    response = requests.post(f"{BASE_URL}/users", data={
        "email": email,
        "password": password
    })
    message = f"Failed to register user: {response.text}"
    assert response.status_code == 200, message
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with incorrect password
    """
    response = requests.post(f"{BASE_URL}/sessions", data={
        "email": email,
        "password": password
    })
    message = "Login with wrong password should fail"
    assert response.status_code == 401, message


def log_in(email: str, password: str) -> str:
    """
    Log in and return session ID
    """
    response = requests.post(f"{BASE_URL}/sessions", data={
        "email": email,
        "password": password
    })
    assert response.status_code == 200, f"Failed to log in: {response.text}"
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Attempt to access profile without logging in
    """
    response = requests.get(f"{BASE_URL}/profile")
    message = "Unlogged profile access should be forbidden"
    assert response.status_code == 403, message


def profile_logged(session_id: str) -> None:
    """
    Access profile with valid session ID
    """
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    message = f"Failed to access profile: {response.text}"
    assert response.status_code == 200, message
    message = "Profile response should contain email"
    assert "email" in response.json(), message


def log_out(session_id: str) -> None:
    """
    Log out the user
    """
    cookies = {"session_id": session_id}
    req_url = f"{BASE_URL}/sessions"
    response = requests.delete(req_url, cookies=cookies)
    message = f"Failed to log out: {response.text}"
    assert response.status_code == 200, message


def reset_password_token(email: str) -> str:
    """
    Get reset password token
    """
    data = {"email": email}
    response = requests.post(f"{BASE_URL}/reset_password", data=data)
    message = f"Failed to get reset password token: {response.text}"
    assert response.status_code == 200, message
    assert "reset_token" in response.json(), "Reset token not in response"
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update password using reset token
    """
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    message = f"Failed to update password: {response.text}"
    assert response.status_code == 200, message
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
