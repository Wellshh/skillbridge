### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

20
==

Command Control Functions
=========================

The chapter describes the AXL-SKILL functions that register and unregister AXL-SKILL functions with Allegro PCB Editor and set various modes in the user interface.

AXL-SKILL Command Control Functions
-----------------------------------

This section lists the command control functions.

### axlCmdRegister

```
axlCmdRegister(t_allegroCmdts_callback?cmdType t_cmdType?doneCmd ts_doneCmd?cancelCmd ts_cancelCmd?undo t)⇒ t/nil
```

#### Description

Registers a command named`t_allegroCmd` with the Allegro PCB Editor shell system. If the command already exists, either because it is a base Allegro PCB Editor command or because it has been registered by this function at an earlier time, it will be hidden.

Once you register a command, Allegro PCB Editor passes its arguments to SKILL-AXL without parsing them.

You can call the`axlCmdRegister` command any time. Once a command is registered, you can type it at the Allegro PCB Editor command line and also incorporate it into menus and pop-ups.

* Interactive mode should be used if you are changing the database. It will "done" an active interactive command before starting your command. General mode should be used to view the database or to provide some non-database capabilities. It is allowed to co-exist with other general and interactive commands. If changing the database using a form only command, for example, not requesting user picks from the canvas, then you should provide a dummy event handler to prevent your skill code from returning to Allegro.
  See example in`<cdsroot>``/share/pcb/examples/skill/cns-design.il` function `_AcDesignEvent()`.
  You can pass arguments from the Allegro command line to your registered Skill function. See `<cdsroot>``/share/pcb/examples/skill/examples/axlcore/arg.il`

> Commands that support undo or redo must follow the programming concepts.

> Programming checklist includes:

* utilize`axlDBTransaction` APIs around database changes

* do not save or open the databases

* do not call`axlRunBatchDBProgram` with an option to reload the database

* make use of`axlShell`

* if your program typically performs extensive database changes, do not register it as undoable due to memory consumption requirements

The following items do not follow undo or redo:

* files saved or updated on disk

* database attachment changes (see`axlCreateAttachment`)

* communication to external programs or user interfaces

* certain design state changes such as active layer

* if your program maintains state across invocations then redo may not work properly

> An interactive command may be updated or written to support undo (see`cline2shape.il`) using two models:

* Undo all Allegro database changes made by the command from start to done. If you use database transactions in an existing SKILL command then to convert it to support undo all you need to do is to add the undo option to`axlCmdRegister`.

* To have it work like place manual, where each individual placement operation is an undo then you will need to revamp the transaction model of your code. You need to start and commit and a database transaction around each user change to the design. The`cline2shape.il` shows how the code is slightly different in transaction handling between the two modes.

|  |  |
| --- | --- | ---
|  |  | Avoid doing a start transaction with the undoMark symbol and a commit if you do not perform database operations.
|  |  |
| --- | --- | ---
|  |  | If you do this incorrectly, additional undo items are listed on the toolbar's undo icon. The code still performs properly but some undo operations will not do anything.
* ***You cannot access interactive Allegro PCB Editor commands via`axlShell` if you register your skill code as interactive, because nesting interactive commands are not supported. This includes using `axlShell` to spawn Allegro PCB Editor scripts that contain interactive commands, which are those that display in the lower right side of the Allegro PCB Editor window (where the `Idle` string appears). For an interactive command the status area shows the command name. Failing that if you notice odd behavior when calling `axlShell`, try changing your command type to General. As noted above, you should not call any APIs in the `axlEnter` or `axlSelect` families in a General command type.***

#### Arguments

|  |
| --- | ---
| `t_allegroCmd` | Name of the command to register. Use lowercase letters for the command name.
| `ts_callback` | Name of SKILL callback routine called when the command is activated from the Allegro PCB Editor window.
| `t_cmdType` | String denoting the type of this command:  `"interactive"`  Allegro PCB Editor interactive command which is the default.  `"general"`  Immediate command that executes as soon as the command is called, even during another command. Use for display refresh commands, for example.  `"sub_cmd"`  Must be called inside an interactive command. Use for pop-ups.
|
|
|
|
|
|
| `ts_doneCmd` | *Done* callback function that Allegro PCB Editor calls when the user types `done` or selects *Done* from the pop-up. Can be either a symbol or string. If `nil`, Allegro PCB Editor calls `axlFinishEnterFun` by default.
| `ts_cancelCmd` | Cancel callback function that Allegro PCB Editor calls when the user types`cancel` or selects *Cancel* from the pop-up. This argument can be either a symbol or a string. If it is `nil`, Allegro PCB Editor calls `axlCancelEnterFun` by default.
| `undo` | If`t`, command can be undone. It is only applicable for `t_cmdType` `"interactive"`. Refer Tip section for programming requirements of undo commands.
|  | Other options may be added at a future time.
#### Value Returned

