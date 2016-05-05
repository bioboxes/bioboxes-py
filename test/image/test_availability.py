import pytest
import biobox.image.availability as avail
import biobox.exception

IMAGE_TAGS = [
        "alpine",
        "alpine:3.3",
        "alpine@sha256:9cacb71397b640eca97488cf08582ae4e4068513101088e9f96c9814bfda95e0"]

UNKNOWN_TAGS = [
        "unknown",
        "unknown:3.3",
        "unknown@sha256:9cacb71397b640eca97488cf08582ae4e4068513101088e9f96c9814bfda95e0"]

def test_list_of_local_images():
    images = avail.list_of_local_images()
    for tag in IMAGE_TAGS:
        assert tag in images

def test_checking_a_locally_available_image():
    for tag in IMAGE_TAGS:
        assert avail.is_image_available_locally(tag)

def test_checking_a_locally_non_existent_image():
    for tag in UNKNOWN_TAGS:
        assert not avail.is_image_available_locally(tag)

def test_getting_an_image():
    for tag in IMAGE_TAGS:
        assert avail.get_image(tag)

@pytest.mark.slow
def test_getting_an_image_that_doesnt_exist():
    with pytest.raises(biobox.exception.NoImageFound):
        for tag in UNKNOWN_TAGS:
            avail.get_image(tag)
