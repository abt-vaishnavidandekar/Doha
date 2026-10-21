import re
from fastapi import HTTPException

def check_date(value):
    if not re.fullmatch(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", value):
        return False
        
    return True

def check_time(value):
    if not re.fullmatch(r"^([01]\d|2[0-3]):[0-5]\d$", value):
        return False
        
    return True

def check_phone(value):
    if not re.fullmatch(r"[6-9]\d{9}", value):
        return False
    
    return True


def validate_email(value: str) -> str:
    value = value.strip()
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.fullmatch(pattern, value):
        return False

    return True


def validate_password(value: str) -> str:
    if not re.search(r"[A-Z]", value):
        return False
    
    if not re.search(r"[a-z]", value):
        return False
    
    if not re.search(r"\d", value):
        return False
    
    if not re.search(r"[^A-Za-z0-9]", value):
        return False


    return True