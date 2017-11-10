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
  -I./output/include \
  -I./src
DEP_INCPATH=


#BUILDMAKE UUID
BUILDMAKE_MD5=5a9051f3cf914da09378f18798c7d1d7  BUILDMAKE


.PHONY:all
all:buildmake_makefile_check app-simple-glob 
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
	rm -rf app-simple-glob
	rm -rf ./output/bin/app-simple-glob
	rm -rf src/app-simple-glob_main.o
	rm -rf src/math/app-simple-glob_math.o

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

app-simple-glob:src/app-simple-glob_main.o \
  src/math/app-simple-glob_math.o
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mapp-simple-glob[0m']"
	$(CXX) src/app-simple-glob_main.o \
  src/math/app-simple-glob_math.o -Xlinker "-("   -lpthread \
  -lcrypto \
  -lrt -Xlinker "-)" -o app-simple-glob
	mkdir -p ./output/bin
	cp -f --link app-simple-glob ./output/bin

src/app-simple-glob_main.o:src/main.cpp \
  src/math/math.h
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40msrc/app-simple-glob_main.o[0m']"
	$(CXX) -c $(INCPATH) $(DEP_INCPATH) $(CPPFLAGS) $(CXXFLAGS)  -o src/app-simple-glob_main.o src/main.cpp

src/math/app-simple-glob_math.o:src/math/math.cpp \
  src/math/math.h
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40msrc/math/app-simple-glob_math.o[0m']"
	$(CXX) -c $(INCPATH) $(DEP_INCPATH) $(CPPFLAGS) $(CXXFLAGS)  -o src/math/app-simple-glob_math.o src/math/math.cpp

endif #ifeq ($(shell uname -m), x86_64)


