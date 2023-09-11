
target="$1"
current_dir=$(pwd)
# Check if the target starts with the current directory
if [[ "$target" == "$current_dir"* ]]; then
    echo "${target#$current_dir/}"
else
    echo "$target"
fi
