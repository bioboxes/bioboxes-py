import pytest, helper, tempfile
import biobox.image.execute as exe

IMAGE = 'bioboxes/tadpole@sha256:d20cdfc02f9e305c931a93c34a8678791d2ebc084f257afd57a79f772e0b470d'
CONFIG = [
        {"fastq": [
                {"id": 0, "type": "paired", "value": helper.short_read_fastq()}
            ]
        }
    ]

def test_create_container_with_cgroup_data():
    # Currently {'cpuset' : "0"} is too hard to test because I don't know
    # how to get the CPU IDs for the machine being used for testing
    args = [{'cpu_shares' : 1}, {'mem_limit' : 10000000}]
    out_dir = tempfile.mkdtemp()
    for arg in args:
        cnt = exe.create_container(
                IMAGE,
                CONFIG,
                {"output" : out_dir},
                "default",
                "0.9.0",
                arg)
        helper.clean_up_container(cnt['Id'])
