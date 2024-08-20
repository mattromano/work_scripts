import requests
import pandas as pd
from datetime import datetime, timezone

# Convert target start date to timestamp
target_start_date = int(datetime(2023, 3, 8, 0, 0).replace(tzinfo=timezone.utc).timestamp())

# API setup
url = "https://archive.prod.vertexprotocol.com/v1"
headers = {
    "Content-Type": "application/json",
}

# Initialize an empty dataframe to append all data
all_data_df = pd.DataFrame()

# Initialize max_time to the current time for the first request
max_time = int(datetime.now().timestamp())

# Loop until you reach the target start date
while max_time > target_start_date:
    # Convert max_time to a native int type before using it in the request body
    if max_time is not None:
        max_time = int(max_time)  # Ensures max_time is JSON serializable
    
    # Prepare the request body, adjusting max_time dynamically
    body = {
        "market_snapshots": {
            "interval": {
                "count": 100,  # Number of intervals to fetch
                "granularity": 3600,  # Interval granularity in seconds (1 hour)
                "max_time": max_time,  # Use current time for the first request
            },
            "product_ids": [2]  # Pass a list of product IDs here
        }
    }
    print(max_time)
    
    # Make the request
    response = requests.post(url, json=body, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Convert the response to JSON
        json_data = response.json()
        
        # Convert to DataFrame and normalize 'snapshots' part of the JSON
        if 'snapshots' in json_data and json_data['snapshots']:
            df = pd.json_normalize(json_data['snapshots'])

            # Convert Unix timestamp to datetime and create a new column for it
            df['datetime_timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

            # Append the new dataframe to the aggregated dataframe
            all_data_df = pd.concat([all_data_df, df], ignore_index=True)

            if 'timestamp' in df.columns and not df.empty:
                # Update max_time using the minimum 'timestamp' value in the dataframe
                max_time = df['timestamp'].min() - 1  # Subtract 1 to ensure we don't fetch the last record again
                
                # Break the loop if we have fetched data older than the target_start_date
                if max_time < target_start_date:
                    break
            else:
                print("No 'timestamp' column found or dataframe is empty. Exiting loop.")
                break
        else:
            print("No 'snapshots' data found or JSON response is empty. Exiting loop.")
            break
    else:
        print(f"Request failed with status code {response.status_code}. Exiting loop.")
        break

# Ensure the dataframe has the 'timestamp' column before trying to convert it
if 'timestamp' in all_data_df.columns:
    all_data_df['timestamp_dt'] = pd.to_datetime(all_data_df['timestamp'], unit='s')

# Save the data to a CSV file
all_data_df.to_csv('vertex_export.csv', index=False)