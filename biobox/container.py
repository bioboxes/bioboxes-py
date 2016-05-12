import funcy
import biobox.util as util

def metadata_lookup(path, container_id):
    return funcy.get_in(util.client().inspect_container(container_id), path)

def did_exit_succcessfully(id_):
    return metadata_lookup(['State', 'ExitCode'], id_) == 0

def is_running(id_):
    return metadata_lookup(['State', 'Running'], id_)

def get_runtime_metrics(id_):
    return next(util.client().stats(id_))
