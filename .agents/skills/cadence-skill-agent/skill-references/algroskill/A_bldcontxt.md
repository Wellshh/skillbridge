### Allegro® User Guide: SKILL Reference Product Version 17.2-2016 April 2016

A
=

Building Contexts in Allegro
============================

Introduction
------------

A context via can be created by either of two methods - standard and autoload. Both methods substantially improve performance of Skill code loading. Even more benefits can accrue if you combine several Skill files into one context. The autoload method is a super-set of standard contexts and offers deferred context loading functionality. The autoload method is used by all Allegro provided contexts.

The standard contexts are much easier to build, are more evident to the user, and typically require more memory. The autoload contexts are much harder to build, but the system only loads the contexts upon demand. For a more complete discussion of the differences, see the section on Contexts in theSkill Language User Guide.

### Requirements

You must have a Skill developers license and the cdsmps program. The cdsmps program is part of every standard Allegro release. When running cdsmps on Linux run with the`"cdsmps -64only"` method. Only Windows run the cdsmps64 program.

Since Allegro products are now 64bit binaries, you need to build 64bit contexts.

You cannot use context files built in earlier releases that had 32bit binaries, such as 16.6, with Allegro releases starting with 17.x

### Cautions

Most Skill code can be built into contexts. However, there are several potential problems that you should keep in mind when writing code. A complete discussion of these issues can be found in Chapter 10 of theSkill Language User Guide.

**Note:** Cadence recommends that you prefix your Skill functions with upper case prefixes. This minimizes the chance of naming collisions with Cadence Skill functions that use lower case prefixes.

Additionally, autoload contexts have some additional cautions. Please adhere to the following guidelines:

#### Autoload Context Guidelines

* Files put into an autoload context should only contain variables and procedures (functions).

* Do not load other skill files. Have`startup.il` load them.

* Generally do not call`axlCmdRegister`, `axlReportRegister`, or `axlTriggerSet.`

* Do not do anything outside of a procedure - it will not work.

Building Standard Contexts
--------------------------

#### To build a standard context

* Create a directory that has all the Skill files to be built into the context.

* Add the`startup.il` file (see [File B1](#1035621 "Building Contexts in Allegro")).

* Create a Skill function with the same name as your context that registers your commands with the Allegro shell. This step is required in allegro\_designer if you wish to access your Skill code. Only one of these functions is permitted per context. The function name must be the same as the context name. This step is analogous to the`.ini` file in autoload contexts.

> Format:

> `(defun <ContextName> ()`

> `(axlCmdRegister "mycommand" '<MYSkillCommand> ?cmdType ....)`

> `.... other axlCmdRegister ..`

> `)`

> Example:

> `(defun MYTEST()`

> `(axlCmdRegister "mytest" 'MYTest ?cmdType "general")`

> `)`

* Run the`buildcxt <ContextName>` script (see [File S1](#1035633 "Building Contexts in Allegro")). This produces a single file named, `<ContextName>.cxt.`For example: `buildcxt MYTEST.`

> To load the context into allegro\_designer, issue the Allegro command`loadcontext <ContextName>`. In programs where the Skill type-in mode is available, the Skill functions `loadContext <contextName.cxt>` and `callInitProc <ContextName>` perform the same function.

> Example:

`Allegro > loadcontext MYTEST`

> Skill version:

`skill > (loadContext "MYTEST.txt")`

`skill > (callInitProc "MYTEST")`

Building Autoload Contexts
--------------------------

#### To build a context by the autoload method

* Create directory hierarchies:

> `./pvt/etc/context`

> `./etc/context`

* Under`./pvt/etc/context`, create a directory using your context name and populate it with your Skill files.

* Add a`startup.il` (see [File B1](#1035621 "Building Contexts in Allegro")) to the mix and stir well.

* Insure that the`cxtFuncs.il` (see [File A1](#1035672 "Building Contexts in Allegro")) is in the root directory.

* Run the`buildautocxt` (see [File A2](#1035803 "Building Contexts in Allegro")) UNIX command with your context name . For example: `buildautocxt <myContext>`.

* If the context build is successful, you will have 3 files in the`./etc/context` directory with your context name (`.aux, .cxt, .toc`).

* Add an optional fourth file with a`<myContext>.ini` that has your `axlCmdRegister`. If you do not wish to register your Skill commands as Allegro commands, you may skip this step. However, in allegro\_designer this is the only method for accessing your Skill code.

> Example:

`(axlCmdRegister "my_command" 'MYSkillFunction ?cmdType "interactive")`

* Take the four context files and add them to the directory`<cds_root>/share/pcb/etc/context`.

* Edit the`pcd` file in this directory for the product requiring the context.
  Names are:

> `allegro.pcd` All allegro\_layout (CBD) based products.
> `designer.pcd` allegro\_designer
> `apd.pcd` advanced\_package\_designer
> `floorplan.pcd` allegro\_si

> You need to add a line at the end of the file in the following format:

`<NAME>    <VERSION>    <CONTEXTS>`

> **Note:** Neither the NAME of VERSION is important. It is only used with the Skill function`printBlend`.

> Example:

`MYCONTEXT 1.0        MyContext`

Two environment Bourne variables help in debugging problems in this area. They are:

`CDS_DEBUG_CONTEXTS` file `/tmp/context.log` - context stats
`CDS_DEBUG_CXTINIT` file `/tmp/initCxt.log` - context init
 - also stderr init context print

Files with This Package
-----------------------

### File B1

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

`buildcxt csh` script to for building standard contexts.

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

`cxtFuncs.il` Skill helper program to build autoload contexts.

`;(`

`;---------------------------------------------------`

`; EXPORTED FUNCTIONS:`

`; buildContext : used to build a context`

`; getContext : used to load a context`

`;`

`;    Mods -- fxf 8/25/95 to support local building of contextes`

`;---------------------------------------------------`

`;`

`; Constants`

`; ilcDftSourceFileDir : directory name where Skill source`

`;          files reside`

`; ilcDftDeliveryDir : directory name where delivered`

`; context files are saved.`

`;    (fxf) may be overridden before calling`

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

`;    Load a context and call its init function.`

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

`;    Build a new context, even if one exists.`

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

`;    If there is source and it is newer than the context,`

`;    then build a new context. Otherwise if there is no source`

`;    use the existing context.`

`;`

`(defun updateContext (cxt cxtPath srcPath)`

`(cond ((isDir (cdsGetInstPath srcPath)) (makeCapContext cxt cxtPath srcPath))`

`((loadCxt cxt cxtPath) t)`

`(t (printf "Can't find context %s\n" cxt )))`

`)`

`(defun updateAutoloads (cxt cxtPath srcPath)`

`(let ((afile (sprintf nil "%s/%s.al" (cdsGetInstPath srcPath) cxt))`

`(ifile (sprintf nil "%s/%s.ini" (cdsGetInstPath srcPath) cxt)))`

```
(cond ((isFile ifile) (system (sprintf nil "cp %s %s" ifile (cdsGetInstPath cxtPath))))
```

```
((isFile afile) (system (sprintf nil "cp %s %s" afile (cdsGetInstPath cxtPath))))
```

`(t t))`

`))`

`;`

`; getContext --`

`;    Load the context if it exists, otherwise build it.`

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

`buildautocxt csh` script to build autoload contexts.

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




For support, see [Cadence Online Support](http://support.cadence.com) service.



Copyright © 2016, [Cadence Design Systems, Inc.](http://www.cadence.com)


All rights reserved.
