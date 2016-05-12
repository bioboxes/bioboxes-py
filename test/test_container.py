import time
import biobox.container as ctn
import biobox.util      as util
import test.helper      as hlp

client = util.client()

def test_did_container_succesfully_exit():
    id_ = client.create_container(image='alpine:3.3', command='/bin/sleep 0.01')['Id']
    client.start(id_)
    client.wait(id_)
    assert ctn.did_exit_succcessfully(id_)
    hlp.clean_up_container(id_)

def test_did_container_unssuccesfully_exit():
    id_ = client.create_container(image='alpine:3.3', command='/bin/sleep bad-argument')['Id']
    client.start(id_)
    client.wait(id_)
    assert not ctn.did_exit_succcessfully(id_)
    hlp.clean_up_container(id_)

def test_is_not_container_running():
    id_ = client.create_container(image='alpine:3.3', command='/bin/sleep bad-argument')['Id']
    client.start(id_)
    client.wait(id_)
    assert not ctn.is_running(id_)
    hlp.clean_up_container(id_)

def test_is_container_running():
    id_ = client.create_container(image='alpine:3.3', command='/bin/sleep 10')['Id']
    client.start(id_)
    time.sleep(0.1)
    assert ctn.is_running(id_)
    client.kill(id_)
    hlp.clean_up_container(id_)
