#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import os
import string

import bcontext
import syntax_tag
import btarget

def WORKROOT(value):
    ctx = bcontext.get_context()
    ctx.set_workroot(value)

def BUILDMAKE_BIN_PATH(value):
    ctx = bcontext.get_context()
    ctx.set_buildmake_bin_path(value)

def COPY_USING_HARD_LINK(value):
    ctx = bcontext.get_context()
    ctx.set_copy_using_hard_link(value)

def CPPFLAGS(*value):
    ctx = bcontext.get_context()
    ctx.cpp_flags().add_vs(value)

def CFLAGS(*value):
    ctx = bcontext.get_context()
    ctx.c_flags().add_vs(value)

def CXXFLAGS(*value):
    ctx = bcontext.get_context()
    ctx.cxx_flags().add_vs(value)

def _include_paths(tag, value):
    for s in value:
        ps = string.split(s)
        for x in ps:
            if (x[0] == '$'):
                ctx = bcontext.get_context()
                x = '%s%s' % (ctx.workroot(), x[1:])
                x = os.path.normpath(x)
            tag.add_sv(x)
    return tag

def INCPATHS(*value):
    ctx = bcontext.get_context()
    _include_paths(ctx.include_paths(), value)

def LIBS(*value):
    ctx = bcontext.get_context()
    ctx.libraries().add_vs(value)

def LDFLAGS(*value):
    ctx = bcontext.get_context()
    ctx.link_flags().add_vs(value)

def DEFAULT_LIB_INCLUDE_DIR(value):
    ctx = bcontext.get_context()
    ctx.set_default_lib_include_dir(value)

def DEFAULT_GIT_DOMAIN(value):
    ctx = bcontext.get_context()
    ctx.set_default_git_domain(value)

def DEP_CONFIGS(v1, v2, v3):
    ctx = bcontext.get_context()
    group_name = v1
    project_name = v2
    if (ctx.default_git_domain().strip()):
        if (not ctx.default_git_domain().endswith('/')):
            repository = ctx.default_git_domain() + '/' + v3
        else:
            repository = ctx.default_git_domain() + v3
    else:
        repository = v3
    ctx.git().exec_cmd(group_name, project_name, repository)

import glob
def GLOB(*value):
    strs = []
    for s in value:
        ps = string.split(s)
        for p in ps:
            gs = glob.glob(p)
            gs.sort()
            strs.extend(gs)
    return ' '.join(strs)

def _target(name, type, args):
    ctx = bcontext.get_context()
    ctx.create_target(name, type, args)

def Application(name, *args):
    _target(name, btarget.Application.TYPE, args)

def StaticLibrary(name, *args):
    _target(name, btarget.StaticLibrary.TYPE, args)

def SharedLibrary(name, *args):
    _target(name, btarget.SharedLibrary.TYPE, args)

def HeaderFiles(*value):
    tag = syntax_tag.TagHeaderFiles()
    tag.add_vs(value)
    return tag

def _parse_name_and_args(*value):
    args = []
    names = []
    for s in value:
        if (isinstance(s, str)):
            names.extend(string.split(string.strip(s)))
        else:
            args.append(s)
    return (names, args)

def Sources(*value):
    ctx = bcontext.get_context()
    (names, args) = _parse_name_and_args(*value)
    tag = syntax_tag.TagSources()
    for name in names:
        src = ctx.create_source(name, args)
        tag.add_sv(src)
    return tag


