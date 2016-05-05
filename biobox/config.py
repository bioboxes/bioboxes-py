import os.path

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
