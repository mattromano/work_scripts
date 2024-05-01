import re
import csv
import os

# Define a regular expression pattern to extract information from the log file
pattern = r"(\d+:\d+:\d+\.\d+) \[.*\]: (\d+) of \d+ (PASS|FAIL) (.*?) \[.* in (\d+\.\d+s|\d+\.\d+m)]"

def split_test_name(test_name):
    # Known schema names
    schema_names = [
        'TEST_SILVER',
        'AAVE',
        'BEACON_CHAIN',
        'BETA',
        'BRONZE',
        'BRONZE_API',
        'BRONZE_HEVO',
        'BRONZE_PUBLIC',
        'CHAINLINK',
        'COMPOUND',
        'CORE',
        'DEFI',
        'ENS',
        'ETHEREUM_SHARE',
        'GITHUB_ACTIONS',
        'GITHUB_UTILS',
        'HOUR_GAPS_SILVER',
        'LIVE',
        'MAKER',
        'NFT',
        'PRICE',
        'PUBLIC',
        'SILVER',
        'SILVER_BRIDGE',
        'SILVER_DEX',
        'SILVER_ENS',
        'SILVER_LSD',
        'SILVER_MAKER',
        'SILVER_NFT',
        'SILVER_OBSERVABILITY',
        'STREAMLINE',
        'SYNTHETIX',
        'TEST_SILVER',
        'UNISWAPV3',
        'UTILS',
        '_DATASHARE',
        '_LIVE',
        '_UTILS'

    ]
    schema_names= [s.lower() for s in schema_names]
    # Initialize default return structure
    split_result = {
        "test_name": None,
        "schema": None,
        "table": None,
        "columns": None
    }
    
    # Try to find the schema in the test_name
    schema_found = False
    for schema in schema_names:
        schema_pattern = r"_(%s)__" % schema
        match = re.search(schema_pattern, test_name)
        if match:
            schema_found = True
            # Split the string before and after the schema pattern
            pre_schema = test_name[:match.start()]
            post_schema = test_name[match.end()-1:]  # Include the underscore after the schema name
            split_result['test_name'] = pre_schema.rstrip("_")
            split_result['schema'] = schema
            
            # Further split by "__" to separate table and columns, considering the table is lower case
            table_columns_pattern = r"([a-z0-9_]+)_([A-Z0-9_]+)"
            tc_match = re.search(table_columns_pattern, post_schema)
            if tc_match:
                split_result['table'] = tc_match.group(1)
                split_result['columns'] = tc_match.group(2)
            break
    if not schema_found:
        # Handle the case where no schema is found
        # You'll need to decide how to handle this situation
        print(f"No known schema found in {test_name}")
    
    return split_result

# Define the log folder and CSV file paths
log_folder_path = "logs"  # Folder containing log files
csv_file_path = "test_results.csv"

# Initialize a flag to check if the CSV file already exists
csv_file_exists = os.path.isfile(csv_file_path)

# Open the CSV file for appending
with open(csv_file_path, "a", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write the header row only if the CSV file is being created for the first time
    if not csv_file_exists:
        csvwriter.writerow(["Time", "Test Number", "Test Result", "Test Name", "Schema", "Table", "Columns", "Time Taken (seconds)"])

    total_row_count = 0  # Initialize a counter for the total rows across all files

    # Iterate over each file in the log folder
    for file in os.listdir(log_folder_path):
        # Optional: Check if the file is a log file
        if file.endswith(".log") or file.endswith(".log.2") or file.endswith(".log.3") or file.endswith(".log.4") or file.endswith(".log.5"):
            log_file_path = os.path.join(log_folder_path, file)

            # Open the log file for reading
            with open(log_file_path, "r") as log_file:
                log_data = log_file.read()

            # Find and extract information from the log using the regular expression
            matches = re.findall(pattern, log_data)

            row_count = 0  # Initialize a counter for the rows in the current file

    for match in matches:

        time, test_number, test_result, test_name, time_taken = match

        # Convert time taken to seconds if it's in minutes
        if "m" in time_taken:
            minutes, seconds = time_taken.split("m")
            time_taken = float(minutes) * 60 + float(seconds.rstrip("s"))
        else:
            time_taken = float(time_taken.rstrip("s"))

        # Split the test_name into components
        split_components = split_test_name(test_name)
        table_clean = split_components['table']
        

        # Write the extracted information to the CSV file
        csvwriter.writerow([
            time,
            test_number,
            test_result,
            split_components["test_name"],
            split_components["schema"],
            split_components["table"],
            split_components["columns"],
            time_taken
        ])
        row_count += 1  # Increment the row count

print(f"{row_count} rows of data have been appended to '{csv_file_path}'.")