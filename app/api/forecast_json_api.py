from flask import Blueprint, request, jsonify
from graph.request import get_wind_solar_forecast
from graph.parser import parse_generation_forecast
from api.api_utils import group_hours
import os
from dotenv import load_dotenv
from graph.graphgen import make_date_string

load_dotenv()

forecast_json_bp = Blueprint('forecast_json', __name__)

@forecast_json_bp.route('/forecast-json', methods=['GET'])
def forecast_json():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    if not year or not month or not day:
        return jsonify({"error": "Missing year, month, or day parameters"}), 400

    try:
        time_interval = make_date_string(int(year), int(month), int(day))
        api_key = os.getenv('API_KEY')
        
        wind_xml = get_wind_solar_forecast(api_key, '10YLT-1001A0008Q', time_interval, 'B19')
        solar_xml = get_wind_solar_forecast(api_key, '10YLT-1001A0008Q', time_interval, 'B16')
        
        wind = parse_generation_forecast(wind_xml)
        solar = parse_generation_forecast(solar_xml)
        
        avg_wind = sum(wind) / len(wind)
        avg_solar = sum(solar) / len(solar)
        
        above_avg_wind_hours = [i for i, value in enumerate(wind) if value > avg_wind]
        above_avg_solar_hours = [i for i, value in enumerate(solar) if value > avg_solar]
        
        data = {
            "max_wind": max(wind),
            "min_wind": min(wind),
            "max_solar": max(solar),
            "average_wind": avg_wind,
            "average_solar": avg_solar,
            "above_average_wind_hours": group_hours(above_avg_wind_hours),
            "above_average_solar_hours": group_hours(above_avg_solar_hours)
        }

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500