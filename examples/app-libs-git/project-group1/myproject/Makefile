#BUILDMAKE edit-mode: -*- Makefile -*-
####################64Bit Mode####################
ifeq ($(shell uname -m), x86_64)
CC=gcc
CXX=g++
CPPFLAGS=-D_GNU_SOURCE \
  -D__STDC_LIMIT_MACROS \
  -DVERSION=\"1.9.8.7\"
CFLAGS=-g \
  -pipe \
  -W \
  -Wall \
  -fPIC
CXXFLAGS=-g \
  -pipe \
  -W \
  -Wall \
  -fPIC
INCPATH=-I. \
  -I./include \
  -I./output \
  -I./output/include
DEP_INCPATH=-I../../test/buildmake-test-staticlib \
  -I../../test/buildmake-test-staticlib/include \
  -I../../test/buildmake-test-staticlib/output \
  -I../../test/buildmake-test-staticlib/output/include


#BUILDMAKE UUID
BUILDMAKE_MD5=88e8e3a138a9aeee6907b682a2ccca67  BUILDMAKE


.PHONY:all
all:buildmake_makefile_check myproject 
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mall[0m']"
	@echo "make all done"

PHONY:buildmake_makefile_check
buildmake_makefile_check:
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mbuildmake_makefile_check[0m']"
	#in case of error, update "Makefile" by "buildmake"
	@echo "$(BUILDMAKE_MD5)" > buildmake.md5
	@md5sum -c --status buildmake.md5
	@rm -f buildmake.md5

.PHONY:clean
clean:
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mclean[0m']"
	rm -rf myproject
	rm -rf ./output/bin/myproject
	rm -rf src/myproject_main.o

.PHONY:dist
dist:
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mdist[0m']"
	tar czvf output.tar.gz output
	@echo "make dist done"

.PHONY:distclean
distclean:clean
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mdistclean[0m']"
	rm -f output.tar.gz
	@echo "make distclean done"

.PHONY:love
love:
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mlove[0m']"
	@echo "make love done"

myproject:src/myproject_main.o
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mmyproject[0m']"
	$(CXX) src/myproject_main.o -Xlinker "-("  ../../test/buildmake-test-staticlib/libmath.a -lpthread \
  -lcrypto \
  -lrt -Xlinker "-)" -o myproject
	mkdir -p ./output/bin
	cp -f --link myproject ./output/bin

src/myproject_main.o:src/main.cpp
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40msrc/myproject_main.o[0m']"
	$(CXX) -c $(INCPATH) $(DEP_INCPATH) $(CPPFLAGS) $(CXXFLAGS)  -o src/myproject_main.o src/main.cpp

endif #ifeq ($(shell uname -m), x86_64)


