# Productivity and Automation Scripts for Work

## addalias.sh
- Scipt which automatically adds bash scripts to you machines aliases. This will make it so your bash script is now executable as a command which you can execute without giving the entire path to script everytime. ###
- Takes one argument which is the path to the script. It will automatically name the alias based on the script name

## all_dif_files.sh
- Prints out files paths for all changed files in current branch from main branch

## newbranch.sh
- Automatically updates main branch, creates new branch, and then sets up the virtual environment + DBT profile variables

## pr_test.sh
- Automatically dbt runs all changed files in provided branch. Takes one argument of the PR you are looking to test

## repo_env_setup.sh
- Sets up python virtual environment + dbt profile path

## repo_env_setup_all.sh
- Less helpful after initial mac is set up, but script automtically will pull and set up all Flipside repos provided in the list on line 33
- Check if the script is called with an argument

## scrap_script.sh
- This script will do a regex search of any provided folder path (and all folders in that path). It will export any found addresses into a TSV document with 6 total columns:
    - One with the line of code where the address was found, the address itself, the line number where the address was found, the filepath, the project, and a result of simple table search. Labels can be added and removed on line 20
    - TODO: Consolidate labels to only have one for each blockchain - ie ETH is not eth or ethereum but just ethereum.
