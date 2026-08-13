### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

22
==

Allegro PCB Editor File Access Functions
========================================

AXL-SKILL File Access Functions
-------------------------------

This chapter describes the AXL-SKILL functions that open and close Allegro PCB Editor files.

* Use these functions, instead of SKILL's infile and outfile, to access files using Allegro PCB Editor standards, not via the SKILL path.

### axlDMFileError

`axlDMFileError() -> nil/t_errorMessage`

#### Description

This returns the error from the last`axlDM`xxx call. Subsequent calls reset the error message so you should retrieve the error as soon as a call fails.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `nil` | No error message available.
| `t_errorMessage` | Message indicating why last operation failed.
#### See Also

[axlDMOpenFile](#38826 "22")

#### Example

> `q = axlDMOpenFile("TEMP" "foo.bar" "r")`

> `unless(q`

> `printf("ERROR is %L\n" axlDMFileError()))`

### axlDMFindFile

`axlDMFindFile (t_idt_namet_mode[t_prop])⇒ t_name/nil`

#### Description

Opens a file using Allegro PCB Editor conventions. Adds an extension and optionally looks it up in an Allegro PCB Editor search path.

**Note:** Must have an entry in`fileops.txt` file.

#### Arguments

|  |
| --- | ---
| `t_id` | Id describing file attributes from`fileops.txt`
| `t_name` | Name of file to find.
| `t_mode` | Open mode. One of the following:  `r:`read-only  `w:`write  `wf:` write line-buffered
|
|
|
| `t_prop` | Property string.
#### Value Returned

|  |
| --- | ---
| `t_name` | Name of file opened.
| `nil` | Failed to open file.
#### See Also

[axlDMOpenFile](#38826 "22")

#### Example

> `(setq aPort(axlDMFindFile "ALLEGRO_TEXT","clip","w",":HELP=clipboard"))`

Finds the fully qualified name`clip.txt` for writing.

### axlDMGetFile

`axlDMGetFile(t_idt_namet_mode[t_prop]`

`)`

`⇒ t_name/nil`

#### Description

Gets the file name`t_name` using Allegro PCB Editor conventions as described in the arguments. Returns the full path name of the file. Displays an error message if the file cannot be opened.

#### Arguments

|  |
| --- | ---
| `t_id` | File attribute id.  This string must be one of the types in the Allegro PCB Editor system file`fileops.txt`. Examples are `ALLEGRO_LAYOUT_DB` for Allegro PCB Editor layouts with extension `brd`, `ALLEGRO_REPORT` for Allegro PCB Editor report files with extension `rpt`.
|
| `t_name` | String giving name of the file to open.
| `t_mode` | Open mode. One of the following:  `r`: read-only  `w`: write  `wf`: write line-buffered
|
|
|
| `t_prop` | Property string.
#### Value Returned

|  |
| --- | ---
| `t_name` | Name of the file. In the case of`t_mode` = "`r"`, the file must exist for successful completion.
| `nil` | File not found. Displays a confirmer giving the name of the file it could not find.
#### See Also

[axlDMOpenFile](#38826 "22")

#### Example

> ```
> myfile = axlDMGetFile( "ALLEGRO_TEXT" "clip" "r")    ⇒ "/usr/home/fred/myproj/clip.txt"
> ```

Finds the file`clip.txt`, available for reading.

### axlDMOpenFile

`axlDMOpenFile(t_idt_namet_mode)⇒ p_port/nil`

#### Description

Opens a file in conventional Allegro manner; adds an extension and optionally looks it up in an Allegro search path. Must have an entry in`fileops.txt` file.

Allegro currently does not support directory or file names containing spaces.

Use this in place of Skill's infile/outfile. The Skill interfaces resolve the file location using SKILLPATH which may mean that files may not open in the local directory if the SKILLPATH does not have "." as its first component.`axlDMOpenFile` uses the Allegro convention to open file.

**Note:** If you use`axlDMOpenFile` to open a file, use `axlDMClose` to close it. All other Skill file APIs work on the port returned by this interface.

If you want to use Allegro's standard file extension support (the extension is appended if not present), then see`<cdsroot>/share/pcb/text/fileops.txt`for a list of `t_ids`. Otherwise, if you always provide an extension, use the `TEMP` id.

* Use`get_filename(p_port)` to obtain the name of the file.

#### Arguments

|  |
| --- | ---
| `t_id` | File attribute id. This string must be one of the types in the Allegro PCB Editor system file`fileops.txt`. Examples are `ALLEGRO_LAYOUT_DB` for Allegro PCB Editor layouts with extension `brd`, `ALLEGRO_REPORT` for Allegro PCB Editor report files with extension `rpt`.
| `t_name` | String giving the name of the file to open.
| `t_mode` | Open mode. One of the following:  `r`: read-only  `w`: write, create if doesn't exist, truncate to zero length if exists  `a`: open for writing, create if doesn't exist, go to end of file for appending if exists
|
|
|
In addition, the following modifiers are supported

|
| ---
| `f:`Flush file after each write. This can be slow on Windows if writing across the network. This is typically used if a process will take a long time and you would like to look at the file to see the progress. Example `"wf".`
| `b:`Open in binary mode. This only has effect on Windows. If file is ASCII, this has the effect for reading of not eliminating the carriage-returns (\r) that are in DOS ASCII files. For writing, it does not add the carriage-returns when it sees a linefeed (writes it like a UNIX ASCII file). Example `"rb".`
| `s:`Allow spaces in the file or directory name. Currently, Allegro does not support this behavior. Setting this option is unsupported. Example `"rbs".`
#### Value Returned

|  |
| --- | ---
| `p_port` | Port of the opened file. In the case of`t_mode` `="``r"`, the file must exist for successful completion.
| `nil` | File not found. Displays a confirmer giving the name of the file it could not find.
#### See Also

[axlDMFileError](#652319 "22"), [axlDMFindFile](#652311 "22"), [axlDMGetFile](#40703 "22"), [axlDMOpenLog](#652179 "22"), [axlDMClose](#652248 "22"), [axlDMFileParts](#655376 "22")

#### Example

Opens a file`clip.txt` for writing.

`aPort = axlDMOpenFile("ALLEGRO_TEXT" "clip" "w")`

Opens a file`b.bar`.

`aPort = axlDMOpenFile("TEMP" "foo.bar" "r")`

### axlDMOpenLog

`axlDMOpenLog(t_program)⇒ p_port/nil`

#### Description

Opens a file for writing log messages. Uses the name of your program or application without an extension. Opens a file with that name and the extension`.log`. Returns the port of the file if it succeeds.

#### Arguments

|  |
| --- | ---
| `t_program` | Your program name - no extension.
#### Value Returned

|  |
| --- | ---
| `p_port` | Port of the opened file. In the case of`t_mode``= "r"`, the file must exist for successful completion.
| `nil` | File not found. Displays a confirmer giving the name of the file it could not find.
#### See Also

[axlDMOpenFile](#38826 "22")

#### Example

> `logport = axlDMOpenLog("clipboard"))`

Opens the file`clipboard.log` for writing.

### axlDMClose

`axlDMClose(p_port`

`)`

`⇒ t/nil`

#### Description

Closes a file currently open in Allegro PCB Editor. Instead of using Skill's infile/outfile commands, this command must be used to close the files opened using`axlDMOpenFile` or `axlDMOpenLog` commands.

* While the core SKILL function,`close` can be used to close a file, it is recommended that any file opened using an `axlDM` function, must be closed using this function. Programs that adhere to this standard, will be compatible with future Allegro Data Management enhancements.

#### Arguments

|  |
| --- | ---
| `p_port` | Id of the open port to be closed.
#### Value Returned

|  |
| --- | ---
| `t` | Closed the file.
| `nil` | File not found.
#### Example

> `mylog = axlDMOpenLog("myapplic")    ⇒ port: "/usr/home/fred/myproj/myapplic.log"`

> `axlDMClose(mylog)    ⇒ t`

Opens and closes the file`myapplic.log`.

### axlDMBrowsePath

`axlDMBrowsePath(t_adsFileType[t_title][t_helpTag])⇒ t_fileName/nil`

#### Description

Invokes a standard Allegro PCB Editor file browser supporting paths, for example,`SCRIPTPATH`. To use, pass one of the file types supported by `fileops.txt`. Browses file types that include the fileops `PATH` attribute. `axlDMFileBrowse` should be used to browse other file types. This works on non-PATH file types since this browses in the current working directory. The user is not able to change the directory with this browser.

#### Arguments

|  |
| --- | ---
| `t_adsFileType` | First entry in`fileops.txt`.
| `t_title` | Title for the dialog
| `t_helpTag` | Tag for the help file (used only by Cadence)
#### Value Returned

|  |
| --- | ---
| `t_filename` | Full path to the filename*.*
| `nil` | Error due to incorrect arguments.
#### Example

`ret = axlDMBrowsePath("ALLEGRO_SCRIPT")`

`ret = axlDMBrowsePath("ALLEGRO_CLIPBOARD" "Select Clipboard")`

### axlDMDirectoryBrowse

```
axlDMDirectoryBrowse(t_startingDirectoryg_writeFlag[?helpTag t_helpTag][?title t_title])⇒ t_dirName/nil
```

#### Description

Opens a directory browser. Unlike file browsers, this only allows a user to select a directory. This function call blocks until the user selects or cancels.

#### Arguments

|  |
| --- | ---
| `t_startingDirectory` | Name of the starting directory.
| `g_writeFlag` | A boolean - if the file is to be opened for write (`t)`, or for read (`nil`).
| `t_helpTag` | Defines the help message to display if the*Help* button is selected in the browser. Default help is provided if this option is not set.
| `g_title` | Override default title bar of the browser. Normally, this is the name of the command that invoked the browser.
#### Value Returned

|  |
| --- | ---
| `t_dirName` | Name of directory selected.
| `nil` | No directory selected.
#### Example

`axlDMDirectoryBrowse("." t ?title "Pick a directory")`

Browses the current directory.

### axlDMFileBrowse

```
axlDMFileBrowse(t_fileTypeg_writeFlag[?defaultName t_defaultName][?helpTag t_helpTag][?directorySet g_directorySet][?noDirectoryButton g_noDirectoryButton][?mainFile g_mainFile][?noSticky g_noSticky][?title t_title][?optFilters t_filters])⇒ t_fileName/nil
```

#### Description

Opens a standard file browser. Unlike the other`axlDM` functions, this always presents the user with a file browser. This function call blocks until the user selects a file or cancels.

**Note:** The name of the file is selected and returned to the caller. Does not open the selected file.

The final filter is`'All files` (`*.*`)'.

