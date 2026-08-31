### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

8
=

Allegro PCB Editor Command Shell Functions
==========================================

This chapter describes the AXL-SKILL functions that access the Allegro PCB Editor environment and command shell.

Command Shell Functions
-----------------------

This section lists Allegro PCB Editor command shell functions.

### axlGetAlias

`axlGetAlias(t_alias/nil)⇒ t_value/lt_names/nil`

#### Description

Requests the value of the specified Allegro PCB Editor alias,`t_alias`. If given a `nil`, returns a list of aliases currently set. For compatibility purposes, `axlGetAlias` returns funckey settings.

#### Arguments

|  |
| --- | ---
| `t_alias` | Name of the Allegro PCB Editor environment alias.
#### Value Returned

|  |
| --- | ---
| `t_value` | String value of the Allegro PCB Editor environment alias.
| `lt_names` | List of alias names.
| `nil` | Alias not set.
#### See Also

[axlSetAlias](#895302 "8")`,`[axlGetFuncKey](#894759 "8")

#### Example 1

> `alias = axlGetAlias("SF2")`

> `⇒ "grid"`

Gets the value of the alias assigned to shifted function key F2.

#### Example 2

> `list_alias = axlGetAlias(nil)`

> `⇒ ("F2" "F3" "F4" ...)`

Returns all set aliases.

### axlGetFuncKey

`axlGetFuncKey(t_alias/nil)==> t_value/nil`

#### Description

Requests the value of the specified funckey,`t_alias`. If given `nil`, returns a list of currently set funckeys.

#### Arguments

|           |                                      |
| -----------| --------------------------------------|
| `t_alias` | Name of the environment funckey.     |
| `nil`     | Returns list of all current funckeys |
#### Value Returned

|               |                                                                                  |
| ---------------| ----------------------------------------------------------------------------------|
| `t_value/nil` | String value of the environment funckey. Returns`nil` if the funckey is not set. |
| `lt_names`    | If passed`nil,` returns list of funckeys names.                                  |
#### See Also

[axlSetFunckey](#895632 "8")`,`[axlGetAlias](#894702 "8")

#### EXAMPLEs

* Gets the value of the funckey assigned to shifted function key m.

`alias = axlGetFuncKey("m")`

`==> "grid"`

* Return all set aliases.

`list_alias = axlGetFuncKey(nil)`

`==> ("-" "+" "m")`

### axlGetVariable

`axlGetVariable(t_variable )⇒ t_value/nil`

#### Description

Requests the value of the specified Allegro PCB Editor environment variable,`t_variable`. Returns a list containing the string assigned to the variable or `nil` if the variable is currently not set in Allegro PCB Editor. Use `axlGetVariableList` where the variable stores a list of items (such as a PATH variable) to preserve any spaces in each item.

**Note:** Variable names are case insensitive.

* Variable names and values can change from release to release.

#### Arguments

|  |
| --- | ---
| `t_variable` | String giving name of the Allegro PCB Editor environment variable.
| `nil` | If nil, returns a list of all set variables in Allegro PCB Editor
#### Value Returned

|  |
| --- | ---
| `t_value` | List containing string value of the Allegro PCB Editor environment variable.
| `nil` | Variable not set.
| `lt_names` | List of variable names (returned when`nil` is passed)
#### See Also

[axlUnsetVariable](#896847 "8"), [axlSetVariable](#883036 "8"), [axlGetVariableList](#893710 "8"), [axlReadOnlyVariable](#895229 "8") [axlSetVariableFile](#903021 "8"), [axlUnsetVariableFile](#903107 "8")

#### Example

`menu = axlGetVariable("menuload")`

> `==> "geometry"`

`psmpath = axlGetVariable("psmpath")`

> `==> ". symbols"`

* Gets value of the current menu loaded.

> Variable name is`menuload`.

* Gets the value of the library search path`libpath`.

### axlGetVariableList

`axlGetVariableList(t_variable/nil)==> t_value/lt_value/nil`

#### Description

Requests the value of the specified Allegro PCB Editor environment variable,`t_variable`. Unlike `axlGetVariable` this returns a list of strings, if the variable is an array, such as one of Allegro PCB Editor`s path variables. If variable is a single item, the return is the same as `axlGetVariable`.

Since path variables can contain spaces, using the`axlGetVariable` interface and then using the Skill parseString command, to break them back to the component pieces will not give the correct result.

**Note:** Variable names are case insensitive.

**Note:** Variable names and values can change from release to release.

#### Arguments

|  |
| --- | ---
| `t_variable` | Name of the Allegro PCB Editor environment variable.
| `nil` | If`nil,` returns a list of all set variables in Allegro PCB Editor.
#### Value Returned

|  |
| --- | ---
| `t_value` | String value of the Allegro PCB Editor environment variable.
| `nil` | Returns`nil` if the variable is not set.
| `lt_names` | list of variable names, returned when`nil is`passed as the argument
#### See Also

[axlGetVariable](#883023 "8")

#### Example

Gets the value of the Package Symbol search path:

> `path = axlGetVariableList("psmpath")`

> `==> ( "." "symbols" "/cds/root/share/pcb/allegrolib/symbols")`

### axlJournal

`axlTempFile(g_option)==> t_tempFileName`

#### Description

This function manages the program's journal file. It has several modes of operation:

> `g_option = 'close`

> closes current journal file; returns name of closed file

> `g_option = <t_filename>`

> close current journal file and opens no file, returns`t`if successful, `nil` if can't open file. Side effect of failure is current journal file is closed.

> `g_option = 'name`

> returns fullpath name of current journal file,`nil` if no active journal file

* ***Typically the journal file is buffered. Reading the file while it is open may be unpredictable.***

* ***On Windows, an open file for writing cannot be read. You must close it first.***

#### Argument

|  |
| --- | ---
| `g_mode` | see above
#### Value Returned

See above

#### Example

Name of file

> `axlJournal('name)`

Open new file in tmp in current directory

> `axlJournal("my_journal")`

### axlProtectAlias

`axlProtectAlias(t_aliast/nil)⇒ t/nil`

#### Description

Controls the read-only attribute of an alias.

#### Notes

* Do not unprotect F1 as this is fixed to*Help* by the operating system.

* You must define the alias before you can protect it.

#### Arguments

|  |
| --- | ---
| `t_alias` | Name of the Allegro PCB Editor environment alias.
| `t/nil` | `t` protects the alias, and `nil` unprotects the alias.
#### Value Returned

|  |
| --- | ---
| `t` | Successfully protected or unprotected the alias.
| `nil` | Alias is not set, or the function received invalid data.
#### Example

> `axlProtectAlias( "F2" t)`

Protects the F2 function key.

### axlIsProtectAlias

`axlIsProtectAlias(t_alias)⇒ t/nil`

#### Description

Tests if the alias is read-only (or writeable). This may also be used with funckeys.

#### Arguments

|  |
| --- | ---
| `t_alias` | Name of the Allegro PCB Editor environment alias.
#### Value Returned

|  |
| --- | ---
| `t` | Alias is protected.
| `nil` | Alias is unprotected or not set.
#### See Also

[axlIsProtectAlias](#895182 "8")

### axlReadOnlyVariable

`axlReadOnlyVariable(t_variable[g_Enable])==> t/nil`

#### Description

This sets, unsets or queries the read-only state of a Allegro PCB Editor environment variable. When you set a variable as read-only, it cannot be changed.

**Note:** Variable names are case insensitive.

#### Arguments

|  |
| --- | ---
| `t_variable` | The name of the Allegro PCB Editor environment variable.
| `g_Enable` | `t` to set read-only; `nil` to make writable and do not provide if using to test variable read-only state.
#### Value Returned

|  |
| --- | ---
| `t/nil` | In query mode (`no g_Enable` option) returns `t` if variable is read-only and `nil` if not. If changing the read-only mode, returns `t` if successful and `nil` if variable is not currently set.
#### See Also

[axlGetVariable](#883023 "8")`,`[axlGetVariableList](#893710 "8")

#### Examples

The following example:

* Sets`psmpath` to read-only.

* Queries the setting.

* Resets`psmpath` to writable.

Query the setting:

> `axlReadOnlyVariable("psmpath" t)`

> `axlReadOnlyVariable("psmpath")`

> `==> t`

> `axlReadOnlyVariable("psmpath" nil)`

> `axlReadOnlyVariable("psmpath")`

> `==> nil`

Query all read-only variables:

> `axlReadOnlyVariable("fxf" t)`

> `axlReadOnlyVariable("psmpath" t)`

> `axlReadOnlyVariable(nil)`

`==> ("psmpath" "fxf")`

### axlSetAlias

`axlSetAlias(t_aliasg_value)⇒ t/nil`

#### Description

You can set the Allegro PCB Editor environment alias with the name given by the string`t_alias` to the value `g_value` using the `axlSetAlias` function. `g_value` can be a string, int, t, or nil. Returns the string assigned to the alias or `nil` if the alias cannot be set in Allegro PCB Editor.

You can use function keys F2-F12, most Alpha-numeric keys with the control modifier (although Control-C V and X are reserved for copy, paste, and cut) and the Navigation Keys (Home, Up arrow, Esc, etc.) You can modify these items as shown:

|  |  |
| --- | --- | ---
| ****Modifier**** | **Indicator** | **Example**
| Shift | S | SF2
| Control | C (function keys) | CF2
| Control | ~ (alpha-numeric) | -N
| Meta | A | AF2
Modifiers may be combined as shown in these examples:

|  |
| --- | ---
| CSF2 | Control-Shift F2
| ASF2 | Meta-Shift F2
| CAF2 | Control-Meta F2
| CASF2 | Control-Meta-Shift F2
| ~SZ | Control-Shift Z
| SUp | Shift-Up Arrow
| CUp | Control-Up Arrow
Both axlSetFunckey and axlSetAlias share the same data storage.

**Notes:**

* Alias settings only apply to the current session. They are not saved to the user's local env file.

* Alias changes do not affect programs launched from Allegro PCB Editor, for example, import logic, refresh\_symbol.

* To set funckeys, see

  ```
  axlSetFunckey, axlGetAlias, axlProtectAlias, axlIsProtectAlias, axlSetAlias axlGetAlias, axlProtectAlias
  ```

  , and `axlIsProtectAlias.`

#### Arguments

|  |
| --- | ---
| `t_alias` | Name of the Allegro PCB Editor environment alias.
| `g_value` | Value to which the environment alias is to be set. Can be a string or`nil`.
#### Value Returned

|  |
| --- | ---
| `t` | Alias set.
| `nil` | Invalid data or alias is marked read-only.
#### Example 1

> `axlSetAlias( "F2" "save")`

Sets the F2 function key to the*save* command.

#### Example 2

> `axlSetAlias( "~S" nil)`

Unsets the`Ctrl-S` alias.

### axlSetAlias

`axlSetAlias(t_aliasg_value)⇒ t/nil`

#### Description

You can set the Allegro PCB Editor environment alias with the name given by the string`t_alias` to the value `g_value` using the `axlSetAlias` function. `g_value` can be a string, int, t, or nil. Returns the string assigned to the alias or `nil` if the alias cannot be set in Allegro PCB Editor.

You can use function keys F2-F12, most Alpha-numeric keys with the control modifier (although Control-C V and X are reserved for copy, paste, and cut) and the Navigation Keys (Home, Up arrow, Esc, etc.) You can modify these items as shown:

|  |  |
| --- | --- | ---
| **Modifier** | **Indicator** | **Example**
| Shift | S | SF2
| Control | C (function keys) | CF2
| Control | ~ (alpha-numeric) | -N
| Meta | A | AF2
Modifiers may be combined as shown in these examples:

|  |
| --- | ---
| CSF2 | Control-Shift F2
| ASF2 | Meta-Shift F2
| CAF2 | Control-Meta F2
| CASF2 | Control-Meta-Shift F2
| ~SZ | Control-Shift Z
| SUp | Shift-Up Arrow
| CUp | Control-Up Arrow
Both axlSetFunckey and axlSetAlias share the same data storage.

**Notes:**

* Alias settings only apply to the current session. They are not saved to the user's local env file.

* Alias changes do not affect programs launched from Allegro PCB Editor, for example, import logic, refresh\_symbol.

* To set funckeys, see

  ```
  axlSetFunckey, axlGetAlias, axlProtectAlias, axlIsProtectAlias, axlSetAlias axlGetAlias, axlProtectAlias
  ```

  , and `axlIsProtectAlias.`

#### Arguments

|  |
| --- | ---
| `t_alias` | Name of the Allegro PCB Editor environment alias.
| `g_value` | Value to which the environment alias is to be set. Can be a string or`nil`.
#### Value Returned

|  |
| --- | ---
| `t` | Alias set.
| `nil` | Invalid data or alias is marked read-only.
#### Example 1

> `axlSetAlias( "F2" "save")`

Sets the F2 function key to the*save* command.

#### Example 2

> `axlSetAlias( "~S" nil)`

Unsets the`Ctrl-S` alias.

### axlSetFunckey

`axlSetFunckey(_aliasg_value)==> t/nil`

#### Description

Works similar to`axlSetAlias` except allows alpha-number keys to work like function keys (no Enter key required). See `axlSetAlias` for complete documentation.

* Funckey settings only apply to current session. They are not saved to user's local`env` file.

* Funckey changes do not affect programs launched from Allegro PCB Editor: for example,`import logic` or `refresh_symbol.`

#### Arguments

|  |
| --- | ---
| `t_alias` | name of the Allegro environment alias.
| `g_value` | Value to which the environment alias is to be set. Can be a string, or nil.
#### Value Returned

|  |
| --- | ---
| `t` | Returns`t` if successful.
| `nil` | Returns`nil` if invalid data type of alias is marked read only.
#### See Also

[axlGetFuncKey](#894759 "8")`,`[axlIsProtectAlias](#895182 "8")`,`[axlIsProtectAlias](#895182 "8")`,`[axlSetAlias](#895485 "8")

#### Examples

Set the funckey alias to move

`axlSetFunckey( "m" "move" t)`

Unset the move

`axlSetFunckey( "m" nil)`

### axlSetVariable

`axlSetVariable(t_variable [g_value])⇒ t/nil`

#### Description

Sets the Allegro PCB Editor environment variable with name given by the string`t_variable` to the value `g_value`. `g_value` can be a string, int, `t`, or `nil`. Returns the string assigned to the variable or `nil` if the variable cannot be set in Allegro PCB Editor.

**Note:** 511 is the maximum list long (`lt_variable`).

> **Notes:**

* Variable names and values can change from release to release.

* Variable settings only apply to current session. They are not saved to local env file for the user.

* Variable changes do not effect programs launched from Allegro PCB Editor. For Example, import logic, refresh\_symbol

* Many Allegro operations are done via batch operations such as items in File Import/Export, artwork, axlRunBatchDBProgram, and so on. These operations do NOT see variables changed (like PSMPATH) by this call or by the Allegro set command.

#### Arguments

|  |
| --- | ---
| `t_variable` | String giving the name of the Allegro PCB Editor environment variable.
| `g_value` | Value to which the environment variable is to be set. Can be a string, int,`t`, or `nil`.
#### Value Returned

|  |
| --- | ---
| `t` | Environment variable set.
| `nil` | Environment variable not set.
#### See Also

[axlGetVariable](#883023 "8"), [axlReadOnlyVariable](#895229 "8"), [axlSetVariableFile](#903021 "8"), [axlUnsetVariable](#896847 "8"), [axlUnsetVariableFile](#903107 "8")

#### Example

Sets new library search path`libpath`.

> `(axlSetVariable "libpath" "/mytools/library")⇒ t`

> `libraryPath = (axlGetVariable "libpath")⇒ "/mytools/library"`

Using list mode.

> `axlSetVariable("psmpath" '("." "symbols"))`

> `==> t`

> `axlGetVariableList("psmpath")`

> `==> ("." "symbols")`

### axlSetVariableFile

`axlSetVariableFile(t_variableg_value)==> t/nil`

#### Description

Sets and saves to file Allegro environment variable. This operates the same as[axlSetVariable](#883036 "8") except it also saves the setting to the user's local environment file.

Variable is added in the preference section of the env file.

* ***On Windows, updating the environment file on disk can cause performance issues if this interface is used heavily.***

#### Arguments

|  |
| --- | ---
| `t_variable` | Name of the Allegro environment variable.
| `g_value` | Value to which the environment variable is to be set. Can be a`string`, `int`, `t`, or `nil`.
#### Values Returned

|  |
| --- | ---
| `t/nil` | Returns`t` if successful. Returns `nil` if invalid data type of variable is marked read-only.
#### See Also

[axlSetVariable](#883036 "8"), [axlUnsetVariableFile](#903107 "8")

### axlShell

`axlShell(t_command)⇒ t`

#### Description

Issues the Allegro PCB Editor command string`t_commands` to the connected editor. You can chain commands. This call is synchronous.

* This function might not be portable across Allegro PCB Editor releases.

#### Arguments

|  |
| --- | ---
| `t_command` | Allegro PCB Editor shell command or commands.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### See Also

[axlShellPost](#896845 "8")

#### Example 1

> `(axlShell "status")⇒ t`

Displays Allegro PCB Editor Status form from AXL-SKILL.

**Example 2**

> `axlShell("zoom points; pick 0 0; pick 100 100")`

Chained command example:

### axlShellPost

`axlShellPost(t_command) ==> t`

#### Description

This works similar to`axlShell` except it first requires a return from the Skill interpreter before executing the command(s). It should only be used in the special circumstance where you want to do some processing in Skill, execute an Allegro PCB Editor interactive command and have that command be left active for the user. If more the one command is embedded in post command then subsequent commands should be prefixed with an underscore to inhibit scripting. For example:

> `axlShellPost("zoom points; _pick 10 20")`

* ***Do not attempt to use this as a method to override an existing Allegro PCB Editor command with Skill code and then call the original command. An infinite loop will result.***

* ***This function may not be portable across Allegro PCB Editor releases.***

#### Arguments

|  |
| --- | ---
| `t_command` | Allegro PCB Editor shell command or commands.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t.`
#### See Also

[axlShell](#903025 "8")

#### EXAMPLES

Over the`move` command to print hello and then let user move objects.

`axlCmdRegister( "mymove" 'testSkill ?cmdType "interactive")`

`procedure( testSkill()`

`printf("Hello mymove\n")`

`axlShellPost("echo hello from post; _move")`

`printf("Hello after-mymove\n")`

)

`Output -- showing deferred execute:`

`Hello mymove`

`Hello aftermove`

`hello from post`

`Select element(s) to move.`

### axlUnsetVariable

`axlUnsetVariable(t_variable)⇒ t`

#### Description

Unsets the Allegro PCB Editor environment variable with the name given by the string`t_variable`. The value of the named variable becomes `nil`.

* Variable names and values can change from release to release.

#### Arguments

|  |
| --- | ---
| `t_variable` | String giving the name of the Allegro PCB Editor environment variable.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### See Also

[axlSetVariable](#883036 "8")

Example

> `(axlUnsetVariable "libpath")⇒ "/mytools/library"`

> `libraryPath = (axlGetVariable "libpath")⇒ nil`

Clears the library path`libpath` when its current value is `/mytools/library`*.*

### axlUnsetVariableFile

`axlUnsetVariableFile(t_variable )==> t`

#### Description

Unsets the value of specified Allegro environment variable. Works the same as[axlUnsetVariable](#896847 "8") plus it also updates the local environment file of the user with the change.

* ***On Windows, updating the environment file on disk can cause performance issues if this interface is used heavily.***

#### Arguments

|  |
| --- | ---
| `t_variable` | String giving the name of the Allegro environment variable.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns t.
#### See Also

[axlSetVariableFile](#903021 "8"), [axlSetVariable](#883036 "8")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
