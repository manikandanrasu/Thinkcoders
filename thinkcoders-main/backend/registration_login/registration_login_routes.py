from flask import request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from backend.models import db, User

from backend.registration_login import registration_login_bp
from backend.registration_login.registration_login_api_service import generate_token, confirm_token, send_email

from backend.registration_login.validate_registration_data import validate_signup_data, validate_login_data

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Route: Regsiter new user
@registration_login_bp.route('/signup', methods=['GET', 'POST'])
@validate_signup_data
def signup():
    try:
        if request.method == 'GET':
            return render_template('signup.html')

        data = request.form
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Password hash
        password_hash = generate_password_hash(password)
        
        # Register user
        user = User(username=username, email=email, password=password_hash)

        try:
            db.session.add(user)
            db.session.commit()

        except Exception as e:
            logger.error(f"Database commit failed: {str(e)}")
            flash("Something went wrong, during signup.", "error")
            return redirect(url_for('registration_login_bp.signup'))
        
        # Send verification link for verified user
        try:
            token = generate_token(email)
            verify_url = f'http://127.0.0.1:5000/verify/{token}'
            send_email(email, verify_url)

            return render_template('verify_email.html')

        except Exception as e:
            logger.error(f"Error during send verification link: {str(e)}")
            flash("Signup succeed, but failed to send verification link", "warning")
            return render_template('signup.html')

    except Exception as e:
        logger.error(f"error during signup: {str(e)}")
        flash("Internal server error.", "error")
        return redirect(url_for('index'))

# Route: Verification
@registration_login_bp.route('/verify/<token>')
def verify_email(token):
    try:
        email = confirm_token(token)

        if not email:
            return render_template('verify.html', message = 'Invalid or expired link.')

        user = User.query.filter_by(email=email).first()

        if user:
            user.is_verified = True
            db.session.commit()
        
            session['username'] = user.username
            session.permanent = True

            return redirect(url_for('topics'))

        return render_template('verify.html', message='User not found.')

    except Exception as e:
        logger.error(f"Error during verification: {str(e)}")
        flash("Verification link invalid or expired", "error")
        return redirect(url_for('registration_login_bp.signup'))

# Route: User login
@registration_login_bp.route('/login', methods=['GET', 'POST'])
@validate_login_data
def login():
    try: 
        # Check if username in session
        if 'username' in session:
            return redirect(url_for('topics'))
        
        if request.method == 'GET':
            return render_template('login.html')

        data = request.form

        username =  data.get("username")
        session["username"] = username
        
        flash("Login succesfully.", "success")
        return redirect(url_for('topics'))

    except Exception as e:
        logger.error(f"Error during user login: {str(e)}")
        flash("Internal server error.", "error")
        return redirect(url_for('index'))
        
@registration_login_bp.route('/logout', methods=['POST'])
def logout():
    session.clear('username', None)
    flash("logged out sucessfully!", "success")
    return redirect(url_for('index'))






