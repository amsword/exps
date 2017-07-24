#from settings import pycaffe_root
import sys

#sys.path.append(pycaffe_root)

#import caffe
import psutil

if __name__ == '__main__':
    for process in psutil.process_iter():
        cmd = process.cmdline()
        if process.username() == 'REDMOND.jianfw': 
            if len(cmd) == 2 and 'python' in cmd[0] and 'yolotrain' in cmd[1]:
                print cmd
                process.terminate()
    print 'good'

