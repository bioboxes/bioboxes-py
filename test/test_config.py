import tempfile, os.path
import biobox.config as cnf

dir_1 = tempfile.mkdtemp()
dir_2 = tempfile.mkdtemp()

reads_1 = os.path.join(dir_1, 'reads_1')
reads_2 = os.path.join(dir_1, 'reads_2')
reads_3 = os.path.join(dir_2, 'reads_3')

def create_args(x):
    return [{"fastq" : x}]

def test_remap_args_with_single_file():
    input    = [{"id" : 0 , "value" : reads_1, "type": "paired"}]
    expected = [{"id" : 0 , "value" : "/bbx/mount/0/reads_1", "type": "paired"}]
    assert cnf.remap_biobox_input_paths(create_args(input)) == create_args(expected)

def test_remap_args_with_two_files_in_same_dir():
    input    = [{"id" : 0 , "value" : reads_1, "type": "paired"},
                {"id" : 1 , "value" : reads_2, "type": "paired"}]
    expected = [{"id" : 0 , "value" : "/bbx/mount/0/reads_1", "type": "paired"},
                {"id" : 1 , "value" : "/bbx/mount/0/reads_2", "type": "paired"}]
    assert cnf.remap_biobox_input_paths(create_args(input)) == create_args(expected)

def test_remap_args_with_two_files_in_different_dir():
    input    = [{"id" : 0 , "value" : reads_1, "type": "paired"},
                {"id" : 1 , "value" : reads_3, "type": "paired"}]
    output = cnf.remap_biobox_input_paths(create_args(input))
    assert not os.path.dirname(output[0]['fastq'][0]['value']) == \
            os.path.dirname(output[0]['fastq'][1]['value'])
