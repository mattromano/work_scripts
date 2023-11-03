import re
import snowflake.connector
import os
import snowflake_details as sfd
from datetime import datetime

# Define a regular expression pattern to extract information from the log file
pattern = r"(\d+:\d+:\d+\.\d+) \[.*\]: (\d+) of \d+ (PASS|FAIL) (.*?) \[.* in (\d+\.\d+s|\d+\.\d+m)]"

# Open the log file for reading
log_file_path = "logs/dbt.log"
with open(log_file_path, "r") as log_file:
    log_data = log_file.read()

# Find and extract information from the log using the regular expression
matches = re.findall(pattern, log_data)

# Create a Snowflake connection
conn = snowflake.connector.connect(
    user=sfd.snowflake_user,
    password=sfd.snowflake_password,
    account=sfd.snowflake_account,
    warehouse=sfd.snowflake_warehouse,
    database=sfd.snowflake_database,
    schema=sfd.snowflake_schema
)

# Create a cursor for executing SQL statements
cur = conn.cursor()

# Define the Snowflake table to insert the data
table_name = "bsc_dev.test_silver.test_log"

# Insert the extracted log data into the Snowflake table (no need to create or replace the table)
insert_data_sql = f"INSERT INTO {table_name} (date, time, test_number, test_name, test_result, time_taken_seconds) VALUES (%s, %s, %s, %s, %s, %s)"

for match in matches:
    time, test_number, test_result, test_name, time_taken = match
    # Convert time taken to seconds if it's in minutes
    if time_taken.endswith("m"):
        time_taken = float(time_taken.rstrip("m")) * 60
    else:
        time_taken = float(time_taken.rstrip("s"))

    # Get the current date in UTC
    current_date_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    cur.execute(insert_data_sql, (current_date_utc, time, int(test_number), test_name, test_result, time_taken))

# Commit the changes
conn.commit()

# Close the cursor and the connection
cur.close()
conn.close()

print(f"Data has been appended to the '{table_name}' Snowflake table.")

# CREATE OR REPLACE TABLE bsc_dev.test_silver.test_log (
#     date TIMESTAMP,
#     time TIME,
#     test_number INTEGER,
#     test_name STRING,
#     test_result STRING,
#     time_taken_seconds DECIMAL(10, 2)
# );