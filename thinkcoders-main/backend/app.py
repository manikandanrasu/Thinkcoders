import os
from datetime import timedelta

from flask import Flask, render_template
from flask_session import Session
from flask_migrate import Migrate

from backend.models import db, User
from backend.registration_login import registration_login_bp
from backend.topic_search import topic_search_bp

from backend.config import SESSION_SECRET_KEY

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.secret_key = SESSION_SECRET_KEY

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session config to use database
app.config['SESSION_TYPE']  = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_SQLALCHEMY_TABLE'] = 'session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=90)

# Initialize db, session, migrate
db.init_app(app)
Session(app)
migrate = Migrate(app, db)

app.register_blueprint(registration_login_bp)
app.register_blueprint(topic_search_bp)

# Index route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topics')
def topics():
    return render_template('topics.html')

if __name__ == '__main__':
    app.run(debug=True)