### axlCheckString

`axlCheckString( t_type t_string ) => t_modString/nil`

or

`axlCheckString( nil nil ) => lt_types`

or

`axlCheckString( 'error nil ) => t_errorMsg/nil`

#### Description

Checks the provided string for legal characters and length. You must also provide the data type. Give this API two nils if you want to see the list of supported data types.

It performs the following checks for the data type provided:

- length check

- legal characters

For all data types except PROPVALUE, it may also modify the provided string and return the updated string to meet Allegro database rules.

- stripping leading and trailing white space

- upper case

Unique considerations by data type:

- PROPVALUE checks for common property value restrictions. Typically, a property may have more severe restrictions.

- GROUP checks for common group naming restrictions. A particular group may enforce additional restrictions.

You should use the return string since it may have been modified.

Errors messages may evolve over time. Last error is only maintained until next call to axlCheckString.

#### Arguments

| Name | Description |
|---|---|
| `t_type` | data type (nil to return all supported data types) |
| `t_string` | input string |
| `'error` | fetch last error message |

#### Value Returns

| Name | Description |
|---|---|
| `t_modString` | Modified output string if check is successful |
| `lt_types` | List of data types supported |
| `nil` | Failed check |

#### Examples

- return all supported types

`axlCheckString(nil nil)`

- typical check

`axlCheckString("REFDES" "u1") -> "U1"`

- error

`axlCheckString("NET" "!GND") -> nil`

`axlCheckString('error nil)``-> "ERROR(SPMHUT-1): Illegal character(s) present in the name or value."`

#### See Also

axlDBControl - max name length

### axlCmdList

`axlCmdList( ) => ll_strings/nil`

#### Description

Lists commands registered by `axlCmdRegister`. The list consists of paired strings.

( (<`allegro command`> <`skill function`>)...)

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `ll_strings` | List of registered Allegro PCB Editor commands paired with the related SKILL functions. |
| `nil` | No commands registered. |

#### Examples

`axlCmdRegister("interboxcmd" 'axlEnterBox)`

`axlCmdList()`

`will return the following:`

`(`

`("interboxcmd" "axlEnterBox")`

`)`

### axlDebug

`axlDebug( t/nil ) => t/nil`

#### Description

This enables/disables AXL debug mode. See `axlIsDebug` for description of what this entails.

Enable debug also enables error messages for invalid attributes of Allegro `dbids`. This enables detecting typos when fetching data from `dbids`. This entails a slight performance hit. For example, if you have a pin `dbid`and you do a `pin->bbox` (instead of `pin->bBox`), then an error will be issued.

#### Arguments

`t` To enable AXL Skill debug mode.

`nil` To disable.

#### See Also

axlIsDebug

### axlDetailLoad

`axlDetailLoad( t_filename point f_scale x_rotation g_mirror) => t/nil`

#### Description

This loads a the designated `ipf` file `(t_filename`) into the current design at location (point), with scaling (`f_scale`), rotation (`f_rotation`) and mirror (`g_mirror`). Items are clipped to rectangle provided a save file time. It will load the detail to the active layer.

Note: scale values much less then 1.0 may have unpredictable results.

#### Arguments