#### Arguments

|  |
| --- | ---
| `t_id` | Id describing the file attributes from`fileops.txt`, or list of ids for different types, or `nil` if you use `optFilters` to describe files.
| `g_writeFlag` | If the file is to be opened for write (`t`), for read (`nil`).
| `t_defaultName` | Name of file to select by default.
| `t_helpTag` | Tag that defines the help message to display if the Help button is selected in the browser. Default help provided if option not set.
| `g_directorySet` | Sets the directory change button which, by default, is not set.
| `g_noDirectoryButton` | Hiding of the directory change button in the browser. By default, the button is present.
| `g_noSticky` | File browser normally remembers the directory from the previous invocation. This helps the user who browses in the same location that is different from the current working directory. If`t`, then it starts the browser in the current working directory. Normally, you should set this option if `g_directorySet` is `t`.
| `g_mainFile` | Matches options Allegro PCB Editor uses to open files from the File menu. This is`g_noSticky`=`t` & `g_directorySet`=`t`. For non-main files, use no options.
| `g_title` | Overrides default title bar of the browser. Normally this is the name of the command that invoked the browser.
| `g_filters` | Filters added to default`t_id` filter. The format is:  <`msg`>|<`filter`>|<`msg`>|<`filter`>...
#### Value Returned

|  |
| --- | ---
| `t_fileName` | Name of the file selected.
| `nil` | No file selected.
#### Examples

