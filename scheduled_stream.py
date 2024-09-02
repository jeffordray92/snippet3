import functions_framework
import os
import requests
import json

def main(*args, **kwargs):
    # Load the base URL from environment variables
    base_url = os.environ.get('API_BASE_URL', 'http://localhost:3001')

    # Define the API endpoints
    fetch_shop_list_endpoint = f"{base_url}/api/fetch-shop-list"
    fetch_data_endpoint = f"{base_url}/api/fetch-data"

    response_data = []

    try:
        # Make a request to the fetch-shop-list API
        response = requests.get(fetch_shop_list_endpoint)

        # Check if the response status code is 200 (OK)
        if response.status_code != 200:
            print(f"Error fetching shop list: {response.status_code} - {response.text}")
            return

        # Parse the JSON response
        shop_data = response.json()

        # Iterate over each shop and make a request to the fetch-data API
        for shop in shop_data:
            shop_id = shop['shopID']
            models = [stream['model'] for stream in shop['planStreams']]
            
            # Prepare the payload for the fetch-data API
            payload = {
                "models": models,
                "shopID": shop_id
            }

            # Make a POST request to the fetch-data API
            fetch_data_response = requests.post(fetch_data_endpoint, json=payload)

            # Check if the response status code is 200 (OK)
            if fetch_data_response.status_code != 200:
                response_data.append({
                    "status": "failed",
                    "shopID": f"{shop_id}",
                    "data": fetch_data_response.text
                })
                print(f"Error fetching data for shopID {shop_id}: {fetch_data_response.status_code} - {fetch_data_response.text}")
                continue

            # Parse and print the response from the fetch-data API
            data_result = fetch_data_response.json()

            print(f"Data for shopID {shop_id}: {data_result}")
            response_data.append({
                "status": "success",
                "shopID": f"{shop_id}",
                "data": data_result
            })

        return_json = {
            "status": "success",
            "message": response_data
        }

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return_json = {
            "status": "error",
            "message": f"ERROR: {e}"
        }

    print(json.dumps(return_json, indent=4))

if __name__ == "__main__":
    main()
