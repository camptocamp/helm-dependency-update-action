"""
Simple Python script that is used in a GitHub Action to automatically bump chart dependencies using the Updatecli tool.
"""

from pathlib import Path
import argparse
import fileinput
import os
import subprocess
import sys
import traceback
import yaml

PROGRAM_VERSION = "0.2.1"  # x-release-please-version
DEFAULT_UPGRADE_STRATEGY = "minor"

parser = argparse.ArgumentParser(
    prog="python3 helm_dependency_bumper.py",
    description="Python script to upgrade the dependencies of an Helm chart.",
    add_help=False,
)
parser.add_argument('-h', '--help', action='help', help="Show this help message and exit.")
parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {PROGRAM_VERSION}",
                    help="Show program's version number and exit.")
parser.add_argument('-c', '--chart', default='.', type=str,
                    help="Path to the Helm chart. Defaults to the current directory.")
parser.add_argument('-e', '--exclude-dependency', nargs='?', default=[],
                    help="List the dependencies you want to exclude from the update script. Should be a "
                         "comma-separated list.")
parser.add_argument('-u', '--upgrade-strategy', choices=['major', 'minor', 'patch'],
                    default=f"{DEFAULT_UPGRADE_STRATEGY}", type=str,
                    help=f"Choose the Helm dependency upgrade strategy. "
                         f"\'major\' will upgrade to the absolute latest version available (i.e. *.*.*), "
                         f"\'minor\' will upgrade to the latest minor version available (i.e. X.*.*) and "
                         f"\'patch\' will upgrade to the latest patch version available (i.e. X.Y.*). "
                         f"Defaults to {DEFAULT_UPGRADE_STRATEGY}.")
parser.add_argument('-r', '--update-readme', type=str,
                    help="Update the AsciiDoc attributes with the chart versions on a given *.adoc file. Does not "
                         "have any effect if running in dry-run mode.")
parser.add_argument('-o', '--output', type=str,
                    help="Create a file to output if there was a major upgrade or an upgrade at all. Does not have "
                         "any effect if running in dry-run mode.")
parser.add_argument('-s', '--save-manifest', action='store_true',
                    help="Save the generated manifest.yaml instead of deleting it automatically.")
parser.add_argument('-d', '--dry-run', action='store_true',
                    help="Run updatecli in dry-run mode.")

args = parser.parse_args()


def read_chart_yaml(path: str) -> dict:
    # Open the Chart.yaml file and transform it to a Python object the script can work with.
    with open(path + "/Chart.yaml") as f:
        yaml_content = f.read()
    chart: dict = yaml.safe_load(yaml_content)

    return chart


def generate_updatecli_manifest(chart: dict, path: str, excluded_dependencies: list, upgrade_strategy: str):
    # Create a prototype manifest object that will be converted into a YAML file in the end.
    manifest = {
        "sources": {},
        "conditions": {},
        "targets": {},
    }

    # If no dependencies are found in the provided chart generate an empty manifest.yaml and quit the function
    if "dependencies" not in chart:
        with open("manifest.yaml", "w") as manifest_yaml_file:
            yaml.dump(manifest, manifest_yaml_file)
        return

    for i, dependency in enumerate(chart['dependencies']):
        if dependency['name'] in excluded_dependencies:
            continue

        parse_versions = {
            "major": "*.*.*",
            "minor": f"{dependency['version'].split('.')[0]}.*.*",
            "patch": f"{dependency['version'].split('.')[0]}.{dependency['version'].split('.')[1]}.*",
        }
        version = parse_versions[f"{upgrade_strategy}"]

        manifest['sources'][f"{dependency['name']}_repository_update"] = {
            "name": f"Find latest version available in the Helm repository",
            "kind": "helmchart",
            "spec": {
                "url": dependency['repository'],
                "name": dependency['name'],
                "versionfilter": {
                    "kind": "semver",
                    "pattern": version,
                    "strict": True
                }
            }
        }

        manifest['targets'][f"{dependency['name']}_dependency_bump"] = {
            "name": f"Upgrade dependency on {chart['name']} chart",
            "kind": "helmchart",
            "sourceid": f"{dependency['name']}_repository_update",
            "spec": {
                "name": path,
                "file": "Chart.yaml",
                "key": f"$.dependencies[{i}].version",
                "versionincrement": "none",  # Do not increase the version of the mother chart itself
            },
        }

    with open("manifest.yaml", "w") as manifest_yaml_file:
        yaml.dump(manifest, manifest_yaml_file)


def sort_dependencies(old_chart_dict: dict, new_chart_dict: dict):
    # Sort dependencies on both objects to be sure that we are comparing the versions of the same dependencies.
    # Inspiration: https://stackoverflow.com/questions/72899/how-to-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary-in-python
    old_chart_dict['dependencies'].sort(key=lambda k: k['name'])
    new_chart_dict['dependencies'].sort(key=lambda k: k['name'])


