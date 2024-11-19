#!/usr/bin/env python3
"""
Authentication module for user authentication service
"""
import bcrypt
import uuid
from db import DB
from user import User
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt

    Args:
        password (str): Password to hash

    Returns:
        bytes: Salted hash of the password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a new UUID

    Returns:
        str: String representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database"""

    def __init__(self):
        """Initialize the Auth object"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register new user

        Args:
            email (str): User's email
            password (str): User's password

        Returns:
            User: The newly created user

        Raises:
            ValueError: If user with email already exists
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login credentials

        Args:
            email (str): User's email
            password (str): User's password

        Returns:
            bool: True if credentials are valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            user_password = user.hashed_password
            user_encode = password.encode('utf-8')
            return bcrypt.checkpw(user_encode, user_password)
        except Exception:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Create a new session for the user

        Args:
            email (str): User's email

        Returns:
            str or None: Session ID if user exists, None otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Get user by session ID

        Args:
            session_id (str): Session ID to search for

        Returns:
            User or None: User if found, None otherwise
        """
        if not session_id:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy user's session

        Args:
            user_id (int): User's ID
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate reset password token

        Args:
            email (str): User's email

        Returns:
            str: Reset password token

        Raises:
            ValueError: If user doesn't exist
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update user's password using reset token

        Args:
            reset_token (str): Reset password token
            password (str): New password

        Raises:
            ValueError: If reset token is invalid
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
            )
        except Exception:
            raise ValueError
