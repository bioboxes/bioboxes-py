import os
import biobox.image.volume as vol

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

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
    expected = "/tmp:/bbx/input:ro"
    assert vol.input("/tmp") == expected

def test_create_biobox_file_volume_string():
    expected = "/tmp:/bbx/input:ro"
    assert vol.biobox_file("/tmp") == expected
