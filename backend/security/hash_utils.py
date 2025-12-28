import hashlib

def hash_text(text: str) -> str:
    """
    Returns SHA-256 hash of the given text.
    Used for data integrity verification.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
