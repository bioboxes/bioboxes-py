import os.path, yaml, pytest
import test.helper          as hlp
import biobox.image.execute as exe
import biobox.image.volume  as vol

def test_prepare_biobox_file():
    biobox_file_dir = vol.get_host_path(exe.prepare_biobox_file(hlp.biobox_args()))
    assert os.path.isdir(biobox_file_dir)

    biobox_file = os.path.join(biobox_file_dir, "biobox.yaml")
    assert os.path.isfile(biobox_file)

    with open(biobox_file, 'r') as f:
        contents = yaml.load(f.read())

    container_path = contents['arguments'][0]['fastq'][0]['value']
    assert container_path == '/bbx/mount/0/reads.fq.gz'


def test_prepare_input_volumes_with_single_file():
    config = [{"fastq" : [{"id" : 0 , "value" : "/host/dir/reads.fq.gz", "type": "paired"}]}]
    volumes = exe.prepare_input_volumes(config)
    assert volumes == ["/host/dir:/bbx/mount/0:ro"]
