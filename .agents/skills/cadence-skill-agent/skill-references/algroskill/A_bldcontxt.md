### Requirements

#### Description

You must have a Skill developers license and the cdsmps program. The cdsmps program is part of every standard Allegro release. When running cdsmps on Linux run with the "cdsmps -64only" method. Only Windows run the cdsmps64 program.

Since Allegro products are now 64bit binaries, you need to build 64bit contexts.

You cannot use context files built in earlier releases that had 32bit binaries, such as 16.6, with Allegro releases starting with 17.x

### Cautions

#### Description

Most Skill code can be built into contexts. However, there are several potential problems that you should keep in mind when writing code. A complete discussion of these issues can be found in Chapter 10 of the Skill Language User Guide.

Note: Cadence recommends that you prefix your Skill functions with upper case prefixes. This minimizes the chance of naming collisions with Cadence Skill functions that use lower case prefixes.

Additionally, autoload contexts have some additional cautions. Please adhere to the following guidelines:

### File B1

#### Description

Helper Skill code to load all Skill files in a directory.

`;-----------------------------------------------------------`

`;startup.il`

`foreach(file rexMatchList(".*\\.il$" getDirFiles("."))`

`; don't load myself -- bad idea`

`when( nequal(file, "startup.il")`

`load(file)`

`)`

`)`

`;-----------------------------------------------------------`

### File S1

#### Description

buildcxt csh script to for building standard contexts.

`#!/bin/csh -f`

`# This builds a standard context see README.cxt for other set-up requirements`

`if ($#argv != 1) then`

`echo "Usage: $0 <context name>"`

`echo "Assumes that a startup.il file exists in current directory"`

`echo " this file is used to specify the loading of other skill files"`

`exit 1`

`endif`

`set theContext = $argv[1]`

`if (!(-e startup.il)) then`

`echo "ERROR: Can't find standard.il file"`

`exit 1`

`endif`

`cdsmps -64only << EOF`

`(setSkillPath ".")`

`(setContext "$theContext")`

`(load "startup.il")`

`(defInitProc "$theContext" '${theContext})`

`(saveContext "$theContext.cxt")`

`(exit)`

`EOF`

`echo ""`

`echo ""`

`echo ""`

`echo "Context will be found $theContext.cxt"`

`echo ""`

`exit 0`

### File A1

#### Description

cxtFuncs.il Skill helper program to build autoload contexts.

`;(`

`;---------------------------------------------------`

`; EXPORTED FUNCTIONS:`

`; buildContext : used to build a context`

`; getContext : used to load a context`

`;`

`; Mods -- fxf 8/25/95 to support local building of contextes`

`;---------------------------------------------------`

`;`

`; Constants`

`; ilcDftSourceFileDir : directory name where Skill source`

`; files reside`

`; ilcDftDeliveryDir : directory name where delivered`

`; context files are saved.`

`; (fxf) may be overridden before calling`

`;---------------------------------------------------`

`unless(boundp('ilcDftSourceFileDir) ilcDftSourceFileDir = "pvt/etc/context")`

`unless(boundp('ilcDftDeliveryDir) ilcDftDeliveryDir = "etc/context")`

`(defun _parsePath (path)`

`(let (lpath)`

`(cond (path`

`lpath = parseString(path "/")`

`(while (!rindex(car(lpath) "tools")) lpath = cdr(lpath))`

`buildString(lpath "/")`

`)`

`(t nil))`

`))`

`_stacktrace = 10`

`setSkillPath(strcat(". ~ " prependInstallPath("local")))`

`(cond ((getd 'dbSetPath) (dbSetPath ". ~")))`

`;`

`; loadCxt --`

`; Load a context and call its init function.`

`;`

`(defun loadCxt (cxt cxtPath)`

`(let ((f (strcat (cdsGetInstPath cxtPath) "/" cxt ".cxt")))`

`(cond`

`((null (isFile f)) nil)`

`((null (loadContext f))`

`(printf "load of context %s failed\n" cxt))`

`((null (callInitProc cxt))`

`(printf "init proc of context %s failed\n" cxt))`

`(t (printf "Loading context %s\n" cxt))`

`)`

`)`

`)`

`;`

`; buildContext --`

`; Build a new context, even if one exists.`

`;`

`(defun buildContext (cxt @rest targs)`

