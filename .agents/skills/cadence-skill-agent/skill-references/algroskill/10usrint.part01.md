<!--
source: algroskill/10usrint.md
part: 1/2
estimated_tokens: 12947
-->

### axlCancelOff

#### Description

See axlCancelOn.

### axlCancelOn

`axlCancelOn( ) => t`

#### Description

Allows Skill code to test for when a user clicks Cancel.

When cancel is enabled, the traffic light is yellow.

Although you can nest cancel calls, you should make an equal number of cancel off calls as cancel on calls.

Note: To avoid problems, always place the cancel on/off call pairs in the same function.

These calls do not work from the Skill or Allegro PCB Editor command line because Allegro PCB Editor immediately disables cancel when exiting the Skill environment to prevent the system from hanging.

Notes:

- Only enable cancel processing when you are sure there is no user interaction. Having cancel enabled when the user has to enter information is not supported and will hang the system.

- Calling `axlCancelTest` can adversely impact your program's performance.

#### Arguments

`None`

#### Value Returns

Only `axlCancelTest` returns meaningful data.

| Name | Description |
|---|---|
| `t` | User click cancel. |
| `nil` | User did not click cancel. |

#### Examples

`count = 0`

`axlCancelOn()`

`while ( count < 50000 && !axlCancelTest()``printf("Count = %d\n" count)``count++`

`)`

`axlCancelOff()`

### axlCancelTest

#### Description

See axlCancelOn.

### axlClipboardGetText

`axlClipboardGetText () => t_text/nil`

#### Description

This gets the current text in the system clipboard. Clipboard can contain data other than ASCII text in which case `nil` is returned.

#### Arguments

No arguments

#### Value Returns

| Name | Description |
|---|---|
| `t_text` | Text in clipboard |
| `nil` | No text in clipboard |

#### See Also

`axlClipboardSetText("hello world") text = axlClipboardGet()` axlClipboardSetText

### axlClipboardSetText

`axlClipboardSetText( t_text/nil ) => t/nil`

#### Description

Sends indicated text to system clipboard. Only ASCII text is supported.

#### Arguments

| Name | Description |
|---|---|
| `t_text` | Text string. If `nil` or an empty string is specified, clipboard is emptied. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Updated clipboard |
| `nil` | Failed |

#### Examples

See example section of axlClipboardGetText

#### See Also

axlClipboardGetText

### axlCursorGet

`axlCursorGet ( g_pixel ) => l_xy`

#### Description

This command is used to obtain the current cursor position either in pixels (screen units) or converted into current design units. The mapping from pixels to design units takes into account the current window view and zoom factor of the design.

Accessing this in non-graphic mode is undefined.

#### Arguments

| Name | Description |
|---|---|
| `g_pixel` | If the value is set to `t,` the xy coordinates are specified in pixels. If the value is set to `nil`, current cursor position as it stands in current design is returned. |

#### Value Returns

The cursor position either in pixels (integer) or design units (floating point).

#### See Also

axlCursorWarp, axlUIControl

### axlCursorWarp

`axlCursorWarp ( g_pixel l_xy ) => t/nil`

#### Description

Use this command to set the cursor position. May set the cursor either by pixel or design units. If setting by design units the new value must be within the current viewable window (axlWindowBoxGet).

Note: See axlCursorGet for a discussion between pixel and design units.

#### Arguments

| Name | Description |
|---|---|
| `g_pixel` | If t return xy in pixels else return cursor position where it stands in current design. |
| `l_xy` | The xy values may be specified in pixel (g_pixel=t) or design units (g_pixel=nil) |

#### Value Returns

| Name | Description |
|---|---|
| `t` | If moved cursor |
| `nil` | If bad arguments or moved cursor outside of main window. |

#### See Also

axlCursorGet, axlWindowBoxGet

### axlMeterCreate

`axlMeterCreate( t_title t_infoString g_enableCancel [t_formname] [t_infoString2] [g_formCallback] ) => t/nil`

#### Description

Starts progress meter with optional cancel feature.

Note: Always call `axlMeterDestroy` when done with meter.

#### Arguments

| Name | Description |
|---|---|
| `t_title` | Title bar of meter. |
| `t_infoString` | One line of 28 characters used for anything you want (can be updated at meter update). |
| `g_enableCancel` | `t` enable the application Stop button on graphical UI-based applications. When enabled and the user picks the Stop button, a true is returned by the call to axlMeterIsCancelled`()`. |
| `t_formname` | (Optional) The name of an alternate form that can be used with these functions which has an info field named progressText and a progress field named bar. axlMeterIsCancelled will also notice if a Cancel menu button has been pressed. If you do not give a form name `axlprogress.form` will be used. |
| `t_infoString2` | (Optional) By Default "". |
| `g_formCallback` | (Optional) The name of a Callback function that you want called for any buttons or fillings etc you may have on your form. This works the same as `g_formAction` in axlFormCreate. |

#### Value Returns

`t` On success; otherwise `nil`.

#### See Also

axlMeterCreate, axlMeterIsCancelled, axlMeterDestroy and axlFormCreate

### axlMeterDestroy

`axlMeterDestroy() => t/nil`

#### Description

`axlMeterCreate("SigNoise Design Audit", "", t) total = <total nets> done = 0 while(<still next net> && (!axlMeterIsCancelled()) < do work > axlMeterUpdate( (100 * ++done)/total sprintf(nil "Check %d of %d nets" done total)) ) axlMeterDestroy()` Closes the progress meter form and shuts off Cancel mode if enabled.

#### Arguments

None

#### Value Returns

`t` If meter was destroyed; otherwise `nil`.

#### See Also

axlMeterCreate

### axlMeterIsCancelled

`axlMeterIsCancelled( ) => t/nil`

#### Description

If cancel was enabled at meter creation, the status of cancel is returned (`t` if cancelled; otherwise `nil`).

If a field named Cancel was hit, it is cancelled

#### Arguments

None

#### Value Returns

`t` If meter was cancelled; otherwise `nil`.

