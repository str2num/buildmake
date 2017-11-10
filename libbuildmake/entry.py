#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import os
import sys
import getopt

import generator
import makefile_writer
import bcontext
from bsyntax import *
import bgit

VERSION = "1.0"

HELP = """The buildmake tool can automatically help users build a complete compilation
environment for C/C++ project, and generate Makefile. It will read the BUILDMAKE file 
in the current directory, then build environment and generate Makefile. Users need to 
provide this BUILDMAKE file. The default BUILDMAKE file can generate by buildmake 
using -G option.

VERSION: %s
options:
    -h --help                  help infomation.
    -G --generate              generate default BUILDMAKE file
    -U --update environment    if the current project depends on another third libraries,
                               these libraries can be update from git.
    -B --build environment     building project, then generate the binary file
    -v --version               current version
"""

def usage():
    print HELP % (VERSION)

def process_options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hGUBv',  ['help', 'generate', 'update_env', 'build_env', 'version'])
    except getopt.GetoptError, _:
        usage()
        sys.exit(-1)
        
    UPDATE_ENV = False
    BUILD_ENV = False
    
    for (k, v) in opts:
        if k in ('-h', '--help'):
            usage();
            sys.exit(0)
        elif k in ('-G', '--generate'):
            generator.generate()
            sys.exit(0)
        elif k in ('-v', '--version'):
            print 'buildmake version: ' + (VERSION)
            sys.exit(0)
        elif k in ('-U', '--update'):
            UPDATE_ENV = True
        elif k in ('-B', '--build'):
            BUILD_ENV = True
        
        ctx = bcontext.get_context()
        if (UPDATE_ENV and BUILD_ENV):
            ctx.git().set_cmd(bgit.Cmd.UPDATE_AND_BUILD)
        elif (UPDATE_ENV):
            ctx.git().set_cmd(bgit.Cmd.UPDATE)
        elif (BUILD_ENV):
            ctx.git().set_cmd(bgit.Cmd.BUILD)

def interpret_configs():
    ctx = bcontext.get_context()
    targetstring = ctx.interpret_configs_from_buildmake('BUILDMAKE')
    return targetstring

def interpret_targets(targetstring):
    # In case targetstring contains '\r\n'
    targetstring = '\n'.join(targetstring.splitlines()) + '\n'
    exec(targetstring)

def handle(mkwr):
    ctx = bcontext.get_context(); 
    ctx.clear()
    targetstring = interpret_configs()
    interpret_targets(targetstring)
    ctx.action_depends() 
    ctx.action()
    mkwr.collect(ctx)
    mkwr.write()

def gen_makefile():
    func_name = "[Action:gen_makefile]"
    mkwr = makefile_writer.MakefileWriter()
    handle(mkwr)

def main():
    process_options()
    gen_makefile() 

if __name__ == "__main__":
    main()


