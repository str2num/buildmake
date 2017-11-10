#!/usr/bin/python
#encoding: UTF-8
#author: str2num

import sys
import string
import os
import hashlib

import bsubprocess

PYTHON_HIGH_VERSION = False
if (sys.hexversion > 0x020600F0):
    PYTHON_HIGH_VERSION = True

def exclude(s, exs):
    ns = []
    for x in s:
        if not x in exs:
            ns.append(x)
    return ns

def unique(s, func=lambda x:x):
    if (PYTHON_HIGH_VERSION):
        mask = set()
    else:
        import sets
        mask = sets.set()
    ns = []
    for x in s:
        key = func(x)
        if (not key in mask):
            mask.add(key)
            ns.append(x)
    return ns

def red_it(s):
    if (sys.__stderr__.isatty()):
        return "\033[1;31;40m%s\033[0m" % (s)
    else:
        return s

def green_it(s):
    if (sys.__stderr__.isatty()):
        return "\033[1;32;40m%s\033[0m" % (s)
    else:
        return s

def add_prefix_to_basename(x, prefix):
    (dirname, basename) = os.path.split(x)
    return os.path.join(dirname, '%s%s' % (prefix, basename))

def replace_file_ext_name(x, ext):
    (root, _) = os.path.splitext(x)
    return '%s%s' % (root, ext)

def call_command(cmd):
    p = bsubprocess.Popen('_BUILDMAKE_SUBPROCESS= %s' % (cmd),
            shell = True, bufsize = 0, stdin=bsubprocess.PIPE,
            stdout=bsubprocess.PIPE, stderr=bsubprocess.PIPE)
    (out, err) = p.communicate()
    return (p.returncode, out, err)

def shorten_word(s, threshold=80):
    s = ' '.join(string.split(s.replace('\\\n', ' ')))
    if (len(s) <= threshold):
        return s
    else:
        return s[:threshold/2] + ' ... ' + s[-threshold/2:]

def add_file_ext_name(x, ext):
    return '%s%s' % (x, ext)

def find_files_pred_recursive(p, recursive, pred):
    entries = os.listdir(p)
    files = []
    for e in entries:
        if (e in ('.', '..', '.git')):
            continue
        pe = os.path.join(p, e)
        if (os.path.isdir(pe)):
            if (recursive):
                files.extend(find_files_pred_recursive(pe, recursive, pred))
        elif (pred(pe)):
            files.append(os.path.normpath(pe))
    return files

def find_files_pred(p, recursive, pred):
    return find_files_pred_recursive(p, recursive, pred)

def find_files_exts(p, recursive, ext):
    return find_files_pred(p, recursive, lambda x:os.path.splitext(x)[1] in ext)


