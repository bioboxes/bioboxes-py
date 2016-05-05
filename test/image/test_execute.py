import os.path
import biobox.image.execute as exe
import biobox.image.volume  as vol

CONFIG = [{"fastq" : [{"id" : "i" , "value" : "v", "type": "t"}]}]

def test_prepare_biobox_file():
    biobox_file_dir = vol.get_host_path(exe.prepare_biobox_file(CONFIG))
    os.path.isdir(biobox_file_dir)
    os.path.isfile(os.path.join(biobox_file_dir, "biobox.yaml"))
