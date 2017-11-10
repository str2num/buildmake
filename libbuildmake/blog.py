#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import sys
import threading
import time

import bfunction

class TerminalWriter(object):
    def __init__(self):
        pass

    def write(self, s):
        sys.__stderr__.write(s)

class TerminalLog(object):
    def __init__(self, notice, debug, warning, fatal):
        self._notice = notice
        self._debug = debug
        self._warning = warning
        self._fatal = fatal
        self._quiet = False
        self._debug_level = 0
        self._tw = TerminalWriter()
        self._parallel_mode = False

    def log_notice(self, v):
        if (not self._quiet):
            self._tw.write('%s: %s [%s]\n' % (self._notice, time.strftime('%m-%d %H:%M:%S'), v))

    def log_debug(self, v, trigger = 1):
        if (not self._quiet and
                self._debug_level >= trigger):
            self._tw.write('%s: %s [%s]\n' % (self._debug, time.strftime('%m-%d %H:%M:%S'), v))

    def log_warning(self, v):
        if (not self._quiet):
            self._tw.write('%s: %s [%s]\n' % (self._warning, time.strftime('%m-%d %H:%M:%S'), v))

    def log_fatal(self, v):
        self._tw.write('%s: %s [%s]\n' % (self._fatal, time.strftime('%m-%d %H:%M:%S'), v))
        sys.exit(1) 
    
    def log_notice_with_cc(self, v, cmd, noerror = False):
        if (self._parallel_mode):
            return self._log_notice_with_cc_in_parallel(v, cmd, noerror)
        if (not self._quiet):
            self._tw.write('%s: %s [%s status=' % (self._notice, time.strftime('%m-%d %H:%M:%S'), v))
        (status, out, err) = bfunction.call_command(cmd)
        if (not self._quiet):
            self._tw.write('%d ' % (status))
            if (err and not noerror):
                self._tw.write('err=[%s] ' % (err))
            self._tw.write(']\n') 
        return (status, out, err)
    
    def _log_notice_with_cc_in_parallel(self, v, cmd, noerror):
        if (not self._quiet):
            self._tw.write('%s: %s [%s]\n' % (self._notice, time.strftime('%m-%d %H:%M:%S'), v))
        (status, out, err) = bfunction.call_command(cmd)
        if (not self._quiet):
            if (status == 0 and err and not noerror):
                self._tw.write('%s: %s [status=0 %s err=[%s]]\n' % 
                        (self._debug, time.strftime('%m-%d %H:%M:%S'), v, err))
        return (status, out, err)

BLOG = TerminalLog(
        bfunction.green_it('NOTICE'),
        bfunction.green_it('DEBUG'),
        bfunction.red_it('WARNING'),
        bfunction.red_it('FATAL'))

def get_current():
    global BLOG
    return BLOG


