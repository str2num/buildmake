#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import os
import string
import glob

# BUILDMAKE default template
BUILDMAKE_TEMPLATE = """#edit-mode: -*- python -*-
#coding: UTF-8

# Work root
WORKROOT('../../')

# buildmake bin path
BUILDMAKE_BIN_PATH('~/tools/buildmake/buildmake')

# Using hard link copy.
COPY_USING_HARD_LINK(True)

# C preprocessor params
CPPFLAGS('-D_GNU_SOURCE -D__STDC_LIMIT_MACROS -DVERSION=\\\\\\"1.9.8.7\\\\\\"')

# C compile params
CFLAGS('-g -pipe -W -Wall -fPIC')

# C++ compile params
CXXFLAGS('-g -pipe -W -Wall -fPIC')

# Include path
INCPATHS('. ./include ./output ./output/include')

# Using libs
#LIBS('./lib%(module)s.a')

# Default git domain
#DEFAULT_GIT_DOMAIN('https://github.com/')

# Depend libs in git
# Using default git domain
#DEP_CONFIGS('group_name', 'project_name', 'repository')
# Using local git url
#DEP_CONFIGS('group_name', 'project_name', 'https://mygit.com/repository')

# Link params
LDFLAGS('-lpthread -lcrypto -lrt')

# Default include parent dir for headers file
#DEFAULT_LIB_INCLUDE_DIR('%(module)s')

user_sources=%(sources)s
user_headers=%(headers)s

# Generate an application 
#Application('%(module)s', Sources(user_sources))
# Generate a static library
#StaticLibrary('%(module)s', Sources(user_sources), HeaderFiles(user_headers))
# Generate a share library
#SharedLibrary('%(module)s', Sources(user_sources), HeaderFiles(user_headers))

"""

def generate():
    cwd = os.getcwd()
    ps = string.split(cwd, "/")
    workroot = cwd
    workroot = "'%s'" % (workroot)
    module = os.path.basename(cwd)
    
    sources = glob.glob('*.cpp')
    sources += glob.glob('*.c')
    sources += glob.glob('*.cc')
    sources = "'%s'" % (' '.join(sources))
    
    headers = glob.glob('*.h')
    headers += glob.glob('*.hpp')
    headers = "'%s'" % (' '.join(headers))
    
    filename = 'BUILDMAKE';
    open(filename, 'w').write(BUILDMAKE_TEMPLATE % (locals()))


