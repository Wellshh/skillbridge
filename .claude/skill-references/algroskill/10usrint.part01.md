<!--
source: algroskill/10usrint.md
part: 1/2
estimated_tokens: 13459
-->

### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

10
==

User Interface Functions
========================

This chapter describes the AXL/SKILL functions you use to confirm intent for an action, prompt for text input, display ASCII text files, and flush pending changes in the display buffer.

Window Placement
----------------

Allegro PCB Editor encourages you to place windows in an abstract manner. For example, when you open a form, instead of specifying (*x,y*) coordinates you give a list of placement options. Allegro PCB Editor then calculates the placement location. An advantage of this method is that all windows automatically position themselves relative to the main Allegro PCB Editor window. Windows always position entirely onscreen even in violation of your placement parameters.

The following form placement options (strings with accepted abbreviations in parentheses) are available:

> ```
> north(n)    northeast(ne)    east(e)    southeast(se)south(s)    southwest(sw)    west(w)    northwest(nw)center(c)
> ```

In addition you can modify the placement options with the following parameters:

|  |
| --- | ---
| `Inner` or `Outer` | Places the placement rectangle to the outside or the inside of the main window. The default is`inner`.
| `Canvas` or `Window` | Uses the canvas (drawing) area or the entire window for the placement rectangle.The default is`Window`.
| `Border` or `NoBorder` (Default `Border`) | Leaves a slight border around the placed window. If`noborder` is set, the window is set directly against the placement rectangle. The default is `Border`.
| `MsgLines` (Default 1) | Sets the number of message lines at bottom of the placed window to 0 or 1.  **Note:** Only`forms` supports this parameter.  **Syntax:**  `msglines #`
Using Menu Files
----------------

You can use drawing menus, symbol menus, and shape menus in Allegro PCB Editor. Allegro tools typically support three menus; drawing, symbol and shape. The Allegro command set is very different between these three design editors. Also menu sets exist for different tools such as APD, SIP and the SI (Signal Integrity) products.

All of the tiering (product levels) within a product are managed via the "#ifdef" statements within a single menu file. Typically, the settings of environment variables controlling the tiering are documented at the top of file.

**Note:** You cannot strip out the`#ifdef` statements to gain access to the missing commands.

Allegro finds the menus with its MENUPATH environment variable. You can find the default Allegro PCB Editor menu files in:

> `<cdsroot>/share/pcb/text/cuimenus`

* ***As new products are added in a release, new menu files may be added. Cadence may change the name of any menu file in a release.***

The menus in this directory are as follows (due to the tools and software version you have loaded, some may not be present in your installation). You should not modify any other file type in this directory as only the menu files are supported for user modification.

****Table 10-1****
**Allegro PCB Editor Menu Files**

| **File Name** | **Description**
| `allegro.men` | Allegro PCB Editor menu for all Allegro PCB Editor`.brd` designs
| `pcb_symbol.men` | Symbol menu for PCB products
| `partition.men` | Partition menu for PCB products
| specctraquest.men | PCB SI menu
| `apd.men` | APD menu
| `sip.men` | SiP menu
| `icp_symbol.men` | APD/SIP symbol editor menu
| apd\_partition.men | APD Partition editor menu
| sip\_partition.men | SIP Partition editor menu
| apd\_si.men | APD SI menu
| `padlayout.men` | Pad Designer in the board graphics editor
| `padlaystn.men` | Pad Designer (standalone)
| `allegro_free_viewer.men` | Allegro/SIP Free Viewer
| `viewlayout.men` | Allegro Viewer Plus
#### Menu Terms

* Menu bar - the menu items seen at the top of a Window

* Menu item - a menu line; may either be a command, separator or a submenu.

* Separator - a horizontal line drawn to visually group menu items.

* Submenu - a pulldown (from the menu bar) or a pull-right (from another submenu). Submenus may only have a display and command association is not supported.

#### Menu Design Considerations

* Certain dynamic items may exist. These are currently the MRU (most recently used files) and Quick reports.

> Do not attempt to modify these items.

* Do not use spaces in the display for the menu bar.

* All menu bar items should be submenus. Do not add a command menu item at this level.

* Do not add excessive items to the menu bar. If the menu bar displays on two lines for a typical window width you may have too many items.

* Keep the display text relatively short, especially on the menu bar.

MENU CUSTOMIZATION METHODS

* Provide your own customization menu via CDS\_SITE. Replace the Cadence provided menu (.men file) with your own.

* Advantages: Relatively easy and no Skill programming required.

* Disadvantages: For new releases need to merge your menu changes with new Cadence menus. May need to modify multiple menus

