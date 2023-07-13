#!/bin/bash

# Add the "--dry-run" flag if the dry-run argument is "true".
dry_run=$( [ $1 == "true" ] && echo "--dry-run" || echo "" )

# Add the "--update-readme" flag if the update-readme argument is not empty.
update_readme=$( [ $2 != "" ] && echo "--update-readme $2" || echo "" )

# Run the Python script.
python3 /helm_dependency_bumper.py $dry_run \
                                   $update_readme \
                                   --chart $3 \
                                   --upgrade-strategy $4 \
                                   --exclude-dependency $5 \
                                   --output output.txt

# Exit with error code if the Python script fails.
if [ $(echo $?) == 1 ]; then
  exit 1
fi

# Return the booleans indicating whether any dependency was upgraded or if there was a major upgrade.
echo $(cat output.txt) >> $GITHUB_OUTPUT
rm output.txt

exit 0
