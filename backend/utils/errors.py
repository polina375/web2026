from backend.utils.exception import ApiException
from flask import jsonify

def error_response(status_code, message,details=None):
    error ={
        "code": status_code,
        "message": message,
    }
    if details is not None:
        error["details"] = details
    return jsonify({
        "error": error
    }),status_code

def register_error_handlers(app):
    @app.errorhandler(ApiException)
    def handle_api_error(error):
        return error_response(error.status_code, error.message, error. details)

    @app.errorhandler(404)
    def page_not_found (error):
        return error_response(404, "endpoints не найдены" )
    @app.errorhandler(405)
    def method_not_allowed (error):
        return error_response(405, "метод не разрешен")
    @app.errorhandler(500)
    def internal_error (error):
        return error_response(500, "ошибка сервера")
