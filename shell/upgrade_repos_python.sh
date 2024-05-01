#!/bin/zsh

# Get the current directory
main_dir=$(pwd)

# Loop through all directories that contain 'models' in the name
for dir in *models*/; do
  if [[ -d "$dir" ]]; then
    echo "Entering $dir"
    cd "$dir"

    # Remove the existing dbt-env virtual environment if it exists
    if [[ -d "dbt-env" ]]; then
      echo "Removing existing dbt-env in $dir"
      rm -rf dbt-env
    fi

    # Create a new dbt-env virtual environment with Python 3.10
    echo "Creating new dbt-env with Python 3.10 in $dir"
    python3.10 -m venv dbt-env


    # Move back to the main directory
    cd "$main_dir"
  fi
done

echo "All model directories processed."
