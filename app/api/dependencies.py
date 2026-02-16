from fastapi import HTTPException, Request
from app.core.security import verify_token
from app.core.redis import redis_client
import json


def _parse_authorization_header(request: Request) -> str:
    """Parse and validate Authorization header, returning the token."""
    auth = request.headers.get("Authorization")
    if not auth:
        raise HTTPException(401, "Missing token")
    
    parts = auth.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(401, "Invalid authorization header format")
    
    return parts[1]
