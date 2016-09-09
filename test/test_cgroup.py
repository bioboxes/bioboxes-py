import pytest, time, funcy
import helper        as hlp
import biobox.util   as util
import biobox.cgroup as cgroup

def test_time_diff_in_seconds():
    a = "2016-09-07T14:21:25.783051874Z"
    b = "2016-09-07T14:22:55.783051874Z"
    assert cgroup.time_diff_in_seconds(a, b) == 90


@pytest.mark.slow
def test_collect_metric_with_dead_container():
    id_ = hlp.dummy_container(2)
    stream = util.client().stats(id_, decode = True, stream = True)
    time.sleep(1)
    cgroup.collect_metric(stream)
    time.sleep(1)
    assert cgroup.collect_metric(stream) == None
    hlp.clean_up_container(id_)


def test_collect_metric_with_running_container():
    id_ = hlp.dummy_container(10, False)
    stream = util.client().stats(id_, decode = True, stream = True)
    assert 'read' in cgroup.collect_metric(stream)
    util.client().kill(id_)
    hlp.clean_up_container(id_)


@pytest.mark.slow
def test_collect_metrics():
    id_ = hlp.dummy_container(10, False)
    stats = cgroup.collect_runtime_metrics(id_, interval = 2)
    hlp.clean_up_container(id_)

    cgroup_time = funcy.rpartial(funcy.get_in, ['read'])

    timepoints = list(map(cgroup_time, stats))
    assert len(timepoints) >= 3
    assert len(timepoints)  < 5

    duration = cgroup.time_diff_in_seconds(timepoints[0], timepoints[-1])
    assert duration >= 6
    assert duration < 10
