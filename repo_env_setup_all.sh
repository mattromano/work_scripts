#!/bin/zsh

# Check if the script is called with an argument
if [[ $# -eq 1 && "$1" == "false" ]]; then
  echo "Loop execution is skipped, just setting up pythong venv"
        # Create and activate the virtual environment
      python -m venv dbt-env
      source dbt-env/bin/activate

      # Install dbt-snowflake
      pip install dbt-snowflake==1.4.0

      # Install dbt dependencies
      dbt deps

      # Upgrade dbt-snowflake
      pip install --upgrade dbt-snowflake==1.4.0

      # Set the DBT_PROFILES_DIR environment variable
      export DBT_PROFILES_DIR="/Users/$user_name/.dbt"

      # Upgrade Pip
      python -m pip install --upgrade pip

      # Test dbt connections
      dbt debug

      # Return to the main dir
      cd ..

else
  repo_list=("ethereum" "polygon" "bsc" "arbitrum" "base" "optimism" "gnosis" "crosschain" "avalanche")

  # Set the user variable
  user_name=$USER

  for i in "${repo_list[@]}"; do
      #cloning repo
      git clone "git@github.com:FlipsideCrypto/$i-models.git"

      #moving into repo
      cd "$i-models"
      # Create and activate the virtual environment
      python -m venv dbt-env
      source dbt-env/bin/activate

      # Install dbt-snowflake
      pip install dbt-snowflake==1.4.0

      # Install dbt dependencies
      dbt deps

      # Upgrade dbt-snowflake
      pip install --upgrade dbt-snowflake==1.4.0

      # Set the DBT_PROFILES_DIR environment variable
      export DBT_PROFILES_DIR="/Users/$user_name/.dbt"

      # Upgrade Pip
      python -m pip install --upgrade pip

      # Test dbt connections
      dbt debug

      # Return to the main dir
      cd ..
  done
fi