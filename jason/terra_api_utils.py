# Importing the API and instantiating the client using your keys
from terra.base_client import Terra
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
DEV_ID = os.getenv("DEV_ID")
SECRET = "<Your Signing secret>"

terra = Terra(API_KEY, DEV_ID, SECRET)

def get_user(user_id: str):
    return terra.from_user_id(user_id)

def get_daily_data(user_id: str):
    terra_user = get_user(user_id)
    daily_data_json = terra_user.get_daily(start_date=datetime.strptime('2023-09-01','%Y-%m-%d'), end_date=datetime.strptime('2023-09-02','%Y-%m-%d'), to_webhook = False, with_samples=False)
    return daily_data_json

def get_df_data(daily_resp_json):
    avg_heart_rate = []
    act_seconds = []
    act_calories = []
    avg_stress = []
    for day in daily_resp_json["data"]:
        ahr = day["heart_rate_data"]["summary"]["avg_hr_bpm"]
        act_secs = day["active_durations_data"]["activity_seconds"]
        act_cals = day["calories_data"]["net_activity_calories"]
        avg_strs = day["stress_data"]["avg_stress_level"]
        avg_heart_rate.append(ahr)
        act_seconds.append(act_secs)
        act_calories.append(act_cals)
        avg_stress.append(avg_strs)
    df = pd.DataFrame({
        "avg_heart_rate": avg_heart_rate,
        "act_seconds": act_seconds,
        "act_calories": act_calories,
        "avg_stress": avg_stress,
    })
    return df

def extract_relevant_features():
    # Specify the file name and path
    file_path = "/Users/jasonzhang/Documents/PersonalProjects/HackMIT2023/jason/output.json"

    # Read the JSON file and parse it into a dictionary
    with open(file_path, "r") as file:
        data = json.load(file)
        main_df = pd.read_csv("/Users/jasonzhang/Documents/PersonalProjects/HackMIT2023/jason/tracker_data.csv")

        # Add each partition's data to the main dataframe
        for partition in data:
            df = get_df_data(partition)
            main_df = pd.concat([main_df, df], axis=0)
        
        clean_df = main_df.dropna().reset_index(drop=True)
        clean_df.to_csv("tracker_data.csv", index=False)
