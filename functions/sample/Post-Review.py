"""
This Cloud Function allows you to post a review for a dealership.

Language: Python
Endpoint: /api/review
Method: POST
Parameters:
    JSON of the review as follows:
    {
        "review": {
            "id": 1114,
            "name": "Upkar Lidder",
            "dealership": 15,
            "review": "Great service!",
            "purchase": false,
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021
        }
    }

Error:
500: Something went wrong on the server
"""

import json
import cloudant

def post_review(review_data):
    # Cloudant database credentials
    cloudant_url = 'https://4de1e689-95a2-4931-a915-ecb3999d0311-bluemix.cloudantnosqldb.appdomain.cloud'
    database_name = 'dealerships'  # Replace with your database name

    # Initialize Cloudant client
    client = cloudant.Cloudant(cloudant_url, connect=True)

    try:
        # Connect to the database
        db = client[database_name]

        # Insert the review data into the database
        doc = db.create_document(review_data)

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Review posted successfully', 'reviewId': doc['_id']})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Something went wrong on the server'})
        }
    finally:
        client.disconnect()

def main(params):
    try:
        # Extract the review data from the request body
        review_data = params.get('review', {})

        # Check if review data is provided
        if not review_data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing review data'})
            }

        return post_review(review_data)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Something went wrong on the server'})
        }
