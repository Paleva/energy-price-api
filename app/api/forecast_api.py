from flask import Blueprint, request, jsonify
from graph.graphgen import graphgen_gen_forecast
from dotenv import load_dotenv
from os import getenv
from .paths import FULL_PATH


load_dotenv()

forecast_bp = Blueprint('forecast', __name__)


API_KEY = getenv('API_KEY')

@forecast_bp.route('/forecast', methods=['GET'])
def forecast():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    if not year or not month or not day:
        return jsonify({"error": "Missing year, month, or day parameters"}), 400

    try:
        filename = graphgen_gen_forecast(int(year), int(month), int(day))
        return open(f'{FULL_PATH}{filename}', 'rb').read()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
