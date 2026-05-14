import re

def is_valid_email(target: str) -> bool:
    """
    Validates email format using a standard regex.
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(email_regex, target))

def is_valid_domain(target: str) -> bool:
    """
    Validates domain names (e.g., example.com, sub.example.co.uk).
    """
    # Simplified domain regex: must have at least one dot and no protocol
    domain_regex = r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"
    return bool(re.match(domain_regex, target, re.IGNORECASE))

def is_valid_phone(target: str) -> bool:
    """
    Validates phone numbers. Supports (CC)Number and +CCNumber formats.
    Example: (966)500000000 or +966500000000
    """
    # Clean up common formatting before checking
    cleaned = target.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+", "")
    
    # Check if what's left is all digits and a reasonable length (7-15 digits)
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15

def determine_target_type(target: str) -> str:
    """
    The 'Traffic Controller' of the tool. It guesses the target type.
    
    EXPANSION POINT:
    To add a NEW target type (e.g., IP Address or MAC Address):
    1. Write a new validation function 'is_valid_ip(target)'.
    2. Add an elif block here to return "ip".
    """
    if is_valid_email(target):
        return "email"
    elif is_valid_domain(target):
        return "domain"
    elif is_valid_phone(target):
        return "phone"
    else:
        # If it doesn't match the specific patterns, we treat it as a username
        return "username"