`(let (cxtPath srcPath fullCxtPath)`

`cxtPath = ilcDftDeliveryDir`

`(setq srcPath (strcat ilcDftSourceFileDir "/" cxt))`

`;; <fxf>: doesn't allow local contextes so use above 2 lines`

`;;(cond ((car targs) (setq cxtPath (car targs)))`

`;;((setq cxtPath (_parsePath (_iliGetActualCxtPath cxt))) t)`

`;;(t (setq cxtPath ilcDftDeliveryDir)))`

`;;(cond ((cadr targs) (setq srcPath (cadr targs)))`

`;;((setq srcPath (_parsePath (_iliGetActualSrcPath cxt))) t)`

`;;(t (setq srcPath (strcat ilcDftSourceFileDir "/" cxt))))`

`fullCxtPath = cdsGetInstPath(cxtPath)`

`(deleteFile (strcat fullCxtPath "/" cxt ".cxt"))`

`(deleteFile (strcat fullCxtPath "/" cxt ".al"))`

`(deleteFile (strcat fullCxtPath "/" cxt ".ini"))`

`(updateContext cxt cxtPath srcPath)`

`(updateAutoloads cxt cxtPath srcPath)`

`))`

`;`

`; updateContext --`

`; If there is source and it is newer than the context,`

`; then build a new context. Otherwise if there is no source`

`; use the existing context.`

`;`

`(defun updateContext (cxt cxtPath srcPath)`

`(cond ((isDir (cdsGetInstPath srcPath)) (makeCapContext cxt cxtPath srcPath))`

`((loadCxt cxt cxtPath) t)`

`(t (printf "Can't find context %s\n" cxt )))`

`)`

`(defun updateAutoloads (cxt cxtPath srcPath)`

`(let ((afile (sprintf nil "%s/%s.al" (cdsGetInstPath srcPath) cxt))`

`(ifile (sprintf nil "%s/%s.ini" (cdsGetInstPath srcPath) cxt)))`

`(cond ((isFile ifile) (system (sprintf nil "cp %s %s" ifile (cdsGetInstPath cxtPath))))`

`((isFile afile) (system (sprintf nil "cp %s %s" afile (cdsGetInstPath cxtPath))))`

`(t t))`

`))`

`;`

`; getContext --`

`; Load the context if it exists, otherwise build it.`

`;`

`(defun getContext (cxt @rest targs)`

`(let (cxtPath srcPath)`

`(cond ((car targs) (setq cxtPath (car targs)))`

`((setq cxtPath (_parsePath (_iliGetActualCxtPath cxt))) t)`

`(t (setq cxtPath ilcDftDeliveryDir)))`

`(cond ((cadr targs) (setq srcPath (cadr targs)))`

`((setq srcPath (_parsePath (_iliGetActualSrcPath cxt))) t)`

`(t (setq srcPath (strcat ilcDftSourceFileDir "/" cxt))))`

`(cond ((loadCxt cxt cxtPath) t)`

`((isDir cxt (cdsGetInstPath srcPath))`

`(makeCapContext cxt cxtPath srcPath))`

`(t (printf "Can't get context %s\n" cxt)`

`))`

`))`

`(sstatus trapDefs ilcDftDeliveryDir)`

`(sstatus lazyComp nil)`

### File A2

#### Description

buildautocxt csh script to build autoload contexts.

`#!/bin/csh -f`

`# This builds a context see README.cxt for other set-up requirements`

`if ($#argv != 1) then`

`echo "Usage: $0 <context name>"`

`exit 1`

`endif`

`set theContext = $argv[1]`

`if (!(-e pvt/etc/context/$argv[1])) then`

`echo "pvt/etc/context/$argv[1] does not exit"`

`exit 1`

`endif`

`if (!(-e etc/context)) then`

`mkdir -p etc/context`

`endif`

`cdsmps -64only -ilLoadIL cxtFuncs.il << EOF`

`(getContext "skillCore")`

`(setSkillPath ".")`

`(cdsSetInstPath ".")`

`buildContext "$theContext"`

`exit`

`EOF`

`echo ""`

`echo ""`

`echo ""`

`echo "Context files will be found at etc/context/$theContext.*"`

`echo ""`

`exit 0`

Return to top of page
 
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
Copyright © 2016, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

