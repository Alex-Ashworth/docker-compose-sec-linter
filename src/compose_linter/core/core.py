# Core logic:
import sys
from pathlib import Path
from compose_linter.utils import yaml, open_yaml

compose_path = Path(__file__).with_name("compose_.yml")
compose_dict = open_yaml(compose_path)
service_dict = compose_dict.get("services", {})

def check_services_entry(compose_dict: dict):
    has_service = "services" in compose_dict
    if not has_service:
        print(f"ERROR: Compose file {compose_path} does not have services defined")
        raise InvalidComposeError

def iterate_services(service_dict: dict):
    for service_name, service_data in service_dict.items():
        if not isinstance(service_data, dict):
            continue

        yield service_name, service_data

def check_restart_policy(service_name, service_data):
    has_restart = "restart" in service_data
    if not has_restart:
        print(f"ERROR: No restart policy was found in {service_name}")




def check_service_source(service_name, service_data):
    has_image = "image" in service_data
    has_build = "image" in service_data
    if not has_image and not has_build:
        print(f"ERROR: No image or build entry found in {service_name}")

# If service has image:
   #     optionally validate image against registry
   #        could have edge cases where docker registry is down, individial links are deprecated, etc..

   # If service has build:
   #     validate build config locally, not against registry

   # If service has neither image nor build:
   #     error/warning: service has no image source

def check_privilege(service_name, service_data):
    has_privilege = "privileged" in service_data
    if has_privilege:
        print(f"WARNING: {service_name} is running in privileged mode")

def run_checks(service_dict):
    for service_name, service_data in iterate_services(service_dict):
        check_service_source(service_name, service_data)
        check_privilege(service_name, service_data)
        check_restart_policy(service_name, service_data)

def run():
    check_services_entry(compose_dict)
    run_checks(service_dict)

if __name__ == "__main__":
    run()


# Using .get() returns None when the restart key is missing instead of raising an error.
#
# TODO: check for privileged mode
#
# TODO: learn what is going on with build: entries and handle them in the image check
#
# TODO: figure out how to integrate with CLI -> docker-compose-sec-linter /path/to/compose.yml
#           argparse will likely be better for learning, Click library is the alt
