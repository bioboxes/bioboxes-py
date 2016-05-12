import time, funcy
import biobox.container as ctn
import biobox.util      as util
import test.helper      as hlp

client = util.client()

def container(arg, wait = True):
    container = client.create_container(image='alpine:3.3', command='/bin/sleep {}'.format(str(arg)))
    id_ = container['Id']
    client.start(id_)
    if wait:
        client.wait(id_)
    return id_


def test_did_container_succesfully_exit():
    id_ = container(0.01)
    assert ctn.did_exit_succcessfully(id_)
    hlp.clean_up_container(id_)

def test_did_container_unssuccesfully_exit():
    id_ = container('bad-argument')
    assert not ctn.did_exit_succcessfully(id_)
    hlp.clean_up_container(id_)

def test_is_not_container_running():
    id_ = container('bad-argument')
    assert not ctn.is_running(id_)
    hlp.clean_up_container(id_)

def test_is_container_running():
    id_ = container(10, False)
    time.sleep(0.1)
    assert ctn.is_running(id_)
    client.kill(id_)
    hlp.clean_up_container(id_)

def test_get_runtime_metrics():
    id_ = container(10, False)
    stats = ctn.get_runtime_metrics(id_)
    assert not funcy.isnone(stats)
    assert 'read' in stats
    client.kill(id_)
    hlp.clean_up_container(id_)
