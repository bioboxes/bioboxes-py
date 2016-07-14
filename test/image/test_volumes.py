import os, tempfile, pytest
import biobox.image.volume as vol
import helper              as hlp

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

#################################################
#
# Volume string tests
#
#################################################

def test_create_volume_string_with_relative_dir():
    expected = "{}/tmp:/tmp:ro".format(root)
    assert vol.create_volume_string("tmp", "/tmp") == expected

def test_create_volume_string_with_absolute_dir():
    expected = "/tmp:/tmp:ro"
    assert vol.create_volume_string("/tmp", "/tmp") == expected

def test_create_output_volume_string():
    expected = "/tmp:/bbx/output:rw"
    assert vol.output("/tmp") == expected

def test_create_input_volume_string():
    expected = "/tmp:/bbx/mount:ro"
    assert vol.input("/tmp") == expected

def test_create_biobox_file_volume_string():
    expected = "/tmp:/bbx/input:ro"
    assert vol.biobox_file("/tmp") == expected

#################################################
#
# Volume remapping tests
#
#################################################

import re
DIR_RE    = re.compile("\/bbx\/mount\/[^\/]+")
TARGET_RE = re.compile("\/bbx\/mount\/[^\/]+\/.+")

def test_get_container_mount_with_single_file():
    path   = hlp.create_tmp_file("file_0")
    volume = vol.get_container_mount(path)
    assert volume['host_dir'] == vol.host_directory(path)
    assert DIR_RE.search(volume['container_dir']) != None
    assert TARGET_RE.search(volume['biobox_target']) != None

def test_get_container_mount_with_single_dir():
    path = hlp.create_tmp_dir("dir_1")
    volume = vol.get_container_mount(path)
    assert volume['host_dir'] == vol.host_directory(path)
    assert DIR_RE.search(volume['container_dir']) != None
    assert TARGET_RE.search(volume['biobox_target']) != None

#################################################
#
# Volume creation strings
#
#################################################

def test_create_volume_string_set_with_single_file():
    dir_ = tempfile.mkdtemp()
    path = hlp.create_tmp_file("file_0", dir_)
    expected = "{}:{}:ro".format(dir_, vol.get_container_mount(path)['container_dir'])
    assert vol.create_volume_string_set([path]) == [expected]


def test_create_volume_string_set_with_two_files_in_same_dir():
    dir_ = tempfile.mkdtemp()
    files = [hlp.create_tmp_file("file_0", dir_), hlp.create_tmp_file("file_1", dir_)]
    assert len(vol.create_volume_string_set(files)) == 1


def test_create_volume_string_set_with_two_files_in_different_dir():
    files = [hlp.create_tmp_file("file_0"), hlp.create_tmp_file("file_1")]
    assert len(vol.create_volume_string_set(files)) == 2
