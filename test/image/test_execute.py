import os.path, yaml, pytest, tempfile, funcy
import test.helper          as hlp
import biobox.image.execute as exe
import biobox.image.volume  as vol
import biobox.util          as util

def test_prepare_biobox_file():
    biobox_file_dir = vol.get_host_path(exe.prepare_biobox_file(hlp.biobox_args("short_read_assembler")))
    assert os.path.isdir(biobox_file_dir)

    biobox_file = os.path.join(biobox_file_dir, "biobox.yaml")
    assert os.path.isfile(biobox_file)

    with open(biobox_file, 'r') as f:
        contents = yaml.load(f.read())

    container_path = contents['arguments'][0]['fastq'][0]['value']
    assert container_path == '/bbx/mount/0/reads.fq.gz'


def test_prepare_input_volumes_with_single_file():
    volumes = exe.prepare_input_volumes(hlp.biobox_args("short_read_assembler"))
    assert volumes[0].split(':')[1] == "/bbx/mount/0"


def test_prepare_volumes():
    volumes = exe.prepare_volumes(hlp.biobox_args("short_read_assembler"), "/tmp")
    assert len(volumes) == 3
    for d in map(vol.get_host_path, volumes):
        assert os.path.isdir(d) == True
        assert os.access(d, os.W_OK)
