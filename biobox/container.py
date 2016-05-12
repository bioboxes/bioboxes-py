import funcy
import biobox.util as util
from requests.exceptions import ReadTimeout

def metadata_lookup(path, container_id):
    return funcy.get_in(util.client().inspect_container(container_id), path)

def did_exit_succcessfully(id_):
    return metadata_lookup(['State', 'ExitCode'], id_) == 0

def is_running(id_):
    return metadata_lookup(['State', 'Running'], id_)

def collect_runtime_metrics(container_id, interval = 15, warmup = 1):
    import time
    time.sleep(warmup)

    stream = util.client().stats(container_id, decode = True, stream = True)

    stats = []
    while is_running(container_id):
        stats.append(next(stream))
        time.sleep(interval)
    return stats
