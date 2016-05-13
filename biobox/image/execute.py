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

def prepare_volumes(config, output_directory):
    return prepare_input_volumes(config)  + \
            [prepare_biobox_file(config)] + \
            [vol.output(output_directory)]

def create_container(image, config, output_directory, task = "default", docker_args = {}):
    volumes = prepare_volumes(config, output_directory)
    docker_args['volumes']     = map(vol.get_host_path, volumes)
    docker_args['host_config'] = util.client().create_host_config(binds=volumes)
    return util.client().create_container(image, task, **docker_args)