|  |
| --- | ---
| `t` | Command registered successfully.
| `nil` | Command not registered.
#### See Also

[axlCmdUnregister](#954317 "20"), [axlCmdList](23utils.html#913642 "24"), [axlUIWHelpRegister](10usrint.html#404919 "10"), [axlDBTransactionStart](17dbtran.html#1076430 "18")

#### Example 1

> ```
> axlCmdRegister( "my swap gates" 'axlMySwapGates ?cmdType "interactive" ?doneCmd 'axlMySwapDone?cancelCmd 'axlMySwapCancel)⇒ t
> ```

Registers the command`my swap gates` as calling the function `axlMySwapGates`.

#### Example 2 SKILL Function Example

For commands (`s_allegroCmd` value) that accept parameters as strings, the SKILL function converts the parameters to symbols.

`axlCmdRegister( "do it" 'do_print)`

`do it myFile Text AshFindAllText`

Sample`axlCmdRegister` with a registered function that takes arguments where `myFile` is an output port.

`(defun do_print (arg1 description find_func) ;; Added to deal with strings`

`myport = evalstring(arg1) ;; Added to deal with strings`

`do_print2( myport description find_func) ;; Added to deal with strings`

`) ; do_print ;; Added to deal with strings`

`# Here is the real function`

`(defun do_print2 (p description find_func)`

`(let (list)`

`(fprintf p "Properties on %s:\n" description)`

`(setq list (apply find_func nil))`

`(print_list_props list p)`

`(fprintf p "\n\n")`

`) ; let`

`) ; do_print2`

Parse and process the`do it` arguments.

See`<cdsroot>``/share/pcb/examples/skill/examples/axlcore/cline2shape.il`for the undo examples.

### axlCmdUnregister

`axlCmdUnregister(t_allegroCmd)⇒ t/nil`

#### Description

Unregisters or removes from the Allegro PCB Editor shell system, a previously registered command named`t_allegroCmd`. If the command already exists because it is a base Allegro PCB Editor command, the original command is available again.

#### Arguments

|  |
| --- | ---
| `t_allegroCmd` | Name of command to be unregistered.
#### Value Returned

|  |
| --- | ---
| `t` | Command unregistered successfully.
| `nil` | Failed to unregister the specified command.
#### Example

> `axlCmdUnregister( "my swap gates")⇒ t`

Unregisters the command`my swap gates`.

### axlEndSkillMode

`axlEndSkillMode()⇒ t`

#### Description

Returns from the SKILL command mode to the program's command line. The SKILL exit function is mapped to this function. In a SKILL program this command has no effect.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

> `axlEndSkillMode()⇒ t`

Exits AXL-SKILL.

### axlFlushDisplay

`axlFlushDisplay()⇒ t`

#### Description

Flushes all data from the display buffer to the display screen itself. Displays items intended to be displayed, but not yet displayed because no event has triggered a flush of the display buffer.

You can display the following Items:

* Visible objects added to the database

* Messages

* Highlighting and dehighlighting of selected objects

* Pending display repairs

Generally, AXL delays screen updates until a prompt for user input occurs or an AXL program completes, such as`axlEnterPoint`. Certain programs, such as those that spend long times doing calculations between screen updates, might want to call `axlFlushDisplay` after each batch of screen updates to indicate the progress of the command. Overuse of this call may hurt performance.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

> > ```
> > mypath = axlPathStart( list(8900:4400))axlPathArcRadius(mypath, 12., 8700:5300, nil, nil, 500)myline = axlDBCreatePath( mypath, "etch/top" nil); Arc is not yet visibleaxlFlushDisplay(); Now arc is visible
> > ```

Creates a path and displays it immediately regardless of whether the user has caused a display event such as moving the cursor into the Allegro PCB Editor window.

### axlOKToProceed

`axlOKToProceed()⇒ t`

#### Description

Checks whether Allegro PCB Editor is processing another interactive command or engaged in some process that might interfere with a SKILL command. Use this to check before starting functions such as`dbcreate`, user interactions, and select set operations. Returns `t` if Allegro PCB Editor is ready to properly execute a SKILL command, and returns `nil` if it is not.

#### Arguments

|  |
| --- | ---
| `t` | Suppresses the error message produced when it is not OK to proceed.
#### Value Returned

|  |
| --- | ---
| `t` | Allegro PCB Editor can allow AXL-SKILL database, selection, and interactive functions to execute.
| `nil` | Allegro PCB Editor cannot allow AXL-SKILL database, selection, and interactive functions to execute.
#### Example

`(when axlOKToProceed    ;; do AXL interactive command    )`

### axlSetLineLock

```
axlSetLineLock(?arcEnable    g_arcEnable?lockAngle    f_lockAngle?minRadius    f_minRadius?length45    f_length45?fixed45    g_fixed45?lengthRadius    f_lengthRadius?fixedRadius    g_fixedRadius?lockTangent    g_lockTangent)⇒ t/nil
```

#### Description

Sets one or more of the line lock parameters. The parameters are the same as those accessible in the*Line Lock* section of the Allegro PCB Editor Status form.

All parameters not explicitly set in a call to`axlSetLineLock` keep their current settings.

#### Arguments

|  |
| --- | ---
| `g_arcEnable` | If`t`, sets Lock Mode to `Arc`. Otherwise Lock Mode is Line. Default is Line.
| `f_lockAngle` | Sets Lock Direction. Allowed values are: 45 (degrees), 90 (degrees), or 0 (off, or no lock).
| `f_minRadius` | Sets Minimum Radius, a value in user units.
| `f_length45` | Sets the Fixed 45 Length value in user units.
| `g_fixed45` | If`t`, sets the Fixed 45 Length mode. You cannot set this parameter unless `f_lockAngle` is 45, and `g_arcEnable` is `nil`.
| `f_lengthRadius` | Sets Fixed Radius value in user units.
| `g_fixedRadius` | If`t`, sets the Fixed Radius mode. You cannot set this parameter unless `f_lockAngle` is 45 or 90, and `g_arcEnable` is `t`.
| `g_lockTangent` | If`t`, sets the Tangent mode to `on`.
#### Value Returned

|  |
| --- | ---
| `t` | Set the given line lock parameters successfully.
| `nil` | Failed to set the given line lock parameters.
#### Example

> `axlSetLineLock( ?arcEnable t ?lockAngle 90 ?fixedRadius t?lengthRadius 50)`

Sets the Line Lock parameters to Lock Direction:`90`, Lock Mode: `Arc`, Fixed Radius: `on` at `30` mils.

### axlSetRotateIncrement

`axlSetRotateIncrement(?angular    f_angular?radial    f_radial)⇒ t/nil`

#### Description

Sets the dynamic rotate angle increment in degrees (`f_angular`) or radians (`f_radial`). Sets the rotate increment for rotation of objects in the dynamic buffer.

#### Arguments

|  |
| --- | ---
| `f_angular` | Sets angle lock increment in degrees.
| `f_radial` | Sets radial lock increment in radians.
#### Value Returned

|  |
| --- | ---
| `t` | Set the given rotate increment parameters successfully.
#### Example

> `(axlSetRotateIncrement ?angular 15)⇒ t`

Sets the dynamic rotate angle to 15 degrees.

### axlUIGetUserData

`axlUIGetUserData()⇒ r_userData/nil`

#### Description

Gets the current user data structure from Allegro PCB Editor. The user data structure stores basic information about the state of the user interface. By default it contains the properties:

|  |
| --- | ---
| `doneState` | How the user returned control to the application. Possible values are either:`done` or `cancel`.
| `popupId` | List of the current pop-up values. A list of string pairs, as shown:  `(("Done" "axlFinishEnterFun") ("Cancel" "axlCancelEnterFun"))`
| `ministatForm` | Always`nil`. (Reserved for future releases.)
You can set your own attributes in the user data structure to communicate with callbacks, as shown in the example. You cannot overwrite the three basic attributes:`doneState`, `popupId`, or `ministatForm`.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `r_userData` | User data structure from Allegro PCB Editor.
| `nil` | Failed to get user data structure from Allegro PCB Editor.
#### Example

```
userdata = axlUIGetUserData()    userdata->??    ⇒ (doneState cancel    popupId (("Cancel" "axlCancelEnterFun"))     ministatForm nil )
```

### axlUIPopupDefine

`axlUIPopupDefine(r_popupts_pairs)⇒ r_popup/nil`

#### Description

Creates a pop-up from the name value pair list`ts_pairs`. If `r_popup` already exists, it appends the name value pairs at the end of the existing pairs in `r_popup`. Use the returned `r_popup` id as the argument to `axlUIPopupSet` to make it the active pop-up.

#### Arguments

|  |
| --- | ---
| `r_popup` | Predefined pop-up handle to which to append new entries. Can be`nil` to create a new pop-up.
| `ts_pairs` | List containing the pairs ((`t_display``t_callback`) defining each pop-up entry display name and its AXL function callback.
#### Value Returned

|  |
| --- | ---
| `r_popup` | Id of the pop-up created or updated.
| `nil` | No pop-up created or updated.
#### Example

> ```
> popid = axlUIPopupDefine( nil        (list (list "Complete" 'axlMyComplete)        (list "Rotate" 'axlMyRotate)        (list "Something" 'axlMySomething)        (list "Cancel" 'axlCancelEnterFun))⇒ (        ("Complete" 'axlMyComplete)        ("Rotate" 'axlMyRotate)        ("Something" 'axlMySomething)        ("Cancel" 'axlCancelEnterFun))
> ```

Creates a pop-up with the following selections:

* *Complete*, associated with your function `axlMyComplete`

* *Rotate*, associated with `axlMyRotate`

* *Something*, associated with `axlMySomething`

* *Cancel*, associated with `axlCancelEnterFun`

### axlUIPopupSet

`axlUIPopupSet(r_popup)⇒ t/nil`

#### Description

Sets the active pop-up in Allegro PCB Editor. If`r_popup` is `nil`, unsets the currently active pop-up.

If this call is preceded by a call to axlUICmdPopupSet with a non-nil r\_popup, the contents of this popup are used to control graying of the popup items defined in the call to axlUICmdPopupSet. Otherwise r\_popup is used to replace the popup entries. In both cases, the popup callbacks will be replaced.

**Note:** The popup is invoked by pressing mouse popup button, this is normally the right mouse button.

You can clear the active pop-up by calling outside of the form callback, as follows:

> `axlUIPopup (nil)`

#### Arguments

|  |
| --- | ---
| `r_popup` | Predefined pop-up handle created by`axlUIPopupDefine`.
#### Value Returned

|  |
| --- | ---
| `t` | Set`r_popup` as the active pop-up.
| `nil` | Failed to set`r_popup` as the active pop-up.
#### Example

> ```
> popid = axlUIPopupDefine( nil        (list (list "Complete" 'axlMyComplete)        (list "Rotate" 'axlMyRotate)        (list "Something" 'axlMySomething)        (list "Cancel" 'axlCancelEnterFun))⇒ (        ("Complete" 'axlMyComplete)        ("Rotate" 'axlMyRotate)        ("Something" 'axlMySomething)        ("Cancel" 'axlCancelEnterFun))
> ```

Creates a pop-up with the following selections:

* *Complete*, associated with your function `axlMyComplete`

* *Rotate*, associated with `axlMyRotate`

* *Something*, associated with `axlMySomething`

* *Cancel*, associated with `axlCancelEnterFun`

> `axlUIPopupSet( popid)    ⇒ t`

Sets up the pop-up.

### axlBuildClassPopup

`axlBuildClassPopup(r_formt_field)⇒ t/nil`

#### Description

Supports building a form pop-up with a list of classes.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name in form or pop-up name of form.
#### Value Returned

|  |
| --- | ---
| `t` | Pop-up built.
| `nil` | Failed to build pop-up due to incorrect arguments.
#### Examples

> `axlBuildClassPopup(fw, "CLASS")`

> `axlFormSetField(fw, "CLASS" axlMapClassName("ETCH"))`

### axlBuildSubclassPopup

`axlBuildSubclassPopup(r_formt_fieldt_class)⇒ t/nil`

#### Description

Supports building a form pop-up with a list of subclasses from the indicated class.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle
| `t_field` | Field name
| `t_class` | Class name
#### Value Returned

|  |
| --- | ---
| `t` | Built form subclass pop-up.
| `nil` | Failed to build form subclass pop-up due to incorrect arguments.
#### Example

`# place holder since popup will be overridden by the code`

`POPUP <subclass>"subclass" "subclass".`

`...`

`# field name should match t_field`

`FIELD subclass`

`FLOC 9 3`

`ENUMSET 19`

`OPTIONS prettyprint ownerdrawn`

`POP "subclass"`

`ENDFIELD`

`axlBuildSubclassPopup(fw, "subclass" axlMapClassName("ETCH"))`

`axlFormSetField(fw, "subclass" "GND")`

Form file entry provides a subclass pop-up with color swatch support.

**Note:** `axlMapClassName` supports Allegro Package Designer L and Allegro Package SI XL, which rename certain classes.

### axlSubclassFormPopup

`axlSubclassFormPopup(r_formt_fieldt_classnil/lt_subclass)⇒ t/nil`

#### Description

Builds a form pop-up for a given Allegro PCB Editor class for a given field of`r_form` using the `axlSubclassFormPopup` function. This function is a combination of `axlGetParam` and `axlFormBuildPopup` with color swatching.

If the fourth argument is`nil`, the pop-up is based on all subclasses of the given class.

You can easily build a subclass pop-up containing current colors as swatches. To do this, add the following in the form file for that field:

> `OPTIONS ownerdrawn`

Pop-ups built this way are dispatched back to the application as strings.

**Note:** if list of subclasses are passed, illegal subclass names are silently ignored.

* To take advantage of color swatches in your subclass pulldown (ENUMSET) use this interface and the owner drawn option in the form file. The form file entry for your control should look like:

FIELD`<field name>`

FLOC`<x y location>`

ENUMSET`<width of field>`

OPTIONS`prettyprint ownerdrawn`

POP`<popup name>`

ENDFIELD

Note`prettyprint` option upper/lower cases the popup name the user sees.

#### Arguments

|  |
| --- | ---
| `r_form` | Standard form handle (see[axlFormCreate](11frmint.html#414342 "11"))
| `t_field` | Field name in form or pop-up name of form.
| `t_class` | Class name.
| `nil`/`lt_subclass` | Use`nil` for all members of the class, otherwise specify a list.
#### Value Returned

|  |
| --- | ---
| `t` | Form pop-up built.
| `nil` | Failed to build form pop-up.
#### Example

> `axlSubclassFormPopup( form "subclass_name" "ETCH" nil)`

### axlVisibleUpdate

`axlVisibleUpdate(t_now)⇒ t`

#### Description

The`axlVisible` family and its base building block permit changing layer color and visibility.

`axlSetParam("paramLayerGroup:..."))`

You can also use these functions in conjunction with Find Filter interaction to permit filtering objects by layer via changing visibility.

The SKILL application must indicate display update via`axlVisibleUpdate` when changing visibility on the user.

Updates any forms that display color or visibility to the user.

For most situations, pass`nil` to this function. This defers updating the main graphics canvas until control is returned to the user, allowing a combination of several canvas updates into one update.

#### Arguments

|  |
| --- | ---
| `t` | Update now.
| `nil` | Update when control is returned to the user.
#### Value Returned

|  |
| --- | ---
| `t` | Returns`t` always.
#### Example 1

`;; You should not interact with the user when you have`

`;; visibility modified`

`;; get current visibility`

`p = axlVisibleGet()`

`axlVisibleDesign(nil) ; turn off all layers`

`;;... change visiblity of selected layers ...`

`;;... Selection of objects without user interaction`

`; restore visibility`

`axlVisibleSet(p)`

Selects items using visibility without updating the display.

**Example 2**

`;; only leave top etch layer on`

`axlVisibleLayer("etch" nil)`

`axlVisibleLayer("etch/top" t)`

`; update display when control is returned to the user`

`axlVisibleUpdate(nil)`

Updates the display after changing visibility.

#### Example 3

`p = axlLayerGet("etch/top")`

`; legal numbers are 1 to 24`

`p->color = 10`

`axlSetParam(p)`

`;make this call after you change all colors and visibility`

`axlVisibleUpdate(t)`

Changes color on top etch layer.

###




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
