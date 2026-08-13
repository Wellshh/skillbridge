### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

7
=

I/O and File Handling
=====================

You can read about I/O and file handling topics in the following sections:

* [File System Interface](#1008204 "I/O and File Handling")

* [Ports](#1008398 "I/O and File Handling")

* [Output](#1008463 "I/O and File Handling")

* [Input](#1008613 "I/O and File Handling")

* [System-Related Functions](#1013686 "I/O and File Handling")

File System Interface
---------------------

All input and output in the Cadence® SKILL language is defined with respect to the UNIX file system. Writing I/O statements in SKILL requires an understanding of files, directories, and paths.

### Files

A file contains data, usually organized in multiple records, and has several attributes such asname, the date the file was created, the last time it was accessed, access permissions, and so on. A device is a file with special attributes.

### Directories

A directory has a name, just like a file, but it contains a list of other files. Directories can benested to as many levels as desired. A directory allows related files to be grouped together. Because of the thousands of files that can exist on a single disk, using directories helps to avoid chaos. Most network-wide file systems are dependent on directories.

### Directory Paths

Often, there are several directories you want to search in a particular order by specifying aset of directory paths. You can specify a file name in an absolute sense or in a relative sense.

The following description uses `path' as a generic term where either a file name or a directoryname can be used. However, because a directory under UNIX is just a special kind of file, file name is often used as a synonym for path.

#### Absolute Paths

You can specify the path with a slash character (`/`). When used as the first character of a name, it represents the system root directory. Intermediate levels of directories can use the slash character again as a separator.

#### Relative Paths

Any path that does not begin with a slash is a relative name.

If the path begins with a tilde followed by a slash (`~/`), the search path begins in your home directory.

If the tilde is followed by a name, the name is interpreted as a user name. That is,`~jones/``file1` specifies a file named `file1` in jones' home directory.

If the path begins with a period and a slash (`./`), the search begins with the current working directory.

If the file name begins with two periods and a slash (`../`), the search begins with the parent of the current working directory.

If you are using a function that refers to the SKILL path, refer to the following section.

### The SKILL Path

SKILL provides a flexible mechanism for using relative paths. An internal list of paths, referredto as the `SKILL path`, is used in many file-related functions.

#### Importance of the First Path Character

When a relative path that does not begin with`~` or `./` is given to a function, the paths in the SKILL path are used as directory names and prepended to the given path (with a `/` separator if needed) to form possible paths. The `setSkillPath` and `getSkillPath` functions access and change this internal SKILL path setup.

#### Path Order when the Same File Name Exists in Multiple Directories

The order of the paths onthe SKILL path is very important when the same file name is in multiple directories. If a file is opened for input or queried for status, all readable directories in the SKILL path are checked, in order, for the given file name. The first one found is taken to be the intended path.

#### Path Order when a File is Updated or Written for the First Time

The order of the paths is also very important when a file is updated or written for the first time.If you open an output file, all directory paths in the SKILL path are checked, in the order specified, for that file name. If found, the system overwrites the first updateable file in the list. If no updateable file is found, it places a new file of that name in the first writable directory.

#### Know Your SKILL Path

Having an implicit list of search paths provides a powerful shortcut in many situations, but itcan also be a source of possible confusion. When in doubt, double check the current setup of your SKILL path or set it to `nil`.

When you start your system, the SKILL path might be set to a default value. You can use the `setSkillPath`function to make sure it is set up correctly.

### Working with the SKILL Path

#### Setting the Internal SKILL Path (setSkillPath)

`setSkillPath` sets the internal SKILL path. You can specify the directory paths either as a string, where each alternate path is separated by spaces, or as a list of strings. The system tests the validity of each directory path as it puts the input into standard form.

* If all directory paths exist, it returns`nil`

* If any path does not exist, it returns a list in which each element is an invalid path

The paths onthe SKILL path are always searched for in the path order you specify. Even if a path does not exist (and hence appears in the returned list), it remains on the new SKILL path. The use of the SKILL path in other file-related functions can be effectively disabled by calling setSkillPath with nil as the argument.

```
setSkillPath('("." "~" "~/cpu/test1"))=> nil                       ; If "~/cpu/test1" exists.=> ("~/cpu/test1")           ; If "~/cpu/test1" does not exist.
```

The same task can be done with the following call that puts all paths in one string.

`setSkillPath(". ~ ~/cpu/test1")`

#### Finding the Current SKILL Path (getSkillPath)

`getSkillPath` returns directory paths from the current SKILL path setting. The result is a list where each element is a path component as specified by `setSkillPath`.

```
setSkillPath('("." "~" "~/cpu/test1"))=> nilgetSkillPath()=> ("." "~" "~/cpu/test1")
```

The example below shows how to add a directory to the beginning of your search path(assuming a directory "~/lib").

```
setSkillPath(cons("~/lib" getSkillPath()))=> nilgetSkillPath()=> ("~/lib" "." "~" "~/cpu/test1")
```

### Working with the Installation Path

#### Finding the Installation Path (getInstallPath)

`getInstallPath` returns the system installation path (that is, the root directory where the Cadence products are installed in your file system) as a list of a single string, where

* The path is always returned in absolute format

* The result is always a list of one string

> `getInstallPath( ) => ("/usr5/cds/4.2")`

#### Attaching the Installation Path to a Given Path (prependInstallPath)

`prependInstallPath` prepends the Cadence installation path to the given path (possibly adding a slash (/) separator if needed) and returns the resulting path as a string. The typical use of this function is to compute one member of a list passed to setSkillPath.

`getInstallPath()=> ("/usr5/cds/4.2")`

Assume this is your install path.

`prependInstallPath( "etc/context" )=> "/usr5/cds/4.2/etc/context"`

A slash (/) is added.

`prependInstallPath( "/bin" )=> "/usr5/cds/4.2/bin"`

```
setSkillPath( list("." prependInstallPath("bin")                 prependInstallPath("etc/context")) )=> nil
```

#### Finding the Root of the Hierarchy (cdsGetInstPath)

`getInstallPath` returns the root of the `dfII` hierarchy whereas `cdsGetInstPath` returns the root of the hierarchy. `cdsGetInstPath` is more general and is meant to be used by all `dfII` and non-`dfII` applications. For example:

```
getInstallPath() => ("/usr/mnt/hamilton/9304/tools/dfII")cdsGetInstPath() => "/usr/mnt/hamilton/9304"
```

### Checking File Status

#### Checking if a File Exists (isFile, isFileName)

`isFileName` checks if a file exists. The file name can be specified with either an absolute path or a relative path. In the latter case, the current SKILL path is used if it's not `nil`. Only the presence or absence of the name is checked. If found, the name can belong to either a file or a directory. `isFileName` differs from `isFile` in this regard.

`isFileName("myLib")=> t`

A directory is just a special kind of file.

`isFileName("triadc")=> tisFileName("triad1")=> nil`

Result if`triad1` is not in the current working directory.

`isFile` checks if a file exists. `isFile` is identical to `isFileName`, except that directories are not viewed as (regular) files. Uses the current SKILL path for relative paths.

`isFile( "triadc")=> t`

#### Checking if a Path Exists and if it is the Name of a Directory (isDir)

`isDir` checks if a path exists and if it is the name of a directory. When the path is a relative path, the current SKILL path is used if it's non-`nil`.

`isDir("myLib")       => tisDir("triadc")     => nil`

Assumes`myLib` is a directory and `triadc` is a file under the current working directory and the SKILL path is `nil`.

`isDir("test")=> nil`

Result if `test` does not exist.

#### Checking if You Have Permission to Read a File or List a Directory (isReadable)

`isReadable` checks if you have permission to read the file or list the directory you specify. Uses the current SKILL path for relative paths.

`isReadable("./") => t`

Result if current working directory is readable.

`isReadable("~/myLib")=> nil`

Result if`~/myLib` is not readable or does not exist.

#### Checking for Permission to Write a File or Update a Directory (isWritable)

`isWritable` checks if you have permission to write a file or update a directory that you specify. It uses the current SKILL path for relative paths.

```
isWritable("/tmp")                           => t isWritable("~/test/out.1")        => nil
```

Result if`out.1` does not exist or there is no write permission to it.

#### Checking for Permission to Execute a File or Search a Directory (isExecutable)

`isExecutable` checks if you have permission to execute a file or search a directory. A directory is executable if it allows you to name that directory as part of your UNIX path in searching files. It uses the current SKILL path for relative paths.

```
isExecutable("/bin/ls")               => t isExecutable("/usr/tmp")             => t isExecutable("attachFiles")      => nil
```

Result if`attachFiles` does not exist or is not executable.

#### Determining the Number of Bytes in a File (fileLength)

`fileLength` determines the number of bytes in a file. A directory is viewed just as a file in this case. `fileLength` uses the current SKILL path if a relative path is given.

`fileLength("/tmp")                              => 1024`

Return value is system-dependent.

`fileLength("~/test/out.1")         => 32157`

This examples assumes the file exists. If the file does not exist, you get an error message,such as

`*Error* fileLength: no such file or directory - "~/test/out.1"`

#### Getting Information About Open Files (numOpenFiles)

`numOpenFiles` returns the number of files that are open and the maximum number of files that a process can open. The numbers are returned as a two-element list.

`numOpenFiles()                                        => (6 64)`

Result is system-dependent.

```
f = infile("/dev/null")               => port:"/dev/null"numOpenFiles()                                        => (7 64)
```

One more file is open now.

#### Working with File Offsets (fileTell, fileSeek)

`fileTell` returns the current offset (from the beginning of the file) in bytes for the file opened on a port.

`fileSeek` sets the position for the next operation to perform on the file opened on a port. The position is specified in bytes. `fileSeek` takes three arguments. The first two are for port and for offset designated in number of bytes to move forward (or backward with a negative argument). The valid values for the third argument are

0  Offset from the beginning of the file
1  Offset from current position of file pointer
2  Offset from the end of the file.

Let the file`test.data` contain the single line of text:

`0123456789 test xyz`

```
p = infile("test.data")  => port:"test.data"fileTell(p)              => 0for(i 1 10 getc(p))      => t     Skip first 10 charactersfileTell(p)              => 10fscanf(p "%s" s)         => 1    s = "test" nowfileTell(p)              => 15
```

```
fileSeek(p 0 0)          => tfscanf(p "%d" x)         => 1    x = 123456789 nowfileSeek(p 6 1)          => tfscanf(p "%s" s)         => 1     s = "xyz" now
```

`fileSeek(p -12 2)        => tfscanf(p "%d" x)         => 1     x = 89 now`

### Working with Directories

#### Creating a Directory (createDir)

`createDir` creates a directory. The directory name can be specified with either an absolute or relative path; the SKILL path is used in the latter case. You get an error message if the directory cannot be created because you do not have permission to update the parent directory or a parent directory does not exist.

`createDir("/usr/tmp/test")        => tcreateDir("/usr/tmp/test")        => nil`

Directory already exists.

#### Creating Parent Directories (createDirHier)

`CreateDirHier` creates all directories specified in the given SKILL path that do not already exist. The directory names in the given SKILL path can be specified with either absolute or relative; the SKILL path is used in the latter case. A path that is anchored to the current directory, for example, ./, ../, or ../../.., etc., is not considered as a relative path.

The permissions associated with new directories are subject to the file creation mask onsystems supporting that concept. If the directory with the specified name already exists, nil is returned.

#### Deleting a Directory (deleteDir)

`deleteDir` deletes a directory. The directory name can be specified with either an absolute or relative path; the SKILL path is used in the latter case. You get an error message if you do not have permission to delete a directory or the directory you want to delete is not empty.

```
createDir("/usr/tmp/test")=> tdeleteDir("/usr/tmp/test")=> tdeleteDir("/usr/bin")
```

If you do not have permission to delete`/bin`, you get an error message about permission violation.

`deleteDir("~")`

Assuming there are some files in ~, you get an error message that the directory is not empty.

#### Deleting a File (deleteFile)

`deleteFile` deletes a file. The file name can be specified with either an absolute or relative path; the SKILL path is used in the latter case. If a symbolic link is passed in as the argument, it is the link itself, not the file or directory referenced by the link, that gets removed.

`deleteFile("~/test/out.1") => t`

If the file exists and is deleted.

`deleteFile("~/test/out.2")=> nil`

If the file does not exist.

`deleteFile("/bin/ls")`

If you do not have write permission for`/bin`, signals an error about permission violation.

#### Creating a Unique File Name (makeTempFileName)

`makeTempFileName` appends a string suffix to the last component of a path template such that the resultant composite string does not duplicate any existing file name. (That is, it checks that the file does not exist; the SKILL path is not used in this checking.)

Successive calls to`makeTempFileName` return different results `only if the first``name returned is actually used to create a file` in the same directory before a second call is made.

* The last component of the resultant path is guaranteed to be no more than 14 characters.The example below requests a "file" with 15 characters

> `makeTempFileName("/tmp/123456789123456")=> "/tmp/12345678a08717"`

* If the original template has a long last component, it is truncated from the end if needed

> `makeTempFileName("/tmp/123456789.123456")=> "/tmp/12345678a08717"`

* Any trailing Xs are removed from the template before the new string suffix is appended

You should follow the convention of placing temporary files in the`/tmp` directory on your system.

`d = makeTempFileName("/tmp/testXXXX") => "/tmp/testa00324"`

Trailing Xs are removed.

```
createDir(d)                                                                   => t
```

The name is used this time.

`makeTempFileName("/tmp/test")                      => "/tmp/testb00324"`

A new name is returned this time.

#### Listing the Names of All Files and Directories (getDirFiles)

`getDirFiles` lists the names of all files and directories (including . and ..) in a directory. Uses the current SKILL path for relative paths.

```
getDirFiles(car(getInstallPath())) =>("." ".." "bin" "cdsuser" "etc" "group" "include" "lib" "pvt""samples" "share" "test" "tools" "man" "local" )
```

#### Expanding the Name of a File to its Full Path (simplifyFilename)

`simplifyFilename` returns the fully expanded name of a file. Tilde expansion is performed, ./ and ../ are compressed, and redundant slashes are removed. Symbolic links are also resolved by default, unless the second (optional) argument `g_dontResolveLinks` is specified to non-nil. If the file you supply is not absolute, the current working directory is prefixed to the returned file name.

`simplifyFilename("~/test") => "/usr/mnt/user/test"`

Returns the fully expanded name of`test`, assuming the user's home directory is `/usr/``mnt/user.`

#### Getting the Current Working Directory (getWorkingDir)

`getWorkingDir` returns the current working directory as a string. The result is put into a "~/prefixed" form if possible by testing for commonality with the current user's home directory. For example, `~/test` is returned in preference to `/usr/mnt/user1/test`, assuming that the home directory for `user1` is `/usr/mnt/user1` and the current working directory is `/``usr1/mnt/user1/test`.

`getWorkingDir() => "~/project/cpu/layout"`

#### Changing the Current Working Directory (changeWorkingDir)

Changes the working directory to the name you supply. The name can be specified with either a relative or absolute path. If you supply a relative path, the `cdpath` shell variable is used to search for the directory, not the SKILL path.

Different error messages are output if the operation fails because the directory does not existor you do not have search (execute) permission.

* ***Use this function with care: if "." is either part of the SKILL path or thelibraryPath, changing the working directory can affect the visibility of SKILL files or design data.***

Assume there is a directory`/usr5/design/cpu` with proper permission and there is no `test` directory under `/usr5/design/cpu`.

`changeWorkingDir( "/usr5/design/cpu") => tchangeWorkingDir( "test")`

Signals an error that no such directory exits.

Ports
-----

All input and output in SKILL goes through a data type called a port. A port can be openedeither for reading (an input port) or writing (an output port). Ports are analogous to FILE\* variables used by the `stdio` library in C. Most implementations of the UNIX operating system impose a strict limit (typically between 30 and 64) on the number of files that can be open at any time.

Your application typically needs to use some of these scarce file descriptors, leaving you withonly a few free ports with which to work. You should therefore always close ports that are no longer in use and avoid using an excessive number of ports; you might otherwise run out of ports when your code is moved to a different UNIX machine.

### Predefined Ports

Most I/O functions in SKILL accept a port as an optional argument. If a port is not specified,the `piport` and `poport` are used as default ports for input and output respectively. The table below lists the names and the use of the input/output ports predefined in SKILL.

* ***You can redefine the default values, if necessary, but many internal SKILLfunctions are hard wired to use particular ports and you should be careful not to assign any of them an illegal value.***

The`stdin`, `stdout`, and `stderr` ports are also predefined. These ports correspond to the standard input, standard output, and standard error streams available to every UNIX program.

****Predefined Input/Output Ports****

| **Name** | **Usage**
| piport | Standard input port, analogous to and initialized to stdin in C
| poport | Standard output port, analogous to and initialized to stdout in C
| errport | Output port for printing error messages, analogous to and initialized tostderr in C
| ptport | Output port for printing trace information; initialized to stdoutin C
| woport | Output port for printing warning messages; analogous to and initialized tostdout in C.
### Opening and Closing Ports

The following functions work with opening and closing ports. Both of the file opening functionsuse the SKILL path variable.

#### Opening an Input Port to Read a File (infile)

`infile` opens an input port ready to read a file you specify. The file name can be specified with either an absolute path or a relative path. In the latter case, the current SKILL path is used if it's not nil.

> `infile("~/test/input.il")=> port:"~/test/input.il"`

Result if such a file exists and is readable.

> `infile("myFile") => nil`

Result if`myFile` does not exist according to the SKILL path or exists but is not readable.

#### Opening an Output Port to Write a File (outfile)

`outfile` opens an output port ready to write to the file you specify. The file name can be specified with either an absolute path or a relative path.

* If a relative path is given and the current SKILL path setting is not`nil`, all directory paths from the SKILL path are checked, in the order specified, for that file name

* If found, the system overwrites the first updateable file in the list

* If no updateable file is found, it places a new file of that name in the first writable directory

> `p = outfile("out.il" "w")   => port:"out.il"`

Returns the name of the output port ready to write to the file.

> `outfile("/bin/ls")                                        => nil`

Returns`nil` if the file cannot be opened for writing.

#### Writing Out All Characters in the Output Buffer of a Port (drain)

`drain` writes out all characters that are in the output buffer of a port. `drain` is analogous to a combination of `fflush` and `fsync`in C. You get an error message if the port to drain is an input port or has been closed.

`drain()                        => tdrain(poport)          => t`

#### Draining, Closing, and Freeing a Port (close)

The port is drained, closed, and freed. When a file is closed, it frees the FILE\* associated withthe port. Do not use this function on `piport`, `poport`, `stdin`, `stdout`, and `stderr`.

```
p = outfile("~/test/myFile")   => port:"~/test/myFile"close(p)                                                        => t
```

Output
------

SKILL provides functions for unformatted and formatted output.

### Unformatted Output

#### Printing the Value of an Expression in the Default Format (print, println)

`print` prints the value of an expression using the default format for the data type of the value (for example, strings are enclosed in double quotes).

`print("hello")"hello"=> nil`

Prints to`poport` and returns `nil`.

`println` prints the value of an expression just like `print`, but a newline character is automatically printed after printing the input value. `println` flushes the output port after printing each newline character.

`println("Hello World!")"Hello World!"=> nil`

#### Printing a Newline (\n) Character (newline)

Prints a newline (\n) character. If you do not specify the output port, it defaults to`poport`, the standard output port. The `newline` function flushes the output port after printing each newline character.

`print("Hello") newline() print("World!")"Hello""World!"=> nil`

#### Printing a List with a Limited Number of Elements and Levels of Nesting (printlev)

`printlev` prints a list with a limited number of elements and levels of nesting. Lists are normally printed in their entirety no matter how many elements they have or how deeply nested they are.

Applications can, however, set upper limits on the number of elements and the levels ofnesting shown when printing lists using `printlev`. These limits are sometimes necessary to control the volume of interactive output because the SKILL top-level automatically prints the results of expression evaluation. Limits can also protect against infinite looping on circular lists possibly created when novices use the destructive list modification functions, such as `rplaca` or `rplacd`, without a thorough understanding of how they work.`printlev` uses the following syntax:

`printlev( g_value x_level x_length [p_outputPort] ) => nil`

Two integer variables, print length and print level (specified by`x_length` and `x_level`), control the maximum number of elements and the levels of nesting that are printed. List elements beyond the maximum specified by print length are abbreviated as "…" and lists nested deeper than the maximum level specified by print level are abbreviated as "&." Both print length and print level are initialized to `nil` (meaning no limits are imposed) by SKILL, but each application can set its own limits.

The`printlev` function is identical to `print` except that it takes two additional arguments specifying the maximum level and length to use in printing the expression.

`List = '(1 2 (3 (4 (5))) 6)printlev(List 100 2)(1 2 …)=> nil`

`printlev(List 3 100)(1 2 (3 (4 &)) 6)=> nil`

`printlev(List 3 3 p)(1 2 (3 (4 &)) …)=> nil`

Assumes port p exists. Prints to port p.

### Formatted Output

You can precede format characters with a field width specification. For example, %5d printsan integer in a field that is 5 columns wide. If the field width begins with the digit "0", zero padding is done instead of blank padding. For the format characters`f` and `e`, the width specification can be followed by a period "." and an integer specifying the precision, that is, the number of digits to print after the decimal point.

Output is right justified within a field by default unless an optional minus sign "-" immediatelyfollows the "%" character, which will then be left justified. To print a percent sign, you must use two percent signs in succession. You must explicitly put "\n" in your format string to print a newline character and "\t" for a tab.

**Common Output Format Specifications**

| **FormatSpecification** | **Type(s) ofArgument** | **Prints**
| %d | fixnum | Integer in decimal radix
| %o | fixnum | Integer in octal
| %x | fixnum | Integer in hexadecimal
| %f | flonum | Floating-point number in the style [-]ddd.ddd
| %e | flonum | Floating-point number in the style [-]d.ddde[-]ddd
| %g | flonum | Floating-point number in style f or e, whichevergives full precision in minimum space
| %s | string, symbol | Prints out a string (without quotes) or the printname of a symbol
| %c | string, symbol | The first character
| %n | fixnum, flonum | Number
| %L | list | Default format for the data type
| %P | list | Point
| %B | list | Box
For formatted output, SKILL makes available the standard C`stdio` library routines `printf`, `fprintf`, and `sprintf`. SKILL provides a robust interface to these routines. Below is a brief description of each routine in the context of the SKILL runtime environment. If more detailed descriptions are needed for these functions, consult your C programming manual.

#### Writing Formatted Output to Ooport (printf)

`printf` writes formatted output to `poport`. Optional arguments following the format string are printed according to their corresponding format specifications. printf is identical to fprintf except that it does not take a port argument and the output is written to poport.

`x = 197.9687printf("The test measures %10.2f.\n" x)`

Prints the following line to`poport` and returns `t`.

`The test measures            197.97. => t`

#### Writing Formatted Output to a Port (fprintf)

`fprintf` writes formatted output to the port given as the first argument. The optional arguments following the format string are printed according to their corresponding format specifications.

`x = 197.9687fprintf(p "The test measures %10.2f.\n" x)`

Prints the following line to port p and returns`t`.

`The test measures            197.97. => t`

#### Writing Formatted Output to a String Variable (sprintf)

`sprintf` formats the output and puts the resultant string into the variable given as the first argument. If `nil` is specified as the first argument, no assignment is made. The formatted string is returned. Because of internal buffering in `sprintf`, there is a limit to how many characters `sprintf` can handle, but the limit is large enough (8192 characters) that it should not present any problem.

```
sprintf(s "Memorize %s number %d!" "transaction" 5)=> "Memorize transaction number 5!"
```

`s => "Memorize transaction number 5!"`

`p = outfile(sprintf(nil "test%d.out" 10))=> port:"test10.out"`

### Pretty Printing

SKILL provides functions for "pretty printing" function definitions and long data lists withproper indenting to make them more readable and easier to manipulate in text form.

You need the SKILL Development Environment license to pretty print function definitionsusing the `pp` SKILL function below.

#### Pretty Printing a Function Definition (pp)

`pp` pretty prints a function definition. The function must be a readable interpreted function. (Binary functions cannot be pretty printed.) Each function definition is printed so it can be read back into SKILL. `pp` does not evaluate its first argument but does evaluate the second argument, if given.

```
procedure(fac(n) if(n <= 1 1 n*fac(n-1)))=> facpp fac procedure(fac(n)      if((n <= 1) 1            (n * fac(n - 1)))      ))=> nil
```

Defines the factorial function`fac`, then pretty prints it to poport.

#### Pretty Printing Long Data Lists (pprint)

`pprint` is identical to `print` except that it tries to pretty print the value whenever possible. (`pprint` does not work the same as the `pp` function. `pp` is an `nlambda` and only takes a function name whereas `pprint` is a lambda and takes an arbitrary SKILL object.)

The`pprint` function is useful, for example, when printing out a long list where `print` simply prints the list on one (possibly huge) line but `pprint` limits the output on a single line and produces a multiple-line printout if necessary. This multiple-line printout makes later input much easier.

```
pprint '(1 2 3 4 5 6 7 8 9 0 a b c d e f g h i j k) (1 2 3 4 5      6 7 8 9 0      a b c d e      f g h i j      k)=> nil
```

Input
-----

When describing input functions, this manual often uses the term "form" to refer to a logicalunit of input. A form can be an expression, such as source code or a data list that can span multiple input lines. Input functions such as `lineread` read in one input line at a time but continue reading if they do not find a complete form at the end of a line.

You can think of input forms and how the SKILL functions work with them in the followingways.

**Input Functions**

| **Input Source** | **SKILLEvaluated** | **SKILL Not Evaluated** | **Application-SpecificFormats**
| File | load loadi | lineread | infile gets getc fscanf close
| String | evalstring loadstring errsetstring | linereadstring | instring gets getc fscanf close
SKILL forms read from a file are either evaluated or not evaluated. Input strings can have anapplication-specific syntax of their own, such as a netlist syntax. It is the programmer's responsibility to open a port, understand the application-specific syntax, process the input, and then close the port.

### Reading and Evaluating SKILL Formats

#### Reading and Evaluating an Expression Stored in a String (evalstring)

`evalstring` reads and evaluates an expression stored in a string. The resulting value is returned. Notice that `evalstring` does not allow the outermost set of parentheses to be omitted, as in the top level. Refer to the ["Top Levels"](chap9.html#1008553 "Advanced Topics") for a discussion of the top level.

```
evalstring("1+2")                                        => 3evalstring("cons('a '(b c))")           => (a b c)car '(1 2 3)                                                         => 1
```

`evalstring("car '(1 2 3)")`

Signals that`car` is an unbound variable.

#### Opening a String and Executing its Expressions (loadstring)

`loadstring` opens a string for reading, then parses and executes expressions stored in the string just as `load` does in loading a file. `loadstring` is different from `evalstring` in two ways. `loadstring`

* Uses`lineread` mode

* Always returns`t` if it evaluates successfully

```
loadstring "1+2"                      => tloadstring "procedure( f(n) x=x+n )"  => tloadstring "x=10\n f 20\n f 30"       => tx                                     => 60
```

#### Reading and Evaluating an Expression then Checking for Errors (errsetstring)

`errsetstring` reads and evaluates an expression stored in a string. Same as `evalstring` except that it calls `errset` to catch any errors that might occur during the parsing and evaluation.

`errsetstring("1+2")            => (3)errsetstring("1+'a")           => nil`

Returns`nil` because an error occurred.

`errsetstring("1+'a" t)         => nil`

`Prints out an error message:*Error* plus: can't handle (1 + a)`

#### Loading Files (load, loadi)

`load` opens a file, repeatedly calls `lineread` to read in the file, and immediately evaluates each form after it is read in. It closes the file when end of file is reached. Unless errors are discovered, the file is read in quietly. If `load` is interrupted by pressing Control-c, the function skips the rest of the file being loaded.

SKILL has an autoload feature that allows applications to load functions into SKILL ondemand. If a function being executed is undefined, SKILL checks if the name of the function (a symbol) has a property called autoload attached to it. If the property exists, its value, which must be either a string or a function call that returns a string, is used as the name of a file to load. The file should contain a definition for the function that triggered the autoload. Execution proceeds normally after the function is defined. The whole autoload sequence is functionally transparent. Refer to ["Delivering Products"](chap10.html#1008199 "Delivering Products")

```
load( "testfns.il")                 ; Load file testfns.ilfn.autoload = "myfunc.il"           ; Declares an autoload property.fn(1)
```

`fn` is undefined at this point, so this call triggers an autoload of `myfunc.il`, which contains the definition of `fn`.

`fn(2)              ; fn is now defined and executes normally.`

`loadi` is identical to `load`, except that `loadi` ignores errors encountered during the load, prints an error message, and then continues loading.

`loadi( "testfns.il" )`

Loads the`testfns.il` file.

`loadi( "/tmp/test.il")`

Loads the`test.il` file from the `tmp` directory.

### Reading but Not Evaluating SKILL Formats

#### Parsing the Next Line in the Input Pport into a List (lineread)

`lineread` parses the next line in the input port into a list that you can further manipulate. It is used by the interpreter's top level to read in all input and understands only SKILL syntax.

Only one line of input is read in unless there are still open parentheses pending at the end ofthe first line, or binary `infix` operators whose right-hand argument has not yet been supplied, in which case additional input lines are read until all open parentheses have been closed and all binary `infix` operators satisfied. The symbol `t` is returned if `lineread` reads a blank input line and `nil` is returned at the end of the input file.

```
lineread(piport)         ; Reads in the next input expressionf 1 2 +                  ; First input line of the file being read3                        ; Second input line=> f (1 (2 + 3))
```

```
lineread(piport)f(a b c)                 ; Another input line of the file=> ((f a b c))           ; Returns a list of input objects
```

#### Reading a String into a List (linereadstring)

`linereadstring` executes `lineread` on a string and returns the form read in. Anything after the first form is ignored.

```
linereadstring "abc"                      => (abc)linereadstring "f a b c"                  => (f a b c)linereadstring "x + y"                    => ((x + y))linereadstring "f a b c\n g 1 2 3"        => (f a b c)
```

In the last example, only the first form is read in.

### Reading Application-Specific Formats

The following input functions are helpful when you must read input from a file that was notwritten in SKILL-compatible format.

#### Reading Formatted Input (fscanf)

`fscanf` reads the input from a port according to format specifications in a format string. The results are stored in corresponding variables in the call. `fscanf` can be considered the inverse of the `fprintf` output function. `fscanf` returns the number of input items it successfully matches with its format string. It returns `nil` if it encounters an end of file.

The maximum size of any input string being read as a string variable for`fscanf` is 8K. Also, the function`lineread` is a faster alternative to `fscanf` for reading SKILL objects.

The input formats accepted by`fscanf` are summarized below.

**Common Input Format Specifications**

| **FormatSpecification** | **Type(s) ofArgument** | **Scans for**
| %d | fixnum | An integer
| %f | flonum | A floating-point number
| %s | string | A string (delimited by spaces) in the input
`fscanf( p "%d %f" i d )`

Scans for an integer and a floating-point number from the input port`p` and stores the values read in the variables `i` and `d`, respectively.

Assume there is a file`testcase` with one line:

`hello 2 3 world`

```
x = infile("testcase") => port:"testcase"fscanf( x "%s %d %d %s" a b c d )=> 4(list a b c d)                                                  => ("hello" 2 3 "world")
```

#### Reading a Line and Storing it in a Variable (gets)

`gets` reads a line from the input port and stores it as a string in a variable. The string is also returned as the value of `gets`. The terminating newline character of the line becomes the last character in the string. `gets` returns `nil` if EOF is encountered and the variable maintains its last value. Assume the`test1.data` file has the following first two lines:

`#This is the data for test10001 1100 1011 0111`

```
p = infile("test1.data")   => port:"test1.data"gets(s p)                                       => "#This is the data for test1\n"gets(s p)                                       => "0001 1100 1011 0111\n"s                                                                => "0001 1100 1011 0111\n"
```

#### Reading and Returning a Single Character from an Input Port (getc)

`getc` reads a single character from the input port and returns it as the value of `getc`. If the character returned is a non-printable character, its octal value is stored as a symbol. If you are familiar with C, you should note that the `getc` and `getchar` SKILL functions are totally unrelated. `getc` returns `nil` if EOF is encountered.

The input port arguments for both`gets` and `getc` are optional. If the port is not given, the functions take their input from `piport`. In the following example assume the file `test1.data` has its first line read as:

`#This is the data for test1`

```
p = infile("test1.data")  => port:"test1.data"getc(p)                                           => \#getc(p)                                           => Tgetc(p)                                               => h
```

### Reading Application-Specific Formats from Strings

In addition to being able to accept input from the terminal and from text files, SKILL can alsotake its input directly from strings. Some applications store programs internally as strings and then parse the strings into their corresponding internal SKILL representations as needed.

Because parsing is a relatively expensive operation, you should avoid calling any of thefollowing functions repeatedly on the same string. It is a good practice to convert each string into its internal SKILL representation before using it more than once.

#### Opening a String for Reading (instring)

Opens a string for reading just as`infile` opens a file. An input port that can be used to read the string is returned.

```
s = "Hello World!"                           => "Hello World!"p = instring(s)                                  => port:"*string*"fscanf(p "%s %s" a b)=> 2a                                                                    => "Hello"b                                                                    => "World!"close(p)                                                        => t
```

* ***Always remember to close the port when you are done.***

#### Opening a String for Writing (outstring)

The`outstring`function takes no arguments and returns an opened output port for strings (or an outport). After a port is opened, it can be used with functions, such as fprintf, println, and close that write to an output port. You can use the `close` function to close the output port.

You need to use the`getOutstring` function to retrieve the content of the output port (while it is open). For example:

`s = outstring()`

`= >port:"*string*"`

`fprintf(s "Quick brown")`

`getOutstring(s)`

`=>"Quick brown"`

`fprintf(s " fox jumps")`

`getOutstring(s)`

`=> "Quick brown fox jumps"`

`fprintf(s " over the lazy dog")`

`getOutstring(s)`

`=> "Quick brown fox jumps over the lazy dog"`

`close(s)`

`getOutstring(s)`

`=> nil`

System-Related Functions
------------------------

Various SKILL functions are available to interact with and query the system environment.

### Executing UNIX Commands

From within SKILL, you can execute individual UNIX commands or invoke the`sh` or `csh` UNIX shell.

#### Starting the UNIX Bourne-Shell (sh, shell)

Starts the UNIX Bourne-shell sh as a child process to execute a command string. If the sh function is called with no arguments, an interactive UNIX shell is invoked that prompts you for UNIX command input (available only in nongraphic applications).

`sh( "rm /tmp/junk")`

Removes the`junk` file from the`/tmp` directory and returns `t` if it is removed successfully.

#### Starting the UNIX C-Shell (csh)

Starts the UNIX C-shell`csh` as a child process to execute a command string. Identical to the sh function, but invokes the C-shell (csh) rather than the Bourne-shell (sh).

`csh( "mkdir ~/tmp" )`

Creates a directory called`tmp` in your home directory.

### System Environment

The following functions find and compare the current time, retrieve the version number of thesoftware you are using, and determine the value of a UNIX environment variable.

#### Getting the Current Time (getCurrentTime)

`getCurrentTime` returns the current time in the form of a string. The format of the string is `month day hour:minute:second year`.

`getCurrentTime( ) => "Jan 26 18:15:18 1993"`

#### Comparing Times (compareTime)

`compareTime` compares two string arguments, representing a clock-calendar time. The format of the string is `month day hour:minute:second year`. The units are seconds.

`compareTime( "Apr 8 4:21:39 1991" "Apr 16 3:24:36 1991")=> -687777.`

687,777 seconds have occurred between the two dates. For a positive number of seconds,the most recent date needs to be the first argument.

`compareTime("Apr 16 3:24:36 1991" "Apr 16 3:14:36 1991")=> 600`

600 seconds (10 minutes) have occurred between the two dates.

#### Getting the Current Version Number of Cadence Software (getVersion)

Returns the version number of software you are using.

`getVersion() => "cds3 version 4.2.2 Fri Jan 26 20:40:28 PST 1993"`

#### Getting the Value of a UNIX Environment Variable (getShellEnvVar)

`getShellEnvVar` returns the value of a UNIX environment variable, if it has been set.

`getShellEnvVar("SHELL") => "/bin/csh"`

Returns the current value of the`SHELL` environment variable.

#### Setting a UNIX Environment Variable (setShellEnvVar)

`setShellEnvVar` sets the value of a UNIX environment variable to a new value.

`setShellEnvVar("PWD=/tmp") => t`

Sets the current working directory to the`/tmp` directory .

`getShellEnvVar("PWD")=> "/tmp"`

Gets the current working directory.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
