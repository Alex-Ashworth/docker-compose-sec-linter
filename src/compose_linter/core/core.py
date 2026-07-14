# Core logic:
import sys
from pathlib import Path
from compose_linter.termcolors import *
from compose_linter.utils import yaml, open_yaml

compose_path = Path(__file__).with_name('compose.yml')
compose_dict = open_yaml(compose_path)
service_dict = compose_dict.get('services', {})
container_name = service_dict.get('container_name', {})

def check_services_entry(compose_dict: dict):
    has_service = 'services' in compose_dict
    if not has_service:
        print(f'{error_text('ERROR:')} Compose file {compose_path} does not have services defined')
        raise InvalidComposeError

def iterate_services(service_dict: dict):
    for service_name, service_data in service_dict.items():
        if not isinstance(service_data, dict):
            continue

        yield service_name, service_data

def check_restart_policy(service_name, service_data):
    has_restart = 'restart' in service_data
    if not has_restart:
        print(f'{error_text('ERROR:')} No restart policy was found in {service_name}')




def check_service_source(service_name, service_data):
    has_image = 'image' in service_data
    has_build = 'image' in service_data
    if not has_image and not has_build:
        print(f'{error_text('ERROR:')} No image or build entry found in {service_name}')

# If service has image:
   #     optionally validate image against registry
   #        could have edge cases where docker registry is down, individial links are deprecated, etc..

   # If service has build:
   #     validate build config locally, not against registry

   # If service has neither image nor build:
   #     error/warning: service has no image source

def check_privilege(service_name, service_data):
    has_privilege = 'privileged' in service_data
    if has_privilege:
        print(f'{warning_text('WARNING:')} {service_name} is running in privileged mode')

def check_writeable(service_name, service_data):
    volumes = service_data.get('volumes', [])
    if not volumes:
        print(f'No volumes found under {service_name}')
        return
    for volume_entry in volumes:
        source, target, mode = parse_volume(volume_entry)
        if mode is None:
            options = []
        else:
            options = mode.split(',')
        # handle long read_only syntax
        print(source)
        print(target)
        print(mode)
        if 'ro' in options:
            print(f'{volume_entry} is read-only')
        else:
            print(f'{warning_text('WARNING:')} {highlight_text(service_name)} is writing data from the container\'s {info_text(source)} to the host\'s {info_text(target)}')
            # TODO: source & target

def parse_volume(volume_entry):
    sections = volume_entry.split(':')
    if len(sections) == 2:
        source, target = sections
        mode = None
    elif len(sections) == 3:
        source, target, mode = sections
    else:
        print(f'{error_text('ERROR:')} Could not parse volume: {volume_entry}')
        return None, None, None
    return source, target, mode

def run_checks(service_dict):
    for service_name, service_data in iterate_services(service_dict):
        print(f'{info_text('Scanning Service:')} {highlight_text(f'{service_name}')}')
        check_service_source(service_name, service_data)
        check_privilege(service_name, service_data)
        check_restart_policy(service_name, service_data)
        check_writeable(service_name, service_data)

def run():
    check_services_entry(compose_dict)
    run_checks(service_dict)

if __name__ == '__main__':
    run()


# Using .get() returns None when the restart key is missing instead of raising an error.
#
# TODO: check for writeable binds, check for dependencies
#
# TODO: learn what is going on with build: entries and handle them in the image check
#
# TODO: figure out how to integrate with CLI -> docker-compose-sec-linter /path/to/compose.yml
#           argparse will likely be better for learning, Click library is the alt
