# ReviewTrackers Backend Code Challenge
## Endpoints:
### /reviews
Method: GET  
Params: url (required), page (optional)  
- Accepts a lendingtree.com business URL (e.g., https://www.lendingtree.com/reviews/business/ondeck/51886298) and optional page number.
- Returns a list of reviews for the given business and page number. Page defaults to 1 if not specified.

### To install:
```pip install -r requirements.txt```

### To run locally:
```python3 main.py```  
- Server will run on http://127.0.0.1:5000
