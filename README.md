# **🌐 Azure AD Integrated Python Web App**

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/theryb/Azure-AD/app.yml?branch=main) 
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/github/license/theryb/Azure-AD)
![Repo Size](https://img.shields.io/github/repo-size/theryb/Azure-AD)

This project is a **Python** web application integrated with **Azure Active Directory (Azure AD)** for authentication. Users are authenticated using their Microsoft account, and role-based access control is enforced to allow or deny access to certain parts of the app.

## 🚀 Features

- **Azure AD Authentication** using MSAL
- **Role-Based Access Control (RBAC)** to restrict access based on user roles (Admin/User)
- **Flask** web framework
- User login and logout functionality
- Minimal and clean UI design with custom styles
- **Environment variables** for secure configuration

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS (with custom styles)
- **Authentication**: Azure AD using MSAL
- **Role-Based Access Control**: Azure AD roles (Admin/User)
- **Environment Management**: `.env` file

---

## 📝 Installation & Setup

###  Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


# Create a Virtual Environment (Optional but Recommended) :-

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


# Install Dependencies :-

pip install -r requirements.txt


# Set Up Environment Variables :-

Create a .env file in the root of the project with the following content:

TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
REDIRECT_URI=http://localhost:5000/getAToken

Note: The .env file contains sensitive information and should not be pushed to GitHub. Ensure that it is listed in your .gitignore file to prevent accidental commits.


# Run the App :-

flask run
The application will be available at http://localhost:5000.


# 📂 Project Structure 

.
├── static
│   └── css
│       └── styles.css        # CSS file for styling
├── templates
│   ├── home.html             # Home page after login
│   └── login.html            # Login page for Microsoft authentication
├── .gitignore                 # Specifies files to be ignored by Git
├── .env                       # Environment variables (not to be pushed)
├── .env.example               # Example environment variable file for reference
├── app.py                     # Main Flask app
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation

```


## 📚 How It Works 

1. When users visit the home page (/), they are redirected to the login page if they are not authenticated.
2. The login page generates a Microsoft login URL using MSAL and redirects the user to Microsoft login.
3. Upon successful login, Azure AD returns an authorization code to the redirect URI (/getAToken).
4. The authorization code is exchanged for an access token, and the user's information is saved in the session.
5. The user is then redirected to the home page, where their profile information is displayed.
6. Users can log out by clicking the "Logout" button, clearing their session.


## 🛡️ Role-Based Access Control (RBAC)

In this app, role-based access is controlled as follows:

1. Only users with roles "Admin" or "User" can access the home page.
2. Users without the required roles will be shown an "Access Denied" message with an HTTP status code 403.

You can define additional routes and check user roles before granting access.

```bash
@app.route('/admin')
def admin_page():
    if not has_role("Admin"):
        return "Access denied: You do not have the required role to view this page.", 403
    return render_template('admin.html')

@app.route('/user')
def user_page():
    if not has_role("User"):
        return "Access denied: You do not have the required role to view this page.", 403
    return render_template('user.html')
```

## 🔑 Azure AD Configuration 

To integrate Azure AD, you need to:

1. Register your app in the Azure Portal.
2. Set up a client secret and configure redirect URIs.
3. Define API permissions, e.g., User.Read.
4. Assign roles (Admin/User) to users in the Azure Portal.
5. Use the credentials in your .env file for local development.


## 🤖 Continuous Integration 

This project includes a GitHub Actions workflow to automate the installation of dependencies and run tests on each push and pull request. The workflow is defined in the .github/workflows/app.yml file.


## 🎉 Acknowledgements 

1. Flask for making Python web apps simple.
2. MSAL for Python for seamless Azure AD integration.
3. Azure Active Directory for providing role-based access control functionality.

