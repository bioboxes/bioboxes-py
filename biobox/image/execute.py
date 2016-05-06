import docker.utils
import biobox.util         as util
import biobox.config       as cfg
import biobox.image.volume as volume

def prepare_biobox_file(config):
    return volume.biobox_file(
            cfg.create_biobox_directory(
                cfg.generate_biobox_file_content(
                    cfg.remap_biobox_input_paths(config))))

def prepare_input_volumes(config):
    None

def prepare_volumes(config, output_directory):
    return [prepare_biobox_file(config),
            prepare_input_volumes(config),
            volume.output(output_directory)]

def create_container(image, config, output_directory, task = "default"):
    volumes = prepare_volumes(config, output_directory)
    return util.client().create_container(
            image,
            task,
            volumes     = map(volume.get_host_path, volumes),
            host_config = docker.utils.create_host_config(binds=volumes))
