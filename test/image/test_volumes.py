import os
import biobox.image.volume as vol

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

import tempfile
DIR_1 = tempfile.mkdtemp("1", "1")
DIR_2 = tempfile.mkdtemp("2", "2")

def create_tmp_file(dir_, name):
    path = os.path.join(dir_, name)
    with open(path, 'a'):
        os.utime(path, None)
    return path

def create_tmp_dir(dir_, name):
    path = os.path.join(dir_, name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def test_create_remapping_with_single_file():
    paths   = [create_tmp_file(DIR_1, "file_0")]
    mapping = vol.create_host_container_directory_mapping(paths)
    assert mapping == {DIR_1 : "/bbx/mount/0"}

def test_create_remapping_with_single_directory():
    paths = [create_tmp_dir(DIR_1, "dir_1")]
    mapping = vol.create_host_container_directory_mapping(paths)
    assert mapping == {DIR_1 : "/bbx/mount/0"}

def test_create_remapping_with_two_files_in_same_dir():
    paths = [create_tmp_file(DIR_1, "file_0"), create_tmp_file(DIR_1, "file_1")]
    mapping = vol.create_host_container_directory_mapping(paths)
    assert mapping == {DIR_1 : "/bbx/mount/0"}

def test_create_remapping_with_file_and_dir_in_same_dir():
    paths = [create_tmp_file(DIR_1, "file_0"), create_tmp_dir(DIR_1, "dir_1")]
    mapping = vol.create_host_container_directory_mapping(paths)
    assert mapping == {DIR_1 : "/bbx/mount/0"}

def test_create_remapping_with_two_files_in_different_dir():
    paths = [create_tmp_file(DIR_1, "file_0"), create_tmp_file(DIR_2, "file_1")]
    mapping = vol.create_host_container_directory_mapping(paths)
    assert mapping == {DIR_1 : "/bbx/mount/0",
                       DIR_2 : "/bbx/mount/1"}

def test_create_remapping_with_file_and_dir_in_different_dir():
    paths = [create_tmp_file(DIR_1, "file_0"), create_tmp_dir(DIR_2, "dir_0")]
    mapping = vol.create_host_container_directory_mapping(paths)
    assert mapping == {DIR_1 : "/bbx/mount/0",
                       DIR_2 : "/bbx/mount/1"}

#################################################
#
# Creating volume strings
#
#################################################

def test_create_input_volume_strings_with_two_files():
    paths = ["/host/dir/0/file_0", "/host/dir/1/file_0"]
    volumes = vol.create_input_volume_strings(paths)
    assert volumes == ["/host/dir/1:/bbx/mount/1:ro", "/host/dir/0:/bbx/mount/0:ro"]

def test_create_input_volume_strings_with_single_directory():
    paths = [create_tmp_dir(DIR_1, "dir_0")]
    volumes = vol.create_input_volume_strings(paths)
    assert volumes == ["{}:/bbx/mount/0:ro".format(DIR_1)]

def test_create_input_volume_strings_with_file_and_dir_in_different_dir():
    paths = [create_tmp_file(DIR_1, "file_0"), create_tmp_dir(DIR_2, "dir_0")]
    volumes = vol.create_input_volume_strings(paths)
    assert volumes == ["{}:/bbx/mount/0:ro".format(DIR_1), "{}:/bbx/mount/1:ro".format(DIR_2)]
