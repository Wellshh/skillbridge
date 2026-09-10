<!--
source: algroskill/10usrint.md
part: 2/2
estimated_tokens: 1853
-->

### axlUIWTimerAdd

`axlUIWTimerAdd( o_window x_timeout g_oneshot u_callback ) => o_timerId/nil`

#### Description

Adds or removes a callback for an interval timer.

This is not a real-time timer. It is synchronous with the processing of window based messages. The actual callback interval may vary. The timer does not go off (and call you back) unless window events for the timer window (`o_window`) are being processed. You must be waiting in a UI related call (for example, `axlEnter*`, a blocking `axlFormDisplay`, `axlUIWBlock`, etc.)

To receive callbacks return to the main program message processing. Another window in blocking mode, however, can delay your return to the main program.

You may add properties to the returned `timerId` to store your own data for access in your timer callback.

Points to be remembered while using the provided callback function.

- Processing in the callback should be relatively short in time

- Do not open or save the design

- Do not open or close forms or windows

- dbids may become stale

- axlAddSimpleRbandDynamics should not be used.

- Too many triggers active can impede performance.

- Allegro dbids are only valid within the callback. You cannot pass dbids in or out of this callback function. You always need to refetch them from the database.

#### Arguments

| Name | Description |
|---|---|
| `o_window` | The window the timer is associated with. If `o_window` is `nil`, the timer is associated with the main window. |
| `x_timeout` | Timeout in milliseconds before the timer is triggered and calls your callback procedure. Timeout is not precise because it depends on processing window messages. |
| `g_oneshot` | Controls how many times the timer triggers. Use one of these values: `t` - Timer goes off once and automatically removes itself. `nil` - Timer goes off at the set time interval continuously until it is removed by `axlUIWTimerRemove`. |
| `u_callback` | Procedure called when the timer goes off. Called with these arguments with its return value ignored: `u_callback``( o_window o_timerId n_elapsedTime o_window:`Window you provided to `axlUIWTimerAdd o_timerId:`Timer id which returned by `axlUIWTimerAdd`. `x_elapsedTime:`Approximate elapsed time in milliseconds since the timer was added. |

#### Value Returns

| Name | Description |
|---|---|
| `o_timerId` | The identifier for the timer. Use this to remove the timer. This return value is subject to garbage collection when it goes out of scope. When the garbage is collected, the timer is removed. Do not count on garbage collection to remove the timer, however, because you do not know when garbage collection will start. If you need a timer that lasts forever, assign this to a global variable. |
| `nil` | No timer added. |

#### Examples

- Basic:

- Other examples can be found at `<cdsroot>``/share/pcb/examples/skill/ui/timer.il`

#### See Also

axlUIWTimerRemove

### axlUIWTimerRemove

`axlUIWTimerRemove( o_timerId ) => t/nil`

#### Description

`procedure( YourSkillProcedure() ; set up a continuous timer using the main window timerId = axlUIWTimerAdd(nil 2000 nil 'YourTimerCallback) timerId->yourData = yourdata ) procedure( YourTimerCallback( window timerId elapsedTime) ; your time period has elapsed. do something. )` Removes a timer added by `axlUIWTimerAdd`.

#### Arguments

| Name | Description |
|---|---|
| `o_timerId` | Id returned by `axlUIWTimerAdd`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Timer removed. |
| `nil` | Timer id invalid. |

### axlUIWUpdate

`axlUIWUpdate( r_window/nil ) => t/nil`

#### Description

Forces an update of a window. If you made several changes to a window and are not planning on going back to the main loop or doing a SKILL call that requires user interaction, use this call to update a window. You could use this, for example, if you are doing time-consuming processing without giving back the control to the UI message pump.

To use, make all your window changes and then make this call. If window ID is `nil,` exposes the main window.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window id or `nil` if the main window. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Window updated. |
| `nil` | Window already closed or invalid window ID. |

### axlUIYesNoCancel

`axlUIYesNoCancel( t_message [t_title] [s_default] ) => x_result`

#### Description

Displays a blocking Yes`/`No`/`Cancel dialog box with the prompt message provided.

#### Arguments

| Name | Description |
|---|---|
| `t_message` | Message to display. |
| `t_title` | Optional. What to put in the title bar of confirm. The default is the program display name. |
| `s_default` | Optional. May be either `yes`, `no` or `cancel` to specify default response. The default is `yes`. |

#### Value Returns

| Name | Description |
|---|---|
| `x_result` | Number based on the user's choice: `0` for No `1` for Yes `2` for Cancel |

### axlUIDataBrowse

`axlUIDataBrowse( s_dataType ls_options t_title g_sorted [t_helpTag] [l_callback] [g_args] ) => lg_return`

#### Description

Analyzes all objects requested by the caller function, passing each through the caller's callback function. Then puts the objects in a single-selection list.

This list blocks until a user makes a selection. Once the user selects an object, it is passed back to the caller in a list containing two objects: the selected name and, for a database object, the AXL dbid of the object.

#### Arguments

| Name | Description |
|---|---|
| `s_dataType` | One of the following:`' NET 'PADSTACK 'PACKAGE_SYMBOL 'DEVICE 'PARTNUMBER 'REFDES 'BOARD_SYMBOL 'FORMAT_SYMBOL 'SHAPE_SYMBOL 'FLASH_SYMBOL 'BRD_TEMPLATE 'SYM_TEMPLATE 'TECH_FILE` |
| `ls_options` | List containing at least one of the following:<br><br>`'RETRIEVE_OBJECT:`Object selected returns its dbid `'RETRIEVE_NAME:`Object selected returns its name `'EXAMINE_DATABASE:`Initially look in the database for list of objects `'EXAMINE_LIBRARY:`Initially use env PATH variable when looking for list of objects `'DATABASE_FIXED:`Read-only check box for the database `LIBRARY_FIXED:`Read-only check box for files (library) |
| `t_title` | Prompt for the title of the dialog |
| `g_sorted` | Switch indicating whether or not the list should be sorted |
| `t_helpTag` | Help tag for the browser |
| `l_callback` | Callback filter function which takes the arguments name, object, and `g_arg` passed in. Returns t or nil based on whether or not the object is eligible for browsing. |
| `g_arg` | Generic argument passed through to `l_callback` as the third argument. |

#### Value Returns

| Name | Description |
|---|---|
| `t_name o_dbid` | Selection was made and RETRIEVE_OBJECT used. |
| `t_name nil` | Selection was made and RETRIEVE_NAME used. |

#### Examples

`axlUIDataBrowse('NET '(RETRIEVE_NAME) "hi" t)`

`axlUIDataBrowse('PADSTACK '(RETRIEVE_NAME) "hi" t)`

`axlUIDataBrowse('PACKAGE_SYMBOL '(EXAMINE_DATABASE EXAMINE_LIBRARY``RETRIEVE_NAME)"hi" t)`

`axlUIDataBrowse('PACKAGE_SYMBOL '(EXAMINE_LIBRARY RETRIEVE_OBJECT) "hi" t)`

`axlUIDataBrowse('PACKAGE_SYMBOL '(EXAMINE_LIBRARY RETRIEVE_NAME) "hi" t)`

`axlUIDataBrowse('PARTNUMBER '(RETRIEVE_OBJECT) "Part Number" t)`

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

