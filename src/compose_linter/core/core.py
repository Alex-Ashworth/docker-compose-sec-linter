# Core logic:
import sys
from pathlib import Path
from compose_linter.utils import yaml, open_yaml

compose_path = Path(__file__).with_name("compose.yml")
compose_dict = open_yaml(compose_path)
services_dict = compose_dict.get("services", {})

def check_services_entry(compose_dict: dict):
    if "services" not in compose_dict:
        print("ERROR: No services detected")
        # have this check what IS in the file and suggest/correct
        # raise an error here? - prob so
        # can't think of how to continue without services as a basis, couldn't be 100% certain that im accessing the correct data
    else:
        return


def get_service_names(services_dict: dict):
    service_names = []
    for service_name, service_data in services_dict.items():
        service_names.append(service_name)
    
    return service_names

def check_restart_policy(services_dict: dict):
    for service_name, service_data in services_dict.items():
        if isinstance(service_data, dict):
            restart_policy = service_data.get("restart")
            # Do something with the data
            yaml.dump(restart_policy, sys.stdout)
            print(type(restart_policy))
        else:
            restart_policy = None
            yaml.dump(restart_policy, sys.stdout)
            
        if restart_policy is None:
            print(f"ERROR: No restart policy detected for", service_name)



def check_image_entry(services_dict) -> bool:
    service_names = get_service_names(services_dict)
    for names in service_names:
        service_data = services_dict[names]
        images = service_data.get("image", {})
        if not images:
            print(f"ERROR: No image is defined for", names)
        else:
            return True
   # If service has image:
   #     optionally validate image against registry
   #        could have edge cases where docker registry is down, individial links are deprecated, etc..

   # If service has build:
   #     validate build config locally, not against registry

   # If service has neither image nor build:
   #     error/warning: service has no image source

def run():
    check_image_entry(services_dict)

if __name__ == "__main__":
    run()


# Using .get() returns None when the restart key is missing instead of raising an error.
#
# TODO: check if services: exists, 
