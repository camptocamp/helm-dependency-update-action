#!/bin/bash

# Add the "--dry-run" flag if the dry-run argument is "true"
dry_run=$( [ $1 == "true" ] && echo "--dry-run" || echo "" )

python3 /helm_dependency_bumper.py $dry_run --chart $2 --upgrade-strategy $3 --exclude-dependency $4

# Exit with error code if the Python script fails
if [ $(echo $?) ]; then
  exit 1
fi

# Return a boolean indicating whether the any dependency was upgraded
upgraded=$( [[ `git status --porcelain` ]] && echo true || echo false )
echo "chart-upgraded=$upgraded" >> $GITHUB_OUTPUT

exit 0
