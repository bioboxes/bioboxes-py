import os.path
import biobox.util

def clean_up_container(id_):
    if not "CIRCLECI" in os.environ:
        biobox.util.client().remove_container(id_)


def short_read_fastq():
    return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..', 'tmp/data/reads.fq.gz')

def biobox_args():
    return [{"fastq" : [
        {"id" : 0 , "value" : short_read_fastq(), "type": "paired"}]}]
