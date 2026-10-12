from flask import Flask, jsonify

from backend.routes.requests import requests_bp
from backend.utils.errors import register_error_handlers


app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"]="*"
    response.headers["Access-Control-Allow-Headers"]="Content-Type"
    response.headers["Access-Control-Allow-Methods"]=(
        "GET, POST, PATCH, DELETE, QUERY, OPTIONS"
    )
    return response

app.register_blueprint(requests_bp)
register_error_handlers(app)

@app.route("/")
def hello():
    return jsonify({
        "message": "Student Dormitory API is running"
    })

if __name__ == "__main__":
    app.run()