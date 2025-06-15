from flask import Blueprint, request, jsonify
from graph.request import get_wind_solar_forecast, get_energy_generation
from graph.parser import parse_generation_forecast, parse_generation_actual
import os
from dotenv import load_dotenv
from graph.graphgen import make_date_string

load_dotenv()

generation_comparison_bp = Blueprint('generation_comparison', __name__)

@generation_comparison_bp.route('/generation-comparison', methods=['GET'])
def generation_comparison():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    if not year or not month or not day:
        return jsonify({"error": "Missing year, month, or day parameters"}), 400

    try:
        time_interval = make_date_string(int(year), int(month), int(day))
        api_key = os.getenv('API_KEY')

        forecast_wind_xml = get_wind_solar_forecast(api_key, '10YLT-1001A0008Q', time_interval, 'B19')
        forecast_solar_xml = get_wind_solar_forecast(api_key, '10YLT-1001A0008Q', time_interval, 'B16')
        actual_wind_xml = get_energy_generation(api_key, '10YLT-1001A0008Q', time_interval)
        actual_solar_xml = get_energy_generation(api_key, '10YLT-1001A0008Q', time_interval)

        forecast_wind = parse_generation_forecast(forecast_wind_xml)
        forecast_solar = parse_generation_forecast(forecast_solar_xml)
        actual_wind = parse_generation_actual(actual_wind_xml, 'B19')
        actual_solar = parse_generation_actual(actual_solar_xml, 'B16')

        avg_forecast_wind = sum(forecast_wind) / len(forecast_wind) if len(forecast_wind) > 0 else 0
        avg_forecast_solar = sum(forecast_solar) / len(forecast_solar) if len(forecast_solar) > 0 else 0
        avg_actual_wind = sum(actual_wind) / len(actual_wind) if len(actual_wind) > 0 else 0
        avg_actual_solar = sum(actual_solar) / len(actual_solar) if len(actual_solar) > 0 else 0

        def calculate_error_percentage(actual, forecast):
            return (actual - forecast) / forecast * 100 if forecast != 0 else None

        wind_error_percentage = calculate_error_percentage(avg_actual_wind, avg_forecast_wind)
        solar_error_percentage = calculate_error_percentage(avg_actual_solar, avg_forecast_solar)

        def determine_status(error_percentage):
            if error_percentage is None:
                return "not as expected"  # Handle division by zero case
            elif error_percentage > 20:
                return "better than expected"
            elif -20 <= error_percentage <= 20:
                return "as expected"
            else:
                return "not as expected"

        wind_status = determine_status(wind_error_percentage)
        solar_status = determine_status(solar_error_percentage)

        data = {
            "forecast": {
                "average_wind": round(avg_forecast_wind, 2),
                "average_solar": round(avg_forecast_solar, 2)
            },
            "actual": {
                "average_wind": round(avg_actual_wind, 2),
                "average_solar": round(avg_actual_solar, 2)
            },
            "error_percentage": {
                "wind": round(wind_error_percentage, 2) if wind_error_percentage is not None else None,
                "solar": round(solar_error_percentage, 2) if solar_error_percentage is not None else None
            },
            "status": {
                "wind": wind_status,
                "solar": solar_status
            }
        }

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
