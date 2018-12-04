#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import os
import sys
import string
import commands

import bfunction
from bsyntax import *

class Cmd:
    UPDATE = 0
    BUILD = 1
    UPDATE_AND_BUILD = 2
    DEPEND = 3

class Git(object):
    def __init__(self, ctx):
        self._ctx = ctx
        self._log = ctx.log()
        self._cmd = Cmd.DEPEND
        self._local_lib = {}
        self._depends = []

    def set_cmd(self, value):
        self._cmd = value

    def exec_cmd(self, group_name, project_name, repository):
        if self._cmd == Cmd.UPDATE:
            self._update(group_name, project_name, repository)
        elif self._cmd == Cmd.BUILD:
            self._build(group_name, project_name, repository)
        elif self._cmd == Cmd.UPDATE_AND_BUILD:
            self._update(group_name, project_name, repository)
            self._build(group_name, project_name, repository)
        
        self._depend(group_name, project_name)

    def _update(self, group_name, project_name, repository):
        func_name = 'func_name=Git.UPDATE'
        workroot = self._ctx.workroot()
        if (not os.path.exists('%s%s' % (workroot, group_name))):
            command = 'cd %s && mkdir -p %s' % (workroot, group_name)
            os.system(command)
        
        self._log.log_notice('%s msg=[Update %s/%s from %s]' % (func_name, group_name, project_name, repository))
        # Update from git
        if (not os.path.exists('%s%s/%s' % (workroot, group_name, project_name))):
            command = 'cd %s%s && git clone %s' % (workroot, group_name, repository)
        else:
            command = 'cd %s%s/%s && git pull' % (workroot, group_name, project_name)
        os.system(command)
        
    def _build(self, group_name, project_name, repository):
        func_name = 'func_name=Git.BUILD'
        self._log.log_notice('%s msg=[Build %s/%s]' % (func_name, group_name, project_name))
        workroot = self._ctx.workroot()
        if (os.path.exists('%s%s/%s/BUILDMAKE' % (workroot, group_name, project_name))):
            command = 'cd %s%s/%s && %s && make' % (workroot, group_name, 
                    project_name, self._ctx.buildmake_bin_path())
            print command
        if (os.system(command) != 0):
            print "command exec failed, please check buildmake path, buildmake path can be modified by BUILDAMKE config file."
            exit(0)
    
    def _depend(self, group_name, project_name):
        workroot = self._ctx.workroot()
        basepath = os.path.normpath(os.path.join(workroot, group_name, project_name))
        action = 'action=Git.DEPEND'
        objects = ''
        if (os.path.exists(basepath)):
            objects = self._detect_local_lib(basepath)
        
        if (not objects):
            self._log.log_warning('%s basepath=%s msg=[object is NULL]' % (action, basepath))
            self._depends.append(self._ctx.create_depend(group_name, project_name, ''))
            return
        
        for obj in objects:
            self._depends.append(self._ctx.create_depend(group_name, project_name, obj))

    def _detect_local_lib(self, path):
        if (path in self._local_lib):
            return self._local_lib[path]

        cwd = os.getcwd()
        os.chdir(path)
        exts = ('.a', )
        # 1. find in current path
        libs = bfunction.find_files_exts('.', False, exts)
        # 2. find in ./output
        if (os.path.exists('./output')):
            libs += bfunction.find_files_exts('./output', True, exts)
        # 3. find in ./lib
        if (os.path.exists('./lib')):
            libs += bfunction.find_files_exts('./lib', True, exts)

        # 4. unique
        libs = bfunction.unique(libs, lambda x:os.path.basename(x))
        os.chdir(cwd)

        self._local_lib[path] = libs
        return libs


