### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

28
==

Plugin Functions
================

Overview
--------

This chapter describes the AXL-SKILL functions related to plugin APIs.

The axlDll family of APIs provides the ability to bind compiled Dll (shared library) packages into programs supporting the Skill axl APIs. Any publically exported functions from a Dll can be imported. The only restriction is that exported Dll functions must support the API specified below.

Any reference to 'DLL' is the equivalent to a shared library for UNIX and Linux programmers. All UNIX references apply to Linux.

Creating a plugin requires two components:

* Skill code to import and wrap the functionality provided by the dll.

* The dll/shared library implementing the plugin functionality.

### SKILL Programming

The Skill progamming model for plugins is:

* Locate and open a plugin via`axlDllOpen`. We suggest assigning a handle to a global Skill symbol. On subsequent calls into your Skill application, the symbol will be non-nil, so the call to `axlDllOpen` can be skipped. (See `axlDllOpen`.)

* Import the required symbols from the plugin via`axlDLLSym`. Like the handle returned by `axlDllOpen`, these handles should be assigned to global symbols.

* Use either`axlDllCall` or `axlDllCallList` to access the capability from the plugin.

* The I/O data types that are supported are documented in`axlDllCall`.

### DLL Programming

DLL programming allows the use of external developers to utilize existing C/C++ code or devevlop new capabilities in C/C++ to plugin as extensions to SPB software. SPB software supporting this capability are those that incorporate the "axl" extension package to Skill.

Implementation of a plugin dll:

* Obtain the compiler environment required by Cadence. (See the Allegro platform documentation.)

* Use the existing Cadence Makefile (UNIX) or Project file (Microsoft) which contains the required compile/link options. You can use these files to build your plugin to adapt your own software configuration environment. (See`<cdsroot>/share/pcb/examples/skill/plugin.`)

* Ensure that the exported Dll functions meet the API requirements. (See API plugin functions below). The include file,`<cdsroot>/share/pcb/include/axlplugin.h,` has the required structure definitions and defines.

* Build your plugin.

* Test it.

Required Cadence files for plugin programming:

`<cdsroot>/share/pcb/include/axlplugin.h`

#### API Plugin Functions

The C API for any plugin function is as follows:

`long <function>(AXLPluginArgs *output, AXLPluginArgs *input)`

The API takes identical structures for both its input and output arguments. The calling Cadence software updates the input structure with the data passed by the calling Skill code. It also initializes the output structure.

The Plugin function must return a value and optionally update the output structure with return data (`argv` and `count`). The plugin return value is passed back to the calling Skill code as follows:

`return == 0` Returns a list of from output data structure up to the count value. If count in output structure is 0, returns an empty list.

`return != 0` Return value is returned to Skill as an integer.

#### AXLPluginArgs Input/Output Structure Members

`version = AXLPLUGIN_VERS_IN` Version of input structure. If additional capability is added in the future, this version number will be bumped. It informs the plugin of the capability supported in the structure.

`flag = 0` Future use

`maxEntries = AXLPLUGIN_MAX` Can be ignored on input. On ouput, you cannot exceed this value for return arguments.

`count = <number of argv entries>` Number of entries in `argv`. Basically, the number of arguments provided to the `axlDLLCall` APIs. Will never be more the `maxEntries`.

`argv[]` Array of `AXLPluginEntry` arguments

#### AXLPluginEntry (argv) Structure Members

(See Input/Output Data Primitives.)

`type` Indicates type of data

`data` Union of primitive types supported

For the called Dll function to return data to calling Skill code, both`set the count` and `argv` entries should be set in the output data structure. For each `argv` entry return, you should also set the data type to one of the primitives shown below. Under no situation should you attempt to return more then `maxEntries`.

If your exported dll functions will be used outside your progamming environment, then you should valid check the input arguments either in the Skill wrapper or in your Dll function. For example, if you expect a string argument and the calling Skill code passes an integer, a program exception will occur if the data is not checked.

### Input/Output Data Primitives

A set of I/O data primitives is supported. The`argv` entry of `AXLPluginArgs` is an array of these structures. Each array member has its data type indicated and the data itself. Both the input and output data use the `AXLPluginArgs` structure.

The data primitives that are supported are:

|  |  |  |
| --- | --- | --- | ---
| ****Type**** | **Skill type** | **C type** | **C struct member**
| AP\_BOOL | t/nil | int | b\_value
| AP\_LONG | x\_value | long | l\_value
| AP\_DOUBLE | f\_value | double | d\_value
| AP\_CONST\_STRING | t\_value/s\_value | char \* | cs\_value
| AP\_STRING | t\_value | char \* | s\_value (output only)
| AP\_XY | f\_value:f\_value | AXLXY | xy\_value
`AP_STRING` types will not be seen on input. All strings passed from Allegro to the plugin are `AP_CONST_STRING`. To return a string, the plugin may use either `AP_CONST_STRING` or `AP_STRING`. If `AP_STRING` is used, then Allegro will free the memory associated with the string using the standard C "free" API, which means you must allocate it via `malloc`.

