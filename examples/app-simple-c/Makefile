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
BUILDMAKE_MD5=495264159637dabc2bbf9518cc892e8d  BUILDMAKE


.PHONY:all
all:buildmake_makefile_check app-simple-c 
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
	rm -rf app-simple-c
	rm -rf ./output/bin/app-simple-c
	rm -rf src/app-simple-c_main.o
	rm -rf src/app-simple-c_math.o

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

app-simple-c:src/app-simple-c_main.o \
  src/app-simple-c_math.o
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mapp-simple-c[0m']"
	$(CXX) src/app-simple-c_main.o \
  src/app-simple-c_math.o -Xlinker "-("   -lpthread \
  -lcrypto \
  -lrt -Xlinker "-)" -o app-simple-c
	mkdir -p ./output/bin
	cp -f --link app-simple-c ./output/bin

src/app-simple-c_main.o:src/main.c \
  src/math.h
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40msrc/app-simple-c_main.o[0m']"
	$(CC) -c $(INCPATH) $(DEP_INCPATH) $(CPPFLAGS) $(CFLAGS)  -o src/app-simple-c_main.o src/main.c

src/app-simple-c_math.o:src/math.c \
  src/math.h
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40msrc/app-simple-c_math.o[0m']"
	$(CC) -c $(INCPATH) $(DEP_INCPATH) $(CPPFLAGS) $(CFLAGS)  -o src/app-simple-c_math.o src/math.c

endif #ifeq ($(shell uname -m), x86_64)


