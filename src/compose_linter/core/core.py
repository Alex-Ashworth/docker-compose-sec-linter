# Core logic:
import sys
from pathlib import Path
from compose_linter.utils import yaml, open_yaml

compose_path = Path(__file__).with_name("compose_.yml")
compose_data = open_yaml(compose_path)
services = compose_data.get("services", {})

# def check_services():
#    if compose_data.get("services")


def get_service_names(services):
    service_names = []
    for service_name, service_data in services.items():
        service_names.append(service_name)
    
    return service_names

def check_restart_policy(services):
    for service_name, service_data in services.items():
        if isinstance(service_data, dict):
            restart_policy = service_data.get("restart")
            yaml.dump(restart_policy, sys.stdout)
            print(type(restart_policy))
        else:
            restart_policy = None
            yaml.dump(restart_policy, sys.stdout)
            
        if restart_policy is None:
            print(f"ERROR: No restart policy detected for", service_name)

        

def run():
    get_service_names(services)
    check_restart_policy(services)
    boog = services.keys()
    print(boog)
# scan_file()

if __name__ == "__main__":
    run()


# Using .get() returns None when the restart key is missing instead of raising an error.
