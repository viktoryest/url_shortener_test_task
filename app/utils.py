import secrets
import string

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6


def generate_short_code() -> str:
    """Generate a random short code using base62 alphabet."""
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


def build_short_url(base_url: str, code: str) -> str:
    """Format the final short URL."""
    return f"{base_url.rstrip('/')}/{code}"
