import os.path
from functools import partial

def remap_entries(entry_type, xs):

    def host_directory(x):
        return os.path.dirname(os.path.abspath(x))

    def container_directory(index):
        return "/" + os.path.join(entry_type, str(index))

    def remap(path_dict, x):
        x['value'] = os.path.join(path_dict[host_directory(x['value'])], os.path.basename(x['value']))
        return x

    uniq_paths = set(map(lambda x: host_directory(x['value']), xs))
    mapping = dict(map(lambda (i, v): (v, container_directory(i)), enumerate(uniq_paths)))
    return map(partial(remap, mapping), xs)

def remap_biobox_input_paths(args):
    return map(lambda i: dict(map(lambda (k, v): (k, remap_entries(k, v)), i.items())), args)

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
