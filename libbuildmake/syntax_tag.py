#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import string
import copy

import bfunction

class TagVector(object):
    def __init__(self):
        self._v = []

    def add_v(self, v):
        self._v.extend(string.split(v))

    def add_vs(self, vs):
        for v in vs:
            self._v.extend(string.split(v))

    def add_sv(self, v):
        self._v.append(v)

    def add_svs(self, vs):
        for v in vs:
            self._v.append(v)

    def v(self):
        return self._v

    def __add__(self, v):
        newtag = copy.copy(self)
        newtag._v = copy.copy(self._v)
        newtag._v.extend(v._v)
        return newtag
    
    def __sub__(self, v):
        newtag = copy.copy(self)
        newv = bfunction.exclude(newtag._v, v._v)
        newtag._v = newv
        return newtag

class TagScalar(object):
    def __init__(self):
        pass

    def set_v(self, v):
        self._v = v

    def v(self):
        return self._v

class TagCppFlags(TagVector):
    def __init__(self):
        TagVector.__init__(self)

class TagCFlags(TagVector):
    def __init__(self):
        TagVector.__init__(self)

class TagCxxFlags(TagVector):
    def __init__(self):
        TagVector.__init__(self)

class TagIncludePaths(TagVector):
    def __init__(self):
        TagVector.__init__(self)

class TagLibraries(TagVector):
    def __init__(self):
        TagVector.__init__(self)

class TagLinkFlags(TagVector):
    def __init__(self):
        TagVector.__init__(self)

class TagSources(TagVector):
    def __init__(self):
        TagVector.__init__(self)

class TagFileMode(TagScalar):
    def __init__(self):
        TagScalar.__init__(self)

class TagHeaderFiles(TagVector):
    def __init__(self):
        TagVector.__init__(self)

class TagOutputPath(TagScalar):
    def __init__(self):
        TagScalar.__init__(self)

class TagHeaderOutputPath(TagScalar):
    def __init__(self):
        TagScalar.__init__(self)