* Overload your menu customizations on Cadence menus via Skill[axlUIMenuRegister](#383589 "10").

* Advantages: Relatively easy with minimal Skill programming. Depending on your site's additions may be immune to many Cadence menu changes.

* Disadvantages: Cannot delete Cadence menu items or restrict your changes to a one Cadence menu.

* Register a axl menu Trigger notification via[axlTriggerSet](14dsnctl.html#706908 "14").

* Advantages: Almost as much flexibility as overriding the default menu file including targeting specific menus.

* Disadvantages: Need to examine your Skill code with new Cadence releases. Requires much more Skill programming knowledge.

Dynamically Loading Menus
-------------------------

All tools support overriding their default menus by putting your menu file before the default Cadence menu file via the`MENUPATH`. Programs that support AXL-Skill allow menus to be dynamically changed while the program is running. You do this using the `axlUIMenuLoad` Skill function. This is not supported in `allegro_pcb` and *allegro\_viewer*.

Tools support dynamically (via Skill) modifying menus. For information, see[axlUIMenuFind](#390729 "10").

Understanding the Menu File Format
----------------------------------

You can have only one menu definition per file. The following shows the menu syntax in BNF format. The use of indentation reflects hierarchy in the`.men` file.

Menu file grammar reflects the following conventions:

|  |
| --- | ---
| **Convention** | **Description**
| `[ ]` | Optional
| `{ }` | May repeat one or more times.
| `< >` | Supplied by the user
| `|` | Choose one or the other
| `:` | Definition of a token
| `CAPS` | Items in caps are keywords
The following defines the menu file format:

`FILE:`

`[comment]`

`[ifdef]`

`<name>MENU DISCARDABLE`

`BEGIN`

`{popup}`

`END`

`popup:`

`POPUP "<display>"`

`BEGIN`

`{MENUITEM "<display>"    "<command>}`

`[{separator}]`

`{[popup]}`

`END`

`{[//]}    - comment lines`

`separator:`

`MENUITEM SEPARATOR`

```
- this inserts a separator line at this spot in the menu. This is not supported at the top level menubar.
```

`name:    This text is ignored. Use the file name without the extension.`

`comment:    Double slash (//) can be used to start a comment.`

`display:    Text shown to the user.`

```
& -This is used to enable keyboard access to the menus. For this to work, each menu level must have a unique key assigned to it. Use double ampersand (&&) to display a "&".
```

`... -The three dots convention signifies that this command displays a form.`

```
command:    This is any Allegro command, sequence of Allegro commands, or Skill statement.The Allegro command parser acts on this statement so it offers considerable flexibility. The command should be placed within a set of double quotes ("). Double quotes are not supported within this command string.
```

```
ifdef:    Use #ifdef/#endif and #ifndef/#endif to make items conditionally appear in the menu, depending on whether or not a specified environment variable is set.
```

```
An #ifdef causes the menu item(s) to be ignored unless the environment variable is set. A #ifndef causes the menu item(s) to be ignored if the environment variable is not set. You must have one #endif for each #ifdef or #ifndef to end the block of conditional menu items. Also, #ifdef, #ifndef, and #endif must start at the first column of the line in the menu file.
```

`The #ifndef is the negation of #ifdef.`

```
>              environment variable is set.  A #ifdef will cause the menu item(s)
```

`> to be ignored if the environment variable is not set. You must`

`> have one #endif for each #ifdef or #ifndef to end the block of`

```
>              conditional menu items.  Also,  the #ifdef, #ifndef and #endif must
```

`> start at the first column of its line in the menufile.`

`< The condition syntax supports multiple variables with OR '||' or`

`< AND '&&' conditions. Also the negation character '!' is supported`

`< for the variables:`

These statements may be nested. The simple syntax for`#ifdef` follows:

`#ifdef <env variable name>`

`[menu items which appear if the env variable is set]`

`#endif`

`#ifndef <env variable name>`

`[menu items which appear if the env variable is not set]`

`#endif`

```
<                  # logically equivalent to above state using negation character
```

`< #ifdef !<env variable name>`

`< [menu items which appear if the env variable is NOT set]`

`< #endif`

`<`

`< Also logical statements`

```
<               1) if variable1 and variable2 are both set do the included statement
```

`< #ifdef <var1> && <var2>`

`< [menu items which appear if both variables are set]`

`< #endif`

`<`

`< 2) if either variable1 or variable2 is do the included statement`

`< #ifdef <var1> || <var2>`

`< [menu items which appear if either variable is set]`

`< #endif`

The items between the`#if[n]def/#endif`can be one or more `MENUITEMS` or could be a `POPUP`.

#### Example 1

`#ifdef menu_enable_export`

`POPUP "&Export"`

`BEGIN`

`MENUITEM "&Logic...", "feedback"`

`END`

`#endif`

The*Export* popup appears in the menu only if the `menu_enable_export` environment variable is set.

#### Example 2

`#ifndef menu_disable_product_notes`

`MENUITEM "&Product Notes", "help -file algpn"`

`#endif`

The*Product Notes* menu item appears in the menu only if the `menu_disable_product_notes` environment variable is NOT set.

#### Example 3 - Simple Menu Example

`DISPLAY (indents reflect the various pulldown levels)`

`File    Help`

`Open        Contents`

`Export        Product Notes`

`Logic        Known Problems and Solutions`

`Exit        ----------------------------`

`About Allegro...`

`FILE:`

`simple MENU DISCARDABLE`

`BEGIN`

`POPUP "&File"`

`BEGIN`

`MENUITEM "&Open",    "open"`

`POPUP "&Export"`

`BEGIN`

`MENUITEM "&Logic...",    "feedback"`

`END`

`MENUITEM "&Exit",    "exit"`

`END`

`POPUP "&Help"`

`BEGIN`

`MENUITEM "&Contents",    "help"`

`MENUITEM "&Product Notes",    "help -file algpn"`

`MENUITEM "&Known Problems and Solutions",    "help -file alkpns"`

`MENUITEM SEPARATOR`

`MENUITEM "&About Allegro...",    "about"`

`END`

`END`

A simple menu and the simple file required to display the menu.

AXL-SKILL User Interface Functions
----------------------------------

This section lists the user interface functions.

### axlCancelOff

See`axlCancelOn`.

### axlCancelOn

`axlCancelOn()⇒ t`

`axlCancelOff()⇒ t`

`axlCancelTest()⇒ t/nil`

#### Description

Allows Skill code to test for when a user clicks*Cancel*.

When cancel is enabled, the traffic light is yellow.

Although you can nest cancel calls, you should make an equal number of cancel off calls as cancel on calls.

**Note:** To avoid problems, always place the cancel on/off call pairs in the same function.

These calls do not work from the Skill or Allegro PCB Editor command line because Allegro PCB Editor immediately disables cancel when exiting the Skill environment to prevent the system from hanging.

**Notes:**

* Only enable cancel processing when you are sure there is no user interaction. Having cancel enabled when the user has to enter information is not supported and will hang the system.

* Calling`axlCancelTest` can adversely impact your program's performance.

#### Arguments

`None`

#### Value Returned

Only`axlCancelTest` returns meaningful data.

|  |
| --- | ---
| `t` | User click cancel.
| `nil` | User did not click cancel.
#### Examples

> `count = 0`

> `axlCancelOn()`

> ```
> while ( count < 50000 && !axlCancelTest()    printf("Count = %d\n" count)    count++
> ```

> `)`

> `axlCancelOff()`

### axlCancelTest

See[axlCancelOn](#381672 "10").

### axlClipboardGetText

`axlClipboardGetText ()=> t_text/nil`

#### Description

This gets the current text in the system clipboard. Clipboard can contain data other than ASCII text in which case`nil` is returned.

#### Arguments

No arguments

#### Value Returns

|  |
| --- | ---
| `t_text` | Text in clipboard
| `nil` | No text in clipboard
#### Examples

`axlClipboardSetText("hello world")`

`text = axlClipboardGet()`

#### See Also

[axlClipboardSetText](#417404 "10")

### axlClipboardSetText

`axlClipboardSetText(t_text/nil)=> t/nil`

#### Description

Sends indicated text to system clipboard. Only ASCII text is supported.

#### Arguments

|  |
| --- | ---
| `t_text` | Text string. If`nil` or an empty string is specified, clipboard is emptied.
#### Value Returns

|  |
| --- | ---
| `t` | Updated clipboard
| `nil` | Failed
#### Examples

See example section of[axlClipboardGetText](#417343 "10")

#### See Also

[axlClipboardGetText](#417343 "10")

### axlCursorGet

`axlCursorGet (g_pixel) ==> l_xy`

**Description**

This command is used to obtain the current cursor position either in pixels (screen units) or converted into current design units. The mapping from pixels to design units takes into account the current window view and zoom factor of the design.

Accessing this in non-graphic mode is undefined.

#### Arguments

|  |
| --- | ---
| `g_pixel` | If the value is set to`t,` the xy coordinates are specified in pixels. If the value is set to `nil`, current cursor position as it stands in current design is returned.
#### Value Returned

The cursor position either in pixels (integer) or design units (floating point).

#### See Also

[axlCursorWarp](#405062 "10"), [axlUIControl](#410372 "10")

### axlCursorWarp

`axlCursorWarp (g_pixell_xy) ==> t/nil`

#### Description

Use this command to set the cursor position. May set the cursor either by pixel or design units. If setting by design units the new value must be within the current viewable window ([axlWindowBoxGet](06intedt.html#810387 "5")).

**Note:** See[axlCursorGet](#405060 "10") for a discussion between pixel and design units.

#### Arguments

|  |
| --- | ---
| `g_pixel` | If t return xy in pixels else return cursor position where it stands in current design.
| `l_xy` | The xy values may be specified in pixel (g\_pixel=t) or design units (g\_pixel=nil)
#### Value Returned

|  |
| --- | ---
| `t` | If moved cursor
| `nil` | If bad arguments or moved cursor outside of main window.
#### See Also

[axlCursorGet](#405060 "10"), [axlWindowBoxGet](06intedt.html#810387 "5")

### axlMeterCreate

```
axlMeterCreate(    t_title     t_infoString     g_enableCancel     [t_formname]    [t_infoString2]    [g_formCallback]-> t/nil
```

#### Description

Starts progress meter with optional cancel feature.

**Note:** Always call`axlMeterDestroy` when done with meter.

#### Arguments

|  |
| --- | ---
| `t_title` | Title bar of meter.
| `t_infoString` | One line of 28 characters used for anything you want (can be updated at meter update).
| `g_enableCancel` | `t` enable the application *Stop* button on graphical UI-based applications. When enabled and the user picks the *Stop* button, a true is returned by the call to [axlMeterIsCancelled](#382852 "10")`()`.
| `t_formname` | (Optional) The name of an alternate form that can be used with these functions which has an info field named*progressText* and a progress field named *bar*. [axlMeterIsCancelled](#382852 "10") will also notice if a *Cancel* menu button has been pressed. If you do not give a form name `axlprogress.form` will be used.
| `t_infoString2` | (Optional) By Default "".
| `g_formCallback` | (Optional) The name of a Callback function that you want called for any buttons or fillings etc you may have on your form. This works the same as`g_formAction` in [axlFormCreate](11frmint.html#414342 "11").
#### Value Returned

`t` On success; otherwise `nil`.

#### See Also

[axlMeterCreate](#381730 "10"), [axlMeterIsCancelled](#382852 "10"), [axlMeterDestroy](#382496 "10") and [axlFormCreate](11frmint.html#414342 "11")

#### Example

`axlMeterCreate("SigNoise Design Audit", "", t)`

`total = <total nets>`

`done = 0`

`while(<still next net> && (!axlMeterIsCancelled())`

`< do work >`

`axlMeterUpdate( (100 * ++done)/total`

`sprintf(nil "Check %d of %d nets" done total))`

`)`

`axlMeterDestroy()`

### axlMeterDestroy

`axlMeterDestroy() -> t/nil`

#### Description

Closes the progress meter form and shuts off Cancel mode if enabled.

#### Arguments

None

#### Value Returned

`t` If meter was destroyed; otherwise `nil`.

#### See Also

[axlMeterCreate](#381730 "10")

### axlMeterIsCancelled

`axlMeterIsCancelled() -> t/nil`

#### Description

If cancel was enabled at meter creation, the status of cancel is returned (`t` if cancelled; otherwise `nil`).

If a field named*Cancel* was hit, it is cancelled

#### Arguments

None

#### Value Returned

`t` If meter was cancelled; otherwise `nil`.

#### See Also

[axlMeterCreate](#381730 "10")

### axlMeterUpdate

`axlMeterUpdate(x_percentDonet_infoString[t_infoStr2]) -> t/nil`

#### Description

Updates progress meter bar and/or info text. The percent done and/or the info string may be updated.

#### Arguments

`x_percentDone` Integer task percent done (0-100)

`t_infoString` Update text for progress meter info text line.
 Value is one of:
 nil - leave info text as it is.
 "" - clear info string field.

`newText` Update field with new text.

`t_infoStr2` (optional) Text for second line.

#### Value Returned

`t` On success; otherwise `nil`.

#### See Also

[axlMeterCreate](#381730 "10")

### axlUIMenuLoad

`axlUIMenuLoad (t_menufile`

)⇒ `t_previousMenuName`/nil

#### Description

Loads the main window menu from the file`t_menuFile`. Adds a default menu file name extension if `t_menuFile` has none. The `MENUPATH` environment variable is used to locate the file if `t_menuFile` does not include the entire path from the root drive.

**Note:** The intent of this procedure is to allow a custom menu to be loaded for debugging purposes.

#### Arguments

|  |
| --- | ---
| `t_menuFile` | Name of the file to which the menu is dumped. If`t_menuFile` is `nil`, the file name is based on the program's default menu name, which may vary based on the current state of the program.
#### Value Returned

|  |
| --- | ---
| `t_previousMenuName` | Name of the previous menu.
| `nil` | Menu not be located.
#### See Also

[axlUIMenuFind](#390729 "10")

### axlUIMenuDump

`axlUIMenuDump (t_MenuFile[g_debug]) ⇒ t_previousMenuName/nil`

#### Description

Dumps the current menu of the main window to the`t_menuFile`file. Adds default menu file name extension if `t_menuFile` has none.

**Notes:**

* There is no user interaction when an existing file is overwritten.

* This function is for the Windows-based GUI only.

#### Arguments

|  |
| --- | ---
| `t_menuFile` | Name of the file to which the menu is dumped. If`t_menuFile` is `nil`, the file name is based on the program's default menu name, which may vary based on the current state of the program.
| `[g_debug]` | If this is`'print` then, only the commands contained in the menu file are dumped out. Allows for easier comparison between old and new menu files.
#### Value Returned

|  |
| --- | ---
| `t_previousMenuName` | Full name of the file that is written.
| `nil` | No file is written.
**Note:** The intent of this procedure is to provde a base menu file using which you can develop a customized menu.

### axlUIColorDialog

`axlUIColorDialog(r_window/nill_rgb) -> l_rgb/nil`

#### Description

Invokes standard color selection dialog box. You must provide a parent window, Allegro PCB Editor defaults to the main window of the application. The`l_rgb` is a red, green, or blue palette list. Each item is an integer between the values of `0` and `255`. `0` indicates color is off, and a value of `255` indicates color is completely on. For example, `255 255 255` indicates white.

#### Arguments

|  |
| --- | ---
| `r_window` | Parent window. If`nil`, use main program window. Return handle of `axlFormCreate` is of type`r_window`.
| `l_rgb` | Seeded red, green, or blue.
#### Value Returned

|  |
| --- | ---
| `l_rgb` | User selected values.
| `nil` | User canceled dialog box.
#### See Also

[axlColorSet](04parmgt.html#1095354 "3"), [axlColorGet](04parmgt.html#1093245 "3")

#### Examples

Get color`1` and change it:

> `rgb = axlColorGet(1)`

> `rgb = axlUIColorDialog(nil rgb)`

> `when(rgb`

> `axlColorSet(1 rgb)`

> `axlVisibleUpdate(t))`

### axlUIConfirm

`axlUIConfirm(t_message[s_level])==> t`

#### Description

Displays the string`t_message` in a confirmer window.

The user must respond before any further interaction with Allegro PCB Editor. Useful mainly for informing the user about a severe fatal error before exiting your program. Use this blocker function very rarely.

**Note:** If environment variable`noconfirm` is set, we immediately return.

#### Arguments

|  |
| --- | ---
| `t_message` | Message string.
| `s_level` | Option level symbol; default is info level, other levels are`warn` and `error`.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

> Inform user when a significant transition is being made:

> `axlUIConfirm( "Returning to Allegro. Please confirm." )`

> Alert user to an error:

> `axlUIConfirm( "Selected object has FIXED property." 'error )`

#### See also

[axlUIPrompt](#386611 "10"), [axlUIYesNo](#101837 "10"), [axlUIYesNoCancel](#380347 "10"), [axlUIConfirmEx](#383585 "10")

### axlUIConfirmEx

`axlUIConfirmEx(t_messaget_key/nil[s_level])==> t`

#### Description

Displays the string`t_message` in a confirmer window with an optional check box to never show the box again.

Functions same as axlUIConfirm except allows a check box to never show confirmer again. System remembers this selection so if user has indicated they do not want the box the call immediately returns.

Requires a unique t\_key string which is used to remember the selection.

The optional s\_level argument changes the info displayed to the user.

On program start/exit writes a file to`<HOME>``/pcbenv/remember_<program>.txt`

#### Arguments

|  |
| --- | ---
| `t_message` | Message string.
| `t_key` | Unique key to remember user selection. If value of this parameter is nil, the command works like[axlUIConfirm](#101764 "10").
| `s_level` | Option level symbol; default is`info` level, other levels are `'warn` and `'error`.
#### Value Returned

`t`: Always returns `t`

#### See Also

[axlUIConfirm](#101764 "10")

#### Examples

Inform user when a significant transition is being made:

> `axlUIConfirmEx( "Use this command at your own risk." "mynewcommand")`

### axlUIControl

`axlUIControl(s_name[g_value])==> g_currentValue/ls_names`

#### Description

Inquire about graphics canvas. Inquires and sets the value of graphics. If setting a value, the return is the old value of the control.

A side effect of most of these controls is if a form is active that is displaying the current setting it may not be updated. Additional side effects of individual controls are listed. Items will be added over time. Items currently supported:

```
Name:   screenValue:  (x_width x_height)Set?:   NoDescription: Retrieves the screen's width and height in pixelsEquiv:  noneSide Effects: none
```

```
Name:   vscreenValue:  (x_width x_height)Set?:   NoDescription: Retrieves the screen's virtual width and height in pixels. This will not be the same as 'screen if running Windows XP and enabled monitor spanning option. Also requires multiple monitors and graphic card(s) capable of supporting multiple monitors.Equiv:  noneSide Effects: On UNIX always returns the same size as screen.
```

`Name: vedge`

`Value: (x_x x_y)`

`Set?: No`

`Description: Retrieves the virtual left top edge of the screen in pixels`

`Equiv: none`

`Side Effects: On UNIX always returns (0 0)`

```
Name:   monitorsValue:  x_numberSet?:   NoDescription: Retrieves the number of monitors available.Equiv:  noneSide Effects: On UNIX always returns 1 since we currently do not support multi-monitors on UNIX.
```

```
Name:   pixel2UserUnitsValue:  f_numberSet?:   NoDescription: Returns number user units per pixel taking into account the current canvas size and zoom factor. Changes with the current zoom factor.Equiv:  noneSide Effects: none
```

#### Arguments

|  |
| --- | ---
| `s_name` | Symbol name of control.`nil` returns all possible names.
| `s_value` | Optional symbol value to set. Usually a`t` or a `nil`.
#### Value Returned

|  |
| --- | ---
| `ls_names` | If name is`nil` then returns a list of all controls.
See above

#### See Also

[axlOSControl](23utils.html#929974 "24")

#### Examples:

Get screen size:

> `size = axlUIControl('screen)`

> `-> (1280 1024)`

Get pixel to user units:

> `axlUIControl('pixel2UserUnits)`

> `-> 17.2`

### axlUIMenuChange

`axlUIMenuChange(x_menuIds_optiong_mode... <pairs of s_option/g_mode>) -> t/nil`

#### Description

This changes one or more parameters of an existing menu item.

Unlike other menu commands this function can be safely done outside of the menu trigger callback if the menu command is associated with your Skill code.

Changes allowed are a variable set of new value pairs:

****Table 10-2****

|  | **s\_option** | **g\_mode**
| Enable/Disable menu | `'enable` | `t/nil`
| Set/Unset Check mark | `'check` | `t/nil`
| Change display text | `'display` | `<new text display>`
| Change command text | `'command` | `<new command string>`
You should not attempt to change any separator menu items. Also do not attempt to assign command text to a submenu.

**Note:** See discussion in[axlUIMenuFind](#390729 "10") about menu changes.

#### Arguments

|  |
| --- | ---
| `x_menuId` | The menuId from[axlUIMenuFind](#390729 "10")
| `s_option/g_mode pairs` | See[Table 10-2](#395991 "10")
#### Value Returned

`t`, if menu item is changed, and `nil` if the command failed to change the menu item.

#### See Also

[axlUIMenuFind](#390729 "10")

#### Examples

* Set menu to be disabled

> `q = axlUIMenuFind( nil "add rect")`

> `axlUIMenuChange(q 'enable nil)`

* Enable and set check mark from previous example

> `axlUIMenuChange(q 'enable t 'check t)`

### axlUIMenuDebug

`axlUIMenuDebug([g_option]) => ll_menu/t/nil`

#### Description

A debug function for axl Menu Trigger. This helps debug issues with[axlUIMenuRegister](#383589 "10").

#### Arguments

|  |
| --- | ---
| `g_option` | data to query/clear  'clear = clear the list of menus to load  'list = return list of menus to be loaded (nil no menus)  'trigger = clear the menu trigger callback and menus loaded
#### Value Returned

`t`, call succeeded

`nil`, failed or if clear no menus present

`ll_menu`, current list of menus queued

#### See Also

[axlUIMenuRegister](#383589 "10")

### axlUIMenuDelete

`axlUIMenuDelete(x_menuId) t/nil`

#### Description

This deletes a single menu item or submenu based upon what is the current find menu item.

**Note:** See discussion in[axlUIMenuFind](#390729 "10") about menu changes.

#### Arguments

|  |
| --- | ---
| `x_menuId` | the menuId from[axlUIMenuFind](#390729 "10")
#### Value Returned

`t`, if menu item is deleted else `nil` if failed to delete menu item

#### See Also

[axlUIMenuFind](#390729 "10")

#### Example

* Delete add rect command menu (add rect command is still available from command line)

`q = axlUIMenuFind( nil "add rect")`

`axlUIMenuDelete(q)`

* Delete entire edit menu (assumes 2 menu item in menu bar)

`q = axlUIMenuFind( nil 1)`

`axlUIMenuDelete(q)`

### axlUIMenuFind

`axlUIMenuFind(x_menuId/nilt_cmdName/x_location[g_menuOption]) ==> x_menuId/nil`

#### Description

Finds a menu item by location or a command. The location (`x_location`) is 0 based. The 0 location is the left or top most menu item. (Typically, this is the *File* menu item on the menu bar). A negative number may be used to specify a menu counting from the right side with a -1 indicating the menu furthest to the left or bottom.

Two modes are possible:

* Find by name, finds menu item by command name.

> This method cannot find menu bar items such as*File*. When finding by name you should pass `nil` as the first argument.

* Find by`x_location`, identifies a menu item off the menu bar (`menuId = nil`) or sub-menu.

> Menu searching is controlled via a menu stack. The first argument,`x_menuId`, controls the stack. For most operations, you should pass a nil to this argument. Typically, searching via the menu stack would use `x_location` as the second argument since the `t_cmdName` method is sufficient to find commands multi-levels deep in the menu hierarchy. If you have a nested search active then passing a nil will reset the stack. The stack is also popped if you provide a `menuId` older then the last id.

> The`g_menuOption` when used in location mode returns the top or bottom of the indexed sub-menu (see below).

* Examples shown below provide typical uses.

* ***CAUTIONS (release to release portability)***

|  |  |
| --- | --- | ---
|  |  | While not frequent, command names may change from release to release.
|  |  |
| --- | --- | ---
|  |  | Certain products or product tiers may not have a command.
|  |  |
| --- | --- | ---
|  |  | Menus may be reorganized so expecting to find a command on a particular sub-menu may not return the expected result in a new release.
|  |  |
| --- | --- | ---
|  |  | As always, adding Allegro commands or scripts to menus may require updates in a new release.
|  |  |
| --- | --- | ---
|  |  | See introduction of this section on menu recommendations.
#### Arguments

|  |
| --- | ---
| `x_menuId` | menuId return of previous call or nil to search from menu root.
| `x_location` | Find item by location. Location is 0 based. Therefore, the "File" menu is location 0. Negative numbers may be used where -1 is the right-most (or bottom-most) menu item.
| `t_cmdName` | Find item by command name. This may not be just a command but is really a command line. For example, if the command is registered as "*echo hello*" then you must find by "*echo hello*" and not "echo".
| `g_menuOption` | Permitted values are`top` or `bottom`.  If used with find by command returns the top or bottom of the menu where the command exists.  Bottom option also indicates to[axlUIMenuInsert](#392601 "10") to that a new menu item should be appended to end of the menu.  If used with find by location and the item is a submenu returns the top or bottom of that submenu.
#### Value Returned

If successful returns a menu number else failure is indicated by a`nil`.

#### See Also

[axlUIMenuInsert](#392601 "10"), [axlUIMenuChange](#390726 "10"), [axlUIMenuDelete](#390814 "10"), [axlUIMenuDump](#379567 "10"), [axlUIMenuLoad](#379533 "10"), [axlUIMenuRegister](#383589 "10"), [axlTriggerSet](14dsnctl.html#706908 "14")

#### Example

* To add to end of "Add" menu either of the following are equivalent (assumes add line exists on 3rd item of menu bar):

`l = axlUIMenuFind(nil 3 'bottom)`

`l = axlUIMenuFind(nil "add line" 'bottom)`

* Find Help menu, useful for adding a new sub-menu before the help menu

`l = axlUIMenuFind(nil -1 nil)`

* Find Top of Help menu, useful for adding new help menu items.

`l = axlUIMenuFind(nil -1 'top)`

* Find file menu

`l = axlUIMenuFind(nil 0 nil)`

* Find bottom of File - Import Menu

`l = axlUIMenuFind(nil "load plot" 'bottom)`

### axlUIMenuInsert

* Command to add menu item

`axlUIMenuInsert(x_menuIdt_displayt_command) -> t/nil`

* Command to add Separator

`axlUIMenuInsert(x_menuId'separator) -> t/nil`

* Command to add Sub-menu

`axlUIMenuInsert(x_menuId'popupt_display) -> x_subMenuId/nil`

* Command to add Sub-menu end (optional)

`axlUIMenuInsert(x_menuId'end) -> t/nil`

* Command to add multiple items

`axlUIMenuInsert(x_menuIdll_items) -> t/nil`

#### Description

Inserts menu items to an existing menu. Several modes are supported:

* Add a new menu item which dispatches a command when selected by user.

|
| ---
|
 **a.** | Add a new visual separator to menu.
* Add a new sub-menu item. Assumption is that it will be populated by additional menu insert calls.

|
| ---
|
 **a.** | End a sub-menu. This is optional, see menu stack discussion below.
* Add multiple menu items.

This is implemented using a menu stack.[axlUIMenuFind](#390729 "10") resets the stack and each submenu created increments the stack. The 'end mode (submenu) decrements the stack. The menu stack allows the building of a menu tree with very little coding overhead. The stack depth is restricted to 8.

* ***Menu items should not be created outside a menu trigger. See discussion in[axlUIMenuFind](#390729 "10"). For development purposes you can create menu items outside of the menu trigger.***

#### Arguments

* menu id which can be obtained from axlUIMenuFind or creating a submenu via this API. If nil uses the current menu on the menu stack
* text that is shown in the menu. Possible values are:

  `separator` - add a separator (horizontal line)

  `popup` - create a new submenu
* pops the menu stack if creating a menu tree
* this is ignored for a 'separator
* this is the display string for '`popup` option 'end
* This is a list of`t_display/t_command` value pairs that instruct this interface to add multiple menu items and submenus in a single call. Both the `'separator` and `'end` options do not have to be a list.

#### Value Returned

`t` - successful

`nil` - failed

`x_menuId` - if creating a new submenu, the nesting id of new submenu

#### See Also

[axlUIMenuFind](#390729 "10")

#### Example

* Add a separator before the add rect command

> `q = axlUIMenuFind( nil "add rect")`

> `z = axlUIMenuInsert(q 'separator )`

* Add a web link at the top of the help menu

> `q = axlUIMenuFind( nil -1 'top)`

> `z = axlUIMenuInsert(q "Google" "http http://google.com" )`

* Add a new submenu to the right of the help menu with two commands

> `q = axlUIMenuFind( nil -1)`

> `; the nil is intention in here since it demostrates`

> `; the use of the currrent menu from find.`

> `z = axlUIMenuInsert(q 'popup "MyMenu")`

> `; the nil is required for the next 2 calls since we want to`

> `; insert these these items into MyMenu`

> `z = axlUIMenuInsert(z "1" "echo hello 1" )`

> `z = axlUIMenuInsert(z "2" "echo hello 2" )`

* More nested menu

See`<cdsroot>``/share/pcb/examples/skill/ui/menu.il`

### axlUIMenuRegister

`axlUIMenuRegister(t_command/x_locationll_menu[g_menuOption]) => t/nil`

#### Description

This allows you to register menu items to be loaded when Allegro loads a new menu. It is a combination of[axlUIMenuFind](#390729 "10") and [axlUIMenuInsert](#392601 "10").

If more elaborate menu configuration is required consider calling[axlTriggerSet](14dsnctl.html#706908 "14") directly.

* For registering menu items based upon product you need to use this API plus the[axlTriggerSet](14dsnctl.html#706908 "14") method with one or more of the following APIs.

* To deterimine if the symbol editor is active use[axlIsSymbolEditor](14dsnctl.html#721385 "14") function.

* [axlDesignType](14dsnctl.html#688746 "14") may be used to differentiate betwene PCB, APD or SIP.

* Finally,[axlVersion](23utils.html#913164 "24") with an option:

|  |  |
| --- | --- | ---
|  |  | `'programName` - another method to differentiate between PCB, APD or SIP
|  |  |
| --- | --- | ---
|  |  | `'displayName` - differentiates between the products (PCB XL vs PCB Performance). This tends change considerably between releases and may change via ISR.
|  |  |
| --- | --- | ---
|  |  | other options to this interface further classifiy products in a simple`t`/`nil` return classification.
|  |  |
| --- | --- | ---
|  |  | See[axlUIMenuFind](#390729 "10") for cautions about portability across releases.
|  |  |
| --- | --- | ---
|  |  | When multiple menu registers are done, there may be depedencies. For example, if the first menu register adds a new submenu before the File menu the result will be not as expected if the second attempts to add a new item to the Edit menu via the location method.
|  |  |
| --- | --- | ---
|  |  | This API must never be called from within a axlTriggerSet callback function.
#### Arguments

|  |
| --- | ---
| `t_command` | Command to insert menu before (see[axlUIMenuFind](#390729 "10"))
| `x_location` | Location before to insert menu (see[axlUIMenuFind](#390729 "10"))
| `ll_menu` | List of menu items to load (see format 3 option of[axlUIMenuInsert](#392601 "10"))
| `g_menuOption` | Indication to add to top or bottom of menu (see[axlUIMenuFind](#390729 "10"))
#### Value Returned

`t`, if register function for indicated callback, `nil`, if the command failed to register trigger

#### See Also

[axlUIMenuFind](#390729 "10"), [axlUIMenuInsert](#392601 "10"), [axlTriggerSet](14dsnctl.html#706908 "14"), [axlUIMenuDebug](#390812 "10"), [axlIsSymbolEditor](14dsnctl.html#721385 "14")

#### Example

See`<cdsroot>``/share/pcb/examples/skill/ui/menu.il`

### axlUIPrompt

`axlUIPrompt(`

`t_message`

`[t_default]/'password`

`)`

`==> t_response/nil`

#### Description

Displays the string`t_message` in a form. The user must type a response into the field. Displays the argument `t_default` in brackets to the left of the field. The user presses the *Return* key or clicks the *OK*button in the window to accept the value of `t_default` as the function return value. If the user selects the *Cancel* button, the function returns `nil`.

This function is a blocker. The user must respond before any further interaction with Allegro PCB Editor.

#### Arguments

|  |
| --- | ---
| `t_message` | Message string displayed.
| `t_default` | Default value displayed to the user and returned if user presses only the*Return* key or clicks *OK*.
| `'password:` | Obscure and do not script user input.
#### Value Returned

|  |
| --- | ---
| `t_response` | User response or default value.
| `nil` | User selected*Cancel*.
#### Example

> `axlUIPrompt( "Enter module name" "demo" )`

> `⇒ "mymcm"`

Prompts for a module name with a default`demo`. Typing`mymcm`overrides the default.

A text field displays, with the default value "`demo.` To accept the default value, you may either press *Return* or select *OK*. Otherwise, type a new value in the text field and press *Return* or click *OK*. In this example, enter `"mymcm"` in the text field and click *Return*.

`axlprompt` returns the following:

> `==> "mymcm"`

Password prompt:

> `ret = axlUIPrompt( "Enter password" 'password )`

#### See also

[axlUIConfirm](#101764 "10")

### axlUIWCloseAll

`axlUIWCloseAll()==> t / nil`

#### Description

This closes all temporary windows (dialogs and text view windows). A temporary window is a dialog that closes if you open another design (e.g. brd). Via Skill this window attribute is set by the axlUIWPerm API. The constraint manager is currently considered a permanent window but this may change in future releases. A blocking window (e.g. File Browser dialogs) cannot be closed via this call.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t` | always
#### See Also

[axlUIWPerm](#380009 "10")

### axlUIWIconify

`axlUIWIconify (r_window/t_windowt/nil)=> t/nil`

#### Description

This command either creates an icon for a window or open a window from an icon.This is different from[axlUIWExpose](#101852 "10"), which also opens a window from an icon but exposes hidden windows and permits raising a window to the top of the stack. Note all sub-windows also open or closed to an icon. So, if you make the main Allegro PCB Editor window an icon, all of its child windows are also closed.`t_window` name may change from release to release although this is not normal. `nil` may be used for the main window. Currently, Constraint Manager interface is not supported by this skill command.

#### Arguments

|  |
| --- | ---
| `r_window` | Window ID.
| `t_window` | Window name.  This is the name that appears in PCB Editor scripting -- invoked using the`setwindow` command.
| `t` | To iconify window,`nil` open from an icon.
#### Value Returned

|  |
| --- | ---
| `t` | For success
| `nil` | For failure (The specified window could not be found)'
#### Examples

Command to iconify Allegro PCB Editor

> `axlUIWIconify("pcb")`

#### See Also

[axlUIWIsWindow](#417824 "10"), [axlUIWIsIconic](#417702 "10"), [axlUIWExpose](#101852 "10")

### axlUIWIsIconic

`axlUIWIsIconic(r_window/t_window)=> t/nil`

#### Description

Is the window in an icon state.`nil` may be used for the main window. `t_window` name may change from release to release although this is not normal. Constraint Manager is not yet supported by this skill command.

#### Arguments

|  |
| --- | ---
| `r_window` | Window ID.
| `t_window` | Window name. This is the name that appears in Allegro scripting window -- using the`setwindow` command.
#### Value Returned

|  |
| --- | ---
| `t` | For success
| `nil` | For failure (when the specified window cannot be found)'
#### Examples

Check if main window is in icon state

`axlUIWIsIconic("pcb")`

#### See Also

[axlUIWIsWindow](#417824 "10"), [axlUIWIconify](#417517 "10")

### axlUIWIsWindow

`axlUIWIsWindow (t_window)=> t/nil`

#### Description

Returns`t` if named window is open. `t_window` name may change from release to release although this is not normal.

#### Arguments

|  |
| --- | ---
| `t_window` | Window name. This is the name that appears in Allegro PCB Editor -- using the`setwindow` command.
#### Value Returns

|  |
| --- | ---
| `t` | For success
| `nil` | No window by that name is open
#### Examples

Is Constraint Manager open

axlUIWIsWindow("cmgr")

#### See Also

[axlUIWClose](#101864 "10")

### axlUIWMove

`axlUIWMove(r_window/nilt_windowl_xy)-> t/nil`

#### Description

Moves a window. New location (`l_xy`) which is upper left corner, is specified in pixels.

`nil` may be used for the main window.

`t_window` name may change from release to release although this is not normal.

> **Note:** Constraint Manager is not yet supported.

#### Arguments

|  |
| --- | ---
| `r_window` | Window ID or if nil the main window.
| `t_window` | Window name. This is the name that appears in Allegro scripting from the setwindow command.
| `l_xy` | (`x_X x_y`)
#### Value Returned

|  |
| --- | ---
| `t` | window moved
| `nil` | Error, handle is not a window
#### See Also

[axlUIWSize](#413785 "10")

#### Example

Move main window to upper left corner of the display.

`axlUIWMove(nil 0:0)`

### axlUIWRedraw

`axlUIWRedraw(r_window/nil)=> t/nil`

#### Description

Redraws indicated window. If window ID is`nil` redraws the main window.

#### Arguments

|  |
| --- | ---
| `r_window` | Window ID or if`nil`, the main window.
#### Value Returns

|  |
| --- | ---
| `t` | For success
| `nil` | In case of failure (window already closed or not a window)
### axlUIWSize

`axlUIWSize(r_window/nil)-> ll_rect`

#### Description

Returns outer size of a window. Size is in pixels. x and y coordinates are upper left corner of window.

On UNIX/Linux, the`y` value will typically include an offset due to title bar height.

#### Arguments

|  |
| --- | ---
| `r_window` | Window id or if`nil` the main window.
#### Value Returned

|  |
| --- | ---
| `ll_rect` | `( (x_X x_Y) (x_Width x_Height))`
| `nil` | Error, handle is not a window
#### See Also

[axlUIWMove](#386643 "10")

### axlIsViewFileType

`axlIsViewFileType(g_userType)⇒ t/nil`

#### Description

Tests whether`g_userType` is a long message window type.

#### Arguments

|  |
| --- | ---
| `g_userType` | Argument to test.
#### Value Returned

|  |
| --- | ---
| `t` | `g_userType` is of type `r_windowMsg`.
| `nil` | `g_userType` is not of type `r_windowMsg`.
#### Example

> > ```
> > logWindow =    axlUIViewFileCreate("batch_drc.log" "Batch DRC Log" t)    axlIsViewFileType(logWindow)⇒ t
> > ```

* Creates a window using`axlUIViewFileCreate` (See [axlUIViewFileCreate](#101806 "10").)

* Tests whether the window is a view file type.

* Returns`t`.

#### See Also

[axlUIViewFileCreate](#101806 "10")

### axlUIViewFileCreate

```
axlUIViewFileCreate(t_filet_titleg_deleteFile[lx_size][lt_placement][g_formToExpose])⇒ r_windowMsg/nil
```

#### Description

Opens a file view window to display a file (`t_file`), it is an error for file not to exist. Window should be given a title (t\_title).

If`g_deleteFile` is set to `t`, the file is deleted when view window is quit or reused. It is suggested that applications not delete view files themselves as the Save and Print buttons will not work.

Size of viewable window is controlled by`lx_size.`Default size is 24x80. Unpredictable results may occur for large row/column values.

Placement of window is handled by`lt_placement` list. If this value is `nil`, the window is centered on editor.

Window may be deleted via program control via[axlUIWClose](#101864 "10") function.

#### Arguments

|  |
| --- | ---
| `t_file` | Name of the ASCII file to display. If the value is "" then last registered log file is displayed.
| `t_title` | Title to be display in window title bar.
| `g_deleteFile` | Deletes the file when the user quits the window or another task reuses the window.
| `lx_size` | Initial size of the window in character rows and columns. The default is 24 by 80. Setting a large window size may cause unpredictable results.
| `lt_placement` | Window placement hints.  See the section on[Window Placement](#101699 "10").
| `g_formToExpose` | Optional handle of another window. If specified then this window is brought to the top of the desktop when the view file window is closed. If not specified then the main program window is the parent.
#### Value Returned

|  |
| --- | ---
| `r_windowMsg` | Window`r_windowMsg`.
| `nil` | `r_windowMsg` not displayed.
#### Example

* Displays the batch DRC log file, saving the window id.

* Deletes the file`drc.log` when the user exits the window.

> `logWindow = axlUIViewFileCreate("batch_drc.log" "Batch DRC Log" nil)`

The log file displays in a window. When the user choosesClose, deletes the file `batch_drc.log`.

### axlUIViewFileReuse

`axlUIViewFileReuse(r_windowMsgt_filet_titleg_deleteFile[g_formToExpose])⇒ t/nil`

#### Description

Reuses the view window to display a file (t\_file). Error is thrown if the file does not exist. Window is given a title (t\_title).

Expects r\_windowMsg to be type of view window. If user quit the window it will re-open it at the old size/position.

File is deleted is g\_deleteFile is t when view window is quit or reused. It is suggested that applications not delete view files themselves as the Save and Print buttons will not work.

#### Arguments

|  |
| --- | ---
| `r_windowMsg` | `dbid` of the existing view window created earlier with `axlUIViewFileCreate`.
| `t_file` | Name of the ASCII file to display.
| `t_title` | Title to display in window title bar.
| `g_deleteFile` | Deletes file when the user quits the window or another task reuses the window.
| `g_formToExpose` | Optional argument that defines the handle of a window to be exposed when the text file window is closed. Default is the parent set by[axlUIViewFileCreate](#101806 "10"). Normally you should not use this argument.
#### Value Returned

|  |
| --- | ---
| `t` | File displayed.
| `nil` | File not displayed.
#### Example

> `(axlUIViewFileReuse logWindow "ncdrill.log" "NC Drill Log" nil)`

* Displays the file`ncdrill.log`, reusing the window `logWindow` created when displaying `batch_drc.log` in the `axlUIViewFileCreate` example.

* Exiting the window automatically deletes the file`ncdrill.log`.

### axlUIYesNo

`axlUIYesNo(`

`t_message`

`[t_title]`

`[s_default]`

`)`

`==> t/nil`

#### Description

Provides a dialog box displaying the message`t_message`. Returns `t` if you choose *Yes* and `nil` for *No*.

This function is a blocker. You must respond before any further interaction with Allegro PCB Editor.

**Note:**

* If environment variable`noconfirm` is set, we immediately return `t`for yes and`nil`for no.

#### Arguments

|  |
| --- | ---
| `t_message` | Message string to display.
#### Value Returned

|  |
| --- | ---
| `t` | User responded*Yes*.
| `nil` | User responded*No*.
#### See Also

[axlUIConfirm](#101764 "10")

#### Examples

The following examples are a typical overwrite question.

> `axlUIYesNo( "Overwrite module?" )`

> `axlUIYesNo( "Overwrite module?" nil 'no )`

> `axlUIYesNo( "Overwrite module?" "My Skill Program" )`

> `A confirmer window is displayed. If the user selects Yes, the`

> `function returns t, otherwise it returns nil.`

> `**/`

> `list`

> `axlUIYesNo(int argc, list *argv)`

> `{`

> `char *str, *title;`

> `int dflt;`

> `str = axluGetString(NULL, argv[0]);`

> `title = (argc>1) ? axluGetString(NULL, argv[1]) : NULL;`

> `dflt = (argc>2) ? DfltResponse(argv[2]) : MN_YES;`

> `return(MNYesNoWTitle(str, title, dflt) ? ilcT : ilcNil);`

> `}`

> `/*`

> `#ifdef DOC_C`

### axlUIWExpose

`axlUIWExpose(r_window/nil)⇒ t/nil`

#### Description

Opens and redisplays a hidden or iconified window, bringing it to the front of all other current windows on the display. If`nil`, the main window is displayed.

#### Arguments

|  |
| --- | ---
| `r_window` | Window`dbid`.
#### Value Returned

|  |
| --- | ---
| `t` | Window opened and brought to front.
| `nil` | `dbid` was not of a window.
#### Example

> > ```
> > logWindow =    axlUIViewFileCreate("batch_drc.log" "Batch DRC Log" t); Other interactive code, possibly; causing Batch DRC Log window to be covered; Uncover the log window:axlUIWExpose(logWindow)⇒ t
> > ```

* Displays a window using`axlUIViewFileCreate`.

* Interactively moves window behind one or more other windows using the*back* selection of your window manager.

* Calls`axlUIWExpose`.

> Window comes to the top above all other windows.

### axlUIWClose

`axlUIWClose(r_window/t_window)⇒ t/nil`

#### Description

Closes a window, if it is open.

**Note:** Window may also be closed by user. See initial sections of the chapter for specific window types.

#### Arguments

|  |
| --- | ---
| `r_window` | Window`dbid`.
| `t_window` | Window name. This is the name that appears in Allegro scripting from the setwindow command.
`t_window` name may change from release to release although this is not normal.

#### Value Returned

|  |
| --- | ---
| `t` | Window closed.
| `nil` | Window already closed, or`dbid` is not of a window.
#### Example

* The following example, displays a window using axlUIViewFileCreate, and closes it using axlUIWClose.

> `logWindow = axlUIViewFileCreate("batch_drc.log" "Batch DRC Log" t)`

> ;;; Other interactive code

> `axlUIWClose(logWindow)`

* Close Constraint Manager

> `axlUIWClose("cmgr")`

#### See Also

[axlUIWIsWindow](#417824 "10")

### axlUIWHelpRegister

* Command to register new help file

`axlUIWHelpRegister(t_cmdt_helpFile) -> t/nil`

* Query if help file registered for command

`axlUIWHelpRegister(t_cmd) -> t_file`

* Delete help file registered for command

`axlUIWHelpRegister(t_cmd"") -> t/nil`

* Lists all cmds registered for help

`axlUIWHelpRegister(nil) -> lt_cmds`

#### Description

This registers a help document for a user written skill command or form (dialog). This is typically used in conjunction with axlCmdRegister. You should make this call at the time you do a axlCmdRegister instead of waiting until the skill code associated with the command executes.

You can also add the registrations via the`help_config.txt` file (see `<cdsroot>``/share/pcb/help/help_config.txt`) placed at the site or pcbenv directory.

The document types (determined via file extension) supported on all platforms are:

* `.txt` - a plain text file displayed via Allegro's internal long message window

* `.html` - html browser displayed via a web browser

* `.pdf` - Acrobat file displayed by a Acrobat reader

On Windows other extensions are typically supported which are determined by what programs are installed on the computer (e.g. doc for Word and ppt for PowerPoint).

#### Arguments

|  |
| --- | ---
| `t_cmd` | Command name or form.<formname> for registering help for form buttons
| `t_helpFile` | Document to display. Variable expansion is supported so you can embed Allegro env variables to make the installed location of the files relative to the variable setting.
#### Value Returned

`t` for success, `nil` for failure (invalid arguments)

#### See Also

[axlCmdRegister](19cmdctl.html#954297 "20")

#### Examples

Override add line help with contents of Allegro's env file

> `axlCmdRegister("add line" "$TELENV")`

### axlUIWPrint

`axlUIWPrint(r_window/nilt_formatString[g_arg1 ...]`

`)`

`⇒ t/nil`

#### Description

Prints a message to a window other than the main window. If`r_window` does not have a message line, the message goes to the main window. This function does not buffer messages, but displays them immediately. If the message string does not start with a message class (for example \e), it is treated as a text (\t) message. (See [axlMsgPut](13msghnd.html#673546 "13")) If `nil`, displays the main window.

#### Arguments

