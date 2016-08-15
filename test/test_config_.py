import tempfile, os.path, funcy
from functools import partial
import helper as hlp

import biobox.config       as cnf
import biobox.image.volume as vol

#################################################
#
# Test getting paths from biobox args
#
#################################################

def test_get_biobox_paths_with_single_file():
    path = hlp.create_tmp_file("file_0")
    biobox = [{"fastq": [
                        {"id": 0, "type": "paired", "value": path}
                        ]
                    }]
    assert cnf.get_all_biobox_paths(biobox) == [path]


def test_get_biobox_paths_with_two_files():
    path_0 = hlp.create_tmp_file("file_0")
    path_1 = hlp.create_tmp_file("file_1")
    biobox = [{"fastq": [
                        {"id": 0, "type": "paired", "value": path_0},
                        {"id": 0, "type": "paired", "value": path_1}
                        ]
                    }]
    assert cnf.get_all_biobox_paths(biobox) == [path_0, path_1]

#################################################
#
# Test remapping biobox input file paths
#
#################################################

def wrap(t, x):
    return [{t : x}]

def fastq(path):
    return {"id" : 0 , "value" : path, "type": "paired"}

def reference(path):
    return {"id" : 0 , "value" : path, "type": "reference"}

def test_remap_args_with_single_file_entry():
    host_file      = hlp.create_tmp_file("file_0")
    container_file = vol.get_container_mount(host_file)['biobox_target']
    assert cnf.remap_biobox_input_paths(wrap("fastq", [fastq(host_file)])) == \
            wrap("fastq", [fastq(container_file)])

def test_remap_args_with_single_directory_entry():
    host_dir      = hlp.create_tmp_dir("dir_0")
    container_dir = vol.get_container_mount(host_dir)['biobox_target']
    assert cnf.remap_biobox_input_paths(wrap("fasta_dir", [reference(host_dir)])) == \
            wrap("fasta_dir", [reference(container_dir)])
