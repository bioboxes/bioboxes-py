import pytest
import helper        as hlp
import biobox.util   as util
import biobox.cgroup as cgroup

def test_time_diff_in_seconds():
    a = "2016-09-07T14:21:25.783051874Z"
    b = "2016-09-07T14:22:55.783051874Z"
    assert cgroup.time_diff_in_seconds(a, b) == 90


@pytest.mark.slow
def test_collect_metric_with_dead_container():
    id_ = hlp.dummy_container(0.01)
    assert cgroup.collect_metric(id_) == None
    hlp.clean_up_container(id_)


def test_collect_metric_with_running_container():
    id_ = hlp.dummy_container(10, False)
    assert 'read' in cgroup.collect_metric(id_)
    util.client().kill(id_)
    hlp.clean_up_container(id_)
