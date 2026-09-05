# Core logic:
import requests
from pathlib import Path
from ipaddress import ip_address
from compose_linter.termcolors import (
    error_text,
    info_text,
    highlight_text,
    warning_text,
)
from compose_linter.utils import open_yaml

compose_path = Path(__file__).with_name("compose.yml")
compose_dict = open_yaml(compose_path)
service_dict = compose_dict.get("services", {})
container_name = service_dict.get("container_name", {})


def check_services_entry(compose_dict: dict):
    # check if services are defined
    has_service = "services" in compose_dict
    if not has_service:
        print(
            f"{error_text('ERROR:')} Compose file {compose_path} does not have services defined"
        )
        raise InvalidComposeError


def iterate_services(service_dict: dict):
    # helper to iterate over services
    for service_name, service_data in service_dict.items():
        if not isinstance(service_data, dict):
            continue

        yield service_name, service_data


def check_restart_policy(service_name: str, service_data: dict):
    # check if restart policy is defined and enabled
    has_restart = "restart" in service_data
    if not has_restart:
        print(f"{error_text('ERROR:')} No restart policy was found in {service_name}")
    restart_policy = service_data.get("restart", [])
    if "no" in restart_policy:
        print(
            f"{warning_text('WARNING:')} Restart policy is set to never restart for {service_name}"
        )
    else:
        return

    # add logic for defined, but disabled policy


def check_service_source(service_name: str, service_data: dict):
    # check if image/build is valid
    has_image = "image" in service_data
    has_build = "build" in service_data
    if not has_image and not has_build:
        print(f"{error_text('ERROR:')} No image or build entry found in {service_name}")
    elif has_image:
        verify_image()
        # FIXME: define this with type hints


def verify_image(registry: str, foo: str, image: str):
    print()


def parse_image(image_entry: str):
    image_section = image_entry.split(":")

    # TODO: add logic to split on / if the registry is pulled


# If service has image:
#     optionally validate image against registry
#        could have edge cases where docker registry is down, individial links are deprecated, etc..

# If service has build:
#     validate build config locally, not against registry

# If service has neither image nor build:
#     error/warning: service has no image source


def check_privilege(service_name: str, service_data: dict):
    # check if container is running in priveleged mode
    has_privilege = "privileged" in service_data
    if has_privilege:
        print(
            f"{warning_text('WARNING:')} {service_name} is running in privileged mode"
        )


def check_writeable(service_name: str, service_data: dict):
    # check if volumes are writable to the host
    volumes = service_data.get("volumes", [])
    if not volumes:
        print(f"No volumes found under {service_name}")
        return
    for volume_entry in volumes:
        source, target, mode = parse_volume(volume_entry)
        if mode is None:
            options = []
        else:
            options = mode.split(",")
        if "ro" in options:
            print(f"{volume_entry} is read-only")
        else:
            print(
                f"{warning_text('WARNING:')} {highlight_text(service_name)} is writing data from the host's {info_text(source)} to the container's {info_text(target)}"
            )


def parse_volume(volume_entry: str):
    # split volume entries
    volume_sections = volume_entry.split(":")
    if len(volume_sections) == 2:
        source, target = volume_sections
        mode = None
    elif len(volume_sections) == 3:
        source, target, mode = volume_sections
    else:
        print(f"{error_text('ERROR:')} Could not parse volume: {volume_entry}")
        return None, None, None
    return source, target, mode


def network_check():
    print(f"{info_text('Scanning network..')}")


# TODO: public ip detection, printing and error_text
def check_ports(service_name: str, service_data: dict):
    # check for publicly exposed ports
    ports = service_data.get("ports", [])
    if not ports:
        print(f"No port entries found under {service_name}")
        return
    for port_entry in ports:
        port_section, protocol = parse_protocol(port_entry)
        host_ip, published, target = parse_port(port_section)
        if not host_ip or host_ip == "0.0.0.0" or host_ip == "::":
            print(
                f"{warning_text('WARNING:')} {highlight_text(service_name)} does not have an IP address defined. This container could be exposed externally"
            )
        else:
            host_ip_address = ip_address(host_ip)
            if host_ip_address.is_global:
                print(
                    f"{warning_text('WARNING:')} {info_text(service_name)}:{highlight_text(port_section)} {warning_text('has a publicly exposed IP address! Proceed with caution!')}"
                )
            else:
                print(
                    f"{info_text(service_name)}:{highlight_text(port_section)} has no publicly exposed ports"
                )


