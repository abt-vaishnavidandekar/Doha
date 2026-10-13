import re
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException



def check_phone(value):
    if not re.fullmatch(r"[6-9]\d{9}", value):
        raise HTTPException(
            status_code=400,
            detail= "Enter a valid Phone Number with proper 10 digits",
        )
    return value


def validate_email(value: str) -> str:
    value = value.strip()
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.fullmatch(pattern, value):
        raise HTTPException(
            status_code=400,
            detail="Enter a valid Email",
        )
        
    
    return value.lower()


def validate_password(value: str) -> str:
    if not re.search(r"[A-Z]", value):
        raise HTTPException(
            status_code=400,
            detail="Password needs an uppercase letter",
        )
    if not re.search(r"[a-z]", value):
        raise HTTPException(
            status_code=400,
            detail="Password needs a lowercase letter",
        )
    if not re.search(r"\d", value):
        raise HTTPException(
            status_code=400,
            detail="Password needs a digit letter",
        )
    if not re.search(r"[^A-Za-z0-9]", value):
        raise HTTPException(
            status_code=400,
            detail="Password needs an Special Character",
        )
    if len(value.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must not exceed 72 UTF-8 bytes",
        )

    return value