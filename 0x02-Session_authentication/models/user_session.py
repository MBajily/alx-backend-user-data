#!/usr/bin/env python3
"""User session module."""
from models.base import Base
from typing import Optional


class UserSession(Base):
    """Class representing a user session."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance."""
        super().__init__(*args, **kwargs)
        self.user_id: Optional[str] = kwargs.get('user_id')
        self.session_id: Optional[str] = kwargs.get('session_id')