#### See Also

axlMeterCreate

### axlMeterUpdate

`axlMeterUpdate( x_percentDone t_infoString [t_infoStr2] ) => t/nil`

#### Description

Updates progress meter bar and/or info text. The percent done and/or the info string may be updated.

#### Arguments

`x_percentDone` Integer task percent done (0-100)

`t_infoString` Update text for progress meter info text line.	Value is one of: nil - leave info text as it is. "" - clear info string field.

`newText` Update field with new text.

`t_infoStr2` (optional) Text for second line.

#### Value Returns

`t` On success; otherwise `nil`.

#### See Also

axlMeterCreate

### axlUIMenuLoad

`axlUIMenuLoad ( t_menufile ) => t_previousMenuName/nil`

#### Description

Loads the main window menu from the file `t_menuFile`. Adds a default menu file name extension if `t_menuFile` has none. The `MENUPATH` environment variable is used to locate the file if `t_menuFile` does not include the entire path from the root drive.

Note: The intent of this procedure is to allow a custom menu to be loaded for debugging purposes.

#### Arguments

| Name | Description |
|---|---|
| `t_menuFile` | Name of the file to which the menu is dumped. If `t_menuFile` is `nil`, the file name is based on the program's default menu name, which may vary based on the current state of the program. |

#### Value Returns

| Name | Description |
|---|---|
| `t_previousMenuName` | Name of the previous menu. |
| `nil` | Menu not be located. |

#### See Also

axlUIMenuFind

### axlUIMenuDump

`axlUIMenuDump ( t_MenuFile [g_debug] ) => t_previousMenuName/nil`

#### Description

Dumps the current menu of the main window to the `t_menuFile`file. Adds default menu file name extension if `t_menuFile` has none.

Notes:

- There is no user interaction when an existing file is overwritten.

- This function is for the Windows-based GUI only.

#### Arguments

| Name | Description |
|---|---|
| `t_menuFile` | Name of the file to which the menu is dumped. If `t_menuFile` is `nil`, the file name is based on the program's default menu name, which may vary based on the current state of the program. |
| `[g_debug]` | If this is `'print` then, only the commands contained in the menu file are dumped out. Allows for easier comparison between old and new menu files. |

#### Value Returns

| Name | Description |
|---|---|
| `t_previousMenuName` | Full name of the file that is written. |
| `nil` | No file is written. |

Note: The intent of this procedure is to provde a base menu file using which you can develop a customized menu.

### axlUIColorDialog

`axlUIColorDialog( r_window/nil l_rgb ) => l_rgb/nil`

#### Description

Invokes standard color selection dialog box. You must provide a parent window, Allegro PCB Editor defaults to the main window of the application. The `l_rgb` is a red, green, or blue palette list. Each item is an integer between the values of `0` and `255`. `0` indicates color is off, and a value of `255` indicates color is completely on. For example, `255 255 255` indicates white.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Parent window. If `nil`, use main program window. Return handle of `axlFormCreate` is of type`r_window`. |
| `l_rgb` | Seeded red, green, or blue. |

#### Value Returns

| Name | Description |
|---|---|
| `l_rgb` | User selected values. |
| `nil` | User canceled dialog box. |

#### Examples

Get color `1` and change it:

`rgb = axlColorGet(1)`

`rgb = axlUIColorDialog(nil rgb)`

`when(rgb`

`axlColorSet(1 rgb)`

`axlVisibleUpdate(t))`

#### See Also

axlColorSet, axlColorGet

### axlUIConfirm

`axlUIConfirm( t_message [s_level] ) => t`

#### Description

Displays the string `t_message` in a confirmer window.

The user must respond before any further interaction with Allegro PCB Editor. Useful mainly for informing the user about a severe fatal error before exiting your program. Use this blocker function very rarely.

Note: If environment variable `noconfirm` is set, we immediately return.

#### Arguments

| Name | Description |
|---|---|
| `t_message` | Message string. |
| `s_level` | Option level symbol; default is info level, other levels are `warn` and `error`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

Inform user when a significant transition is being made:

`axlUIConfirm( "Returning to Allegro. Please confirm." )`

Alert user to an error:

`axlUIConfirm( "Selected object has FIXED property." 'error )`

#### See Also

axlUIPrompt, axlUIYesNo, axlUIYesNoCancel, axlUIConfirmEx

### axlUIConfirmEx

`axlUIConfirmEx( t_message t_key/nil [s_level] ) => t`

#### Description

Displays the string `t_message` in a confirmer window with an optional check box to never show the box again.

Functions same as axlUIConfirm except allows a check box to never show confirmer again. System remembers this selection so if user has indicated they do not want the box the call immediately returns.

Requires a unique t_key string which is used to remember the selection.

The optional s_level argument changes the info displayed to the user.

On program start/exit writes a file to `<HOME>``/pcbenv/remember_<program>.txt`

#### Arguments

| Name | Description |
|---|---|
| `t_message` | Message string. |
| `t_key` | Unique key to remember user selection. If value of this parameter is nil, the command works like axlUIConfirm. |
| `s_level` | Option level symbol; default is `info` level, other levels are `'warn` and `'error`. |

#### Value Returns

`t`: Always returns `t`

#### Examples

Inform user when a significant transition is being made:

`axlUIConfirmEx( "Use this command at your own risk." "mynewcommand")`

#### See Also

axlUIConfirm

### axlUIControl

`axlUIControl( s_name [g_value] ) => g_currentValue/ls_names`

#### Description

Inquire about graphics canvas. Inquires and sets the value of graphics. If setting a value, the return is the old value of the control.

A side effect of most of these controls is if a form is active that is displaying the current setting it may not be updated. Additional side effects of individual controls are listed. Items will be added over time. Items currently supported:

`Name: screen``Value: (x_width x_height)``Set?: No``Description: Retrieves the screen's width and height in pixels``Equiv: none``Side Effects: none`