Other data type restrictions are:

* The plugin must not modify in place any input`AP_CONST_STRING`; corruption of Skill will occur.

* To maintain`AP_CONST_STRING` input data across function calls, you should make a copy of them. Skill may garbage collect the memory after your Dll function returns.

* If you use your own memory manager, do not use`AP_STRING` types for return. These require the use the standard `malloc` memory manager.

* Input arguments can be Skill symbols (`'<symbol>`) but these are converted to `AP_CONST_STRING` types.

* The`STRING` types do not support wide character sets; use only characters in the ASCII character set.

* `AP_XY` reprensents a (x y) location and is implemented as a structure of two doubles.

* If`AP_BOOL` type is used, two defines are provided in `axlplugin.h`:

* `AXLPLUGIN_TRUE = 1`

* `AXLPLUGIN_FALSE = 0`

Return value from plugin exported back to Skill:

* If`output->count` is 0, then the we look at the return value from the plugin function and return `x_value` to symbol.

* Else (non-zero count), we return this value to Skill as a Skill integer type.

### Programming Restrictions, Cautions and Hints

* Cadence only supports the compiler listed in the SPB Platform documentation. Also required are any compiler and DLL linker options listed.

* If your DLL has dependancies upon other Dlls, make sure those do not conflict with Dlls used by Cadence. Typically, they need to be the same version and not built with debug options.

> To determine the DLLs used by Cadence use:

* Window:`depends` or `procexp` (`www.sysinternals.com`)

* Solaris, Linux:`ldd <program name>`

* AIX:`dump -H <program name>`

* On Windows, you can include UI components in your plugin. This capability is not supported on Unix.

* Wide character types are not supported in the plugin to the Allegro interface.

* On Unix, if threading is used, then you should`POSIX` threads (`pthreads`).

* STL programming should use the default STL provided by the Cadence required compiler. Do not use a third party STL.

* On Windows, if DLL is MFC based, then do not compile it debug. MFC Classes change in size if code is built debug and are not compatible with non-debug MFC code. There are methods described on the Web on how to build MFC debuggable without requiring the MFC debug shared library. Typically on Windows, Debug Dlls are not compatible with non-Debug Dlls. Also many different versions of MFC exist which are impatible with one another. Use one of the binary query tools (see above) to determine the version of MFC currently required by Cadence.

* There are currently no methods to make function calls back to Allegro from the plugin.

* Your DLL can be used across multiple Cadence releases without recompiling your plugin. Re-compiling is only required if Cadence changes the compiler in the release.

* Programming errors in your plugin can crash the host program. In rare cases, these bugs can corrupt an Allegro database. (See customer support below.)

* On Windows, to access`stdout/stderr`, set the `TELCONSOLE=1` as the OS level. This variable cannot be set via Allegro's `env` file. This is also considered a debug environment so it should not be used during board design.

### Performance Considerations

The following issues should be considered if high performance is required:

* Locating and loading a plugin. This should be done once per activation. Assign the handle return by`axlDllOpen` to a global symbol to prevent Skill garbage collection. Do not close the plugin.

* Import symbols of a plugin once. The`axlDll` interface internally caches symbol import so subsequent lookups will be faster than the initial call.

* A plugin function should do meaningful work since there is some overhead converting input data from Skill to native C types and doing the opposite for return data.

### Cadence Customer Support

Cadence does not supporting debugging customer developed plugins.

An environment variable,`allegro_noextension_plugin`, is available to disable plugin capability. If Allegro starts crashing or databases become corrupt, you should set this variable to determine if a plugin is the cause.

### Examples

An example containing Skill, the plugin C code, Gnu Makefile (UNIX) and project file (Visual.NET) is contained at`<cdsroot>/share/pcb/examples/plugin`. In addition, a prebuilt plugin module is contained in the Cadence install hierarchy so you do not need to compile and link the plugin source code to run the Skill code.

The example plugin provided has three exported symbols:

* An echo API which returns as output any input given.

* A`x_value` API which returns the number of input arguments.

* A distance implementation to calculate the distance between two points.

### axlDllCall

`axlDllCall(`

`o_pluginFunc`

`[g_arg1]`

`...`

`[g_arg10]`

`) -> nil/x_value/lg_data`

#### Description

Calls a symbol that has been imported from a plugin. As the first argument, it requires`o_pluginFunc` which was returned via a call to `axlDllSym`. The rest of the arguments are what the implement plugin API has defined.

The return from the call is one of the following:

* `nil`: error processing data

* `x_value`: plugin function returned a non-zero result

* `lg_data`: plugin function returned a zero and it calls the import function from the plugin

#### Arguments

`o_pluginFunc` plugin symbol handle

`[g_arg1..10]` up to 10 arguments

#### Value Returned

`nil` Error in processing arguments or funding functions.

