import secrets

def generate_device_id() -> str:
    """Generate a random 16-character hex string representing an Android device ID."""
    return secrets.token_hex(8)
