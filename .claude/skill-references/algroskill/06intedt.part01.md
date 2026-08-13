<!--
source: algroskill/06intedt.md
part: 1/2
estimated_tokens: 13229
-->

### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

5
=

Interactive Edit Functions
==========================

Overview
--------

This chapter describes the basic database edit functions`axlDeleteObject` and `axlDBDeleteProp`. It also describes `axlShowObject`, which you can use to display the data about an object.

`axlDeleteObject` does not allow you to delete Allegro PCB Editor logical or parameter objects. Also, certain figure or property objects may be marked `readOnly`. `axlDeleteObject` ignores objects with that property. DRC markers created by Allegro PCB Editor are an example of `readOnly` Allegro PCB Editor figure objects. An AXL program cannot modify DRC objects directly.

AXL/SKILL Interactive Edit Functions
------------------------------------

This section lists interactive edit functions.

### axlBondFingerDelete

`axlBondFingerDelete(bondFingersdeleteWires)==> t/nil`

#### Description

Deletes the (list of) bond fingers passed in. Optionally, it will delete the connect bond wire elements as well.

#### Arguments

|  |
| --- | ---
| bondFingers | either a dbid or a list of dbids representing the bond fingers to be deleted.
| deleteWires | t/nil to tell the system whether it should remove any bond wires connected to the fingers.
#### Value Returned

Value is`t` returned, if one or more objects are deleted; otherwise the return value is `nil`.

### axlDeleteBondWire

`axlBondWireDelete(bondWiresdeleteFingers)==> t/nil`

#### Description

Deletes the (list of) bond wires passed in. Optionally, it will delete the connect bond finger elements as well.

#### Arguments

* **Value...**
* `dbid` or list of `dbid`, representing the bond wires to be deleted.
* `nil`:Connect bond fingers are not deleted
* `t`: Bond fingers connected to the wires are removed

#### Value Returned

Value is`t` returned, if one or more objects are deleted; otherwise the return value is `nil`.

### axlChangeLine2Cline

`axlChangeLine2Cline(lo_dbid/o_dbid)==> x_cnt/nil`

#### Description

Changes provided lines to clines. Lines not on an etch layer are ignored. If a line is converted to a cline then it may be assigned to a net, otherwise it will be left on a the standalone branch.

#### Arguments

|  |
| --- | ---
| `lo_dbid/o_dbid` | A single dbid or list of line dbids
#### Value Returned

`t` if succeeded, `nil` if failure

FAILURES: (for debug purposes set axlDebug(t) to see additional messages)

- dbid is not a line or a line on ETCH class

- line is LOCKED or FIXED

#### Examples

* Convert a line

> `res = axlDBCreateLine('(0:0 100:100) 5 "ETCH/TOP")`

> `res = car(res)`

> `cnt = axlChangeLine2Cline(res)`

#### See Also

