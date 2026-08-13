<!--
source: sklangref/inputoutput.md
part: 1/2
estimated_tokens: 13467
-->

### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

11
==

Input Output Functions
======================

### close

`close( p_port ) => t`

#### Description

Drains, closes, and frees a port.

When a file is closed, it frees the`FILE*` associated with `p_port`. Do not use this function on `piport`, `poport`, `stdin`, `stdout`, and `stderr`.

#### Arguments

|  |
| --- | ---
| `p_port` | Name of port to close.
#### Value Returned

|  |
| --- | ---
| `t` | Returns`t` if the port is closed successfully.
#### Example

```
p = outfile("~/test/myFile") => port:"~/test/myFile"close(p)                     => t
```

#### Reference

`outfile, infile, drain`

### compress

`compress( t_sourceFile t_destFile ) => t | error message`

#### Description

Reduces the size of a SKILL file, which must be SKILL source code, and places the output into another file.

Compression renders the data less readable because indentation and comments are lost. Itis not the same as encrypting the file because the representation of `t_destFile` is still in ASCII format. This process does not remove the source file.

#### Arguments

|  |
| --- | ---
| `t_sourceFile` | Name of the SKILL source file.
|  |
| --- | ---
| `t_destFile` | Name of the destination file.
#### Value Returned

|  |
| --- | ---
| `t` | Returns`t` when function executes successfully.
|  |
| --- | ---
| `error message` | Signals an error if problems are encountered compressing thefile.
#### Example

`compress( "triad.il" "triad_cmp.il") => t`

#### Reference

`encrypt`

### display

`display( g_obj [ p_port ] ) => t | nil`

#### Description

Writes a representation of an object to the given port.

Strings that appear in the written representation are not enclosed in double quotes, and nocharacters are escaped within those strings.

#### Arguments

|  |
| --- | ---
| `g_obj` | Any SKILL object.
|  |
| --- | ---
| `p_port` | Optional output port.`poport` is the default.
#### Value Returned

|  |
| --- | ---
| `t` | Usually ignored. Function is for side effects only.
|  |
| --- | ---
| `nil` | Usually ignored. Function is for side effects only.
#### Example

`(display "Hello!")=> t`

The side effect is to display`Hello!` to `poport`.

#### Reference

`drain, print, write`

### drain

`drain( [ p_outputPort ] ) => t | nil`

#### Description

Writes out all characters that are in the output buffer of a port.

Analogous to`fflush` in C (plus `fsync` if the port is a file). Not all systems guarantee that the disk is updated on each write. As a result, it is possible for a set of seemingly successful writes to actually fail when the port is closed.

To protect your data, call`drain` after a logical set of writes to a file port. It is not recommended that you call `drain` after every write however, because this could impact your program's performance.

#### Arguments

|  |
| --- | ---
| `p_outputPort` | Port to flush output from. If no argument is given this functiondoes nothing.
#### Value Returned

|  |
| --- | ---
| `t` | If all buffered data was successfully written out.
|  |
| --- | ---
| `nil` | There was a problem writing out the data, and some or all of itwas not successfully written out.
|  |
| --- | ---
|  | Signals an error if the port to be drained is an input port or hasbeen closed.
#### Example

`drain()          => tdrain(poport)    => t`

`myPort = outfile("/tmp/myfile")=> port:"/tmp/myfile"`

`for(i 0 15 fprintf(myPort "Test output%d\n" i))=> t`

```
system( "ls -l /tmp/myfile")--rw-r--r-- 1 root 0 Aug12 14:44 /tmp/myFilefileLength( "/tmp/myfile")=> 0drain(myPort)=> t
```

`fileLength( "/tmp/myfile" )=> 230close(myPort)=> t`

```
drain(myPort)=> *Error* drain: cannot send output to a closed port - port:        "/tmp/myfile"
```

```
drain(piport)=> *Error* drain: cannot send output to an input port -       port:"*stdin*"
```

`drain(poport)=> t`

```
defun(handleWriteError (x)    printf("WARNING - %L write unsuccessful\n" x) nil)=> handleWriteErrormyPort=outfile("/tmp/myfile")=> port:"/tmp/myfile"for(i 0 15 fprintf(myPort "%d\n" (2**i)))=> tif(!drain(myPort) handleWriteError(myPort) t)=> t
```

#### Reference

`outfile, close`

### ed

`ed( [ t_fileName ] ) => t | nil`

#### Description

Edits the named file.

#### Arguments

|  |
| --- | ---
| `t_fileName` | File to edit. If no argument is given, defaults to the previouslyedited file, or `temp.il`, if there is no previous file.
#### Value Returned

|  |
| --- | ---
| `t` | The operation was successfully completed.
|  |
| --- | ---
| `nil` | The file does not exist or there is an error condition.
#### Reference

`edi, edl, edit`

### edi

`edi( [ t_fileName ] ) => t | nil`

#### Description

Edits the named file, then includes the file into SKILL.

#### Arguments

|  |
| --- | ---
| `t_fileName` | File to edit. If no argument is given, defaults to the previouslyedited file, or `temp.il`, if there is no previous file.
#### Value Returned

|  |
| --- | ---
| `t` | The operation was successfully completed.
|  |
| --- | ---
| `nil` | The file does not exist or there is an error condition.
#### Example

`edi( "~/myFile.il" )`

#### Reference

`ed, edit, edl`

### edit

`edit( S_object [ g_loadFlag ] ) => x_childId`

#### Description

Edits a file, function, or variable.This function only works if you are in graphical mode. This is an `nlambda` function.

`edit` brings up an editor window in a separate process and thus doesn't lock up the CIW. If the object being edited is a function that was loaded after debug mode was turned on, then `edit` opens up the file that contains the function. If the editor is `vi` or `emacs` it jumps to the start of the function. If `g_loadFlag` is `t` the file is loaded into SKILL when the editor is exited. Be sure the `editor` variable is set up properly if you are using an editor other than `vi` or `emacs`.

#### Arguments

|  |
| --- | ---
| `S_object` | If you are editing a file, the object you are editing must be astring. If you are editing a function or variable, it must be an unquoted symbol.
|  |
| --- | ---
| `g_loadFlag` | Determines whether to load the file after the editor window isexited.  Valid values: `t` or `nil`  Default: `nil`.
#### Value Returned

