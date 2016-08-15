import docker.utils, funcy
import biobox.util         as util
import biobox.config       as cfg
import biobox.image.volume as vol

from functools import partial

def prepare_biobox_file(config):
    """
    Creates a biobox file in a temporary directory and returns a
    Docker volume string for the location.
    """
    f = funcy.compose(
            vol.biobox_file,
            cfg.create_biobox_directory,
            cfg.generate_biobox_file_content,
            cfg.remap_biobox_input_paths)
    return f(config)

def prepare_input_volumes(config):
    """
    Creates volume strings for all input arguments defined in
    the biobox config.
    """
    f = funcy.compose(
            vol.create_input_volume_strings,
            partial(funcy.pluck, 'value'),
            funcy.flatten,
            funcy.cat,
            partial(map, funcy.itervalues))
    return f(config)

def prepare_volumes(config, output_directory, metadata_directory = None):
    vols = prepare_input_volumes(config)  + \
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
    docker_args['host_config'] = util.client().create_host_config(binds=volumes)
    return util.client().create_container(image, task, **docker_args)
