import os.path

def short_read_fastq():
    return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..', 'tmp/data/reads.fq.gz')

def biobox_args():
    return [{"fastq" : [
        {"id" : 0 , "value" : short_read_fastq(), "type": "paired"}]}]
