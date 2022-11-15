import re
import requests
from bs4 import BeautifulSoup


class ReviewFetcher:
    @staticmethod
    def get_reviews(url, page=1):
        url = f"{url}?sort=&pid={page}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            reviews_not_found = soup.find_all(string="No Review Found")
            if reviews_not_found:
                result = {
                    "error": "No reviews found.",
                }
                return (result, 400)

            reviews = []
            review_details = soup.find_all("div", class_="reviewDetail")
            ratings = soup.find_all("div", class_="numRec")
            pagination_raw = (soup.find_all("ul", class_="pagination"))[1].text
            pagination = re.findall("\d of \d", pagination_raw)[0].split()
            current_page = int(pagination[0])
            total_pages = int(pagination[2])

            for i in range(len(review_details)):
                current = review_details[i]
                title = current.find("p", class_="reviewTitle").text
                content = current.find("p", class_="reviewText").text
                author_raw = current.find("p", class_="consumerName").text.strip().split()
                author = " ".join(author_raw)
                date_raw = current.find("p", class_="consumerReviewDate").text.split()
                date = " ".join(date_raw[2:])
                rating_raw = ratings[i].text
                rating = re.findall("[1-5]", rating_raw)[0]
                review = {
                    "title": title,
                    "author": author,
                    "date": date,
                    "rating": rating,
                    "content": content,
                }
                reviews.append(review)

            result = {
                "reviews": reviews,
                "page": current_page,
                "total_pages": total_pages,
            }
        elif response.status_code == 404:
            result = {
                "error": "Page not found.",
            }
        else:
            result = {
                "error": "Unknown error.",
            }
        return (result, response.status_code)


