from flask import Blueprint, request, jsonify
from graph.request import get_energy_price
from graph.parser import parse_price
import os
from dotenv import load_dotenv
from datetime import datetime
from graph.graphgen import make_date_string

load_dotenv()

price_json_bp = Blueprint('price_json', __name__)

@price_json_bp.route('/price-json', methods=['GET'])
def price_json():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

   
    if not year or not month or not day:
        return jsonify({"error": "Missing year, month, or day parameters"}), 400

    try:
        
        time_interval = make_date_string(int(year), int(month), int(day))

        api_key = os.getenv('API_KEY')
        xml = get_energy_price(api_key, '10YLT-1001A0008Q', '10YLT-1001A0008Q', time_interval)
    
        prices = parse_price(xml)

        max_price = max(prices)
        min_price = min(prices)
        avg_price = round(sum(prices) / len(prices), 2)
        below_avg_hours = [i for i, price in enumerate(prices) if price < avg_price]

        ranges = []
        current_range = []
        
        for i in below_avg_hours:
            if not current_range or i == current_range[-1] + 1:
                current_range.append(i)
            else:
                ranges.append(current_range)
                current_range = [i]
        if current_range:
            ranges.append(current_range)

        below_avg_ranges = {f"range_{i+1}": r for i, r in enumerate(ranges)}

        data = {
            "max_price": max_price,
            "min_price": min_price,
            "average_price": avg_price,
            "below_average_hours": below_avg_ranges
        }

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