* Browses Allegro PCB Editor text files.

> `axlDMFileBrowse("ALLEGRO_TEXT" nil)`

* Browses Allegro PCB Editor text files and allows secondary filter of`*.log`.

> `axlDMFileBrowse("ALLEGRO_TEXT" nil ?optFilters "All log files|*.log|")`

* Browse Skill files (both il and ils extensions).

> ```
> axlDMFileBrowse(nil nil ?optFilters "Skill files(*.il)|*.il|Skill Oops(*.ils)|*.ils|")
> ```

### axlDMFileParts

`axlDMFileParts(t_filespec)⇒ (directory file fileWext ext)`

#### Description

Breaks a filename into it's component parts.

#### Arguments

|  |
| --- | ---
| `t_filespec` | Filename or full path spec.
#### Value Returned

|  |
| --- | ---
| `list` | `(``directory``file``fileWext``ext``)`
#### See Also

[axlDMOpenFile](#38826 "22")

#### Example

`fileparts = axlDMFileParts("/usr1/xxx/stuff.txt"))`

`--> ("/usr1/xxx/" "stuff" "stuff.txt" "txt")`

`fileparts = axlDMFileParts("stuff.txt"))`

`--> ("/usr1/xxx/" "stuff" "stuff.txt" "txt")`

\*\*where /usr1/xxx is the cwd

### axlOSFileCopy

`axlOSFileCopy(t_srct_destg_append)⇒ t/nil`

#### Description

Copies a given source file to a given destination with optional append.

#### Arguments

|  |
| --- | ---
| `t_src` | Full path of the source file.
| `t_dest` | Full path of the destination file.
| `g_append` | Flag for the append function (`t`/`nil`)
#### Value Returned

|  |
| --- | ---
| `t` | Copied file.
| `nil` | Failed to copy file due to incorrect arguments.
#### Example

```
unless(axlOSFileCopy("~/myfile" "~/newfile" nil)    axlUIConfirm("file copy FAILED") )
```

### axlOSFileMove

`axlOSFileMove(t_srct__dest)⇒ t/nil`

#### Description

Moves the given source file to the given destination.

#### Arguments

|  |
| --- | ---
| `t_src` | Full path of the source file.
| `t_dest` | Full path of the destination file.
#### Value Returned

|  |
| --- | ---
| `t` | Moved file.
| `nil` | Failed to move file.
#### Example

```
unless (axlOSFileMove("/mydir/myfile" "/newdir/newfile")    axlUIConfirm("file move FAILED") )
```

### axlOSSlash

`axlOSSlash(t_directory)⇒ t_directory/nil`

#### Description

Changes DOS style backslashes to UNIX style slashes which are more amenable to SKILL. On UNIX, returns the incoming string.

#### Arguments

|  |
| --- | ---
| `t_directory` | Given directory path.
#### Value Returned

|  |
| --- | ---
| `t_directory` | Directory path using UNIX style slashes (/).
| `nil` | Failed due to incorrect argument.
#### See Also

[axlOSBackSlash](23utils.html#929945 "24")

#### Example

`p = axlOSSlash("\tmp\mydir")    -> "/tmp/mydir"`

### axlRecursiveDelete

`axlRecursiveDelete(t_directory)⇒ t/nil`

#### Description

Recursively removes directories and subdirectories in the argument list. Directory is emptied of files and removed. If the removal of a non-empty, write-protected directory is attempted, the utility fails. If it encounters protected files or sub-directories, it does not remove them or the parent directories, but removes all other objects.

* ***This can be dangerous since it can severely damage your system or data if not used with care. For example, axlRecursiveDelete("/") could delete your OS and all of your data.***

#### Arguments

|  |
| --- | ---
| `t_directory` | The given directory or filename.
#### Value Returned

|  |
| --- | ---
| `t` | Directory is successfully removed.
| `nil` | Failed for one of the following reasons:  - doesn't exist  - read protected  - sub-file or directory does not allow remove (*partial success*)  - sub-file or directory is in use (NT only) (partial success)  A partial success means that some of the files and directories were deleted.
|
|
|
|
|
#### Example

> `parent = "./tmp"`

> `child = (strcat parent "/child")`

> `(createDir parent)`

> `(createDir child)`

> `(axlOSFileCopy"~/.cshrc" (strcat parent"/csh") nil)`

> `(axlOSFileCopy"~/.cshrc" (strcat child"/csh") nil)`

> `(axlRecursiveDelete parent)`

### axlTempDirectory

`axlTempDirectory()⇒ t_directoryName/nil`

#### Description

Returns the temporary directory for the current platform.

#### Arguments

`none`

#### Value Returned

|  |
| --- | ---
| `t_directory` | Temporary directory for the current platform.
| `nil` | Failed to identify temporary directory for the current platform.
### axlTempFile

`axlTempFile([g_local])⇒ t_tempFileName/nil`

#### Description

Returns a unique temp file name. The temp file should be removed, even if not used, by`axlTempFileRemove`.

By default, the files are written to`/tmp`, but you can modify this with the environment variable `TEMPDIR`.

#### Arguments

|  |
| --- | ---
| `g_local` | Flag, which if`t`, creates a temp file in the current directory. Most applications should use the default `/tmp` directory. The local directory should only be used if the file will be more than 2 megabytes.
#### Value Returned

|  |
| --- | ---
| `t_tempFileName` | Name of the unique temp file.
| `nil` | Failed to create temp file.
### axlTempFileRemove

`axlTempFileRemove(t_filename)⇒ t`

#### Description

Deletes the temporary file and removes the temporary name from the pool. It is important to call this function once you are finished with a temporary filename.

This can also be used to delete files whose names are not obtained from`axlTempFile`.

#### Arguments

|  |
| --- | ---
| `t_filename` | Name of the file to delete.
#### Value Returned

|  |
| --- | ---
| `t` | Deleted temporary file specified.
| `nil` | Failed to delete temporary file specified due to incorrect argument.
For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
