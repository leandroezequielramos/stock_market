from typing import List
import secrets


def generate_api_key(system_api_keys: List[str], nbytes: int) -> str:
    api_key = secrets.token_urlsafe(nbytes=nbytes)
    while api_key in system_api_keys:
        # The intention here is to avoid collitions
        api_key = secrets.token_urlsafe(nbytes=nbytes)
    return api_key
