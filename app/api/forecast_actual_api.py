from flask import Blueprint, request, jsonify
from graph.graphgen import graphgen_actual_forecast_solar, graphgen_actual_forecast_wind
from .paths import FULL_PATH

forecast_actual_bp = Blueprint('forecast_actual', __name__)


@forecast_actual_bp.route('/forecast-actual-wind', methods=['GET'])
def forecast_actual_wind():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    if not year or not month or not day:
        return jsonify({"error": "Missing year, month, or day parameters"}), 400

    try:    
        filename = graphgen_actual_forecast_wind(int(year), int(month), int(day))
        return open(f'{FULL_PATH}{filename}', 'rb').read()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@forecast_actual_bp.route('/forecast-actual-solar', methods=['GET'])
def forecast_actual_solar():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    if not year or not month or not day:
        return jsonify({"error": "Missing year, month, or day parameters"}), 400

    try:
        filename = graphgen_actual_forecast_solar(int(year), int(month), int(day))
        return open(f'{FULL_PATH}{filename}', 'rb').read()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500