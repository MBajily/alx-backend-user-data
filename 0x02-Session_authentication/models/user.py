#!/usr/bin/env python3
"""User module."""
import hashlib
from models.base import Base
from typing import Optional


class User(Base):
    """User class representing a system user."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance."""
        super().__init__(*args, **kwargs)
        self.email: Optional[str] = kwargs.get('email')
        self._password: Optional[str] = kwargs.get('_password')
        self.first_name: Optional[str] = kwargs.get('first_name')
        self.last_name: Optional[str] = kwargs.get('last_name')

    @property
    def password(self) -> Optional[str]:
        """Get the hashed password."""
        return self._password

    @password.setter
    def password(self, pwd: Optional[str]) -> None:
        """Set a new password, encrypting it with SHA256.
        
        WARNING: For production systems, use stronger algorithms like bcrypt or argon2.
        """
        if pwd and isinstance(pwd, str):
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()
        else:
            self._password = None

    def is_valid_password(self, pwd: Optional[str]) -> bool:
        """Validate the provided password against the stored hashed password."""
        if not pwd or not isinstance(pwd, str) or not self.password:
            return False
        return hashlib.sha256(pwd.encode()).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """Return a formatted display name for the user."""
        if not self.email and not self.first_name and not self.last_name:
            return ""
        if not self.first_name and not self.last_name:
            return self.email or ""
        if not self.last_name:
            return self.first_name or ""
        if not self.first_name:
            return self.last_name or ""
        return f"{self.first_name} {self.last_name}"
