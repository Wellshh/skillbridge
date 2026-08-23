### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

14
==

Environment Functions
=====================

### cdsGetInstPath

`cdsGetInstPath( [ t_name ] ) => t_string`

#### Description

Returns the absolute path of the Cadence installation directoryas a string. `cdsGetInstPath` is for the cds root hierarchy and is meant to be used by all Virtuoso and non-Virtuoso applications.

**Note:** Starting from version SKILL06.50 and beyond, the following calls are equivalent:

`cdsGetInstPath("tools/[subDirPath]")`

`cdsGetToolsPath("[subDirPath]")`

#### Arguments

|  |
| --- | ---
| `t_name` | The optional argument`t_name` is appended to the end of the cds root path with a directory separator if necessary.
#### Value Returned

|  |
| --- | ---
| `t_string` | Returns the installation path as a string.
#### Example

`cdsGetInstPath() => "/cds/99.02/latest.il"`

`cdsGetInstPath("tools") =>"/cds/99.02/latest.il/tools"`

#### Reference

`cdsGetToolsPath, , getSkillPath, ,`

### cdsGetToolsPath

`cdsGetToolsPath( [ t_subDirPath ] ) => t_cdsToolsPath`

#### Description

Returns the absolute path of the Cadence installation`tools` directory as a string after resolving the `tools` directory appropriately. This function is provided for multiple platform support mainly to simplify access to a common Cadence installation hierarchy for all Unix platforms.

**Note:** SKILL code from version 6.5 and beyond should use`cdsGetToolsPath("[``subDirPath``]")` instead of `cdsGetInstPath("tools/``[``subDirPath``]")`.

#### Arguments

|  |
| --- | ---
| `t_subDirPath` | The optional argument`t_subDirPath` is appended to the end of the Cadence installation `tools` directory path with a directory separator if necessary.
#### Value Returned

|  |
| --- | ---
| `t_cdsToolsPath` | Returns the absolute path of the Cadence installation`tools` directory as a string.
#### Example

`cdsGetToolsPath() => "/cds/06.01/latest.il/tools"`

`cdsGetToolsPath("") => "/cds/06.01/latest.il/tools/"`

`cdsGetToolsPath("bin") => "/cds/06.01/latest.il/tools/bin"`

#### Reference

