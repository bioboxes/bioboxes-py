import os.path, yaml, pytest, tempfile, funcy
import test.helper          as hlp
import biobox.image.execute as exe
import biobox.image.volume  as vol
import biobox.util          as util

IMAGE = 'bioboxes/tadpole@sha256:d20cdfc02f9e305c931a93c34a8678791d2ebc084f257afd57a79f772e0b470d'



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
    volumes = exe.prepare_input_volumes(hlp.biobox_args())
    assert volumes[0].split(':')[1] == "/bbx/mount/0"


def test_prepare_volumes():
    volumes = exe.prepare_volumes(hlp.biobox_args(), "/tmp")
    assert len(volumes) == 3
    for d in map(vol.get_host_path, volumes):
        assert os.path.isdir(d) == True
        assert os.access(d, os.W_OK)


def test_prepare_volumes_with_metadata_dir():
    volumes = exe.prepare_volumes(hlp.biobox_args(), tempfile.mkdtemp(), tempfile.mkdtemp())
    assert len(volumes) == 4
    for d in map(vol.get_host_path, volumes):
        assert os.path.isdir(d) == True
        assert os.access(d, os.W_OK)


def test_create_container():
    cnt = exe.create_container(
            IMAGE,
            hlp.biobox_args(),
            {"output" : tempfile.mkdtemp()})
    assert "Id" in cnt
    hlp.clean_up_container(cnt["Id"])


@pytest.mark.slow
def test_executing_container():
    out_dir = tempfile.mkdtemp()
    cnt = exe.create_container(
            IMAGE,
            hlp.biobox_args(),
            {"output" : out_dir},
            "default",
            {"detach" : False})
    id_ = cnt['Id']
    util.client().start(id_)
    util.client().wait(id_)
    assert funcy.get_in(util.client().inspect_container(id_), ['State', 'ExitCode']) == 0
    assert os.path.isfile(os.path.join(out_dir, 'contigs.fa'))
    hlp.clean_up_container(id_)


@pytest.mark.slow
def test_executing_container_with_metadata():
    out_dir  = tempfile.mkdtemp()
    meta_dir = tempfile.mkdtemp()
    cnt = exe.create_container(
            IMAGE,
            hlp.biobox_args(),
            {"output" : out_dir, "metadata" : meta_dir},
            "default",
            {"detach" : False})
    id_ = cnt['Id']
    util.client().start(id_)
    util.client().wait(id_)
    assert funcy.get_in(util.client().inspect_container(id_), ['State', 'ExitCode']) == 0
    assert os.path.isfile(os.path.join(out_dir, 'contigs.fa'))
    assert os.path.isfile(os.path.join(meta_dir, 'log.txt'))
    hlp.clean_up_container(id_)
