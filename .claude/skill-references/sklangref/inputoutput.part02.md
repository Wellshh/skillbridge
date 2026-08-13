<!--
source: sklangref/inputoutput.md
part: 2/2
estimated_tokens: 2862
-->

Two integer variables, print length and print level (specified by`x_length` and `x_level`), control the maximum number of elements and the levels of nesting that are printed. List elements beyond the maximum specified by print length are abbreviated as "`...`" and lists nested deeper than the maximum level specified by print level are abbreviated as `&`. Both print length and print level are initialized to `nil` (meaning no limits are imposed) by SKILL, but each application is free to set its own limits.

The`printlev` function is identical to `print` except that it takes two additional arguments specifying the maximum level and length to be used in printing the expression.

#### Arguments

|  |
| --- | ---
| `g_value` | Any SKILL value.
|  |
| --- | ---
| `x_level` | Specifies the level of nesting that you want to print; lists nesteddeeper than the maximum level specified are abbreviated as "&".
|  |
| --- | ---
| `x_length` | Specifies the length (or maximum number of elements) you wantto print. List elements beyond the maximum specified here are abbreviated as "`...`".
|  |
| --- | ---
| `p_outputPort` | Output port. Default is`poport`.
#### Value Returned

|  |
| --- | ---
| `nil` | Prints the argument value and then returns`nil`.
#### Example

```
List = '(1 2 (3 (4 (5))) 6)=> '(1 2 (3 (4 (5))) 6)printlev(List 100 2)(1 2 ...)=> nil
```

`printlev(List 3 100)(1 2 (3 (4 &)) 6)=> nil`

```
printlev(List 3 3 p)            ; Assumes port p exists.(1 2 (3 (4 &)) ...)             ; Prints to port p.=> nil
```

#### Reference

`list, print`

### println

`println( g_value [ p_outputPort ] ) => nil`

#### Description

Prints a SKILL object using the default format for the data type of the value, then prints anewline character.

A newline character is automatically printed after printing`g_value`. `println` flushes the output port after printing each newline character.

#### Arguments

|  |
| --- | ---
| `g_value` | Any SKILL value.
|  |
| --- | ---
| `p_outputPort` | Port to be used for output. The default is`poport`.
#### Value Returned

|  |
| --- | ---
| `nil` | Prints the given object and returns`nil`.
#### Example

```
for( i 1 3 println( "hello" ))    ;Prints hello three times."hello""hello""hello"=> t                             ;for always returns t
```

#### Reference

`drain, print, newline`

### putc

`putc(x_symbolp_port)`

`=> s_symbol`

#### Description

Puts the`x_symbol` to `p_port` (to complement getc function)

#### Arguments

|  |
| --- | ---
| `x_symbol` | Symbol number
|  |
| --- | ---
| `p_port` | An output port
|  |
| --- | ---
|  |
#### Value Returned

|  |
| --- | ---
| `s_symbol` | The symbol that was put
#### Example

`putc(1 poport)`

`=> \001`

### read

`read( [ p_inputPort ] ) => g_result | nil | t`

#### Description

Parses and returns the next expression from an input port.

Returns the next expression regardless of how many lines the expression takes up - even ifthere are other expressions on the same line. If the next line is empty, returns `t`. If the port is positioned at end of file, then it returns `nil`.

#### Arguments

|  |
| --- | ---
| `p_inputPort` | Input port. Default is`piport`.
#### Values Returned

|  |
| --- | ---
| `g_result` | The object read in.
|  |
| --- | ---
| `nil` | When the port is at the end of file.
|  |
| --- | ---
| `t` | If an empty line is encountered.
#### Example

Suppose the file`SkillSyntaxFile.il`contains the following expressions. Note that a blank line follows the second expression:

```
define( x 1 )define( y 2 )procedure( add( x y ) x+y )myPort = infile( "SkillSyntaxFile.il" )                     => port:SkillSyntaxFile.il"read( myPort )      => define(x 1)read( myPort )      => define(y 2)read( myPort )      => tread( myPort )      => procedure((add x y) (x + y ) )read( myPort )      => nilclose( myPort )     => t
```

#### Reference

`lineread`

### readTable

`readTable( S_fileName o_table ) => t | nil`

#### Description

Reads and appends the contents of a file to an existing association table.

#### Prerequisites

The file submitted must have been created with the`writeTable` function so that the contents are in a usable format.

#### Arguments

|  |
| --- | ---
| `S_fileName` | File name (either a string or symbol) from which to read the data.
|  |
| --- | ---
| `o_table` | Association table to which the file contents are appended.
#### Value Returned

|  |
| --- | ---
| `t` | The data is read and appended.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

```
myTable = makeTable("table1")    => table:table1myTable2 = makeTable("table2")   => table:table2myTable["three"] = 3             => 3writeTable("table.out" myTable)  => treadTable("table.out" myTable2)  => t
```

#### Reference

`makeTempFileName, writeTable`

### renameFile

`renameFile( S_old S_new ) => t | nil`

#### Description:

The`renameFile``()` function changes the name of a file or directory.The `S_old` argument points to the pathname of the file or directory to be renamed. The `S_new` argument points to the new pathname of the file or directory. If the SKILL path is nil, `renameFile``()` would search the current directory. Otherwise, the SKILL path would be searched first for `S_old`. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

#### Arguments:

|  |
| --- | ---
| `S_old` | Points to the pathname of the file or directory to be renamed.
|  |
| --- | ---
| `S_new` | Points to the new pathname of the file or directory.
#### Value Returned