def parse_port(port_section: str):
    # split port entries
    split_sections = port_section.split(":")
    if len(split_sections) == 1:
        target = port_section
        host_ip, published = None, None
    elif len(split_sections) == 2:
        published, target = split_sections
        host_ip = None
    elif len(split_sections) == 3:
        host_ip, published, target = split_sections
    else:
        print(f"{error_text('ERROR:')} Could not parse ports: {port_section}")
        return None, None, None
    return host_ip, published, target


def parse_protocol(port_entry: str):
    # split ports and protocols
    port_section, separator, protocol = port_entry.partition("/")
    protocol = protocol if separator else "tcp"
    return port_section, protocol


def run_checks(service_dict: dict):
    for service_name, service_data in iterate_services(service_dict):
        print(f"{info_text('Scanning Service:')} {highlight_text(f'{service_name}')}")
        check_service_source(service_name, service_data)
        check_privilege(service_name, service_data)
        check_restart_policy(service_name, service_data)
        check_writeable(service_name, service_data)
        check_ports(service_name, service_data)


def run():
    check_services_entry(compose_dict)
    run_checks(service_dict)


if __name__ == "__main__":
    run()

# service_name = str
# service_data = dict
# service_dict = dict
# volume_entry = str
# source, target, mode = str
# options = list

# Using .get() returns None when the restart key is missing instead of raising an error.
#
# TODO: check for publicly exposded ports, check for dependencies
#
# TODO: learn what is going on with build: entries and handle them in the image check
#
# TODO: figure out how to integrate with CLI -> docker-compose-sec-linter /path/to/compose.yml
#           argparse will likely be better for learning, Click library is the alt
#
# Decided not to handle long syntax
#
# TODO: Move Compose loading out of module scope so run() receives a file path and parsed document instead of always scanning the bundled fixture.
#
# TODO: Add an argparse CLI that accepts a file or directory, discovers compose.yml, compose.yaml, docker-compose.yml, and docker-compose.yaml, and returns documented exit codes.
#
# TODO: Handle missing, unreadable, empty, malformed, and non-mapping YAML files with concise errors instead of tracebacks.
#
# TODO: Declare termcolor and ruamel.yaml as package dependencies and support color-free output for redirected or editor-driven runs.
#
# TODO: Collect structured findings with a rule ID, severity, service, message, file, and source location before rendering human-readable output.
#
# TODO: Add a root-user rule that distinguishes explicit root values such as user: root or user: 0 from an omitted user whose image default is unknown.
#
# TODO: Fix the privileged-mode rule so it reports only privileged: true and supports valid Compose value types.
#
# TODO: Add a host-network rule for services using network_mode: host.
#
# TODO: Finish public-port detection for short syntax, treating omitted host IPs and wildcard addresses as public while allowing loopback bindings.
#
# TODO: Strengthen restart-policy checks for missing policies and explicitly disabled values without assuming every parsed value is a string.
#
# TODO: Detect likely hardcoded secrets in mapping and list forms of environment, ignore variable references, and never include secret values in findings.
#
# TODO: Add a healthcheck rule for missing checks and explicitly disabled healthchecks.
#
# TODO: Extend writable-mount checks to distinguish bind mounts from named volumes and support both short and long Compose syntax.
#
# TODO: Flag image references that use latest or omit a tag or digest while correctly handling registry host ports.
#
# TODO: Warn when a service joins more networks than a configurable threshold, with a documented default.
#
# TODO: Add focused fixtures and tests for every rule, valid Compose syntax variants, malformed input, CLI exit codes, and false-positive cases.
#
# TODO: Add stable JSON output so editor integrations can consume findings without parsing colored terminal text.
#
# TODO: Build a VS Code extension that runs the CLI and displays findings as diagnostics on the relevant Compose lines.
#
# TODO: Build a Neovim integration that maps the same JSON findings into native diagnostics.
#
