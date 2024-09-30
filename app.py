from flask import Flask, redirect, url_for, session, request, render_template
import msal
import os
import logging


app = Flask(__name__)
app.secret_key = os.urandom(24)

logging.basicConfig(level=logging.DEBUG)

# Read environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]


# MSAL configuration
msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

@app.route('/')
def home():
    if not session.get("user"):
        return redirect(url_for("login"))
    user = session["user"]
    roles = user.get("roles", [])
    if "Admin" in roles or "User" in roles:
        return render_template('home.html', user=user)
    else:
        return "Access denied: You do not have the required role to view this page.", 403

@app.route('/login')
def login():
    auth_url = msal_app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    return render_template('login.html', login_url=auth_url)

@app.route('/getAToken')
def get_token():
    if "code" not in request.args:
        logging.error("Authorization code not found in request.")
        return redirect(url_for("login"))
    
    logging.debug("Authorization code found in request.")
    token_response = msal_app.acquire_token_by_authorization_code(
        request.args["code"], scopes=SCOPE, redirect_uri=REDIRECT_URI
    )
    
    logging.debug(f"Token response: {token_response}")  # Log the token response
    
    if "access_token" in token_response:
        # user's roles from id_token
        user_roles = token_response.get("id_token_claims").get("roles", [])
        session["user"] = {
            "username": token_response.get("id_token_claims").get("name"),
            "roles": user_roles
        }
        return redirect(url_for("home"))
    
    logging.error(f"Token acquisition failed: {token_response}")  # Log the failure
    return "Login failed"

@app.route('/logout')
def logout():
    session.clear()
    return redirect("https://login.microsoftonline.com/common/oauth2/v2.0/logout")

if __name__ == "__main__":
    app.run(debug=True)
    