`Name: vscreen``Value: (x_width x_height)``Set?: No``Description: Retrieves the screen's virtual width and height in pixels. This will not be the same as 'screen if running Windows XP and enabled monitor spanning option. Also requires multiple monitors and graphic card(s) capable of supporting multiple monitors.``Equiv: none``Side Effects: On UNIX always returns the same size as screen.`

`Name: vedge`

`Value: (x_x x_y)`

`Set?: No`

`Description: Retrieves the virtual left top edge of the screen in pixels`

`Equiv: none`

`Side Effects: On UNIX always returns (0 0)`

`Name: monitors``Value: x_number``Set?: No``Description: Retrieves the number of monitors available.``Equiv: none``Side Effects: On UNIX always returns 1 since we currently do not support multi-monitors on UNIX.`

`Name: pixel2UserUnits``Value: f_number``Set?: No``Description: Returns number user units per pixel taking into account the current canvas size and zoom factor. Changes with the current zoom factor.``Equiv: none``Side Effects: none`

#### Arguments

| Name | Description |
|---|---|
| `s_name` | Symbol name of control. `nil` returns all possible names. |
| `s_value` | Optional symbol value to set. Usually a `t` or a `nil`. |

#### Value Returns

| Name | Description |
|---|---|
| `ls_names` | If name is `nil` then returns a list of all controls. |

See above

#### Examples

Get screen size:

`size = axlUIControl('screen)`

`-> (1280 1024)`

Get pixel to user units:

`axlUIControl('pixel2UserUnits)`

`-> 17.2`

#### See Also

axlOSControl

### axlUIMenuChange

`axlUIMenuChange( x_menuId s_option g_mode ... <pairs of s_option/g_mode> ) => t/nil`

#### Description

This changes one or more parameters of an existing menu item.

Unlike other menu commands this function can be safely done outside of the menu trigger callback if the menu command is associated with your Skill code.

Changes allowed are a variable set of new value pairs:

Table 10-2

| Name | Description |
|---|---|
|  | s_option; g_mode |
| Enable/Disable menu | `'enable`; `t/nil` |
| Set/Unset Check mark | `'check`; `t/nil` |
| Change display text | `'display`; `<new text display>` |
| Change command text | `'command`; `<new command string>` |

You should not attempt to change any separator menu items. Also do not attempt to assign command text to a submenu.

Note: See discussion in axlUIMenuFind about menu changes.

#### Arguments

| Name | Description |
|---|---|
| `x_menuId` | The menuId from axlUIMenuFind |
| `s_option/g_mode pairs` | See Table 10-2 |

#### Value Returns

`t`, if menu item is changed, and `nil` if the command failed to change the menu item.

#### Examples

- Set menu to be disabled

`q = axlUIMenuFind( nil "add rect")`

`axlUIMenuChange(q 'enable nil)`

- Enable and set check mark from previous example

`axlUIMenuChange(q 'enable t 'check t)`

#### See Also

axlUIMenuFind

### axlUIMenuDebug

`axlUIMenuDebug( [g_option] ) => ll_menu/t/nil`

#### Description

A debug function for axl Menu Trigger. This helps debug issues with axlUIMenuRegister.

#### Arguments

| Name | Description |
|---|---|
| `g_option` | data to query/clear
 'clear = clear the list of menus to load
 'list = return list of menus to be loaded (nil no menus)
 'trigger = clear the menu trigger callback and menus loaded |

#### Value Returns

`t`, call succeeded

`nil`, failed or if clear no menus present

`ll_menu`, current list of menus queued

#### See Also

axlUIMenuRegister

### axlUIMenuDelete

`axlUIMenuDelete( x_menuId ) => t/nil`

#### Description

This deletes a single menu item or submenu based upon what is the current find menu item.

Note: See discussion in axlUIMenuFind about menu changes.

#### Arguments

| Name | Description |
|---|---|
| `x_menuId` | the menuId from axlUIMenuFind |

#### Value Returns

`t`, if menu item is deleted else `nil` if failed to delete menu item

#### Examples

- Delete add rect command menu (add rect command is still available from command line)

- Delete entire edit menu (assumes 2 menu item in menu bar)

#### See Also

axlUIMenuFind

### axlUIMenuFind

`axlUIMenuFind( x_menuId/nil t_cmdName/x_location [g_menuOption] ) => x_menuId/nil`

#### Description

`q = axlUIMenuFind( nil "add rect") axlUIMenuDelete(q) q = axlUIMenuFind( nil 1) axlUIMenuDelete(q)` Finds a menu item by location or a command. The location (`x_location`) is 0 based. The 0 location is the left or top most menu item. (Typically, this is the File menu item on the menu bar). A negative number may be used to specify a menu counting from the right side with a -1 indicating the menu furthest to the left or bottom.

Two modes are possible:

| Name | Description |
|---|---|
| 1. | Find by name, finds menu item by command name. |

This method cannot find menu bar items such as File. When finding by name you should pass `nil` as the first argument.

| Name | Description |
|---|---|
| 2. | Find by `x_location`, identifies a menu item off the menu bar (`menuId = nil`) or sub-menu. |

Menu searching is controlled via a menu stack. The first argument, `x_menuId`, controls the stack. For most operations, you should pass a nil to this argument. Typically, searching via the menu stack would use `x_location` as the second argument since the `t_cmdName` method is sufficient to find commands multi-levels deep in the menu hierarchy. If you have a nested search active then passing a nil will reset the stack. The stack is also popped if you provide a `menuId` older then the last id.

The `g_menuOption` when used in location mode returns the top or bottom of the indexed sub-menu (see below).

- Examples shown below provide typical uses.

- CAUTIONS (release to release portability)

- While not frequent, command names may change from release to release.

- Certain products or product tiers may not have a command.

- Menus may be reorganized so expecting to find a command on a particular sub-menu may not return the expected result in a new release.

- As always, adding Allegro commands or scripts to menus may require updates in a new release.

- See introduction of this section on menu recommendations.

#### Arguments

