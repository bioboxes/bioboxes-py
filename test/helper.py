import os.path, tempfile
import biobox.util

def clean_up_container(id_):
    if not "CIRCLECI" in os.environ:
        biobox.util.client().remove_container(id_)

#################################################
#
# Example files for testing
#
#################################################

def create_tmp_file(name, dir_ = None):
    if not dir_:
        dir_ = tempfile.mkdtemp()
    path = os.path.join(dir_, name)
    with open(path, 'a'):
        os.utime(path, None)
    return path

def create_tmp_dir(name):
    path = os.path.join(tempfile.mkdtemp(), name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def test_file(path):
    return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..', 'tmp', path)

def short_read_fastq():
    return test_file('data/reads.fq.gz')

def contigs():
    return test_file('data/contigs.fa')

def references():
    return test_file('reference')
