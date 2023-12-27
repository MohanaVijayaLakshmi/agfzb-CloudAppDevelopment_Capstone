import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer
import logging

logger = logging.getLogger(__name__)

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):  
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    response = None
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    if response is not None:
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    else:
        print("Error: No response")
        return None

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    # json_result = get_request(url)
    response = requests.get(url)

    if response.status_code == 200:
    # if json_result:
        # Get the row list in JSON as dealers
        # dealers = json_result
        try:
            # dealers = json.loads(json_result)
            dealers = response.json()
            # For each dealer object
            for dealer in dealers:
                logger.info(type(dealer))
                # Get its content in `doc` object
                dealer_doc = dealer
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(id=dealer_doc["id"],
                                    city=dealer_doc["city"],
                                    # state=dealer_doc["state"],
                                    st=dealer_doc["st"],
                                    address=dealer_doc["address"],
                                    zip=dealer_doc["zip"],
                                    lat=dealer_doc["lat"],
                                    long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    full_name=dealer_doc["full_name"])
                results.append(dealer_obj)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