|  |
| --- | ---
| `x_childId` | Integer identifying the process spawned for the editor.
#### Example

`edit( "~/.cdsinit" )`

Edits the`.cdsinit` file in your home directory.

`edit( myFun)`

Edits the`myFun` function.

`edit( myVar )`

Edits the`myVar` variable and loads in the new value when the editor window is closed.

#### Reference

`ed, edl, edi, isFile`

### edl

`edl( [ t_fileName ] ) => t | nil`

#### Description

Edits the named file, then loads the file into SKILL.

#### Arguments

|  |
| --- | ---
| `t_fileName` | File to edit. If no argument is given, defaults to the previouslyedited file, or `temp.il`, if there is no previous file.
#### Value Returned

|  |
| --- | ---
| `t` | The operation was successfully completed.
|  |
| --- | ---
| `nil` | The file does not exist or there is an error condition.
#### Example

`edl( "/tmp/demo.il" )`

#### Reference

`ed, edi, edit`

### encrypt

`encrypt( t_sourceFile t_destFile [ t_password ] ) => t`

#### Description

Encrypts a SKILL file and places the output into another file.

If a password is supplied, the same password must be given to the command used to reloadthe encrypted file.

#### Arguments

|  |
| --- | ---
| `t_sourceFile` | Name of theSKILL file you are encrypting.
|  |
| --- | ---
| `t_destFile` | Destination file you want the encrypted file to be placed in.
|  |
| --- | ---
| `t_password` | Optional password; you are asked for it before you can reload theencrypted file.
#### Value Returned

|  |
| --- | ---
| `t` | When the file has been encrypted and placed in`t_destFile`. Signals an error if you fail to name a destination file or give the name of a file already present.
#### Example

`encrypt( "triadb" "myPlace" "option") => t`

Encrypts the`triadb` file into the `myPlace` file with `option` as the password. Returns `t` if successful.

#### Reference

compress, load

### expandMacroDeep

`expandMacroDeep(g_form)=> g_expandedForm`

#### Description

This function recursively expands all macros specified in`g_form`.

#### Arguments

|  |
| --- | ---
| `g_form` | Form that can be a macro call.
#### Value Returned

|  |
| --- | ---
| `g_expandedForm` | Expanded form or the original form if the given argument is not amacro call.
#### Example

`expandMacroDeep(myFunction(1 2))`

### fileLength

`fileLength( S_name ) => x_size | 0`

#### Description

Determines the number of bytes in a file.

A directory is viewed just as a file in this case. Uses the current SKILL path if a relative pathis given. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../``../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Name of the file you want the size of.
#### Value Returned

|  |
| --- | ---
| `x_size` | Number of bytes in the`S_name` file.
1. The file exists but is empty.Signals an error if the named file does not exist.

#### Example

`fileLength("/tmp")                   => 1024`

Return value is system-dependent.

`fileLength("~/test/out.1")           => 32157`

Assuming the named file exists and is 32157 bytes long.

#### Reference

`isFile, isFileName`

### fileSeek

`fileSeek( p_port x_offset x_whence ) => t | nil`

#### Description

Sets the position for the next operation to be performed on the file opened on a port. The position is specified in bytes.

#### Arguments

|  |
| --- | ---
| `p_port` | Port associated with the file.
|  |
| --- | ---
| `x_offset` | Number of bytes to move forward (or backward with negativeargument).
|  |
| --- | ---
| `x_whence` | Valid Values: `0` Offset from the beginning of the file. `1` Offset from current position of file pointer. `2` Offset from the end of the file.
#### Value Returned

|  |
| --- | ---
| `t` | The operation was successfully completed.
|  |
| --- | ---
| `nil` | The file does not exist or the position given is out of range for aninput file.
#### Example

Let the file`test.data` contain the single line of text:

`0123456789 test xyz`

```
p = infile("test.data")  => port:"test.data"fileTell(p)              => 0for(i 1 10 getc(p))      => t   ; Skip first 10 charactersfileTell(p)              => 10fscanf(p "%s" s)         => 1   ; s = "test" nowfileTell(p)              => 15
```

```
fileSeek(p 0 0)          => tfscanf(p "%d" x)         => 1   ; x = 123456789 nowfileSeek(p 6 1)          => tfscanf(p "%s" s)         => 1   ; s = "xyz" now
```

#### Reference

`fileTell, isFile, isFileName`

### fileTell

`fileTell( p_port ) => x_offset`

#### Description

Returns the current offset in bytes for the file opened on a port.

#### Arguments

|  |
| --- | ---
| `p_port` | Port associated with the file.
#### Value Returned

|  |
| --- | ---
| `x_offset` | Current offset (from the beginning of the file) in bytes for the fileopened on `p_port`.
#### Example

Let the file`test.data` contain the single line of text:

`0123456789 test xyz`

```
p = infile("test.data")  => port:"test.data"fileTell(p)              => 0for(i 1 10 getc(p))      => t    ; Skip first 10 charactersfileTell(p)              => 10fscanf(p "%s" s)         => 1    ;s = "test" nowfileTell(p)              => 15
```

#### Reference

`infile, isFile, fileSeek, outfile`

### fileTimeModified

`fileTimeModified( t_filename ) => x_time | nil`

#### Description

Gets the time a given file was last modified.

The return value is an internal, numeric, representation of the time the named file was lastmodified (for example, the number of 1/100 seconds from January 1, 1970). The actual number, which is system-dependent, is derived from the underlying UNIX system.

#### Arguments

|  |
| --- | ---
| `t_filename` | Name of a file.
#### Value Returned

|  |
| --- | ---
| `x_time` | Last time`t_filename` was modified.
|  |
| --- | ---
| `nil` | No file with the given name was found.
#### Example

`fileTimeModified( "~/.cshrc" )=> 787435470`

#### Reference

`getCurrentTime`

### fprintf

`fprintf( p_port t_formatString [ g_arg1 ... ] ) => t`

#### Description

Writes formatted output to a port.

