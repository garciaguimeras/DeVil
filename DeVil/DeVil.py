#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import time
import signal


class daemon(object):

    def __init__(self, process_name):
        self.process_name = process_name
        self.base_commands = {
            "start": (self._start, "Starts daemon"),
            "stop": (self._stop, "Stops daemon"),
            "status": (self._status, "Gets daemon status"),
            "pid": (self._pid, "Prints pid number")
        }

    def start(self):
        pass

    def stop(self):
        pass

    def commands(self):
        return {}

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
        print("Base arguments are:")
        for k in self.base_commands:
            print("    {0}    {1}".format(k, self.base_commands[k][1]))
        commands = self.commands()
        if len(commands) == 0:
            return
        print("Other arguments are:")
        for k in commands:
            print("    {0}    {1}".format(k, commands[k][1]))

    ### Main method    
    def run(self):
        argv = sys.argv[1:]
        if len(argv) < 1:
            self._help()
            return
        arg0 = argv[0]
        args = argv[1:]
        if arg0 in self.base_commands:
            f = self.base_commands[arg0][0]
            f()
            return
        commands = self.commands()
        if arg0 in commands:
            f = commands[arg0][0]
            f(*args)
            return
        self._help()
