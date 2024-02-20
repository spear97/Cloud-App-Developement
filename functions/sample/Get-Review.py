"""
This Cloud Function retrieves dealership reviews based on the provided dealerId.

Parameters:
    dealerId (str): The unique ID of the dealership to retrieve reviews for.

Output:
    - If successful, returns a JSON list of reviews for the specified dealership.
    - Error responses:
        - 400: Missing dealerId parameter
        - 404: dealerId does not exist
        - 500: Something went wrong on the server

Cloudant Database Credentials:
    - cloudant_url (str): The URL of the Cloudant database.
    - database_name (str): The name of the Cloudant database.

Note: Replace 'cloudant_url' and 'database_name' with your actual Cloudant credentials.
"""
import json
import cloudant

def get_reviews(dealer_id):
    # Cloudant database credentials
    cloudant_url = 'https://4de1e689-95a2-4931-a915-ecb3999d0311-bluemix.cloudantnosqldb.appdomain.cloud'
    database_name = 'reviews'

    # Initialize Cloudant client
    client = cloudant.Cloudant(cloudant_url, connect=True)

    try:
        # Connect to the database
        db = client[database_name]

        # Query reviews for the specified dealerId
        reviews = [doc for doc in db if 'dealerId' in doc and doc['dealerId'] == dealer_id]

        if not reviews:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'dealerId does not exist'})
            }

        return {
            'statusCode': 200,
            'body': json.dumps(reviews)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Something went wrong on the server'})
        }
    finally:
        client.disconnect()

def main(params):
    # Extract the dealerId parameter from the query string
    dealer_id = params.get('dealerId', '')

    # Check if dealerId is provided
    if not dealer_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing dealerId parameter'})
        }

    return get_reviews(dealer_id)
