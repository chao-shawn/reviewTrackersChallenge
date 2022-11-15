from bs4 import BeautifulSoup
from unittest import TestCase
from unittest.mock import MagicMock, patch

import sample_expected_result
from classes.reviewFetcher import ReviewFetcher


class TestReviewFetcher(TestCase):
    @patch("classes.reviewFetcher.BeautifulSoup")
    @patch("classes.reviewFetcher.requests")
    def test_valid_reviews(self, mock_requests, mock_soup):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response

        with open("sample.html") as html_file:
            mock_soup.return_value = BeautifulSoup(html_file)

        expected_result = sample_expected_result.expected_result
        self.assertEqual(ReviewFetcher.get_reviews("test_url"), (expected_result, 200))

    @patch("classes.reviewFetcher.BeautifulSoup")
    @patch("classes.reviewFetcher.requests")
    def test_reviews_not_found(self, mock_requests, mock_soup):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response

        with open("sample_no_reviews.html") as html_file:
            mock_soup.return_value = BeautifulSoup(html_file)

        expected_result = {
            "error": "No reviews found.",
        }
        self.assertEqual(ReviewFetcher.get_reviews("test_url"), (expected_result, 400))

    @patch("classes.reviewFetcher.requests")
    def test_404_not_found(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests.get.return_value = mock_response

        expected_result = {
            "error": "Page not found.",
        }
        self.assertEqual(ReviewFetcher.get_reviews("test_url"), (expected_result, 404))

    @patch("classes.reviewFetcher.requests")
    def test_other_error(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_requests.get.return_value = mock_response

        expected_result = {
            "error": "Unknown error.",
        }
        self.assertEqual(ReviewFetcher.get_reviews("test_url"), (expected_result, 503))