The`fprintf` function writes formatted output to the port given as the first argument. The optional arguments following the format string are printed according to their corresponding format specifications.

`printf` is identical to `fprintf` except that it does not take the `p_port` argument and the output is written to [poport](../sklanguser/chap7.html#ioports).

Output is right justified within a field by default unless an optional minus sign "-" immediately follows the `%` character, which will then be left justified. To print a percent sign, you must use two percent signs in succession. You must explicitly put `\n` in your format string to print a newline character and `\t` for a tab.

****Common Output Format Specifications****

| **FormatSpecification** | **Type(s) ofArgument** | **Prints**
| %d | fixnum | Integer in decimal radix
| %o | fixnum | Integer in octal
| %x | fixnum | Integer in hexadecimal
| %f | flonum | Floating-point number in the style [-]ddd.ddd
| %e | flonum | Floating-point number in the style [-]d.ddde[-]ddd
| %g | flonum | Floating-point number in style f or e, whichevergives full precision in minimum space  **Note:** Qualifying %g with width may causeimprecise results to be printed.
| %s | string, symbol | Prints out a string (without quotes) or the printname of a symbol
| %c | string, symbol | The first character
| %n | fixnum, flonum | Number
| %P | list | Point
| %B | list | Box
| %N | any | Prints an object in the old style, that is, does notcall the `printself` function
| %L | list | Default format for the data type  Print behavior depends on the value of theprintpretty variable:  If printpretty is`nil`, this behaves like %N  If printpretty is`non-nil` (default), %L uses `printself` for standard objects
| %A | any | Prints any type of object using the`printself` representation
The`t_formatString` argument is a conversion control string containing directives listed in the table above. The %L, %P, and %B directives ignore the width and precision fields.

```
%[-][width][.precision]conversion_code     [-]              = left justify     [width]          = minimum number of character positions     [.precision]     = number of characters to be printed     conversion_code
```

#### Arguments

|  |
| --- | ---
| `p_port` | Output port to write to.
|  |
| --- | ---
| `t_formatString` | Characters to be printed verbatim, intermixed with formatspecifications prefixed by the `%` sign.
|  |
| --- | ---
| `g_arg1` | The arguments following the format string are printed accordingto their corresponding format specifications.
#### Value Returned

|  |
| --- | ---
| `t` | Prints the formatted output and returns`t`.
#### Example 1

`p = outfile("power.out")=> port:"power.out"`

`for(i 0 15 fprintf(p "%20d %-20d\n" 2**i 3**i))=> t`

`close( p)`

At this point the`power.out` file has the following contents.

#### Example 2

This example shows the use of`%A`. Note that `%A` calls the `printself` method.

`defmethod(printself ((obj fixnum))`

> `sprintf(nil "FIXNUM{%d}" obj));;Defines the printself method`

> `printf("Print control A returns: %A\n" 42);; %A calls the printself method`

`=>Print control A returns: FIXNUM{42}`

#### Example 3

This example shows the use of`%L`. Note that `%L` only calls `printself` for standard objects.

`defmethod(printself ((obj fixnum))`

> `sprintf(nil "FIXNUM{%d}" obj));;Defines the printself method`

> `printf("Print control L returns: %L\n" 42)`

`=>Print control L returns: 42`

#### Example 4

This example shows the use of`%L`,`%A`, and `%N`print controls with `printf` when printing standard objects. Note that `%A` prints the same result as `%L` and `%N` does not call the `printself` method.

`defclass(A () ());; Defines a class A`

`defmethod(printself ((obj A));; Defines the printself method`

> `sprintf(nil "OBJ_A{%L}" obj))`

> `printf("Print control L returns: %L\n" Instance('A))`

> `printf("Print control A returns: %A\n" Instance('A))`

> `printf("Print control N returns: %N\n" Instance('A))`

`=>Print control L returns: OBJ_A{stdobj@0x83bf024}`

`Print control A returns: OBJ_A{stdobj@0x83bf024}`

`Print control N returns: stdobj@0x83bf03c`

#### Reference

`close, fscanf, scanf, sscanf, outfile, printf`

### fscanf, scanf, sscanf

```
fscanf( p_inputPort t_formatString [ s_var1 ... ] ) => x_items | nilscanf( t_formatString [ s_var1 ... ] ) => x_items | nilsscanf( t_sourceString t_formatString [ s_var1 ... ] ) => x_items | nil
```

#### Description

The only difference between these functions is the source of input.`fscanf` reads input from a port according to format specifications and returns the number of items read in. `scanf` takes its input from `piport` implicitly. `scanf` only works in standalone SKILL when the `piport` is not the CIW. `sscanf` reads its input from a string instead of a port.

The results are stored into corresponding variables in the call. The`fscanf` function can be considered the inverse function of the `fprintf` output function. The `fscanf` function returns the number of input items it successfully matched with its format string. It returns `nil` if it encounters an end of file.

The maximum size of any input string being read as a string variable for`fscanf` is currently limited to 8K. Also, the function `lineread` is a faster alternative to `fscanf` for reading SKILL objects.

If an error is found while scanning for input, only those variables read before the error will beassigned.

The common input formats accepted by`fscanf` are summarized below.

**Common Input Format Specifications**

| **FormatSpecification** | **Type(s) ofArgument** | **Scans for**
| %d | fixnum | An integer
| %f | flonum | A floating-point number
| %s | string | A string (delimited by spaces) in the input
#### Arguments

|  |
| --- | ---
| `p_inputPort` | Input port`fscanf` reads from. The input port cannot be the CIW for `fscanf`.
|  |
| --- | ---
| `t_sourceString` | Input string for`sscanf`.
|  |
| --- | ---
| `t_formatString` | Format string to match against in the reading.
|  |
| --- | ---
| `s_var1` | Name of variable to store results of read.
#### Value Returned

|  |
| --- | ---
| `x_items` | The number of input items it successfully read in. As a side-effect, the items read in are assigned to the corresponding variables specified in the call.
|  |
| --- | ---
| nil | It encounters an end of file.
#### Example

`fscanf( p "%d %f" i d )`

Scans for an integer and a floating-point number from the input port`p` and stores the values read in the variables `i` and `d`, respectively.

Assume a file`testcase` with one line:

`hello 2 3 world`

```
x = infile("testcase")=> port:"testcase"fscanf( x "%s %d %d %s" a b c d )=> 4(list a b c d) => ("hello" 2 3 "world")
```

#### Reference

`fprintf, lineread`

### get\_filename

`get_filename( p_port ) => s_result`

#### Description

Returns the file name of a port.

#### Arguments

|  |
| --- | ---
| `p_port` | A port object.
#### Value Returned

|  |
| --- | ---
| `x_result` | The file name of the port.
#### Examples

`aPort                 => port:"inFile"get_filename( aPort ) => "inFile"`

### getc

`getc( [ p_inputPort ] ) => s_char`

#### Description

Reads and returns a single character from an input port. Unlike the C library, the `getc` and `getchar` SKILL functions are totally unrelated.

The input port arguments for both`gets` and `getc` are optional. If the port is not given, the functions take their input from `piport`.

#### Arguments

|  |
| --- | ---
| `p_inputPort` | Input port; if not given, function defaults to`piport`.
#### Value Returned

|  |
| --- | ---
| `s_char` | Single character from the input port in symbol form. If the character returned is a non-printable character, its octal value is stored as a symbol.
#### Example

In the following assume the file`test1.data` has its first line read as:

`#This is the data for test1`

```
p = infile("test1.data") => port:"test1.data"getc(p)                  => \#getc(p)                  => Tgetc(p)                  => h
```

#### Reference

`gets`

### getDirFiles

`getDirFiles( S_name ) => l_strings`

#### Description

Returns a list of the names of all files and directories, including`.` and `..`, in a directory.

Uses the current SKILL path for relative paths. Note that a path which is anchored to currentdirectory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Name of the directory in either string or symbol form.
#### Value Returned

|  |
| --- | ---
| `l_strings` | List of names of all files and directories in a given directory name(including `.` and `..`).
|  |
| --- | ---
|  | Signals an error if the directory does not exist or is inaccessible.
#### Example

```
getDirFiles(car(getInstallPath()))=> ("." ".." "bin" "cdsuser" "etc" "group" "include" "lib" "pvt" "samples" "share" "test" "tools" "man" "local" )
```

#### Reference

`gets, getSkillPath`

### getOutstring

`getOutstring( s_port) => t_string/nil`

#### Description

Retrieves the content of the outstring port (while it is open).

#### Arguments

|  |
| --- | ---
| `s_port` | Specifies the outstring port from which the content needs to beretrieved
#### Value Returned

|  |
| --- | ---
| `t_string` | Returns the string read from the outstring port
|  |
| --- | ---
| `nil` | Returns`nil` if the string cannot be read from the outstring port
#### Example

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

### gets

`gets( s_variableName [ p_inputPort ] ) => t_string |nil`

#### Description

Reads a line from the input port and stores the line as a string in the variable. This is a macro.

The string is also returned as the value of`gets`. The terminating newline character of the line becomes the last character in the string.

#### Arguments

|  |
| --- | ---
| `s_variableName` | Variable to store input string in.
|  |
| --- | ---
| `p_inputPort` | Name of input port;`piport` is used if none is given.
#### Value Returned

|  |
| --- | ---
| `t_string` | Returns the input string when successful.
|  |
| --- | ---
| `nil` | When EOF is reached. `s_variableName` stores the last value returned (that is, `nil`).
#### Example

Assume the`test1.data` file has the following first two lines:

`#This is the data for test1    0001 1100 1011 0111`

```
p = infile("test1.data")     => port:"test1.data"gets(s p)                    => "#This is the data for test1\n"gets(s p)                    => "0001 1100 1011 0111\n"s                            => "0001 1100 1011 0111\n"
```

#### Reference

`getc, getchar, infile`

### include

`include(t_file)=> t/error`

#### Description

Loads the file with name`t_file` in SKILL regardless of any errors in the file.

#### Arguments

|  |
| --- | ---
| `t_file` | Name of the file you want to load; it should be a string value.
#### Value Returned

|  |
| --- | ---
| `t` | The file loads sucessfully.
|  |
| --- | ---
| `error` | The file specified as`t_file` does not exist.
#### Example 1

`include("./test.il")`

`t`

#### Example 2

`include("")`

`*WARNING* open : empty file name`

`*Error* include: can't access file - ""`

### infile

`infile( S_fileName ) => p_inport | nil`

#### Description

Opens an input port ready to read a file.Always remember to close the port when you are done.

The file name can be specified with either an absolute path or a relative path. In the lattercase, current SKILL path is used if it's not `nil`. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

**Note:** Always remember to close the port when you are done.

#### Arguments

|  |
| --- | ---
| `S_fileName` | Name of the file to be read; it can be either a string or a symbol.
#### Value Returned

|  |
| --- | ---
| `p_inport` | Port opened for reading the named file.
|  |
| --- | ---
| `nil` | The file does not exist or cannot be opened for reading.
#### Example

`in = infile("~/test/input.il") => port:"~/test/input.il"`

If such a file exists and is readable.

`infile("myFile") => nil`

If`myFile` does not exist according to the current setting of the SKILL path or exists but is not readable.

`close(in) => t`

#### Reference

`close, isFileName, isReadable, outfile, portp`

### info

`info( t_formatString [ g_args1... ]) => nil`

#### Description

Prints the formatted output to poport according to the specification.

#### Arguments

|  |
| --- | ---
| `r_formatString` | Format specification string.
|  |
| --- | ---
| `g_args` | Arguments following the format string.
#### Value Returned

|  |
| --- | ---
| `nil` | Prints the argument value to poport.
#### Example1

`info("Hello Skill") ; prints "Hello Skill"Hello Skillnil`

#### Example2

`info("value = %d" 42) ; prints value = 42value = 42nil`

### inportp

`inportp( g_obj ) => t | nil`

#### Description

Checks if an object is an input port.

**Note:** An input port may be closed, so if`inportp` returns `t`, that does not guarantee a successful read from the port.

#### Arguments

|  |
| --- | ---
| `g_obj` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | The given object is an input port.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`(inportp piport)   => t(inportp poport)   => nil(inportp 123)      => nil`

#### Reference

`outportp`

### instring

`instring( t_string ) => p_port`

#### Description

Opens a string for reading, just as infile would open a file.

An input port that can be used to read the string is returned.*Always remember to close* *the port when you are done*.

#### Arguments

|  |
| --- | ---
| `t_string` | Input string opened for reading.
#### Value Returned

|  |
| --- | ---
| `p_port` | Port for the input string.
#### Example

```
s = "Hello World!"       => "Hello World!"p = instring(s)          => port:"*string*"fscanf(p "%s %s" a b)    => 2a                        => "Hello"b                        => "World!"close(p)=> t
```

#### Reference

`gets, infile`

### isExecutable

`isExecutable( S_name [ tl_path ] ) => t | nil`

#### Description

Checks if you have permission to execute a file or search a directory.

A directory is executable if it allows you to name that directory as part of your path insearching files. It uses the current SKILL path for relative paths. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Name of the file or directory you want to check for execution/search permission.
|  |
| --- | ---
| `tl_path` | List of paths that overrides the SKILL path.
#### Value Returned

|  |
| --- | ---
| `t` | If you have permission to execute the file or search the directoryspecified by `S_name`.
|  |
| --- | ---
| `nil` | The directory does not exist or you do not have the requiredpermissions.
#### Example

```
isExecutable("/bin/ls")      => t isExecutable("/usr/tmp")     => t isExecutable("attachFiles")  => nil
```

Result if`attachFiles` does not exist or is non-executable.

#### Reference

`isFile, isReadable, isWritable`

### isFile

`isFile( S_name [ tl_path ] ) => t | nil`

#### Description

Checks if a file exists and that it is not a directory.

Identical to`isFileName`, except that directories are not viewed as (regular) files. Uses the current SKILL path for relative paths. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

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
| `t` | The`S_name` file exists.
|  |
| --- | ---
| `nil` | The`S_name` file does not exist.
#### Example

`isFile( "DACLib") => nil`

Assumes`DACLib` is a directory and `triadc` is a file in the current working directory and the SKILL path is `nil`. A directory is not viewed as a file in this se.

`isFile( "triadc") => tisFile( ".cshrc" list("." "~")) => t`

#### Reference

`isFileName, getSkillPath`

### isFileEncrypted

`isFileEncrypted( S_name ) => t | nil`

#### Description

Checks if a file exists and is encrypted.

Similar to`isFile`, except that it returns `t` only if the file exists and is encrypted. Uses the current SKILL path for relative paths. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | File you want to check.
#### Value Returned

|  |
| --- | ---
| `t` | The`S_name` file exists and is encrypted.
|  |
| --- | ---
| `nil` | The`S_name` file does not exist or is not encrypted.
#### Example

```
isFileEncrypted( "~/testfns.il") => nil encrypt( "~/testfns.il" "~/testfns.ile")isFileEncrypted( "~/testfns.ile") => t
```

#### Reference

`getSkillPath, isFile`

### isFileName

`isFileName( S_name [ tl_path ] ) => t | nil`

#### Description

Checks if a file or directory exists.

The file name can be specified with either an absolute path or a relative path. In the lattercase, current SKILL path is used if it's not `nil`. Only the presence or absence of the name is checked. If found, the name can belong to either a file or a directory. `isFileName` differs from `isFile` in this regard. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Path you want to check.
|  |
| --- | ---
| `tl_path` | List of paths to override the SKILL path.
#### Value Returned

|  |
| --- | ---
| `t` | The`S_name` path exists.
|  |
| --- | ---
| `nil` | The`S_name` path does not exist.
#### Example

Suppose`DACLib` is a directory and `triadc` is a file in the current working directory and the SKILL path is `nil`.

`isFileName("DACLib") => t`

A directory is just a special kind of file.

`isFileName("triadc") => tisFileName("triad1") => nil`

Result if`triad1` does not exist in current working directory.

`isFileName( ".cshrc" list("." "~")) => t`

#### Reference

`isFile, getSkillPath`

### isLargeFile

`isLargeFile(S_name [ tl_path ] ) => t | nil`

#### Description

Checks if a file is a large file (with size greater than 2GB).

The file name can be specified with either an absolute path or a relative path. In the lattercase, the current SKILL path is searched if it's not nil. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

The SKILL path can be overriden by specifying`tl_path`.

#### Arguments

|  |
| --- | ---
| `S_name` | Name of the file you want to check.
|  |
| --- | ---
| `tl_path` | List of paths to override the SKILL path.
#### Value Returned

|  |
| --- | ---
| t | The`S_name` file has a size greater than 2GB.
|  |
| --- | ---
| nil | The`S_name` file has a size less than or equal to 2GB.
#### Example

`fileLength( "largeFile" ) => 3072000000`

`isLargeFile( "largeFile" ) => t`

#### Reference

`fileLength, isFile, isFileName`

### isLink

`isLink( S_name [ tl_path ] ) => t | nil`

#### Description

Checks if a path exists and if it is a symbolic link.

When`S_name` is a relative path, the current SKILL path is used if it's non-`nil`. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Path you want to check.
|  |
| --- | ---
| `tl_path` | List of paths that override the SKILL path.
#### Value Returned

|  |
| --- | ---
| `t` | The name exists and it is a symbolic link.
|  |
| --- | ---
| `nil` | The name exists and is not a symbolic name or if`S_name` does not exist at all.
#### Example

`isLink("/usr/bin")=> nil`

`isLink("/usr/spool")=> t    ;Assuming it's a link to /var/spool`

#### Reference

`isFile`

### isPortAtEOF

`isPortAtEOF(p_port)=> t | nil`

#### Description

Takes an input port and returns`t` if end-of-file (EOF) has previously been detected while reading the input port; it returns `nil` otherwise.

#### Arguments

|  |
| --- | ---
| `p_port` | Input port. This must be open, otherwise the function will returnan error.
#### Value Returned

|  |
| --- | ---
| `t` | End-of-file (EOF) has previously been detected while reading theinput port `p_port`.
|  |
| --- | ---
| `nil` | End-of-file (EOF) has not been reached yet.
#### Example

`port = infile("input_file")`

`while(! isPortAtEOF(port)`

`printf("%L\n" read(port))`

`)`

`close(port)`

### isReadable

`isReadable( S_name [ tl_path ] ) => t | nil`

#### Description

Checks if you have permission to read a file or list a directory.Uses the current SKILL path for relative paths. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Name of a file or directory you want to know your accesspermissions on.
|  |
| --- | ---
| `tl_path` | List of paths to override the SKILL path.
#### Value Returned

|  |
| --- | ---
| `t` | If`S_name` exists and you have permission to read it (for files) or list the contents (for directories).
|  |
| --- | ---
| `nil` | The file does not exist or does exist, but you do not have permission to read it.
#### Example

`isReadable("./") => t`

Result if current working directory is readable.

`isReadable("~/DACLib") => nil`

Result if*"*`~/DACLib`*"* is not readable or does not exist.

#### Reference

`infile, isExecutable, isFile, isWritable`

### isWritable

`isWritable( S_name [ tl_path ] ) => t | nil`

#### Description

Checks if you have permission to write to a file or update a directory.Uses the current SKILL path for relative paths. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments

|  |
| --- | ---
| `S_name` | Name of a file or directory you want to find out your writepermission on.
|  |
| --- | ---
| `tl_path` | List of paths to search that overrides the SKILL path.
#### Value Returned

|  |
| --- | ---
| `t` | If`S_name` exists and you have permission to write or update it.
|  |
| --- | ---
| `nil` | The file does not exist or does exist, but you do not have permission to read it.
#### Example

`isWritable("/tmp")=> t isWritable("~/test/out.1") => nil`

Result if`out.1` does not exist or there is no write permission to it.

#### Reference

`isExecutable, isFile, isReadable`

### lineread

`lineread( [ p_inputPort ] ) => t | nil | l_results`

#### Description

Parses the next line in the input port into a list that you can further manipulate.It is used bythe interpreter's top level to read in all input and understands SKILL and SKILL++ syntax.

Only one line of input is read in unless there are still open parentheses pending at the end ofthe first line, or binary `infix` operators whose right-hand argument has not yet been supplied, in which case additional input lines are read until all open parentheses have been closed and all binary `infix` operators satisfied. The symbol `t` is returned if `lineread` reads a blank input line and `nil` is returned at the end of the input file.

#### Arguments

|  |
| --- | ---
| `p_inputPort` | Input port. The default is piport.
#### Value Returned

|  |
| --- | ---
| `t` | If the next line read in is blank.
|  |
| --- | ---
| `nil` | If the input port is at the end of file.
|  |
| --- | ---
| `l_results` | Otherwise returns a list of the objects read in from the next(logical) input line
#### Example

```
lineread(piport)       ; Reads in the next input expressionf 1 2 +                ; First input line of the file being read3                      ; Second input line=> (f 1 (2 + 3))
```

```
lineread(piport)f(a b c)               ; Another input line of the file=> ((f a b c))         ; Returns a list of input objects
```

#### Reference

`gets, infile, linereadstring`

### linereadstring

`linereadstring( t_string ) => g_value | nil`

#### Description

Executes`lineread` on a string and returns the first form read in. Anything after the first form is ignored.

#### Arguments

|  |
| --- | ---
| `t_string` | Input string.
#### Value Returned

|  |
| --- | ---
| `g_value` | The first form (line) read in from the argument string.
|  |
| --- | ---
| `nil` | No form is read (that is, the argument string is all spaces).
#### Example

```
linereadstring "abc"                  => (abc)linereadstring "f a b c"              => (f a b c)linereadstring "x + y"                => ((x + y))linereadstring "f a b c\n g 1 2 3"    => (f a b c)
```

> In the last example, only the first form is read in.

#### Reference

`evalstring, gets, instring, lineread`

### load

`load( t_fileName [ t_password ] ) => t`

#### Description

Opens a file, repeatedly calls`lineread` to read in the file, immediately evaluating each form after it is read in. Uses the file extension to determine the language mode (`.il` for SKILL and `.ils` for SKILL++) for processing the language expressions contained in the file. For a SKILL++ file, the loaded code is always evaluated in the top level environment.

It closes the file when end of file is reached. Unless errors are discovered, the file is read inquietly. If `load` is interrupted by pressing `Control-c`, the function skips the rest of the file being loaded.

This function uses the file extension to determine the language mode (`.il` for SKILL and `.ils` for SKILL++) for processing the language expressions contained in the file.

SKILL has an autoload feature that allows applications to load functions into SKILL ondemand. If a function being executed is undefined, SKILL checks to see if the name of the function (a symbol) has a property called `autoload` attached to it. If the property exists, its value, which must be either a string or an expression that evaluates to a string, is used as the name of a file to be loaded. The file should contain a definition for the function that triggered the autoload. Execution proceeds normally after the function is defined.

#### Arguments

|  |
| --- | ---
| `t_fileName` | File to be loaded. Uses the file name extension to determine thelanguage mode to use.  Valid values:
|  |
| --- | ---
| `'ils` | Means the file contains SKILL++ code.
| `'il` | Means the file contains SKILL code.
|  |
| --- | ---
| `t_password` | Password, if`t_fileName` is an encrypted file.
#### Value Returned

|  |
| --- | ---
| `t` | The file is successfully loaded.
#### Example

```
load( "testfns.il")             ; Load file testfns.ilfn.autoload = "myfunc.il"       ; Declares an autoload property.fn(1)
```

`fn` is undefined at this point, so this call triggers an autoload of`myfunc.il`, which contains the definition of `fn`. The function call `fn(1)` is then successfully performed.

`fn(2)      ; fn is now defined and executes normally.`

You might have an application partitioned into two files. Assume that`UtilsA.il` contains classic SKILL code and `UtilsB.ils` contains SKILL/SKILL++ code. The following example loads both files appropriately.

```
procedure( trLoadSystem()    load( "UtilsA.il" )    ;;; SKILL code    load( "UtilsB.ils" )   ;;; SKILL++ code    )                     ; procedure
```

#### Reference

`include, loadContext, loadi, lineread`

### loadi

`loadi( t_fileName [ t_password ] ) => t`

#### Description

Identical to`load`, except that `loadi` ignores errors encountered during the load, prints an error message, and then continues loading.

Opens the named file, repeatedly calls`lineread` to read in the file, immediately evaluates each form after it is read in, then closes the file when end of file is reached. Unlike `load`, `loadi` ignores errors encountered during the load. Rather than stopping, `loadi` causes an error message to be printed and then continues to end of file. Otherwise, `loadi` is the same as `load`.

#### Arguments

|  |
| --- | ---
| `t_fileName` | File to be loaded, with the proper extension to specify thelanguage mode.
|  |
| --- | ---
| `t_password` | Password, if`t_fileName` is an encrypted file.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

`loadi( "testfns.il" )`

Loads the`testfns.il` file.

`loadi( "/tmp/test.il")`

Loads the`test.il` file from the `tmp` directory.

#### Reference

`encrypt, include, load, lineread`

### loadPort

```
loadPort( p_port [?langMode g_langMode][?password g_password][?ignoreErrors g_ignoreErrors])) => t
```

#### Description

Loads a SKILL file from`p_port`.

#### Arguments

|  |
| --- | ---
| `p_port` | An input (SKILL) port.
|  |
| --- | ---
| `g_langMode` | Specifies the language mode to use regardless of the original fileextension.  Valid values:
|  |
| --- | ---
|  |
|  |
| --- | ---
| `'ils` | Loads the file in SKILL++ mode.
| `'il` | Loads the file in SKILL mode.
|  |
| --- | ---
|  | Default is`'il`.
|  |
| --- | ---
| `g_password` | Password, if the file is encrypted.
|  |
| --- | ---
| `g_ignoreErrors` | If specified, ignores errors during load.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

`` loadPort( myPort ?langMode `ils ) ``

### loadstring

`loadstring( t_string [ s_langMode ] ) => t`

#### Description

Opens a string for reading, then parses and executes expressions stored in the string, just as`load` does in loading a file.

**Note:** `loadstring` is different from `evalstring` in two ways: (1) it uses `lineread` mode, and (2) it always returns `t` if it evaluates successfully.

#### Arguments

|  |
| --- | ---
| `t_string` | Input string to be evaluated.
|  |
| --- | ---
| `s_langMode` | Must be a symbol. Valid values:
|  |
| --- | ---
| `'ils` | Means the file contains SKILL++ code.
| `'il` | Means the file contains SKILL code.
#### Value Returned

|  |
| --- | ---
| `t` | When`t_string` has been successfully read in and evaluated.
|  |
| --- | ---
|  | Signals an error if`t_string` is not a string, or contains ill-formed SKILL expressions.
#### Example

```
loadstring "1+2"                      => tloadstring "procedure( f(y) x=x+y )"  => tloadstring "x=10\n f 20\n f 30"       => tx                                     => 60
```

#### Reference

`evalstring, instring, load, gets`

### outstring

`outstring( ) => p_openedPort/nil`

#### Description

Takes no arguments and returns an opened output port for strings (or an outport). After a portis opened, it can be used with functions, such as `fprintf`, `println`, and `close` that write to an output port. You need to use the `getOutstring` function to retrieve the content of output port (while it is open).

You can use the`close` function to close the output port.

#### Arguments

|  |
| --- | ---
| Takes no arguments |
#### Value Returned

|  |
| --- | ---
| `p_openedPort` | The opened output port
|  |
| --- | ---
| `nil` | Returns`nil` if the port cannot be opened
#### Example

`s = outstring() ; string port opened for output`

`=> port:s`

`fprintf(s "the value is %d" 1) ; fprintf into string`

`getOutstring(s)`

`=>the value is 1`

`close(s)`

`getOutstring(s)`

`=> nil`

### makeTempFileName

`makeTempFileName( S_nameTemplate ) => t_name`

#### Description

Appends a string suffix to the last component of a path template so that the resultingcomposite string does not duplicate any existing file name.

That is, it checks that such named file does not exist. SKILL path is not used in this checking.

**Note:** Successive calls to`makeTempFileName` return different results only if the first name returned is actually used to create a file in the same directory before a second call is made.

The last component of the resultant path is guaranteed to be no more than 14 characters. Ifthe original template has a long last component it is truncated from the end if needed. Also, any trailing `X`'s (uppercase only) are removed from the template before the new string suffix is appended. You are encouraged to follow the convention of placing temporary files in the
`/tmp` directory on your system.

#### Arguments

|  |
| --- | ---
| `S_nameTemplate` | Template file name as a string or a symbol.
#### Value Returned

|  |
| --- | ---
| `t_name` | Path that can be used to create a file or directory.
#### Example

`d = makeTempFileName("/tmp/testXXXX")  => "/tmp/testa00324"`

Trailing`X`'s (uppercase only) are removed.

`createDir(d)                            => t`

The name is used this time.

`makeTempFileName("/tmp/test")          => "/tmp/testb00324"`

A new name is returned this time.

### newline

`newline( [ p_outputPort ] ) => nil`

#### Description

Prints a newline (`\n`) character and then flushes the output port.

#### Arguments

|  |
| --- | ---
| `p_outputPort` | Output port. Defaults to `poport`, the standard output port.
#### Value Returned

|  |
| --- | ---
| `nil` | Prints a newline and then returns`nil`.
#### Example

`print("Hello") newline() print("World!")"Hello""World!"=> nil`

#### Reference

`drain, fprintf, outfile`

### numOpenFiles

`numOpenFiles( ) => ( x_current x_maximum )`

#### Description

Returns the number of files now open and the maximum number of files that a process canopen. The numbers are returned as a two-element list.

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `x_current` | Number of files that are currently open.
|  |
| --- | ---
| `x_maximum` | Maximum number of files that a process can open. This isusually platform-dependent.
#### Example

`numOpenFiles()            => (6 64)`

Result is system-dependent.

`f = infile("/dev/null")   => port:"/dev/null"numOpenFiles()            => (7 64)`

One more file is open now.

#### Reference

`close, infile, outfile`

### openportp

`openportp( g_obj ) => t | nil`

#### Description

Checks if the given argument is a port object and it is open (for input or output),`nil` otherwise.

#### Arguments

|  |
| --- | ---
| `g_obj` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_obj` is a port and it is open for input or output.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

```
(portp ip = (infile "inFile")) => t(portp op = (outfile "outFile")) => t(openportp ip) => t(openportp op) => t(close ip) => t(openportp ip) => nil(close op) => t(openportp op) => nil
```

### outfile

`outfile( S_fileName [ t_mode ] [ g_openHiddenFile ]) => p_outport | nil`

#### Description

Opens an output port ready to write to a file.

The file can be specified with either an absolute path or a relative path. If a relative path isgiven and the current SKILL path setting is not `nil`, all directory paths from SKILL path are checked in order, for that file. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path. If found, the system overwrites the first updatable file in the list. If no updatable file is found, it places a new file of that name in the first writable directory.

If the optional`g_openHiddenFile` argument (which is intended to be used on Windows only) is specified, the system will be forced to open a Windows hidden file. The `g_openHiddenFile` must be used for openning existing Windows hidden files only. If the named Windows hidden file does not exist (including the current SKILL path), `outfile`will fail. In addition, the `t_mode` option must also be specified (to either `w` or `a` only) if `g_openHiddenFile` is given.

#### Arguments

|  |
| --- | ---
| `S_fileName` | Name of the file to open or create.
|  |
| --- | ---
| `t_mode` | If the mode string`t_mode` is specified, the file is opened in the mode requested. If `t_mode` is `a`, an existing file is opened in append mode. If it is `w`, a new file is created for writing (any existing file is overwritten). The default is `w`.
|  |
| --- | ---
| `g_openHiddenFile` | If specified to non-nil, the named Windows hidden file is forcedto open. This argument must be used for Windows hidden files only.
#### Value Returned

|  |
| --- | ---
| `p_outport` | An output port ready to write to the specified file.
|  |
| --- | ---
| `nil` | If the named file cannot be opened for writing or the namedWindows hidden file does not exist (including the current SKILL path).
|  |
| --- | ---
|  | An error is signaled if an illegal mode string is supplied.
#### Example

```
p = outfile("/tmp/out.il" "w")    => port:"/tmp/out.il"outfile("/bin/ls")                => nil
```

`outfile( "aHiddenFile" "w" t)`

To force opening a Windows hidden file`t_mode` must also be specified.

#### Reference

`close, drain, getSkillPath, infile`

### outportp

`outportp( g_obj ) => t | nil`

#### Description

Checks if an object is an output port.

**Note:** An output port may be closed, so if`outportp` returns `t`, that does not guarantee a successful write to the port.

#### Arguments

|  |
| --- | ---
| `g_obj` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | The given object is an output port.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`(outportp poport)    => t(outportp piport)    => nil(outportp 123)       => nil`

#### Reference

`inportp`

### portp

`portp( g_value ) => t | nil`

#### Description

Checks if an object is an input or output port.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A data object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is an input or output port, whose type name is `port`.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`portp( piport )    => tportp( 3.0 )       => nil`

#### Reference

`infile, outfile`

### pprint

`pprint( g_value [ p_outputPort ] ) => nil`

#### Description

Identical to`print` except that it pretty prints the value whenever possible.

The`pprint` function is useful, for example, when printing out a long list where `print` simply prints the list on one (possibly huge) line but `pprint` will limit the output on a single line and produce a multiple line printout if necessary. This s the output much more readable.

`pprint` does not work the same as the `pp` function. `pp` is an `nlambda` and only takes a function name whereas `pprint` is a `lambda` and takes an arbitrary SKILL object.

#### Arguments

|  |
| --- | ---
| `g_value` | Any SKILL value to be printed.
|  |
| --- | ---
| `p_outputPort` | Output port to print to. Default is`poport`.
#### Value Returned

|  |
| --- | ---
| `nil` | Prints the argument value (to the given port).
#### Example

```
pprint '(1 2 3 4 5 6 7 8 9 0 a b c d e f g h i j k) (1 2 3 4 5    6 7 8 9 0    a b c d e    f g h i j    k)=> nil
```

#### Reference

`pp, print`

### print

`print( g_value [ p_outputPort ] ) => nil`

#### Description

Prints a SKILL object using the default format for the data type of the value.

For example, strings are enclosed in double quotes. Same as `println`, except no newline character is printed.

#### Arguments

|  |
| --- | ---
| `g_value` | Any SKILL object.
|  |
| --- | ---
| `p_outputPort` | Output port to print to. Default is `poport`.
#### Value Returned

|  |
| --- | ---
| `nil` | Always returns`nil` after printing out the object supplied.
#### Example

`print("hello")"hello"=> nil`

#### Reference

`pprint, println, printlev`

### printf

`printf( t_formatString [ g_arg1 ... ] ) => t`

#### Description

Writes formatted output to`poport`.

The optional arguments following the format string are printed according to theircorresponding format specifications. Refer to the "[Common Output Format Specifications](#1039050 "Input Output Functions")" table on the `fprintf` manual page.

`printf` is identical to `fprintf` except that it does not take the `p_port` argument and the output is written to `poport`.

#### Arguments

|  |
| --- | ---
| `t_formatString` | Characters to be printed verbatim, intermixed with formatspecifications prefixed by the % sign.
|  |
| --- | ---
| `g_arg1` | Arguments following the format string are printed according totheir corresponding format specifications.
#### Value Returned

|  |
| --- | ---
| `t` | Prints the formatted output and returns`t`.
#### Example

`x = 197.9687 => 197.9687printf("The test measures %10.2f.\n" x)`

Prints the following line to`poport` and returns `t`.

`The test measures            197.97. => t`

#### Reference

`fprintf, println`

### printlev

`printlev( g_value x_level x_length [ p_outputPort ] ) => nil`

#### Description

Prints a list with a limited number of elements and levels of nesting.

Lists are normally printed in their entirety no matter how many elements they have or howdeeply nested they are. Applications have the option, however, of setting upper limits on the number of elements and the levels of nesting shown when printing lists. These limits are sometimes necessary to control the volume of interactive output because the SKILL top-level automatically prints the results of expression evaluation. Limits can also protect against the infinite looping on circular lists possibly created by programming mistakes.

