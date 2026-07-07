# Utils, generic functions, and classes:

from ruamel.yaml import YAML

yaml = YAML(typ='safe')
yaml.default_flow_style = False
yaml.preserve_quotes = True
yaml.width = 120
yaml.indent(mapping=2, sequence=4, offset=2)


def open_yaml(path):
    with path.open("r") as compose_file:
        compose_data = yaml.load(compose_file)
    
    return compose_data
