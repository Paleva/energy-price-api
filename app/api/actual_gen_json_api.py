from flask import Blueprint, request, jsonify
from graph.request import get_energy_generation
from graph.parser import parse_generation_actual
from api.api_utils import group_hours
import os
from dotenv import load_dotenv
from graph.graphgen import make_date_string

load_dotenv()

actual_generation_json_bp = Blueprint('actual_generation_json', __name__)

@actual_generation_json_bp.route('/actual-generation-json', methods=['GET'])
def actual_generation_json():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    if not year or not month or not day:
        return jsonify({"error": "Missing year, month, or day parameters"}), 400

    try:
        time_interval = make_date_string(int(year), int(month), int(day))
        api_key = os.getenv('API_KEY')
        
        wind_xml = get_energy_generation(api_key, '10YLT-1001A0008Q', time_interval)
        solar_xml = get_energy_generation(api_key, '10YLT-1001A0008Q', time_interval)
        
        wind = parse_generation_actual(wind_xml, 'B19')
        solar = parse_generation_actual(solar_xml, 'B16')  
        
        max_wind = max(wind) if wind else None
        min_wind = min(wind) if wind else None
        max_solar = max(solar) if solar else None
        
        avg_wind = round(sum(wind) / len(wind), 2) if wind else None
        avg_solar = round(sum(solar) / len(solar), 2) if solar else None
        
        above_avg_wind_hours = [i for i, value in enumerate(wind) if value > avg_wind] if avg_wind else []
        above_avg_solar_hours = [i for i, value in enumerate(solar) if value > avg_solar] if avg_solar else []
        
        data = {
            "max_wind_generation": max_wind,
            "min_wind_generation": min_wind,
            "max_solar_generation": max_solar,
            "average_wind_generation": avg_wind,
            "average_solar_generation": avg_solar,
            "above_average_wind_generation_hours": group_hours(above_avg_wind_hours),
            "above_average_solar_generation_hours": group_hours(above_avg_solar_hours)
        }

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
