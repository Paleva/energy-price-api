from flask import Flask

from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path) 

print(f"Loaded API_KEY: {os.getenv('API_KEY')}")

def register_blueprints(app):

    from api.price_api import price_bp 
    from api.gen_actual_api import generation_actual_bp
    from api.today_api import today_bp  
    from api.forecast_api import forecast_bp
    from api.forecast_actual_api import forecast_actual_bp
    from api.price_json_api import price_json_bp
    from api.forecast_json_api import forecast_json_bp
    from api.actual_gen_json_api import actual_generation_json_bp
    from api.forecast_compared_with_actual_json_api import generation_comparison_bp

    app.register_blueprint(price_bp, url_prefix='/api/v1')
    app.register_blueprint(generation_actual_bp, url_prefix='/api/v1')
    app.register_blueprint(today_bp, url_prefix='/api/v1')
    app.register_blueprint(forecast_bp, url_prefix='/api/v1')
    app.register_blueprint(forecast_actual_bp, url_prefix='/api/v1')

    app.register_blueprint(price_json_bp, url_prefix='/api/v1')
    app.register_blueprint(forecast_json_bp, url_prefix='/api/v1')
    app.register_blueprint(actual_generation_json_bp, url_prefix='/api/v1')
    app.register_blueprint(generation_comparison_bp, url_prefix='/api/v1')

def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app