, ,[getSkillPath](#1039461 "Environment Functions"), ,

### cdsPlat

`cdsPlat()=> t_plat`

#### Description

Returns the platform for the Cadence software that is currently running; one of the followingstrings: `sun4v`, `sol86`, `hppa`, `ibmrs`, `wint`, `lnx86`, or `lni64`.

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `t_plat` | The platform upon which the Cadence software is running. Oneof the following strings:
|  |
| --- | ---
|  | `"sun4v"``"sol86"``"hppa"``"ibmrs"``"wint"``"lnx86"``"lni64"`
#### Example

`system("uname")`

`-> SunOS`

`0`

`cdsPlat()`

-> "sun4v"

### changeWorkingDir

`changeWorkingDir( [ S_name ] ) => t`

#### Description

Changes the working directory to`S_name`.

Different error messages are printed if the operation fails because the directory does not existor you do not have search (execute) permission.

* ***Use this function with care: if "." is either part of the SKILL path or thelibraryPath, changing the working directory can affect the visibility of SKILL files or design data.***

#### Arguments

|  |
| --- | ---
| `S_name` | Name of the working directory you want to use. Can be specifiedwith either a relative or absolute path. If you supply a relative path, the shell environment is used to search for the directory, not the SKILL path.
#### Value Returned

|  |
| --- | ---
| `t` | Returns `t` if the function executes successfully. Prints an error message if the directory you tried to change to does not exist. Prints a permission denied message if you do not have search permission.
#### Example

Assume there is a directory`/usr5/design/cpu` with proper permission and there is no `test` directory under `/usr5/design/cpu`.

`changeWorkingDir( "/usr5/design/cpu") => tchangeWorkingDir( "test")`

Signals an error about a non-existent directory.

#### Reference

### cputime

`cputime( ) => x_result`

#### Description

Returns the total amount of CPU time (user plus system) used in units of 60ths of a second.

#### Value Returned

|  |
| --- | ---
| `x_result` | CPU time in 60ths of a second.
#### Example

cputime()             => 8
integerp( cputime() ) => t
floatp( cputime() )   => nil

### createDir

`createDir( S_name ) => t | nil`

#### Description

Creates a directory.

The directory name can be specified with either an absolute or relative path; the SKILL pathis used in the latter case. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Name of the directory you are creating.
#### Value Returned

|  |
| --- | ---
| `t` | If the directory is created.
|  |
| --- | ---
| `nil` | If the directory is not created because it already exists.
|  |
| --- | ---
|  | If the directory cannot be created because you do not havepermission to update the parent directory, or a parent directory does not exist, an error is signaled.
#### Example

```
createDir("/usr/tmp/test") => tcreateDir("/usr/tmp/test") => nil   ;Directory already exists.
```

#### Reference

, ,

### createDirHier

`createDirHier( t_pathName ) => t/nil`

#### Description

Creates all directories specified in the given SKILL path that do not already exist

The permissions associated with new directories are subject to the file creation mask onsystems supporting that concept. If the directory with the specified name already exists, `nil` is returned. The directory names in the given SKILL path can be specified with either absolute or relative; the SKILL path is used in the latter case.

**Note:** A path that is anchored to the current directory, for example, ./, ../, or ../../.., etc., is notconsidered as a relative path.

#### Arguments

|  |
| --- | ---
| `t_pathName` | Specifies a (hierarchical) SKILL path consisting of all thedirectories that need to be created
#### Value Returned

|  |
| --- | ---
| `t` | Returns`t` if all the directories specified in the given SKILL path are created
|  |
| --- | ---
| `nil` | Returns`nil` if a directory with the same name already exists or an incorrect SKILL path is specified
|  |
| --- | ---
|  | If the directory cannot be created because you do not havepermission to update the parent directory, or a parent directory does not exist, an error is signaled.
#### Example

createDirHier("./dir1/dir2"); creates the directories /dir1/dir2/ as specified inthe given SKILL path

### csh

`csh( [ t_command ] ) => t | nil`

#### Description

Starts the UNIX C-shell as a child process to execute a command string.

Identical to the`sh` function, but invokes the C-shell (`csh`) rather than the Bourne-shell (`sh`).

#### Arguments

|  |
| --- | ---
| `t_command` | Command string to execute.
#### Value Returned

|  |
| --- | ---
| `t` | If the exit status of executing the given shell command is 0.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`csh( "mkdir ~/tmp" ) => t`

Creates a sub-directory called*tmp* in your home directory.

#### Reference

[sh, shell](#1039889 "Environment Functions")

### deleteDir

`deleteDir( S_name ) => t | nil`

#### Description

Deletes a directory.

The directory name can be specified with either an absolute or relative path; the SKILL pathis used in the latter case. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Name of directory to delete.
#### Value Returned

|  |
| --- | ---
| `t` | If the directory has been successfully deleted.
|  |
| --- | ---
| `nil` | If the directory does not exist.
|  |
| --- | ---
|  | Signals an error if you do not have permission to delete adirectory or the directory you want to delete is not empty.
#### Example

```
createDir("/usr/tmp/test") => tdeleteDir("/usr/tmp/test") => tdeleteDir("/usr/bin")
```

Signals an error about permission violation.

`deleteDir("~")`

Assuming there are some files in`~`, signals an error that the directory is not empty.

#### Reference

`createDir, deleteFile, ,`

### deleteFile

`deleteFile( S_name ) => t | nil`

#### Description

Deletes a file.

The file name can be specified with either an absolute or relative path; the SKILL path is usedin the latter case. If a symbolic link is passed in as the argument, it is the link itself, not the file or directory referenced by the link, that gets removed. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Name of file you want to delete.
#### Value Returned

|  |
| --- | ---
| `t` | File is successfully deleted.
|  |
| --- | ---
| `nil` | File does not exist.
|  |
| --- | ---
|  | Signals an error if you do not have permission to delete a file.
#### Example

`deleteFile("~/test/out.1") => t`

If the named file exists and is deleted.

`deleteFile("~/test/out.2") => nil`

If the named file does not exist.

`deleteFile("/bin/ls")`

If you do not have write permission for`/bin`, signals an error about permission violation.

#### Reference

, ,

### exit

`exit( [ x_status ] ) => nil`

#### Description

Causes SKILL to exit with a given process status (defaults to 0), whether in interactive orbatch mode.

Use`exit` functions to customize the behavior of an exit call. Sometimes you might like to do certain cleanup actions before exiting SKILL. You can do this by registering `exit`-before and/or `exit`-after functions.

An`exit`-before function is called before `exit` does anything, and an `exit`-after function is called after `exit` has performed its bookkeeping tasks and just before it returns control to the operating system. The user-defined exit functions do not take any arguments.

To give you even more control, an`exit`-before function can return the atom `ignoreExit` to abort the exit call totally. When `exit` is called, first all the registered `exit`-before functions are called in the reverse order of registration. If any of them returns the special atom `ignoreExit`, the exit request is aborted and it returns `nil` to the caller.

After the`exit`-before functions are called:

* Some bookkeeping tasks are called.

* All the registered`exit`-after functions are called in the reverse order of their registration.

* Finally the process exits to the operating system.

For compatibility with earlier versions of SKILL, you can still define the functions named`exitbefore` and `exitafter` as one of the exit functions. They are treated as the first registered exit functions (the last to be called). To avoid confusing the system setup, do not use these names for other purposes.

#### Arguments

|  |
| --- | ---
| `x_status` | Process exit status; defaults to 0.
#### Value Returned

|  |
| --- | ---
| `nil` | The exit request is aborted. Otherwise there is no return valuebecause the process exits.
#### Example

```
(defun myExitBefore ()    (if (closeMyDataBase)        t                ; if OK in closeMyDataBase then exit        'ignoreExit))    ; otherwise we want to abort exit
```

```
regExitBefore('myExitBefore)=> t                     ; exit function is registered
```

`exit()`

Depending on the result from calling`closeMyDataBase`, the system either exits the application (after asking for confirmation if running in graphic mode) or aborts the exit and returns `nil`.

### getCurrentTime

`getCurrentTime( ) => t_timeString`

#### Description

Returns a string representation of the current time.

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `t_timeString` | Current time in the form of a string. The format of the string is`month day hour:minute:second year`.
#### Example

`getCurrentTime( )=> "Jan 26 18:15:18 1994"`

This format is also used by the`compareTime` function.

### getInstallPath

`getInstallPath( ) => l_string`

#### Description

Returns the absolute path of the Cadence DFII installation directory where the DFII productsare installed on your system as a list of a single string.

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `l_string` | Returns the installation path as a list of a single string.
#### Example

`getInstallPath() => ("/usr5/cds/5.0")`

#### Reference

[getSkillPath](#1039461 "Environment Functions"), , ,

### getLogin

`getLogin( ) => t_loginName`

#### Description

Returns the user's login name as

a string.

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `t_loginName` | Returns the user's login name as a string.
#### Example

`getLogin=> "fred"`

### getPrompts

`getPrompts( ) => l_strings`

#### Description

Returns the current values of the first level and second level prompt text strings, respectively.

The first prompt text string is the first level prompt that represents the topmost top-levelprompt, while the second one indicates the second level prompt which is used whenever a nested top-level is entered.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `l_strings` | The current values of the first level and second level prompt textstrings. The result is a list where the first element is the first level prompt and the second element is the second level prompt specified by `setPrompts`.
#### Example

`skill> getPrompts()("> " "<%d> ")`

`CIW> getPrompts()("> " "> ")`

Default prompts for the SKILL interpreter and CIW, respectively.

#### Reference

### getShellEnvVar

`getShellEnvVar( t_UnixShellVariableName ) => t_value | nil`

#### Description

Returns the value of a UNIX environment variable, if it has been set.

#### Arguments

|  |
| --- | ---
| t\_UnixShellVariableName  Name of the UNIX shell environment variable. |
#### Value Returned

|  |
| --- | ---
| t\_value | Value of named UNIX environment variable.
|  |
| --- | ---
| nil | No environment variable with the given name has been set.
#### Example

`getShellEnvVar("SHELL") => "/bin/csh"`

Returns the current value of theSHELL environment variable.

### getSkillPath

`getSkillPath( ) => l_strings | nil`

#### Description

Returns the current SKILL path.

The SKILL path is used in resolving relative paths for some SKILL functions. See["/O and File Handling"](../sklanguser/chap7.md) in the *Cadence SKILL Language User Guide*.

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `l_strings` | Directory paths from the currentSKILL path setting. The result is a list where each element is a path component as specified by `setSkillPath`.
|  |
| --- | ---
| `nil` | The last call to`setSkillPath` gave `nil` as its argument.
#### Example

```
setSkillPath('("." "~" "~/cpu/test1")) => ("~/cpu/test1")getSkillPath() => ("." "~" "~/cpu/test1")
```

The example below shows how to add a directory to the beginning of your search path(assuming a directory "`~/lib`").

```
setSkillPath(cons("~/lib" getSkillPath())) => ("~/lib" "~/cpu/test1")getSkillPath() => ("~/lib" "." "~" "~/cpu/test1")
```

### getTempDir

`getTempDir( ) => t_TempDir`

#### Description

Returns the system temp directory as a string.

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `t_TempDir` | The name of your current temp directory.
#### Example

getTempDir() => "/tmp"

### getWorkingDir

`getWorkingDir( ) => t_currentDir`

#### Description

Returns the current working directory as a string.

The result is put into a`~/prefixed` form if possible by testing for commonality with the current user's home directory. For example, `~/test` would be returned in preference to `/``usr/mnt/user1/test`*,* assuming that the home directory for `user1`is`/usr/mnt/user1` and the current working directory is`/usr1/mnt/user1/test`.

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `t_currentDir` | The name of your current working directory.
#### Example

`getWorkingDir() => "~/project/cpu/layout"`

#### Reference

### isDir

`isDir( S_name [ tl_path ] ) => t | nil`

#### Description

Checks if a path exists and if it is a directory name.

When`S_name` is a relative path, the current SKILL path is used if it's non-`nil`. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Path you want to check.
|  |
| --- | ---
| `tl_path` | List of paths that overrides the SKILL path.
#### Value Returned

|  |
| --- | ---
| `t` | The name exists and it is the name of a directory.
|  |
| --- | ---
| `nil` | The name exists and is not the name of a directory or`S_name` does not exist at all.
#### Example

`isDir("DACLib")  => tisDir("triadc")  => nil`

Assumes`DACLib` is a directory and `triadc` is a file under the current working directory and the SKILL path is `nil`.

`isDir("test")   => nil`

Result if `test` does not exist.

#### Reference

[getSkillPath](#1039461 "Environment Functions"), ,

### prependInstallPath

`prependInstallPath( S_name ) => t_string`

#### Description

Prepends the Cadence DFII installation path to a file or directory and returns the resultingpath as a string.

Possibly adds a slash (/) separator if needed. The typical use of this function is to computeone member of a list passed to `setSkillPath`.

#### Arguments

|  |
| --- | ---
| `S_name` | File or directory name to append to the installation path. If asymbol is given, its print name is used.
#### Value Returned

|  |
| --- | ---
| `t_string` | String formed by prepending the installation path to theargument path.
#### Example

`getInstallPath() => ("/usr5/cds/4.2")`

`Assume this is your install path.`

`prependInstallPath( "etc/context" ) => "/usr5/cds/4.2/etc/context"`

A slash (/) is added.

`prependInstallPath( "/bin" ) => "/usr5/cds/4.2/bin"`

```
setSkillPath( list("." prependInstallPath("bin")                prependInstallPath("etc/context")) )=> nil
```

`getSkillPath()=> ("." "/usr5/cds/4.2/bin" "/usr5/cds/4.2/etc/context")`

#### Reference

,[getSkillPath](#1039461 "Environment Functions"),

### setShellEnvVar

`setShellEnvVar( t_varName_or_nameValuePair [t_varValue] ) => t | nil`

#### Description

Sets or updates the value of the UNIX environment variable.

#### Arguments

|  |
| --- | ---
| t\_varName\_or\_nameValuePair Environment variable name or assignment expression | (`<name>=<value>`)
|  |
| --- | ---
| t\_varValue | Value of the environment variable
#### Value Returned

|  |
| --- | ---
| `t` | If the shell environment variable was set.
|  |
| --- | ---
| `nil` | If the shell environment variable was not set.
#### Example 1

`setShellEnvVar("PWD=/tmp")    => t`

Sets the parent working directory to the`/tmp` directory.

`getShellEnvVar("PWD")         => "/tmp"`

Gets the parent working directory.

#### Example 2

`setShellEnvVar("TEST=/tmp")    => t`

Sets the Test directory to the`/tmp` directory.

`setShellEnvVar("TEST" "/home")    => t`

Sets the Test directory to the home directory.

`setShellEnvVar("TEST")    => nil`

`WARNING* setShellEnvVar: must have an equal sign to set a value - "TEST"`

Returns nil, as an equal to sign is required to set the value.

`setShellEnvVar("=/tmp")    => nil`

`*WARNING* setShellEnvVar: the argument should include a variable name - "=/tmp"`

Returns nil, as the argument does not have a variable name.

`setShellEnvVar("TEST = /tmp")    => nil`

```
*WARNING* setShellEnvVar: must not have a space before the equal sign - "TEST = /tmp
```

Returns nil, as the argument has a space before the equal to sign.

#### Reference

, ,[sh, shell](#1039889 "Environment Functions")

### setSkillPath

`setSkillPath( {tl_paths | nil }) => l_strings | nil`

#### Description

Sets the internalSKILL path used by some file-related functions in resolving relative path names.

You can specify the directory paths either in a single string, separated by spaces, or as a listof strings. The system tests the validity of each directory path as it puts the input into standard form. If all directory paths exist, it returns `nil`.

If any path does not exist, a list is returned in which each element is an invalid path. Note that

* The directories on the SKILL path are always searched for in the order you specified in`tl_paths`.

* Even if a path does not exist (and hence appears in the returned list) it remains on thenew SKILL path.

The use of the SKILL path in other file-related functions can be effectively disabled by calling`setSkillPath` with `nil` as the argument.

#### Arguments

|  |
| --- | ---
| `tl_paths` | Directory paths specified either in a single string or list of strings.
|  |
| --- | ---
| `nil` | Turns off the use of the SKILL path.
#### Value Returned

|  |
| --- | ---
| `l_strings` | List of directory paths that appear in the`tl_paths` argument but do not actually exist.
|  |
| --- | ---
| `nil` | If all directory paths exist.
#### Example

```
setSkillPath('("." "~" "~/cpu/test1"))=> nil                       ; If "~/cpu/test1" exists.=> ("~/cpu/test1")           ; If "~/cpu/test1" does not exist.
```

The same task can be done with the following call that puts all paths in one string.

`setSkillPath(". ~ ~/cpu/test1")`

#### Reference

[getSkillPath](#1039461 "Environment Functions"),

### sh, shell

`sh( [ t_command ] ) => t | nil shell( [ t_command ] ) => t | nil`

#### Description

Starts the UNIX Bourne shell`sh` as a child process to execute a command string.

If the`sh` function is called with no arguments, an interactive UNIX shell is invoked that prompts you for UNIX command input (available only in nongraphic applications).

#### Arguments

|  |
| --- | ---
| `t_command` | Command string.
#### Value Returned

|  |
| --- | ---
| `t` | If the exit status of executing the given shell command is 0.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`shell( rm /tmp/junk)`

Removes the`junk` file from the `/tmp` directory and returns `t` if it is removed successfully.

#### Reference

, ,[setShellEnvVar](#setShellEnvVar "Environment Functions")

### system

`system( t_command ) => x_result`

#### Description

Spawns a separate UNIX process to execute a command.

#### Arguments

|  |
| --- | ---
| `t_command` | Command to execute.
#### Value Returned

|  |
| --- | ---
| `x_result` | The return code caused by executing the given UNIX command.
#### Example

`system( "date" ) Wed Dec 14 15:14:53 PST 19940system( "daa" )sh: daa: not found1`

#### Reference

,[sh, shell](#1039889 "Environment Functions")

### unsetShellEnvVar

`unsetShellEnvVar( t_envVarName ) => t | nil`

#### Description

Removes an environment variable from the environment of the calling process. If theenvironment variable (`t_envVarName)` does not exist in the current environment, the environment is left unchanged.

#### Arguments

|  |
| --- | ---
| `t_envVarName` | A string representing the environment variable name.
#### Value Returned

|  |
| --- | ---
| `t` | The environment variable is successfully removed.
|  |
| --- | ---
| `nil` | The environment variable does not exist or there is an errorcondition.
#### Example

`setShellEnvVar("test=testValue")`

`=> t`

`getShellEnvVar("test")`

`=> "testValue"`

`unsetShellEnvVar("test")`

`=> t`

`getShellEnvVar("test")`

=> nil

### vi, vii, vil

`vi( [ S_fileName ] ) => t | nil`

#### Description

Edits a file using the`vi` editor. This is an `nlambda` function. Edits the named file using the *vi* editor, and optionally includes (`vii`) or loads (`vil`) the file into SKILL after exiting the editor. These functions are just variants of `ed`, `edi`, and `edl` with explicit request for using the `vi` editor.

#### Arguments

|  |
| --- | ---
| `S_fileName` | File to edit. If no argument is given, defaults to the previouslyedited file, or `temp.il`, if there is no previous file.
#### Value Returned

|  |
| --- | ---
| `t` | If the operation was successfully completed.
|  |
| --- | ---
| `nil` | If the file does not exit or there is an error condition.
#### Example

`vil( "test.il" )`

`vi()`

#### Reference

, , ,




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
