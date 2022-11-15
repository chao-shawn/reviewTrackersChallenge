import json
import pytest

from server import create_app


@pytest.fixture(scope="class")
def app():
    app = create_app()
    return app


class TestServer:
    SERVER_URL = "http://127.0.0.1:5000"

    def test_url_not_found(self, app):
        url = f"{self.SERVER_URL}/invalidURL"
        response = app.test_client().get(url)
        body = response.text
        expected_response = {
            "error": "URL not found.",
        }

        assert response.status_code == 404
        assert json.loads(body) == expected_response

    @pytest.mark.parametrize("method", ["POST", "PUT", "DELETE"])
    def test_method_not_allowed(self, app, method):
        url = f"{self.SERVER_URL}/reviews"

        if method == "POST":
            response = app.test_client().post(url)
        elif method == "PUT":
            response = app.test_client().put(url)
        elif method == "DELETE":
            response = app.test_client().delete(url)
        body = response.text
        expected_response = {
            "error": "Method not allowed. Allowed methods: [GET]",
        }

        assert response.status_code == 405
        assert json.loads(body) == expected_response

    def test_invalid_business_url(self, app):
        business_url = "http://invalid-sample-url.com"
        url = f"{self.SERVER_URL}/reviews?url={business_url}"
        response = app.test_client().get(url)
        body = response.text
        expected_response = {
            "error": f"Invalid business URL: {business_url}",
        }

        assert response.status_code == 400
        assert json.loads(body) == expected_response

    def test_valid_response(self, app):
        business_url = "https://www.lendingtree.com/reviews/business/fundbox-inc/111943337"
        url = f"{self.SERVER_URL}/reviews?url={business_url}"
        response = app.test_client().get(url)

        assert response.status_code == 200
