### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

14
==

Design Control Functions
========================

AXL-SKILL Design Control Functions
----------------------------------

The chapter describes the AXL-SKILL functions you can use to get the name and type of the current design.

### axlCurrentDesign

`axlCurrentDesign()⇒ t_design`

#### Description

Returns the name of the currently active layout. This is the drawing name in the main window's title bar.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `axlCurrentDesign` | Returns the current design name as a string. There is always a current name, even if it is "unnamed" (`unnamed.brd`).
#### See Also

[axlGetDrawingName](#717176 "14"), [axlOpenDesign](#690418 "14")

#### Example

> `axlCurrentDesign()⇒ "mem32meg"`

Gets the name of the currently active layout.

### axlDesignType

`axlDesignType(g_option)⇒ t_type/lt_type`

#### Description

Returns the type of design as a string.

#### Arguments

|  |
| --- | ---
| `g_option` | Possible values are :
* Return design type domain.

  Examples are:

  > LAYOUT for brd or mcm

  > SYMBOL for dra
* 'symbols -- return list of symbol types. If a "SYMBOL" this is sub-type of the dra.
* 'domain -- return universe of domains (strings may be repeated). This is all possible values that nil may return.
* 'members -- return list of fundamental design types.

#### Value Returned

|  |
| --- | ---
| `t_type` | string describing design type.
| `lt_type` | list of strings in a universe.
#### See Also

[axlIsSymbolEditor](#721385 "14")

#### Example

* Gets the high-level design type of the current active layout.

> `axlDesignType(nil)⇒ "LAYOUT"`

* Gets the detailed design type.

> `axlDesignType(t)⇒ "BOARD"`

### axlCompileSymbol

`axlCompileSymbol(?symbol t_name?type t_type)⇒ t_symbolName/nil`

#### Description

Compiles and edit checks the current (symbol) design and saves the compiled version on disk under the name`t_name`. If `t_name` is not provided, then `t_name` is the current drawing name. If `t_name` is provided as `nil`, you are prompted for the name. Uses the symbol type in determining some of the edit checks.

#### Arguments

|  |
| --- | ---
| `t_name` | Name of the compiled symbol.
| `t_type` | Type of symbol, the default is the current symbol type (see[axlDesignType](#688746 "14")).
#### Value Returned

|  |
| --- | ---
| `t_symbolName` | Name of the symbol.
| `nil` | Error due to incorrect arguments.
**Note:** This function is only available in the symbol editor. This is a SKILL interface to the Allegro PCB Editor*"create symbol"* command and thus has the same behavior.

### axlSetSymbolType

`axlSetSymbolType(t_symbolType)⇒ t_symbolType/nil`

#### Description

Sets the Allegro PCB Editor symbol type. Has some minor effect on the commands available and the edit checks performed when the symbol is "compiled" ([axlCompileSymbol](#705886 "14")).

Use[axlDesignType](#688746 "14") to determine current symbol type.

#### Arguments

|  |
| --- | ---
| `t_symbolType` | `"package"`, `"mechanical"`, `"format"` , `"shape"`or`"flash"`
#### Value Returned

|  |
| --- | ---
| `t_symbolType` | Symbol exists.
| `nil` | Error due to incorrect argument.
**Note:** This function is only available in the symbol editor. This is a SKILL interface into the change symbol type in the Drawing Parameters dialog box in*allegro\_symbol*.

#### See Also

[axlCompileSymbol](#705886 "14"), [axlDesignType](#688746 "14")

### axlDBControl

`axlDBControl(s_name[g_value])g_currentValue/ls_names`

#### Description

Inquires and/or sets the value of a special database control. If the setting is a value, the return is the old value of the control.

A side effect of most of these controls is that, if an active dialog box displays the current setting, the setting may not be updated. Additional side effects of individual controls are listed.

**Note:** Several display options have been moved to axlDBDisplayControl but for backward compatibility are still supported via this interface.

Items currently supported for`s_name` include the following:

Name:`busRats`Value: `t` or `nil`Set?: Yes
Description: Queries and changes the bus rats option
Equivalent: Prmed Display group
Side Effects: If changing should do ratsnestDistance first

Name:`drcEnable`Value: `t` or `nil`Set?: Yes
Description: Enables or Disables DRC/CBD system.
Equivalent: Same as status dialog box drc on/off buttons.
Side Effects: Does not perform batch DRC.

Name:`ratnestDistance`Value: `t` or `nil`Set?: Yes
Description: Accesses the ratsnest display mode.

> `t` - pin to pin

> `nil` - closest dangling net cline/via

Equivalent: Same as status dialog box Ratsnest Dist control.
Side Effects: Will recalculate the display when this is changed.

Name:`activeTextBlock`Value: 1 to `maxTextBlock`Set?: Yes
Description: Accesses the active text block number.
Equivalent: Same as status dialog box text block.
Side Effects: None

Name:`maxTextBlock`Value: 16 to 64
Set?: No
Description: Reports the maximum text block number.
Equivalent: None
Side Effects: None

Name:`activeLayer`Value: <`class`> / <`subclass`>
Set?: Yes
Description: Accesses the current class/subclass. To obtain subclass do
`cadr(parseString(axlDBControl('activeLayer "/")) )`Equivalent: Same as ministatus display.
Side Effects: None

Name:`activeAltLayer`Value: `<subclass>`Set?: Yes
Description: Accesses the current alternative etch layer
Equivalent: Same as ministatus display when in add connect.
Side Effects: None

Name:`defaultSymbolHeight`Value: float
Set?: Yes
Description: Sets the default symbol height in the database.
Equivalent: Prmed from DRC Symbol Height.
Side Effects: Will set DRC out of date, and does not update status dialog box if it is present.

Name:`editingTime`Value: int
Set?: Reset
Description: Reports editing time of design in minutes.
Equivalent: status from
Side Effects: Can reset time by passing `g_value == t`

Name:`symbolRotation`Value: float
Set?: Yes
Description: Sets the initial symbol rotation
Equivalent: Prmed form's symbol angle
Side Effects: None

Name:`symbolMirror`Value: `t`/`nil`Set?: Yes
Description: Sets the initial symbol mirror.
Equivalent: Prmed form's Symbol mirror.
Side Effects: None

Name:`schematicBrand`Value: none, concepthdl, capture
Set?: Yes
Description: Queries current database schematic branding. You can set the branding only to 'none via skill.
Equivalent: See netin in the Allegro PCB Editor dialog.
Side Effects: None.

Name:`cmgrEnabledFlow`Value: `t` or `nil`Set?: Yes (only if flag is set)
Description: Reports if board is in constraint manager enabled flow. Only valid in HDL Concept Flow.`t` - Cadence schematic Constraint Manager flow enabled (5 .pst files required)
`nil` - traditional Cadence schematic flow (3 .pst files)
Equivalent: Import Logic Branding shows "Constraint Manager Enabled Flow"
Side Effects: It is not advisable to clear this flag. This interface is provided for those customers who enabled the flow and want to restore the traditional flow. You need to do additional work on the schematic side to clear the option.

Name:`cdszFile`Value:`t` or `nil`Set?:`t` or `nil`Description: Reports if a single `.cdsz` file was used by netrev instead of multiple `.pst` files. If `t`, then `genfeed` format will output a `.cdsz` file.

Name:`schematicDir`Value: directory path
Set?: Yes
Description: Queries/changes the Cadence schematic directory path. This is the directory location for the Cadence `pst` files. This does not support 3rd party netlist location. If database is unbranded (see above), then the directory location is not stored. Existence of location is not verified.
Equivalent: Import Logic Branding Cadence Tab
Side Effects: none

Name:`testPointFixed`Value: `t` or `nil`Set?: Yes
Description: Sets global flag to lock test points. `t` - test points fixed `nil` - test points not fixed
Equivalent: Same as testprep param `"Fixed test points"`Side Effects: None

Name:`ecsetApplyRipupEtch`Value: `t` or `nil`Set?: Yes
Description: If enabled, and the schedule is anything other than min tree, ripup any etch that disagrees with the schedule. Etch may be ripped up when a refdes is renamed due to this option. Only applicable with Allegro PCB Design XL tools. Applies setting at system level to all open designs.

> `t` - ripup etch
> `nil` - preserve etch

Equivalent: Same as Constraint Manager*Tools -- Options -- "Rip up etch..."*Side Effects: None

Name:`maxEtchLayers`Value: number
Set?: No
Description: Returns maximum number of etch subclasses.
Equivalent: none
Side Effects: none

Name:`dynamicFillMode`Value: 'wysiwyg, 'rough, `nil` (Disabled) (must be a symbol not a string)
Set?: Yes
Description: Controls filling of dynamic shapes.
Equivalent: shape global param
Side Effects: Disabled in symbol editor.

Name:`maxNameLength`Value: number
Set?: Yes
Description: Sets maximum name length. Minimum is 31 and maximum is 255. For designs, you cannot set it lower then the current length. For new designs, the initial value is set by the value in the env variable allegro\_long\_name\_size.
Equiv: Design Parameter Editor, Long Name Size

Name:`dynamicFillMode`Value: wysiwyg, rough, nil (Disabled)
Set?: Yes
Description: Controls filling of dynamic shapes
Equiv: shape global param
Side Effects: Disabled in symbol editor

Name:`dynamicFilletsOn`Value: t nil
Set?: Yes
Description: Controls filling of dynamic shapes
Equiv: Gloss param fillet - dynamic fillets option
Side Effects: Disabled in symbol editor and lower level PCB tools. When enabled
                     will update design with fillets.

Name:`newFlashMode`Value: t/nil
Set?: Yes
Description: Returns if board is running old style (nil) or new style (t) flash mode (WYSIWYG negative artwork using fsm files) Note WYSIWYG is now Smooth in the display.
Equiv: none
Side Effects: If you change the mode to t without updating flash symbols, wrong artwork may occur. You should only change the mode at design creation time before any padstacks with flashes are loaded into the design.

Name:`maxAttachmentSize`Value: integer value in bytes
Set?: No
Description: Returns the largest attachment size (`axlCreateAttachment`) that may attach to the database.
Equivalent: None.
Side Effects: None.

Name:`dbSize`Value: int
Set?: No
Description: returns current database size (memory footprint)
Equiv: none
Side Effects: none

Name:`retainElecCnsOnNets`Value: t or nil
Set?: Yes
Description: Queries and changes the retain electrical constraints on nets
Equiv: netrev based option
Side Effects: This should only be set on new designs. With populated designs existing Electrical constraints will remain at xnet level. Setting the option will not promote existing settings to the xnet.

Name:`mirrorUserMask`Value: t or nil
Set?: t or nil
Description: Most designs with padstack user mask layers offer Allegro mirror capability (layers with suffix \_TOP will mirror to layer suffix \_BOTTOM and vice versa). When padstack user mask layers was introduced in 16.2, they did not offer this capability. New designs will offer this capability but designs containing user mask layers that were created in 16.2 or 16.3 will have this mirror option disabled. a cdsz file.

Name:`xnetState`Value: dml, gates, or off
Set?: No
Description: Queries current database xnet state
Equiv: none
Side Effects: none

* The first argument is a symbol ('drcEnable) and not a string ("drcEnable"). See [axlBackdrillGet](07dbaccs.html#739500 "6") to get backdrill status.

#### Arguments

|  |
| --- | ---
| `s_name` | Symbol name of control.`nil` returns all possible names.
| `g_value` | Optional symbol value to set. Usually a`t` or a `nil`.
#### Value Returned

See above.

|  |
| --- | ---
| `ls_names` | If name is`nil`, then returns a list of all controls.
#### Example

* Sets DRC system off.

> `old = axlDBControl('drcEnable, nil)`

* Gets current value of pin-2-pin ratsnest.

> `current = axlDBControl('ratsnestDistance)`

* Gets all names supported by this interface.

> `listOfNames = axlDBControl(nil)`

* Set dynamic shape mode to smooth

> `old = axloDBControl('dynamicFillMode, 'wysiwyg)`

#### See Also

[axlDBDisplayControl](#721955 "14")

### axlDBGetExtents

`axlDBGetExtents(o_dbidg_visibleOnly)==> bBox/nil`

#### Description

Provides the extents of a physical database object. You choose between getting the extents of the entire object (even if it is currently not visible) or just the current visible objects.

With the visible option the extents may be smaller then the`bBox` attribute of the element `dbid bBox`.

If a list of`dbids` is provided, the union of the extents is returned.

Unsupported dbids are ignored. Dbids that contribute to the extent are SEGMENT, CLINE, LINE, RECTANGLE, FRECTANGLE, FIGURE, TEXT, SHAPE, VOID, VIA, PIN, and SYMBOL\_INSTANCE.

#### Arguments

|  |
| --- | ---
| `o_dbid` | `dbid` of an element.
| `lo_dbid` | list of`dbids`
| `visible_only` | `t`return the extents of visible parts of the element.  `nil` return the extents of the entire element.
|
#### Value Returned

|  |
| --- | ---
| `bBox` | The extents of the element. This might be zero extents, if the object has no extents visible or does not have extents (for example, nets).
| `nil` | Error; bad arguments
### axlDBIgnoreFixed

`axlDBIgnoreFixed([g_ignore]) -> t/nil`

#### Description

Provides similar functionality to that offered by many Allegro batch programs which allow FIXED and LOCKED properties to be ignored (for example:`netrev -z`).

If`g_ignore` is `t,` FIXED testing is ignored; `nil` restores FIXED testing. No argument reports the current state of FIXED testing.

This does not disable READ-ONLY states. A parent can be locked, which means the children cannot be modified (symbols locked to prevent editing of its components). READ-ONLY objects are typically seen when you are in the partition editor.

* ***It is important that FIXED property testing be restored. Allegro automatically restores FIXED testing if your Skill program returns to Allegro. This includes calling`axlShell`.***

**Note:** Recommend using[axlDBCloak](17dbtran.html#1065349 "18") since that API catches any Skill errors and restores the mode.

#### Arguments

`g_ignore` If `t,` turn off FIXED testing; `nil` restore.

no argument Return current state of FIXED testing.

#### Value Returned

old fixed (`nil` FIXED is enable, `t` is enabled)

#### See Also

[axlDBIsFixed](07dbaccs.html#719327 "6")`,`[axlDBCloak](17dbtran.html#1065349 "18")

#### Examples

; Select an object

`p = ashOne()`

; Add fixed property

`axlDBAddProp(p, '("FIXED" t))`

; Attempt to delete it

`axlDeleteObject(p)`

; now delete it

`axlDBIgnoreFixed(t)`

`axlDeleteObject(p)`

`axlDBIgnoreFixed(nil)`

### axlDBIsReadOnly

`axlDBIsReadOnly(o_dbid) -> t/nil`

#### Description

This API command checks if indicated database object is read-only.

An example of why an object is marked read-only due to a partition being active.

#### Arguments

|  |
| --- | ---
| `o_dbid` | dbid of the element to be checked.
#### Value Returned

* `t` - object is read-only

* `nil`- not read-only or not a dbid

#### See Also

[axlDBIsFixed](07dbaccs.html#719327 "6")

#### Example

> `p = axlSelectByname("SYMBOL" "U1")`

> `ret = axlDBIsReadOnly(p)`

### axlDBSectorSize - Obsolete

`axlDBSectorSize([f_size])==> nil`

#### Description

This is obsolete. It is kept for backwards compatibility. It now calls[axlDBTuneSectorSize](#716035 "14"). Tuning sectors is now built into dbdoctor.

### axlGetDrawingName

`axlGetDrawingName()⇒ t_drawingPathName`

#### Description

Retrieves the full path of the drawing.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t_drawingPathName` | Full path of the drawing.
#### See Also

[axlCurrentDesign](#688736 "14")

#### Example

`axlGetDrawingName() => "/net/nile/home/neeti/testboards/test1.brd"`

### axlIgnoreFixed

See[axlDBIgnoreFixed](#715890 "14")`.`

### axlInTrigger

`axlInTrigger() ==> t/nil`

#### Description

Tests if the application or the utility in a axlTrigger callback. Returns`t` if currently in a trigger call. This function is only required in rare cases when you might have a utility that you want to run differently if called as part of a axlTrigger callback.

#### Arguments

None

#### Value Returned

`t` if in a trigger callback, `nil` otherwise

#### See Also

[axlTriggerSet](#706908 "14"), [axlInTriggerFunc](#735150 "14")

### axlInTriggerFunc

`axlInTriggerFunc() -> s_triggerFunc/nil`

#### Description

If in a trigger callback, reports trigger function symbol.`nil`, if not in a trigger callback.

#### Arguments

No argument required

#### Value Returned

|  |
| --- | ---
| `s_triggerFunc` | Current function name if in a trigger or`nil` if not in a trigger
#### See Also

[axlTriggerSet](#706908 "14"), [axlInTrigger](#721368 "14")

### axlIsSymbolEditor

`axlIsSymbolEditor() -> t/nil`

#### Description

Returns`t` if in symbol editor, `nil` for all other editors.

When loading custom menus you might want to differentiate between the symbol editor and design editor.

#### Arguments

None.

#### Value Returned

Returns`t` if symbol editor.

#### Ses Also

[axlDesignType](#688746 "14")

#### Example

`axlIsSymbolEditor()`

### axlKillDesign

`axlKillDesign()⇒ t/nil`

#### Description

Same as (`axlOpenDesign``<``unnamed``> "wf"`), where <`unnamed`>is the standard Allegro PCB Editor name provided for an unnamed design. If the specific name is important, you can determine it using the [axlCurrentDesign](#688736 "14") command.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t` | New design opened, replacing current design.
| `nil` | No new design opened.
#### Note

This will void all`axl dbid` handles and clear the selection set.

#### See Also

[axlOpenDesign](#690418 "14")

### axlOpenDesign

```
axlOpenDesign(?design t_design?mode t_mode?noMru g_noMru?ignoreLock g_noMru)⇒ t_design/nil
```

#### Description

Opens a design. The new design replaces the current design. If the current design has unsaved edits, you are asked to confirm before discarding them unless the current design was opened in "`r`" mode (not supported in this release) or unless `g_mode` is "`wf"`. If you cancel the confirmer, the function returns `nil` and the current design remains open.

If`t_design` is not provided, you are prompted for the name of the design to open.

If`t_design` does not exist on disk, the standard Allegro PCB Editor Drawing Parameters dialog box appears.

The designType of the new design is set as the same as the current design. It can be changed using axlSetDesignType.

#### Arguments

|  |
| --- | ---
| `t_design` | Name of the new design to edit
| `g_mode` | `"w"` or "`wf"` (see above)  add a`"l"` to disable Allegro file locking  example:`"wl"` for no locking
| `g_noMru` | If`t` does not update the Most Recently Used file list. (Default is to update.)
| `ignoreLock` | if`t`, ignores the design lock file that may be present.  The is not recommended by Cadence.
#### Value Returned

|  |
| --- | ---
| `t_design` | New design name.
| `nil` | No design opened due to incorrect argument.
**Note:** Functions the same as the Allegro PCB Editor*open* command, except you can set the `t_mode` to "`wf"` in order to discard the current edits without confirmation.

Since confirmation uses the standard Allegro PCB Editor confirmer, using the`"wf"` mode is the same as setting the `NOCONFIRM` environment variable.

This will void all`axl dbid` handles and clear the selection set.

#### See Also

[axlCurrentDesign](#688736 "14")`,`[axlKillDesign](#711442 "14")`,`[axlRenameDesign](#690475 "14")`,`[axlSaveDesign](#690505 "14")`,`[axlSetSymbolType](#690003 "14")`,`[axlRunBatchDBProgram](23utils.html#911838 "24")`,`[axlSaveEnable](#711074 "14")`,`[axlCompileSymbol](#705886 "14")

### axlOpenDesignForBatch

`axlOpenDesignForBatch(t_designt_mode)==> t_design/nil`

#### Description

Opens a design. The new design replaces the current design. Since this is for batch usage, commands and menus are not changed. If the current design has unsaved edits, then you are asked to confirm the discard unless the current design was opened in`"r"` mode (not supported in this release) or `g_mode` is `"wf"`. If you cancel the confirmer, then the function returns `nil` and the current design is left open.

If`t_design` is not provided, then you are prompted for the name of the design to open.

If`t_design` does not exist on the disk, then the standard Allegro Drawing Parameters form appears.

The`designType` of the new design is set the same as the current design. It can be changed using `axlSetDesignType`.

#### Arguments

|  |
| --- | ---
| `t_design` | The name of the new design to edit
| `g_mode` | `"w"` or `"wf"` (see above)  add a "l" to disable Allegro file locking  example: "wl" for no locking
#### Value Returned

`t_design` if opened, or `nil` if error

**Note:** This command functions the same as the Allegro`edit` command, except that the `t_mode` can be set to `"wf"` in order to discard the current edits without confirmation. Since confirmation uses the standard Allegro confirmer, the `"wf"` mode is the same as setting the `NOCONFIRM` environment variable.

This removes all axl dbid handles and clears the selection set.

#### Example

Open`u.dra` in current directory with noconfirm option

`axlOpenDesignForBatch("u.dra" "wf")`

### axlRenameDesign

`axlRenameDesign(t_design)⇒ t_design/nil`

#### Description

Changes the current design name. Has no effect on the existing disk version of the current design. The new current design name will be displayed in the window border and becomes the default name for`axlSaveDesign`.

#### Arguments

|  |
| --- | ---
| `t_design` | New current design name (without file extension).
#### Value Returned

|  |
| --- | ---
| `t_design` | New current design name.
| `nil` | Error due to incorrect argument.
#### See Also

[axlOpenDesign](#690418 "14")

#### Examples

`axlRenameDesign("foobar")`

### axlSaveDesign

```
axlSaveDesign(?design t_design?mode t_option?noMru g_noMru?noConfirm g_noConfirm?writeModel g_write)⇒ t_design/nil
```

#### Description

Saves the design with the name specified (`t_design`). If `t_design` is not specified, the current design name is used. If `t_design` is provided but the value is `nil`, you are prompted for the name. If `t_option` is `"nocheck"`, the database "quick check" is not provided. Use this option only when there is a very compelling reason.

**NOTES**

* This is essentially the Allegro "save" command.

* This will clear all axl dbid handles and the selection set.

* Use axlRunBatchDBProgram, if the intent is to save the design to run another program.

#### Arguments

|  |
| --- | ---
| `t_design` | Name for the saved design.
| `t_option` | `"nocheck`" - No database check performed.
| `g_noMru` | If`t` does not update the Most Recently Used file list. (Default is to update.)
| `g_noConfirm` | If`t` does not present a confirmer if overwriting an existing design. File is overwritten.
| `g_write` | If`t` uses allegro write file model. This means file is written to disk with provided name but current drawing name is not updated.
#### Value Returned

|  |
| --- | ---
| `t_design` | Name for the saved design.
| `nil` | Error due to incorrect argument(s).
**Note:** Essentially the Allegro PCB Editor*save* command. The current design name is not changed. Use `axlRenameDesign` to change the current design name.

This will void all`axl dbid` handles and clear the selection set.

#### See Also

[axlOpenDesign](#690418 "14")`,`[axlRenameDesign](#690475 "14")`,`[axlRunBatchDBProgram](23utils.html#911838 "24")

### axlSaveEnable

`axlSaveEnable([g_saveEnable]) -> t/nil`

#### Description

This queries or sets the design to save design. When`t,` the *File - Save design* menu command is enabled. If `nil,` it is disabled.

If no arguments are provided, then returns the current status. If`g_saveEnable` is `t,` then enables save menu (reset of next database save). If `g_saveEnable` is `nil,` disables the save menu.

It is not recommended that you unset the save enable.

#### Arguments

`g_saveEnable` `t`

If not provided, just does query.

#### Value Returned

Returns current save setting if query and previous setting if changing the value.

#### See Also

[axlSaveDesign](#690505 "14")

#### Examples

1) Query state of save

`state = axlSaveEnable()`

2) Set state of save to`t` (enable save menu)

`oldState = axlSaveEnable(t)`

### axlDBChangeDesignExtents

`axlDBChangeDesignExtents(l_bBox)⇒ t/nil`

#### Description

Changes design extents. This may fail if an object falls outside the new extents or if the extents exceed the database range.

#### Arguments

|  |
| --- | ---
| `l_bBox` | New design extents.
#### Value Returned

|  |
| --- | ---
| `t` | Size changed.
| `nil` | Failed to change size.
**Note:** This function may take extra time on large designs.

#### Example 1

> `extents = axlExtentDB('obstacle)        axlDBChangeDesignExtents(extents)`

Reduces the database to its smaller extent.

#### Example 2

`extents = axlExtentDB('obstacle)`

`extents = bBoxAdd(extents '((-100 -100) (100 100))`

`axlDBChangeDesignExtents(extents)`

To reduces the database to its minimum size plus 100 mils all around.

### axlDBChangeDesignOrigin

`axlDBChangeDesignOrigin(l_point)⇒ t/nil`

#### Description

Changes the origin of the design. This may fail if the new design origin falls outside the maximum integer range.

This is an offset. A negative number moves the database left or down and a positive number moves the database to the right or up.

**Note:** This may take extra time on large designs.

#### Arguments

|  |
| --- | ---
| `l_point` | `X``/``Y`offset.
#### Value Returned

|  |
| --- | ---
| `t` | Changed the origin of the design.
| `nil` | Failed to change the origin of the design due to an incorrect argument.
#### Example

`axlDBChangeDesignOrigin(900:900)`

Moves the origin.

### axlDBChangeDesignUnits

`axlDBChangeDesignUnits(t_units/nilx_accuracy/nilx_drcCount/nil)⇒ x_drcCount/nil`

#### Description

Changes the units and accuracy of the design. To maintain the current design value, use`nil` for `t_units` or `x_accuracy`.

When you change units, also change accuracy to maintain adequate precision within the database. Reference the following table to determine the appropriate accuracy.

|  |  |  |
| --- | --- | --- | ---
| ****Units**** | **Min Accuracy** | **Max Accuracy** | **Delta**
| mils | 0 | 4 | 0 (more then 2 not advised due Gerber)
| inches | 2 | 4 | 3
| microns | 0 | 4 | 0
| millimeters | 1 | 4 | 3
| centimeters | 2 | 4 | 4
* Decreasing accuracy is not recommended.

* Switching units between Metric and English is not recommended due to inevitable rounding issues.

* Use the new`DELTA` to decide what the accuracy should be when changing units.

`new acc = orig acc + (new delta - old delta)`

> This example shows mils to millimeters with a current accuracy of 1.

`new acc        = orig acc    + (millim delta    - mils delta)`

`4     = 1         +     3        -    0`

* When changing from one English unit to another or from one Metric unit to another, the default accuracy must match that of the previous unit. For example, if your design uses`MILS` 0 and you change to `INCHES`, the accuracy must be set to 3.

* If you change from an English unit to a Metric unit or from a Metric unit to an English unit, then the accuracy must be set to a number that is at least as accurate as the current database. For example, if the design is in`MILS` 0 and you change to `MILLIMETERS`, then the accuracy must be set to 2. Then if you change to `INCHES`, the accuracy must be set to 3 (inches and 3 = mils and 0.)

* If the accuracy needed is not allowed due to a limitation on the number of decimal places allowed for a particular unit, or if you reduce the level of accuracy, the error message,
  "`E-Accuracy will be decreased, database round-offs may occur`," displays. For example, if your design is in `MICRONS` and an accuracy of 1 and you change to `CENTIMETERS`, you get an error since `CENTIMETERS` are not allowed with an accuracy of 5.

#### Arguments

|  |
| --- | ---
| `t_units` | `Mils, inches, millimeters, centimeters, or microns.`
| `x_accuracy` | Range is 0 to 4, according to the table shown.
#### Value Returned

|  |
| --- | ---
| `x_drcCount` | drc count.
| `nil` | Failed to change design units.
**Notes:**

* This function may take extra time on large designs.

* This function reruns DRC if enabled.

#### Example 1

`axlDBChangeDesignUnits("millimeters" 4)`

Changes a design from mils/0 to millim/4 (accuracy maintains database precision).

#### Example 2

`axlDBChangeDesignUnits(nil 2)`

Increases accuracy from 0 to 2 and keeps the same units.

### axlDBCheck

`axlDBCheck(g_option/lg_options[p_file])⇒ (x_errors x_warnings)/nil`

#### Description

Runs*dbdoctor* on the current database. By default, no log file is produced. You can specify the `'log` option which writes the standard `dbdoctor.log` file. A port descriptor can be the second argument to write the `dbdoctor` output to an external file.

#### Arguments

`g_option``/``lg_options`

* **Function**
* Performs a full database check.
* Performs a full database check.
* Performs a full database check.
* Slow on large databases.
* May be slow for complicated shapes.
* Normally fast.
* Performs a full check and fix. Does not perform a shape check.
* Performs a batch DRC.
* Uses the standard`dbdoctor.log` file for output.

|  |
| --- | ---
| `p_file` | Port to write dbcheck logging.
#### Value Returned

|  |
| --- | ---
| `(x_errors x_warnings)` | Results of the check.
#### Examples

`` res = axlDBCheck (`all) ``

`printf ("errors = %d; warnings = %d", car (res), cadr (res);`

`p = outfile ("mylogfile")`

`res = axlDBCheck('(links shapes) p)`

`close(p)`

### axlDBCopyPadstack

`axlDBCopyPadstack(o_dbid/t_padstackNamelt_startEnd[g_dontTrim])⇒ o_dbid/nil`

#### Description

Creates a new padstack by copying an existing padstack, with optional removal of layers. The name for the new padstack automatically derives from the existing name by adding a unique post fix. The padstack is marked in the design as derived from its starting padstack.

Start/end must be provided and must be legal ETCH layers.

* ***If the padstack is not used, it is deleted by the next dbdoctor run.***

#### Arguments

|  |
| --- | ---
| `o_dbid` | `dbid` of the padstack to copy from.
| `t_padstackName` | Name of the padstack to copy from.
| `lt_startEnd` | List of start (`class`/`subclass`) and stop (`class`/`subclass`) layers.If class is used, it must be ETCH (PCB) or CONDUCTOR (ICP)
| `g_dontTrim` | Obsolete, ignored.
#### Value Returned

|  |
| --- | ---
| `dbid` | `dbid` of the new padstack.
| `nil` | Failed to create new padstack.
#### Example

1) To derive an exact copy:

`newPadId = axlDBCopyPadstack(padId, '("ETCH/TOP" "ETCH/BOTTOM"))`

2) To derive and trim to only connect from top layer to 2

`newPadId = axlDBCopyPadstack(padId, '("TOP" "2") nil)`

> > or

> `newPadId = axlDBCopyPadstack("VIA", '("TOP" "GND") nil)`

### axlDBDelLock

`axlDBDellLock([t_password])⇒ t/nil`

#### Description

Deletes a lock on the database. If the database is locked with a password, you must supply the correct password to unlock it.

View locks cannot be unlocked.

#### Arguments

|  |
| --- | ---
| `t_password` | Optional password string.  String length should be 6 to 20 characters.  Period (.), space, forward slash (\) and some character patterns are not legal.
#### Value Returned

|  |
| --- | ---
| `t` | Lock is removed or there is no lock to remove.
| `nil` | Failed to remove lock due to an incorrect password.
#### See Also

[axlDBSetLock](#706672 "14"), [axlDBGetLock](#706694 "14")

#### Example

* Delete lock with no password.

> `axlDBDelLock()`

* Delete lock with the password, "foobar".

> `axlDBDelLock("foobar")`

### axlDBGetLock

`axlDBGetLock()⇒ nil/l_info`

#### Description

Returns information about a lock on the database. You retrieve the following information:

|  |
| --- | ---
| `t_userName` | User login who locked the database (auto-generated)
| `t_lockDate` | Date the database was locked (auto-generated)
| `t_systemName` | System on which the database was locked (auto-generated)
| `t_locklevel` | Level of the lock: view, export or write
| `t_expiration` | Expiration duration associated with the lock from the lock date
| `t_comments` | Comments set by user who locked database
| `g_useNtp` | `t` if using a NTP for timer, `nil` uses system time
| `t_ntpServer` | NTP server name or nul
You can also determine whether or not a database is locked as this function returns`nil` when the database is unlocked, and returns a list of information when the database is locked.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `nil` | Database is unlocked.
| `l_info` | List (`t_userName` `t_lockDate` `t_systemName` `t_locklevel` `t_expiration` `t_comments` `g_useNtp` `t_ntpServer`)  Database is locked.
#### See Also

[axlDBSetLock](#706672 "14"), [axlDBDelLock](#708657 "14")

### axlDBMemoryReclaim

`axlDBMemoryReclaim( )-> x_sizeReclaimed`

#### Description

Reclaims database memory for reuse by the Allegro database. Normally in Skill memory of deleted database objects is not reused until Skill code returns to the main processing loop.

Should only be used in special cases since the default programming model works for most all Skill programs. For a well written Skill program this is typically not required.

Before utilizing this API, first try the following techniques:

* use axlDBCloak if are adding/deleting objects that are etch based (vias, clines, etch shapes, pings (e.g. like moving a symbol).

* insure that you do not have any long running db transactions (axlDBTransactionStart). E.g. commit all transactions you have active.Transactions can be nested so you should commit all the way to the initial transaction.

The one known programming model that uses this API is the "try-it" model. This is where a program adds an object to the database, performs a test and then deletes it (e.g. utilizes axlAirGap to get distances to other db objects).

For the API to be most effective make sure:

* Are not inside an axlDBCloak.

* The most memory can be reclaimed if you have no active db transactions.

Memory reclaimed is returned to the database for reuse. It is not be returned to the program's memory pool nor returned to the OS. The program's memory usage at the OS level is NOT reduced.

As a side effect some of the dbids that are checked-out may be reclaimed since they actually link to deleted db objects. They are reported as "dbid:remove".

**Note:** Do NOT use instead axl trigger callbacks.

#### Arguments

none

#### Value Returned

Amount of memory reclaimed (bytes).

#### See Also

[axlDBCloak](17dbtran.html#1065349 "18"), [axlDBTransactionStart](17dbtran.html#1076430 "18")

### axlDBSetLock

```
axlDBSetLock(['password t_password]['locklevel             t_locklevel]['expiration            t_expiration/x_expiration]['comments t_comments]['useNtp                t/nil]['ntpServer             t_server])⇒ t/nil
```

#### Description

Provides a mechanism to lock the database against future changes. If you lock the database it is locked in memory, to save the lock, you need to save the database to disk. Therefore, after locking the database, you can save the database once before all further attempts to save the database are rejected.

When a user opens a locked database, a warning, indicating that the database is locked, is thrown. An attempt to save the database fails with the above exception of above and uprev (see following text).

**Arguments**

* leading dash (-)
* Password must be greater then 5 or less then 20.
* Following characters are not allowed in the password.
* \ whitespace
* Three levels of locking are provided with the lock -- view, export, and write. If user does not provide any locklevel, or provides the wrong argument, or provides it without any password, default level of write would be used.
* With the lock, user can set the expiration duration for the design. The arguments passed must in number of days with a minimum of 1. If wrong expiration is provided, then default (no duration limit) is used.
* Free form comments. You may embed carriage returns ("\r") in the string to force a new-line in the locking user interface.
* Use NTP server to verify time when a expiration value is provided
* NTP Server to use for verify an expiration lock. If not provided uses NTPSERVER environment variable which defaults to`0.pool.ntp.org`.

* ***If using NPT based expiration locks then you must ensure that the user opening the design can access the NTP server specified. Frequently, firewalls block the NTP serve/port. The port is 123 UDP.***

**Note:** Upreving the database from to a new version ignores the lock flag. For a simple lock provide no arguments. If a nil is provided, it returns list of options to this function.

#### Value Returned

|  |
| --- | ---
| `t` | Locked database.
| `nil` | Failed to lock database due to argument errors or database already locked
#### Examples

* Most basic lock (no password, no locklevel, no expiration, no comments)

> `axlDBSetLock()`

* Lock with comments and disable data export

> ```
> axlDBSetLock('password "passwd" 'locklevel "view" 'expiration 6 'comments "Test")
> ```

> `axlSaveDesign(?design "locked_data")`

> `printf("Locked info %L\n" axlDBGetLock())`

#### See Also

[axlDBGetLock](#706694 "14"), [axlDBDelLock](#708657 "14"), [axlSaveDesign](#690505 "14")

### axlDBTuneSectorSize

`axlDBTuneSectorSize( )==> nil/l_result`

#### Description

This tune's Allegro's sector size for better performance. Normally, this occurs automatically via dbdoctor or performance advisor. In addition, it is done periodically during design open.

Allegro's optimal sector size changes over the course of a design cycle. As the design becomes complete a smaller sector size typically results in better performance at a cost of a slightly higher memory requirement.

**Note:** For the current release, the sector size is in dbunits, future releases may change this to design units.

#### Arguments

None

#### Value Returned

* `nil`: If no tuning is required

* a disembody property list: If tuning was required. The a disembody property list contains:

|  |  |
| --- | --- | ---
|  |  | old sectors
|  |  |
| --- | --- | ---
|  |  | their size
|  |  |
| --- | --- | ---
|  |  | new sectors
|  |  |
| --- | --- | ---
|  |  | new sector size
### axlTechnologyType

`axlTechnologyType()⇒ t_technology`

#### Description

Returns the type of design technology in use.

#### Arguments

`none`

#### Value Returned

|  |
| --- | ---
| `t_technology` | Technology type as shown:
|  |
| --- | ---
| **Technology Type** | **Product**
| "mcm" | Allegro Package Designer L or Allegro Package SI XL
| "pcb" | Allegro PCB Editor
### axlTriggerClear

`axlTriggerClear(s_triggers_function)⇒ t/nil`

#### Description

Removes a registered callback trigger. You pass the same arguments you passed as you registered the trigger.

#### Arguments

|  |
| --- | ---
| `s_trigger` | Trigger type. See`axlTriggerSet.`
| `s_function` | Trigger function to remove - the same as you passed to`axlTriggerSet`.
#### Value Returned

|  |
| --- | ---
| `t` | Trigger removed.
| `nil` | Failed to find a trigger by the specified name.
#### Example

See`axlTriggerSet` for an example.

### axlTriggerPrint

`axlTriggerPrint()⇒ t`

#### Description

Debug function that prints what is registered for triggers.

#### Arguments

`none`

#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
### axlTriggerSet

`axlTriggerSet(s_triggers_function)⇒ t/nil`

`axlTriggerSet(nilnil)⇒ (ls_listOfSupportTriggers)`

#### Description

Allows an application to register interest in events that occur in Allegro PCB Editor. When called with both arguments as`nil`, returns a list of supported triggers.

#### Restrictions

Unless otherwise indicated, in you Skill callback trigger you cannot:

* open, save or close the current database.

* call axlShell.

* call any of the axlEnter functions or any of the Select.

* object functions to request a user pick.

You should restrict any user interaction to blocking dialogs (forms).

#### Notes

* All trigger functions take a single argument. If you provide a function that does not match this standard, your trigger is**not** called.

* Any processing you do in triggers increases the time to open or save a database. So it is recommended that you must keep these short. If it must be longer, inform the user regarding the processing delay using`axlUIWPrint`.

* You can register multiple functions for a single trigger, but each registration must have a different function. The order that these functions are called when the trigger occurs is undefined.

* Allegro PCB Editor sends a close trigger when Allegro PCB Editor exits normally. Abnormal exits such as crash, user kill, etc. result in this trigger not being generated.

* You can do user interface work in triggers. You must have the user enter all information before returning from the trigger. Opening a dialog box may involve returning before getting data from the user. To avoid this problem, call`axlUIWBlock` after `axlFormDisplay`. This ensures you do all processing inside the trigger. For correct dialog box display, use the block option in `axlFormCreate`, the `lt_placement` parameter.

* You should use caution when using axlShell API within a trigger function. Cadence advises against this and does not support it. For example, calling Allegro commands or running scripts is not supported. Using axlShell API within a trigger function can cause the following:

|  |  |
| --- | --- | ---
|  |  | Allegro may block in the script resulting in trigger failures.
|  |  |
| --- | --- | ---
|  |  | Messages may appear to the user that you cannot suppress.
|  |  |
| --- | --- | ---
|  |  | Scripts, commands and command behavioral can change from release to release.
|  |  |
| --- | --- | ---
|  |  | User can also issue commands to different functionality.
* The triggers for opening and saving the database are generally not called when the database needs to do temporary saves, for example,`axlRunBatchDBProgram`, reports, or `netrev`.

* You can disable triggering by setting the environment variable`dbg_noskilltriggers`. If you suspect that applications running on triggers are causing problems, set this environment variable to help you debug.

#### Arguments

|  |
| --- | ---
| `s_trigger` | Trigger type as shown
:

* **Description**
* Called immediately after a database is opened. Passed a list of two items: the name of the database and`t` if existing or `nil` if a new database.

  Restrictions: You should not open, save, and close the current database.
* Called before a database is saved to disk. Passed a list of two items: the old name of the database and the new name of the database. If these are the same, then the database was overwritten. This is not called when autosaving.
* Called before another database is opened. The single item is the name of the database being discarded.
* Do not display dialogs or blocking confirmers.
* Do not read or change the database.
* Do not call axlUIMenuLoad.
* While a database is active do not change the database.
* Do not display dialogs or blocking confirmers.
* Keep processing at a minimum since this will impact user interactive performance.
* Do not change the database
* Do not invoke a dialog or blocking confirmer

|  |
| --- | ---
| `s_function` | Callback function for the event. Each trigger should have its own function. If you use the same function for multiple triggers you can not determine what function caused the trigger.
#### Value Returned

|  |
| --- | ---
| `t` | Trigger is registered for the indicated callback.
| `nil` | Trigger is not registered for the indicated callback.
#### See Also

[axlTriggerClear](#706815 "14"), [axlTriggerPrint](#706903 "14"), [axlInTrigger](#721368 "14"), [axlInTriggerFunc](#735150 "14")

#### Examples

See`<``cdsroot``>/share/pcb/examples/skill/trigger` for an example.

#### Example 1

In`ilinit`, add:

> `procedure( MyTriggerOpen( t_open)`

> `let( (brd old)`

> `brd = car(t_open)`

> `old = cadr(t_open)`

> `if (old then`

> `old = "Existing"`

> `else`

> `old = "New"`

> `)`

> `printf("SKILLCB Open %s database %s\n" old brd)`

> `t`

> `))`

> `axlTriggerSet('open 'MyTriggerOpen)`

Shows how to use this with`~/pcbenv/allegro.ilinit` to be notified when your user opens a new board. Echoes a print every time a user opens a new database.

#### Example 2

> `( isCallable('axlTriggerSet) axlTriggerSet('open 'MyTriggerOpen))`

To be compatible with pre-14.1 software, substitute for`axlTriggerSet` in `allegro.ilinit`.

### axlGetActiveLayer

`axlGetActiveLayer()⇒ t_layer`

#### Description

Retrieves active class and subclass of the design.

**Note:** This function is obsolete and is kept for compatibility reasons. Use`axlDBControl`.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t_layer` | Returns a string denoting the active class and subclass.
#### Example

`axlGetActiveLayer()    ⇒ "MANUFACTURING/PHOTOPLOT_OUTLINE"`

### axlGetActiveTextBlock

`axlGetActiveTextBlock()⇒ _textBlock`

#### Description

Gets the current active text block, equivalent to the status dialog box.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `_textBlock` | Returns the current active text block number.
### axlSetActiveLayer

`axlSetActiveLayer(t_layer)⇒ t/nil`

#### Description

Sets the active class and subclass of the design.

**Note:** This function is obsolete and is kept for compatibility reasons. Use`axlDBControl`.

#### Arguments

|  |
| --- | ---
| `t_layer` | String with the format:<`class`> **/** <`subclass`>.
#### Value Returned

|  |
| --- | ---
| `t` | Set the given active class and subclass successfully.
| `nil` | Failed to set active the given class and subclass.
#### Example

> `axlSetActiveLayer( "MANUFACTURING/PHOTOPLOT_OUTLINE")⇒ t`

### axlWFMAnyExported

`axlWFMAnyExported()==> t/nil`

#### Description

Reports if there are any exported partitions.

Use axlDesignType to see if the design is currently a partition.

#### Arguments

None

#### Value Returned

`t`, if one or more partitions are currently exported

`nil`, if no partitions exported

#### See Also

[axlDesignType](#688746 "14")

#### Examples

`axlWFMAnyExported()`

### axlDBDisplayControl

`axlDBDisplayControl(s_name[g_value])==> g_currentValue/ls_names`

#### Description

This command is used to inquire and set the display database controls. When used for setting a value, the command returns the old value of the control.

**Note:** For most of these controls, if the form that is displaying the current setting is active, it may not be updated. Additional side effects of individual controls are listed.

Use the[axlColorGet](04parmgt.html#1093245 "3") and [axlColorSet](04parmgt.html#1095354 "3") commands to change the background color.

Items currently supported are listed in[Table 14-1](#721974 "14").

****Table 14-1****
**Supported Controls**

| **Name** | **Value** | **Set** | **Description** | **Equivalent** | **Side Effects**
| connectPointSize | dbrep | Yes | Changes the size of connect points (diamond figures) | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| connectPointEnabled | t/nil | Yes | Changes visibility of connect points (diamond figures) | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| customColorEnabled | t/nil | Yes | Changes the display of custom colors | color192 dialog ("Enable Custom Colors") | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| displayNetNames | t/nil | Yes | Enables the display of net names on etch. OpenGL must be enabled. | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| designOrigin | t/nil | Yes | Enables the display of design origin | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| drcMakerSize | dbrep | Yes | Changes the size of DRC markers | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| endcapsEnable | t or nil | Yes | Controls display of line endcaps | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| filledPadsEnable | t or nil | Yes | Pads are displayed filled or hollow | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| gridColor | `1` to `<maxcolor>` | Yes | Changes the grid color  **Note:** You can find the <`maxColor`> by running the command, `` maxColor = axlColorGet(`count) `` | color dialog Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| gridEnable | `t` or `nil` | Yes | Queries and changes the grid visibility | Color form, Display Group, Grids | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| highlightColor | `1` to `<maxcolor>` | Yes | Queries/changes the permanent highlight color.  Can be used with axlHighlightObject | Color form, Display Group, Permanent highlight | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| holeColor | `1` to `<maxcolor>` | Yes | Queries/changes the drill hole color. | Color form, Display Group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| backdrillHoleColor | `1` to `<maxcolor>` | Yes | Queries/changes the backdrill hole color. | Color form, Display Group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| lastSaveUser | string | No | Reports last user login who saved design. This may be an empty string, if the design was never saved. | Status form | None
| nonPlatedHolesEnable | `t` or `nil` | Yes | Queries and changes the non-plated holes visibility.  Unlike in the prmed dialog, setting this option to`t` does not set `padlessHolesEnable` to t. | Color form, Display Group, Grids | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| backdrillHolesEnable | `t` or `nil` | Yes | Queries and changes the non-plated holes visibility.  Must have performed the backdrill process to see the holes. | Color form, Display Group, Grids | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| padlessHolesEnable | t or nil | Yes | Queries and changes the padless holes visibility | Color form, Display Group, Grids | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| platedHolesEnable | t or nil | Yes | Queries and changes the plated visibility.  Unlike in the prmed dialog, setting this option to`t` does not set `padlessHolesEnable` to t. | Color form, Display Group, Grids | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| tempColor | `1` to `<maxcolor>` | Yes | Queries/changes the temporary highlight color.  Can be used with axlHighlightObject | Color form, Display Group, Temporary highlight | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| ratsnestColor | `1` to `<maxcolor>` | Yes | Queries/changes the ratsnest color for top to bottom ratsnest. In pre-16.2 releases, this set the color for all ratsnest. | Color form, Display Group, Ratsnest Color | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| ratsnestBBColor | `1` to `<maxcolor>` | Yes | Queries/changes the ratsnest color for bottom to bottom ratsnest. | Color form, Display Group, Ratsnest Color | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| ratsnestTTColor | `1` to `<maxcolor>` | Yes | Queries/changes the ratsnest color for top to top ratsnest. | Color form, Display Group, Ratsnest Color | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| ratsnestJog | t/nil | Yes | Queries/changes the ratsnest jog option. | prmed form, Display Group, Ratsnest Jog | None
| ratTSize | dbrep | Yes | Changes the size of RatT markers | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| thermalPadEnable | t/nil | Yes | Queries and changes the thermal pads. Only applicable for negative planes. | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| transparencyGlobal | 1 to 255 | Yes | Changes the OpenGL global transparency where 1 is completely translucent and 255 is solid. | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| transparencyShape | 1 to 255 | Yes | Changes the OpenGL shape transparency where 1 is completely translucent and 255 is solid. | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| viaLabel | t/nil | Yes | Queries and changes the via label display. | prmed Display group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| viaLabelColor | `1` to `<maxcolor>` | Yes | Queries and changes the via label color. | Color form, Display Group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| stackedViaLabelColor | `1` to `<maxcolor>` | Yes | Queries and changes the stacked via label color. | Color form, Display Group | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| waiveDRCColor | `1` to `<maxcolor>` | Yes | Queries and changes the waived DRC color. | Color form, Display Group, Waived DRC | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
| waiveDRCEnable | t/nil | Yes | Queries and changes the waived DRC display state | Color form, Display Group, Waived DRC | Call[axlVisibleUpdate](19cmdctl.html#984586 "20") to update display.
#### Arguments

|  |
| --- | ---
| `s_name` | symbol name of control. nil returns all possible names
| `s_value` | optional symbol value to set. Usually a`t` or a `nil`.
#### Value Returned

See above

`ls_names`: If name is `nil` then returns a list of all controls.

#### See Also

[axlDBControl](#690074 "14"), [axlColorGet](04parmgt.html#1093245 "3"), [axlColorShadowGet](04parmgt.html#1096002 "3")

#### Examples

* Find out grid color

> `color = axlDBDisplayControl('gridColor, nil)`

* Turn on grids

> `old = axlDBDisplayControl('gridEnable t)`

* Get all names supported by this interface

> `listOfNames = axlDBDisplayControl(nil)`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
