#
# Builds axlecho_plugin shared library plugin for Solaris, AIX or Linux
#
# Requirements:
#	See Readme.txt
#
# To use
#	Solaris: gnumake ARCH=sun4v
#	Linux:   gnumake ARCH=linux
#	AIX:     gnumake ARCH=ibmrs
#

OBJS	      = axlecho_plugin.o

#-------------------------------------------------------
ifeq ($(ARCH),sun4v)
CC = cc
CFLAGS = -KPIC  -D_REENTRANT -mr -xCC
LDFLAGS = -G 
SLIBS         = -lm -lc
endif

#-------------------------------------------------------
ifeq ($(ARCH),linux)
CC = gcc
CFLAGS = -fPIC -march=i486
LDFLAGS = -fPIC -shared -Wl,-Bsymbolic
SLIBS         = -lm -lc
endif

#-------------------------------------------------------
ifeq ($(ARCH),ibmrs)
CC = cc
CFLAGS = -G -qcpluscmt 
LDFLAGS =    -brtl -G 
SLIBS    = -lm -lc_r 
endif


PROGRAM	 = axlecho_plugin.so

##### rules... ############################

all: $(PROGRAM)

$(PROGRAM): $(OBJS) 
	@echo Linking $(PROGRAM) ...
	$(CC) $(LDFLAGS) $(OBJS) $(SLIBS) -o $(PROGRAM)
	@echo "done"


clean:;		/bin/rm -f $(OBJS) $(PROGRAM) 
