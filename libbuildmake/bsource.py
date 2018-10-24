#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import os
import glob
import string

import syntax_tag
import bfunction

class Source(object):
    TYPE = 'source'
    def __init__(self, infile, args, ctx):
        self._infile = os.path.normpath(infile)
        self._outfile = self._infile
        self._args = args
        self._ctx = ctx
        self._log = ctx.log()
        self._target = None
        self._depends = []
        
        self._make_lines = []
        self._clean_files = []
        self._incpaths = []
        self._cxxflags = []
        self._cppflags = []
        self._cflags = []
        self._prefixes = []
        self._line_delim=' \\\n  '
        self._space_delim=' '

        self._incpaths_flag = False
        self._cxxflags_flag = False
        self._cppflags_flag = False
        self._cflags_flag = False
        
        self._incpaths_s = ''
        self._cxxflags_s = ''
        self._cppflags_s = ''
        self._cflags_s = ''
        self._depends_incpaths = []
        self._depends_incpaths_s = ''

    def in_file(self):
        return self._infile
    
    def out_file(self):
        return self._outfile
    
    def clean_files(self):
        return self._clean_files

    def set_target(self, target):
        self._target = target
    
    def set_depends(self, v):
        self._depends = v
    
    def make_lines(self):
        return self._make_lines

    def pre_action(self):
        if (not self._incpaths_flag):
            self._incpaths = self._ctx.include_paths().v()
        if (not self._cxxflags_flag):
            self._cxxflags = self._ctx.cxx_flags().v()
        if (not self._cppflags_flag):
            self._cppflags = self._ctx.cpp_flags().v()
        if (not self._cflags_flag):
            self._cflags = self._ctx.c_flags().v()
        if (not self._depends_incpaths):
            self._depends_incpaths = self._ctx.depends_include_paths()

        self._incpaths_s = self._line_delim.join(map(lambda x:'-I%s' % x, self._incpaths))
        self._depends_incpaths_s = self._line_delim.join(map(lambda x:'-I%s' % x, self._depends_incpaths))
        self._cxxflags_s = self._line_delim.join(self._cxxflags)
        self._cppflags_s = self._line_delim.join(self._cppflags)
        self._cflags_s = self._line_delim.join(self._cflags)
        
    def action(self):
        pass

class CSource(Source):
    EXTS = ('.c')
    TYPE = 'c'
    def __init__(self, infile, args, ctx):
        Source.__init__(self, infile, args, ctx)
    
    def pre_action(self):
        Source.pre_action(self)

    def action(self): 
        Source.action(self)
        cfile = self._infile
        objfile = bfunction.replace_file_ext_name(
            bfunction.add_prefix_to_basename(
                cfile,
                self._target.basename() + '_'),
            '.o')
        gccflags_s = "%(_incpaths_s)s %(_depends_incpaths_s)s " % (self.__dict__)
        gccflags_s += "%(_cppflags_s)s %(_cflags_s)s " % (self.__dict__)
        real_cc = self._ctx.cc()
        command1 = '%(real_cc)s -MG -MM %(gccflags_s)s %(cfile)s' % (locals())
        command2 = 'cpp -E %(gccflags_s)s %(cfile)s' % (locals())
        depfiles = []
        depfiles.append(cfile)
        depfiles.extend(self._prefixes)
        depfiles.extend(get_cpp_depend_files(command1, command2, self._ctx, self._infile))
        cc = "$(CC)"

        if(not self._incpaths_flag):
            r_gccflags_s = "$(INCPATH) "
        else:
            r_gccflags_s = "%(_incpaths_s)s " % (self.__dict__)

        r_gccflags_s += "$(DEP_INCPATH) "

        if(not self._cppflags_flag):
            r_gccflags_s += "$(CPPFLAGS) "
        else:
            r_gccflags_s += "%(_cppflags_s)s "%(self.__dict__)

        if(not self._cflags_flag):
            r_gccflags_s += "$(CFLAGS) "
        else:
            r_gccflags_s += "%(_cflags_s)s "%(self.__dict__)

        cmd='%(cc)s -c %(r_gccflags_s)s -o %(objfile)s %(cfile)s'%(locals())
        commands = []
        commands.append(cmd)
        r=(objfile, self._line_delim.join(depfiles), commands)
        self._make_lines.append(r)
        self._clean_files.append(objfile)
        self._outfile = objfile 