| Name | Description |
|---|---|
| `x_menuId` | menuId return of previous call or nil to search from menu root. |
| `x_location` | Find item by location. Location is 0 based. Therefore, the "File" menu is location 0. Negative numbers may be used where -1 is the right-most (or bottom-most) menu item. |
| `t_cmdName` | Find item by command name. This may not be just a command but is really a command line. For example, if the command is registered as "echo hello" then you must find by "echo hello" and not "echo". |
| `g_menuOption` | Permitted values are `top` or `bottom`. 
 If used with find by command returns the top or bottom of the menu where the command exists.
 Bottom option also indicates to axlUIMenuInsert to that a new menu item should be appended to end of the menu.
 If used with find by location and the item is a submenu returns the top or bottom of that submenu. |

#### Value Returns

If successful returns a menu number else failure is indicated by a `nil`.

#### Examples

- To add to end of "Add" menu either of the following are equivalent (assumes add line exists on 3rd item of menu bar):

- Find Help menu, useful for adding a new sub-menu before the help menu

- Find Top of Help menu, useful for adding new help menu items.

- Find file menu

- Find bottom of File - Import Menu

`l = axlUIMenuFind(nil 3 'bottom) l = axlUIMenuFind(nil "add line" 'bottom) l = axlUIMenuFind(nil -1 nil) l = axlUIMenuFind(nil -1 'top) l = axlUIMenuFind(nil 0 nil) l = axlUIMenuFind(nil "load plot" 'bottom)`

#### See Also

axlUIMenuInsert, axlUIMenuChange, axlUIMenuDelete, axlUIMenuDump, axlUIMenuLoad, axlUIMenuRegister, axlTriggerSet

### axlUIMenuInsert

Command to add menu item

`axlUIMenuInsert( x_menuId t_display t_command ) => t/nil`

Command to add Separator

`axlUIMenuInsert( x_menuId 'separator ) => t/nil`

Command to add Sub-menu

`axlUIMenuInsert( x_menuId 'popup t_display ) => x_subMenuId/nil`

Command to add Sub-menu end (optional)

`axlUIMenuInsert( x_menuId 'end ) => t/nil`

Command to add multiple items

`axlUIMenuInsert( x_menuId ll_items ) => t/nil`

#### Description

Inserts menu items to an existing menu. Several modes are supported:

| Name | Description |
|---|---|
| 1. | Add a new menu item which dispatches a command when selected by user. |

- a.; Add a new visual separator to menu.

| Name | Description |
|---|---|
| 2. | Add a new sub-menu item. Assumption is that it will be populated by additional menu insert calls. |

- a.; End a sub-menu. This is optional, see menu stack discussion below.

| Name | Description |
|---|---|
| 3. | Add multiple menu items. |

This is implemented using a menu stack. axlUIMenuFind resets the stack and each submenu created increments the stack. The 'end mode (submenu) decrements the stack. The menu stack allows the building of a menu tree with very little coding overhead. The stack depth is restricted to 8.

- Menu items should not be created outside a menu trigger. See discussion in axlUIMenuFind. For development purposes you can create menu items outside of the menu trigger.

#### Arguments

| Name | Description |
|---|---|
| `x_menuId` | menu id which can be obtained from axlUIMenuFind or creating a submenu via this API. If nil uses the current menu on the menu stack |
| `t_display` | text that is shown in the menu. Possible values are: `separator` - add a separator (horizontal line) `popup` - create a new submenu |
| `t_command` | command to run
 
 this is ignored for a 'separator
 
 
 this is the display string for '`popup` option 'end
 
 
 pops the menu stack if creating a menu tree |
| `ll_items` | This is a list of `t_display/t_command` value pairs that instruct this interface to add multiple menu items and submenus in a single call. Both the `'separator` and `'end` options do not have to be a list. |

#### Value Returns

`t` - successful

`nil` - failed

`x_menuId` - if creating a new submenu, the nesting id of new submenu

#### Examples

- Add a separator before the add rect command

`q = axlUIMenuFind( nil "add rect")`

`z = axlUIMenuInsert(q 'separator )`

- Add a web link at the top of the help menu

`q = axlUIMenuFind( nil -1 'top)`

`z = axlUIMenuInsert(q "Google" "http http://google.com" )`

- Add a new submenu to the right of the help menu with two commands

`q = axlUIMenuFind( nil -1)`

`; the nil is intention in here since it demostrates`

`; the use of the currrent menu from find.`

`z = axlUIMenuInsert(q 'popup "MyMenu")`

`; the nil is required for the next 2 calls since we want to`

`; insert these these items into MyMenu`

`z = axlUIMenuInsert(z "1" "echo hello 1" )`

`z = axlUIMenuInsert(z "2" "echo hello 2" )`

- More nested menu

See `<cdsroot>``/share/pcb/examples/skill/ui/menu.il`

#### See Also

axlUIMenuFind

### axlUIMenuRegister

`axlUIMenuRegister( t_command/x_location ll_menu [g_menuOption] ) => t/nil`

#### Description

This allows you to register menu items to be loaded when Allegro loads a new menu. It is a combination of axlUIMenuFind and axlUIMenuInsert.

If more elaborate menu configuration is required consider calling axlTriggerSet directly.

- For registering menu items based upon product you need to use this API plus the axlTriggerSet method with one or more of the following APIs.

- To deterimine if the symbol editor is active use axlIsSymbolEditor function.

- axlDesignType may be used to differentiate betwene PCB, APD or SIP.

- Finally, axlVersion with an option:

- `'programName` - another method to differentiate between PCB, APD or SIP

- `'displayName` - differentiates between the products (PCB XL vs PCB Performance). This tends change considerably between releases and may change via ISR.

- other options to this interface further classifiy products in a simple `t`/`nil` return classification.

- See axlUIMenuFind for cautions about portability across releases.

- When multiple menu registers are done, there may be depedencies.For example, if the first menu register adds a new submenu before the File menu the result will be not as expected if the second attempts to add a new item to the Edit menu via the location method.

- This API must never be called from within a axlTriggerSet callback function.

#### Arguments

