"""
Microsoft Azure AD SSO — OAuth2 Authorization Code Flow
-------------------------------------------------------
Setup steps (one-time, done in Azure Portal):
  1. Go to https://portal.azure.com → Azure Active Directory → App registrations → New registration
  2. Name: "SupportSages Training Portal"
  3. Supported account types: "Accounts in this organizational directory only (Single tenant)"
  4. Redirect URI: Web → http://95.217.135.102/api/auth/microsoft/callback
  5. After creating: copy "Application (client) ID" → MICROSOFT_CLIENT_ID
                     copy "Directory (tenant) ID"    → MICROSOFT_TENANT_ID
  6. Under "Certificates & secrets" → New client secret → copy Value → MICROSOFT_CLIENT_SECRET
  7. Under "API permissions" → Add → Microsoft Graph → Delegated → User.Read → Grant admin consent

Then fill in the three values below.
"""
import os
import secrets
import urllib.parse
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import auth as auth_utils

router = APIRouter(prefix="/auth", tags=["sso"])

# ── Config ────────────────────────────────────────────────────────────────────
# Fill these in after registering the app in Azure AD.
# Or set them as environment variables on the server.
MICROSOFT_CLIENT_ID     = os.getenv("MS_CLIENT_ID",     "YOUR_CLIENT_ID_HERE")
MICROSOFT_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET", "YOUR_CLIENT_SECRET_HERE")
MICROSOFT_TENANT_ID     = os.getenv("MS_TENANT_ID",     "YOUR_TENANT_ID_HERE")

ALLOWED_DOMAIN = "supportsages.com"
REDIRECT_URI   = os.getenv("MS_REDIRECT_URI", "http://95.217.135.102/api/auth/microsoft/callback")
FRONTEND_URL   = os.getenv("FRONTEND_URL",    "http://95.217.135.102")

AUTHORIZE_URL = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/oauth2/v2.0/authorize"
TOKEN_URL     = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/oauth2/v2.0/token"
GRAPH_ME_URL  = "https://graph.microsoft.com/v1.0/me"

# In-memory state store (fine for small scale; cleared on restart)
_pending_states: dict[str, bool] = {}


# ── Step 1: Redirect user to Microsoft login ──────────────────────────────────

@router.get("/microsoft")
def microsoft_login():
    state = secrets.token_urlsafe(24)
    _pending_states[state] = True

    params = {
        "client_id":     MICROSOFT_CLIENT_ID,
        "response_type": "code",
        "redirect_uri":  REDIRECT_URI,
        "response_mode": "query",
        "scope":         "openid email profile User.Read",
        "state":         state,
    }
    url = AUTHORIZE_URL + "?" + urllib.parse.urlencode(params)
    return RedirectResponse(url)


# ── Step 2: Microsoft redirects back here with ?code=... ─────────────────────

@router.get("/microsoft/callback")
async def microsoft_callback(request: Request, code: str = None, state: str = None,
                              error: str = None, error_description: str = None):
    def fail(msg: str):
        encoded = urllib.parse.quote(msg)
        return RedirectResponse(f"{FRONTEND_URL}/login?sso_error={encoded}")

    # Auth error from Microsoft
    if error:
        return fail(error_description or error)

    if not code or not state:
        return fail("Missing code or state from Microsoft.")

    # Validate state to prevent CSRF
    if state not in _pending_states:
        return fail("Invalid or expired SSO state. Please try again.")
    del _pending_states[state]

    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(TOKEN_URL, data={
            "client_id":     MICROSOFT_CLIENT_ID,
            "client_secret": MICROSOFT_CLIENT_SECRET,
            "code":          code,
            "redirect_uri":  REDIRECT_URI,
            "grant_type":    "authorization_code",
        })

    if token_resp.status_code != 200:
        return fail("Failed to exchange code for token. Check Azure AD app configuration.")

    access_token = token_resp.json().get("access_token")
    if not access_token:
        return fail("No access token in Microsoft response.")

    # Get user profile from Microsoft Graph
    async with httpx.AsyncClient() as client:
        me_resp = await client.get(GRAPH_ME_URL, headers={"Authorization": f"Bearer {access_token}"})

    if me_resp.status_code != 200:
        return fail("Could not retrieve user info from Microsoft.")

    profile = me_resp.json()
    email = (profile.get("mail") or profile.get("userPrincipalName") or "").lower().strip()
    display_name = profile.get("displayName") or email.split("@")[0]

    if not email:
        return fail("Could not read email from your Microsoft account.")

    # Only allow @supportsages.com
    if not email.endswith(f"@{ALLOWED_DOMAIN}"):
        return fail(f"Only @{ALLOWED_DOMAIN} accounts are allowed.")

    # Find or create user in DB
    db: Session = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()

        if not user:
            # Create new trainee account from SSO
            username = email.split("@")[0].replace(".", "_").replace("-", "_")
            # Ensure username is unique
            base = username
            counter = 1
            while db.query(models.User).filter(models.User.username == username).first():
                username = f"{base}{counter}"
                counter += 1

            user = models.User(
                username=username,
                email=email,
                full_name=display_name,
                password_hash=auth_utils.hash_password(secrets.token_urlsafe(32)),
                role="trainee",
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Generate portal JWT
        jwt_token = auth_utils.create_access_token({"sub": str(user.id), "role": user.role})

        params = urllib.parse.urlencode({
            "sso_token": jwt_token,
            "role":      user.role,
            "name":      user.full_name or user.username,
            "user_id":   user.id,
        })
        return RedirectResponse(f"{FRONTEND_URL}/login?{params}")

    finally:
        db.close()
