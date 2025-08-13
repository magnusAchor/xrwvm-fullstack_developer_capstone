# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = "https://kutiyoung-8000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/"
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# def get_request(endpoint, **kwargs):
# Add code for get requests to back end

# def analyze_review_sentiments(text):
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments

# def post_review(data_dict):
# Add code for posting review
