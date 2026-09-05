from ipaddress import ip_address
from termcolors import (
    error_text,
    info_text,
    highlight_text,
    warning_text,
)


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
