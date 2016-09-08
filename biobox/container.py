import funcy
import biobox.util as util
from requests.exceptions import ReadTimeout

def metadata_lookup(path, container_id):
    """
    Look up metadata about the docker container for the given path
    """
    return funcy.get_in(util.client().inspect_container(container_id), path)

def did_exit_succcessfully(id_):
    """
    Checks if the container exited with 0 exit code
    """
    return metadata_lookup(['State', 'ExitCode'], id_) == 0

def is_running(id_):
    """
    Checks if the container is running
    """
    return metadata_lookup(['State', 'Running'], id_)
