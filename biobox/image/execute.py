import docker.utils, funcy
import biobox.util         as util
import biobox.config       as cfg
import biobox.image.volume as vol

from functools import partial

def prepare_biobox_file(config):
    """
    Creates a biobox file in a temporary directory and returns a
    Docker volume string for that directory's location.
    """
    f = funcy.compose(
            vol.biobox_file,
            cfg.create_biobox_directory,
            cfg.generate_biobox_file_content,
            cfg.remap_biobox_input_paths)
    return f(config)


def prepare_volumes(config, output_directory, metadata_directory = None):
    vols = vol.create_volume_string_set(cfg.get_all_biobox_paths(config)) +\
            [prepare_biobox_file(config)] + \
            [vol.output(output_directory)]
    if metadata_directory:
        return vols + [vol.metadata(metadata_directory)]
    else:
        return vols


def create_container(image, config, directories, task = "default", docker_args = {}):
    """
    Returns a new biobox Docker container created from the given image name. The
    container is not started.

    Keyword arguments:
      image       -- name of a docker image, may optionally include sha256
      config      -- biobox configuration as specified by the biobox.yaml format
      directories -- dictionary of host directories locations with the keys:
                     output   -- REQUIRED location of output destination directory
                     metadata -- OPTIONAL location of metadata destination directory
      task        -- biobox container task to execute, defaults to "default".
      docker_args -- Optional cgroup data passed to the docker daemon. See the
                     docker documentation for a list of available values
    """

    volumes = prepare_volumes(config, directories.get('output'), directories.get('metadata'))
    docker_args['volumes']     = list(map(vol.get_host_path, volumes))

    host_config = {'binds' : volumes}
    if 'mem_limit' in docker_args:
        host_config['mem_limit'] = docker_args['mem_limit']
        del docker_args['mem_limit']

    docker_args['host_config'] = util.client().create_host_config(**host_config)
    return util.client().create_container(image, task, **docker_args)
