"""Strict validation — for fake/random emails block ."""

import re

# Strict email regex
EMAIL_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._%+-]{1,}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

# Common fake/spam patterns to reject
BLOCKED_EMAIL_PATTERNS = [
    r"^(test|fake|abc|xyz|aaa|bbb|ccc|ddd|eee|fff|ggg|hhh|iii|jjj|kkk|lll|mmm|nnn|ooo|ppp|qqq|rrr|sss|ttt|uuu|vvv|www|yyy|zzz)@",
    r"^(temp|trash|throwaway|noreply|spam|noone|nobody|null|undefined|example|sample)@",
    r"@(test\.com|example\.com|test\.in|fake\.com|invalid\.com)$",
    r"^(.)\1{3,}@",  # aaaa@, bbbb@, 1111@
    r"^[^@]{1,2}@",  # too short local part (a@, ab@)
]

BLOCKED_EMAIL_RE = [re.compile(p, re.IGNORECASE) for p in BLOCKED_EMAIL_PATTERNS]

# phone no validation - 6-9, 10 digits, no obvious fakes
PHONE_RE = re.compile(r"^[6-9]\d{9}$")

# Blocked phone patterns
BLOCKED_PHONES = {
    "0000000000", "1111111111", "2222222222", "3333333333",
    "4444444444", "5555555555", "6666666666", "7777777777",
    "8888888888", "9999999999", "1234567890", "9876543210",
    "0123456789",
}


def validate_email(email: str) -> bool:
    """Email format valid hai? Strict check."""
    if not email:
        return False
    email = email.strip().lower()
    
    # Basic format check
    if not EMAIL_RE.match(email):
        return False
    
    # Blocked patterns check
    for pattern in BLOCKED_EMAIL_RE:
        if pattern.search(email):
            return False
    
    # Must have at least one dot in domain
    domain = email.split("@")[1]
    if "." not in domain:
        return False
    
    # Domain part before TLD must be at least 2 chars
    parts = domain.split(".")
    if len(parts[0]) < 2:
        return False
    
    return True


def validate_phone(phone: str) -> bool:
    
    if not phone:
        return True 
    digits = re.sub(r"\D", "", phone)
    if not PHONE_RE.match(digits):
        return False
    if digits in BLOCKED_PHONES:
        return False
    
    return True
