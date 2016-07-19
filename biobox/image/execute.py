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


def prepare_volumes(config, output_directory):
    input_strings = vol.create_volume_string_set(cfg.get_all_biobox_paths(config))
    return input_strings + \
            [prepare_biobox_file(config)] + \
            [vol.output(output_directory)]

def create_container(image, config, output_directory, task = "default", docker_args = {}):
    volumes = prepare_volumes(config, output_directory)
    docker_args['volumes']     = list(map(vol.get_host_path, volumes))

    host_config = {'binds' : volumes}
    if 'mem_limit' in docker_args:
        host_config['mem_limit'] = docker_args['mem_limit']
        del docker_args['mem_limit']

    docker_args['host_config'] = util.client().create_host_config(**host_config)
    return util.client().create_container(image, task, **docker_args)
