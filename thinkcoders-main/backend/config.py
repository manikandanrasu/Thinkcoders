import os
from dotenv import load_dotenv
load_dotenv()

# Secret key for flask session
SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY')

# Secret key for email verfication token
EMAIL_SECRET_KEY = os.getenv('EMAIL_SECRET_KEY')