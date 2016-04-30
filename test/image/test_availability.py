import pytest
import biobox.image.availability as avail
import biobox.exception

def test_checking_a_locally_available_image():
    assert avail.is_image_available_locally("alpine")

def test_checking_an_locally_available_image_with_tag():
    assert avail.is_image_available_locally("alpine:3.3")

def test_checking_a_locally_non_existent_image():
    assert not avail.is_image_available_locally("bioboxes/unknown")

def test_getting_an_image():
    avail.get_image("alpine")

def test_getting_an_image_with_tag():
    avail.get_image("alpine:3.3")

def test_getting_an_image_that_doesnt_exist():
    with pytest.raises(biobox.exception.NoImageFound):
        avail.get_image("bioboxes/unknown")
