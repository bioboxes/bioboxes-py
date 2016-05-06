import docker.utils
import biobox.util         as util
import biobox.config       as cfg
import biobox.image.volume as volume

def prepare_biobox_file(config):
    return volume.biobox_file(
            cfg.create_biobox_directory(
                cfg.generate_biobox_file_content(
                    cfg.remap_biobox_input_paths(config))))
