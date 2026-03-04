"""TOTP (Time-based One-Time Password) generation."""

import base64
import hashlib
import hmac
import struct
import time


def generate_totp(secret: str, interval: int = 30) -> str:
    """
    Generate a TOTP code from a secret.

    Args:
        secret: Base32-encoded TOTP secret
        interval: Time interval in seconds (default 30)

    Returns:
        6-digit TOTP code as string

    Example:
        >>> code = generate_totp("JBSWY3DPEHPK3PXP")
        >>> len(code)
        6
    """
    # Normalize and pad secret
    secret = secret.upper().replace(" ", "")
    padding = "=" * ((8 - len(secret) % 8) % 8)
    key = base64.b32decode(secret + padding)

    # Calculate counter from current time
    counter = int(time.time() // interval)
    counter_bytes = struct.pack(">Q", counter)

    # Generate HMAC-SHA1
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    # Dynamic truncation
    offset = hmac_hash[-1] & 0x0F
    truncated = struct.unpack(">I", hmac_hash[offset : offset + 4])[0]

    # Generate 6-digit code
    code = (truncated & 0x7FFFFFFF) % 1000000
    return str(code).zfill(6)


def get_totp_remaining_seconds(interval: int = 30) -> int:
    """
    Get seconds remaining until next TOTP code.

    Args:
        interval: Time interval in seconds

    Returns:
        Seconds until next code
    """
    return interval - (int(time.time()) % interval)


def wait_for_fresh_totp(min_seconds: int = 5, interval: int = 30) -> None:
    """
    Wait until TOTP has at least min_seconds validity.

    Useful to avoid race conditions when entering TOTP.

    Args:
        min_seconds: Minimum seconds of validity needed
        interval: TOTP interval
    """
    remaining = get_totp_remaining_seconds(interval)
    if remaining < min_seconds:
        wait_time = interval - remaining + 1
        time.sleep(wait_time)
