#!/bin/bash
### Scipt which automatically adds bash scripts to you machines aliases. This will make it so your bash script is now executable as a command which you can execute without giving the entire path to script everytime. ###
### Takes one argument which is the path to the script. It will automatically name the alias based on the script name. ###
# Validate input
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /path/to/your/script.sh"
    exit 1
fi

# Validate if the provided file is a regular file
if [ ! -f "$1" ]; then
    echo "Error: '$1' is not a regular file."
    exit 1
fi

# Set the destination directory
dest_dir="/Users/mattromano/Desktop/scripts"

# Ensure the directory exists
if [ ! -d "$dest_dir" ]; then
    mkdir -p "$dest_dir"
fi

# Copy the script to the destination directory
script_name=$(basename "$1")
cp "$1" "$dest_dir/$script_name"
alias_name="${script_name/.sh/}"
# Add it as a source alias in .zshrc
echo "alias $alias_name='source $dest_dir/$script_name'" >> ~/.zshrc
echo "Script added to $dest_dir and alias added in .zshrc as $alias_name"
source ~/.zshrc
