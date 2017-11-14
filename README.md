# buildmake
A simple and fast tools written in python for generating a c/c++ project's Makefile

# Tutorial
## Configure
```shell
# Create a dir
mkdir -p ~/tools
cd ~/tools

# Get buildmake
git clone https://github.com/str2num/buildmake.git

# Create alias
# Add line below to .bashrc
alias buildmake='~/tools/buildmake/buildmake'
source ~/.bashrc

# Check buildmake
buildmake -h

#Output:
The buildmake tool can automatically help users build a complete compilation
environment for C/C++ project, and generate Makefile. It will read the BUILDMAKE file
in the current directory, then build environment and generate Makefile. Users need to
provide this BUILDMAKE file. The default BUILDMAKE file can generate by buildmake
using -G option.

VERSION: 1.0
options:
    -h --help                  help infomation.
    -G --generate              generate default BUILDMAKE file
    -U --update environment    if the current project depends on another third libraries,
                               these libraries can be update from git.
    -B --build environment     building project, then generate the binary file
    -v --version               current version

```
