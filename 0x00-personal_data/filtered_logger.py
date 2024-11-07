#!/usr/bin/env python3
import re


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated.

    Args:
        fields (list): A list of strings representing all fields to obfuscate.
        redaction (str): A string representing by what the
        field will be obfuscated.
        message (str): A string representing the log line.
        separator (str): A string representing by which character
        is separating all fields in the log line (message).

    Returns:
        str: The log message obfuscated.
    """
    for field in fields:
        a1 = fr"{field}=.+?{separator}"
        a2 = f"{field}={redaction}{separator}"
        message = re.sub(a1, a2, message)
    return message
