"""Minimal one-time-password store for two-factor authentication."""

import secrets

_OTPS: dict[str, str] = {}


def issue_otp(username: str) -> str:
    otp = f"{secrets.randbelow(1_000_000):06d}"
    _OTPS[username] = otp
    return otp


def verify_otp(username: str, otp: str) -> bool:
    return _OTPS.get(username) == otp
