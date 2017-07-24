import os 
import sys

project_root = '/home/jianfw'
if not os.path.exists(project_root):
    project_root = '/work'
    assert os.path.exists(project_root)

code_root = os.path.join(project_root, 'code')

caffe_root = os.path.join(code_root, 'caffe-fast-rcnn')

pycaffe_root = os.path.join(caffe_root, 'python')

quickdetection_root = os.path.join(code_root, 'quickdetection')

quickdetection_script_root = os.path.join(quickdetection_root, 'scripts')

sys.path.append(quickdetection_script_root)

if __name__ == '__main__':
    print pycaffe_root
