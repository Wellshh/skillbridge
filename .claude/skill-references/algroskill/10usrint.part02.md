<!--
source: algroskill/10usrint.md
part: 2/2
estimated_tokens: 4375
-->

|  |
| --- | ---
| `r_window` | Window`dbid`.
| `t_formatString` | Context message (`printf`-like) format string.
| `g_arg1...` | Any number of substitution arguments to be printed using`t_formatString`. Use as you would a C-language `printf` statement.
#### Value Returned

|  |
| --- | ---
| `t` | Message printed to window.
| `nil` | `dbid` is not of a window.
#### Example

> `axlUIWPrint(nil "Please enter a value:")`

> `Please enter a value:⇒ t`

Prints a message in the main window.

### axlUIWRedraw

`axlUIWRedraw(r_window/nil`

`)`

`⇒ t/nil`

#### Description

Redraws the indicated window. If the window`dbid` is `nil`, redraws the main window.

#### Arguments

|  |
| --- | ---
| `r_window` | Window`dbid` or, if `nil`, the main window.
#### Value Returned

|  |
| --- | ---
| `t` | Window is redrawn.
| `nil` | `dbid` is not of a window.
### axlUIWBlock

`axlUIWBlock(r_window`

`)`

`⇒ t/nil`

#### Description

* ***This function is not compatible with the g\_nonBlock = nil option to axlFormCreate. If using this function with axlFormCreate you must set a callback on the g\_formAction.***

This places a block on the indicated window until it is destroyed. All other windows are disabled. It may be called recursively, unlike the block option in`axlFormCreate`.

Once you enter a blocking mode you should not bring up a window that is non-blocking. This behavior is not defined and is not supported.

If you block, you should set the block attribute`block` in the Window Placement list `lt_placement` so that the title bar shows it is a blocking window.

If you have a window callback registered you must allow the window to close since the unblock facility unblocks other windows upon close so that the correct window will get the focus after the blocked window is destroyed.

**Note:** You should set the block symbol option using the*lt\_placement* option in the function that creates the window to visually indicate that the window is in blocking mode.

#### Arguments

|  |
| --- | ---
| `r_window` | Window`dbid`.
#### Value Returned

|  |
| --- | ---
| `t` | Success
| `nil` | Failure (For example, the window is closed or the`dbid` is not of a window).
### axlUIEditFile

`axlUIEditFile(t_filenamet_title/nilg_block`

`)`

`⇒ r_window/t/nil`

#### Description

Allows the user to edit a file in an OS independent manner (works under both UNIX and Windows.)

User may override the default editor by setting either the`VISUAL` or `EDITOR` environment variables.

**Windows notes**

* The default editor is*Notepad*.

* The title bar setting is not supported.

**Unix notes**

* The default editor is`vi`.

* An additional environment variable,`WINDOW_EDITOR`, allows the user to specify an
  X-based editor such as `xedit`. The title bar is not supported in this mode.

**Note:** In blocking mode, the windows of the main program do not repaint until the file editor window exits.

Only`axlUIWClose` supports the `r_window` handle returned by this function.

#### Arguments

|  |
| --- | ---
| `t_filename` | Name of file to edit.
| `t_title` | Title bar name, or`nil` for default title bar.
| `g_block` | Flag specifying blocking mode (`t`) or non-blocking mode (`nil`).
#### Value Returned in Non-blocking Mode

|  |
| --- | ---
| `r_window` | Success
| `nil` | Failure
#### Value Returned in Blocking Mode

|  |
| --- | ---
| `t` | Success
| `nil` | Failure
### axlUIMultipleChoice

`axlUIMultipleChoice(t_questionlt_answers[t_title]`

`)`

`⇒ x_answer/nil`

#### Description

Displays a dialog box containing a question with a set of two or more answers in a list. You must choose one of the answers to continue. Returns the chosen answer.

#### Arguments

|  |
| --- | ---
| `t_question` | Text of the question for display.
| `lt_answers` | A list of text strings that represent the possible answers.
| `t_title` | Optional title. If not present, a generic title is provided.
#### Value Returned

|  |
| --- | ---
| `x_answer` | An integer number indicating the answer chosen. This value is zero-based, that is, a zero represents the first answer, a one the second answer, and so on.
| `nil` | An error is detected.
#### Example

`ret = axlUIMultipleChoice("Pick a choice"`

`'("Pick me" "No Pick me" "I'm here!") "Cmd title")`

### axlUIViewFileScrollTo

