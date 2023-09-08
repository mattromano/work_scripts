#!/bin/zsh
### Automatically updates main branch, creates new branch, and then sets up the virtual environment + DBT profile variables 
#activate virtual env
source dbt-env/bin/activate

#git checkout main branch
git checkout main

#refresh
git pull

#setup new branch based on variable provided
git checkout -b $1

#make sure env variable is set up
export DBT_PROFILES_DIR="/Users/$USER/.dbt"

