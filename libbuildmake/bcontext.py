#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import os
import platform

import syntax_tag
import blog
from bsyntax import *
import bsource
import btarget
import bgit
import bdepend
import bfunction

class BContext(object):
    def __init__(self):
        self.clear()
        self._log_handler = blog.get_current()
        self._git_handler = bgit.Git(self)

        self._init_bit_lib()

    def clear(self):
        self._workroot = ''
        self._buildmake_bin_path = ''
        self._cc = 'gcc'
        self._cxx = 'g++'
        self._copy_using_hard_link = False       
        self._default_lib_include_dir = ''
        self._default_git_domain = ''

        self._cppflags = syntax_tag.TagCppFlags()
        self._cflags = syntax_tag.TagCFlags()
        self._cxxflags = syntax_tag.TagCxxFlags()
        self._flags_extra = syntax_tag.TagFlagsExtra()
        self._user_sources_extra = syntax_tag.TagUserSourcesExtra()
        self._incpaths = syntax_tag.TagIncludePaths()
        self._libs = syntax_tag.TagLibraries()
        self._ldflags = syntax_tag.TagLinkFlags()
       
        self._depends = []
        self._sources = []
        self._targets = []
        self._exports = []
        
        self._map_depends = {}

        self._line_delim = ' \\\n  '
        self._depends_incpaths = []

    def print_var(self, lines):
        lines.append("CC=%s" % (self.cc()))
        lines.append("CXX=%s" % (self.cxx()))
     
        cppflags = self.cpp_flags().v()
        cppflags_s = self._line_delim.join(cppflags)
        lines.append("CPPFLAGS=%s" % (cppflags_s))
        
        cflags = self.c_flags().v()
        cflags_s = self._line_delim.join(cflags)
        lines.append("CFLAGS=%s" % (cflags_s))
        
        cxxflags = self.cxx_flags().v()
        cxxflags_s = self._line_delim.join(cxxflags)
        lines.append('CXXFLAGS=%s' % (cxxflags_s))
     
        flags_extra = self.flags_extra().v()
        flags_extra_s = self._line_delim.join(flags_extra)
        lines.append('FLAGSEXTRA=%s' % (flags_extra_s))
   
        incpaths = self.include_paths().v()
        incpaths_s = self._line_delim.join(map(lambda x:'-I%s' % x, incpaths))
        lines.append('INCPATH=%s' % incpaths_s)
        
        depends_incpaths = self.depends_include_paths();
        depends_incpaths_s = self._line_delim.join(map(lambda x:'-I%s' % x, depends_incpaths))
        lines.append('DEP_INCPATH=%s' % (depends_incpaths_s))
        lines.append('\n')        
       
        md5_content = os.popen('md5sum BUILDMAKE').read().strip()
        lines.append('#BUILDMAKE UUID')
        lines.append('BUILDMAKE_MD5=%s' % md5_content)
        lines.append('\n')

    def _init_bit_lib(self):
        self._bit = int(platform.architecture()[0][:2])
        if (64 == self._bit):
            self._lib_env = '64'
        elif (32 == self._bit):
            if (self.cpu().startswith('arm')):
                self._lib_env = 'arm32'
            else:
                self._lib_env = '32'
   
    def workroot(self):
        return self._workroot
    
    def set_workroot(self, value):
        self._workroot = value
    
    def buildmake_bin_path(self):
        return self._buildmake_bin_path

    def set_buildmake_bin_path(self, value):
        self._buildmake_bin_path = value

    def cpu(self):
        return os.popen('uname -m').read().strip()

    def cc(self):
        return self._cc

    def set_cc(self, value):
        self._cc = value
    
    def cxx(self):
        return self._cxx

    def set_cxx(self, value):
        self._cxx = value
    
    def copy_using_hard_link(self):
        return self._copy_using_hard_link

    def set_copy_using_hard_link(self, value):
        self._copy_using_hard_link = value
   
    def default_lib_include_dir(self):
        return self._default_lib_include_dir

    def set_default_lib_include_dir(self, value):
        self._default_lib_include_dir = value 
    
    def default_git_domain(self):
        return self._default_git_domain
    
    def set_default_git_domain(self, value):
        self._default_git_domain = value

    def cpp_flags(self):
        return self._cppflags
    
    def c_flags(self):
        return self._cflags

    def cxx_flags(self):
        return self._cxxflags
    
    def flags_extra(self):
        return self._flags_extra
    
    def user_sources_extra(self):
        return self._user_sources_extra

    def include_paths(self):
        return self._incpaths
   
    def libraries(self):
        return self._libs

    def link_flags(self):
        return self._ldflags
   
    def depends(self):
        return self._depends

    def sources(self):
        return self._sources
    
    def targets(self):
        return self._targets
    
    def exports(self):
        return self._exports
    
    def set_exports(self):
        return self._exports

    def bit(self):
        return self._bit
   
    def set_depends_include_paths(self):
        self._depends_incpaths = []
        for depend in self._depends:
            self._depends_incpaths.extend(
                    map(lambda x:os.path.normpath(os.path.join(depend.base_path(self), x)),
                        depend.include_paths())
                    )
        self._depends_incpaths = bfunction.unique(self._depends_incpaths)
        self._depends_incpaths.sort(lambda x,y:cmp(x, y))

    def depends_include_paths(self):
        return self._depends_incpaths

    def log(self):
        return self._log_handler
    
    def git(self):
        return self._git_handler

    def _need_read_next_line(self, line, right_paren_required):
        prev_c = None
        for c in line:
            if c == '#':
                c = prev_c
                break
            if c == '(':
                right_paren_required += 1
            if c == ')':
                right_paren_required -= 1
            prev_c = c

        if c == '\\' or right_paren_required > 0:
            return True, right_paren_required
        else:
            return False, 0

    def filter_buildmake_for_configs(self, f):
        # Cut BUILDMAKE into two parts
        # <s>: strings on dep info
        # <r>: others
        s = ''
        r = ''
        next_line = False
        right_paren_required = 0
        fd = open(f, 'r')
        lines = fd.readlines()
        fd.close()
        for l in lines:
            origin_line = l
            line = l.strip()
            if not line:
                r += origin_line
                continue
            if next_line:
                r += '\n'
                s += line + '\n'
                result, right_paren_required = self._need_read_next_line(line, right_paren_required)
                if result:
                    next_line = True
                else:
                    next_line = False
                continue
            if line.startswith('WORKROOT'):
                r += origin_line
                s += line + '\n'
                result, right_paren_required = self._need_read_next_line(line, 0)
                if result:
                    next_line = True
                continue
            r += origin_line
        return (s, r) 

    def interpret_configs_from_buildmake(self, f):
        func_name = 'action=interpret_configs_from_buildmake'
        if (not os.path.exists(f)):
            self._log_handler.log_fatal('%s msg=[!exists:%s]' % (func_name, f))
        (configstring, otherstring) = self.filter_buildmake_for_configs(f)
        exec(configstring)
        return otherstring
    
    def create_source(self, name, args):
        file_mode = False
        for arg in args:
            if (isinstance(arg, syntax_tag.TagFileMode)):
                file_mode = True
        # If file mode is True, then ignore the file suffix
        # else according to the suffix to use rules
        if (file_mode):
            src = bsource.FileSource(name, args, self)
        else:
            (_, ext) = os.path.splitext(name)
            if (ext in bsource.CSource.EXTS):
                src = bsource.CSource(name, args, self)
            elif (ext in bsource.CXXSource.EXTS):
                src = bsource.CXXSource(name, args, self)
            else:
                src = bsource.FileSource(name, args, self)
        
        self._sources.append(src)
        return src
    
    def create_target(self, name, type, args):
        func_name = 'action=create_target'
        if (name in ('all', 'clean', 'love', 'dist')):
            self.log().log_fatal('%s msg=["%s" is keyword]' % (func_name, name))
        target = ''
        if (type == btarget.Application.TYPE):
            target = btarget.Application(name, args, self)
        elif (type == btarget.StaticLibrary.TYPE):
            target = btarget.StaticLibrary(name, args, self)
        elif (type == btarget.SharedLibrary.TYPE):
            target = btarget.SharedLibrary(name, args, self)
        
        self._targets.append(target)
        return target
    
    def create_depend(self, group_name, project_name, obj):
        s = '%s/%s:%s' % (group_name, project_name, obj)
        if (s in self._map_depends):
            return self._map_depends[s]

        dep = bdepend.Depend(group_name, project_name, obj, self)
        self._map_depends[s] = dep
        self._depends.append(dep)
        return dep
    
    def action_depends(self):
        action = 'action=action_depends'
        for depend in self._depends:
            depend.detect()
        self._log_handler.log_notice('%s depends=[%s]' % (action,
            '\n'.join(map(lambda x:'%s/%s:%s' % (x.group_name(), x.project_name(),
                x.obj()), self._depends))))

    def action(self):
        # Set include paths of all depends 
        self.set_depends_include_paths()
        
        for target in self._targets:
            target.action()
            
        if (not self._exports):
            self._exports = map(lambda x:x.target(), self._targets)

BUILD_CONTEXT = BContext()

def set_context(context):
    global BUILD_CONTEXT
    BUILD_CONTEXT = context

def get_context():
    global BUILD_CONTEXT
    return BUILD_CONTEXT