def is_updated(old_chart_dict: dict, new_chart_dict: dict) -> bool:
    sort_dependencies(old_chart_dict, new_chart_dict)

    if len(old_chart_dict['dependencies']) != len(new_chart_dict['dependencies']):
        raise ValueError("Not the same number of dependencies on both charts.")

    # Compare the versions of each dependency, starting from the smallest to biggest.
    for i in range(len(old_chart_dict['dependencies'])):
        if old_chart_dict['dependencies'][i]['version'].split('.')[2] < \
                new_chart_dict['dependencies'][i]['version'].split('.')[2]:
            return True
        elif old_chart_dict['dependencies'][i]['version'].split('.')[1] < \
                new_chart_dict['dependencies'][i]['version'].split('.')[1]:
            return True
        elif old_chart_dict['dependencies'][i]['version'].split('.')[0] < \
                new_chart_dict['dependencies'][i]['version'].split('.')[0]:
            return True
        else:
            continue

    # Return false in the case that none of the dependencies had an update.
    return False


def is_major(old_chart_dict: dict, new_chart_dict: dict) -> bool:
    sort_dependencies(old_chart_dict, new_chart_dict)

    if len(old_chart_dict['dependencies']) != len(new_chart_dict['dependencies']):
        raise ValueError("Not the same number of dependencies on both charts.")

    # Compare the versions of each dependency.
    for i in range(len(old_chart_dict['dependencies'])):
        if old_chart_dict['dependencies'][i]['version'].split('.')[0] < \
                new_chart_dict['dependencies'][i]['version'].split('.')[0]:
            return True
        else:
            continue

    # Return false in the case that none of the dependencies had a major upgrade.
    return False


def read_versions(chart: dict) -> dict:
    deps_versions = {}
    for i, dependency in enumerate(chart['dependencies']):
        deps_versions.update({f"{dependency['name']}": f"{dependency['version']}"})
    return deps_versions


# FIXME Probably there is a more performance optimised way of doing this instead of nested for loops with a check on
#  each one.
def update_asciidoc_attributes(path: str, versions_dict: dict):
    for x in versions_dict:
        for line in fileinput.input(path, inplace=True):
            if line.contains(f":{x}-chart-version:"):
                print(f":{x}-chart-version: {versions_dict[x]}")


def error_exit(message: str, enable_traceback=False):
    print(message)
    if enable_traceback:
        print(traceback.format_exc())
    sys.exit(1)


if __name__ == "__main__":
    # Test if Updatecli is installed.
    try:
        subprocess.check_call(['updatecli'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except OSError:
        print("\nCould not find the updatecli executable.\nPlease make sure it is installed and added to $PATH.")
        sys.exit(1)

    chart_path = str(Path(args.chart).absolute())

    # Parse the contents of the Chart.yaml to upgrade.
    try:
        old_chart = read_chart_yaml(chart_path)
    except Exception:
        print(f"Failed to parse the Chart.yaml in '{args.chart}' before the upgrade.")
        print(traceback.format_exc())
        sys.exit(1)

    # Generate the manifest.yaml.
    try:
        generate_updatecli_manifest(old_chart, chart_path, args.exclude_dependency, args.upgrade_strategy)
    except Exception:
        print("Unable to generate the manifest.yaml")
        print(traceback.format_exc())
        sys.exit(1)

    # Run the Updatecli binary and perform the chart upgrade.
    try:
        subprocess.check_output(f"updatecli {'diff' if args.dry_run else 'apply'} --config manifest.yaml".split(" "))
        if not args.save_manifest and os.path.exists("manifest.yaml"):
            os.remove("manifest.yaml")
    except Exception:
        if os.path.exists("manifest.yaml"):
            os.remove("manifest.yaml")
        print("Error when executing updatecli.")
        print(traceback.format_exc())
        sys.exit(1)

    # Parse the contents of the upgraded Chart.yaml.
    try:
        new_chart = read_chart_yaml(chart_path)
    except Exception:
        print(f"Failed to parse the Chart.yaml in '{args.chart}' after the upgrade.")
        print(traceback.format_exc())
        sys.exit(1)

    is_major_bool = is_major(old_chart, new_chart)
    is_updated_bool = is_updated(old_chart, new_chart)

    # Create the file containing the outputs if demanded by the user. Does not run
    if not args.dry_run and args.output:
        output_path = str(Path(args.output).absolute())
        try:
            with open(output_path, "w") as output_file:
                output_file.write(f"is-major={'true' if is_major_bool else 'false'}\n")
                output_file.write(f"is-updated={'true' if is_updated_bool else 'false'}\n")
        except Exception:
            print(f"Failed to create file with the outputs.")
            print(traceback.format_exc())
            sys.exit(1)

    # Update a *.adoc if a path is given
    if not args.dry_run and args.update_readme and is_updated_bool:
        readme_path = str(Path(args.update_readme).absolute())
        versions = read_versions(new_chart)
        try:
            update_asciidoc_attributes(readme_path, versions)
        except FileNotFoundError:
            print(f"Could not find the *.adoc file in '{args.update_readme}'.")
            sys.exit(1)
        except Exception:
            error_exit(f"Failed to write versions to the *.adoc in '{args.update_readme}'.")
            print(traceback.format_exc())
            sys.exit(1)
