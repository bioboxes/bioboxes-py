import docker
import docker.utils

def client():
    return docker.Client(**docker.utils.kwargs_from_env(assert_hostname = False))
