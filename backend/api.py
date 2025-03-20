from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
import requests
import json

KEYCLOAK_URL = "http://architecture-sprint-8-keycloak-1:8080"
REALM = "reports-realm"
CLIENT_ID = "reports-frontend"
JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

app = FastAPI()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
)

def get_jwks():
    response = requests.get(JWKS_URL)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=500, detail="Unable to fetch JWKS")

JWKS = get_jwks()

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        key = next((k for k in JWKS["keys"] if k["kid"] == kid), None)

        if not key:
            raise HTTPException(status_code=401, detail="Invalid token signature")

        public_key = json.dumps(key)
        payload = jwt.decode(token, public_key, algorithms=["RS256"], audience=CLIENT_ID)
        
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(payload=Depends(verify_token)):
    roles = payload.get("realm_access", {}).get("roles", [])
    if "prothetic_user" not in roles:
        raise HTTPException(status_code=403, detail="Access denied")
    return payload

@app.get("/reports")
def get_reports(user=Depends(get_current_user)):
    return {
        "user": user["preferred_username"],
        "report": {
            "device_id": "72384792384",
            "device_name": "SANDALI-3000",
            "uptime": "1000 hours",
            "error_logs": ["No errors detected"],
            "battery_health": "22%"
        }
    }
