### buildmake
采用python编写的一个用于快速构建c/c++项目编译环境的工具。具体功能如下:
+ 支持快速生成一个c/c++项目的Makefile文件
+ 支持快速构建大中型c/c++项目的完整编译环境，包括各种第三方lib库的依赖
+ 能够与github或者其它git管理平台有机结合，灵活的支持大中型项目的编译依赖管理，包括依赖库的下载，自动更新，指定特定的git分支依赖等
+ 支持二进制可执行文件，静态链接库，动态链接库等各种形式的源码发布

### Requirement
+ linux平台下的c/c++项目 
+ 需要安装python 2.x环境

### Tutorial
#### Configure
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

# Output is:
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
#### usage
```shell

# Step1 Generate a default BUILDMAKE file
buildmake -G

# Step2 Modify the buildmake as needed
vim BUILDMAKE

# Step3 Generate Makefile using appropriate options
buildmake -UB

# Step4 Exec make
make

```

### More detailed documentation and tutorials
https://www.str2num.com/opensource/buildmake/



