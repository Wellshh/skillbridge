
This directory contains an example of the Allegro Skill Plugin capability.
Plugin capability is the ability to bind additional functionality via
a compiled shared library/Dll using C or C++.

See the axlDllDoc in the Allegro Skill Reference manual.

Contains:
	ashplugin.il: Example skill code that loads and accesses an 
		shared library/DLl.
	axlecho_plugin.c: Source code that implements plugin functionality.
	Makefile - gnumake compitible Makefile
	axldll.vcproj - Visual.NET project file


Basic compiler requirements are;
	(This is a summary, detail infomation can be found in the
	 Allegro platform requirements documentation.)


  Windows:
	Requires at least Visual.NET 2003

  UNIX/Linux:
  	gnumake is a requirement

  Solaris:
	Sun Compiler at least Workshop 10
		gnumake ARCH=sun4v

  Linux
	Allegro supplied gnu compiler (see 
	   <cdsroot>/tools/<mainwin>/misc/linux/gcc/fixed3/bin
		gnumake ARCH=linux

  AIX:
	Visual Age compiler, at least 7.0
		gnumake ARCH=ibmrs
