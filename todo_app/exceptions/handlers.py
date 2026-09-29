from flask import jsonify
from exceptions.exceptions import AppException

def register_error_handlers(app):

    @app.errorhandler(AppException)
    def handle_app_exception(e):
        return jsonify({"error": e.message}), e.status_code

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(405)
    def handle_405(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Internal server error"}), 500
