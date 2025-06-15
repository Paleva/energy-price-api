from flask import Blueprint, jsonify
from graph.graphgen import graphgen_price, graphgen_gen_actual, graphgen_gen_forecast, graphgen_actual_forecast_wind, graphgen_actual_forecast_solar
import datetime as DT
from .paths import FULL_PATH


today_bp = Blueprint('today', __name__)

@today_bp.route('/today-price', methods=['GET'])
def today_price():
    try:
        today = DT.datetime.today()
        filename = graphgen_price(today.year, today.month, today.day)
        return open(f'{FULL_PATH}{filename}', 'rb').read()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@today_bp.route('/today-actual', methods=['GET'])
def today_actual():
    try:
        today = DT.datetime.today()
        filename = graphgen_gen_actual(today.year, today.month, today.day)
        return open(f'{FULL_PATH}{filename}', 'rb').read()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@today_bp.route('/today-forecast', methods=['GET'])
def today_forecast():
    try:
        today = DT.datetime.today()
        filename = graphgen_gen_forecast(today.year, today.month, today.day)
        return open(f'{FULL_PATH}{filename}', 'rb').read()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@today_bp.route('/today-forecast-actual-wind', methods=['GET'])
def today_forecast_actual_wind():
    try:
        today = DT.datetime.today()
        filename = graphgen_actual_forecast_wind(today.year, today.month, today.day)
        return open(f'{FULL_PATH}{filename}', 'rb').read()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@today_bp.route('/today-forecast-actual-solar', methods=['GET'])
def today_forecast_actual_solar():
    try:
        today = DT.datetime.today()
        filename = graphgen_actual_forecast_solar(today.year, today.month, today.day)
        return open(f'{FULL_PATH}{filename}', 'rb').read()
    except Exception as e:
        return jsonify({"error": str(e)}), 500