`x_value` If plugin function returns a non-zero, then this is what is returned.

`lg_data` If plugin function returns zero, then its output arguments are processed and returned as a list. If the output argument list from the plugin has 0 entries, then an empty list is returned.

#### See Also

[axlDllOpen](#1087703 "28")

#### Example

Example carried from`axlDllSym`

`axlDllCall(_ashDistance 10:0 25.1:0) -> 15.1`

### axlDllCallList

`axlDllCall(    o_pluginFunc    l_args/nil) -> nil/x_value/lg_data`

#### Description

This function is identical to`axlDllCall` except it takes a list of arguments to pass to the plugin function. Unlike `axlDllCall,` which is limited to 10 arguments, this interface can take up to 512 arguments.

See`axlDllCall` for a further explanation.

#### Arguments

`o_pluginFunc` Plugin symbol handle

`l_args` A list of up to 512 arguments

#### Value Returned

`nil` Error in processing arguments or funding functions.

`x_value` If plugin function returns a non-zero, then this is what is returned.

`lg_data` If plugin function returns zero, then its output arguments are processed and returned as a list. If the output argument list from the plugin has 0 entries, then an empty list is returned.

#### See Also

[axlDllCall](#1082969 "28")`,`[axlDllOpen](#1087703 "28")

#### Example

From`axlDllOpen` example

`_ashEcho = axlDllSym(_ashTestDll "ashEcho")`

`axlDllCallList(_ashEcho list(-1 -2.0 nil "another string"`

`-10.1:-2 0.2))`

### axlDllClose

`axlDllClose(o_plugin)==> t/nil`

#### Description

This closes an open plugin handle. Once a handle is closed, you can no longer call functions obtained from the plugin. Also, a plugin is automatically closed when there are no active references to it via Skill's garbage collection.

It is not advisable to close a plugin due to performance considerations.

#### Arguments

`o_plugin` Plugin handle obtained from `axlDllOpen`.

#### Value Returned

`t` if successful to close, `nil` if handle is not a legal handle

#### See Also

[axlDllOpen](#1087703 "28")

#### Example

See example referenced by`axlDllOpen`.

### axlDllDump

`axlDllDump()==> l_dllLoad/nil`

#### Description

This is a debug function that reports all plugins loaded by Skill.

#### Arguments

None

#### Value Returned

List of plugin handles or`nil` if no loaded plugins.

#### See Also

[axlDllOpen](#1087703 "28")

#### Example

`axlDllDump()`

### axlDllOpen

`axlDllOpen(t_dllname)==> o_plugin/nil`

#### Description

This binds a dll/shared library to the current program. While this can load any dll, only those built to be compatible with the axl Plugin model can be utilized via Skill (see[DLL Programming](#1084169 "28") for information on building compatible dlls).

If the dll name does not have a directory path component, then`AXLPLUGINPATH` environment variable is used to search for the dll.

After a dll is successfully loaded, you need to import one or more symbols (`axlDllSym`).

Plugin Attributes

|  |  |
| --- | --- | ---
| **Name** | **Type** | **Description**
| name | string | Name of plugin file (dll name)
| functions | l\_dbid | Disembodied property list name/value pairs of imported symbols (`t_name o_pluginFunc`)
| objType | string | "plugin"
**Note:** To access imported plugin function types do a

> `<o_plugin>->functions-><pluginFuncName>`

#### Arguments

`t_dllname` Name of dll. For platform indendence, it is strongly suggested that you do not include the file extension or a directory path component.

#### Value Returned

`o_plugin`

`nil` Can't locate library or not a dll.

#### See Also

[DLL Programming](#1084169 "28")`,`[axlDllSym](#1088093 "28")`,`[axlDllCall](#1082969 "28")`,`[axlDllCallList](#1091355 "28")[axlDllClose](#1083879 "28")`,`[axlDllDump](#1083931 "28")

#### Example

Open Cadence test dll

`_ashTestDll = axlDllOpen("axlecho_plugin")`

### axlDllSym

`axlDllSym(o_plugint_symbolName)==> o_pluginFunc/nil`

#### Description

This imports a symbol from a loaded dll. A dll can have one or more exported symbols. The symbol must have been exported from the dll when the dll was compiled and linked (See`axlDllDoc`).

PluginFunc Attributes

|  |  |
| --- | --- | ---
| **Name** | **Type** | **Description**
| name | string | Name of imported symbol file
| functions | nil | Always`nil`
| objType | string | "pluginFunc"
#### Arguments

`o_plugin` dll handle from `axlDllOpen`

`t_symbolName` Name of an exported function within the dll

#### Value Returned

`o_pluginFunc` Symbol handle

`nil` Error; symbol not present in dll.

#### See Also

[axlDllOpen](#1087703 "28")

#### Example

Load the distance symbol from the axl plugin test dll

`_ashDistance = axlDllSym(_ashTestDll "ashDistance")`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
