# Dummy authentication storage (use a DB in real life)
USERS = {}

def register_user(name, dob, email, password):
    USERS[email] = {"name": name, "dob": dob, "password": password}

def authenticate_user(email, password):
    return email in USERS and USERS[email]["password"] == password
