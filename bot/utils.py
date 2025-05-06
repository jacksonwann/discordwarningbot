import re

def is_valid_reason(reason: str) -> bool:
    """
    Validates a reason string using RegEx:
    - Only allows letters, numbers, spaces, and punctuation
    - Must be 5 to 100 characters long
    """
    pattern = r"^[a-zA-Z0-9 ,.!?'-]{5,100}$"
    return bool(re.match(pattern, reason))