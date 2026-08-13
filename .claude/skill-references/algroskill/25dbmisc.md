### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

26
==

Database Miscellaneous Functions
================================

Overview
--------

This chapter describes the AXL-SKILL functions that do not fit into other sections.

### axlAirGap

```
axlAirGap(o_item1DBIDo_item2DBID/l_xy[t_layer]/nil[s_mode])==> l_airGapData/nil/(s_error l_airGapData/l_errorData)
```

#### Description

Finds the air gap and location between two given items. Gap is the same as reported by the`show measure` command. Any geometric objects; logical, group or symbols not supported (same as show measure). Unfilled shapes are currently treated as filled but this may change in the future.

You only need to provide a layer option when measuring between to pin or vias (also called pad comparison). When doing pad comparison without the layer, we use the current active layer. The layer syntax should either be "ETCH/<subclass>" or "<subclass>".

For spacing to the special via or pin subclasses below, either provide "PIN or "VIA CLASS" as the class name.

* SOLDERMASK\_TOP

* SOLDERMASK\_BOTTOM

* PASTEMASK\_TOP

* PASTEMASK\_BOTTOM

* FILMMASKTOP

* FILMMASKBOTTOM

Both of these class names work equally well with pins and vias. If you want the soldermask top spacing between a pin and via, then use "PIN/SOLDERMASK\_TOP".

The second argument may be a location (in design units). Gap reports the minimum distance from the first object to this location. In enhanced mode, the location is reported as the "ETCH/TOP" layer.

Output data appears in one of the following formats depending on the`s_mode` option:

* Default is`s_mode (s_mode==nil)` returns the `l_airGapData` or a `nil` if there is an error. If `s_mode` is `t` then data is returned as `(s_error l_airGapData)` where `s_error` is one of the following:

