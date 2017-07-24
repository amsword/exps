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

from common import ensure_folder

class CIFAR(object):
    def __init__(self, which):
        self.train_test_image = None
        self.train_test_label = None
        self.label_names = None
        self.which = which

    def run(self, idx):
        root_folder = '/home/jianfw/';
        curr_folder = os.path.join(root_folder, 'data')
        which = self.which
        class_name = self.__class__.__name__
        if class_name.startswith('Alg'):
            class_name = class_name[3:]
        assert which in [10, 100], (which, type(which))
        base_name = 'cifar-{}-python.tar.gz'.format(which)
        file_name = os.path.join(curr_folder, \
                class_name, \
                base_name)
        self._ensure_data_file(file_name);
        if self.train_test_image is None:
            self._read_image_label(file_name)
        if idx == 0:
            return self.train_test_image[0]
        elif idx == 1:
            return np.array(self.train_test_label[0])
        elif idx == 2:
            return self.train_test_image[1]
        elif idx == 3:
            return np.array(self.train_test_label[1])
        elif idx == 4:
            return self.label_names

    def _ensure_data_file(self, file_name):
        if not os.path.exists(file_name):
            ensure_folder(os.path.dirname(file_name));
            base_name = os.path.basename(file_name)
            url = 'http://www.cs.toronto.edu/~kriz/' + base_name;
            urllib.urlretrieve(url, file_name)
    
    def _add(self, dict_data, type):
        x = dict_data['data']
        assert x.shape[1] == 32 * 32 * 3
        x = x.reshape((x.shape[0], 3, 32, 32)).transpose(0, 2, 3, 1)
        if self.which == 10:
            y = dict_data['labels']
        elif self.which == 100:
            y = dict_data['fine_labels']
        if self.train_test_image is None:
            self.train_test_image = [None] * 2
        if self.train_test_label is None:
            self.train_test_label = [None] * 2
        idx = 0 if type == 'train' else 1
        if self.train_test_image[idx] is None:
            self.train_test_image[idx] = x
        else:
            self.train_test_image[idx] = np.concatenate(\
                    (self.train_test_image[idx], x))
        if self.train_test_label[idx] is None:
            self.train_test_label[idx] = y
        else:
            self.train_test_label[idx].extend(y)

    def _read_image_label(self, file_name):
        fp = tarfile.open(file_name, 'r')
        all_train = [None] * 5
        for member in fp.getmembers():
            if not member.isfile():
                continue
            name = member.name
            if ('readme' in name) or ('file.txt~' in name):
                continue
            if 'test' in name:
                f = fp.extractfile(member)
                x = load(f)
                self._add(x, 'test')
            elif 'data_batch' in name or 'train' in name:
                try:
                    idx = int(float(name[-1])) - 1
                    all_train[idx] = member
                except:
                    all_train = [member]
            elif 'meta' in name:
                f = fp.extractfile(member)
                x = load(f)
                if self.which == 10:
                    self.label_names = x['label_names'] 
                elif self.which == 100:
                    self.label_names = x['fine_label_names'] 
        for member in all_train:
            f = fp.extractfile(member)
            x = load(f)
            self._add(x, 'train')
        fp.close()
