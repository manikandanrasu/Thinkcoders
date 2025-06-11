from flask import Blueprint

topic_search_bp = Blueprint('topic_search', __name__)

from . import search