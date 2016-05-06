import os
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
    Creates volume string for the biobox output directory path
    """
    return create_volume_string(host_directory_path, "/bbx/output", False)


def input(host_directory_path):
    """
    Creates volume string for the biobox input directory path
    """
    return create_volume_string(host_directory_path, BIOBOX_INPUT_MOUNT_LOC, True)


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


def host_directory(x):
    return os.path.dirname(os.path.abspath(x))


def create_host_container_directory_mapping(paths):
    """
    Given a list of dirs on the host returns a dictionary mapping
    them to dirs within the Docker container
    """

    def container_directory(index):
        return os.path.join(BIOBOX_INPUT_MOUNT_LOC, str(index))

    uniq_paths = set(map(host_directory, paths))
    return dict(map(lambda (i, v): (v, container_directory(i)), enumerate(uniq_paths)))


def create_input_volume_strings(paths):
    """
    Given a list of dirs on the host returns the volume strings used by the
    Docker daemon to mount the dirs into the container
    """
    return map(partial(apply, create_volume_string),
            create_host_container_directory_mapping(paths).items())
