import iso8601, time
import biobox.util      as util
import biobox.container as ctn

def time_diff_in_seconds(a, b):
    """
    Determines the difference in seconds between two string iso8601 dates.
    """
    time_delta = iso8601.parse_date(b) - iso8601.parse_date(a)
    return time_delta.seconds


def collect_metric(container_id):
    """
    Returns a cgroup metric dict for given container id, returns None if a
    ReadTimeoutError is encoutered from the stream. Prevents race conditions
    occuring from checking whether a container is running and then it subsequently
    shutting down before collecting the cgroup metrics.
    """
    import requests.packages.urllib3.exceptions as ex
    try:
        return next(util.client().stats(container_id, decode = True))
    except ex.ReadTimeoutError:
        return None
