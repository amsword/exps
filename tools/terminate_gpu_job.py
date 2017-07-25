#from settings import pycaffe_root
import sys

#sys.path.append(pycaffe_root)

#import caffe
import psutil

def terminate():
    for process in psutil.process_iter():
        cmd = process.cmdline()
        if process.username() == 'REDMOND.jianfw': 
            if len(cmd) == 2 and 'python' in cmd[0] and 'yolotrain' in cmd[1]:
                print cmd
                process.terminate()

def print_process_info(pid):
    for process in psutil.process_iter():
        if process.pid == pid:
            cmd = process.cmdline()
            print process.username(), \
                    ' '.join(cmd)

if __name__ == '__main__':
    print_process_info(57091)

