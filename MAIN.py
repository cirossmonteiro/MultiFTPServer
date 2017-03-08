import os, thread as th, time, subprocess as sp, signal, psutil
from multiprocessing import Pool, Process

def correct_space(s):
    s2 = ""
    for c in s:
        if c == ' ':
            s2 += '\\'
        s2 += c
    return str(s2)

class MultiFTP():

    def __init__(self, par = "portas;portas passivas;diretorio"):
        self.__par = par

    def __start(self, arg):
        cmd = "python runFTPserver.py %d %d %d %s"%arg
        print "Starting FTP server: ", arg, '\n'
        os.system(cmd)

    def start(self):
        fh = open(self.__par)
        data = fh.read()
        fh.close()
        data = data.split('\n')[:-1]
        for i in xrange(len(data)):
            if len(data[i]) > 5:
                data[i] = data[i].split(';')
                q1,q2 = data[i][1].split(',')
                args = ((int(q1), int(q2), int(data[i][0]), correct_space(data[i][-1])),)
                th.start_new_thread(self.__start, args)
                time.sleep(1)

    def stop(self):
        pids = psutil.pids()
        for pid in pids:
            if "runFTPserver.py" in psutil.Process(pid).cmdline():
                os.kill(pid, signal.SIGKILL)

    def __del__(self):
        self.stop()


many = MultiFTP()
#many.start()
#many.stop()
