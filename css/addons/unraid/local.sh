#!/bin/bash
#
# Theme-Park Theme CSS Synchronization Script
#
# This script synchronizes the CSS files needed for the theme-park.dev Unraid theme
# into the Dynamix CSS styles folder. The script creates destination subfolders if
# they don't exist and performs rsync for each subfolder. It then updates the @import references 
# in the CSS files so the files get correctly loaded by the client.
#
# This script is intended for users of the "Theme Engine" plugin, allowing custom
# styling to be added into the HTML head that references the copied CSS files.
#
# After running this script, you can use the following code snippet as an example
# in your HTML head (Custom styling (advanced)) to include the copied CSS files using the "Theme Engine" plugin:
#
# <!-- Example for Theme Engine plugin -->
# </style>
#   <link type="text/css" rel="stylesheet" href="/webGui/styles/theme-park/css/base/unraid/nord.css"/>
#
# Tip: You can use the "User Scripts" plugin in Unraid to schedule this script to run
# automatically when the Unraid array starts.
#

# Define root source folder (CHANGE THIS TO YOUR DESIRED SOURCE FOLDER)
root_source_folder="/path/to/the/theme-park/root/folder"


# -------------------- Start of Script --------------------
# Define subfolders
subfolders=("base/unraid" "theme-options" "defaults" "community-theme-options")

# Main destination folder
main_destination_folder="/usr/local/emhttp/plugins/dynamix/styles/theme-park/css/"

# User instructions
# Instructions: Only change the 'root_source_folder' variable to point to your desired source directory.
# Do NOT modify other variables unless you understand their purpose.

# Create subfolders if they don't exist
for subfolder in "${subfolders[@]}"; do
    destination_folder="$main_destination_folder$subfolder"
    if [ ! -d "$destination_folder" ]; then
        echo "Destination folder not found. Creating destination folder: $destination_folder"
        mkdir -p "$destination_folder"
    fi
done

# Perform rsync for each subfolder to its corresponding destination
for subfolder in "${subfolders[@]}"; do
    source_folder="$root_source_folder/$subfolder"
    destination_folder="$main_destination_folder$subfolder"
    
    # Check if source folder exists
    if [ ! -d "$source_folder" ]; then
        echo "Source folder not found: $source_folder"
        exit 1
    fi
    
    rsync -av --delete "$source_folder/" "$destination_folder"
    echo "Synchronization complete for source: $source_folder to destination: $destination_folder"
done

# Update import references in CSS files so the the files get correctly loaded on the client
echo "Updating import references..."
find "$main_destination_folder" -type f -name "*.css" -exec sed -i 's|@import url("/css/|@import url("/webGui/styles/theme-park/css/|g' {} +

echo "Reference update complete."

# ---- End of Script ----

echo "All synchronizations complete."
