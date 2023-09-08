#!/bin/bash

### This script will do a regex search of any provided folder path (and all folders in that path). It will export any found addresses into a TSV document with 6 total columns: 
    ## One with the line of code where the address was found, the address itself, the line number where the address was found, the filepath, the project, and a result of simple table search. Labels can be added and removed on line 20
    ## TODO: Consolidate labels to only have one for each blockchain - ie ETH is not eth or ethereum but just ethereum.
# Check if the provided path is valid
if [ ! -d "$1" ]; then
    echo "Usage: $0 path_to_repository"
    exit 1
fi

repository_path="$1"
output_dir=$(dirname "$repository_path")
output_file_base=$(basename "$repository_path")
output_file="${output_dir}/${output_file_base}_address_extract.tsv"

# Output tab-delimited header
echo -e "Line Content\tLine Number\tFile Path\tProject\tExtracted Address\tLabel" > "$output_file"

# List of labels
labels="bsc|ethereum|optimism|op|arbitrum|polygon|poly|eth|avax|base|gnosis"

# Use find to recursively search through files in the directory and only process text files to avoid the encoding issue
find "$repository_path" -type f -exec file --mime-type {} \; | grep text | cut -d: -f1 | while read file; do
    # Use awk to search for the pattern in each file, extract the project name, address, and label
    awk -v labels="$labels" '
    /0[xX][0-9a-fA-F]+/ {
        # Remove tabs
        gsub(/\t/, " ", $0)

        # Extract the matched address
        matched_address = ""
        if (match($0, /0[xX][0-9a-fA-F]+/)) {
            matched_address = substr($0, RSTART, RLENGTH)
        }

        # Search for labels (case-insensitive)
        label_found = ""
        split(labels, arr, "|")
        for (i in arr) {
            if (index(tolower($0), tolower(arr[i])) != 0) {
                label_found = arr[i]
                break
            }
        }

        # Extract the project name
        split(FILENAME, parts, "/")
        project = parts[length(parts)-1]
        
        # Print to TSV
        print $0 "\t" NR "\t" FILENAME "\t" project "\t" matched_address "\t" label_found >> "'"$output_file"'"
        
        # Print the found message
        printf "Found address in %s on line %d\n", FILENAME, NR
    }
    ' "$file"
done

# Count the rows in the generated TSV, excluding the header
total_addresses=$(( $(wc -l < "$output_file") - 1 ))

# Display the total number of addresses found
echo "Total addresses found: $total_addresses"
