import os.path, pytest, tempfile, funcy

import ruamel.yaml          as yaml
import helper               as hlp

import biobox.image.execute as exe
import biobox.image.volume  as vol
import biobox.util          as util

IMAGE = 'bioboxes/velvet@sha256:6611675a6d3755515592aa71932bd4ea4c26bccad34fae7a3ec1198ddcccddad'

def biobox_cfg(fastq):
    return [
        {"fastq": [
                {"id": 0, "type": "paired", "value": fastq}
            ]
        }
    ]


def test_prepare_biobox_file():
    config = biobox_cfg(hlp.short_read_fastq())
    biobox_file = os.path.join(
            vol.get_host_path(exe.prepare_biobox_file(config)),
            "biobox.yaml")

    assert os.path.isfile(biobox_file)
    with open(biobox_file, 'r') as f:
        biobox_args = yaml.load(f.read())['arguments']
    assert biobox_args == biobox_cfg(vol.get_container_mount(hlp.short_read_fastq())['biobox_target'])


def test_prepare_volumes():
    volumes = exe.prepare_volumes(biobox_cfg(hlp.short_read_fastq()), "/tmp")
    assert len(volumes) == 3
    for d in map(vol.get_host_path, volumes):
        assert os.path.isdir(d) == True
        assert os.access(d, os.W_OK)




@pytest.mark.slow
def test_executing_container():
    out_dir = tempfile.mkdtemp()
    cnt = exe.create_container(
            IMAGE,
            biobox_cfg(hlp.short_read_fastq()),
            out_dir,
            "default",
            {"detach" : False})
    id_ = cnt['Id']
    util.client().start(id_)
    util.client().wait(id_)
    assert funcy.get_in(util.client().inspect_container(id_), ['State', 'ExitCode']) == 0
    assert os.path.isfile(os.path.join(out_dir, 'contigs.fa'))
    hlp.clean_up_container(id_)
