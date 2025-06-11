from functools import wraps
from flask import redirect, url_for, flash, request

from werkzeug.security import generate_password_hash, check_password_hash

from backend.models import db, User

def validate_signup_data(func):
    @wraps(func)
    def validate_and_proceed(*args, **kwargs):

        if request.method == 'POST':
            data = request.form

            username = data.get("username")
            password = data.get("password")
            email = data.get("email")

            # Check if all fields filled
            if not username or not password or not email:
                flash("Required fields missing.", "error")
                return redirect(url_for('registration_login.signup'))

            # Check email validation
            if '@' not in email or '.' not in email.split('@')[-1]:
                flash("Invalid email format.", "error")
                return redirect(url_for('registration_login.signup'))

            # Check if password characters long
            if len(password) < 8:
                flash("Password must be at least 8 characters long.", "error")
                return redirect(url_for('registration_login.signup'))

            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                flash("Email already registered, Please try again with valid email.", "error")
                return redirect(url_for('registration_login.signup'))
        
        return func(*args, **kwargs)
    
    return validate_and_proceed

def validate_login_data(func):
    @wraps(func)
    def validate_and_proceed(*args, **kwargs):

        if request.method == 'POST':
            data = request.form

            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                flash("Required fields missing.", "error")
                return redirect(url_for('registration_login.login'))

            # Check if username already exists
            user = User.query.filter_by(username=username).first()

            # Hashed_password = password
            hashed_password = user.password
            is_password_correct = check_password_hash(hashed_password, password)

            if not user or not check_password_hash(user.password, password):
                flash("Username or password, not found.", "error")
                return redirect(url_for('registration_login.login'))

        return func(*args, **kwargs)

    return validate_and_proceed