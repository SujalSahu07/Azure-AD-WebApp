from flask import Flask, redirect, url_for, session, request, render_template
import msal
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Read environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]

# MSAL configuration
msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

@app.route('/')
def home():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('home.html', user=session['user'])

@app.route('/login')
def login():
    auth_url = msal_app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    return render_template('login.html', login_url=auth_url)

@app.route('/getAToken')
def get_token():
    if "code" not in request.args:
        return redirect(url_for("login"))
    token_response = msal_app.acquire_token_by_authorization_code(
        request.args["code"], scopes=SCOPE, redirect_uri=REDIRECT_URI
    )
    if "access_token" in token_response:
        session["user"] = token_response.get("id_token_claims")
        return redirect(url_for("home"))
    return "Login failed"

@app.route('/logout')
def logout():
    session.clear()
    return redirect("https://login.microsoftonline.com/common/oauth2/v2.0/logout")

if __name__ == "__main__":
    app.run(debug=True)
