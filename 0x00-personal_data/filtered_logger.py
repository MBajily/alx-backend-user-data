#!/usr/bin/env python3
import re
from typing import List


def filter_datum(fields, redaction, message, separator):
    """Obfuscates the specified fields in a log message."""
    for field in fields:
        a = fr"{field}=[^{separator}]*"
        b = f"{field}={redaction}"
        message = re.sub(a, b, message)
    return message
