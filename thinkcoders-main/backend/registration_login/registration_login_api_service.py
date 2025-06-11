import smtplib
from email.mime.text import MIMEText

from itsdangerous import URLSafeTimedSerializer
from backend.config import EMAIL_SECRET_KEY

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SMTP Configuration
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USERNAME="thinkcoders2025@gmail.com"
SMTP_PASSWORD="uhgomnoxhtoazvzg"

# Generate verification token
def generate_token(email):
    try:
        serializer = URLSafeTimedSerializer(EMAIL_SECRET_KEY)

        # Encode email to get the token
        token = serializer.dumps(email, salt='email-confirm')

        if not token:
            logger.error("Error during generate token")
            return None

        return token

    except Exception as e:
        logger.error(f"Error during generate token: {str(e)}")
        return None

# Token confirmation        
def confirm_token(token, expiration=1800):
    try:
        serializer = URLSafeTimedSerializer(EMAIL_SECRET_KEY)

        # Decode token to get the email
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)

        if not email:
            logger.error("Decoded token but email is empty or invalid")
            return None
        
        return email
        
    except Exception as e:
        logger.error(f"Error during token verification: {str(e)}")
        return None

# Function to send email via SMTP
def send_email(user_email, verify_url):
    try:
        # Email body
        body = f"Click to verify your email: {verify_url}"

        # Setup the MIME message
        msg = MIMEText(body)
        msg['From'] = SMTP_USERNAME
        msg['To'] = user_email
        msg['Subject'] = 'Verify your email'

        # Connect to the SMTP server and send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls() # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            
            logger.info(f"Mail send to {user_email}")

    except Exception as e:
        logger.error(f"Error during send mail: {str(e)}")
        return None