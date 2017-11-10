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
  -I./deps/math/include
DEP_INCPATH=


#BUILDMAKE UUID
BUILDMAKE_MD5=1494ad3ce94156e36b51eb58598e3513  BUILDMAKE


.PHONY:all
all:buildmake_makefile_check app-libs-depends 
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
	rm -rf app-libs-depends
	rm -rf ./output/bin/app-libs-depends
	rm -rf src/app-libs-depends_main.o

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

app-libs-depends:src/app-libs-depends_main.o \
  ./deps/math/lib/libmath.a
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40mapp-libs-depends[0m']"
	$(CXX) src/app-libs-depends_main.o -Xlinker "-(" ./deps/math/lib/libmath.a  -lpthread \
  -lcrypto \
  -lrt -Xlinker "-)" -o app-libs-depends
	mkdir -p ./output/bin
	cp -f --link app-libs-depends ./output/bin

src/app-libs-depends_main.o:src/main.cpp \
  deps/math/include/math/math.h
	@echo "[[1;32;40mBUILDMAKE:BUILD[0m][Target:'[1;32;40msrc/app-libs-depends_main.o[0m']"
	$(CXX) -c $(INCPATH) $(DEP_INCPATH) $(CPPFLAGS) $(CXXFLAGS)  -o src/app-libs-depends_main.o src/main.cpp

endif #ifeq ($(shell uname -m), x86_64)


