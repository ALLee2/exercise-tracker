import requests
from datetime import datetime
import os

app_id = os.environ["APP_ID"]
api_key = os.environ["API_KEY"]
token = os.environ["TOKEN"]

nurtitionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.environ["SHEETY_ENDPOINT"]

headers = {
    "x-app-id": app_id,
    "x-app-key": api_key,
}

params = {
    "query": input("What exercise(s) did you do today? "),
    "gender": "male",
    "weight_kg": 58.15,
    "height_cm": 160,
    "age": 30,
}

nurtitionix_response = requests.post(url=nurtitionix_endpoint, headers=headers, json=params)
nurtitionix_result = nurtitionix_response.json()["exercises"]

date_now = datetime.now().strftime("%d/%m/%Y")
time_now = datetime.now().strftime("%X")

for exercise in nurtitionix_result:
    sheety_inputs = {
        "workout": {
            "date": date_now,
            "time": time_now,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # # No Auth
    # sheety_response = requests.post(url=sheety_endpoint, json=sheety_inputs)

    #Basic Auth
    # sheety_response = requests.post(
    #     sheety_endpoint,
    #     json=sheety_inputs,
    #     auth=(
    #         os.environ["USERNAME"],
    #         os.environ["PASSWORD"],
    #     )
    # )

    # Bearer Token
    bearer_headers = {
    "Authorization": f"Bearer {token}"
    }
    sheety_response = requests.post(
        sheety_endpoint,
        json=sheety_inputs,
        headers=bearer_headers
    )

    print(sheety_response.text)
