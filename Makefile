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
BUILDMAKE_MD5=80d5c12fd92ed6411cc08450bcfc8b4e  BUILDMAKE


.PHONY:all
all:buildmake_makefile_check libmath.a 
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
	rm -rf libmath.a
	rm -rf ./output/lib/libmath.a
	rm -rf ./output/include/math.h
	rm -rf src/math_math.o

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

libmath.a:src/math_math.o \
  ./src/math.h
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mlibmath.a[0m']"
	ar crs libmath.a src/math_math.o
	mkdir -p ./output/lib
	cp -f --link libmath.a ./output/lib
	mkdir -p ./output/include
	cp -f --link ./src/math.h ./output/include

src/math_math.o:src/math.cpp \
  src/math.h
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40msrc/math_math.o[0m']"
	$(CXX) -c $(INCPATH) $(DEP_INCPATH) $(CPPFLAGS) $(CXXFLAGS)  -o src/math_math.o src/math.cpp

endif #ifeq ($(shell uname -m), x86_64)


