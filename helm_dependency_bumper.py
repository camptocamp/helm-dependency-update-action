"""
Simple Python script that is used in a GitHub Action to automatically bump chart dependencies using the Updatecli tool.
"""

from pathlib import Path
import argparse
import subprocess
import sys
import yaml
import traceback

PROGRAM_VERSION = "1.0.0"  # x-release-please-version
DEFAULT_UPGRADE_STRATEGY = "minor"

parser = argparse.ArgumentParser(
    prog="helm_dependency_bumper.py",
    description="Python script to upgrade the dependencies of an Helm chart.",
    add_help=False,
)
parser.add_argument('-d', '--dry-run', action='store_true',
                    help="Show which dependencies will be upgraded but do not execute the upgrade.")
parser.add_argument('-h', '--help', action='help', help="Show this help message and exit.")
parser.add_argument('-s', '--upgrade-strategy', choices=['major', 'minor', 'patch'],
                    default=f"{DEFAULT_UPGRADE_STRATEGY}", type=str,
                    help=f"Choose the Helm dependency upgrade strategy. "
                         f"\'major\' will upgrade to the absolute latest version available (i.e. *.*.*), "
                         f"\'minor\' will upgrade to the latest minor version available (i.e. X.*.*) and "
                         f"\'patch\' will upgrade to the latest patch version available (i.e. X.Y.*). "
                         f"Defaults to {DEFAULT_UPGRADE_STRATEGY}.")
parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {PROGRAM_VERSION}",
                    help="Show program's version number and exit.")
parser.add_argument('-c', '--chart', default='.', type=str, help="Path to the Helm chart. Defaults to the current "
                                                                 "directory.")
parser.add_argument('-e', '--exclude-dependency', nargs='?', default=[],
                    help="List the dependencies you want to exclude from the update script. Should be a "
                         "comma-separated list.")

args = parser.parse_args()


def generate_updatecli_manifest(path_chart: str, excluded_dependencies: list, upgrade_strategy: str):
    # Open the Chart.yaml file and transform it to a Python object the script can work with.
    with open(path_chart + "/Chart.yaml") as f:
        yaml_content = f.read()
    chart: dict = yaml.safe_load(yaml_content)

    # Create a prototype manifest object that will be converted into a YAML file in the end.
    manifest = {
        "sources": {},
        "conditions": {},
        "targets": {},
    }

    # Quit the functions if no dependencies are found in the provided
    if "dependencies" not in chart:
        return

    for i, dependency in enumerate(chart["dependencies"]):
        if dependency['name'] in excluded_dependencies:
            print(f"Skipping {dependency['name']} because it is excluded..")
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
            "name": f"Upgrade dependency on {path_chart.split('/')[-1]} chart",
            "kind": "helmchart",
            "sourceid": f"{dependency['name']}_repository_update",
            "spec": {
                "name": path_chart,
                "file": "Chart.yaml",
                "key": f"$.dependencies[{i}].version",
                "versionincrement": "none",
            },
        }

    with open("manifest.yaml", "w") as yaml_file:
        yaml.dump(manifest, yaml_file)


def run_updatecli_manifest(dry_run: bool):
    subprocess.check_output(f"updatecli {'diff' if dry_run else 'apply'} --config manifest.yaml".split(" "))
    return


if __name__ == "__main__":
    try:
        # Test if Updatecli is installed
        subprocess.check_call(['updatecli'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except OSError:
        print("\nCould not find the updatecli executable.\nPlease make sure it is installed and added to $PATH.")
        sys.exit(1)

    try:
        generate_updatecli_manifest(str(Path(args.chart).absolute()), args.exclude_dependency,
                                    args.upgrade_strategy)
    except Exception:
        print(f"Failed while processing the chart in '{args.chart}'.")
        print(traceback.format_exc())
        sys.exit(1)

    try:
        run_updatecli_manifest(args.dry_run)
    except Exception:
        print("Error when executing updatecli.")
        print(traceback.format_exc())
        sys.exit(1)