`axlUIViewFileScrollTo(r_windowMsgx_line/nil)⇒ x_lines/nil`

#### Description

Scrolls to a specified line in the file viewer. A value of`-1` goes to the end of the viewer.

**Note:** The number of the line in the view window may not match the number of lines in the file due to line wrapping in the viewer.

* ***With the html based viewer the command is unable to return the number of items in scroll window. Return is only valid for the legacy text window.***

#### Arguments

|  |
| --- | ---
| `r_windowMsg` | Existing view window.
| `x_line` | Line to scroll:  `0` is top of the file,  `-1` is bottom of the file,  `-2` returns the number of lines in the viewer.
#### Value Returned

|  |
| --- | ---
| `x_lines` | Number of lines in the view window.
| `nil` | No view file window.
#### Example

> `pm = axlUIViewFileCreate("topology.log" "Topology" nil)`

> `axlUIViewFileScrollTo(pm -1)`

* Displays the file`topology.log`

* Scrolls to the end of the file

### axlUIWBeep

`axlUIWBeep()⇒ t`

#### Description

Sends an alert to the user, usually a beep.

#### Arguments

`None`

#### Value Returned

`None`

#### Example

`axlUIWBeep()`

### axlUIWDisableQuit

`axlUIDisableQuit(o_window`

`)`

`⇒ t/nil`

#### Description

Disables the system menu*Quit* option so the user cannot choose it to close the window.

#### Arguments

|  |
| --- | ---
| `o_window` | Window handle.
#### Value Returned

|  |
| --- | ---
| `t` | Window handle is valid.
| `nil` | Window handle is invalid.
### axlUIWExposeByName

`axlUIWExposeByName(t_windowName`

`)`

`⇒ t/nil`

#### Description

Finds a window by name and exposes it (raises it to the top of the window stack and restores it to a window state it if it is an icon).

You can use the`setwindow`command argument to get Allegro PCB Editor window names via scripting. If the window is a form, you get the name by removing the `form.` prefix from its name.

**Note:** Names of windows may change from release to release.

To raise an item in the control panel, (for example,*Options*,) use the `axlControlRaise()` function.

#### Arguments

|  |
| --- | ---
| `t_windowName` | Window name.
#### Value Returned

|  |
| --- | ---
| `t` | Window is found.
| `nil` | Window is not found.
### axlUIWPerm

`axlUIWPerm(r_window[t/nil]`

`)`

`⇒ t/nil`

#### Description

Normally forms and other windows close automatically when another database opens. This function allows that default behavior to be overridden.

**Notes:**

* When you use this function, consider that windows automatically close when a new database opens because the data the windows display may no longer apply to the new database.

* If you do not provide a second argument, returns the current state of the window.

#### Arguments

|  |
| --- | ---
| `r_window` | Window id.
| `t`/`nil` | `t` - set permanent  `nil` - reset permanent.
#### Value Returned

|  |
| --- | ---
| `t` | Window exists.
| `nil` | Window does not exist.
#### Example 1

> `handle = axlFormCreate('testForm "axlform" nil 'testFormCb, t nil)`

> `axlUIWPerm(handle t)`

Opens a test form and makes it permanent.

#### Example 2

> `ret = axlUIWPerm(handle)`

Tests whether the window is permanent.

### axlUIWSetHelpTag

`axlUIWSetHelpTag(r_windowt_tag)⇒ t/nil`

#### Description

