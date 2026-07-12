"""Liveness endpoint used by orchestrators and load balancers."""

import time

_STARTED_AT = time.time()


def health_check() -> dict:
    return {"status": "ok", "uptime_seconds": time.time() - _STARTED_AT}


def health_blueprint() -> dict:
    return {"/health": health_check}
