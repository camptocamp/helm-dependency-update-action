#!/bin/bash

# Add the "--dry-run" flag if the dry-run argument is "true"
dry_run=$( [ $1 == "true" ] && echo "--dry-run" || echo "" )

# Run the Python script
python3 /helm_dependency_bumper.py $dry_run --chart $2 --upgrade-strategy $3 --exclude-dependency $4

# Exit with error code if the Python script fails
if [ $(echo $?) == 1 ]; then
  exit 1
fi

# Remove the manifest so it is not committed to the repository
rm manifest.yaml

exit 0