class CXXSource(Source):
    EXTS = ('.cpp', '.cc', '.cxx')
    TYPE = 'cxx'
    def __init__(self, infile, args, ctx):
        Source.__init__(self, infile, args, ctx)
    
    def action(self):
        Source.action(self)
        cxxfile = self._infile
        objfile = bfunction.replace_file_ext_name(
                bfunction.add_prefix_to_basename(cxxfile, self._target.basename() + '_'), '.o')
        gccflags_s = '%(_incpaths_s)s %(_depends_incpaths_s)s ' % (self.__dict__)
        gccflags_s += '%(_cppflags_s)s %(_cxxflags_s)s ' % (self.__dict__)
        
        real_cc = self._ctx.cxx()
        command1 = '%(real_cc)s -MG -MM %(gccflags_s)s %(cxxfile)s' % (locals())
        command2 = 'cpp -E %(gccflags_s)s %(cxxfile)s' % (locals())
        cxx = '$(CXX)'

        depfiles = []
        depfiles.append(cxxfile)
        depfiles.extend(self._prefixes)
        depfiles.extend(get_cpp_depend_files(command1, command2, self._ctx, self._infile))
 
        if (not self._incpaths_flag):
            r_gccflags_s = '$(INCPATH) '
        else:
            r_gccflags_s = '%(_incpaths_s)s ' % (self.__dict__)

        r_gccflags_s += '$(DEP_INCPATH) '
        
        if (not self._cppflags_flag):
            r_gccflags_s += '$(CPPFLAGS) '
        else:
            r_gccflags_s += '%(_cppflags_s)s ' % (self.__dict__)

        if (not self._cxxflags_flag):
            r_gccflags_s += '$(CXXFLAGS) '
        else:
            r_gccflags_s += '%(_cxxflags_s)s ' % (self.__dict__)
        
        cmd='%(cxx)s -c %(r_gccflags_s)s -o %(objfile)s %(cxxfile)s' % (locals())
        commands = []
        commands.append(cmd)
        r = (objfile, self._line_delim.join(depfiles), commands)
        self._make_lines.append(r)
        self._clean_files.append(objfile)
        self._outfile = objfile

class FileSource(Source):
    def __init__(self, infile, args, ctx):
        Source.__init__(self, infile, args, ctx)

def get_cpp_depend_files(command1, command2, ctx, infile):
    func_name = 'action=get_cpp_depend_files'
    log = ctx.log()
    a = os.getenv('PRE')
    if a == 'True':
        (status, output, err) = (0, ':', '')
    else:
        (status, output, err) = log.log_notice_with_cc('%s cmd=[%s]' % (func_name, 
            bfunction.shorten_word(command1)), command1)
    if (status):
        log.log_fatal('%s cmd=[%s] status=%d err=[%s]' % (func_name, command1, status, err))
    line = ' '.join(string.split(output, '\\\n'))
    depfiles = string.split(string.split(line, ':')[1])
    cwd = '%s/' % (os.path.abspath(os.getcwd())) 
    a = os.getenv('QUOT_ALL_DEPS')
    if a != 'True':
        depfiles = map(lambda x:os.path.normpath(x), 
                filter(lambda x:os.path.abspath(x).startswith(cwd), depfiles))
    for depfile in depfiles:
        if (not os.path.exists(depfile)):
            (status, _, err) = log.log_notice_with_cc('%s cmd=[%s]' % 
                    (func_name, bfunction.shorten_word(command2)), command2)
            assert(status)
            log.log_fatal('%s cmd=[%s] status=%d err=[%s]' % (func_name, 
                command2, status, err))

    if (depfiles and infile == depfiles[0]):
        depfiles = depfiles[1:]

    return depfiles


