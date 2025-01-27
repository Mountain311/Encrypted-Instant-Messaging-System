# util.py (same as before)
import secrets

KEY_LENGTH = 128


def format_key(key: str) -> str:
    key_str = ""
    count = 0

    for i in str(key):
        if count <= 3:
            key_str += i
            count += 1
        else:
            count = 0
            key_str += " "

    return key_str.strip()


def generate_key() -> int:
    return secrets.randbits(KEY_LENGTH)
