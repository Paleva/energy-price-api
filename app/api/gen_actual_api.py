from flask import Blueprint, request, jsonify
from graph.graphgen import graphgen_gen_actual
import os
from dotenv import load_dotenv
from .paths import FULL_PATH

load_dotenv()

generation_actual_bp = Blueprint('generation_actual', __name__)

API_KEY = os.getenv('API_KEY')

@generation_actual_bp.route('/generation-actual', methods=['GET'])
def generation_actual():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    if not year or not month or not day:
        return jsonify({"error": "Missing year, month, or day parameters"}), 400

    try:
        filename = graphgen_gen_actual(int(year), int(month), int(day))
        return open(f'{FULL_PATH}{filename}', 'rb').read() 
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