This has been mostly replaced by[axlUIWHelpRegister](#404919 "10") that works for commands and forms.

Attaches the given help tag to a pre-existing dialog with a port. This function supports subclassing of the help tags, that is, if a help tag is already associated with the dialog, it will not be replaced. This functions adds the new help tag. Adding a new help tag to a pre-existing one is done by concatenating the two with a dot.

For example:

|  |
| --- | ---
| Pre-existing Help Tag: | myOldTag
| New Help Tag: | myNewTag
| Resulting Help Tag: | myOldTag.myNewTag
#### Arguments

|  |
| --- | ---
| `r_window` | Window id.
| `t_tag` | Subclass of the help string.
#### Value Returned

|  |
| --- | ---
| `t` | Help tag attached.
| `nil` | Invalid arguments.
#### See Also

[axlUIWHelpRegister](#404919 "10")

### axlUIWSetParent

`axlUIWSetParent(o_childWindowo_parentWindow/nil`

`)`

`⇒ t/nil`

#### Description

Sets the parent of a window. When a window is created, its parent is the main window of the application, which is sufficient for most implementations. To run blocking mode on a form launched from another form, set the child form's parent window to be the launched form.

Setting the parent provides these benefits:

* Allows blocking mode to behave correctly.

* If the parent is closed, then the child is also closed.

* If the parent is iconified, then the child is hidden.

* The child stays on top of its parent in the window stacking order.

#### Arguments

|  |
| --- | ---
| `o_childWindow` | Child window handle.
| `o_parentWindow` | Parent window (if`nil`, then the main window of the application which is normally the default parent.)
**Note:** A parent and child cannot be the same window.

#### Value Returned

|  |
| --- | ---
| `t` | Parent is successfully set.
| `nil` | Could not set the parent due to an illegal window handle.
### axlUIWShow

`axlUIWShow(r_window/nils_option)⇒ t/nil`

#### Description

Shows or hides a window depending on the option passed. If the window id passed is`nil`, the function applies to the main window.

**Notes:**

* Using the`showna` option on a window may make the window active.

* Using the`show` option on a window that is already visible may not make it active.

#### Arguments

|  |
| --- | ---
| `r_window` | The window id. If`nil,` signifies the main window.
| `s_option` | One of the following:
|  | 'show:Show and activate the window
|  | 'showna:Show but don't activate the window.
|  | 'hide:Hide the window.
|  | nil:Show available options.
#### Value Returned

|  |
| --- | ---
| `t` | Window shown or hidden.
| `nil` | Window id not correct or an invalid option given.
### axlUIWTimerAdd

`axlUIWTimerAdd(o_windowx_timeoutg_oneshotu_callback)⇒ o_timerId/nil`

#### Description

Adds or removes a callback for an interval timer.

This is not a real-time timer. It is synchronous with the processing of window based messages. The actual callback interval may vary. The timer does not go off (and call you back) unless window events for the timer window (`o_window`) are being processed. You must be waiting in a UI related call (for example, `axlEnter*`, a blocking `axlFormDisplay`, `axlUIWBlock`, etc.)

To receive callbacks return to the main program message processing. Another window in blocking mode, however, can delay your return to the main program.

You may add properties to the returned`timerId` to store your own data for access in your timer callback.

Points to be remembered while using the provided callback function.

* Processing in the callback should be relatively short in time

* Do not open or save the design

* Do not open or close forms or windows

* dbids may become stale

* axlAddSimpleRbandDynamics should not be used.

* Too many triggers active can impede performance.

* Allegro dbids are only valid within the callback. You cannot pass dbids in or out of this callback function. You always need to refetch them from the database.

#### Arguments

|  |
| --- | ---
| `o_window` | The window the timer is associated with. If`o_window` is `nil`, the timer is associated with the main window.
| `x_timeout` | Timeout in milliseconds before the timer is triggered and calls your callback procedure. Timeout is not precise because it depends on processing window messages.
| `g_oneshot` | Controls how many times the timer triggers. Use one of these values:  `t` - Timer goes off once and automatically removes itself.  `nil` - Timer goes off at the set time interval continuously until it is removed by `axlUIWTimerRemove`.
| `u_callback` | Procedure called when the timer goes off. Called with these arguments with its return value ignored:  `u_callback(`  `o_window`  `o_timerId`  `n_elapsedTime`  `o_window:`Window you provided to `axlUIWTimerAdd`  `o_timerId:`Timer id which returned by `axlUIWTimerAdd`.  `x_elapsedTime:`Approximate elapsed time in milliseconds since the timer was added.
#### Value Returned

|  |
| --- | ---
| `o_timerId` | The identifier for the timer. Use this to remove the timer. This return value is subject to garbage collection when it goes out of scope. When the garbage is collected, the timer is removed. Do not count on garbage collection to remove the timer, however, because you do not know when garbage collection will start. If you need a timer that lasts forever, assign this to a global variable.
| `nil` | No timer added.
#### See Also

[axlUIWTimerRemove](#380248 "10")

#### Example

* Basic:

```
procedure( YourSkillProcedure(); set up a continuous timer using the main windowtimerId = axlUIWTimerAdd(nil 2000 nil 'YourTimerCallback)timerId->yourData = yourdata)
```

```
procedure( YourTimerCallback( window timerId elapsedTime); your time period has elapsed. do something.)
```

* Other examples can be found at`<cdsroot>``/share/pcb/examples/skill/ui/timer.il`

### axlUIWTimerRemove

`axlUIWTimerRemoveSet(o_timerId`

`)`

`⇒ t/nil`

#### Description

Removes a timer added by`axlUIWTimerAdd`.

#### Arguments

|  |
| --- | ---
| `o_timerId` | Id returned by`axlUIWTimerAdd`.
#### Value Returned

|  |
| --- | ---
| `t` | Timer removed.
| `nil` | Timer id invalid.
### axlUIWUpdate

`axlUIWUpdate(r_window/nil)⇒ t/nil`

#### Description

Forces an update of a window. If you made several changes to a window and are not planning on going back to the main loop or doing a SKILL call that requires user interaction, use this call to update a window. You could use this, for example, if you are doing time-consuming processing without giving back the control to the UI message pump.

To use, make all your window changes and then make this call. If window ID is`nil,` exposes the main window.

#### Arguments

|  |
| --- | ---
| `r_window` | Window id or`nil` if the main window.
#### Value Returned

|  |
| --- | ---
| `t` | Window updated.
| `nil` | Window already closed or invalid window ID.
### axlUIYesNoCancel

`axlUIYesNoCancel(t_message[t_title][s_default])⇒ x_result`

#### Description

Displays a blocking*Yes*`/`*No*`/`*Cancel* dialog box with the prompt message provided.

#### Arguments

|  |
| --- | ---
| `t_message` | Message to display.
| `t_title` | Optional. What to put in the title bar of confirm. The default is the program display name.
| `s_default` | Optional. May be either`yes`, `no` or `cancel` to specify default response. The default is `yes`.
#### Value Returned

|  |
| --- | ---
| `x_result` | Number based on the user's choice:  `0` for *No*  `1` for *Yes*  `2` for *Cancel*
#### Examples

### axlUIDataBrowse

```
axlUIDataBrowse(s_dataTypels_optionst_titleg_sorted[t_helpTag][l_callback][g_args])⇒ lg_return
```

#### Description

Analyzes all objects requested by the caller function, passing each through the caller's callback function. Then puts the objects in a single-selection list.

This list blocks until a user makes a selection. Once the user selects an object, it is passed back to the caller in a list containing two objects: the selected name and, for a database object, the AXL dbid of the object.

#### Arguments

|  |
| --- | ---
| `s_dataType` | One of the following:`'`  `NET`  `'PADSTACK`  `'PACKAGE_SYMBOL`  `'DEVICE`  `'PARTNUMBER`  `'REFDES`  `'BOARD_SYMBOL`  `'FORMAT_SYMBOL`  `'SHAPE_SYMBOL`  `'FLASH_SYMBOL`  `'BRD_TEMPLATE`  `'SYM_TEMPLATE`  `'TECH_FILE`
| `ls_options` | List containing at least one of the following:
|  | `'RETRIEVE_OBJECT:`Object selected returns its dbid  `'RETRIEVE_NAME:`Object selected returns its name  `'EXAMINE_DATABASE:`Initially look in the database for list of objects  `'EXAMINE_LIBRARY:`Initially use env PATH variable when looking for list of objects  `'DATABASE_FIXED:`Read-only check box for the database  `LIBRARY_FIXED:`Read-only check box for files (library)
| `t_title` | Prompt for the title of the dialog
| `g_sorted` | Switch indicating whether or not the list should be sorted
| `t_helpTag` | Help tag for the browser
| `l_callback` | Callback filter function which takes the arguments name, object, and`g_arg` passed in. Returns t or nil based on whether or not the object is eligible for browsing.
| `g_arg` | Generic argument passed through to`l_callback` as the third argument.
#### Value Returned

|  |
| --- | ---
| `t_name o_dbid` | Selection was made and RETRIEVE\_OBJECT used.
| `t_name` `nil` | Selection was made and RETRIEVE\_NAME used.
#### Examples

`axlUIDataBrowse('NET '(RETRIEVE_NAME) "hi" t)`

`axlUIDataBrowse('PADSTACK '(RETRIEVE_NAME) "hi" t)`

```
axlUIDataBrowse('PACKAGE_SYMBOL '(EXAMINE_DATABASE EXAMINE_LIBRARY    RETRIEVE_NAME)"hi" t)
```

`axlUIDataBrowse('PACKAGE_SYMBOL '(EXAMINE_LIBRARY RETRIEVE_OBJECT) "hi" t)`

`axlUIDataBrowse('PACKAGE_SYMBOL '(EXAMINE_LIBRARY RETRIEVE_NAME) "hi" t)`

`axlUIDataBrowse('PARTNUMBER '(RETRIEVE_OBJECT) "Part Number" t)`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
