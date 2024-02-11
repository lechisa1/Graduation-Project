# app/__init__.py
from flask import Flask
from app.routes.tokenization_routes import tokenization_routes
from app.routes.home_routes import index_app
from app.routes.error_detection_routes import error_detection_routes
from app.routes.error_correction_routes import error_correction_routes
from app.routes.morphological_generator_routes import morphological_generator_routes
from app.routes.suggestion_routes import suggestion_ranking_routes
from app.routes.ignored_word_routes import ignored_word_routes
from app.routes.custom_dictionary_routes import custom_dictionary_routes
def create_app():
    app = Flask(__name__, static_url_path='/static')

    app.register_blueprint(tokenization_routes, url_prefix='/')
    app.register_blueprint(index_app, url_prefix='/')
    app.register_blueprint(error_detection_routes, url_prefix='/')
    app.register_blueprint(error_correction_routes,url_prefix='/')
    app.register_blueprint(morphological_generator_routes,url_prefix='/')
    app.register_blueprint(suggestion_ranking_routes,url_prefix='/')
    app.register_blueprint(ignored_word_routes,url_prefix='/')
    app.register_blueprint(custom_dictionary_routes,url_prefix='/')

    return app
