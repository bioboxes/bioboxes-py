import pytest, tempfile, funcy, os.path
import biobox.image.execute as exe
import test.helper          as hlp
import biobox.util          as util

IMAGE = 'bioboxes/velvet@sha256:6611675a6d3755515592aa71932bd4ea4c26bccad34fae7a3ec1198ddcccddad'

@pytest.mark.slow
def test_executing_container():
    out_dir = tempfile.mkdtemp()
    cnt = exe.create_container(
            IMAGE,
            hlp.biobox_args("short_read_assembler"),
            out_dir,
            "default",
            {"detach" : False})
    id_ = cnt['Id']
    util.client().start(id_)
    util.client().wait(id_)
    assert funcy.get_in(util.client().inspect_container(id_), ['State', 'ExitCode']) == 0
    assert os.path.isfile(os.path.join(out_dir, 'contigs.fa'))
    hlp.clean_up_container(id_)
