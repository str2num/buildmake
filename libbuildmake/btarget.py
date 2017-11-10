#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import os
import syntax_tag
import bfunction

warn_linkdeps_once = False

class Target(object):
    TYPE = 'target'
    
    def __init__(self, name, args, ctx):
        self._name = os.path.normpath(name)
        self._args = args
        self._ctx = ctx
        self._target = ''
        
        self._make_lines = []
        self._make_clean_lines = []
        self._clean_files = []
        self._phony_mode = False
        self._prefixes = []
        self._sources = []
        self._depends = []
        self._header_files = []
        self._line_delim = ' \\\n  '
        self._space_delim = ' '

        self._depends_libs = []
        self._depends_libs_s = ''
        self._sources_infiles = []
        self._sources_outfiles = []
    
    def name(self):
        return self.name

    def basename(self):
        return os.path.basename(self._name)
    
    def target(self):
        return self._target
    
    def make_lines(self):
        return self._make_lines
    
    def make_clean_lines(self):
        return self._make_clean_lines

    def clean_files(self):
        return self._clean_files
    
    def phony_mode(self):
        return self._phony_mode

    def prefixes(self):
        return self._prefixes
    
    def header_files(self):
        return self._header_files
    
    def _move_libs_from_depends(self, libs):
        action = '_move_libs_from_depends'
        for lib in libs:
            if (lib in self._depends_libs):
                self._depends_libs.remove(lib)
            else:
                msg = '%s not found, please check it' % lib
                self._env.log().log_fatal('%s msg=[%s]' % (action, msg))
        if (libs):
            self._depends_libs_s = self._line_delim.join(self._depends_libs)

    def action(self):
        for arg in self._args:
            if (isinstance(arg, syntax_tag.TagSources)):
                self._sources.extend(arg.v())
        self._depends = self._ctx.depends()
        
        for source in self._sources:
            source.set_target(self)
            source.set_depends(self._depends)
            source.pre_action()
        for source in self._sources:
            source.action()
        
        self._sources_infiles = bfunction.unique(
                map(lambda x:os.path.normpath(x.in_file()), self._sources))
        self._sources_outfiles = bfunction.unique(
                map(lambda x:os.path.normpath(x.out_file()), self._sources))
        self._depends = filter(lambda x:x.obj() != os.path.normpath(''), self._depends)
        
        for depend in self._depends:
            self._depends_libs.append(os.path.join(depend.base_path(self._ctx),
                depend.obj()))
        
        self._depends_libs.sort(lambda x,y:cmp(x,y))
        self._depends_libs_s = self._line_delim.join(self._depends_libs)
    
    def _get_compiler_bin_by_src(self, srcs):
        for src in srcs:
            (_, ext) = os.path.splitext(src)
            if (ext != '.c'):
                return '$(CXX)'
        return '$(CC)'

class Application(Target):
    TYPE = 'app'
    
    def __init__(self, name, args, ctx):
        Target.__init__(self, name, args, ctx)
        self._target = self._name
 
    def action(self):
        Target.action(self)
        target = self._target
        output_path = './output/bin'

        libs_flag = False
        ldflags_flag = False
        libs = []
        ldflags = []
        link_libs = []
        
        for arg in self._args:
            pass

        if (not libs_flag):
            libs = self._ctx.libraries().v()
        if (not ldflags_flag):
            ldflags = self._ctx.link_flags().v()

        libs_s = self._line_delim.join(libs)
        ldflags_s = self._line_delim.join(ldflags)
        objs_s = self._line_delim.join(self._sources_outfiles)
        depends_libs_s = self._depends_libs_s
        cpflags_s = '-f' # copy option
        if (self._ctx.copy_using_hard_link()):
            cpflags_s += ' --link'
        
        # Shell commands
        # cxx = self._ctx.cxx()
        cxx = "$(CXX)"
        
        commands = []
        if (link_libs):
            link_libs_s = self._line_delim.join(link_libs)
            cmd = '%(cxx)s %(objs_s) -Xlinker "-(" %(link_libs_s)s %(ldflags_s)s -Xlinker "-)" -o %(target)s' % (locals())
        else:
            cmd = '%(cxx)s %(objs_s)s -Xlinker "-(" %(libs_s)s ' % (locals())
            cmd += '%(depends_libs_s)s %(ldflags_s)s -Xlinker "-)" -o %(target)s' % (locals())
            commands.append(cmd)
        if (output_path):
            commands.append('mkdir -p %(output_path)s' % (locals()))
            commands.append('cp %(cpflags_s)s %(target)s %(output_path)s' % (locals()))
            
        r = (target, 
            self._line_delim.join(self._prefixes + self._sources_outfiles + libs),
            commands)
        self._make_lines.append(r)

        # Clean commands
        self._clean_files.append(target)
        if (output_path):
            self._clean_files.append(os.path.join(output_path, os.path.basename(target)))