* `Success (t (l_airGapData))`
* No subclass matches between pin or via and object. Returns object's layer. (`NOMATCH (t_layer)`)
* No subclass match between two etch elements (one or both must be a pad element (pin or via). If common layers exist, Allegro PCB Editor returns the top and bottom layer where matches exist otherwise returns`nil`: (`ETCH (t_topMatch t_bottomMatch)`)
* it is an error in s\_mode=nil or s\_mode=t
* in anyLayer mode we will return the distance between the closest pad layers.

* *PROGRAMMING TIP:*For legacy purposes, this interface does not return an air gap if the two objects do not share the same layer. If you want the air gap any layer use `s_mode = 'anyLayer` or `s_mode ='enhanced`.

#### Arguments

* `dbid` of the first item.
* `dbid` of the second item.
* The second item can be a xy location in design units and must be in the design extents.
* Optional layer used to resolve gap comparison between two pin or via elements.
* If in 'anyLayer or 'enhanced mode this targets a particular layer for comparison. It is most useful in measuring mask layer gaps.
* Return additional info to clarify error. This may be:
* `enhanced`: return disembodied property list of additional air gap criteria (see above)
* `nil:`Default mode (objects must be on same layer)
* `t`: `("full mode") return l_airGapData` or if not share see above (objects must be on same layer)
* `anyLayer`: support any layer measure return just gap

#### Value Returned

|  |
| --- | ---
| `l_airGapData` | List containing the following items:
|  | (l\_airGapPt1 l\_airGapPt2 f\_airGapDistance)
where:

|  |
| --- | ---
| `l_airGapPt1` | (X,Y) point on the 1st item where the gap is measured.
| `l_airGapPt2` | (X,Y) point on the 2nd item where the gap is measured.
| `f_airGapDistance` | Distance between the two points.
| `nil` | Input data error; element 1 and 2 are the same or no air gap can be computed between the two items. If`t_layer` is used but does not specify an etch layer.
| `s_error` | See error symbols listed above.
#### Examples

Basic input:

> `axlAirGap(el1 el2)`

> `-> ((1337.5 1100.0) (1362.5 1100.0) 25.0)`

Basic input layer:

> `axlAirGap(el1 el2 "TOP")`

> `-> ((1337.5 1100.0) (1362.5 1100.0) 25.0)`

Full output success:

> `axlAirGap(el1 el2 nil t)`

> `-> (t ((1337.5 1100.0) (1362.5 1100.0) 25.0))`

Any layer airgap:

> `q = axlAirGap(el1 el2 nil 'anyLayer)`

Enhanced output:

> `q = axlAirGap(el1 el2 nil 'enhanced)`

Obtain soldermask spacing

> `axlAirGap(el1 el2 ""PIN/SOLDERMASK_TOP" )`

> `-> (((1337.5 1100.0) (1362.5 1100.0) 40.0))`

Obtain spacing to design origin

> `q = axlAirGap(el1 0:0 nil 'enhanced)`

Full output failure:

> `axlAirGap(el3 el2 nil t)`

> `-> (RANGE ("TOP" "GND"))`

### axlBackDrill

`axlBackDrill(o_dbids_layer) -> l_result/nil`

#### Description

This interface is obsolete. Use[axlBackdrillGet](07dbaccs.html#739500 "6") to retrieve actual backdrilling of pins and vias. Data returned by this interface may not match the actual backdrill results in the design.

Does a backdrill analysis on a given pin or a via (`o_dbid`) where the backdrill should start on top or bottom (`s_layer`).

**Note:** This is a tier limited feature.

#### Arguments

* **Valid Values**
* via
* pin
* bottom
* top

#### Value Returned

* argument specified is not a pin or a via
* This feature is not available in this editor
* a disembody property list see above for description

### axlDBGetLength

`axlDBGetLength(o_dbid)==> f_etchlength/nil`

#### Description

Calculates the length of the given object which may be a NET, CLINE, SEGMENT, or RATSNEST. If RATSNEST returns the Manhattan length. If a net is partially routed, includes sum of all ratsnest Manhattan lengths.

Currently does not include VIA-Z or PIN\_DELAY in its calculation.

#### Arguments

`o_dbid` `dbid`

#### Value Returned

`nil` Not a legal object

`f_etchLength` Length of object

#### See Also

[axlDBGetManhattan](#1077976 "26"), [axlDBPinPairLength](#1095182 "26")

#### Example

`Skill> p = ashOne()`

`Skill> axlDBGetLength(p)`

`-> 2676.777`

### axlDBGetManhattan

`axlDBGetManhattan(o_dbid_net)⇒ l_result/nil`

#### Description

Given a net, calculates an etch, path, and Manhattan length. The result is the same as that used by list element.

* Etch - The current length of etch. The length is 0 when there is no etch.

* Path - The etch plus remaining length. When the net is fully connected, there is no remaining, and path is equal to etch.

* Manhattan - The estimated routing length.

**Note:** Path is equal to Manhattan when the net has no etch.

#### Arguments

|  |
| --- | ---
| `o_dbid` | Net`dbid`.
#### Value Returned

|  |
| --- | ---
| `l_result` | `(``etchLength path manhattan`)
| `nil` | Not a net`dbid`.  Net is out of date.  No ratsnest.
See Also

[axlDBGetLength](#1081218 "26")

**Example**

> `p = ashOne()`

> `axlDBGetManhattan(p)`

> `(2676.777 3300.0)`

### axlDBGetSymbolBodyExtent

`axlDBGetSymbolBodyExtent(o_dbid)-> bBox/nil`

#### Description

This returns the body extent of a symbol. Unlike the bBox associated with a dbid, a body extents is either one of the following.

* the extent box created by the union of all shapes on layers PACKAGE\_GEOMETRY (PLACE\_BOUND\_TOP, PLACE\_BOUND\_BOTTOM, DFA\_BOUND\_TOP, DFA\_BOUND\_BOTTOM) and EMBEDDED\_GEOMETRY (PLACE\_BOUND and DFA\_BOUND)

* the symbol bbox, a union of all items in symbol

The symbol instance extent box is based upon the design origin while the symdef box is based upon the symbol origin.

#### Arguments

|  |
| --- | ---
| `o_dbid` | A symbol instance or definition
#### Value Returned

|  |
| --- | ---
| `bBox` | body box of symbol`(minX:minY maxX:maxY)`
| `nil` | dbid is not a symbol instance (symbol) or definition (symdef)
#### See Also

[axlDBAltOrigin](06intedt.html#825701 "5")

### axlDBPinPairLength

`axlDBPinPairLength(o_pin1o_pin2)==> f_etchlength/nil`

#### Description

Calculate the shortest length between 2 pins. Pins must be on the same xnet. The pin can also be a VIA or RAT\_T. If the distance is not fully routed, it includes a Manhattan estimate of the unrouted portion.

Includes VIA-Z or PIN\_DELAY in its calculation if these options are enabled and if your license permits this capability.

#### Arguments

|  |
| --- | ---
| `o_pin1` | A pin, via or rat\_t
| `o_pin2` | A pin, via or rat\_t on same xnet as o\_pin1
#### Value Returned

`nil` - Not a legal object; unsupported dbid or items not on same xnet

`f_etchLength` - length of object

#### See Also

[axlDBGetLength](#1081218 "26")

#### Example

> `Skill> pin1 = ashOne()`

> `Skill> pin2 = ashOne()`

> `Skill> axlDBPinPairLength(pin1 pin2)`

> `-> 2676.777`

### axlDeleteByLayer

`axlDeleteByLayer(t_layerName/lt_layerName[nil/'fixed])==> x_cnt/nil`

#### Description

Deletes all data on one or more provided layers. The following should be noted:

* Does not delete pins or vias.

* Deletes pins escapes and other symbol data associated with symbols.

* Does not delete objects on a symbol definition. If you are using this interface as a prerequisite to deleting a layer, objects on a symbol definition may prevent you from deleting the layer.

* To delete dynamic shapes, you also need to delete data on the equivalent BOUNDARY class.

* Certain classes, such as, DRC\_ERROR\_CLASS, PIN, VIA\_CLASS, ROUTER\_PLAN and CAVITY, are ignored.

#### Arguments

|  |
| --- | ---
| `t_layerName` | layer name <class>/<subclass>
| `lt_layerName` | list of layer names
| `'fixed` | Optional, ignore FIXED property
#### Value Returned

|  |
| --- | ---
| `x_cnt` | number of items deleted
| `nil` | any error
#### Example

* Delete all data on ETCH/TOP except for fixed data

> `axlDeleteByLayer("ETCH/TOP")`

* Delete all data on ETCH/BOTTOM plus OUTLINE layers including fixed

> `axlDeleteByLayer(list("ETCH/TOP" "BOARD GEOMETRY/OUTLINE") 'fixed)`

### axlExtentDB

`axlExtentDB()⇒ l_bBox/nil`

#### Description

Determines a design type and returns the`bBox` extent. See [axlExtentLayout](#1065432 "26") and [axlExtentSymbol](#1065544 "26") for what Allegro PCB Editor considers an extent.

#### Arguments

None

#### Valued Returned

|  |
| --- | ---
| `l_bBox` | Returns`bBox` extent.
| `nil` | Unknown drawing type.
### axlExtentLayout

`axlExtentLayout()⇒ l_bBox/nil`

#### Description

Obsolete. Use`axlExtentDB`. Kept for backward compatibility.

Computes the layout extents and returns the smallest bounding box to be used for window-fit. Only`lines`, `linesegs`, and `shapes` are searched on selected layers in the following order:

* `BOARD GEOMETRY/OUTLINE`

* `PACKAGE KEEPIN/ALL`

* `ROUTE KEEPIN/ALL`

The first layer with any elements is used to determine the layout extents. If no elements are found on these layers, the design extents are returned.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `l_bBox` | Returns`bBox` of the layout. (See `axlExtentDB`.)
| `nil` | Error such as the failure of`axlVisibleGet`.
#### See Also

[axlExtentDB](#1095185 "26")

### axlExtentSymbol

`axlExtentSymbol()⇒ l_bBox`

#### Description

Obsolete. Use[axlExtentDB](#1095185 "26"). Kept for backward compatibility.

Computes the bounding box enclosing all objects visible for a drawing (a`.dra`file).

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `l_bBox` | Smallest bounding box enclosing all visible objects. If no objects are visible, set to the design extents. (See`axlExtentDB`.)
#### See Also

[axlExtentDB](#1095185 "26")

### axlFindPath

`axlFindPath(o_oneDbido_twoDbid[g_altPath])==> lo_dbid/llo_dbid/nil`

#### Description

Finds an etch path from one object to another. Items must be on the same net and must be connect type, such as, pins, vias, clines or shapes, and tee.

Restrictions:

* A partial connection between the 2 objects (ratsnest still exists) results in a nil return.

* Segments are promoted to their owning cline (path)

Return list is ordered by:

> `o_oneDbid, ... <connected items>, o_twoDbid`

To use this for finding loops on a net, you must compare every node to every other node. This can be very time consuming for large pin count nets.

* ***- If multiple paths exist between the two objects, returns will follow a single path but the one it uses is not defined (by this it may decide on the shortest or longest.

  - Because of the high number of interconnects, VOLTAGE nets may not return correct results since the algorithm is recursive and terminates if it nests too deeply.***

#### Arguments

|  |
| --- | ---
| `o_oneDbid` | first net item
| `o_twoDbid` | second net item
| `[g_altPath]` | enable alternate path
#### Value Returned

|  |
| --- | ---
| `nil` | no path exists between objects or an error
| `lo_dbid` | path list if`g_altPath` is `nil`
| `llo_dbid` | path list if`g_altPath` is `t`. First item is one path and second item is nil or the alternative path. (`lo_1dbid` `lo1dbid`)
#### Example

* Find a path between two items

> ```
> ; ashOne is a selection utility found at <cdsroot>/pcb/examples/skill/ash-fxf/ashone.il
> ```

> `one = ashOne()`

> `two = ashOne()`

> `; pick a line, cline or segment (set find filter)`

> `path = axlFindPath(one two)`

> `axlShowObject(path)`

* See if the two objects is a start/end point of a loop

> `path = axlFindPath(one two t)`

### axlGeoPointInShape

`axlGeoPointInShape(l_pointo_dbid/o_polygon[g_include_voids][t/nil])⇒ t/nil`

#### Description

Given a point and a shape`dbid`, determines whether that point is inside or outside the shape or a polygon. For a shape with voids, a point is considered *outside* the given shape if inside a void. If shape has voids and g\_include\_voids is t then point is outside if inside a void.

The command does not allow hole polygons as input. When polygon holes is passed the following warning is displayed:

`Invalid polygon id argument -<argument>`

#### Arguments

|  |
| --- | ---
| `l_point` | Point to check.
| `o_dbid/o_polygon` | dbid of the shape / o\_polygon
| `[g_include_voids]` | Applicable only in case the second parameter is a shape otherwise it's ignored.  In case of shapes, if the parameter value is nil, voids are excluded. The default value is`t`.
| [`t`/`nil`] | `t` means include voids, `nil`means use the shape outline only.
| Default is`t`. |
#### Value Returned

|  |
| --- | ---
| `t` | Point is inside the shape.
| `nil` | Point is outside the shape, or incorrect arguments were given.
**See Also**: [axlGeoPointShapeInfo](#1080089 "26")

### axlGeoPointShapeInfo

`axlGeoPointShapeInfo(l_pointo_dbid) ==> (g_state o_dbid)/nil`

#### Description

Given a point and a shape dbid returns relation of point to shape. State may be outside, inside or on. Additional dbid is returned in the second argument to indicate if void or shape is involved.

Return matrix:

|  |
| --- | ---
| **G\_STATE** | **O\_DBID**
| outside | nil if outside shape, void dbid if inside void
| inside | nil
| on | shape dbid if on shape else void dbid
* Assumes that cross-hatch shapes are solid filled.

* Rounds point to database units. If database accuracy is 2 and you pass a 3 decimal place point, we will round it to 2 places before doing the test.

#### Arguments

|  |
| --- | ---
| `l_point` | the point
| `o_dbid` | dbid of the shape
#### Value Returned

`nil` - if an error since as an invalid argument

`g_state/o_dbid` - see *Description*

### axlGetImpedance

`axlGetImpedance(o_dbid) => (f_min f_max)/nil`

**Description**

Returns minimum and maximum impedance for given item. Item can be either cline, cline segment, net or xnet. Impedance is in ohms by default.

**Arguments**

|  |
| --- | ---
| `o_dbid` | Segment cline
**Value Returned**

|  |
| --- | ---
| `f_min f_max` | Impedance in current MKS units.
| `nil` | Segment is not a cline segment.
#### See Also

[axlSegDelayAndZ0](#1073778 "26")

### axlImpdedanceGetLayerBroadsideDPImp

```
axlImpdedanceGetLayerBroadsideDPImp(t_layer1/x_layerNum1t_layer2/x_layerNum2f_width) ==> f_diffImpedance/nil
```

#### Description

Computes the differential impedance of a broadside-coupled diffpair with the given line width and two specified layers on which the signal lines will be routed. A warning message may be given if the parameters are inappropriate for the calculation.

#### Arguments

`t_layer1` Layer name (example "ETCH/TOP" or "TOP")

`x_layerNum1` Number of the etch subclass. Layers are numbered starting with 0 for the Top layer.

`t_layer2` Layer name (example "ETCH/TOP" or "TOP")

`x_layerNum2` Number of the etch subclass. Layers are numbered starting with 0 for the Top layer.

`f_width:` The line width in user units.

#### Value Returned

The line differential impedance in ohms (float) or`nil` on error.

#### See Also

[axlImpedance2Width](#1077241 "26")

### axlImpdedanceGetLayerBroadsideDPWidth

```
axlImpdedanceGetLayerBroadsideDPWidth(t_layer1/x_layerNum1t_layer2/x_layerNum2f_diffImpedance)==> f_lineWidth/nil
```

#### Description

Computes the differential impedance of a broadside-coupled diffpair with the given line width and two specified layers on which the signal lines will be routed. A warning message may be given if the parameters are inappropriate for the calculation.

#### Arguments

`t_layer1` Layer name (example "ETCH/TOP" or "TOP")

`x_layerNum1` Number of the etch subclass. Layers are numbered starting with 0 for the Top layer.

`t_layer2` Layer name (example "ETCH/TOP" or "TOP")

`x_layerNum2` Number of the etch subclass. Layers are numbered starting with 0 for the Top layer.

`diffImp:` The target differential impedance in ohms.

#### Values Returned

The line width in user units or`nil` on error.

#### See Also

[axlImpedance2Width](#1077241 "26")

### axlImpdedanceGetLayerEdgeDPImp

```
axlImpdedanceGetLayerEdgeDPImp(t_layer/x_layerNumf_spacingf_width) ==> f_diffImpedance/nil
```

#### Description

Computes the differential impedance of a edge-coupled diffpair with the given line width and spacing on a specified layer. A warning message may be given if the parameters are inappropriate for the calculation.

#### Arguments

`t_layer` Layer name (example "ETCH/TOP" or "TOP").

`x_layerNum` Number of the etch subclass. Layers are numbered starting with 0 for the Top layer.

`f_spacing:` Spacing between the two signal lines in use units.

`f_width:` The line width in user units.

#### Value Returned

The differential impedance value in ohms (float) or`nil` on error.

#### See Also

[axlImpedance2Width](#1077241 "26")

### axlImpdedanceGetLayerEdgeDPSpacing

```
axlImpdedanceGetLayerEdgeDPSpacing(t_layer/x_layerNumf_widthf_diffImp)==> f_spacing/nil
```

#### Description

Given the line width of the two signal lines of an edge-coupled diffpair on the specified layer, finds the spacing such that the differential impedance is closest to the target value. A warning message may be given if the parameters are inappropriate for the calculation.

#### Arguments

`t_layer` Layer name (example "ETCH/TOP" or "TOP").

`x_layerNum` Number of the etch subclass. Layers are numbered starting with 0 for the Top layer.

`f_width:` The given line width, in user units.

`f_diffImp:` The target differential impedance in ohms.

#### Value Returned

The target spacing in user units or`nil` on error.

#### See Also

[axlImpedance2Width](#1077241 "26")

### axlImpdedanceGetLayerEdgeDPWidth

```
axlImpdedanceGetLayerEdgeDPWidth(t_layer/x_layerNumf_spacingf_diffImp) ==> f_width/nil
```

#### Description

Given the spacing of the two signal lines of an edge-coupled diffpair on the specified layer, finds the line width such that the differential impedance is closest to the target value. A warning message may be given if the parameters are inappropriate for the calculation.

#### Arguments

`t_layer` Layer name (example "ETCH/TOP" or "TOP").

`x_layerNum` Number of the etch subclass. Layers are numbered starting with 0 for the Top layer.

`f_spacing:` The spacing between the two signal lines in user units.

`f_diffImp:` The target differential impedance in ohms.

#### Value Returned

The line width in database units (float) or`nil` on error.

#### See Also

[axlImpedance2Width](#1077241 "26")

### axlImpedance2Width

`axlImpedance2Width(t_layer/x_layerNumf_impedance) ==> f_lineWidth/nil`

#### Description

Converts the given impedance on a specified layer to a line width.

**Note:** None of the`axlImpedance` APIs are available in Allegro PCB L.

#### Arguments

`t_layer` Layer name (example "ETCH/TOP" or "TOP").

`x_layerNum` Number of the etch subclass. Layers are numbered starting with 0 for the Top layer.

`f_impedance` The impedance value, in ohms, that is to be converted to a line width.

#### Value Returned

`f_lineWidth` The converted line width in drawing units.

`nil` Conversion was not successful.

#### See Also

[axlImpedance2Width](#1077241 "26")

[axlImpdedanceGetLayerEdgeDPImp](#1076505 "26")

[axlImpdedanceGetLayerEdgeDPWidth](#1076996 "26")

[axlImpdedanceGetLayerEdgeDPSpacing](#1076777 "26")

[axlImpdedanceGetLayerBroadsideDPImp](#1076247 "26")

[axlImpdedanceGetLayerBroadsideDPWidth](#1076248 "26")

### axlPadOnLayer

`axlPadOnLayer(o_dbidt_layer/x_layerNumber[g_noPadSuppress])==> t/nil`

#### Description

Tests if a pad is present on an etch layer. A pad is present on the layer if the padstack has a regular, anti or thermal pad and it is not suppressed by the rules of Pad Suppression.

While this does support a padstack dbid, for best operation, pass the VIA or PIN object.

#### Arguments

|  |
| --- | ---
| `o_dbid` | A via, pin or padstack
| `t_layer` | Name of layer (e.g. "TOP")
| `x_layerNumber` | layer number (starts at 0)
| `g_noPadSuppress` | t if ignore pad suppression, nil (default) use pad suppression
#### Value Returned

`t` if a pad is on layer; `nil` no pad on layer

#### See Also

[axlPadSuppressGet](04parmgt.html#1167420 "3")

#### Example

* Using ashOne shareware in`<cdsroot>/share/pcb/examples/skill/ash-fxf/ashone.il`

> Assuming a design where pad suppression is enabled on etch layer GND

> `pad = ashOne(list("vias" "pins"))`

> `res1 = axlPadOnLayer(pad "GND")`

> `res2 = axlPadOnLayer(pad "GND" t)`

### axlPinExport

`axlPinExport(g_includeTextLocation[t_csvfile])--> t/nil`

#### Description

This exports all pins in the symbol editor in csv format. The format of the csv file is described in[axlPinImport](#1095314 "26").

> **Note:** Function is only enabled in symbol editor.

#### Arguments

|  |
| --- | ---
| `g_includeTextLocation` | if`t`, include pin text location (offset, rotation and mirror); `nil` omits data which means pin text when loaded into a symbol will be located at pin origin.
| `t_csvfile` | Name of csv file; default is symbol name. Assumes a csv extension.
#### Value Returned

|  |
| --- | ---
| `t` | csv file created
| `nil` | failed to create csv file
#### See Also

[axlPinImport](#1095314 "26")

#### Example

See example in[axlPinImport](#1095314 "26").

### axlPinImport

`axlPinImport(t_csvFile)--> l_cnt/nil`

#### Description

This imports pin csv (comma separated values) file into the symbol editor. With this file you can describe the location and other characteristics of a set of pins (including mechanical) that comprise a symbol.

**Note:** This function is only enabled in symbol editor.

To best understand the format of this file, you should export one via axlPinExport.

Two formats are supported:

* pin only, pin text is located at pin origin

* pin with text

File format:

* A '#' indicates a comment

* (Optional) Units,`<units strings>`

* table describing pins

Pin Table (column number indicated)

* PinNumber - Pin number, if blank then a mechanical pin.

* Padstack - name of padstack

* x - x location of pin (no units)

* y - y location of pin (no units)

* rotation - pin rotations, if blank has no rotations

If the pin text option is used then the following columns should be present.

* x offset location from pin origin

* y offset location from pin origin

* rotation of text (absolute), if blank no rotation

* textMirror; blank no mirror, "m" text should be mirrored

Text block used for pin text is the design active text block.

**Note:** Setting axlDebug() may give additional info on why pins fail to load.

#### Arguments

|  |
| --- | ---
| `t_csvFile` | csv file, assumes a .csv extension.
#### Value Returned

|  |
| --- | ---
| `nil` | Unable to open file or no pins loaded
| `l_cnt` | A list of`(x_pinsLoaded x_pinFailed)`
#### See Also

[axlPinExport](#1078217 "26")

#### Example

* In the symbol editor with a`dra` file loaded. Export pins with text location, date, delete all pins and then import them:

> `axlPinExport(nil "foo")`

> `axlDeleteObject(axlDBGetDesign()->pins nil`

> `axlPinImport(foo")`

### axlReratNet

`axlReratNet(t_netName/o_dbid)==> t/nil`

#### Description

Rerats a net. Normally this is not required since Allegro PCB Editor automatically updates ratsnesting as required.

#### Arguments

|  |
| --- | ---
| `t_old_name` | the existing net name.
| `o_dbid` | Alternative is a dbid that is on a net
#### Value Returned

|  |
| --- | ---
| `t` | the net is successfully reratted.
| `nil` | fails.
#### Example

`axlReratNet("NET1")`

### axlText2Lines

`axlText2Lines(o_textDbid)==> llr_path/nil`

#### Description

This vectorizes a text dbid into a list of lists of`r_path` objects.

The return is a list of list`r_paths` for each character:

`llr_path = (l_rpathChar1, l_rpathChar2 ... l_lrpath_CharLast)`

Each character can have one or more line draws and each line draw can have one or more segments. For example, an 'A' has 2 line draws; one have 2 segments and the second 1 segment.

> `l_rpathChar1 = (l_rpathLine1, ... lrpathLineN)`

> where:

> > `l_rpathLineX->_width -> thickness of line`

> > `l_rpathLineX->__pathList -> list of segments making up a line`

Things of note:

* Vectorization returns line segments (no arcs) although this may change in the future.

* A single character may return multiple r\_paths and one r\_path may have multiple segments.

* The width is the same for all lines making up a single`textDbid`. This means that the width for all segments undefined since the r\_path has the width.

* Characters are returned left to right.

* Whitespace is skipped.

Allegro draws all text as stroke text. This converts a text dbid into a series of line draws using`r_path` structures.

* You can convert a`r_path` to an `o_polygon` by using axlPolyFromDB using its "`?line2poly t`" option.

#### Arguments

|  |
| --- | ---
| `o_textDbid` | A text dbid
#### Value Returned

|  |
| --- | ---
| `llr_path` | A list of list of r\_paths (see above)
| `nil` | An error (not a text dbid) or text dbid is an empty string (shown in Allegro with a small triangle).
#### See Also

[axlPolyFromDB](20plyopr.html#1076123 "21"), [Path Functions](03dbcre8.html#367312 "15")

#### Example

Function ashOne is a shareware utility that allows user to select one object (see`<cdsroot>/share/pcb/examples/skill/ash-fxf/ashone.il`).

* Pick a text and add converted lines on BOARD GEOMETRY/OUTLINE layer

> `text = ashOne("TEXT")`

> `lines = axlText2Lines(text)`

> `layer = "BOARD GEOMETRY/OUTLINE"`

> `; flatten list`

> `flattened = foreach( mapcan x lines x)`

> `; create objects in database`

> `foreach(path flattened i = axlDBCreatePath(path layer nil nil nil))`

* Pick a text and add converted to shapes on "BOARD GEOMETRY/ASSEMBLY\_DETAIL

> `text = ashOne("TEXT")`

> `lines = axlText2Lines(text)`

> `layer = "BOARD GEOMETRY/ASSEMBLY_DETAIL"`

> `; flatten list`

> `flattened = foreach( mapcan x lines x)`

> `foreach(path flattened`

> `; may return multiple polys`

> `polys = axlPolyFromDB(path ?endCapType 'ROUND ?line2poly t)`

> `; create shapes in database`

> `foreach(poly polys i = axlDBCreateShape(poly t layer nil nil))`

> `)`

### axlUnfixAll

`axlUnfixAll()==> x_count`

#### Description

This is a convenience API.

If removes the FIXED property from all elements in the design.

#### Arguments

`none`

#### Value Returned

|  |
| --- | ---
| `x_count` | Number of fixed properties removed.
#### Example

`axlUnfixAll()`

### axlWidth2Impedance

`axlWidth2Impedance(t_layer/x_layerNumf_lineWidth) ==> f_impedance/nil`

#### Description

Converts the given line width on a specified layer to an impedance. This uses the field solver to compute the impedance

#### Arguments

`t_layer` Layer name (example "ETCH/TOP" or "TOP").

`x_layerNum` Number of the etch subclass. Layers are numbered starting with 0 for the Top layer.

`f_lineWidth` The line width to be converted to an impedance.

#### Value Returned

`f_impedance` The converted impedance value.

`nil` Conversion was not successful.

#### See Also

[axlImpedance2Width](#1077241 "26")

### axlIsHighlighted

`axlIsHighlighted(o_dbid)==> x_highlightColor/nil`

#### Description

If the object is permanently highlighted returns the highlight color; otherwise`nil`.

**Note:** Pins can be highlighted.

Only symbols, nets, pins and DRC errors can be highlighted. Cadence suggests that you do not highlight drc objects unless they are external DRCs, since Allegro PCB Editor DRCs are frequently recreated.

#### Arguments

|  |
| --- | ---
| `o_dbid` | A`dbid` for which highlighting information is desired.
#### Value Returned

|  |
| --- | ---
| `x_highlightColor` | Highlight color;`nil` if not highlighted, or object does not support highlighting.
#### See Also

[axlHighlightObject](08intprm.html#572099 "7")

#### Examples

See[axlHighlightObject](08intprm.html#572099 "7")

### axlTestPoint

`axlTestPointo_dbidtop|bottom|nil)⇒ t/nil/s_error`

#### Description

Sets or clears a pin and/or via's test point status. Abides by the rules of the testprep parameter form in its ability to add a test point (see possible errors, below). If testprep rules prevent adding a test point, an error symbol is returned. If the command fails for other reasons,`nil` is returned. On success, a `t` is returned.

If you add a test point to a pin/via that already has a test point, the existing test point is replaced.

Uses current testprep parameter settings except (these may be relaxed in future releases):

* set to flood

* set allow SMT/Blind or Thru pad stack type

Not enabled in a symbol editor.

Adds test point text using same rules as the`testpoint manual` command.

**Note:** Does not delete associated test point text. This may be a future enhancement. For the present, use`axlDeleteObject` and `axlDBGetAttachedText`.

Supports`axlDebug` API to print failure to place error.

#### Arguments

|  |
| --- | ---
| `o_dbid` | Pin or via`dbid`
| `g_mode` | Add test point to top or bottom, or clear one.
#### Value Returned

|  |
| --- | ---
| `t` | Object changed.
| `nil` | Error other than test point checks.
| `s_error` | Symbol indicating an error from testprep parameter check.
#### Errors

|  |
| --- | ---
| `PAD_TOO_SMALL` | Size does not meet parameter minimums
| `PAD_UNDER_COMP` | Padstack under component
| `PIN_OFF_GRID` | Pin off grid
| `PAD_UNDEFINED` | Layer of padstack not defined on required layer
| `PAD_NOT_SMD` | Padstack must be a SMD
| `PAD_NOT_THRU` | Padstack must be a thru pad
| `PAD_IN_NO_PROBE_AREA` | Testpoint pad in`NO_PROBE` area
| `PIN_IS_VIA` | Pin type requires a via or any point
| `PIN_NOT_VIA` | Pin type requires a via
| `PIN_NOT_OUTPUT` | Pin type requires an output pin for test point
| `PIN_NOT_IO` | Pin type requires an IOpin for test point
| `PIN_TOO_CLOSE` | Pin too close to another test point
| `PAD_UNDER_PIN` | Test point under another pin
| `PIN_NOT_NODE` | Test point requires a node for testbench
| `FIXED_TEST_POINTS` | Testpoints are fixed and cannot be removed
| `OTHER` | Unclassified error
#### Examples

The following examples use the`ashone.il` file in `<cdsroot>/share/pcb/skill/examples` to allow you to select objects:

1) Add testpoint to top

`axlUIWPrint(nil 'info1 "Select pin or via to add testpoint")`

`dbid = ashOne('(VIAS PINS))`

`ret = axlTestPoint(dbid 'top)`

2) Clear a testpoint

`axlUIWPrint(nil 'info1 "Select pin or via to clear testpoint")`

`dbid = ashOne('(VIAS PINS))`

`ret = axlTestPoint(dbid nil)`

### axlChangeNet

`axlChangeNet(o_dbidt_netName/o_netdbid)⇒ t/nil`

#### Description

Changes the net an object is currently on. Restricted to shapes, filled rectangles (frectangles), pins and vias. Returns`t` when successful. Will not rip up clines or vias.

Failure can occur for the following reasons:

* Object is not supported.

* netName does not exist.

The following restrictions apply to this function:

* Pins must be assigned. Pins must have an associated component. Mechanical pins are un-assigned.

* Via net assignment is advised. The via must be able to connect to something on the provided net to remain on that net. Otherwise, it will fall back to the original net or possibly another net.

* If a via is in open space, it will be on a dummy net. This API cannot be used to force it onto a net.

* This API is useful for a via, if it touches multiple shapes but it is assigned to the wrong shape's net.

Potential side effects of this function:

* It may not properly reconnect two touching cline segments that were previously connected by the shape.

* Clines only attached to the shape will inherit the new net of the shape.

* Vias attached to the shape will not inherit the new net. This is different from the Allegro change net command.

#### Arguments

|  |
| --- | ---
| `o_dbid` | Shape`dbid`
| `t_netName/o_netdbid` | Name of a net or a netdbid (for dummy nets)
#### Value Returned

|  |
| --- | ---
| `t` | Object changed.
| `nil` | No object changed.
### axlSegDelayAndZ0

`axlSegDelayAndZ0(o_clineSegDbid)⇒ (f_delay f_z0)/nil`

#### Description

Returns the delay and impedance of a cline segment. Returns`nil` if a segment isn't a cline segment. Normally, delay is in nanoseconds and impedance is in ohms.

This function is noisy if you pass in non-cline segments.

#### Arguments

|  |
| --- | ---
| `o_clineSegDbid` | Segment cline
#### Value Returned

|  |
| --- | ---
| `f_delay` `f_z0` | Delay and impedance in current MKS units.
| `nil` | Segment is not a cline segment.
#### See Also

[axlGetImpedance](#1089568 "26")

### axlSetDefaultDieInformation

`axlSetDefaultDieInformation(comp)==> t/nil`

#### Description

Sets the default die information for a component.

This function will configure a newly-placed IC-class component as a die in a MCM or SIP design. Based on the placed component's information the die will be flagged as either wire bond or flip-chip.

#### Arguments

|  |
| --- | ---
| `comp` | dbid of the component / symbol to set default information for.
#### Value Returned

`t` if successful, `nil` otherwise.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
