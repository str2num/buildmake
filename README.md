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

# 1. 生成一个默认的BUILDMAKE配置文件模板
buildmake -G

# 2. 根据实际需要修改模板中相应的编译选项
vim BUILDMAKE

# 3. 更新所有的第三方库依赖并编译
buildmake -UB

# 4. 生成Makefile文件
buildmake

# 5. 编译项目
make

```

### More detailed documentation and tutorials
https://buildmake.mydoc.io

### 更新记录

buildmake_1.4 2019-05-17
+  依赖模块可以指定特定的分支版本
+  fix构建完整编译环境时，依赖模块的依赖无法正常获取
+  支持第三方依赖模块自定义build.sh编译脚本，buildmake发现模块根目录下存在build.sh会优先执行sh build.sh

buildmake_1.1 2018-10-24
+  修复了_depends_incpaths_s为空的bug，这会导致在buildmake过程中，报依赖的第三方库的头文件无法找到的错误。

buildmake_1.0 2018-07-23
+ 第一个版本



