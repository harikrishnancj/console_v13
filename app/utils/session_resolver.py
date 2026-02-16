import json
from fastapi import HTTPException
from app.core.redis import redis_client
from app.core.security import verify_token

def get_session_identity(session_id: str):
    
    # 1. Lookup Session in Redis
    vault_json = redis_client.get(f"session:{session_id}")
    if not vault_json:
        raise HTTPException(status_code=401, detail="Invalid Session")
        
    # 2. Open Vault
    try:
        vault = json.loads(vault_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=401, detail="Invalid Session Data")

    # 3. Verify Internal Access Token 
    access_token = vault.get("access_token")
    payload = verify_token(access_token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Session Expired")

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
        
    # 4. Extract Identity Information
    tenant_id = vault.get("tenant_id")
    user_id = vault.get("user_id")
    role = vault.get("role")
    
    # Logic to normalize tenant_id for different roles
    # If the user is a tenant themselves, the user_id is the tenant_id
    if tenant_id is None:
        if role == "tenant":
            tenant_id = user_id
        else:
            # Check payload as fallback if vault structure is older
            tenant_id = payload.get("tenant_id")

    if tenant_id is None:
        raise HTTPException(status_code=401, detail="Tenant identity not found")

    return {
        "tenant_id": int(tenant_id),
        "user_id": int(user_id) if vault.get("type") == "user" else None,
        "role": role,
        "type": vault.get("type")
    }
