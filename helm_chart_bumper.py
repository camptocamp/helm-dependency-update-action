"""
Simple Python script that is used in GitHub actions to
automatically bump chart dependencies using the Updatecli CLI tool.
"""

from pathlib import Path
import subprocess
import yaml
import os
import traceback

# Add charts here where it is known that higher versions are not
# yet stable or that you would like to disable automatic upgrades for
# EXCLUDED_CHARTS = os.environ.get("EXCLUDE_CHARTS")
EXCLUDED_CHARTS = []

# Inject a BUMP_MAJOR env variable if you would like the script to automatically
# bump major chart versions too. Make sure you inspect the upgrade instructions before merging!
BUMP_MAJOR = os.environ.get("BUMP_MAJOR") == "true"


def generate_updatecli_manifest(path_chart: str):
    # Open the Chart.yaml file and transform it to a Python object the script can work with.
    # TODO Consider adding a variable to define the Chart.yaml name? Or it is canonical?
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

        if dependency['name'] in EXCLUDED_CHARTS:
            print(f"Skipping {dependency['name']} because it is excluded..")
            continue

        # TODO Define here if we can implement a way to do a major, minor or patch only
        version = f"{dependency['version'].split('.')[0]}.*.*" if not BUMP_MAJOR else "*.*.*"

        manifest['sources'][f"{dependency['name']}_repository_update"] = {
            "name": f"Find latest version available in the Helm repository",
            "kind": "helmchart",
            "spec": {
                "url": dependency['repository'],
                "name": dependency['name'],
                "version": version,
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
    if dry_run:
        subprocess.check_output("updatecli diff --config manifest.yaml".split(" "))
    else:
        subprocess.check_output("updatecli apply --config manifest.yaml".split(" "))
    return


if __name__ == "__main__":

    # loop through all the charts and use updatecli
    # to bump the chart versions if a newer version exists
    paths = Path("charts")
    for path in paths.iterdir():
        try:
            generate_updatecli_manifest(str(path.absolute()))
        except Exception as e:
            print(f"Failed processing chart {path}")
            print(traceback.format_exc())