| Name | Description |
|---|---|
| `t_filename` | the name of the plot file which contains the detail. |
| `point` | the location to place the detail. |
| `f_scale` | the scaling factor of the details as a floating point number (1.0 is no scaling). Most be greater then 0.1 |
| `x_rotation` | the rotating angle in degrees. Rotation is restricted to integers. |
| `g_mirror` | whether the detail should be mirrored (t/nil. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | was able to load |
| `nil` | otherwise |

#### Examples

Select a group of objects and load at 0,0 with double scaling.

- use `ashSelect` function in Skill examples area

`file = "myplt.plt"`

`objs = ashSelect(nil)`

`lyr = "MANUFACTURING/DETAIL"`

`win = axlDBGetDesign()->bBox`

`when(objs`

`axlDetailSave(file win objs)`

`axlLayerCreateNonConductor(layer)`

`axlVisibleLayer(layer t)`

`axlSetActiveLayer(layer)`

`axlDetailLoad(file 0:0 2.0 0 nil)`

`)`

#### See Also

axlDetailSave, axlSetActiveLayer

### axlDetailSave

`axlDetailSave( t_filename l_bBox o_dbid/lo_dbid [g_filledPads] ) => t/nil`

#### Description

This saves a clipping box (l_bBox) and the passed set of geometries (lo_dbid) to a Allegro ipf file (t_filename).

Notes:

- Any attached text to the dbids is saved.

- Ignores logical dbids such as nets, components, etc.

#### Arguments

| Name | Description |
|---|---|
| `t_filename` | the name of the file into which the detail is saved |
| `l_bBox` | list of two xy coordinates defining selection box |
| `lo_dbid` | list of AXL DBID's or single DBID |
| `g_filledPads` | output filled pads as filled (t) or unfilled (nil). Default is filled. Certain other filled figures may be effected by this option |

#### Value Returns

| Name | Description |
|---|---|
| `t` | was able to save into the file |
| `nil` | otherwise |

#### See Also

axlDetailLoad

### axlEmail

`axlEmail( t_to t_cc/nil t_subject t_body ) => t/nil`

#### Description

Sends an e-mail. If multiple To or Cc addresses are required; separate their names with a semicolon (;). On Windows, a warning confirmer may generate. To disable the warning, add the following to the registry:

`HKEY_CURRENT_USER/Identities/[ident code]/Software/`

`Microsoft/Outlook Express/5.0/Mail/Warn on Mapi Send`

Set the data value to `0`.

- On UNIX, it is not possible for the interface to return an e-mail delivery failure.

#### Arguments

| Name | Description |
|---|---|
| `t_to` | E-mail address. |
| `t_cc` | Any carbon copy persons to send; `nil` if none. |
| `t_subject` | What to put on the subject line. |
| `t_body` | Body of message. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | If successful. |
| `nil` | Failure. |

#### Examples

`axlEmail("aperson" nil "A test message" "anybody home?")`

### axlHistory

`axlHistory( [x_num] [s_operation t_filename] ) => t/nil`

#### Description

`axlHistory(``[x_num]``) -> t`

- Read or write history to a file

`axlHistory(``s_operation``t_filename``) -> t/nil`

- This is a developers aid only. Do NOT use it in a Skill program.

Provides command recall capability to the Skill development window.

Functionality also applies to the Allegro PCB Editor command line except the command is: `"history <n>"` where n is the print the last N commands.

The command line has no ability to read or write history files. They are automatically read on program startup and saved on exit.

History environment variables:

- `allegro_history = <n>` (default is 200 commands)

Command recall buffer length.

- `allegro_savehist = <n>` (efault off)

Save history file to be saved on program exit. Will be read next time on startup. File is saved at `<HOME>``/pcbenv/history_``<name>``.txt`

where `<name>`

- is skill for the skill command area

- program name for Allegro command area

History support:

- `!!` - last command (same as `!-1`)

- `!<num>` - redo command number (ex `!5`)

- `!-<num>` - redo relative to last cmd (ex `!-2`)

- `!<str>` - redo cmd starting with string last to first search (ex `!echo`)

- `!?<str>` - redo cmd matching with string last to first search. For example, `!?unnamed`

#### Arguments

| Name | Description |
|---|---|
| `x_num` | print last `<num>`commands, `0` or no argument prints entire recall buffer |
| `s_operation` | `'read` - read history buffer from provided file and append to history `'write` - write history buffer to provided file |
| `t_filename` | A history file (default extension is `.txt`) |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Operation succeeded |
| `nil` | Failed |

Also prints history buffer if running with option 1.

#### Examples

- Report history buffer

`a = 1`

`b = 2`

`axlHistory()`

- Save history

`axlHistory('write "skillhist")`

- Read history

`axlHistory()`

`axlHistory('read "skillhist")`

`axlHistory()`

### axlHttp

`axlHttp( t_url ) => t`

#### Description

Displays a URL from Allegro PCB Editor in an external web browser. First attempts to use the last active window of a running web browser, raising the browser window to the top if required. If no browser is running, tries to start one.

On UNIX, supports only the browser, Netscape. If Netscape is not running, tries to start it. May not detect failure if the web page fails to load.

Note: Netscape must be in your search path.

You can override the program name using the environment variable:

`set http_netscape = <``program name``>`

For example:

`set http_netscape = netscape405`

Note: On UNIX, this function has been tested with Netscape only and may not function properly with another web browser.

On Windows, this function uses the default web browser listed in the Windows registry. If no browser is registered, this function fails. Both Netscape and Windows Explorer work with this function. You can open any file type with a Windows registry entry.

#### Arguments

| Name | Description |
|---|---|
| `t_url` | URL to display. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | URL displayed in web browser. |
| `nil` | Failure due to web browser not being found (on UNIX), not being registered (on Windows), or being unable to load the URL. |

Note: The function may not detect when a URL has not loaded on UNIX.

#### Examples

`axlHttp("http://www.cadence.com")`

### axlIsDebug

`axlIsDebug( ) => t/nil`

#### Description

This checks if AXL debug mode is enabled. This is associated with the `axldebug` Allegro environment variable.

When this mode is set, AXL may print additional AXL API argument warnings when arguments to AXL functions are incorrect. Many warnings do not obey this variable because they are considered serious or edge conditions. Warnings supported are less serious and are known from user feedback to be troublesome to program around.

Typically, when an AXL API function encounters an argument error, it will print a warning and return `nil`.

When unset, the code runs in development mode and eliminates many of these warnings. You should have this mode enabled when developing Skill code.

This functionality was introduced in 15.2. Currently, few AXL functions take advantage of this option.

#### Arguments

None

#### Value Returns

`t` if mode is enabled, `nil` otherwise.

#### See Also

axlDebug

### axlIsProductLineActive

`axlIsProductLineActive(t_productLine) => t/nil`

#### Description

`when( axlIsDebug() printf("Error\n"))` This routine determines if a product in a given product line has been started.

#### Arguments

| Name | Description |
|---|---|
| `productLine` | The product line that you want to check.<br><br>The legal values are:<br><br>SI
 
 
 PCB
 
 
 CONCEPT
 
 
 ORCAD
 
 
 APD
 
 
 SIP
 
 
 PACKAGING
 
 Note: PACKAGING" is equivalent to "APD" + "SIP" |

#### Value Returns

- `t`: There is a license checked out for the given product line.

- `nil`: There is no license checked out for the given product line.

### axlISProductStarted

`axlISProductStarted( t_productName ) => t/nil`

#### Description

- This should not be used, use axlLicIsProductEnabled.

### axlLicDefaultVersion

`axlLicDefaultVersion( ) => f_version`

#### Description

This returns the default version number used in licensing. Most applications in a release will use this version number when checking out licenses.

#### Arguments

None

#### Value Returns

`f_version` - floating point number (e.g. 16.6)

### axlLicFeatureExists

`axlLicFeatureExists( t_license [f_version] ) => t/nil`

#### Description

Checks if license feature exists. Does not verify that the license is available. If no version is provided, the tool default version (see axlLicDefaultVersion) is used.

#### Arguments

| Name | Description |
|---|---|
| `t_license` | license name |
| `f_version` | floating point number (e.g. 16.3) |

#### Value Returns

`t` if checkout, `nil` in case of failure

#### See Also

axlLicIsProductEnabled

### axlLicIsProductEnabled

`axlLicIsProductEnabled( t_license ) => t/nil`

or

`axlLicIsProductEnabled( all ) => lt_licenses`

#### Description

Checks if license is checked-out by tool.

In first form, if given a license string returns `t` when license is checked-out and `nil` if it isn't. The test is based on the result obtained by running tool. There is no Skill method to determine licenses.

In the second form, if called with the symbol `all` returns a list of licenses currently checked out by the tool.

#### Arguments

| Name | Description |
|---|---|
| `t_license` | Name of license (case sensitive) |
| `'all` | Get all licenses currently checked-out by the program. |

#### Value Returns

- `t` - license checked out

- `nil` - license not checked out

- `lt_licenses` - list of licenses checked-out by program (all mode)

#### Examples

See if skill developer license (product 900) is checked out:

`axlLicIsProductEnabled("skillDev")`

#### See Also

axlLicFeatureExists, axlLicDefaultVersion

### axlLogHeader

`axlLogHeader( p_port t_titleString [t_prefix] ) => t/nil`

#### Description

Writes the standard Allegro PCB Editor log file header to the passed open file. The header record includes:

- Title String

- Drawing Name

- Software Release

- Date and Time

#### Arguments

| Name | Description |
|---|---|
| `p_port` | SKILL port for the open file. |
| `t_titleString` | Title string in the log file header. |
| `t_prefix` | Optional prefix string to header for easier parsing (recommend "#") |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Wrote log file header to open file. |
| `nil` | Failed to write log file header to open file due to incorrect arguments. |

### axlMKS2UU

`axlMKS2UU( t_mksString ) => f_value/nil`

#### Description

Converts between an MKS string to the current database user units. String can be any length name plus many common abbreviations (see `units.dat` file in the Allegro PCB Editor share/text hierarchy for supported names.)

Conversion can fail for the following reasons:

- Input string not a legal MKS format.

- Conversion will overflow the maximum allowed database size.

Notes:

- Conversion between metric and english units may result in rounding.

- Return number is rounded to the database precision.

#### Arguments

| Name | Description |
|---|---|
| `t_mksString` | Input unit's string with MKS units. |

#### Value Returns

| Name | Description |
|---|---|
| `f_value` | Floating point number. |
| `nil` | Conversion failed. See previous description for possible reasons. |

### axlMKSAlias

`axlMKSalias( t_MKSAlias ) => t_alias/nil`

#### Description

Searches the MKS unit database for the current definition associated with `unitName`. Unlike `axlMKSConvert`, this function does not convert.

You load the MKS database from the following file:

`<``cds_root``>/share/pcb/text/units.dat`

#### Arguments

| Name | Description |
|---|---|
| `t_mksAlias` | Name of the alias string. |

#### Value Returns

| Name | Description |
|---|---|
| `t_def` | Definition name as a string. |
| `nil` | Definition name could not be found. |

#### Examples

`axlMKSAlias("VOLTAGE") -> "V" (Intended usage)`

`axlMKSAliaas("M") -> "METER"`

`axlMKSAlias("KG") -> NIL (The function supports only the use of basic units.)`

### axlMKSConvert

#### Description

Operates in several ways, depending on the arguments passed.

| Name | Description |
|---|---|
| 1. | To convert a number from an input units type to an output unit type, general case: |

`axlMKSConvert (``n_input``t_inUnits``[t_outUnits]``)``=> f_output/nil`

| Name | Description |
|---|---|
| 2. | To convert a number from an input units type to MKS units: |

`axlMKSConvert (``n_input``t_inUnits``nil``)``=> f_output/nil`

| Name | Description |
|---|---|
| 3. | To convert a number from MKS units to an output unit type: |

`axlMKSConvert (``n_input``nil``t_outUnits``)``=> f_output/nil`

| Name | Description |
|---|---|
| 4. | To convert an MKS string to an output units, i.e. ".5 MILS" to "INCHES": |

`axlMKSConvert (``t_input``[t_outUnits]``)``=> f_output/nil`

| Name | Description |
|---|---|
| 5. | To pre-register an input units, so that subsequent calls need not specify units: |

`axlMKSConvert (``nil``t_inUnits``)``=> t/nil`

| Name | Description |
|---|---|
| 6. | To convert a unit from a pre-registered input units: |

`axlMKSConvert (``n_input``)``=> f_output/nil`

Converts any allowable unit to any other allowable unit. It operates in several ways, depending on the arguments.

In all instances with `t_outUnits` as an argument, if that argument is omitted, the function converts to active design units.

| Name | Description |
|---|---|
| 1. | If the first argument is a number and the second argument is evaluated as the units of that number, the number is converted to the units specified by the third argument. |

A special case is if first argument is a number, the second is "design" and the third is a length unit then the input number is converted from current design units to specified length units.

| Name | Description |
|---|---|
| 2. | In the case where the first argument is a string, that string must be a fully instantiated units string, i.e. "15 MILS". In this case the second string is interpreted as the output units, and the value of the first string is converted to these units. |

| Name | Description |
|---|---|
| 3. | If the first argument is nil, then the input units specified by the second argument is remembered for the future calls. The output units will default to the active design, and the function will fail as above if no design is active. Note that pre-registration will not work if there is no active design. |

| Name | Description |
|---|---|
| 4. | When only a number is specified, the function will confirm that an input unit has been pre-registered, and will convert that number, in the pre- registered units, to the design units. Function will issue a warning and return nil if no pre-registered input units, or no active design |

| Name | Description |
|---|---|
| 5. | When the second and third arguments are present but one is nil, it represents MKS standard units for the input or output units, respectively. |

#### Arguments

| Name | Description |
|---|---|
| `n_input` | Number to convert |
| `t_inUnits` | String giving the units of the input number. If first argument is not specified, this string should specify the input number to convert and its units. |
| `t_outUnits` | String giving the new units for `f_output`. If `t_outUnits` is `nil`, converts the number to the current units of the layout. |

#### Value Returns

| Name | Description |
|---|---|
| `f_output` | Converted value of `n_input`. |
| `nil` | Failed to convert value due to incorrect arguments. |

#### Examples

- Typical use, convert from design units to another type (design is in mils)

`axlMKSConvert(.5 "design" "INCHES") => 0.0005`

`axlMKSConvert(".5 MILS" "INCHES") => 0.0005`

- Pre-register a unit type then use if on future conversions

`axlMKSConvert(nil "MILS") => t`

`axlMKSConvert(.5) => 0.0005`

- Go to default output conversion (METERS)

`axlMKSConvert(.5 "MILS" nil) => 2.54e-05`

- Not just length is supported (go to farads)

`axlMKSConvert(1e-09 nil "pF") => 1000.0`

### axlMKSStr2UU

`axlMKSStr2UU( t_String ) => t_mksString/nil`

#### Description

Converts an input string to a MKS string in current database units. If the input string is in MKS units, that is used as the basis for the conversion. If the string has no units, the function uses the default database units for the string.

Conversion may fail for the following reasons:

- Input string is not a legal MKS format.

- Conversion overflows the maximum database size allowed.

Notes:

- Conversion between metric and english units may result in rounding.

- Number returned is rounded to the database precision.

#### Arguments

| Name | Description |
|---|---|
| `t_String` | Input string. |

#### Value Returns

| Name | Description |
|---|---|
| `t_mksString` | MKS string in current database units. |
| `nil` | Failed to convert input string. See earlier Description for possible reasons. |

#### Examples

`axlMKSStr2UU("100.1") -> "100.0 MILS"`

Default conversion with the database in mils.

### axlMapClassName

`axlMapClassName( t_oldName/lt_oldName [g_mapToPCB] ) => t_newName/lt_newName`

#### Description

Use this function to write a SKILL program that runs in Allegro PCB Editor and APD. You can map from class names to the name appropriate to the program running your SKILL program. For example, you can write a program using Allegro PCB Editor class names and have the program run in APD.

The table shows the name mapping between Allegro PCB Editor and APD.

Table 24-1 
 Class Name Mapping

| Name | Description |
|---|---|
| Allegro PCB Editor Class Name | APD Class Name |
| BOARD GEOMETRY | SUBSTRATE GEOMETRY |
| ETCH | CONDUCTOR |
| ANTI ETCH | ANTI CONDUCTOR |
| PACKAGE GEOMETRY | COMPONENT GEOMETRY |
| PACKAGE KEEPIN | COMPONENT KEEPIN |
| PACKAGE KEEPOUT | COMPONENT KEEPOUT |
| BOARD | SUBSTRATE |

When using the list of names mode, names that are not recognized are returned "as is".

#### Arguments

| Name | Description |
|---|---|
| `t_oldName` | Allegro PCB Editor class name. |
| `lt_oldName` | List of Allegro PCB Editor class name. |
| `g_mapToPCB` | Optional. `t` maps from the APD name to the PCB names. Default is `nil` (PCB to APD conversion). |

#### Value Returns

| Name | Description |
|---|---|
| `t_newName` | Appropriate class name based on product type. |
| `lt_newName` | List of class names renamed. |

#### Examples

| Name | Description |
|---|---|
| 1. | Get APD class name when in APD. |

`axlMapClassName("ETCH") -> "CONDUCTOR"`

| Name | Description |
|---|---|
| 2. | Gets Allegro PCB Editor class name when in Allegro PCB Editor. |

`axlMapClassName("ETCH") -> "ETCH"`

| Name | Description |
|---|---|
| 3. | List in APD |

`axlMapClassName('("ETCH" "ANALYSIS")) -> ("CONDUCTOR" "ANALYSIS")`

### axlMemSize

`axlMemSize( ) => x_size`

#### Description

Returns an estimate of memory use. Returns not what the program is using, rather what it is requesting from the operating system.

#### Arguments

nothing

#### Value Returns

| Name | Description |
|---|---|
| `x_size` | Estimate of memory use in bytes. |

### axlOSBackSlash

`axlOSBackSlash( t_directory ) => t_directory/nil`

#### Description

This changes UNIX style forward slashes to DOS style backslashes. While most applications support either style, certain older Windows applications only support DOS style path.

The UNIX style is more amenable to Skill programming.

On UNIX this just returns the incoming string.

#### Arguments

| Name | Description |
|---|---|
| `t_directory` | String containing directory path with forward slashes |

#### Value Returns

`t_directory/nil`

#### See Also

axlOSSlash

### axlOSControl

`axlOSControl( s_name [g_value] ) => g_currentValue/ls_names`

#### Description

`p = axlOSBackSlash("/tmp/foo") -> "\\tmp\\foo"` Inquires and/or sets the value dealing with the graphics. If setting a value, the return is the old value of the control.

A side effect of most of these controls is if a form is active that is displaying the current setting it may not be updated. Additional side effects of individual controls, currently supported, are listed in the following table.

| Name | Description |
|---|---|
| cpu | x_number; No; Returns number of available CPUs. Included in the number are multi-cpu multi-core, and hyper threading.; none; none |
| is64exe | t/nil; No; Returns t if this executable is 64bit; none; none |
| is64os | t/nil; No; Returns t if this is a 64bit based OS.; none; none |
| isWindows | t/nil; No; Returns t if a Windows OS and nil if UNIX or Linux.; none; none |
| hostname | string; No; Returns hostname of computer this programming is running on.; none; none |
| physicalMemory | x_number; No; Returns in units of 1Mbyte the amount of physical memory. This is not to be confused with virtual memory.
 Note: 32bit OS can at most address 4GB (4000MB) of memory. 32bit Windows is restricted to 3GB. So even if you have more installed on your PC this will still report 3GB.; none; none |

#### Arguments

| Name | Description |
|---|---|
| `s_name` | Symbol name of control. If this value is `nil`, all possible names are returned. |
| `g_value` | Optional symbol value to set. Usually a `t` or a `nil`. |

#### Value Returns

See above

| Name | Description |
|---|---|
| `ls_names` | If name is `nil` then returns a list of all controls. |

#### Examples

| Name | Description |
|---|---|
| 1. | Get CPUs |

`size = axlOSControl('cpu)``-> 2`

| Name | Description |
|---|---|
| 2. | Get if 64bit program |

`axlOSControl('is64exe)`

`-> nil`

#### See Also

axlUIControl, axlMemSize

### axlOSNtp

`axlOSNtp( s_mode t_serverName/nil ) => x_nwtime/t_nwtime/t_server/nil`

#### Description

Reports time from a NTP server.

If the value of `s_mode` is set to `'name`, then Allegro PCB Editor reports the default NTP server, obtained using the environment variable NTPSERVER. Default is `0.pool.ntp.org`.

Currently, the `axlOSNtp` command uses a timeout of 50 milliseconds.

On Linux, you can query NTP time using the following command.

`/usr/sbin/ntpdate -q``<hostname>`

Note: IPv6 networks not supported.

- Must be connected to Internet and, if a firewall is enable, it must be configured to allow port 123.

#### Arguments

| Name | Description |
|---|---|
| `s_mode` | The possible values are: ``name`: Returns default NTP server name for Allegro PCB Editor. `t`: Returns network time and date as string (current time zone) `nil`: Returns time ID (seconds since 00:00:00 UTC, January 1, 1970) |
| `t_serverName` | Use NTP server or if the value specified in `nil`, default Allegro NTP server is used. |

#### Value Returns

- `x_nwtime`: A time ID. This value is returned when the value of `s_mode` is set to `nil`.

- `t_nwtime`: Time and date in ASCII using current time zone. This value is returned when the value of `s_mode` is set to `t`.

- `t_server`: Name of the default time server. Returned when the value of `s_mode` is set to ``name`.

- `nil`: Returned in case of an error.

### axlPPrint

`axlPPrint( t_name ) => t_pname`

#### Description

`time = axlOSNtp(t nil)` Converts a string with Allegro PCB Editor's pretty print text function as follows:

- Ensures that the first character after a white space, _ (underscore) or / (forward slash) is capitalized.

- Ensures the rest of the text in the given string is lower case.

#### Arguments

| Name | Description |
|---|---|
| `t_name` | A string. |

#### Value Returns

| Name | Description |
|---|---|
| `t_pname` | The converted string. |

#### Examples

`axlPPrint("ETCH/TOP") -> "Etch/Top"`

### axlPdfView

`axlPdfView( t_pdfFile ) => t`

#### Description

Displays a PDF file from Allegro PCB Editor. If just the filename is given, attempts to find the PDF file using Allegro PCB Editor's `PDFPATH` variable. Displays the PDF file in an external PDF viewer.

On UNIX, the only supported PDF viewer is Acroread. The program, Acroread, must be in your `PATH`.

On Windows, uses the default PDF viewer registered with the Windows registry. If there is no registered PDF viewer, the call fails.

#### Arguments

| Name | Description |
|---|---|
| `t_pdfFile` | Name of PDF file to display. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | PDF file displayed. |
| `nil` | Failed to display PDF file due one of the following:
 - No Acroread PDF viewer found on UNIX.
 - No PDF viewer registered on Windows. |

#### Examples

`axlPdfView("allegro.pdf")`

### axlPrintDbid

`axlPrintDbid( o_dbid/lo_dbid [o_port] ) => t`

#### Description

This is a debug function to print one or a list of dbids. Output format is terse and parsable. This will not print all attribute data in a dbid but is customized to aid in understanding the dbid data.

`Format: <key> <attribute> <value>` where key can be

| Name | Description |
|---|---|
| c | common value of attribute (objType, name, xy) |
| a | other attributes |
| l | printable detail on list of dbids associated with element Not all list of dbids are reported. |
| g | what groups have the object. 
 Format: `g group <type> name= <name>` |

Output is either directed to the Skill window or if port is provided written to a file.

Note using the environment variable, `pv_showelem` you can get the same data in the show element command.

#### Arguments

| Name | Description |
|---|---|
| `o_dbid/lo_dbid` | dbid or a list of dbids |
| `o_port` | option port object (from outfile) |

#### Value Returns

`t`

#### Examples

`l = axlGetDesign()`

`axlPrintDbid(l)`

#### See Also

axlShowObject

### axlRegexpIs

`axlRegexpIs( t_exp ) => t/nil`

#### Description

Determines whether an environment variable expression contains Allegro PCB Editor compatible wildcard characters. Certain select-by-name functions support wildcard characters. You can test for the presence of wildcards before calling the select-by-name type of functions.

Regular expressions used by Allegro PCB Editor are more compatible with the character set allowed in the Allegro PCB Editor object names than SKILL regular expressions. Do not use to test patterns being sent to the SKILL `regexp` family of functions.

#### Arguments

| Name | Description |
|---|---|
| `t_exp` | SKILL symbol for the environment variable name. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Expression contains Allegro PCB Editor compatible wildcards. |
| `nil` | Expression does not contain Allegro PCB Editor compatible wildcards. |

### axlRunBatchDBProgram

`axlRunBatchDBProgram( t_prog t_cmdFmt [?logfile t_logfile] [?startMsg t_startMsg] [?reloadDB t/nil] [?noUnload t/nil] [?silent t/nil] [?noProgress t/nil] [?warnProgram t/nil] ) => t/x_error`

#### Description

Spawns batch jobs that require an open database via an abstract model. When the job completes, it prints a message and optionally reloads (`?reloadDB`) the database if successful. If the database is saved from the current active database, it uses a temporary name to avoid overwriting the database on disk.

The following options are always required (UIBatchSpawn):

| Name | Description |
|---|---|
| `t_prog` | Name of the program to run. |
| `t_cmdFmt` | Command string. |

The following options are optional.

| Name | Description |
|---|---|
| `t_logFile` | Name of log file that the program creates. Registers this with the log file viewlog facility if the program ends in an error. If no log file is required, do not set this option. If no extension is given, adds `.log` as the extension. |
| `startMsg` | Enables a start message to display when the program starts. Defaults to the program name. If you override by providing this string, the message begins with `"Starting..."` |
| `reloadDB` | If you set this to `t`, the database reloads after a successful run of the program. If the batch program does not save the database(e.g. reports) then there is no reason to reload database. dbids are refreshed. |
| `noUnload` | If you set this to `t`, you don't save the database to disk. You use this for a program that creates a new database or doesn't require an Allegro PCB Editor database. Default is `nil`. |
| `silent` | If you set this to `t`, no messages are displayed. Use when the user does not need to know that a program is spawned. Default is `nil`. |
| `noProgress` | If `t`, the progress meter does not display. Default is `nil`. |
| `noLogview` | When set, it prevents display if log file on program exit. |
| `noWarnOnExit` | When set, suppresses some exit warning messages. |
| `warnProgram` | Program supports warning status (returns 0, if success; 1, if warnings; and 2, if errors). |
| `noExitMsgs` | When set, suppresses messages about program success or failure. |

Note: For`t_cmdFmt`, the formatting should include everything except the design filename. Place a `%s` where the design should appear. To get a `%s` while doing a `sprintf`, use a "`%%s`" as shown in following examples:

`cmdFmt = "netrev -$ -q -r %s"`

`sprintf(cmdFmt, "%s -$ %s %s %%s", prog, argq argr)`

- a.; For debug, set the env variable, `wait_debug`, on the Allegro command line:

`set wait_debug`

or in Skill

`axlSetVariable("wait_debug" nil)`

This echos the spawning arguments of your program. You can also use this variable to see how Allegro spawns programs from its dialogs. The `"#T<num>.tmp"` name seen in this output is the temporary save of the current design to disk and the use of the `"%s"` argument in your `t_cmdFmt` statement.

- b.; For a list of Allegro programs and their command line arguments see the directory:

`<cdsroot>/share/pcb/batchhelp`

or run the batch program with the `"-help"` argument.

`Example: idf_in -help`

- c.; Many Allegro batch programs support `'-$'` as a standard argument. This prevents prompting for missing input arguments.

#### Arguments

| Name | Description |
|---|---|
| `t_prog` | string containing program name |
| `t_cmdFmt` | string containing starting arguments (including program) |
| `t_logfile` | optional string showing logfile |
| `t_startMsg` | optional string having start message |
| `?reloadDB` | Optional t/nil having database be reloaded after job completes |
| `?noUnload` | Optional t/nil stating database shouldn't be saved |
| `?silent` | Optional t/nil controlling info messages |
| `?noProgress` | Optional t/nil controlling progress meter |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Batch job ran. |
| `x_error` | Error number that is program dependent on failure. |

#### Examples

- Spawn genfeedformat which requires design to be saved to a temp file

Program Args:

- `-$` - silent

- `-b` - name of design (required)

- `%%s` - because we `sprintf` the format before calling batch we need to escape the `%s` by prepending an extra %

Skill:

`sprintf(format "genfeedformat -$ %s %%s", "-b")``;format= "genfeedformat -$ -b %s"``axlRunBatchDBProgram("genfeedformat" format``?logfile "genfeed")`

Without `sprintf`

`axlRunBatchDBProgram("genfeedformat" "genfeedformat -$ -b %s" ?logfile "genfeed")`

- Spawn 3rd party program, notepad, on an existing file `"allegro.jrl".`In this case we do not want to save design (`?noUnload t`) and no progress meter is required (`?noProgress t`)

`axlRunBatchDBProgram("notepad" "notepad allegro.jrl"``?noUnload t ?noProgress t)`

- Spawn 3rd party import login, a program that requires read/write database wrapping. Read existing 3rd party netlist file called "netlist.txt". Since design needs to be reloaded if import is successful use the "?reloadDB t" option.

Program Args:

- `-$` - silent

- `-g` - run gate assign

- `-y 1` - Always Place changed component

- `netlist` - name of netlist file (e.g. netlist.txt)

- `%s` - use current design

Skill:

- Export IDF

`axlRunBatchDBProgram("netin" "netin -$ -g -y 1 netlist %s" ?startMsg "Logic Import" ?logfile "netin" ?reloadDB t)` Program Args:

- -d IDF - File name type

- -V 3.0 - IDF version

- -h 2000 - default package height

- -s ... - Source id (note \"...\" allows spaces in name)

- -o myidf - output idf files (with bdf and ldf extensions)

- %s - axl will enter name of temp database saved to disk

Skill:

- Import IDF, assumes an existing bdf file, unnamed.bdf. If successful load updated design back into memory via the reload option (`?reloadDB t`).

`axlRunBatchDBProgram("idf_out" "idf_out %s -d IDF -o myidf -s \"allegro_16.3\" -b 1 -h 2000 -V 3.0")` Program Args:

- -o %s - name of current design (%s - substitute in current design)

- unnamed - name of bdf file on disk

Skill:

`axlRunBatchDBProgram("idf_in" "idf_in -o %s unnamed" ?reloadDB t)`

### axlShowObject

`axlShowObject( lud_dbid ) => t/nil`

#### Description

Displays the object data for each `dbid` in `lud_dbid` in a Show Element window. Does the same function as the interactive command `list element.``lud_dbid` can be either a single `dbid` or a list of `dbids`.

#### Arguments

| Name | Description |
|---|---|
| `lud_dbid` | `dbid`, or list of `dbids`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Displayed the Show Element window for any objects. |
| `nil` | Failed to display the Show Element window for any objects. |

#### Examples

`axlDBCreatePropDictEntry(``"myprop", "real", list( "pins" "nets" "symbols"),``list( -50. 100), "level")``axlClearSelSet()``axlSetFindFilter(``?enabled '("NOALL" "ALLTYPES" "NAMEFORM")``?onButtons "ALLTYPES")``axlSingleSelectName( "NET" "ENA2")``axlDBAddProp(axlGetSelSet(), list("MYPROP" 23.5))``axlShowObject(axlGetSelSet())``⇒ t`

| Name | Description |
|---|---|
| 1. | Defines the string-valued property `MYPROP`. |

| Name | Description |
|---|---|
| 2. | Adds it to the net `ENA2`. |

| Name | Description |
|---|---|
| 3. | Displays the result to the user with `axlShowObject`. |

### axlSleep

`axlSleep( x_time ) => t/nil`

#### Description

Sleeps specified time.

This is a replacement for Skill's sleep which is actually provided by the IPC Skill package. On Windows the IPC sleep crashes if you call `axlEnterEvent`.

If you are using the IPC interfaces then you should call `axlSleep` instead of using `sleep`.

#### Arguments

`x_time` Time in seconds.

#### Value Returns

`t`All of the time.

### axlSort

`axlSort( t_infile t_outfile [t_sortfields] [t_sort_options] ) => t/nil`

#### Description

Sorts contents of a given input file and places results in the output file. No warning is given if the output file overwrites an existing file - any checking must be done by the caller of this function.

Default sort is a left to right, ASCII ascending sort of the input file, with duplicate lines left in. You can control the sort behavior using the optional parameters.

#### Arguments

| Name | Description |
|---|---|
| `t_infile` | Name of the input file to sort. |
| `t_outfile` | Name of the file containing results of the sort. |
| `t_sortfields` | String specifying which fields to use as sort keys, the sort order of those fields, and how to interpret the data type of the field for sorting. String contains a series of triplets: `field_number sortOrder fieldType` String can contain multiple triplets separated by commas. Triplets can contain valid elements as shown: |

| Name | Description |
|---|---|
| Triplet Element | Description |
| `field_number` | Number representing the position of the field on the line, from left to right. Numbering starts at 1. |
| `sortOrder` | A - Ascending sort order
 D - Descending sort order |
| `fieldType` | A - Alpha
 I - Integer
 F - Float |

An example of a `t_sortfields` triplet:

`"3 A A, 5 D I, 1 A F"`

This triplet sorts based on the following:

| Name | Description |
|---|---|
| 1. | The third field, ascending, field type ASCII. |

| Name | Description |
|---|---|
| 2. | The fifth field, descending, field type Integer. |

| Name | Description |
|---|---|
| 3. | The first field, ascending, field type Float. |

| Name | Description |
|---|---|
| `t_sort_options` | String containing directives controlling the global sort parameters. Sort options can appear in any order, and must be separated by commas. These options are available: |

| Name | Description |
|---|---|
| Option | Description |
| Field Delimiter | Supported delimiters include any character in punctuation character class except comma. |
| U | Remove duplicate lines. Default is keep duplicate lines. |
| D | Descending order. Default is ascending order. |

An example of the `t_sort_options` string:

`"!,U"`

This means to use the ``!`' character as the field delimiter and to remove any duplicate lines.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Sort successful. |
| `nil` | Sort unsuccessful due to incorrect arguments. |

#### Examples

Input file

`2!3!4!5!6`

`2!3!4!5!6`

`5!6!7!8!9`

`5!1!7!8!9`

`2!2!3!4!5`

`1!2!3!4!5`

`3!4!5!6!7`

`4!5!6!7!8`

Example 1

`(axlSort "input.txt" "output.txt" nil "!,U")`

Results 1

`1!2!3!4!5`

`2!2!3!4!5`

`2!3!4!5!6`

`3!4!5!6!7`

`4!5!6!7!8`

`5!1!7!8!9`

`5!6!7!8!9`

Example 2

`(axlSort "input.txt" "output.txt" "2 A I, 1 D I" "!")`

Results 2

`5!1!7!8!9`

`2!2!3!4!5`

`1!2!3!4!5`

`2!3!4!5!6`

`2!3!4!5!6`

`3!4!5!6!7`

`4!5!6!7!8`

`5!6!7!8!9`

### axlStrcmpAlpNum

`axlStrcmpAlpNum( t_str1 t_str2 ) => t/nil`

#### Description

Provides an alpha-numeric sort similar to `alphalessp` with one important distinction. If both strings end in the number, the number portion is separated and the two stripped strings are first compared. If they are equal, then the number sections are compared as numbers, rather than strings.

| Name | Description |
|---|---|
| `alphalessp` sort | `U1 U10 U2` |
| `axlStrcmpAlpNum` sort | `U1 U2 U10` |

#### Arguments

| Name | Description |
|---|---|
| `t_str1` | A string |
| `t_str2` | A string |

#### Value Returns

| Name | Description |
|---|---|
| `0` | The two strings are equal. |
| `+num` | If `t_str1` is greater than `t_str2` (1 goes after 2) |
| `nil` | If `t_str1` is less than `t_str2` (1 goes before 2) |

#### Examples

`l = '("U5" "U10" "U1" "U5" "U2")`

`sort(l 'axlStrcmpAlpNum)`

`===> ("U1" "U2" "U5" "U5" "U10")`

### axlStringCSVParse

`axlStringCSVParse( t_string [g_stripWhite] [t_separator] ) => lt_string/nil`

#### Description

Parses a comma delimited line (typical from Excel). This differs from the Skill prehistorian function in several areas which make it compatible with Excel csv file format:

- parseString ignores two adjacent commas.

- if a separator is contained within a cell, Excel quotes the cell. `parseString` treats this as two cells.

- Correctly processes double quotes in a cell.

#### Arguments

| Name | Description |
|---|---|
| `t_string` | A csv string |
| `g_stripWhite` | Option to strip leading and trailing white space from each output string. Default is to leave whitespace. Do not advise using this option with separator set to " ". |
| `t_separator` | Optional separator character, default is a comma (,). |

#### Value Returns

| Name | Description |
|---|---|
| `lt_string` | list of strings parsed based on comma separator. |
| `nil` | error (unlikely to happen) |

#### Examples

- white space strip example

`ret = axlStringCSVParse(" a ,b" t)`

`-> ( "a" "b")`

- properly parse a csv file

`ret = axlStringCSVParse("a,,c,\"d,e\"" )`

`-> ( "a" "" "c" "d,e")`

- properly parse a csv file

`ret = axlStringCSVParse("a||c|\"d|e\"" nil "|" )`

#### See Also

parseString in Cadence SKILL Language Reference

### axlStringRemoveSpaces

`axlStringRemoveSpaces( t_string ) => t_modString/nil`

or

`axlStringRemoveSpaces( lt_string ) => lt_modString/nil`

#### Description

This will strip leading or trailing whitespace from a string (standard C `ilspace()` macro). Has two modes:

- one string

- list of strings

In list of strings, items in list that are not a string are filtered out of the return.

#### Arguments

| Name | Description |
|---|---|
| `t_string` | A string. |
| `lt_string` | list of strings |

#### Value Returns

| Name | Description |
|---|---|
| `t_modString` | Modified string |
| `lt_modString` | Modified strings |
| `nil` | Not a string |

#### Examples

`ret = axlStringRemoveSpaces(" a ")`

`ret = axlStringRemoveSpaces( '(" a " " b "))`

#### See Also

axlCheckString

### axlVersion

`axlVersion( s_option ) => g_value/nil`

#### Description

Returns Allegro PCB Editor or OS dependent data.

#### Arguments

| Name | Description |
|---|---|
| `s_option` | SKILL symbol for the environment variable name. |

#### Value Returns

Return depends upon option given.

| Name | Description |
|---|---|
| Option | Value; Returns |
| none | `ls_values`; List of available options. |
| version | `f_value`; Allegro PCB Editor program version, for example, 15.7. |
| tVersion | `t_value`; Allegro PCB Editor program version as a string, for example, 16.3. |
| fullVersion | `t_value`; Allegro PCB Editor program version and patch as a string ( for example, 15.7 s01). |
| buildDate | `t_value`; Date program was built at Cadence (month/day/year),for example, 7/19/2006. |
| release | `t_value`; Allegro PCB Editor release value. Consists of a prefix and a number (`<p><nn>`), where prefixes are as shown:
 A - Alpha
 B - Beta
 P - Production
 S - Patch
 For example, S23 indicates the 23`rd` patch release. |
| internalVersion | `t_value`; Internal program version, for example, v15-1-25A. |
| programName | `t_value`; Executable being run, for example, `allegro`. |
| displayName | `t_value`; Short display name of program (may contain spaces.) Certain programs may change this during run-time depending on the license level. This may be the same or shorter then the formal name. It may change from release to release.
 Example: `"Allegro PCB Design XL"` |
| formalName | t_value; Long Display name of program (may contain spaces). This is the full formal name of program and may change during run-time since it depends upon the license level. The name can be the same or longer than `displayName`, and may change from release to release. |
| isWindows | `g_value`; `t` if Windows operating system. `nil` if UNIX operating system. |
| isSQ | `g_value`; `t` if Allegro PCB SI (SpecctraQuest base product), `nil` otherwise. |
| isPI | g_value; `t` if Allegro PCB PI Option XL (SpecctraQuest Power Integrity option), `nil` otherwise. |
| isPDN | g_value; `t` if PDN analysis option, `nil` otherwise |
| isAPDSi | g_value; `t` if Allegro Package Designer SI L (or 610), `nil` otherwise |
| isAPDSiL | `g_value`; `t`if Allegro Package Designer SI L, `nil` otherwise |
| isAllegroExpert | `g_value`; `t` if Allegro Export product, `nil` otherwise. |
| isAllegroDesigner | `g_value`; `t` if Allegro Designer product, `nil` otherwise. |
| isAllegroOrcad | `g_value`; `t` if Allegro OrCAD product, `nil` otherwise. |
| isAllegroPCB | `g_value`; `t` if Allegro PCB product, `nil` otherwise. |
| isAPD | `g_value`; `t` if Allegro Package Designer product, `nil` otherwise. |
| isAPDL | `g_value`; `t` if Allegro Package Designer L, `nil` otherwise |
| isAPDXL | `g_value`; `t` if Allegro Package Designer XL, `nil`otherwise |
| isAPDLegacy | `g_value`; `t` if Allegro Package Designer VT2300, `nil` otherwise |
| isChipIOPlanner | `g_value`; `t` if any Chip I/O Planner product, `nil`otherwise |
| isICP | `g_value`; `t`if any ICP based product (apd, sip), `nil`otherwise |
| isSIP | `g_value`; `t`if any SIP product, `nil`otherwise |
| isSIPDigital | `g_value`; `t` if any SIP Digital product, `nil`otherwise |
| isSIPDigArch_L | `g_value`; `t`if running the SIP Digital Architect L product, `nil` otherwise |
| isSIPDigArch_GXL | `g_value`; `t` if running the SIP Digital Architect GXL product , `nil` otherwise |
| isSIPDigSI_XL | `g_value`; `t` if running the SIP Digital SI XL product, `nil` otherwise |
| isSIPDigLay_GXL | `g_value`; `t` if running the SIP Digital Layout GXL product, `nil` otherwise |
| isSIPRF | `g_value`; `t` if running any SIP RF product, `nil` otherwise |
| isSIPRFArch_L | `g_value`; t if running the SIP RF Architect L product, `nil` otherwise |
| isSIPRFLay_GXL | `g_value`; t if running the SIP RF Layout GXL product, `nil` otherwise |
| isSigxp | `g_value`; `t` if any version of SigXP, `nil` otherwise. |
| isSxExpert | `g_value`; `t` if SigXP Expert product, `nil` otherwise. |
| isSxExplorer | `g_value`; `t` if SigXP Explorer product, `nil` otherwise. |
| isEmbedded | `g_value`; `t` if Embedded placement allowed. |
| isBackdrill | `g_value`; `t` if Backdrill functionality allowed. |
| isToolbox | `g_value`; `nil` no toolbox, `'orcad` - OrCAD toolbox active, `'allegro` - Allegro toolbox `axlIsToolbox()`: API is provided for legacy purposes and returns the same results. |
| isSymphony | `g_value`; `t` if running in Symphony (multi-user) mode. |

#### Examples

`axlVersion()`

### axlVersionIdGet

`axlVersionIdGet( ) => x_time`

#### Description

Returns an id stamp based upon computer time.

#### Arguments

none

#### Value Returns

| Name | Description |
|---|---|
| `x_time` | Returns an id stamp based on computer time. |

### axlVersionIdPrint

`axlVersionIdPrint( x_time/t_time ) => t_printTime/nil`

#### Description

Prints version_id.

VERSION_ID is stored as a property on the database root and on the symbol definitions as shown:

`axlDBGetDesign()->prop->VERSION_ID`

Use to determine if a symbol should be refreshed. VERSION_ID is updated every time the database is saved, except if done as part of an uprev.

#### Arguments

| Name | Description |
|---|---|
| `x_time`/`t_time` | VERSION_ID obtained from the database property or returned from `axlVersionIdGet()`. |

#### Value Returns

| Name | Description |
|---|---|
| `t_printTime` | Printable string in standard Allegro PCB Editor date/time format. |
| `nil` | Failed to print VERSION_ID due to incorrect argument. |

#### Examples

`axlVersionIdPrint(axlDBGetDesign()->prop->VERSION_ID``-> "Mon Dec 16 12:45:16 2004"`

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

