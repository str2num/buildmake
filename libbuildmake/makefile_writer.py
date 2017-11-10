#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import bfunction

class MakefileWriter(object):
    def __init__(self):
        self._lines = []
        self.mfname = ''
    
    def all(self):
        r0 = ('.PHONY', 'all', [])
        r1_dep = 'buildmake_makefile_check '
        for exp in self._ctx.exports():
            r1_dep += '%s ' % (exp)
        r1 = ('all', r1_dep, ['@echo "make all done"'])
        # Check BUILDMAKE is newer than Makefile
        r2 = ('PHONY', 'buildmake_makefile_check', [])
        md5_file = 'buildmake.md5'
        commands = []
        commands.append('#in case of error, update "Makefile" by "buildmake"')
        commands.append('@echo "$(BUILDMAKE_MD5)" > %s' % md5_file)
        commands.append('@md5sum -c --status %s' % md5_file)
        commands.append('@rm -f %s' % md5_file)
        r3 = ('buildmake_makefile_check', '', commands)
        return (r0, r1, r2, r3)
    
    def clean(self):
        r0 = ('.PHONY', 'clean', [])
        commands = []
        for target in self._ctx.targets():
            for x in target.clean_files():
                commands.append('rm -rf %s' % (x)) 
            commands.extend(target.make_clean_lines())

        sources = bfunction.unique(self._ctx.sources(), lambda x:x.out_file())
        for source in sources:
            for x in source.clean_files():
                commands.append('rm -rf %s' % (x))

        r1 = ('clean', '', commands)
        return (r0, r1)
    
    def love(self):
        r0 = ('.PHONY', 'love', [])
        r1 = ('love', '', ['@echo "make love done"'])
        return (r0, r1)
    
    def dist(self):
        r0 = ('.PHONY', 'dist', [])
        commands = []
        directory = 'output'
        commands.append('tar czvf %(directory)s.tar.gz %(directory)s' % (locals()))
        commands.append('@echo "make dist done"')
        r1 = ('dist', '', commands)
        return (r0, r1)
    
    def dist_clean(self):
        r0 = ('.PHONY', 'distclean', [])
        commands = []
        directory = 'output'
        commands.append('rm -f %(directory)s.tar.gz' % (locals()))
        commands.append('@echo "make distclean done"')
        r1 = ('distclean', 'clean', commands)
        return (r0, r1)

    def collect(self, ctx):
        self._ctx = ctx
        self.mfname = 'Makefile'
        
        make_lines = []
        make_lines.extend(self.all())
        make_lines.extend(self.clean())
        make_lines.extend(self.dist())
        make_lines.extend(self.dist_clean()) 
        make_lines.extend(self.love())
        
        for target in self._ctx.targets():
            if (target.phony_mode()):
                r = ('.PHONY', target.target(), [])
                make_lines.append(r)
            make_lines.extend(target.make_lines())

        for source in self._ctx.sources():
            make_lines.extend(source.make_lines())

        make_lines = bfunction.unique(make_lines, lambda x:(x[0], x[1]))
         
        # Convert make_lines to Makefile format
        lines = []
        self._ctx.print_var(lines)
        for x in make_lines:
            (t, dep, cmds) = x
            lines.append('%s:%s' % (t, dep))
            if (not cmds):
                continue
            lines.append("\t@echo \"[%s][Target:'%s']\"" % (
                bfunction.green_it("BUILDMAKE:BUILD"),
                bfunction.green_it(t)))

            for cmd in cmds:
                lines.append('\t%s' % (cmd))
            lines.append('')

        # Operation for 32/64bit platform
        self._lines.append('####################%dBit Mode####################\n' % (ctx.bit()))
        self._lines.append('ifeq ($(shell uname -m), %s)\n' % ctx.cpu())
        self._lines.extend(map(lambda x:'%s\n' % x, lines))
        self._lines.append('endif #ifeq ($(shell uname -m), %s)\n\n\n' % (ctx.cpu()))
        
    def write(self):
        header_lines = ['#BUILDMAKE edit-mode: -*- Makefile -*-\n']
        fp = open('%s' % self.mfname, 'w')
        fp.writelines(header_lines + self._lines)
        fp.close()


