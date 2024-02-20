import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        response.raise_for_status()  # Raise HTTPError for bad requests
        json_data = response.json()  # Automatically handles JSON decoding and raises JSONDecodeError if the response is not valid JSON
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None # Return None to indicate failure
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None # Return None to indicate failure

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    
    results = []

    try:
        # Call get request with a URL parameter
        dealers = get_request(url)
        if dealers:
            # For each index in dealer object
            for i in range(len(dealers)):
                # Get contents in each index in dealers
                dealer_doc = dealers[i]["doc"]
                # Create a CarDealer object with values in 'doc' object
                dealer_obj = CarDealer(
                    address=dealer_doc["address"],
                    city=dealer_doc["city"], 
                    full_name=dealer_doc["full_name"], 
                    id=dealer_doc["id"],
                    lat=dealer_doc["lat"], 
                    long=dealer_doc["long"],
                    short_name=dealer_doc["short_name"], 
                    st=dealer_doc["st"],
                    zip=dealer_doc["zip"]
                    )
                # Append dealer_obj to 'doc'
                results.append(dealer_obj)
                
    except Exception as e:

        # Output error to console, but return nothing to indicate an error
        print(f"An error occurred: {e}")

    return results

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf_by_id(url, dealer_id=None, **kwargs):
    
    results = []

    try:
        # Call get request with a URL parameter
        dealers = get_request(url)

        if dealers:
            # For each index in dealer object
            if dealer_id is not None and 0 <= dealer_id < len(dealers):

                dealer_doc = dealers[dealer_id]["doc"]
                dealer_obj = CarDealer(
                    address=dealer_doc["address"],
                    city=dealer_doc["city"],
                    full_name=dealer_doc["full_name"],
                    id=dealer_doc["id"],
                    lat=dealer_doc["lat"],
                    long=dealer_doc["long"],
                    short_name=dealer_doc["short_name"],
                    st=dealer_doc["st"],
                    zip=dealer_doc["zip"]
                )

                # Append dealer_obj to 'doc'
                results.append(dealer_obj)
                
    except Exception as e:

        # Output error to console, but return nothing to indicate an error
        print(f"An error occurred: {e}")

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    params = {'dealerId': dealer_id}
    review_data = get_request(url, params=params)
    return []

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
