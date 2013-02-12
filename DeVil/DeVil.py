#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import time
import signal


class daemon(object):

    def __init__(self, process_name):
        self.process_name = process_name

    def start(self):
        pass

    def stop(self):
        pass

    ### Methods
    def _print(self, text):
        print("[{0}] {1}".format(self.process_name, text))

    def _child(self):
        self.start()
        os._exit(0) 
        
    def _parent(self, newpid):
        self._print("Daemon started with pid {0}".format(str(newpid)))
        
    def _get_pid(self):
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        found_pid = None
        for pid in pids:
            name = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
            if pid <> str(os.getpid()) and name.find(self.process_name) > -1:
                found_pid = int(pid)
        return found_pid
        
    ### Daemon commands    
    def _start(self):
        pid = self._get_pid()
        if pid is not None:
            self._print("Daemon already running with pid {0}".format(str(pid)))
            return
        newpid = os.fork()
        if newpid == 0:
            self._child()
        else:
            self._parent(newpid)

    def _status(self):
        pid = self._get_pid()
        if pid is None:
            self._print("No daemon running")
            return
        self._print("Daemon is running with pid {0}".format(str(pid)))
            
    def _stop(self):
        pid = self._get_pid()
        if pid is None:
            self._print("No daemon thread running")
            return
        try:
            self.stop()
            os.kill(pid, signal.SIGTERM)
            self._print("Producer thread terminated")
        except OSError:
            self._print("Daemon already stopped")
            
    def _pid(self):
        pid = self._get_pid()
        self._print("PID {0}".format(pid))
        
    def _help(self):
        print("{0} daemon".format(self.process_name))
        print("Expected arguments are:")
        print("     start       Starts producer thread daemon")
        print("     status      Gets producer thread status")    
        print("     stop        Stops producer thread daemon")
        print("     pid         Prints pid number")


    ### Main method    
    def run(self):
        argv = sys.argv[1:]
        if len(argv) <> 1:
            self._help()
            return
        argv = argv[0]
        if argv == "start":
            self._start()
            return
        if argv == "status":
            self._status()
            return        
        if argv == "stop":
            self._stop()
            return
        if argv == "pid":
            self._pid()
            return         
        self._help()
