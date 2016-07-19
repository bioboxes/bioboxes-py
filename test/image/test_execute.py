import pytest, helper, tempfile
import biobox.image.execute as exe

IMAGE  = 'bioboxes/velvet@sha256:6611675a6d3755515592aa71932bd4ea4c26bccad34fae7a3ec1198ddcccddad'
CONFIG = [
        {"fastq": [
                {"id": 0, "type": "paired", "value": helper.short_read_fastq()}
            ]
        }
    ]

def test_create_container_with_cgroup_data():
    args = [{'cpuset' : "0"}, {'cpu_shares' : 1}, {'mem_limit' : 10000000}]
    out_dir = tempfile.mkdtemp()
    for arg in args:
        cnt = exe.create_container(
                IMAGE,
                CONFIG,
                out_dir,
                "default",
                arg)
        helper.clean_up_container(cnt['Id'])
