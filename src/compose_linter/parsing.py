from compose_linter.termcolors import error_text


def parse_reference(image_entry: str):
    image, separator, digest = image_entry.partition("@")
    if separator:
        return image, digest
    else:
        return image, None


def parse_image(image_entry: str):
    image, digest = parse_reference(image_entry)
    tag = None
    registry = "docker.io"
    repo = None

    if not image or len(image_entry.split()) != 1 or image_entry != image_entry.strip():
        print(f"{error_text('ERROR:')} Could not parse image: {image_entry}")
        return None, None, None, None, None

    if digest is not None:
        algorithm, separator, value = digest.partition(":")
        if not algorithm or not separator or not value or "@" in digest or ":" in value:
            print(f"{error_text('ERROR:')} Could not parse image: {image_entry}")
            return None, None, None, None, None

    image_sections = image.split("/")
    image = image_sections[-1]
    if ":" in image:
        image, tag = image.rsplit(":", 1)
        if not tag or ":" in image:
            print(f"{error_text('ERROR:')} Could not parse image: {image_entry}")
            return None, None, None, None, None
    image_sections[-1] = image

    for section in image_sections:
        if not section:
            print(f"{error_text('ERROR:')} Could not parse image: {image_entry}")
            return None, None, None, None, None

    if len(image_sections) > 1:
        first_section = image_sections[0]
        if "." in first_section or ":" in first_section or first_section == "localhost":
            registry = first_section
            image_sections = image_sections[1:]

    for section in image_sections[:-1]:
        if ":" in section:
            print(f"{error_text('ERROR:')} Could not parse image: {image_entry}")
            return None, None, None, None, None

    if len(image_sections) > 1:
        repo = "/".join(image_sections[:-1])
    elif registry == "docker.io":
        repo = "library"

    if tag is None and digest is None:
        tag = "latest"

    return registry, repo, image, tag, digest


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
