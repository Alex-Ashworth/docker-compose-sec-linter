from termcolors import error_text


# handle if there is no colon TODO:
# define default_registry
def parse_reference(image_entry: str):
    image, separator, digest = image_entry.partition("@")
    if separator:
        return image, digest
    else:
        return image, None


def parse_image(image_entry: str):
    image, digest = parse_reference(image_entry)
    if digest is None:
        tag_section = image.split(":")
        if len(tag_section) > 1:
            image, tag = tag_section
        elif len(tag_section) == 1:
            image_section = image.split("/")
            if len(image_section) == 1:
                image = image_section
                registry = "docker.io"
                repo = "library"
                tag = "latest"
            elif len(image_section) == 2:
                repo, image = image_section
                # need to handle the multiple /
            elif len(image_section) == 3:
                print()
    # TODO: add logic to split on / if the registry is pulled, [registry/][project/]image[:tag|@digest]


def parse_port(port_section: str):
    # split port entries
    port_split_sections = port_section.split(":")
    if len(port_split_sections) == 1:
        target = port_section
        host_ip, published = None, None
    elif len(port_split_sections) == 2:
        published, target = port_split_sections
        host_ip = None
    elif len(port_split_sections) == 3:
        host_ip, published, target = port_split_sections
    else:
        print(f"{error_text('ERROR:')} Could not parse ports: {port_section}")
        return None, None, None
    return host_ip, published, target


def parse_protocol(port_entry: str):
    # split ports and protocols
    port_section, separator, protocol = port_entry.partition("/")
    protocol = protocol if separator else "tcp"
    return port_section, protocol


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
