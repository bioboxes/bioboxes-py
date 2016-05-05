import biobox.util      as util
import biobox.exception

def get_image_tags(docker_dict):
    """
    Returns list of the names with and without tags for a given Docker image.
    E.g. returns ["python", "python:2.7"]
    """
    tags = docker_dict['RepoTags']
    if (tags is None) or (tags == [u'<none>:<none>']):
        return []
    else:
        return reduce(lambda acc, x: acc + [x, x.split(":")[0]], tags, [])

def get_image_digests(docker_dict):
    """
    Returns list all digests, if they exist, for a Docker image
    """
    digests = docker_dict['RepoDigests']
    if (digests is None) or (digests == [u'<none>@<none>']):
        return []
    else:
        return digests

def list_of_local_images():
    """
    Returns a set containing all local docker image tags and digests.
    """
    images = util.client().images()
    tags_and_digests = map(get_image_tags, images) + map(get_image_digests, images)
    return set(reduce(lambda acc, x: acc + x, tags_and_digests, []))

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
    return True