[axlTransformObject](#821370 "5")

### axlChangeLineFont

`axlChangeLineFont(o_dbidx_newFont)==> lo_dbid/nil`

#### Description

Changes font on a line or segment.

#### Arguments

|  |
| --- | ---
| `o_dbid` | A line dbid
| `x_newFont` | The new font. The valid values are`'SOLID` `'HIDDEN` `'PHANTOM` `'DOTTED` `'CENTER`  `nil` is same as `SOLID`
|
#### Value Returned

FAILURES:

> > - dbid is not a cline, line or line/arc segment of a line/cline

> > - illegal option types

> > - transformed object is outside of database extents

#### Examples

* Changes the font of a line to hidden

> ```
> ; ashOne is a selection utility found at <cdsroot>/share/pcb/examples/skill/ash-fxf/ashone.il
> ```

> `dbid = ashOne()`

> `; pick a line, cline or segment (set find filter)`

> `updatedDbid = axlChangeLineFont(dbid 'hidden)`

#### See Also

[axlTransformObject](#821370 "5"), [axlChangeLayer](sipapd.html#1086782 "9")

### axlChangeWidth

`axlChangeWidth(lo_dbid/o_dbidf_newWidth[g_invisible])==> lo_dbid/nil`

#### Description

Changes width of lines, clines and segments (arc and line).

By default, only visible lines are changed. This allows layer filtering by temporary changing the visible layers (see example in[axlVisibleUpdate](19cmdctl.html#984586 "20")). If you wish to override this behavior then set the value of the optional variable `g_invisible` to `t`.

**Note:** If you need to change the width of multiple lines, it is more efficient to pass them as a list of`dbids` than to call this function for each `dbid`. This function does not support change in the width of shape borders.

#### Arguments

|  |
| --- | ---
| `lo_dbid/o_dbid` | Single`dbid` or list of `dbids`.
| `f_newWidth` | New width of line.
| `g_invisible` | If`t` objects do not need to be visible on the display to have their width changed.
#### Value Returned

List of width objects or`nil` if failed.

Failures:

* `dbid` is not a cline, line or line/arc segment of a line/cline.

* Illegal option types.

* Transformed object is outside of database extents.

#### Example

Changes the width of a cline to 20 in current database use units

> `; ashOne is a selection utility found at`

> `; <cdsroot>/pcb/examples/skill/ash-fxf/ashone.il`

> `dbid = ashOne()`

> `; pick a line, cline or segment (set find filter)`

> `updatedDbid = axlChangeWidth(dbid, 20.0)`

#### See Also

[axlTransformObject](#821370 "5"), [axlChangeLayer](sipapd.html#1086782 "9")

### axlCopyProperties

`axlCopyProperties(o_destDbido_srcDbid)==> t/nil`

#### Description

This copies properties from one object to another. It filters certain properties. If you need to copy properties suggest you utilize this interface instead doing it yourself.

Side effects may happen when properies are copied.

Properties filtered are:

* IDX family

* IDF\_OWNER

* CLIP\_DRAWING

* FIXED

* FIXED\_PRIVATE

* DYN\_SHAPE\_PRIORITY

* SUBNET\_NAME only if shape is not on ETCH

Also properties may not be copied if they do not meet the rules for the destination element (example not legal for element type).

Existing properties are maintained on destination object but they may be overridden by source object.

#### Arguments

|  |
| --- | ---
| `o_destDbid` | Destination for properties
| `o_srcDbid` | Source for properties
#### Value Returned

`t` if objects are dbids, `nil` if one or more object is not a dbid.

#### See Also

[axlCopyObject](#832061 "5")

### axlCopyObject

```
axlCopyObject(lo_dbid/o_dbid?move           l_deltaPoint?mirror         t/nil?angle          f_angle?origin         l_rotatePoint?allOrNone      t/nil?retainNet      t/nil)==> t/nil
```

**Description**

Use this function to copy the database object(s). This supports the same functionality as[axlTransformObject](#821370 "5") except it copies and transforms one or more objects.

One additional option supported is retainNet. This only applies to vias. If the value of this option is set to`t,` the net of the via is retained on copy, `nil` allows the via to connect to whatever it touches at the new location. In the board, pins are not supported.

* ***Properties and text attached to the database object are also copied. Alsosee [axlTransformObject](#821370 "5") cautions.***

#### Arguments

|  |
| --- | ---
| `lo_dbid/o_dbid` | a single dbid or list of dbids
| `l_deltaPoint` | optional move distance
| `mirror` | optional mirror object (see above table)
| `f_angle` | optional rotation angle
| `l_rotatePoint` | optional rotation point
| `allOrNone` | if t and a group of objects, transform must succeed on all objects or fail
| `retainNet` | t/nil (applies to vias only)
#### Value Returned

list of transformed objects or`nil` if failed.

* If you need to copy a group of objects the performance is much better if you call this function with the object group instead of passing each dbid individually.

#### Examples

ldbid = list of database objects

dbid = one database object

***Case 1***: Copy a set of objects 1000 database units vertically

`r = axlCopyObject(ldbid, ?move '1000.0:0.0)`

***Case 2***: Copy and rotate an object about its origin 45 degrees

`r = axlCopyObject(dbid, ?angle 45)`

***Case 3***: Copy and rotate an object about a rotate point

`r = axlCopyObject(dbid, ?angle 45 ?origin 100:100)`

#### See Also

[axlTransformObject](#821370 "5"), [axlDBCloak](17dbtran.html#1065349 "18"), [axlCopyProperties](#860810 "5")

### axlDBAltOrigin

`axlDBAltOrigin(g_modeo_dbid)⇒ xy/nil`

#### Description

Returns alternative center for a`dbid`. This provides Skill access to the `move` command's origin point option in the Options tab.

It is intended for symbols instances (it will convert a component instance to its symbol). Body origin rules for symbols, origin is the first rule that is met:

* the origin of text on the PACKAGE\_GEOMETRY/BODY\_CENTER layer

* the center of an extent box created by the union of all shapes on layers PACKAGE\_GEOMETRY (PLACE\_BOUND\_TOP, PLACE\_BOUND\_BOTTOM, DFA\_BOUND\_TOP, DFA\_BOUND\_BOTTOM) and EMBEDDED\_GEOMETRY (PLACE\_BOUND and DFA\_BOUND)

* center of the symbol bbox

Other Allegro figure`dbids` can be supplied, but all options may not be supported. For example, a CLINE supports the center option, but not `'origin`or `'pin1`.

#### Arguments

|  |
| --- | ---
| `g_mode` | The ``center` option returns the body center of an object.  The`` `origin `` option returns the origin of an object (normally if `dbid` has an `xy` attribute, this is the same coordinate).  For Symbols, the board origin can be set by the origin of text on the PACKAGE\_GEOMETRY/BODY\_CENTER layer.  The`` `pin1 `` option returns pin1 as center.
|
|
|
| `o_dbid` | A figure (geometric object)`dbid.`
#### Value Returned

|  |
| --- | ---
| `xy` | Location requested.
| `nil` | Not a`dbid`, `dbid` is not a figure dbid, or mode is not supported for that object.
#### See Also

[axlDBGetSymbolBodyExtent](25dbmisc.html#1095181 "26")

#### Example

The`;ashOne` utility is supplied in the examples Skill code.

`sym = ashOne()`

`; select symbol in Find filter and select a symbol`

`sym->xy`

`; prints (3503.0 1058.0)`

`axlDBAltOrigin('origin sym)`

`; prints (3503.0 1058.0) -- origin of symbol is same as xy`

`axlDBAltOrigin('center sym)`

`; prints (3250.0 1737.0)`

`axlDBAltOrigin('pin1 sym)`

`; prints (3503.0 1058.0) -- pin1 of symbol is same as its x`

### axlDBChangeText

`axlDBChangeText(o_dbidt_text[r_textOrientation/x_textBlock])==> l_result/nil`

#### Description

Modifies the characteristics of a text string in the layout. To keep current settings on the text, set the arguments,`t_text` and `r_textOrientation` to `nil`. To move text use the [axlTransformObject](#821370 "5") object.

**Note:** For renaming refdes this works the same as edit text in that it checks for the HARD\_LOCATION property and will not rename refdes if this property is present. If you want to ignore this property, use[axlRenameRefdes](26logacc.html#1075491 "30").

#### Arguments

|  |
| --- | ---
| `o_dbid` | Database ID of text
| `t_text` | Text string.  If the value of this argument is set to`nil`, current settings are retained on the text
| `r_textOrientation` | Orientation of text  The`nil` value indicates that current settings are to be retained on the text.  See[Structure](#835951 "5").
| `x_textBlock` | To be specified if only the text block is to be changed
#### *Structure*

The`axlTextOrientation` structure is as follows.

|  |
| --- | ---
| `defstruct axlTextOrientation` |
| `r_textOrientation ;` | orientation of text
| `textBlock;` | A string specifying the text block name
| `rotation;` | A floatnum variable specifying rotation in degrees
| `mirrored;` | Possible values are:  |  |  |  | | --- | --- | --- | |  |  | `t`: mirrored |  |  |  |  | | --- | --- | --- | |  |  | `nil`: not mirrored |  |  |  |  | | --- | --- | --- | |  |  | `GEOMETRY`: only geometry is mirrored. |
| `justify;` | Supported values:  |  |  |  | | --- | --- | --- | |  |  | left |  |  |  |  | | --- | --- | --- | |  |  | center |  |  |  |  | | --- | --- | --- | |  |  | right |
If any of these arguments is modified, then you need to provide values for all arguments. Arguments for which the values are not changed, copy the values from the existing text dbid.

**Note:** As with all SKILL defstructs, use constructor function,`make_axlTextOrientation` to create instances of `axlTextOrientation`. To copy instances of `axlTextOrientation`, use the copy function, `copy_axlTextOrientation`.

#### Value Returned

* defstruct not created
* (cadr) t if DRCs created or nil.
* (car) list of DBID of the text

* ***Do not pass text string with newlines as an argument.***

#### See Also

[axlTransformObject](#821370 "5"), [axlChangeLayer](sipapd.html#1086782 "9"), [axlRenameRefdes](26logacc.html#1075491 "30"), [axlTextOrientationCopy](#847294 "5")

#### Example

Example is text added in axlDBCreateText`text = car(ret)`

* Change text

`cret = axlDBChangeText(text "Chamfer neither sides")`

* Change text block

`cret = axlDBChangeText(text nil 4)`

* Change rotation and text

`axlTextOrientationCopy(text myorient)`

`myorient->rotation = 0.0`

`cret = axlDBChangeText(text "New text" myorient)`

### axlDeleteObject

`axlDeleteObject(o_dbid/lo_dbid[g_mode])⇒ t/nil`

#### Description

Deletes single or list of database objects from database.
Deletion of components deletes the symbol owner as well.
Deletion of nets is LOGIC only, and leaves the physical objects.

Command allows for rip-up of associated etch via the ripup option.

`axlDeleteObject(lo_dbid 'ripup)`

Except for Nets, objects will be erased before they are deleted. Only the Net's Ratsnests is erased. Other parts of a Net will not be erased because there is no ripup. If a Net is in a highlighted state, it will be dehighlighted.

Also allows deletion of the following parameter records:

* artwork (films)

> Both individual films can be deleted and all films If all films are deleted then next time the artwork dialog is opened then it will be auto-populated with the default films.

* subclasses

> subclasses must by empty and legal for deletion (cannot delete PIN subclasses).

In the case of deleting parameter records, the current restriction is to only pass that single object. Do not try to pass multiple parameter objects or to mix them with non-parameter objects.

#### Arguments

|  |
| --- | ---
| `o_dbid/lo_dbid` | `dbid`, or list of `dbids` to delete from layout.
| `g_mode` | optional delete options.'`ripup` - enable etch ripup option (same as Allegro delete ripup command ripup option)
#### Value Returned

|  |
| --- | ---
| `t` | Deleted one or more objects from the layout.
| `nil` | Deleted no objects from the layout.
* ***If passed component or net dbid will delete the logic. This is different from the Allegro`delete` command which will delete the physical objects associated with the logic (clines/vias for nets and symbols for components). To emulate the Allegro `delete` command behavior, select and then set objects selection using `axlSetFindFilter` with the `equivlogic` parameter passed to the `?enabled` option (See example below).***

#### Example

The following example loops on`axlSelect` and `axlDeleteObject`, deleting objects interactively selected by user. This could be dangerous because object is deleted without allowing *oops* (left as an exercise to the reader -- required use of `axlDBStartTransaction` and popup enhancement).

`(defun DelElement ()`

`let ((mypopup)`

`"Delete selected Objects"`

`mypopup = axlUIPopupDefine(nil`

`'(("Done" axlFinishEnterFun)`

`("Cancel" axlCancelEnterFun)))`

`axlUIPopupSet(mypopup)`

`axlSetFindFilter(?enabled '("ALL" "EQUIVLOGIC") ?onButtons '("ALL"))`

`while( axlSelect() axlDeleteObject(axlGetSelSet()))`

`axlUIPopupSet( axlUIPopupDefine(nil nil))`

`))`

The following deletes the TOP artwork film record

`p = axlGetParam("artwork:TOP")axlDeleteObject(p)`

The following deletes all films

`axlDeleteObject(axlGetParam("artwork"))`

### axlDeleteTaper

`axlDeleteTaper(o_dbid)==> t/nil`

#### Description

Deletes tapers

#### Arguments

|  |
| --- | ---
| `o_dbid` | dbid of Shape or PATH.
#### Value Returned

* `t` - indicates success

* `nil` - command failed

### axlDBDeleteProp

`axlDBDeleteProp(lo_attachlt_name)⇒ l_result/nil`

#### Description

Deletes the properties listed by name, in`lt_name`, from the objects whose `dbids` are in `lo_attach`.

#### Arguments

|  |
| --- | ---
| `lo_attach` | List of`dbids` of objects from which properties are to be deleted. `lo_attach` may be a single `dbid`. If `lo_attach` is `nil`, then the property is to be deleted from the design itself.
| `lt_name` | List of names of the properties to be deleted.`lt_name` may be a list of strings for several properties, or a single string, if only one property is to be deleted.
#### Value Returned

|  |
| --- | ---
| `l_result` | List.  (`car`) list of `dbids` of members of `lo_attach` that successfully had at least one property deleted.  (`cadr`) always `nil`.
| `nil` | No properties deleted.
#### See Also

[axlDBAddProp](03dbcre8.html#367701 "15")`,`[axlDBDeletePropAll](#827023 "5")

#### Example

```
axlDBCreatePropDictEntry(    "myprop", "real", list( "pins" "nets" "symbols"),    list( -50. 100), "level")axlClearSelSet()axlSetFindFilter(    ?enabled '("NOALL" "ALLTYPES" "NAMEFORM")    ?onButtons "ALLTYPES")axlSingleSelectName( "NET" "ENA2")axlDBAddProp(axlGetSelSet(), list("MYPROP" 23.5))axlShowObject(axlGetSelSet())
```

First defines the string-valued property`"myprop",` then adds it to the net `"ena2",` then deletes the property from the net.

The following**Show Element** form shows the net with `"MYPROP"` attached.

`axlDBDeleteProp(axlGetSelSet() list("myprop"))axlShowObject(axlGetSelSet())`

Using`axlDBDeleteProp`, deletes the attached property.

The following Show Element form shows the net with*MYPROP* deleted.

### axlDBDeletePropAll

`axlDBDeletePropAll(t_name)==> x_count/nil`

#### Description

Deletes all instances of the property t\_name in the database. This includes properties that exist on the symDef and compDef that cannot be access via the property edit command. If you delete a property that effects the DRC system, you may wish to wrap this call with a axlDBCloak for better performance.

#### Arguments

|  |
| --- | ---
| `t_name` | Name of property to have all its instances deleted.
#### Value Returned

|  |
| --- | ---
| `x_count` | Returns number of properties deleted
| `nil` | Error, property definition doesn't exist
#### See Also

[axlDBAddProp](03dbcre8.html#367701 "15")`,`[axlDBDeleteProp](#808739 "5")`,` and [axlDBCloak](17dbtran.html#1065349 "18")

#### EXAMPLE

Delete all fixed properties in database

`axlDBDeletePropAll("FIXED")`

### axlDBDeletePropDictEntry

`axlDBDeletePropDictEntry(t_name)==> t/nil`

`Description`

Deletes an unused user property definition. Property entry must be unused. The property definition must be a user property and its useCount (`axlDBGetPropDictEntry`) must be zero for you to delete it. Use `axlDBDeletePropAll` if property is in use.

`Arguments`

|  |
| --- | ---
| *t\_name* | String specifying the name of the user property dictionary entry to be deleted.
`Value Returned`

|  |
| --- | ---
| `t:` | Deleted the property definition.
| `nil` | Property is in use, is an Allegro property, property does not exist, or name is not legal.
#### See Also

[axlDBAddProp](03dbcre8.html#367701 "15")`,`[axlDBDeleteProp](#808739 "5")`,` and [axlDBCreatePropDictEntry](03dbcre8.html#367783 "15")

`EXAMPLE`

take property, myprop, created`axlDBCreatePropDictEntry`

`axlDBDeletePropDictEntry("myprop")`

### axlDBOpenShape

`axlDBOpenShape(o_shapeDbid/nil[o_polygon/r_path/nil][g_close])==> o_dbid/nil`

#### Description

Opens an existing shape to replace its boundary or to modify its voids.

Shape can be left open so you can update the voids within the shape. If only the outline needs to be replaced, you can close the shape as part of this call. The new outline cannot overlap existing voids or allow existing voids to exist outside the outline.

**Note:** A side-effect of opening an existing shape is the shape will be displayed as unfilled until it is closed.

#### Arguments

|  |
| --- | ---
| `o_shapeDbid` | dbid of shape to be modified. If dbid is nil then use the existing open shape
| `o_polygon` | new shape outline in polygon format
| `r_path` | new shape outline in r\_path format
| `g_close` | optional option to close the shape (t) boundary modification
#### Value Returned

|  |
| --- | ---
| o\_dbid | dbid of provided shape or nil if an error
#### See Also

[axlDBCreateCloseShape](03dbcre8.html#367549 "15"), [axlDBCreateOpenShape](03dbcre8.html#438449 "15"), [axlDBCreateVoid](03dbcre8.html#367581 "15"), [axlShapeDeleteVoids](#823700 "5"), [axlShapeAutoVoid](#851093 "5")

#### Examples

ashOne is a shareware utility that allows user to select an object (see`<CDSROOT>``/share/pcb/examples/skill/ash-fxf/ashone.il`)

* Select a shape and expand it by 100

> `shp = ashOne("shapes")`

> `edge = car( axlPolyFromDB(shp) )`

> `newedge = car( axlPolyExpand(edge 100.0 'NONE) )`

> `newshp = axlDBOpenShape(shp newedge t)`

* Select a void delete it

> `shp = ashOne("voids")`

> `edge = axlPolyFromDB(shp)`

> `newedge = car( axlPolyExpand(edge 100.0 'NONE) )`

> `newshp = axlDBOpenShape(shp newedge)`

> `q = axlDBCreateCloseShape(newshp)`

* Select a shape, delete all voids and contract boundary by 100

> `shp = ashOne("shapes")`

> `edge = car( axlPolyFromDB(shp) )`

> `newedge = car( axlPolyExpand(edge -100.0 'NONE) )`

> `newshp = axlDBOpenShape(shp nil)`

> `axlShapeDeleteVoids(shp)`

> `q = axlDBCreateCloseShape(newshp)`

### axlDeleteFillet

`axlDeleteFillet(o_dbid)⇒ t/nil`

#### Description

Deletes fillet associated with a PIN, VIA, T, or CLINE. The command also deletes a single fillet if`o_dbid` is a fillet shape.

When deleting via a cline, Allegro PCB Editor searches for the via/pin connections and deletes the fillets from that pin or via. It only deletes FILLETS on the layer of the CLINE. If deleting FILLETS from a PIN or VIA, it deletes FILLETS on all layers.

#### Arguments

|  |
| --- | ---
| `o_dbid` | `dbid` of a `PIN`, `VIA`, `PATH`, or `T`.
#### Value Returned

|  |
| --- | ---
| `t` | Fillet deleted.
| `nil` | No fillet deleted.
### axlFillet

`axlFillet (o_dbid)⇒ t/nil`

#### Description

Adds fillet between cline and pin/via, and at T. Removes and re-generates existing fillets. Fillet parameters are controlled from the Glossing**Pad and T Parameter** form.

#### Arguments

|  |
| --- | ---
| `o_dbid` | `dbid` can either be a `NET` or `CLINE`.
#### Value Returned

|  |
| --- | ---
| `t` | Fillet(s) added.
| `nil` | Error or no fillet added.
#### Notes

Pins, vias and Ts are not supported; use`axlDBGetConnect` on these objects to get a list of clines that connect.

For best performance, especially if fillets impact dynamic shapes, make a single call with the list of objects to be filleted.

#### Examples

`fillet new MEMDATA8`

`axlFillet(car(axlSelectByName("NET" "MEM_DATA8")))`

### axlFilletConvert

`axlFilletConvert(o_dbid) -> t/nilDescription`

#### Description

Converts a fillet or taper to a static shape.

This command should only be used if converting a design to another form such as if you are crafting a panelization solution.

* Dynamic fillets should be diabled when using this command.

Some of the side effects of using this command are:

* The converted fillets remain if etch is deleted/modified

* If dynamic fillets are enabled, a duplicate fillet appears.

* DRCs may occur because the converted fillet or taper uses shape spacing.

* Voiding other shapes may change.

* Etch length calculations may be effected.

* Etch editing may work differently on these traces.

#### Arguments

|  |
| --- | ---
| `o_dbid` | A fillet shape dbid.
#### Value Returned

`t` if the fillet is successfully converted to a static shape, `nil` if dbid is not a fillet shape.

#### See Also

[axlDeleteFillet](#861756 "5")

### axlGetLastEnterPoint

`axlGetLastEnterPoint ()⇒ l_point/nil`

#### Description

Gets the last pick location from`axlEnterPoint`.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `axlGetLastEnterPoint` | User pick from last call to`axlEnterPoint()`.
#### Example

Returned list for a pick:`(1000.000 2000.000)`.

### axlLastPick

`axlLastPick(l_mode) ⇒ xy`

#### Description

This returns the last processed cursor pick. You can snap to current grid (`l_mode` ) ⇒`t`) or leave it unsnapped. Position is returned in design units. The grid used depends on the active layer. A pick event causes the last pick. In Skill, a call to axlEnterPoint, axlEnterEvent, etc. may generate this. It allows switching from a snapped to an unsnapped event. If a user has made no pick since launching Allegro PCB Editor, then it returns `(0 0`).

#### Arguments

|  |
| --- | ---
| `l_mode` | `t` for snapped and `nil`for unsnapped.
#### Value Returned

|
| ---
| Last pick as an`xy` list.
**Examples**

`snappedPoint = axlEnterPoint(?prompts list("Pick origin point") ?gridSnap t)`

`unsnapped = axlLastPick(nil)`

### axlWindowBoxGet

`axlWindowBoxGet()⇒ l_bBox`

#### Description

Returns the bounding box of the Allegro PCB Editor window currently visible to the user, in design units.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `l_bBox` | bBox of the current Allegro PCB Editor window.
### axlWindowBoxSet

`axlWindowBoxSet(l_bBox)⇒ l_bBox/nil`

#### Description

Sets Allegro PCB Editor display to given bBox. Adjusts it according to the aspect ratio and returns the adjusted bBox.

#### Arguments

|  |
| --- | ---
| `l_bBox` | bBox for display change.
#### Value Returned

|  |
| --- | ---
| `l_bBox` | Adjusted bBox.
| `nil` | Invalid argument.
### axlReplacePadstack

`axlReplacePadstack (o_dbid/lo_dbido_padstackdbid/t_padname)⇒ lo_dbid`

#### Description

Replaces the padstack on a pin or via (or a list of them). Will not print any error messages unless you have argument errors.

The pin/via can be a list or a single`dbid`. Ignores items in the list that are not pins or vias.

The padstack can be referenced by name or a`dbid` and must be present in the Allegro PCB Editor database. Use `axlDBCreatePadStack` to obtain a `dbid`.

Returns a list of pins/vias that have had their padstacks changed. This may not be the same as your initial list as the software removes`dbids` that are not pins or vias and those items where changing the padstack would create a database error.

**Note:** This function will not change symbol definition pins.

* ***Changing the padstack on a pin in the drawing editor results in an exploded pin which increases your database size and impacts refresh\_symbol.

  Using this function can result in disconnects and new DRC violations.***

#### Performance Hints

To change all instances of a particular padstack, it is faster to change the padstack itself.

If you are changing many pins and vias to the same padstack, you can save time by calling this function with a list of pins/vias instead of calling it for each pin or via.

### axlPurgePadstacks

`axlPurgePadstack (S_modet/nil)⇒ x-cnt`

#### Description

Purges unused padstacks from the database in the area controlled by`S_mode` symbol.

`

|  |  |
| --- | --- | ---
| ****S\_mode symbol**** | **2nd arg =`t`** | **2nd arg =`nil`**
| `'padstacks` | Only purges unused derived padstacks. | Purges all unused padstacks.
| `'via` | Purges vias not found from all via list constraints under the physical rule set and purges vias not loaded in the database, but found by looking on the disk via the`PSMPATH` environment variable. | Purges vias not found from all the via list constraints under the physical rule set.  The`nil` option is NOT available from the Allegro PCB Editor user interface.
* For best results, first delete the unused padstacks from the database, then purge the via lists.

#### Arguments

|  |
| --- | ---
| `S_mode` | `'padstacks` or `'via`.
| `option` | `t`- purge unused derived padstacks  or  `nil` - purge all
|
|
#### Value Returned

|  |
| --- | ---
| `x_cnt` | Number of padstacks eliminated.
#### Examples

`axlPurgePadstacks('padstacks nil)`

`axlPurgePadstacks('via t)`

Emulates the default Allegro PCB Editor user interface behavior.

### axlShapeAutoVoid

`axlShapeAutoVoid(o_shapeId[s_options/ls_options])==> lo_shapeIds/nil`

#### Description

Autovoids a static shape using current static shape parameters to control voiding except where options provide an override. Voiding dynamic shapes or dynamically-generated shapes is not supported.

This function produces a file,`shape.log`, as a side effect of the autovoid.

Options:

* '`noRipThermals` - by default autovoid rips up all existing thermal ties in the shape and creates a new set, maintaining existing thermals.

* '`fragment` - by default, if shape fragments into multiple shapes, prompts you before proceeding. If you proceed, Allegro PCB Editor allows a silent fragment. Overrides setting in static shape parameter record.

* '`noFragment` - opposite of fragment. API fails if shape needs to be fragmented.

* ***Do not use this function to void shapes on negative planes. Artwork does not represent inside voiding.***

#### Arguments

|  |
| --- | ---
| `o_shapeId` | Voidable shape.
| `s_options` | Single option symbol (see above).
| `ls_options` | List of options (see above).
#### Value Returned

|  |
| --- | ---
| `lo_shapeId` | List of voided shape. Normally this is one shape unless shape is broken into multiple pieces.
| `nil` | Failed to void or illegal arguments.
#### See Also

[axlShapeDeleteVoids](#823700 "5")

#### Examples

See`<cdsroot>/share/pcb/examples/skill/ash/ashshape.il`

`axlShapeAutoVoid(shapeDbid '(noRipThermals fragment))`

### axlShapeChangeDynamicType

```
axlShapeChangeDynamicType(o_shapeIdg_dynamicg_msgs) -> o_dynShapeId/l_staticShapeId/nil
```

#### Description

Swaps a connectivity shape from static to dynamic or the reverse. This offers the same functionality as the Allegro PCB Editor command`shape change type`.

Notes:

* Voids in static are deleted when shape is converted to dynamic.

* Converting a dynamic shape to static can result in the loss of the original boundary since Allegro PCB Editor converts the generated shapes (on ETCH) to static shapes not boundary shapes.

* Shapes converted to static maintain voids.

* Filled rectangles are supported on ETCH, converted to a shape.

* If changing the type of multiple shapes or doing multiple operations on a single shape (for example, convert then raise priority) consider wrapping the code in`axlDBCloak` to batch updates.

#### Arguments

|  |
| --- | ---
| `o_shapeId` | Dynamic shape id or static id.
| `g_dynamic` | `t` makes the shape dynamic, `nil` makes the shape static.
| `g_msgs` | `t` issue error messages if failed to convert; else be silent
#### Value Returned

|  |
| --- | ---
| `nil` | Failure.
| `o_dynShapeId` | `dbid` of the dynamic shape converted from static.
| `l_staticShapeId` | List of static shapes converted from dynamic shapes.
#### See Also

[axlShapeChangeDynamicType](#823379 "5")

#### Examples

See`<cdsroot>/share/pcb/examples/skill/axlcore/ashshape.il`

Change to dynamic shape with messages:

> `ret = axlShapeChangeDynamicType(shape t t)`

Change to static shape; no messages

> `ret = axlShapeChangeDynamicType(shape nil nil)`

### axlShapeDeleteVoids

`axlShapeAutoVoid(o_shapeId/o_voidId/lo_voidid) -> t/nil`

#### Description

Lets you delete voids in a shape. Supports the following three forms of arguments:

* Shape that deletes all voids in that shape

* Delete single void

* Delete list of voids

Non-voids in list of voids options are silently ignored. You cannot delete the voids that are a part of auto-generated shapes.

If you are making a series of modifications to a shape, such as, deleting and adding voids or changing the shape boundary, then for best performance, it is recommended that you wrap your calls in[axlDBOpenShape](#832168 "5") and [axlDBCreateCloseShape](03dbcre8.html#367549 "15").

#### Arguments

|  |
| --- | ---
| `o_shapeId` | Given a shape; deletes all voids associated with that shape.
| `o_voidId` | Deletes the given void.
| `lo_voidid` | Deletes the list of voids.
#### Value Returned

|  |
| --- | ---
| `t` | Deletes voids.
| `nil` | Error.
#### See Also

[axlShapeAutoVoid](#851093 "5"), [axlDBOpenShape](#832168 "5"), [axlDBCreateCloseShape](03dbcre8.html#367549 "15")

#### Examples

See`<cdsroot>/share/pcb/examples/skill/axlcore/ashshape.il`

Assuming you have shape`dbid` (`shapeId`):

* Delete a single void

> `axlShapeDeleteVoids(car(p->voids))`

* Delete all voids in shape except first:

> `axlShapeDeleteVoids(cdr(p->voids))`

* Delete all voids in the shape:

> `axlShapeDeleteVoids(p)`

### axlShapeDynamicUpdate

`axlShapeDynamicUpdate(o_shapeDbid/nilg_force) -> x_ood/nil`

#### Description

Updates a dynamic shape, or if`nil`, all dynamic shapes are updated. This ignores the current dynamic shape mode setting of the design.

By default, only updates the shape if it is out of date unless`g_force` is `t`. In this case, it updates the shape. If `g_force` is `nil` the shape is only updated if `dbid->fillOOD` is `t`. This function supports shapes whose `dbid->shapeIsBoundary` is `t`. Updating a dynamic shape includes voiding, artwork smoothing, and thermal relief generation.

#### Arguments

|  |
| --- | ---
| `o_shapeDbid` | `dbid` a dynamic shape.
| `g_force` | Force shape to update even if it is up to date.
#### Value Returned

|  |
| --- | ---
| `x_ood` | If updating all returns count of all shapes that failed in updating. If single shape returns`0`; update successful, `1` otherwise.
| `nil` | Return if there is an error;`dbid` is not a dynamic shape.
#### Examples

Force update of one dynamic shape:

> `axlShapeDynamicUpdate(shapeId, t) -> 0`

Update all shapes`ood:`

> `axlShapeDynamicUpdate(nil nil) -> 0`

### axlShapeRaisePriority

`axlShapeRaisePriority(o_shapeId) -> x_priority/nil`

#### Description

Raises the voiding priority of a dynamic shape (`o_shapeId`) to the highest on the chosen layer. If this shape overlaps other dynamic shapes on the layer, the other shapes void away from this shape.

The priority number is relative. Allegro PCB Editor adjusts the numbers, as necessary. You should only use the priority number for comparison with other dynamic shape priority numbers.

For a dynamic shape (those on CLASS=BOUNDARY) the attribute priority reflects the current priority (for example,`dbid->priority`).

* If raising priority on multiple shapes or doing multiple operations on a single shape (for example, convert; then raise priority) consider wrapping the code in`axlDBCloak` to batch updates.

#### Arguments

|  |
| --- | ---
| `o_shapeId` | Dynamic shape id.
#### Value Returned

|  |
| --- | ---
| `x_priority > 0` | New priority of shape.
| `-1` | Already at highest priority.
| `nil` | Not a dynamic shape.
#### See Also

[axlShapeChangeDynamicType](#823379 "5")

#### Example

See`<cdsroot>/share/pcb/examples/skill/axlcore/ashshape.il`

> `axlShapeRaisePriority(shape)`

### axlShapeMerge

```
axlShapeMerge(o_shapeIdlo_shapesg_options/lg_options) -> o_dynShapeId/l_staticShapeId/nil
```

#### Description

This merges shapes. Shapes must be overlapped without the fixed property to merge. All merging shapes (`lo_shapes`) must overlap the primary shape (`o_shapeId`).

Supports merging db types; shapes, rectangle and filled rectangles.

The resulting shape will take on the characteristics of the first shape. This includes shape type and properties. Any properties on the secondary shapes are lost.

* If changing type of multiple shapes or doing multiple operations on a single shape (e.g. convert then raise priority) consider wrapping the code in axlDBCloak to batch updates.

#### Arguments

|  |
| --- | ---
| `o_shapeId` | dynamic shape id or static id.
| `g_dynamic` | `t` make shape dynamic, `nil` make static
| `g_options` | Available options are:  `check` - do not merge only perform checks for merging  `'quiet` - do not output any messages
#### Value Returned

* `nil`: indicates failure

* `o_dynShapeId`: the dbid of the dynamic shape that was converted from static

* `l_staticShapeId`: list of static shapes that was converted from a dynamic shape.

#### See Also

[axlShapeChangeDynamicType](#823379 "5")

#### Example

ashOne is a shareware utility that allows user to select an object (See`<cdsroot>``/share/pcb/examples/skill/ash/ashshape.il)`

* Merge two shapes; interactively select two shapes that overlap

`s1 = ashOne("shapes")`

`s2 = ashOne("shapes")`

`shapeResult = axlShapeMerge(s1 s2 'quiet)`

### axlShoveItems

`list`

`axlShoveItems(l_itemList)⇒ t/nil`

#### Description

Takes a list of`dbids` and shoves them according to the parameters set using `axlShoveSetParams`.

#### Arguments

|  |
| --- | ---
| `l_itemList` | List of`dbids` (clines, pins, or vias) to be shoved.
#### Value Returned

|  |
| --- | ---
| `t` | One or more items shoved.
| `nil` | No items shoved.
**Note:** Pins and vias are not shoved, but the clines around them are shoved in an attempt to eliminate any DRCs between the pin/via and the cline.

The list of`dbids` passed in does not reflect the results of the shove, as the original item may be deleted and/or replaced.

#### Example

`(defun ShoveElement ()`

`axlSetFindFilter (?enabled '("CLINES" "VIAS")`

`?onButtons '("CLINES" "VIAS"))`

`axlSelect()`

`axlShoveItems (axlGetSelSet())`

`)`

Shoves an item (or items) interactively selected by the user.

### axlShoveSetParams

`axlShoveSetParams(l_params)⇒ t/nil`

#### Description

Sets the parameters used for shoving by the`axlShoveItems`. If you do not provide all values, the indicated default is used.

#### Arguments

|  |
| --- | ---
| `l_params` | List of parameters of the form:
`(shoveMode cornerType gridded smooth oop samenet)`

`ShoveMode` is an integer as shown:

1. **Description**
2. hug preferred - Items passed in try to mold around items they are in violation with (default)
3. shove preferred - Items passed in try to shove items they are in violation with.

`CornerType` is an integer as shown:

1. **Description**
2. 90 degree corners.
3. 45 degree corners.
4. Any angle corners.

`Gridded` is an integer as shown:

1. **Description**
2. Ignore grids (default)
3. Perform shoves on grid.

`Smooth` allows smoothing of shoved traces and is an integer as shown:

1. **Description**
2. No smoothing (default)
3. Minimal smoothing.
4. More smoothing.
5. Still more smoothing.
6. Full smoothing.

`Oops` allows aborting the shove of DRCs result and is an integer as shown:

1. **Description**
2. `Oops` off (default)
3. `Oops` if drcs are left over.

`Samenet` tests for samenet violations.

**Note:** This results in a post-shove check for drcs that is meaningful only if you also set`oops` to the `"oops if drcs"` value.

1. **Description**
2. No`samenet` tests (default).
3. Enable`samenet` DRC checking.

#### Value Returned

|  |
| --- | ---
| `t` | Shove parameters set.
| `nil` | No shove parameters set.
#### Example

`(defun SetParams ()`

`(let (params (shoveMode 1) (cornerType 45) (gridded 1))`

`params = list(shoveMode cornerType gridded)`

`axlShoveSetParams(params)`

`))`

Sets shove parameters to shove preferred, 45 degree mode, and snap to grid.

### axlSmoothDesign

`axlSmoothDesign(lx_numPasses) -> x_change`

#### Description

Smooths the entire design. For good results on complicated designs, multiple passes are necessary. Since changes in one pass may open space that can be used in the next pass. Suggest 3 is a typical number although very complex designs can benefit from a higher number of passes. But the more passes the longer it will take.

#### Arguments

|  |
| --- | ---
| `lx_numPasses` | list of number of passes to perform
#### Value Returned

`x_change`, number of items changed

#### Example

Smooth design using 3 passes

`axlSmoothSetParams(list("45" -1.0 "0" 10.0 0))`

`res = axlSmoothDesign(list(3))`

#### See Also

[axlSmoothSetParams](#832247 "5")

### axlSmoothItems

`axlSmoothItems (lo_clineList) ==> (x_list`

#### Description

Takes a list of dbids representing clines and/or cline segments and smooths them according to the parameters set using the[axlSmoothSetParams](#832247 "5")() function.

#### Arguments

|  |
| --- | ---
| `lo_clineList` | List of dbids representing clines and/or cline segments to be smoothed.
#### Value Returned

This function returns a list containing the number of clines that were changed by the smoothing process and the list of changed items. The format is as follows:

`(x_change (o_dbid1 o_dbid2 o_dbid3))`

> > Where`x_change` indicates the number of items changed, or `-1` if a user interrupt occurred.
> > If an error occurs, the function will return `nil`.

#### Example

* Smooth a set of clines

`clines = <list of ...>`

`axlSmoothSetParams(list("45" -1.0 "0" 10.0 0))`

`res = axlSmoothItems(clines)`

#### See Also

[axlSmoothSetParams](#832247 "5")

### axlSmoothSetParams

`axlSmoothSetParams(l_params) ==> t/nil`

#### Description

Sets the parameters used for smoothing the routes. All parameters must be supplied but a nil as a parameter option will leave the existing setting.

The smooth functionality is provided on an "as-is" basis. It works well on many designs but has the following restrictions:

* not differential pair aware.

* may have issues with electrically constrained nets

* See[axlDBIgnoreFixed](14dsnctl.html#715890 "14") if you want to temporary disable FIXED testing.

#### Arguments

|  |
| --- | ---
| `l_params` | List containing the parameters, the list is of the following format.
* `(cornerType maxCornerLength padEntryRestriction minPadEntryLength sortDirection)`
* Can be one of the following string values:
* for 90 degree corners
* for 45 degree corners
* for any angle corners
* for arc corners
* This is an integer value indicating the maximum length of a bubble or jog in dbunits. A negative value indicates UNLIMITED.
* Can be one of the following string values:
* Indicates that there are no restrictions
* Indicates that all pad entry segments be fixed
* Indicates that the entry segments for all rectangular pads be fixed
* This is an double value indicating the minimum length of fixed pad entry segments in user units. If a pad entry segment is longer than this length, it will be broken at or near that point so that smoothing can occur on that segment. A negative value indicates UNLIMITED. This value is not applicable if padEntryRestriction is "2".
* This indicates how the clines are to be sorted before smoothing begins. This can be one of the following integer values:
* No sorting.
* Sort from the North.
* Sort from the NorthEast.
* Sort from the East.
* Sort from the SouthEast.
* Sort from the South
* Sort from the SouthWest
* Sort from the SouthWest
* Sort from the NorthWest

#### Value Returned

`t` if successful, `nil` if not.

#### Example

* set params

`axlSmoothSetParams(list("45" -1.0 "0" 10.0 0))`

* Update cornertype to 90

`axlSmoothSetParams(list("90" nil nil nil nil))`

#### See Also

[axlSmoothItems](#832246 "5"), [axlSmoothDesign](#832245 "5"), [axlDBIgnoreFixed](14dsnctl.html#715890 "14")

### axlSymbolAttach

`axlSymbolAttach(o_symInstDbido_dbid/lo_dbid)==> t/nil`

#### Description

Attaches an object or list of objects to symbol instance. For etch objects, provides the ability to associate pin escapes with a symbol.

Attach/detach rules:

* For detaching, object must be linked to the symbol instance provided. For attaching, the object can not be linked to any other symbol.

* If text appears of a REFDES class, it can't be linked or unlinked

* Linking or unlinking non-etch objects cause them to be deleted or duplicated if refresh symbol is run. Etch objects is more fully supported by refresh symbol.

* CLINES, LINES, SHAPES, RECTS, FRECTS and TEXT are supported with the layer limits noted below:

|  |  |
| --- | --- | ---
|  |  | Items on BOUNDARY class items are NOT supported.
|  |  |
| --- | --- | ---
|  |  | Shapes cannot be dynamic or generated from a dynamic shape.
|  |  |
| --- | --- | ---
|  |  | Objects cannot be on the DRC class.
* ***Running refresh\_symbol may result in deletion of design level attachments.***

#### Arguments

|  |
| --- | ---
| `o_symInstDbid` | symbol instance
| `o_dbid` | dbid to assign to symbol
| `lo_dbid` | list of dbid to assign to symbol
#### Value Returned

|  |
| --- | ---
| `t` | was able to change object
| `nil` | otherwise
#### See Also

[axlSymbolDetach](#853787 "5")

#### Example

Examples use ashOne which is a shareware utility that allows user to select an object (see`<cdsroot>/share/pcb/examples/skill/ash-fxf/ashone.il`)

* Attach an object to a symbol:

> `symdbid = ashOne("SYMBOLS")`

> `dbid = ashOne("NOALL")`

> `ret = axlSymbolAttach(symdbid dbid)`

### axlSymbolDetach

`axlSymbolDetach(o_symInstDbido_dbid/lo_dbid/g_mode)==> t/nil`

#### Description

Remove an object from a symbol instance. This function unlinks objects from the given symbol instance.

For pin escapes, two special modes are provided to detach all or most symbol etch from a given symbol instance.

It only unlinks an object from a symbol if it matches the provided symbol instance.

See[axlSymbolAttach](#853770 "5") for the rules.

* ***Running refresh\_symbol result results in duplicate objects as the detached objects are loaded again.***

#### Arguments

|  |
| --- | ---
| `o_symInstDbid` | symbol instance to modify.
| `o_dbid` | dbid to unlink from symbol
| `lo_dbid` | list of dbids to unlink from symbol
| `g_mode` | special modes for unlinking all "etch" from symbol
|  |  |
| --- | --- | ---
|  |  | `'allEtch` - deassign all etch from symbol
|  |  |
| --- | --- | ---
|  |  | `'allClineVia` - design all etch except for shapes from symbol
#### Value Returned

|  |
| --- | ---
| `t` | was able to change symbol
| `nil` | Otherwise
#### See Also

[axlSymbolAttach](#853770 "5")

#### Example

Examples use ashOne which is a shareware utility that allows user to select an object (see`<cdsroot>/share/pcb/examples/skill/ash-fxf/ashone.il`)

* Typical method: To get the symdbid from the object:

> - if etch

> > `symdbid = dbid->symbolEtch`

> - if nonetch

> > `symdbid = dbid->parent`

> > `symdbid = ashOne("SYMBOLS")`

> > `dbid = ashOne("NOALL")`

> > `ret = axlSymbolDetach(symdbid, dbid)`

* Deassign all etch from symbol except shapes

> `symdbid = ashOne("SYMBOLS")`

> `ret = axlSymbolDetach(symdbid, 'allClineVia)`

### axlAddTaper

`axlAddTaper(o_dbid/lo_dbid)==> t/nil`

#### Description

Adds tapered trace. Tapered trace parameters are controlled from the Glossing "Pad and T" Parameter form.

#### Arguments

|  |
| --- | ---
| `o_dbid` | dbid can either be a Path (CLINE) or line (segment).
#### Value Returned

* `t`, returned when the function call is successful

* `nil`, indicates failure

### axlTextOrientationCopy

`axlTextOrientationCopy(o_textDbid[orient]) -> orient/nil`

#### Description

This is a convenience function that updates a TextOrientation defstruct based upon a text dbid. This is typically used with axlDBCreateText or[axlDBChangeText](#832157 "5").

#### Arguments

|  |
| --- | ---
| `o_textDbid` | text dbid
| `orient` | optional existing defstruct, if`nil` will create a new defstruct
#### Value Returned

* `orient`, update TextOrientation defstruct

* `nil`, if there are error in the arguments

#### See Also

[axlDBChangeText](#832157 "5")

### axlTransformObject

```
axlTransformObject(lo_dbid/o_dbid?move     l_deltaPoint?mirror     t/nil/'GEOMETRY?angle     f_angle?origin     l_rotatePoint?allOrNone     t/nil))⇒ lo_dbid/nil
```

#### Description

Moves, rotates, and/or spins one object or a list of objects. Each Allegro PCB Editor database object has a legal set of transforms (see[Table 5-1](#846554 "5")). If the object does not accept a transform, then that transform is silently ignored.

If multiple transformations are applied, the order used is:

* move

* mirror

* rotate

If`allOrNone` flag is set, then the entire transformation fails when one object's transformation fails. By default, one object's failure does not stop the transformation on the other objects. A failure is a database failure. For example, a move that puts an object outside of the database extents is a database failure. Attempting an illegal transform is NOT a failure. If one or more objects are not transformed, there is no failure.

****Table 5-1****
**Supported Transforms**

| **OBJECT** | **MOVE** | **MIRROR** | **GEOMETRY** | **ROTATE** | **SPIN** | **ORIGIN (5)** | **NOTES**
| segments | `X` | `X` | `X` | `X` |  | `box` |
| `cline` | `X` | `X` | `X` | `X` |  | `box` |
| `line` | `X` | `X` | `X` | `X` |  | `box` |
| `symbol` | `X` | `X` |  | `X` |  | `xy` |
| `shape` | `X` | `X` | `X` | `X` |  | `box` |
| `text` | `X` | `X` | `X` | `X` |  | `xy` |
| `pin` | `X` |  |  | `X` |  | `xy` | 3,4
| `via` | `X` | `X` | `X` | `X` |  | `xy` |
| rat\_t | `X` |  |  | `X` |  | `xy` |
| group | `X` | `X` | `X` | `X` |  | `xy` | 7
#### Notes

* If object is not listed, then it is not supported.

* If object has attached text, it also has the transformation applied.

* Mirror occurs within the same class. See mirror rules.

* Symbol is exploded and`refresh_symbol` does not maintain transformation.

* For Pins on a board to be transformed, the`UNFIXED_PINS` either must be present on the drawing or on the symbol owning the pin.

* `ORIGIN` column shows what rotate/mirror uses when operating on a single object without the origin option. For box, the `dbid` does not have an origin and it uses the center of its bounding box `(dbid->bBox)`. For an `xy` object that has an origin `(dbid->xy)`, it rotates about the origin. For further discussion, see the note 9 on angles.

* This API rejects objects whose owner is a symbol definition

* The only groups that support a transform are user and module group types.

* If mirror is`t` then we mirror in x-direction AND across subclasses. For example, if object is on ETCH/TOP it will be mirrored both in x and to layer ETCH/BOTTOM. If mirror is `GEOMETRY only a x-direction is done and the object remains on its layer.

* Rotation (angle option) works as follows:

* Positive angle results in a counter-clockwise rotation.

* If just angle is provided, then the object is rotated about its origin point. If the`dbid` has no origin, then the center of its bounding box is used. If a list of `dbids` is provided, then the rotation always occurs about the center of the object set.

* You can provide a rotation origin.

> > `(?origin l_rotatePoint).`

> > This point is then used as the rotation point.

#### Cautions

* More objects may be added in the future. For example, voids.

* The return list may be changed to show the actual set of objects that were transformed.

* Spin (rotate a list of objects about each of their centers) is not supported. Use`axlTransformObject` for each object in the list.

* If you pass a list containing a symbol and pins of the symbol, you get unexpected results.

* If transforming multiple objects, enclose this operation in an axlDBCloak call.

* If transforming a segment, it will have a new owning path`dbid`.

#### Arguments

|  |
| --- | ---
| `lo_dbid`/`o_dbid` | Single`dbid` or a list of `dbids`.
| `l_deltaPoint` | Move distance.
| `mirror` | Mirror object (see table)
| `f_angle` | Rotation angle.
| `l_rotatePoint` | Rotation point.
| `allOrNone` | If`t` and a group of objects, transform must succeed on all objects, or fail.
#### Value Returned

|  |
| --- | ---
| `lo_dbid` | List of transformed objects.
| `nil` | Failure due to one of the following:
|  |  |
| --- | --- | ---
|  |  | An object can't be transformed (for example, a net)
|  |  |
| --- | --- | ---
|  |  | An object is fixed or a pin does not have an`UNFIX_PINS` property.
|  |  |
| --- | --- | ---
|  |  | Illegal option types used.
|  |  |
| --- | --- | ---
|  |  | Transformed object is outside of the database extents.
* For better performance when transforming a group of objects, call this function with the object group instead of passing each`dbid` individually.

#### See Also

[axlDBCloak](17dbtran.html#1065349 "18"), [axlCopyObject](#832061 "5")

#### Examples

`dbid` represents one database objects.

`ldbid` represents a list of database objects.

#### Example 1

`axlTransformObject(ldbid, ?move '(100.0 0.0))`

Moves a set of objects`100` database units vertically.

#### Example 2

`axlTransformObject(dbid ?angle 45)`

Rotates an object about its origin`45` degrees.

#### Example 3

`axlTransformObject(dbid ?angle 45 ?origin 100:100)`

Rotates an object about a rotation point.

Padstack Access Functions
-------------------------

This section lists padstack access functions.

### axlDBCreatePadStack

`axlDBCreatePadStack(t_namer_drilll_pad[g_nocheck])⇒ l_result/nil`

#### Description

Adds a padstack`t_name`, using drill hole `r_drill` and pad definition `l_pad`.

#### *Defstructs used to create padstack*

Drill`(r_drill)` use `make_axlPadStackPad`. Elements are:

