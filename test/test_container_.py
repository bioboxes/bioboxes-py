import time, pytest
import helper           as hlp
import biobox.util      as util
import biobox.container as ctn

def test_did_container_succesfully_exit():
    id_ = hlp.dummy_container(0.01)
    assert ctn.did_exit_succcessfully(id_)
    hlp.clean_up_container(id_)

def test_did_container_unssuccesfully_exit():
    id_ = hlp.dummy_container('bad-argument')
    assert not ctn.did_exit_succcessfully(id_)
    hlp.clean_up_container(id_)

def test_is_not_container_running():
    id_ = hlp.dummy_container('bad-argument')
    assert not ctn.is_running(id_)
    hlp.clean_up_container(id_)

def test_is_container_running():
    id_ = hlp.dummy_container(10, False)
    time.sleep(0.1)
    assert ctn.is_running(id_)
    util.client().kill(id_)
    hlp.clean_up_container(id_)
