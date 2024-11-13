#!/usr/bin/env python3
"""Base module."""
import json
import uuid
from os import path
from datetime import datetime
from typing import TypeVar, List, Iterable, Dict, Optional

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA: Dict[str, Dict[str, 'Base']] = {}


class Base:
    """Base class."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Base instance."""
        class_name = self.__class__.__name__

        # Initialize class storage if not already present
        if class_name not in DATA:
            DATA[class_name] = {}

        self.id: str = kwargs.get('id', str(uuid.uuid4()))
        self.created_at: datetime = self._parse_datetime(kwargs.get('created_at')) or datetime.utcnow()
        self.updated_at: datetime = self._parse_datetime(kwargs.get('updated_at')) or datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Check if two Base objects are equal."""
        return isinstance(other, Base) and self.id == other.id

    @staticmethod
    def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
        """Parse a datetime string to a datetime object."""
        if value:
            return datetime.strptime(value, TIMESTAMP_FORMAT)
        return None

    def to_json(self, for_serialization: bool = False) -> dict:
        """Convert the object to a JSON dictionary."""
        return {
            key: (value.strftime(TIMESTAMP_FORMAT) if isinstance(value, datetime) else value)
            for key, value in self.__dict__.items()
            if for_serialization or not key.startswith('_')
        }

    @classmethod
    def _get_file_path(cls) -> str:
        """Generate the file path for storing objects."""
        return f".db_{cls.__name__}.json"

    @classmethod
    def load_from_file(cls) -> None:
        """Load all objects from a file."""
        file_path = cls._get_file_path()
        class_name = cls.__name__

        DATA[class_name] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as file:
            objects_json = json.load(file)
            for obj_json in objects_json.values():
                obj = cls(**obj_json)
                DATA[class_name][obj.id] = obj

    @classmethod
    def save_to_file(cls) -> None:
        """Save all objects to a file."""
        file_path = cls._get_file_path()
        class_name = cls.__name__

        with open(file_path, 'w') as file:
            json.dump({obj.id: obj.to_json(True) for obj in DATA[class_name].values()}, file)

    def save(self) -> None:
        """Save the current object."""
        self.updated_at = datetime.utcnow()
        DATA[self.__class__.__name__][self.id] = self
        self.__class__.save_to_file()

    def remove(self) -> None:
        """Remove the current object."""
        class_name = self.__class__.__name__
        if self.id in DATA[class_name]:
            del DATA[class_name][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Count all objects of this class."""
        return len(DATA.get(cls.__name__, {}))

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """Return all objects of this class."""
        return list(DATA.get(cls.__name__, {}).values())

    @classmethod
    def get(cls, obj_id: str) -> Optional[TypeVar('Base')]:
        """Return one object by ID."""
        return DATA.get(cls.__name__, {}).get(obj_id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search all objects with matching attributes."""
        def matches(obj: Base) -> bool:
            return all(getattr(obj, key, None) == value for key, value in attributes.items())
        
        return [obj for obj in DATA.get(cls.__name__, {}).values() if matches(obj)]
