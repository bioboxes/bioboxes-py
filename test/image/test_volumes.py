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

def test_create_remapping_with_single_file():
    paths = ["/host/dir/0/file_0"]
    mapping = vol.create_host_container_directory_mapping(paths)
    assert mapping == {"/host/dir/0" : "/bbx/mount/0"}

def test_create_remapping_with_two_files_in_same_dir():
    paths = ["/host/dir/0/file_0", "/host/dir/0/file_1"]
    mapping = vol.create_host_container_directory_mapping(paths)
    assert mapping == {"/host/dir/0" : "/bbx/mount/0"}

def test_create_remapping_with_two_files_in_different_dir():
    paths = ["/host/dir/0/file_0", "/host/dir/1/file_0"]
    mapping = vol.create_host_container_directory_mapping(paths)
    assert mapping == {"/host/dir/0" : "/bbx/mount/1",
                       "/host/dir/1" : "/bbx/mount/0" }

def test_create_input_volume_strings_with_a_single_file():
    paths = ["/host/dir/0/file_0", "/host/dir/1/file_0"]
    volumes = vol.create_input_volume_strings(paths)
    assert volumes == ["/host/dir/1:/bbx/mount/0:ro", "/host/dir/0:/bbx/mount/1:ro"]

