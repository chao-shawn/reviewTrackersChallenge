from flask import Flask, jsonify, make_response, request
from datetime import datetime

from classes.reviewFetcher import ReviewFetcher


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        time = datetime.now()
        return f"Hello World! The time is now {time}."

    @app.route('/reviews', methods=['GET'])
    def get_reviews():
        url = request.args.get("url")
        page = request.args.get("page", default=1)
        if check_url(url):
            review_fetcher = ReviewFetcher()
            result, status_code = review_fetcher.get_reviews(url, page)
        else:
            result = {
                "error": f"Invalid business URL: {url}",
            }
            status_code = 400
        return make_response(jsonify(result), status_code)

    @app.errorhandler(404)
    def url_not_found(e):
        result = {
            "error": "URL not found.",
        }
        return make_response(jsonify(result), 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        result = {
            "error": "Method not allowed. Allowed methods: [GET]",
        }
        return make_response(jsonify(result), 405)

    def check_url(url):
        BASE_URL = "https://www.lendingtree.com/reviews/business"
        return url.startswith(BASE_URL)

    return app