| Name | Description |
|---|---|
| `t_command` | Command to insert menu before (see axlUIMenuFind) |
| `x_location` | Location before to insert menu (see axlUIMenuFind) |
| `ll_menu` | List of menu items to load (see format 3 option of axlUIMenuInsert) |
| `g_menuOption` | Indication to add to top or bottom of menu (see axlUIMenuFind) |

#### Value Returns

`t`, if register function for indicated callback, `nil`, if the command failed to register trigger

#### Examples

See `<cdsroot>``/share/pcb/examples/skill/ui/menu.il`

#### See Also

axlUIMenuFind, axlUIMenuInsert, axlTriggerSet, axlUIMenuDebug, axlIsSymbolEditor

### axlUIPrompt

`axlUIPrompt( t_message [t_default]/'password ) => t_response/nil`

#### Description

Displays the string `t_message` in a form. The user must type a response into the field. Displays the argument `t_default` in brackets to the left of the field. The user presses the Return key or clicks the OK button in the window to accept the value of `t_default` as the function return value. If the user selects the Cancel button, the function returns `nil`.

This function is a blocker. The user must respond before any further interaction with Allegro PCB Editor.

#### Arguments

| Name | Description |
|---|---|
| `t_message` | Message string displayed. |
| `t_default` | Default value displayed to the user and returned if user presses only the Return key or clicks OK. |
| `'password:` | Obscure and do not script user input. |

#### Value Returns

| Name | Description |
|---|---|
| `t_response` | User response or default value. |
| `nil` | User selected Cancel. |

#### Examples

`axlUIPrompt( "Enter module name" "demo" )`

`⇒``"mymcm"`

Prompts for a module name with a default `demo`. Typing `mymcm` overrides the default.

A text field displays, with the default value "`demo.` To accept the default value, you may either press Return or select OK. Otherwise, type a new value in the text field and press Return or click OK. In this example, enter `"mymcm"` in the text field and click Return.

`axlprompt` returns the following:

`==> "mymcm"`

Password prompt:

`ret = axlUIPrompt( "Enter password" 'password )`

#### See Also

axlUIConfirm

### axlUIWCloseAll

`axlUIWCloseAll( ) => t / nil`

#### Description

