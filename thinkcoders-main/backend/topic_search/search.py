from flask import request, render_template, jsonify

from . import topic_search_bp
from backend.ai_gen_module.cohere_integration import generate_q

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@topic_search_bp.route('/topics', methods=['GET'])
def main():
    return render_template('topics.html')

# Route: Serve the MCQ page
@topic_search_bp.route('/topics/<topic>', methods=['GET'])
def serve_mcq_page(topic):
    return render_template('mcq.html', topic=topic)

# Route: Generate a new question dynamically
@topic_search_bp.route('/api/get-question/<topic>', methods=['GET'])
def get_question_api(topic):
    try:
        question, options, answer = generate_q(topic)

        return jsonify({
            "question": question,
            "options": options,
            "answer": answer
        })

    except Exception as e:
        logger.error(f"Error during generating question for '{topic}': {str(e)}")
        return jsonify({"error":"Internal server error"}), 500