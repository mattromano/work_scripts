echo "Loop execution is skipped, just setting up pythong venv"
    # Create and activate the virtual environment
    python -m venv dbt-env
    source dbt-env/bin/activate

    # Install dbt-snowflake
    pip install dbt-snowflake==1.7.0

    # Install dbt dependencies
    dbt deps

    # Upgrade dbt-snowflake
    pip install --upgrade dbt-snowflake==1.7.0

    # Set the DBT_PROFILES_DIR environment variable
    export DBT_PROFILES_DIR="/Users/$USER/.dbt"

    # Upgrade Pip
    python -m pip install --upgrade pip

    # Test dbt connections
    dbt debug

    # Return to the main dir
    cd ..
