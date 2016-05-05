import os

def create_volume_string(host_dir, container_dir, read_only = True):
    """
    Creates the volume strings used by the Docker daemon for mounting volumes
    """
    access = "ro" if read_only else "rw"
    return ":".join([os.path.abspath(host_dir), container_dir, access])

def output(host_directory_path):
    """
    Creates volume string for the biobox output directory path
    """
    return create_volume_string(host_directory_path, "/bbx/output", False)

def input(host_directory_path):
    """
    Creates volume string for the biobox input directory path
    """
    return create_volume_string(host_directory_path, "/bbx/input", True)

def biobox_file(host_directory_path):
    """
    Creates volume string for the directory containing biobox.yaml
    """
    return create_volume_string(host_directory_path, "/bbx/input")

def get_host_path(volume_string):
    """
    Returns the host path from a Docker volume string
    """
    return volume_string.split(":")[0]
