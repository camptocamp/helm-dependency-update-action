#!/bin/bash

# Add the "--exclude-dependency" flag if the exclude-dependency argument is not empty.
exclude_dependency=$( [ $3 != "" ] && echo "--exclude-dependency $3" || echo "" )

# Add the "--update-readme" flag if the update-readme argument is not empty.
update_readme=$( [ $4 != "" ] && echo "--update-readme $4" || echo "" )

# Add the "--dry-run" flag if the dry-run argument is "true".
dry_run=$( [ $5 == "true" ] && echo "--dry-run" || echo "" )

# Run the Python script.
python3 /helm_dependency_bumper.py --chart $1 \
                                   --update-strategy $2 \
                                   $exclude_dependency \
                                   $dry_run \
                                   $update_readme \
                                   --output output.txt

# Exit with error code if the Python script fails.
if [ $(echo $?) == 1 ]; then
  exit 1
fi

# Return the booleans indicating whether any dependency was updated or if there was a major update.
echo $(cat output.txt) >> $GITHUB_OUTPUT
rm output.txt

exit 0
