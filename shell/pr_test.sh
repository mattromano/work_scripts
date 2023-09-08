#!/bin/zsh

### Automatically dbt runs all changed files in provided branch. Takes one argument of the PR you are looking to test ###

# Script takes one argument, which is the name of the branch
BRANCH=$1
echo "Checking out branch: $BRANCH"
# Check if virtual environment is activated
if [[ -z $VIRTUAL_ENV ]]; then
    # Activate the virtual environment
    # Assumes the venv directory is in the root of your repository
    source dbt-env/bin/activate
    

fi

export DBT_PROFILES_DIR="/Users/$USER/.dbt"

# Checkout the given branch
git checkout $BRANCH

# Pull down the latest changes
git pull origin $BRANCH

# Get list of changed .sql and .yml files
CHANGED_FILES=$(git diff --name-only main | grep -E '\.sql$|\.yml$' | tr '\n' ' '| xargs)
echo "$CHANGED_FILES"

# Iterate over changed files
for FILE in $CHANGED_FILES
do
    # Check if file is a .sql file
    if [[ $FILE == *.sql* ]]
    then
        # Run dbt on the .sql model file
        echo "dbt run --models $FILE"
        dbt run --models $FILE
    elif [[ $FILE == *.yml* ]]
    then
        # Run dbt test on the .yml test file
        echo "dbt test --models $FILE"
        dbt test --models $FILE
    fi
done
