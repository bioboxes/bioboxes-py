import pytest
import biobox.cgroup as cgroup

def test_time_diff_in_seconds():
    a = "2016-09-07T14:21:25.783051874Z"
    b = "2016-09-07T14:22:55.783051874Z"
    assert cgroup.time_diff_in_seconds(a, b) == 90
