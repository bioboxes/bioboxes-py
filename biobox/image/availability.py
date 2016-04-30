import biobox.util      as util
import biobox.exception

def get_image_tags(docker_dict):
    """
    Returns list of all Docker image names with and without tags.
    E.g. includes both python and python:2.7
    """
    return reduce(lambda acc, x: acc + [x, x.split(":")[0]],
            docker_dict['RepoTags'], [])

def list_of_local_images():
    """
    Returns a set containing all local docker image names and tags.
    """
    image_tags = map(get_image_tags, util.client().images())
    return set(reduce(lambda acc, x: acc + x, image_tags, []))

def is_image_available_locally(name):
    """
    Does what you might expect.
    """
    return name in list_of_local_images()

def get_image(name):
    """
    Fetches the Docker image if it is not present locally.
    """
    if not is_image_available_locally(name):
        output = util.client().pull(name)
        if "error" in output:
            raise biobox.exception.NoImageFound(name)
