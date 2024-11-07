import re


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated.

    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character
    is separating all fields in the log line (message)
    """
    for field in fields:
        a1 = f'{field}=.*?{separator}'
        a2 = f'{field}={redaction}{separator}'
        message = re.sub(a1, a2, message)
    return message
