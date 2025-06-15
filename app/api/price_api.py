from flask import Blueprint, request, jsonify
from graph.graphgen import graphgen_price
import os
from dotenv import load_dotenv
from .paths import FULL_PATH

load_dotenv()

price_bp = Blueprint('price', __name__)

API_KEY = os.getenv('API_KEY')

@price_bp.route('/price', methods=['GET'])
def price():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    if not year or not month or not day:
        return jsonify({"error": "Missing year, month, or day parameters"}), 400

    try:
        filename = graphgen_price(int(year), int(month), int(day))
        return open(f'{FULL_PATH}{filename}', 'rb').read()
    except ValueError: 
        return jsonify({"error": "Invalid date format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
