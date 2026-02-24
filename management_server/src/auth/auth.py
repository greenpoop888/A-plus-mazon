from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
from ..config.config import settings

security = HTTPBearer()


REGION = settings.REGION
USER_POOL_ID = settings.COGNITO_USER_POOL_ID
APP_CLIENT_ID = settings.COGNITO_CLIENT_ID
JWKS_URL = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"

def get_current_user(res: HTTPAuthorizationCredentials = Depends(security)):
    token = res.credentials
    try:
        payload = jwt.decode(token, requests.get(JWKS_URL).json(), algorithms=["RS256"], audience=APP_CLIENT_ID)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )