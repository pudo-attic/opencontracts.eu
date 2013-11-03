import os
#import shutil
#from dataset import freeze

from opencontracts.web import app
from opencontracts.db import engine

client = app.test_client()


def get_output_dir():
    return "/tmp"
    return os.path.join(app.root_path, '..', 'build')


def freeze_request(req_path):
    print "Freezing %s..." % req_path
    path = os.path.join(get_output_dir(), req_path.lstrip('/'))
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    fh = open(path, 'w')
    res = client.get(req_path)
    print res.headers
    fh.write(res.data)
    fh.close()



if __name__ == '__main__':
    freeze_request('/index.html')
