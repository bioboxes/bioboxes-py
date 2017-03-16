import pytest, tempfile, funcy, os.path
import biobox.image.execute as exe
import helper               as hlp
import biobox.util          as util

IMAGE = 'bioboxes/quast@sha256:1dfe1fb0eb84cd7344b6821cd4f4cdb3f5c1ccb330438eea640b4ce6fda1c4bb'

def biobox_cfg(fasta, refs):
    return [
        {"fasta"    : [ {"id": 0, "type": "contigs", "value": fasta} ] },
        {"fasta_dir": [ {"id": 1, "type": "references", "value": refs} ] },
    ]

@pytest.mark.slow
def test_executing_container():
    out_dir = tempfile.mkdtemp()
    cnt = exe.create_container(
            IMAGE,
            biobox_cfg(hlp.contigs(), hlp.references()),
            {"output" : out_dir},
            "default",
            "0.9.0",
            {"detach" : False})
    id_ = cnt['Id']
    util.client().start(id_)
    util.client().wait(id_)
    assert funcy.get_in(util.client().inspect_container(id_), ['State', 'ExitCode']) == 0
    assert os.path.isfile(os.path.join(out_dir, 'report.tsv'))
    hlp.clean_up_container(id_)
