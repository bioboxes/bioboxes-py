import iso8601, time
import biobox.util      as util
import biobox.container as ctn

def time_diff_in_seconds(a, b):
    """
    Determines the difference in seconds between two string iso8601 dates.
    """
    time_delta = iso8601.parse_date(b) - iso8601.parse_date(a)
    return time_delta.seconds


def collect_metric(stream):
    """
    Returns a cgroup metric dict from a given container stream, returns None if a
    ReadTimeoutError or StopIteration is encoutered from the stream. Prevents race
    conditions occuring from checking whether a container is running and then it
    subsequently shutting down before collecting the cgroup metrics.
    """
    import requests.packages.urllib3.exceptions as ex
    try:
        return next(stream)
    except ex.ReadTimeoutError:
        return None
    except StopIteration:
        return None


def collect_runtime_metrics(container_id, interval = 15, warmup = 1):
    """
    Collects cgroup runtime metrics from the specified container at the given
    per-second intervals.
    """

    stream = util.client().stats(container_id, decode = True, stream = True)
    time.sleep(warmup)
    stats  = [next(stream)]

    while ctn.is_running(container_id):
        time.sleep(1)
        entry = collect_metric(stream)

        # Remove this when docker/docker-py#1195 is fixed
        if not entry:
            pass
        else:
            # Save the cgroup entry if it is greater than given time interval
            if time_diff_in_seconds(stats[-1]['read'], entry['read']) > interval:
                stats.append(entry)
    return stats
