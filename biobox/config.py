import os.path, funcy
import ruamel.yaml         as yaml
import biobox.image.volume as vol

from functools import partial

def get_all_biobox_paths(config):
    """
    Returns all paths listed in the biobox file
    """
    f = funcy.compose(
            partial(funcy.pluck, 'value'),
            funcy.flatten,
            partial(funcy.mapcat, funcy.itervalues))
    return list(f(config))


def remap_entries(xs):
    def remap(x):
        f = lambda i: vol.get_container_mount(i)['biobox_target']
        return funcy.update_in(x, ['value'], f)
    return list(map(remap, xs))


def remap_biobox_input_paths(args):
    return list(map(partial(funcy.walk_values, remap_entries), args))


def generate_biobox_file_content(args):
    output = {"version" : "0.9.0", "arguments" : args}
    return yaml.safe_dump(output, default_flow_style = False)


def create_biobox_directory(content):
    import tempfile
    dir_ = tempfile.mkdtemp()
    with open(os.path.join(dir_, "biobox.yaml"), "w") as f:
        f.write(content)
    return dir_
