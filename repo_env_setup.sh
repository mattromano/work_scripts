#!/bin/zsh
### Sets up python virtual environment + 
source dbt-env/bin/activate

# Set the DBT_PROFILES_DIR environment variable
export DBT_PROFILES_DIR="/Users/$USER/.dbt"

echo "Virtual Env is active and profile path variable is set"