This closes all temporary windows (dialogs and text view windows). A temporary window is a dialog that closes if you open another design (e.g. brd). Via Skill this window attribute is set by the axlUIWPerm API. The constraint manager is currently considered a permanent window but this may change in future releases. A blocking window (e.g. File Browser dialogs) cannot be closed via this call.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t` | always |

#### See Also

axlUIWPerm

### axlUIWIconify

`axlUIWIconify ( r_window/t_window t/nil ) => t/nil`

#### Description

This command either creates an icon for a window or open a window from an icon.This is different from axlUIWExpose, which also opens a window from an icon but exposes hidden windows and permits raising a window to the top of the stack. Note all sub-windows also open or closed to an icon. So, if you make the main Allegro PCB Editor window an icon, all of its child windows are also closed.`t_window` name may change from release to release although this is not normal. `nil` may be used for the main window. Currently, Constraint Manager interface is not supported by this skill command.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window ID. |
| `t_window` | Window name. 
 This is the name that appears in PCB Editor scripting -- invoked using the `setwindow` command. |
| `t` | To iconify window, `nil` open from an icon. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | For success |
| `nil` | For failure (The specified window could not be found)' |

#### Examples

Command to iconify Allegro PCB Editor

`axlUIWIconify("pcb")`

#### See Also

axlUIWIsWindow, axlUIWIsIconic, axlUIWExpose

### axlUIWIsIconic

`axlUIWIsIconic( r_window/t_window ) => t/nil`

#### Description

Is the window in an icon state. `nil` may be used for the main window. `t_window` name may change from release to release although this is not normal. Constraint Manager is not yet supported by this skill command.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window ID. |
| `t_window` | Window name. This is the name that appears in Allegro scripting window -- using the `setwindow` command. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | For success |
| `nil` | For failure (when the specified window cannot be found)' |

#### Examples

Check if main window is in icon state

#### See Also

`axlUIWIsIconic("pcb")` axlUIWIsWindow, axlUIWIconify

### axlUIWIsWindow

`axlUIWIsWindow ( t_window ) => t/nil`

#### Description

Returns `t` if named window is open. `t_window` name may change from release to release although this is not normal.

#### Arguments

| Name | Description |
|---|---|
| `t_window` | Window name. This is the name that appears in Allegro PCB Editor -- using the `setwindow` command. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | For success |
| `nil` | No window by that name is open |

#### Examples

Is Constraint Manager open

axlUIWIsWindow("cmgr")

#### See Also

axlUIWClose

### axlUIWMove

`axlUIWMove( r_window/nil t_window l_xy ) => t/nil`

#### Description

Moves a window. New location (`l_xy`) which is upper left corner, is specified in pixels.

`nil` may be used for the main window.

`t_window` name may change from release to release although this is not normal.

Note: Constraint Manager is not yet supported.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window ID or if nil the main window. |
| `t_window` | Window name. This is the name that appears in Allegro scripting from the setwindow command. |
| `l_xy` | (`x_X x_y`) |

#### Value Returns

| Name | Description |
|---|---|
| `t` | window moved |
| `nil` | Error, handle is not a window |

#### Examples

Move main window to upper left corner of the display.

`axlUIWMove(nil 0:0)`

#### See Also

axlUIWSize

### axlUIWRedraw

`axlUIWRedraw( r_window/nil ) => t/nil`

#### Description

Redraws indicated window. If window ID is `nil` redraws the main window.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window ID or if `nil`, the main window. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | For success |
| `nil` | In case of failure (window already closed or not a window) |

### axlUIWSize

`axlUIWSize( r_window/nil ) => ll_rect`

#### Description

Returns outer size of a window. Size is in pixels. x and y coordinates are upper left corner of window.

On UNIX/Linux, the `y` value will typically include an offset due to title bar height.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window id or if `nil` the main window. |

#### Value Returns

| Name | Description |
|---|---|
| `ll_rect` | `( (x_X x_Y) (x_Width x_Height))` |
| `nil` | Error, handle is not a window |

#### See Also

axlUIWMove

### axlIsViewFileType

`axlIsViewFileType( g_userType ) => t/nil`

#### Description

Tests whether `g_userType` is a long message window type.

#### Arguments

| Name | Description |
|---|---|
| `g_userType` | Argument to test. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | `g_userType` is of type `r_windowMsg`. |
| `nil` | `g_userType` is not of type `r_windowMsg`. |

#### Examples

`logWindow =``axlUIViewFileCreate("batch_drc.log" "Batch DRC Log" t)``axlIsViewFileType(logWindow)``⇒ t`

- Creates a window using `axlUIViewFileCreate` (See axlUIViewFileCreate.)

- Tests whether the window is a view file type.

- Returns`t`.

#### See Also

axlUIViewFileCreate

### axlUIViewFileCreate

`axlUIViewFileCreate( t_file t_title g_deleteFile [lx_size] [lt_placement] [g_formToExpose] ) => r_windowMsg/nil`

#### Description

Opens a file view window to display a file (`t_file`), it is an error for file not to exist. Window should be given a title (t_title).

If `g_deleteFile` is set to `t`, the file is deleted when view window is quit or reused. It is suggested that applications not delete view files themselves as the Save and Print buttons will not work.

Size of viewable window is controlled by `lx_size.`Default size is 24x80. Unpredictable results may occur for large row/column values.

Placement of window is handled by `lt_placement` list. If this value is `nil`, the window is centered on editor.

Window may be deleted via program control via axlUIWClose function.

#### Arguments

| Name | Description |
|---|---|
| `t_file` | Name of the ASCII file to display. If the value is "" then last registered log file is displayed. |
| `t_title` | Title to be display in window title bar. |
| `g_deleteFile` | Deletes the file when the user quits the window or another task reuses the window. |
| `lx_size` | Initial size of the window in character rows and columns. The default is 24 by 80. Setting a large window size may cause unpredictable results. |
| `lt_placement` | Window placement hints. 
 See the section on Window Placement. |
| `g_formToExpose` | Optional handle of another window. If specified then this window is brought to the top of the desktop when the view file window is closed. If not specified then the main program window is the parent. |

#### Value Returns

| Name | Description |
|---|---|
| `r_windowMsg` | Window `r_windowMsg`. |
| `nil` | `r_windowMsg` not displayed. |

#### Examples

- Displays the batch DRC log file, saving the window id.

- Deletes the file `drc.log` when the user exits the window.

`logWindow = axlUIViewFileCreate("batch_drc.log" "Batch DRC Log" nil)`

The log file displays in a window. When the user chooses Close, deletes the file `batch_drc.log`.

### axlUIViewFileReuse

`axlUIViewFileReuse( r_windowMsg t_file t_title g_deleteFile [g_formToExpose] ) => t/nil`

#### Description

Reuses the view window to display a file (t_file). Error is thrown if the file does not exist. Window is given a title (t_title).

Expects r_windowMsg to be type of view window. If user quit the window it will re-open it at the old size/position.

File is deleted is g_deleteFile is t when view window is quit or reused. It is suggested that applications not delete view files themselves as the Save and Print buttons will not work.

#### Arguments

| Name | Description |
|---|---|
| `r_windowMsg` | `dbid` of the existing view window created earlier with `axlUIViewFileCreate`. |
| `t_file` | Name of the ASCII file to display. |
| `t_title` | Title to display in window title bar. |
| `g_deleteFile` | Deletes file when the user quits the window or another task reuses the window. |
| `g_formToExpose` | Optional argument that defines the handle of a window to be exposed when the text file window is closed. Default is the parent set by axlUIViewFileCreate. Normally you should not use this argument. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | File displayed. |
| `nil` | File not displayed. |

#### Examples

`(axlUIViewFileReuse logWindow "ncdrill.log" "NC Drill Log" nil)`

- Displays the file`ncdrill.log`, reusing the window `logWindow` created when displaying `batch_drc.log` in the `axlUIViewFileCreate` example.

- Exiting the window automatically deletes the file `ncdrill.log`.

### axlUIYesNo

`axlUIYesNo( t_message [t_title] [s_default] ) => t/nil`

#### Description

Provides a dialog box displaying the message `t_message`. Returns `t` if you choose Yes and `nil` for No.

This function is a blocker. You must respond before any further interaction with Allegro PCB Editor.

Note:

- If environment variable `noconfirm` is set, we immediately return `t`for yes and`nil`for no.

#### Arguments

| Name | Description |
|---|---|
| `t_message` | Message string to display. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | User responded Yes. |
| `nil` | User responded No. |

#### Examples

The following examples are a typical overwrite question.

`axlUIYesNo( "Overwrite module?" )`

`axlUIYesNo( "Overwrite module?" nil 'no )`

`axlUIYesNo( "Overwrite module?" "My Skill Program" )`

`A confirmer window is displayed. If the user selects Yes, the`

`function returns t, otherwise it returns nil.`

`**/`

`list`

`axlUIYesNo(int argc, list *argv)`

`{`

`char *str, *title;`

`int dflt;`

`str = axluGetString(NULL, argv[0]);`

`title = (argc>1) ? axluGetString(NULL, argv[1]) : NULL;`

`dflt = (argc>2) ? DfltResponse(argv[2]) : MN_YES;`

`return(MNYesNoWTitle(str, title, dflt) ? ilcT : ilcNil);`

`}`

`/*`

`#ifdef DOC_C`

#### See Also

axlUIConfirm

### axlUIWExpose

`axlUIWExpose( r_window/nil ) => t/nil`

#### Description

Opens and redisplays a hidden or iconified window, bringing it to the front of all other current windows on the display. If `nil`, the main window is displayed.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window `dbid`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Window opened and brought to front. |
| `nil` | `dbid` was not of a window. |

#### Examples

`logWindow =``axlUIViewFileCreate("batch_drc.log" "Batch DRC Log" t)``; Other interactive code, possibly``; causing Batch DRC Log window to be covered``; Uncover the log window:``axlUIWExpose(logWindow)``⇒ t`

- Displays a window using `axlUIViewFileCreate`.

- Interactively moves window behind one or more other windows using the back selection of your window manager.

- Calls `axlUIWExpose`.

Window comes to the top above all other windows.

### axlUIWClose

`axlUIWClose( r_window/t_window ) => t/nil`

#### Description

Closes a window, if it is open.

Note: Window may also be closed by user. See initial sections of the chapter for specific window types.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window `dbid`. |
| `t_window` | Window name. This is the name that appears in Allegro scripting from the setwindow command. |

`t_window` name may change from release to release although this is not normal.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Window closed. |
| `nil` | Window already closed, or `dbid` is not of a window. |

#### Examples

- The following example, displays a window using axlUIViewFileCreate, and closes it using axlUIWClose.

`logWindow = axlUIViewFileCreate("batch_drc.log" "Batch DRC Log" t)`

;;; Other interactive code

`axlUIWClose(logWindow)`

- Close Constraint Manager

`axlUIWClose("cmgr")`

#### See Also

axlUIWIsWindow

### axlUIWHelpRegister

Command to register new help file

`axlUIWHelpRegister( t_cmd t_helpFile ) => t/nil`

Query if help file registered for command

`axlUIWHelpRegister( t_cmd ) => t_file`

Delete help file registered for command

`axlUIWHelpRegister( t_cmd "" ) => t/nil`

Lists all cmds registered for help

`axlUIWHelpRegister( nil ) => lt_cmds`

#### Description

This registers a help document for a user written skill command or form (dialog). This is typically used in conjunction with axlCmdRegister. You should make this call at the time you do a axlCmdRegister instead of waiting until the skill code associated with the command executes.

You can also add the registrations via the `help_config.txt` file (see `<cdsroot>``/share/pcb/help/help_config.txt`) placed at the site or pcbenv directory.

The document types (determined via file extension) supported on all platforms are:

- `.txt` - a plain text file displayed via Allegro's internal long message window

- `.html` - html browser displayed via a web browser

- `.pdf` - Acrobat file displayed by a Acrobat reader

On Windows other extensions are typically supported which are determined by what programs are installed on the computer (e.g. doc for Word and ppt for PowerPoint).

#### Arguments

| Name | Description |
|---|---|
| `t_cmd` | Command name or form.<formname> for registering help for form buttons |
| `t_helpFile` | Document to display. Variable expansion is supported so you can embed Allegro env variables to make the installed location of the files relative to the variable setting. |

#### Value Returns

`t` for success, `nil` for failure (invalid arguments)

#### Examples

Override add line help with contents of Allegro's env file

`axlCmdRegister("add line" "$TELENV")`

#### See Also

axlCmdRegister

### axlUIWPrint

`axlUIWPrint( r_window/nil t_formatString [g_arg1 ...] ) => t/nil`

#### Description

Prints a message to a window other than the main window. If `r_window` does not have a message line, the message goes to the main window. This function does not buffer messages, but displays them immediately. If the message string does not start with a message class (for example \e), it is treated as a text (\t) message. (See axlMsgPut ) If `nil`, displays the main window.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window `dbid`. |
| `t_formatString` | Context message (`printf`-like) format string. |
| `g_arg1...` | Any number of substitution arguments to be printed using `t_formatString`. Use as you would a C-language `printf` statement. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Message printed to window. |
| `nil` | `dbid` is not of a window. |

#### Examples

`axlUIWPrint(nil "Please enter a value:")`

`Please enter a value:``⇒ t`

Prints a message in the main window.

### axlUIWRedraw

`axlUIWRedraw( r_window/nil ) => t/nil`

#### Description

Redraws the indicated window. If the window `dbid` is `nil`, redraws the main window.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window `dbid` or, if `nil`, the main window. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Window is redrawn. |
| `nil` | `dbid` is not of a window. |

### axlUIWBlock

`axlUIWBlock( r_window ) => t/nil`

#### Description

- This function is not compatible with the g_nonBlock = nil option to axlFormCreate. If using this function with axlFormCreate you must set a callback on the g_formAction.

This places a block on the indicated window until it is destroyed. All other windows are disabled. It may be called recursively, unlike the block option in `axlFormCreate`.

Once you enter a blocking mode you should not bring up a window that is non-blocking. This behavior is not defined and is not supported.

If you block, you should set the block attribute `block` in the Window Placement list `lt_placement` so that the title bar shows it is a blocking window.

If you have a window callback registered you must allow the window to close since the unblock facility unblocks other windows upon close so that the correct window will get the focus after the blocked window is destroyed.

Note: You should set the block symbol option using the lt_placement option in the function that creates the window to visually indicate that the window is in blocking mode.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window `dbid`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Success |
| `nil` | Failure (For example, the window is closed or the `dbid` is not of a window). |

### axlUIEditFile

`axlUIEditFile( t_filename t_title/nil g_block ) => r_window/t/nil`

#### Description

Allows the user to edit a file in an OS independent manner (works under both UNIX and Windows.)

User may override the default editor by setting either the `VISUAL` or `EDITOR` environment variables.

Windows notes

- The default editor is Notepad.

- The title bar setting is not supported.

Unix notes

- The default editor is `vi`.

- An additional environment variable, `WINDOW_EDITOR`, allows the user to specify an X-based editor such as `xedit`. The title bar is not supported in this mode.

Note: In blocking mode, the windows of the main program do not repaint until the file editor window exits.

Only `axlUIWClose` supports the `r_window` handle returned by this function.

#### Arguments

| Name | Description |
|---|---|
| `t_filename` | Name of file to edit. |
| `t_title` | Title bar name, or `nil` for default title bar. |
| `g_block` | Flag specifying blocking mode (`t`) or non-blocking mode (`nil`). |

### axlUIMultipleChoice

`axlUIMultipleChoice( t_question lt_answers [t_title] ) => x_answer/nil`

#### Description

Displays a dialog box containing a question with a set of two or more answers in a list. You must choose one of the answers to continue. Returns the chosen answer.

#### Arguments

| Name | Description |
|---|---|
| `t_question` | Text of the question for display. |
| `lt_answers` | A list of text strings that represent the possible answers. |
| `t_title` | Optional title. If not present, a generic title is provided. |

#### Value Returns

| Name | Description |
|---|---|
| `x_answer` | An integer number indicating the answer chosen. This value is zero-based, that is, a zero represents the first answer, a one the second answer, and so on. |
| `nil` | An error is detected. |

### axlUIViewFileScrollTo

`axlUIViewFileScrollTo( r_windowMsg x_line/nil ) => x_lines/nil`

#### Description

`ret = axlUIMultipleChoice("Pick a choice" '("Pick me" "No Pick me" "I'm here!") "Cmd title")` Scrolls to a specified line in the file viewer. A value of `-1` goes to the end of the viewer.

Note: The number of the line in the view window may not match the number of lines in the file due to line wrapping in the viewer.

- With the html based viewer the command is unable to return the number of items in scroll window. Return is only valid for the legacy text window.

#### Arguments

| Name | Description |
|---|---|
| `r_windowMsg` | Existing view window. |
| `x_line` | Line to scroll: `0` is top of the file, `-1` is bottom of the file, `-2` returns the number of lines in the viewer. |

#### Value Returns

| Name | Description |
|---|---|
| `x_lines` | Number of lines in the view window. |
| `nil` | No view file window. |

#### Examples

`pm = axlUIViewFileCreate("topology.log" "Topology" nil)`

`axlUIViewFileScrollTo(pm -1)`

- Displays the file `topology.log`

- Scrolls to the end of the file

### axlUIWBeep

`axlUIWBeep() => t`

#### Description

Sends an alert to the user, usually a beep.

#### Arguments

`None`

#### Value Returns

`None`

#### Examples

`axlUIWBeep()`

### axlUIWDisableQuit

`axlUIWDisableQuit( o_window ) => t/nil`

#### Description

Disables the system menu Quit option so the user cannot choose it to close the window.

#### Arguments

| Name | Description |
|---|---|
| `o_window` | Window handle. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Window handle is valid. |
| `nil` | Window handle is invalid. |

### axlUIWExposeByName

`axlUIWExposeByName( t_windowName ) => t/nil`

#### Description

Finds a window by name and exposes it (raises it to the top of the window stack and restores it to a window state it if it is an icon).

You can use the `setwindow` command argument to get Allegro PCB Editor window names via scripting. If the window is a form, you get the name by removing the `form.` prefix from its name.

Note: Names of windows may change from release to release.

To raise an item in the control panel, (for example, Options,) use the `axlControlRaise()` function.

#### Arguments

| Name | Description |
|---|---|
| `t_windowName` | Window name. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Window is found. |
| `nil` | Window is not found. |

### axlUIWPerm

`axlUIWPerm( r_window [t/nil] ) => t/nil`

#### Description

Normally forms and other windows close automatically when another database opens. This function allows that default behavior to be overridden.

Notes:

- When you use this function, consider that windows automatically close when a new database opens because the data the windows display may no longer apply to the new database.

- If you do not provide a second argument, returns the current state of the window.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window id. |
| `t`/`nil` | `t` - set permanent `nil` - reset permanent. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Window exists. |
| `nil` | Window does not exist. |

### axlUIWSetHelpTag

`axlUIWSetHelpTag( r_window t_tag ) => t/nil`

#### Description

This has been mostly replaced by axlUIWHelpRegister that works for commands and forms.

Attaches the given help tag to a pre-existing dialog with a port. This function supports subclassing of the help tags, that is, if a help tag is already associated with the dialog, it will not be replaced. This functions adds the new help tag. Adding a new help tag to a pre-existing one is done by concatenating the two with a dot.

For example:

| Name | Description |
|---|---|
| Pre-existing Help Tag: | myOldTag |
| New Help Tag: | myNewTag |
| Resulting Help Tag: | myOldTag.myNewTag |

#### Arguments

| Name | Description |
|---|---|
| `r_window` | Window id. |
| `t_tag` | Subclass of the help string. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Help tag attached. |
| `nil` | Invalid arguments. |

#### See Also

axlUIWHelpRegister

### axlUIWSetParent

`axlUIWSetParent( o_childWindow o_parentWindow/nil ) => t/nil`

#### Description

Sets the parent of a window. When a window is created, its parent is the main window of the application, which is sufficient for most implementations. To run blocking mode on a form launched from another form, set the child form's parent window to be the launched form.

Setting the parent provides these benefits:

- Allows blocking mode to behave correctly.

- If the parent is closed, then the child is also closed.

- If the parent is iconified, then the child is hidden.

- The child stays on top of its parent in the window stacking order.

#### Arguments

| Name | Description |
|---|---|
| `o_childWindow` | Child window handle. |
| `o_parentWindow` | Parent window (if `nil`, then the main window of the application which is normally the default parent.) |

Note: A parent and child cannot be the same window.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Parent is successfully set. |
| `nil` | Could not set the parent due to an illegal window handle. |

### axlUIWShow

`axlUIWShow( r_window/nil s_option ) => t/nil`

#### Description

Shows or hides a window depending on the option passed. If the window id passed is `nil`, the function applies to the main window.

Notes:

- Using the `showna` option on a window may make the window active.

- Using the `show` option on a window that is already visible may not make it active.

#### Arguments

| Name | Description |
|---|---|
| `r_window` | The window id. If `nil,` signifies the main window. |
| `s_option` | One of the following:<br><br>'show:Show and activate the window<br><br>'showna:Show but don't activate the window.<br><br>'hide:Hide the window.<br><br>nil:Show available options. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Window shown or hidden. |
| `nil` | Window id not correct or an invalid option given. |

