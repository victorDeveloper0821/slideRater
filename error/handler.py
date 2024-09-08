# error/handlers.py

from flask import jsonify
from error.custom_error import APIError, BadRequestError, NotFoundError

def register_error_handlers(app):
    """ Register error handlers to handle exceptions globally """
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors."""
        response = jsonify({
            'error': error.message,
            'status_code': error.status_code
        })
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def handle_404_error(error):
        """Handle 404 Not Found errors."""
        return jsonify({'error': 'Resource not found', 'status_code': 404}), 404

    @app.errorhandler(400)
    def handle_400_error(error):
        """Handle 400 Bad Request errors."""
        return jsonify({'error': 'Bad request', 'status_code': 400}), 400

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Handle unexpected errors."""
        response = jsonify({
            'error': str(error),
            'status_code': 500
        })
        response.status_code = 500
        return response
