#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import os

class Depend(object):
    def __init__(self, group_name, project_name, obj, ctx):
        self._group_name = group_name
        self._project_name = project_name
        self._obj = os.path.normpath(obj)
        self._ctx = ctx
        self._incpaths = []
        self._depends = []

    def group_name(self):
        return self._group_name

    def project_name(self):
        return self._project_name
    
    def obj(self):
        return self._obj

    def include_paths(self):
        return self._incpaths

    def base_path(self, ctx):
        return os.path.normpath(os.path.join(ctx.workroot(), 
            self._group_name, self._project_name))
    
    def depends(self):
        return self._depends

    def detect_include_paths(self):
        flag = False
        incpaths = []

        if (not flag):
            incpaths = ['.', './include', './output', './output/include']
            incpaths.append('./output/include/' + self._project_name[3:])
            incpaths = map(lambda x:os.path.normpath(x), incpaths)

        self._incpaths = incpaths
    
    def detect(self):
        self.detect_include_paths()


