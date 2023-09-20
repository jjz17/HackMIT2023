from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from terra.base_client import Terra
from jason.terra_api_utils import get_daily_data, extract_relevant_features
from pydantic import BaseModel
import typing
import json
import os
from dotenv import load_dotenv
from datetime import datetime



class Item(BaseModel):
    data: typing.List[dict]
    type: str
    user: dict

class SimpleJson(BaseModel):
    body: dict


app = FastAPI()

def file_exists(filename):
    return os.path.exists(filename) and os.path.isfile(filename)


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Web hook endpoint to receive large quantities of time series health tracker data
@app.post("/web")
async def root(item: Item):
    print("Hi")

    file_path = "/Users/jasonzhang/Documents/PersonalProjects/HackMIT2023/jason/output.json"

    if file_exists(file_path):
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # Append the new data to the existing list
    existing_data.append(dict(item))

    # Write the updated data back to the JSON file
    with open(file_path, "w") as file:
        json.dump(existing_data, file)

    # Process loaded data
    # extract_relevant_features()

    # Calculate anomolies with bocd and generate report


    return 200 # Success!!

@app.get("/get_anomaly_report")
def get_anomaly_report(user_id, start_date="2023-08-01", end_date="2023-09-10"):
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    DEV_ID = os.getenv("DEV_ID")
    SECRET = "<Your Signing secret>"

    terra = Terra(API_KEY, DEV_ID, SECRET)
    terra_user = terra.from_user_id(user_id)

    start_date_obj = datetime.strptime(start_date,'%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date,'%Y-%m-%d')
    diff = end_date_obj - start_date_obj
    num_days = diff.days + 1
    data = {"message": f"Hello user {user_id}",
            "need_to_process_json": False,
            "num_days": num_days}

    # # Pull data if not exists
    if not file_exists('/Users/jasonzhang/Documents/PersonalProjects/HackMIT2023/jason/tracker_data.csv'):
        # This block sends the webhook request for data
        daily_resp = terra_user.get_daily(start_date=start_date_obj, end_date=end_date_obj, to_webhook = False, with_samples=False )
        daily_resp_json = daily_resp.get_json()
        data["message"] += ", we're loading your data from the API now!"
        data["need_to_process_json"] = False
    else:
        data["message"] += ", here's your cached data!"

    # Process data and send it over
    return JSONResponse(content=data)

@app.get("/get_data")
def get_data(param: str = Query(..., description="Example query parameter")):
    data = {"message": f"Hello, this is your JSON data with parameter: {param}"}
    return JSONResponse(content=data)

@app.get("/daily/{user_id}")
def daily_data(user_id):
    return get_daily_data(user_id)
