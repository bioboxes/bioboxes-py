import os, funcy
from functools import partial

BIOBOX_INPUT_MOUNT_LOC = "/bbx/mount"

def create_volume_string(host_dir, container_dir, read_only = True):
    """
    Creates the volume strings used by the Docker daemon for mounting volumes
    """
    access = "ro" if read_only else "rw"
    return ":".join([os.path.abspath(host_dir), container_dir, access])


def output(host_directory_path):
    """
    Returns volume string for the biobox output directory path
    """
    return create_volume_string(host_directory_path, "/bbx/output", False)


def input(host_directory_path):
    """
    Returns volume string for the biobox input directory path
    """
    return create_volume_string(host_directory_path, BIOBOX_INPUT_MOUNT_LOC, True)


def metadata(host_directory_path):
    """
    Returns volume string for the biobox metadata directory path
    """
    return create_volume_string(host_directory_path, "/bbx/metadata", False)


def biobox_file(host_directory_path):
    """
    Returns volume string for the directory containing biobox.yaml
    """
    return create_volume_string(host_directory_path, "/bbx/input")


def host_directory(x):
    return os.path.dirname(os.path.abspath(x))


def get_host_path(volume_string):
    """
    Returns the host path from a Docker volume string
    """
    return volume_string.split(":")[0]


def get_container_path(host_directory, container_prefix_path = "/tmp"):
    """
    Returns a container directory location under the given prefix path.
    This is deterministic and always returns the same path for the given host path.
    """
    import hashlib
    from hashids import Hashids
    digest = funcy.rcompose(
            lambda x: hashlib.md5(x.encode('utf-8')).hexdigest(),
            lambda x: int(x, base=16),
            Hashids(min_length=6).encode)
    return os.path.join(container_prefix_path, digest(host_directory))


def get_container_mount(path):
    """
    Returns dictionary with container mount locations for a given path.
    """
    host_dir = host_directory(path)
    cont_dir = get_container_path(host_dir, BIOBOX_INPUT_MOUNT_LOC)
    return {"host_dir"      : host_dir,
            "container_dir" : get_container_path(host_dir, BIOBOX_INPUT_MOUNT_LOC),
            "biobox_target" : os.path.join(cont_dir, os.path.basename(path)) }


def create_volume_string_set(paths):
    """
    Returns uniq list of volume strings for a given list host paths
    """
    f = funcy.rcompose(
            get_container_mount,
            lambda x: create_volume_string(x["host_dir"], x["container_dir"]))
    return list(funcy.distinct(map(f, paths)))
