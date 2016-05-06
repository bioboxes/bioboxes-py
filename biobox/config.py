import os.path, funcy
import biobox.image.volume as vol

from functools import partial

def remap_entries(xs):

    def remap(path_dict, x):
        f = lambda i: os.path.join(path_dict[vol.host_directory(i)], os.path.basename(i))
        return funcy.update_in(x, ['value'], f)

    paths = funcy.pluck('value', xs)
    return map(partial(remap, vol.create_host_container_directory_mapping(paths)), xs)

def remap_biobox_input_paths(args):
    return map(partial(funcy.walk_values, remap_entries), args)

def generate_biobox_file_content(args):
    import yaml
    output = {"version" : "0.9.0", "arguments" : args}
    return yaml.safe_dump(output, default_flow_style = False)

def create_biobox_directory(content):
    import tempfile
    dir_ = tempfile.mkdtemp()
    with open(os.path.join(dir_, "biobox.yaml"), "w") as f:
        f.write(content)
    return dir_
