import os
import urllib
import gzip
import struct
import numpy as np
import logging
import tarfile
from cPickle import load
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import ipdb
from cifar import CIFAR
from settings import quickdetection_script_root
import sys
sys.path.append(quickdetection_script_root)

from common import ensure_folder
from process_tsv import tsv_writer 
import cv2
import base64

def test():
    num = 100 # or 100
    c = CIFAR(num)
    train_image = c.run(0)
    train_label = c.run(1)
    test_image = c.run(2)
    test_label = c.run(3)
    label_names = c.label_names

    def write_to_file(images, labels, file_name): 
        num = images.shape[0]
        assert num == len(labels)
        values = []
        for i in xrange(num):
            if (i % 100) == 0:
                print i, num
            im = images[i, :, :, :]
            im_data = cv2.imencode('.png', im)
            assert im_data[0] == True
            assert len(im_data) == 2
            im_data = base64.b64encode(im_data[1])
            label = labels[i]
            values.append((str(i), str(label), im_data))
        tsv_writer(values, file_name)

    train_file = '/home/jianfw/data/cifar{}/train.tsv'.format(num)
    write_to_file(train_image, train_label, train_file)

    test_file = '/home/jianfw/data/cifar{}/test.tsv'.format(num)
    write_to_file(test_image, test_label, test_file)

    label_map_file = '/home/jianfw/data/cifar{}/labelmap.txt'.format(num)
    with open(label_map_file, 'w') as fp:
        fp.write('\n'.join(label_names))

if __name__ == '__main__':
    test()