class StaticLibrary(Target):
    TYPE = 'lib'

    def __init__(self, name, args, ctx):
        Target.__init__(self, name, args, ctx)
        self._target = bfunction.add_prefix_to_basename(
                bfunction.add_file_ext_name(self._name, '.a'),
                'lib')

    def action(self):
        Target.action(self)
        target = self._target
        output_path = './output/lib'
        header_output_path = './output/include'
        if (self._ctx.default_lib_include_dir().strip()):
            header_output_path += '/' + self._ctx.default_lib_include_dir()
        
        for arg in self._args:
            if (isinstance(arg, syntax_tag.TagOutputPath)):
                output_path = arg.v()
            elif (isinstance(arg, syntax_tag.TagHeaderOutputPath)):
                header_output_path = arg.v()
            elif (isinstance(arg, syntax_tag.TagHeaderFiles)):
                self._header_files.extend(arg.v())
            else:
                continue
        objs_s = self._line_delim.join(self._sources_outfiles)
        cpflags_s = '-f' # copy option
        if (self._ctx.copy_using_hard_link()):
            cpflags_s += ' --link'
        
        # shell commands
        commands = []
        commands.append('ar crs %(target)s %(objs_s)s' % (locals()))
        if (output_path):
            commands.append('mkdir -p %(output_path)s' % (locals()))
            commands.append('cp %(cpflags_s)s %(target)s %(output_path)s' % (locals()))

        if (header_output_path and self._header_files):
            commands.append('mkdir -p %(header_output_path)s' % (locals()))
            commands.append('cp %s %s %s' % (cpflags_s,
                                            ' '.join(self._header_files),
                                            header_output_path))
        
        r = (target, self._line_delim.join(self._prefixes + 
                                           self._sources_outfiles +
                                           self._header_files),
            commands)
        self._make_lines.append(r)

        # clean commands
        self._clean_files.append(target)
        if (output_path):
            self._clean_files.append(os.path.join(output_path, os.path.basename(target)))
        if (header_output_path):
            self._clean_files.extend(map(lambda x:os.path.join(header_output_path,
                                                              os.path.basename(x)),
                                        self._header_files))

class SharedLibrary(Target):
    TYPE = 'so'
    
    def __init__(self, name, args, ctx):
        Target.__init__(self, name, args, ctx)
        self._target = bfunction.add_prefix_to_basename(
                bfunction.add_file_ext_name(self._name, '.so'),
                'lib')

    def action(self):
        Target.action(self)
        target = self._target
        output_path = './output/so'
        header_output_path = './output/include'
        if (self._ctx.default_lib_include_dir().strip()):
            header_output_path += '/' + self._ctx.default_lib_include_dir()

        libs_flag = False
        ldflags_flag = False
        linkdeps_flag = False
        libs = []
        ldflags = []
        whole_archive_libs = []
        global warn_linkdeps_once
        for arg in self._args:
            if (isinstance(arg, syntax_tag.TagOutputPath)):
                output_path = arg.v()
            elif (isinstance(arg, syntax_tag.TagHeaderOutputPath)):
                header_output_path = arg.v()
            elif (isinstance(arg, syntax_tag.TagHeaderFiles)):
                self._header_files.extend(arg.v())
            else:
                continue

        if (not warn_linkdeps_once):
            #self._ctx.log().log_warning('SharedLibrary links no dep libs: deprecated, specify SharedLibrary($lib,LinkDeps(False))')
            warn_linkdeps_once = True
        
        if (not libs_flag):
            libs = self._ctx.libraries().v()
        if (not ldflags_flag):
            ldflags = self._ctx.link_flags().v() 

        libs_s = self._line_delim.join(libs)
        ldflags_s = self._line_delim.join(ldflags)
        objs_s = self._line_delim.join(self._sources_outfiles)
        depends_libs_s = self._depends_libs_s
        cpflags_s = '-f' #copy选项.
        if (self._ctx.copy_using_hard_link()):
            cpflags_s += ' --link'

        cc = self._get_compiler_bin_by_src(self._sources_infiles)
        commands = []
        if (linkdeps_flag == False):
            cmd = '%(cc)s -shared %(objs_s)s -Xlinker "-(" %(libs_s)s %(ldflags_s)s -Xlinker "-)" -o %(target)s' % (locals())
        else:
            if (whole_archive_libs):
                whole_archive_libs_s = self._line_delim.join(whole_archive_libs)
                Target._move_libs_from_depends(self, whole_archive_libs)
                #self._depends_libs_s changed after _MoveLibsFromDepends
                depends_libs_s = self._depends_libs_s
                cmd = '%(cc)s -shared %(objs_s)s -Xlinker "-(" --whole-archive %(whole_archive_libs_s)s --no-whole-archive %(libs_s)s %(depends_libs_s)s %(ldflags_s)s -Xlinker "-)" -o %(target)s'%(locals())
            else:
                cmd = '%(cc)s -shared %(objs_s)s -Xlinker "-(" %(libs_s)s %(depends_libs_s)s %(ldflags_s)s -Xlinker "-)" -o %(target)s' % (locals())

        commands.append(cmd)
        
        if (output_path):
            commands.append("mkdir -p %(output_path)s" % (locals()))
            commands.append("cp %(cpflags_s)s %(target)s %(output_path)s" % (locals()))
        if (header_output_path and self._header_files):
            commands.append("mkdir -p %(header_output_path)s" % (locals()))
            commands.append("cp %s %s %s" % (cpflags_s,
                                           ' '.join(self._header_files),
                                           header_output_path))
        r = (target,
           self._line_delim.join(self._prefixes +
                                 self._sources_outfiles +
                                 self._header_files +
                                 libs),
           commands)
        self._make_lines.append(r)
       
        # Clean Commands.
        self._clean_files.append(target)
        if (output_path):
            self._clean_files.append(
                os.path.join(output_path,
                             os.path.basename(target)))
        if (header_output_path):
            self._clean_files.extend(
                map(lambda x:os.path.join(header_output_path,
                                          os.path.basename(x)),
                    self._header_files))


