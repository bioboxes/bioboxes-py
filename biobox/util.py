import docker
import docker.utils

def client(timeout = 60):
    args = docker.utils.kwargs_from_env(assert_hostname = False)
    args['version'] = '1.20'
    args['timeout'] = timeout
    return docker.Client(**args)