|  |
| --- | ---
| `t` | File or directory is successfully re-named.
|  |
| --- | ---
| `nil` | If`S_old` path does not exist.
**Note:** If you do not have sufficient privileges to rename a file or directory, the`renameFile()`function throws an error (neither returns `t`nor `nil`). You can use the `errset()`function to handle such exceptional situations. For more information on the `errset()` function, see [The errset Function](../sklanguser/chap9.html#errset) in the *Cadence SKILL Language User Guide*.

#### Example

`renameFile( "/usr/oldname" "/usr/newName" ) => t`

`renameFile( "/usr/old" "/usr/new" ) => nil ;if old does not exist.`

`renameFile( "old" "new" ) ;if old is a file while new is a directory`

`*Error* renameFile: is a directory`

```
renameFile( "/usr/old" "/usr/new" ) ; if you do not have permissions to rename old
```

`*Error* renameFile: permission denied`

### simplifyFilename

`simplifyFilename( t_name [ g_dontResolveLinks ]) => t_result`

#### Description

Expands the name of a file to its full path.

Returns the fully expanded name of the file`t_name`. Tilde expansion is performed, "./" and "../" are compressed, and redundant slashes are removed. By default, symbolic links are also resolved, unless the second (optional) argument `g_notResolveLinks` is specified to non-nil.

If`t_name` is not absolute, the current working directory is prefixed to the returned file name.

#### Arguments

|  |
| --- | ---
| `t_name` | File to be fully expanded.
|  |
| --- | ---
| `g_dontResolveLinks` | If specified to non-nil, symbolic links are not resolved.
#### Value Returned

|  |
| --- | ---
| `t_result` | Fully expanded name of the file.
#### Example

`simplifyFilename("~/test") => "/usr/mnt/user/test"`

Assumes the user's home directory is`/usr/mnt/user`.

`simplifyFilename( "/tmp/fileName" t) => "/tmp/fileName"`

Assumes`/tmp/fileName` is a symbolic link of `/tmp/fileName.real`.

#### Reference

`isFileName`

### truename

`truename( t_string ) => t_truename`

#### Description

Tries to find the specified file (`t_string`) and returns its truename.

#### Arguments

|  |
| --- | ---
| `t_string` | A string specifying the file name or file path.
#### Value Returned

|  |
| --- | ---
| `t_truename` | The truename of the specified file.
#### Example

```
truename("./runtest")=> "/export/home/opt/cds/CAT32/lnx86/latest.il.32bit/tools.lnx86/dfII/test/il1/runtest"
```

`truename("~/old/cdb")`

`=> nil ; this file/directory does not exist`

`truename("~")`

`=> "/home/deeptik"`

`truename("tmp")`

#### "/home/deeptik/tmp"

#### Reference

`which`

### which

`which( t_fileName ) => t_fullPath | nil`

#### Description

Returns the absolute path of the given context file, or regular file or directory.

The main usage of this function is to load prerequisite context files.

If`t_fileName` identifies a context file (that is with the `.cxt` extension), it looks under the standard contexts location (associated with the application in which this function is called), as well as common Cadence contexts directory, `your_install_path/tools/dfII/etc/``context`, and user contexts location, `youre_install_path/tools/dfII/local/``context`, for the presence of the context file.

If`t_fileName` identifies a regular file or directory, the current SKILL path is searched. Note that a path which is anchored to current directory, for example, `./`, `../`, or `../../..`, etc., is not considered as a relative path.

**Note:** `t_fileName` should be a simple file or directory name, and should not contain directory separators.

#### Arguments

|  |
| --- | ---
| `t_fileName` | Name of a context file, or a regular file or directory that you wantto get the absolute path.
#### Value Returned

|  |
| --- | ---
| `t_fullPath` | The absolute path of`t_fileName`.
|  |
| --- | ---
| `nil` | If`t_fileName` is not found.
#### Example

Loading a prerequisite context file:

`loadContext( which( "myPrereq.cxt" ) ) => t`

Get the absolute path of a file:

`which( ".cdsinit" ) => "/usr/deeptik/.cdsinit"`

#### Reference

`truename`

### write

`write( g_value [ p_outputPort ] ) => nil`

#### Description

Prints a SKILL object using the default format for the data type of the value.

For example, strings are enclosed in ". Same as`print`.

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
| `nil` | Always returns`nil`, after it prints out the object supplied to it.
#### Example

```
for( i 1 3 write( "hello" ))    ;Prints hello three times."hello""hello""hello"=> t
```

#### Reference

`display, pprint, print, println, printlev`

### writeTable

`writeTable( S_fileName o_table ) => t | nil`

#### Description

Writes the contents of an association table to a file with one key/value pair per line.

**Note:** This function is for writing basic SKILL data types that are stored in an associationtable. The function cannot write database objects or other user-defined types that might be stored in association tables.

#### Arguments

|  |
| --- | ---
| `S_fileName` | Name of the print file (either a string or symbol) to which the tablecontents are to be written.
|  |
| --- | ---
| `o_table` | Association table from which the data is accessed.
#### Value Returned

|  |
| --- | ---
| `t` | If the data is successfully written to the file.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`writeTable("inventory" myTable)    => twriteTable(noFile myTable)         => nil`

#### Reference

[makeTempFileName](#1040047 "Input Output Functions"), [readTable](#1040392 "Input Output Functions")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
