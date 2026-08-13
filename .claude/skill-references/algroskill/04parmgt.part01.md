<!--
source: algroskill/04parmgt.md
part: 1/2
estimated_tokens: 13466
-->

### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

3
=

Parameter Management Functions
==============================

Overview
--------

This chapter describes the AXL-SKILL functions that retrieve and set Allegro database parameters. You can access certain Allegro parameters using these functions. Additional functions are built on top of`axlGetParam/axlSetParam` to make programming easier.

See[Chapter 1, "Introduction to Allegro PCB Editor SKILL Functions,"](01ovrvew.html#103136 "1") for a description of available parameter attributes.

The use model follows:

* Get the parameter using`axlGetParam.`

* Modify the values using`axlSetParam.`

* Update the parameter using`axlSetParam.`

AXL-SKILL restricts you from creating new parameters or subclasses.

### axlcreate

`axlcreate`

#### Description

This interface is obsolete. It is kept to support existing SKILL code.

Use[axlFilmCreate](#1148038 "3").

#### Arguments

None

#### Value Returned

The name of the film record created, or`nil` if command fails.

### axlDBGetTextBlockCount

`axlDBGetTextBlockCount()=> x_textBlockCount`

#### Description

Returns a count of the number of text blocks defined.

#### Arguments

NA

#### Value Returns

|  |
| --- | ---
| `x_textBlockCount` | A count of the number of text blocks defined.
#### Examples

`numTextBlocks = axlDBGetTextBlockCount()`

`printf("This database has %d text blocks\n" numTextBlocks)`

### axlDBGridGet

`axlDBGridGet(nil)==> lt_grids`

`axlDBGridGet(t_gridName)==> og_grid`

#### Description

This command returns current grid values. Function has two modes:

* if gridname is nil returns list of names

* If given a grid name return its grid characteristics (see below)

**Note:** Reserved grid name is "non-etch" otherwise grid names follow Allegro ETCH subclass names.

Use[axlDBDisplayControl](14dsnctl.html#721955 "14") to control grid color and visibility.

Grids have the following attributes:

|  |  |
| --- | --- | ---
| **Name** | **Type** | **Description**
| `objType` | string | Name of the object - grids
| readOnly | nil | can modify object
| name | string | Name of grid
| xOrigin | dbrep | X origin of grid
| yOrigin | dbrep | Y origin of grid
| xMajor | dbrep | Major X spacing of grid (read-only)
| yMajor | dbrep | Major Y spacing of grid (read-only)
| xGrids | l\_dbrep | Spacings X of grid (always a list of dbreps)
| yGrids | l\_dbrep | Spacings Y of grid (always a list of dbreps)
#### Arguments

|  |
| --- | ---
| `t_gridName` | name of grid or`nil` to get all grid names
#### Value Returned

* `lt_gridds` - list of grids

* `og_grid` - disembodied property list containing grid settings

#### See Also

[axlDBGridSet](#1120503 "3")

#### Example

Run the following code to get all grids and print them.

`grids = axlDBGridGet(nil)`

```
foreach(g gridsgrd = axlDBGridGet(g)printf("GRID name=%s  values=%L\n", grd->name, grd))
```

### axlDBGridSet

`axlDBGridSet(og_grid)==> t/nil`

#### Description

This command modifies the grid settings in the design.

In addition to the grid names (see[axlDBGridGet](#1120502 "3")), two symbolic grid names are available:

* `'all` - sets all grid values

* `'etch` - sets all ETCH grid values

As a convenience when setting a single the xGrids or yGrids attribute, you can use a float.

Both xMajor and yMajor values are automatically determined by the sum of the spacings in xGrids and yGrids respectively.

**Notes:**

* Non etch grids may not have multiple spacings. We only use the first grid seen.

* Setting grids is not undo-able (this may change in the future).

* Etch grids names are the same as ETCH layer names. This may change in the future.

* Origin values must be within drawing extents or 0.

* If Grid dialog is open it will not be updated when you change the grid settings using this API command.

#### Arguments

|  |
| --- | ---
| `og_grid` | a grid disembodied property list from[axlDBGridGet](#1120502 "3")
#### Value Returned

`t` if the command is successful and the grid is changed, `nil` in case of failure.

#### See Also

[axlDBGridGet](#1120502 "3"), [axlDBDisplayControl](14dsnctl.html#721955 "14")

#### Examples

* Modify TOP grid settings

> > `grid = axlDBGridGet("TOP")`

> > `grid = axlDBG`

* Modify all grids (note allow xGrids and yGrids to NOT be list)

> > `grid = axlDBGridGet("TOP")`

> > `grid->name = 'all`

> > `grid->xGrids = 5.0`

> > `grid->yGrids = 5.0`

> > `axlDBGridSet(grid)`

* Modify all etch grids

> > `grid = axlDBGridGet("TOP")`

> > `grid->name = 'etch`

> > `grid->xGrids = '(5.0 7.0)`

> > `grid->yGrids = '(5.0 6.0)`

> > `axlDBGridSet(grid)`

### axlDBTextBlockCreate

```
axlDBTextBlockCreate(x_blockTemplate?width  f_width?height f_height?lineSpace f_lineSpace?charSpace f_charSpace?photoWidth f_photoWidth) => x_textBlock/nil
```

#### Description

Creates a new text block from the template block number provided. By providing optional text block characteristics, you can get available text blocks by:

`lst = axlGetParam("paramTextBlock")`

#### Arguments

`x_blockTemplate`

`f_XXX`

#### Value Returned

* `x_textBlock` - new text block

* `nil` - Returned if the command fails. Typically, this happens when you have exhausted the number block Allegro provides, or one of the parameters is not of the correct data type.

#### See Also

[axlGetParam](#1126060 "3"), [axlSetParam](#1109729 "3"), [axlDBTextBlockCompact](07dbaccs.html#720279 "6")

#### Examples

Create a new text block based upon text block 1 but change width and height

`blockNum = axlDBTextBlockCreate(1 ?width 15.0 ?height 16.0)`

### axlDBTextBlockFindName

`axlDBTextBlockFindName(t_textBlockName)=> x_textBlockNumber/nil`

#### Description

Finds a text block based on its name.

#### Arguments

|  |
| --- | ---
| `t_textBlockName` | The name of the text block to be found.
#### Value Returned

|  |
| --- | ---
| `x_textBlockNumber` | Number of the text block found.
| `nil` | No text block found with the given name.
#### Examples

* Find the text block with the name "Refdes".

`textBlockNumber = axlDBTextBlockName("Refdes")`

```
if(textBlockNumber then printf("Text block Refdes is number %d\n" textBlockNumber)elseprintf("There is no text block named Refdes\n"))
```

### axlDBTextBlockGetName

`axlDBTextBlockGetName(x_textBlockNumber)=> t_name/nil`

#### Description

Returns the name associated with the given text block. Same as attribute`userName` in `axlGetParam("paramTextBlock:<number>")`.

#### Arguments

|  |
| --- | ---
| `x_textBlockNumber` | The index of the text block whose name it to be returned. Text blocks use a 1-based indexing.
#### Value Returns

|  |
| --- | ---
| `t_name` | The text block name
| `nil` | This text block has no name
#### Examples

`textBlockName = axlDBTExtBlockGetName(textBlockNumber)`

### axlDBTextBlockSetName

`axlDBTextBlockSetName(x_textBlockNumbert_name)=> t/nil`

#### Description

Defines a name for a given text block.

#### Arguments

|  |
| --- | ---
| `x_textBlockNumber` | The index of the text block whose name is to be defined. Text blocks use a 1 based indexing.
| `t_name` | The name being defined for the text block. A`nil` indicates that there is no name.
#### Value Returns

|  |
| --- | ---
| `t` | Success
| `nil` | Error
#### Examples

Define a name of "Refdes" for text block #3.

`axlDBTextBlockSetName(3 "Refdes")`

### axlExportXmlDBRecords

`axlExportXmlDBRecords(t_fileNamelt_parmGroups/nil) -> t/nil`

`axlExportXmlDBRecords(nil) -> lt_parmGroups`

#### Description

This exports an Allegro Parameter file from the current design. It offers the same capability as (*File - Import - Parameter*). Side effect is creation of a `param_write.log` file.

#### Arguments

|  |
| --- | ---
| `t_fileName` | Name of parameter file. Default extension is`.prm` and if not given a path component will locate the file via PARAMPATH. If filename is `nil` report back as a list the supported parameter groups.
| `lt_parmGroups` | List of parameter groups to export or nil to export all.
#### Value Returned

`t` if command is successfully executed, `nil` in case of an error

#### See Also

[axlImportXmlDBRecords](#1120492 "3")

#### Examples

* In an existing dump, save all its settings and load into a new design

> `axlExportXmlDBRecords("myparam" nil)`

> `axlOpenDesign(?design "newDesign")`

> `axlImportXmlDBRecords("myparam")`

* Dump current parameter groups

> `axlExportXmlDBRecords(nil)`

### axlFilmCreate

```
axlFilmCreate(t_filmname?negative               t/nil?undefineLineWidth      f_width?sequence               x_number?rotation               x_angle?xOffset                f_x?yOffset                f_y?shapeBoundingBox       f_value?mirrored               t/nil?fullContact            t/nil?suppressUnconnectPads  t/nil?drawMissingPadApertures t/nil?useApertureRotation    t/nil?suppressShapeFill      t/nil?vectorBasedPad         t/nil?drawHolesOnly          t/nil?layers                 lt_layers?domains                lt_domains?ipc2581                lt_ipcDomains?polyCutLayer t/nil) -> t/nil
```

#### Description

Creates a new artwork film or replaces an existing artwork film.

The terminology used matches the artwork dialog box. For more information on how each field is used, see the dialog box help.

* Defaults for all boolean entiess is`nil`.

* Due to Valor issue suppressShapeFill is always`nil` when using Gerber 4x or 6x.

* If the value of the`drawHolesOnly` parameter is set to `t`, drill holes are drawn for all pads defined on the VIA and PIN CLASS for the film.

* polyCutLayer declares the film as a cut film for poly vias. Film should only have pin and via from the etch family and those layers are utilized to output if any cuts on poly vias exist on the adjacent dielectric layer.

* Enanble`axlDebug` for additional error messages.

#### Arguments

|  |
| --- | ---
| `t_filmname` | Film name
| `f_width` | Undefined line width, default is 0.
| `x_number` | For PDF output ordering. Default is 1, range is 1 to 255. If films have the same number, their database order will determine output.
| `x_angle` | Film rotations, values are 0, 90, 180 or 270, Default is 0.
| `f_x, f_y` | Film offset in design units, Default is 0,0
| `f_value` | Shape bounding box in design units. Default is 0.
| `lt_layers` | List of Allegro layers to apply to film. Default is none. Layer names are fully qualified (include both class and subclass)  Example: "ETCH/TOP"  A mode exists where if you specify the class name all subclasses of that class are listed in the film.   Example: "MANUFACTURING"
| `lt_domains` | List of domains where film should be visible. Values are ipc2581, pdf, artwork and visibility. Default is all.
| `lt_ipcDomains` | List of domains where film should be used in IPC2581. Valid values are`inner`, `outer`, `misc`, `doc`, and `soldermask`.
#### Value Returned

`t` if film is created, `nil` in case of an error.

#### See Also

[axlGetParam](#1126060 "3"), [axlDeleteObject](06intedt.html#832160 "5"), [axlDebug](23utils.html#756141 "24")

#### Examples

* Add/Change

> To understand how to add films, right-click on the artwork dialog to save a film to film (FILM\_SETUP.txt)

* Get all films:

> `p = axlGetParam("artwork")`

> `p->groupMembers`

* Get a single film (where format is "artwork:<film name>"):

> `s = axlGetParam("artwork:top")`

> `s->??`

* Delete a film (in this case top):

> `axlDeleteObject(s)`

### axlImportXmlDBRecords

`axlImportXmlDBRecords(t_fileName) -> t/nil`

#### Description

This command imports an Allegro Parameter file into the current design. It offers the same capability as (*File - Import - Parameter*). A side effect is creation of `param_read.log` file.

* ***For new releases, the`prm` files may require updating to support new parameter records or additions to current records.***

* You can create your own custom parameter files and load them with this interface. While the export interface typically groups several Allegro parameters together, you can custom craft a`prm` file with a single parameter record or just a single parameter from one record (see example below). The only prm file requirements are:

|  |  |
| --- | --- | ---
|  |  | prm file xml header
|  |  |
| --- | --- | ---
|  |  | parameter header and trailer
|  |  |
| --- | --- | ---
|  |  | revision number per parameter (currently these are all 1)
#### Arguments

|  |
| --- | ---
| `t_fileName` | Name of parameter file. Default extension is`.prm`. If filename is not provided component will located the file via PARAMPATH.
#### Value Returned

`t` if success, `nil` an error

#### See Also

[axlExportXmlDBRecords](#1120505 "3")

#### Examples

See[axlExportXmlDBRecords](#1120505 "3")

Example of a parameter file with setting just the dynamic shape min area to 75.0:

`<?xml version="1.0" encoding="UTF-8" standalone="no" ?>`

`<CadenceAllegroParameter xmlns="">`

`<dynfill_parm_type>`

`<rev>1</rev>`

`<min_area>75.0 MIL</min_area>`

`</dynfill_parm_type>`

`</CadenceAllegroParameter>`

### axlMiniStatusReset

`axlMiniStatusReset() => t/nil`

#### Description

This resets the Option panel settings and find filter settings to a new design's default.

* ***Do not run this unless advise by Cadence.***

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `nil` | a command is active
| `t` | panel is reset settings
#### Examples

> `axlMiniStatusReset()`

### axlPadSuppressGet

`axlPadSuppressGet(nil)==> ll_LayerPadSuppress`

`axlDBGridGet(t_layer/x_layerNumber)==> l_LayerPadSuppress`

#### Description

Returns pad suppress layer characteristic for a layer or design. Pad suppression is not available in symbol editor.

Name dielectric layers will appear in the list unlike the pad suppress dialog.

#### Arguments

|  |
| --- | ---
| `nil` | Return all layers
| `t_layer` | Get suppress characteristics of named layer
| `x_layerNumber` | Layer number (1st layer is 0)
#### Value Returned

* `ll_LayerPadSuppress` - list of l\_LayerPadSuppress for all etch layers. Layers are ordered from top to bottom.

* `l_LayerPadSuppress` - suppress characteristics of named layer. The symbols pin and via are optional and if present indicate pin and/or vias will be suppressed on that layer.

> > `(<t_layer> [<s_pin>] [<s_via>])`

#### See Also

[axlPadSuppressSet](#1126058 "3"), [axlPadSuppressOkLayer](#1126057 "3"), [axlDBControl](14dsnctl.html#690074 "14"), [axlSubclassRoute](#1119179 "3"), [axlPadOnLayer](25dbmisc.html#1095281 "26")

#### Example

* Get and print suppress state of all layers

`suppress = axlPadSuppressGet(nil)`

`foreach(item suppressprintf("Layer=%s what= %L\n", car(item) cdr(item)))`

* Get settings for layer "GND"

> `suppress = axlPadSuppressGet("GND")`

* Get settings for layer 1

> `suppress = axlPadSuppressGet(1)`

### axlPadSuppressOkLayer

`axlPadSuppressOkLayer(t_layer/x_layerNumber)==> t/nil`

#### Description

Indicates if layer can be set for pad suppression. Only internal conductor and shape layers that are not set for negative artwork, support pad suppression.

#### Argument

|  |
| --- | ---
| `t_layer` | name of layer (e.g. "TOP")
| `x_layerNumber` | layer number (starts at 0);
#### Value Returned

`t` if layer can allows pad suppress; `nil` otherwise

#### See Also

[axlPadSuppressGet](#1167420 "3")

#### Examples

The following are the same in the PCB tool but may not be in APD or SiP Layout:

> `axlPadSuppressOkLayer("TOP")`

> `axlPadSuppressOkLayer(0)`

### axlPadSuppressSet

`axlPadSuppressSet(g_modell_LayerPadSuppress/'all/'none/nil)==> t/nil`

`axlPadSuppressSet(g_modet_layer/x_layerNumberls_options) ==> t/nil`

#### Description

This modifies the pad suppression settings in the design. Allows control of both dynamic suppression setting (g\_mode) and the individual layer options (subsequent arguments).

**Notes:**

* If passing a list of suppression layers then any errors in the list are ignored.

* Will mark dynamic shapes and DRC out of date.

* If enabling dynamic mode and no suppression layers are enabled the dynamic mode will be left disabled.

* Unlike the dynamic it will not automatically enable the display of padless holes.

* ***Pad suppression dialog should not be open when using this API.***

#### Argument

* `'off` - turn pad suppression off
* `nil` - maintain current pad suppression mode
* `'on` - turn pad suppression on

In the first format, second argument can have one of the following values.

|  |
| --- | ---
| `'all` | Enable suppress on all supported layers
| `'none` | Clear suppression on all supported layers
| `nil` | leave suppression layers allow (typically used to toggle global mode)
| `ll_LayerPadSuppress` | List of layers using same form as[axlPadSuppressGet](#1167420 "3").
Alternatively, use the second format to set suppression on single layers.

|  |
| --- | ---
| `t_layer` | Layer name
> > > or

|  |
| --- | ---
| `x_layerNumber` | Layer number when first layer is 0
| `ls_options` | May be`nil` or a list of `'via` and/or `'pin`
#### Value Returned

`t` if success, `nil` a failure

#### See Also

[axlDBGridGet](#1120502 "3"), [axlDRCUpdate](18consmgt.html#1081297 "19"), [axlDBDynamicShapes](07dbaccs.html#720167 "6")

#### Examples

* Enable dynamic suppression setting

> `axlPadSuppressSet('on nil)`

* Enable all layers and dynamic mode

> `axlPadSuppressSet('on 'all)`

* Delete suppression layer settings and turn off dynamic mode

> `axlPadSuppressSet('off 'none)`

* Turn on via suppression on layer GND

> `axlPadSuppressSet(nil "GND" '(via))`

* Turn on via & pin suppression on layer GND

> `axlPadSuppressSet(nil "GND" '(via pin))`

* Turn off suppression on a layer GND

> `axlPadSuppressSet(nil "GND" nil)`

* Turn on suppression for GND and VCC layers

> `axlPadSuppressSet(nil '(("GND" via pin) ("VCC" via pin)))`

### axlParamFilletDoc

`p = axlGetParam("fillet")`

`axlSetParam(p)`

#### Description

This function supports access to the fillet parameter record. The database is updated when[axlSetParam](#1109729 "3") is called.

* This parameter is not avaible in certain tiers of Allegro PCB Editor.

* If dynamic is enabled, or if a parameter is changed while dynamic fillet is in effect, when axlSetParam is called, all fillet/tapes are updated.

* If one of the min/max attributes is changed, the opposite value may be updated to enfoce the min <= max rule.

#### *Fillet Attributes*

|  |  |  |
| --- | --- | --- | ---
| **NAME** | **Set?** | **TYPE** | **DESCRIPTION**
| objectType | No | string | "fillet"
| dynamic | Yes | t/nil | enables/disables dynamic fillet or taper
| allowDRC | Yes | t/nil | allows fillet or taper to cause DRC
| allowCurved | Yes | t/nil | generates curves for fillet or taper
| unusedNets | Yes | t/nil | generates fillet or tapers on unused nets
| pin | Yes | t/nil | generates fillet on pins
| via | Yes | t/nil | generates fillet on vias
| ts | Yes | t/nil | generates fillet on Ts
| fingers  (APD/SIP only) | Yes | t/nil | generates fillet on fingers
| padsWithoutDrills | Yes | t/nil | generates fillet on pads without drills
| round | Yes | t/nil | generates fillet on round pads
| square | Yes | t/nil | generates fillet on square pads
| rect | Yes | t/nil | generates fillet on rectangule pads
| oblong | Yes | t/nil | generates fillet on oblong pads
| octagon | Yes | t/nil | generates fillet on octagon pads
| padShape | Yes | t/nil | generates fillet on shape pads
| sizeRound | Yes | float | minimum size of round pad to fillet
| sizeSquare | Yes | float | minimum size of square pad to fillet
| sizeRect | Yes | float | minimum size of rectangular pad to fillet
| sizeOblong | Yes | float | minimum size of oblong pad to fillet
| sizeOctagon | Yes | float | minimum size of octagon pad to fillet
| pinDesiredAngle | Yes | integer | desired fillet angle for a pin (0 to 99 degrees)
| viaDesiredAngle | Yes | integer | desired fillet angle for a via (0 to 99 degrees)
| tDesiredAngle | Yes | integer | desired fillet angle for a T (0 to 99 degrees)
| pinMaxAngle | Yes | integer | Maximum fillet angle for a pin (0 to 99 degrees)
| viaMaxAngle | Yes | integer | Maximum fillet angle for a via (0 to 99 degrees)
| tMaxAngle | Yes | integer | Maximum fillet angle for a T (0 to 99 degrees)
| pinMaxOffset | Yes | float | Maximum offset length for a pin
| viaMaxOffset | Yes | float | Maximum offset length for a via
| tMaxOffset | Yes | float | Maximum offset length for a T
| pinMaxArcOffset | Yes | float | Maximum arc offset length for a pin (only if curved fillets are allowed)
| pinMinArcOffset | Yes | float | Minimum arc offset length for a pin (only if curved fillets are allowed)
| viaMaxArcOffset | Yes | float | Maximum arc offset length for a via (only if curved fillets are allowed)
| viaMinArcOffset | Yes | float | Minimum arc offset length for a via (only if curved fillets are allowed)
| pinMinLineWidth | Yes | float | Minimum line width from a fillet to a pin
| viaMinLineWidth | Yes | float | Minimum line width from a fillet to a via
| tMinLineWidth | Yes | float | Minimum line width from a fillet to a T
| pinMaxLineWidth | Yes | float | Maximum line width from a fillet to a pin
| viaMaxLineWidth | Yes | float | Maximum line width from a fillet to a via
| tMaxLineWidth | Yes | float | Maximum line width from a fillet to a T
| taper | Yes | t/nil | enable/disable taper generation
| taperAngle | Yes | integer | desired taper angle (line to line)
| taperMaxOffset | Yes | float | maximum offset length for a line
#### Arguments

|  |
| --- | ---
| `axlGetParam` | Requires "fillet"
| `axlSetParam` | Requires return of axlGetParam
#### Value Returned

* axlGetParam returns fillet parameter record

* axlSetParam returns parameter dbid if successful, nil otherwise

#### Examples

Enable dynamic fillet

`p = axlGetParam("param")`

`p->dynamic = t`

`axlSetParam(p)`

#### See Also

[axlGetParam](#1126060 "3"), [axlSetParam](#1109729 "3")

### axlGetParam

`axlGetParam (t_parm_name)⇒ ﬁo_paramDbid/nil`

`axlGetParam (nil) =>lt_params`

#### Description

Gets the parameter`dbid` for a named object. Supported parameter names are shown below. For descriptions of attributes of a parameter, see are [Chapter 2, "The Allegro PCB Editor Database User Model."](02dbdesc.html#462876 "2")

#### Arguments

* Returns list of parameters supported
* `shapeStatic` and `shapeDynamic` - See `axlParamShapeDoc`
* `paramTextBlock`:`<#>` -- where `#` is 1-<N> (Example: `paramTextBlock:1`) where N is number of text blocks.
* `paramDesign`
* `paramDisplay`
* `paramLayerGroup`:`<name`- where name is a legal Allegro class name
* `paramLayerGroup:ETCH` - is obsolete for getting the cross-section layers, use new `axlXSectionGet()` family of APIs. If the design does not contain multiple cross-sections, this will still return the list of ETCH layers, and if there are no mask layers, this will be the list of all layers. It will be maintained for older Skill code to continue to work in single stackup designs with no mask layers.
* `paramLayerGroup`:`<name>/paramLayer:<name>`
* `paramLayerGroup:name>/includeNonLayers` - ETCH class includes all non-mask layers of the cross-section. By default, `paramLayerGroup:ETCH` includes only those ETCH subclasses that are also cross-section layers. In order to get additional ETCH subclasses that are not layers, such as BOND\_TOP and BOND\_BOTTOM for chip-on-board, add switch `includeNonLayers`.
* `artwork`- List of film names
* `artwork:<filmName>`- A film given by `filmName`
* `testprep` - See `axlParamTestPrepDoc`
* `Fillet`- See `axlParamFilletDoc`

#### Value Returned

|  |
| --- | ---
| `o_paramDbid` | `dbid` for the requested parameter.
| `lt_params` | Returns list of parameter names supported.
| `nil` | Parameter requested not found.
#### See Also

[axlSetParam](#1109729 "3"), and axlIsParamType

#### Example

1) Return all param types supported

`axlGetParam(nil)`

2) Get etch layer (to find all members of the etch class).

`Skill> etch_parm = axlGetParam("paramLayerGroup:ETCH")`

`param:123456`

`Skill> etch_parm->??`

`(objType "paramLayerGroup" name "ETCH" visible`

`-1 nChildren 4 groupMembers`

`("TOP" "GND" "VCC" "BOTTOM")`

`color -1`

`)`

`Skill> etch_parm->color`

`-1`

`Skill> etch_parm->groupMembers`

`("TOP" "GND" "VCC" "BOTTOM")`

3) Access artwork records:

A) Get list of all possible records.

`Skill> p = axlGetParam("artwork")`

`Skill> p->??`

`(objType "artwork" nChildren 4 groupMembers`

`("TOP" "GND" "VCC" "BOTTOM")`

B) Get information on film record "VCC".

`r = axlGetParam("artwork:VCC")`

`Skill> r->??`

`(objType "artwork" groupMembers`

`("ETCH/VCC" "PIN/VCC" "VIA CLASS/VCC") vectorBasedPad`

`t suppressShapeFill t useApertureRotation nil`

`drawMissingPadApertures nil suppressUnconnectPads t fullContact`

`nil mirrored nil shapeBoundingBox 100.0`

`offset (0.0 0.0) rotation 0 undefineLineWidth`

`0.0 negative t name "VCC"`

`)`

C) Delete a TOP parameter record.

`axlDeleteObject(axlGetParam("artwork:TOP"))`

4) Design (`paramDesign`) modification.

`axlDBChangeDesignOrigin: change design origin`

`axlDBChangeDesignExtents: change extents`

`axlDBChangeDesignUnits: change units and/or accuracy`

Also see`axlParamDesignDoc`

### axlSetParam

`axlSetParam (od_paramDbid)⇒ rd_paramDbid/nil`

#### Description

This allows applications to modify certain aspects of Allegro parameters. After a parameter has been retrieved, attributes of it can be changed locally. Those changes can then be put back into the database using`axlSetParam`.

#### Arguments

|  |
| --- | ---
| `od_paramDbid` | Parameter id returned from[axlGetParam](#1126060 "3"). Modify the parameters to be changed then call axlSetParam function to update the database.
#### Value Returned

|  |
| --- | ---
| `rd_paramDbid` | Returns the input parameter id if successful
| `nil` | Database was not modified.
#### Example

* Change visibility (note it is easier to use[axlVisibleSet](#1068662 "3") to do this)

> `(setq etch_top (axlGetParam "paramLayerGroup:ETCH/paramLayer:TOP"))`

> `=>param:123456`

> ; is layer visible ?

> `etch->visible`

> `t`

> ; blank it

> `etch_top->visible = nil`

> `t`

> `(axlSetParam etch_top)`

> `=>param:123456`

> ; layer is now invisible

> `etch_top->visible`

> `nil`

* Change accuracy

> `p = axlGetParam("paramDesign")`

> `p->accuracy = 3`

> `axlSetParam(p)`

Color Access
------------

### axlColorDoc

`axlColorDoc`

#### Description

Allegro supports two color access methods: pre-defined colors and Allegro database colors. Not all Allegro based programs support access to Allegro database colors. (This is only supported by the graphics editors.)

Pre-defined colors are set and accessed by their symbols:

* `'black`

* `'white`

* `'red`

* `'green`

* `'yellow`

* `'blue`

* `'multivalue` - use `dfor` fields where value not the same

* `'button` - current color of button faces (grey)

In addition, graphics editors support access to the colors used for Allegro layers. These are integer numbers.

AXL API calls such as`axlLayerGet("class/subclass")` or its primitive form

`axlGetParm("paramLayerGroup:<class>/paramLayer:<subclass>")`

return the current color setting of a layer via the color attribute call.

Example:

`p = axlLayerGet("etch/top")`

`p->color -> 2`

These colors currently range between 1 and 24 with 0 reserved for the background color.

Interfaces supporting setting color are mostly form based. For there interfaces see:

* `axlFormDoc`

* `axlFormColorize`

* `axlFormGridDoc`

* `axlGRPDoc`

#### Notes

* No AXL method is currently supported to allow you to change the red/green/blue (RGB) of Allegro database colors

* We restrict the pre-defined colors to those defined to minimize use of colors to minimize problems with 8 bit color graphics on UNIX. When 24 (or higher) color cards become standard on UNIX, this will be relaxed.

* On Windows, Microsoft's UI theme overrides the background color. To enable background color control for ENUM cointrols, when specifing the control in the form file add the "OPTION color". The default Microsoft theme for this control is disabled. Also, the drop-down itself drawns with the background color.

  On UNIX, this option is ignored and background coloring just works.

#### Arguments

none

#### Value Returned

none

### axlColorGet

`` axlColorGet(x_number/`background) -> lx_rgb/nil ``

`axlColorGet('count)-> x_count`

`axlColorGet('all)-> llx_rgb`

`axlColorGet('pattern) -> x_count`

#### Description

Get color palette. Supports the following modes:

* If passed, an index less the color count returns a list containing the red, green, blue palette values for that color index. These are integer values between`0` (no color and `255` (maximum color). For example, a value of `255 255 255` is white. Or if passed, '`background` returns the palette for the background.

* If given`'count` returns the current size of the database palette (currently always 24).

* If passed 'all returns a list of list (red, green, blue) for all entire database palette EXCEPT the background.

* Returns number of patterns supported (includes default solid).

The color index is the number assigned to each layer in Allegro PCB Editor. (see`axlVisibleGet`).

#### Arguments

|  |
| --- | ---
| `x_number` | Color number.
| `'background` | Get background color.
| `` `count `` | Query current database color palette size.
| `` `all `` | Get entire database color palette (except background).
#### Value Returned

|  |
| --- | ---
| `x_count` | Size of database palette.
| `nil` | Error.
| `lx_rgb` | A palette.
| `llx_rgb` | The entire database palette.
#### See Also

[axlColorSet](#1095354 "3"), [axlVisibleGet](#1068227 "3")

#### Examples

Get red/green/blue of color 2:

> `clr = axlColorGet(2)`

Get background color:

> `` bground = axlColorGet(`background) ``

Get number of colors:

> `` cnt = axlColorGet(`count) ``

Get all red/green/blue color settings except background:

> `` all = axlColorGet(`all) ``

Get number of display patterns supported

> `` cnt = axlColorGet(`pattern) ``

### axlColorShadowGet

`axlColorShadowGet(g_option) -> t/nil/x_percent`

#### Description

Provides the options of shadow mode.

#### Arguments

|  |
| --- | ---
| `g_option` |
| `'mode` | Shadow mode status (`t` is on, `nil` is off).
| `'activeLayer` | Active layer dimming enabled (`t`). This is called "Dim active layer in Options panel.
| `'highlight` | This is called "Dim color assignments" in the Options panel
| `'percent` | Current brightness percentage (0 to 100).
| `'custom` | Custom colors, these are not shadowed.
#### Value Returned

|  |
| --- | ---
| `t/nil` | Shadow or active layer mode on or off.
| `x_percent` | Brightness percentage.
#### See Also

[axlColorSet](#1095354 "3"), [axlColorShadowSet](#1096006 "3")

#### Examples

Is shadow mode on:

> `axlColorShadowGet('mode)`

Is shadow mode percent:

> `axlColorShadowGet('percent)`

### axlColorShadowSet

`axlColorShadowSet(g_modet/nil) -> t/nil`

`axlColorShadowSet('percentx_percentage) -> t/nil`

#### Description

Sets the shadow mode options. These are equivalent to the color commands in the shadow mode box under the Display group.

The Mode Options are:

* The mode option is either`t` or `nil` to turn shadow mode on or off.

* The activeLayer option is either`t` or `nil` to automatically dim the active layer. This is called "Dim active layer in Options panel.

* The highlight can be`t` or `nil` to dim highlighted objects. This is called *Dim color assignments* in the Options panel.

* The percent option sets the dimness (`0`) to brightness (`100`) percentage.

**Note:** On graphics or display combinations, shadow values of less than 40 percent disappear into the background. For example, you have what appears to be black on black.

After you finish all the color changes, call`axlVisibleUpdate` to update the display.

This interface is disabled if you set the*display\_noshadow* environment variable.

#### Arguments

* `'percent` - Set shadow mode percentage (0 to 100)
* `'mode` - Enable or disable shadow mode.
* `'highlighted` - Enable or disable shadow mode for highlighted objects.
* `'activeLayer` - Enable or disable active layer dimming.

#### Value Returned

|  |
| --- | ---
| `t` | If successful.
| `nil` | An argument error.
#### See Also

[axlColorSet](#1095354 "3"), [axlColorShadowSet](#1096006 "3"), [axlVisibleUpdate](19cmdctl.html#984586 "20")

#### Examples

Is shadow mode on:

> `axlColorShadowSet('mode t)`

Is shadow mode percent:

> `axlColorShadowSet('percent 20)`

### axlColorLoad

`axlColorLoad(t_file/nil) -> t/nil`

#### Description

Loads an Allegro PCB Editor color file (default .`col` file). Master color file is located at `<cdsroot>/share/pcb/text/lallegro.col`.

File format is:

`#     Comment if in first column.`

```
#N     Next line with a number is number of colors (currently only 24 is supported). This should appear first in the file.
```

`Number format`

`#Number`

`24`

```
#B - next line with a number is background color. This should appear after color number. Format of color line must be:
```

`(name is currently ignored):`

`0 <red> <green> <blue> [<name>]`

`EXAMPLE of background format setting it to black`

`#Background Color`

`0 0 0 0`

```
#I - next set of lines sets the colors. These should always appear last in the file. We will read until the first color number that exceeds the color number (currently hardcoded as 24) or the end of file is reached. The order the colors appear in the file determines the initial color [priority (highest (first) to lowest (last)].
```

`Format is:`

`<color number> <pen number> <red> <green> <blue> [<name>]`

`EXAMPLE:`

`1 1 255 255 255 White`

`2 2 14 210 255 LtBlue`

```
<color number>: entry in color table. This is the color number referenced by the allegro subclass (axlLayerGet)
```

```
<pen number>: Used by Allegro plot (UNIX) to control what pen to use during plotting. Not applicable on Windows.
```

`<red> intensity of red to blend into color 0 to 255`

`<green> intensity of green to blend into color 0 to 255`

`<blue> intensity of blue to blend into color 0 to 255`

```
<name> (optional) name of color, currently not used by Allegro but sigxp takes advantage of the name to auto-assign colors.
```

Call`axlVisibleUpdate` to update the display after you finish manipulating the colors.

In Allegro PCB Editor, you need the color file to start a new design. Opening existing databases uses the color table stored in that database. A new database created, when Allegro PCB Editor is already running, copies the color table from the previous database.

#### Arguments

|  |
| --- | ---
| `s_file` | Color file name to load.
| `nil` | Uses`lallegro.col`. If no directory path, Allegro PCB Editor uses the LOCALPATH environment variable to find the file.
#### Value Returned

|  |
| --- | ---
| `t` | If loaded file.
| `nil` | File not found or error in loading file.
#### Example

Load user-defined default color. Overriding and setting current board values:

> `axlColorLoad(nil)`

> `axlVisibleUpdate(t)`

#### See Also

[axlColorSave](#1135484 "3"), [axlColorSet](#1095354 "3").

### axlColorOnGet - Obsolete Command

`axlColorOnGet(g_item) -> t`

#### Description

This function is obsolete. Due to change in display model, switching off colors is no longer supported.

#### Arguments

Ignored

#### Value Returned

always`t`

### axlColorOnSet - Obsolete Command

`axlcolorOnSet(g_itemg_state) -> t`

#### Description

This is an obsolete command. Due to changes in the viewing model, now you cannot turn off a color in Allegro PCB Editor.

#### Arguments

Items are ignored.

#### Value Returned

|  |
| --- | ---
| `t` | Success always.
### axlColorPriorityGet - Obsolete Command

`axlColorPriorityGet(g_item[g_item2]) -> nil`

#### Description

Due to the changes in color model of Allegro PCB Editor, this command is now obsolete. Instead of this command, use[axlLayerPriorityGet](#1120655 "3").

#### Arguments

Items are ignored.

#### Value Returned

`nil`

#### See Also

[axlColorSet](#1095354 "3")

### axlColorPrioritySet - Obsolete Command

`axlColorPrioritySet(g_item[g_item2]) -> t`

#### Description

Due to the changes in color model of Allegro PCB Editor, this command is now obsolete. Instead of this command, use[axlLayerPrioritySet](#1110972 "3").

#### Arguments

Items are ignored.

#### Value Returned

`t`

#### See Also

[axlColorSet](#1095354 "3")

### axlColorSave

`axlColorSave(t_file/nil) -> t/nil`

#### Description

Saves current design colors to specified file.

#### Argument

|  |
| --- | ---
| `t_file` | File name. If`nil`; saves to `<HOME>/pcbenv/lallegro.col.` If no extension, uses .`col` extension.
#### Value Returned

|  |
| --- | ---
| `t` | Successful.
| `nil` | Failed to save.
#### EXAMPLES

Save current design color settings:

> `axlColorSave("mycolor")`

#### See Also

[axlColorSave](#1135484 "3"),[axlColorSet](#1095354 "3")

### axlColorSet

`axlColorSet(x_number/'backgroundl_rbg) -> t/nil`

`axlColorSet('allll_rgb) ->t/nil`

#### Description

Sets red, green, blue palette for a color number or background.

Modes supported:

* Color number (`x_number`) and red/green/blue list. `x_number` must be between one and `axlColorGet('count)`, or '`background` sets red/green/blue as the background color.

* `'all` takes a list of red/green/blue values and sets colors starting at one to the end of the list. Intended to use with `axlColorGet('all)` to save or restore color values.

Red/green/blue colors are values between`0` (least intensity) to `255` (maximum intensity).

After color changes are made, call`axlVisibleUpdate` to update the display.

***Color model:***

A color (or colorNumber) in Allegro PCB Editor has the following attributes:

* A palette of red, green and blue values between`0` and `255`. `0` adds none of the primary color to the mixture while `255` adds the maximum. For example, `0,0,0` is black and `255,255,255` is white. The color mixture is controlled using the palette section of the color command.

* Each color number can be assigned to a layer. Multiple layers will have the same color number, because there are more layers than colors.

* Allegro PCB Editor supports setting a background palette value. Grids, ratsnest, temporary highlight can have a color number assigned via`axlDBControl`.

Color services:

|  |
| --- | ---
| `axlColorSet` | This routine.
| `axlColorGet` | Get red, green, or blue of one or more color numbers.
| `axlColorShadowGet` | Shadow mode options.
| `axlColorShadowSet` | Set shadow mode options.
| `axlLayerPrioritySet` | set a layer to a display priority
| `axlLayerPriorityGet` | get a layer's current priority
| `axlLayerPriorityClearAll` | clear all layer priorities (restore to default)
| `axlLayerPrioritySaveAll` | save existing priority table
| `axlLayerPriorityRestoreAll` | restore saved priority table
| `axlColorSave` | Save color values to file.
| `axlColorLoad` | Load color values from file.
| `axlUIColorDialog` | Standard color chooser dialog box.
| `axlDBControl` | Miscellaneous color number assignments (for example, highlight).
| `axlLayerGet` | Get layer (class/subclass) attributes (control color) number and visibility for individual layers.
| `axlLayerSet` | Set color number or visibility for a layer.
| `axlVisibleLayer` | Set visibility of layer.
| `axlIsVisibleLayer` | Provides the layer visibility.
| `axlVisibleGet` | Get visibility set for design.
| `axlVisibleSet` | Set visibility set for design.
| `axlVisibleDesign` | Global design visibility control.
| `axlVisibleUpdate` | Update windows with color changes.
#### Arguments

|  |
| --- | ---
| `x_number` | Color index.
| `'background` | Set background color.
| `'all` | Set colors based upon a list starting at color number one.
| `l_rgb` | Red/green/blue lists; three integers.
| `ll_rgb` | Lists of red/green/blue values.
#### Value Returned

|  |
| --- | ---
| `t` | Successful.
| `nil` | An error; wrong arguments: color number is less then one or greater than maximum.
#### EXAMPLES

Set color number three same as color two:

> `clr = axlColorGet(2)`

> `axlColorSet(3 clr)`

> `axlVisibleUpdate(nil)`

Set first three colors:

> `axlColorSet('all '((10 10 10) (40 40 40) (100 100 100)))`

### axlCVFColorChooserDlg

```
axlCVFColorChooserDlg([x_color_index][g_show_hilite][x_hilite_flag][x_bitmap_index])==> t/nil
```

#### Description

Displays color palette modal dialog. Color wells reflect current design colors.

#### Arguments

|  |
| --- | ---
| `x_color_index` | Color index to initialize palette dialog. Values 0 to 191.
| `g_show_hilite` | Specifies whether or not the highlight check box is to be displayed. If the value is set to:  t - displays the highlight check box.  `nil/default` - highlight check box is not displayed.
| `x_hilite_flag` | Highlight state to initialize highlight check box (if displayed). Pass 1 or 0.
| `x_bitmap_index` | Bitmap index to initialize palette dialog. Values 0 to 15.
#### Value Returned

|  |
| --- | ---
| `list` | containing one or two int values for user color palette selection and highlight check box selection. if`g_show_hilite` is not `nil`, list contains the two values, or else list contains color index only.
| `nil` | if user cancels the form or error occurred.
### axlClearObjectCustomColor

`axlClearObjectCustomColor([lo_dbid])==> t/nil`

#### Description

Clear custom color of dbids

#### Arguments

|  |
| --- | ---
| `lo_dbid:` | List of dbids to clear custom color.
#### Value Returned

|  |
| --- | ---
| `t/nil:` | Returns`t` if at least one object custom color was cleared.  Returns`nil` otherwise.
#### Examples

See axlCustomColorObject for examples

#### See Also

[axlCustomColorObject](#1110302 "3")

### axlCustomColorObject

`axlCustomColorObject([lo_dbid][g_custom_color])==> t/nil`

#### Description

Custom color the provided dbid or list of dbids. Objects supported are nets, symbol instances, pins, and external DRCs.

The color index is between 1 and`` axlColorGet(`count) ``. The index references a RGB value in the Allegro Color table. The RGB values can be viewed or modifed via axlColorGet.

Custom colors need to be enabled (see[axlDBDisplayControl](14dsnctl.html#721955 "14")) to be viewed.

#### Arguments

|  |
| --- | ---
| `od_dbid` | list of DBIDS or one DBID
| `g_custom_color` | Color index to be used to set custom color. If the value is`nil`, perm highlight will be used.
#### Value Returned

|  |
| --- | ---
| `t` | Something was custom colored.
| `nil` | No valid dbids.
#### See Also

[axlClearObjectCustomColor](#1110182 "3"), [axlDBDisplayControl](14dsnctl.html#721955 "14"), [axlIsCustomColored](#1110545 "3")

#### Example

The example covered in this section uses`axlCustomColorObject` and `axlClearObjectCustomColor` functions to respectively, set and clear custom color of database elements during interactive commands.

The following example does the following:

* Defines the function highlight Loop.

* Loops on the function axlSelect gathering user selections to set/clear custom color.

* Custom colors objects using color 4.

* Waits then clears custom color.

The command can be stopped at any time by selecting Cancel or Done from the pop-up menu.

```
(defun customColorLoop ()axlSetFindFilter( ?enabled '("noall" "alltypes" "nameform")?onButtons "alltypes")while( axlSelect()    axlCustomColorObject( axlGetSelSet() 4)    checkColor = axlIsCustomColored( car(axlGetSelSet()) )    axlSleep(1)    axlClearObjectCustomColor( axlGetSelSet())    ))
```

### axlLayerPriorityClearAll

`axlLayerPriorityClearAll() -> t/nil`

#### Description

Clears all layer priority information in Allegro database. Use[axlLayerPrioritySet](#1110972 "3") for usage.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t:` | success
#### See Also

[axlLayerPrioritySaveAll](#1110848 "3"), [axlLayerPriorityRestoreAll](#1110767 "3")

### axlLayerPriorityGet

get layer's priority

`axlLayerPriorityGet(t_layer) -> x_priority/t_mapClass/nil`

#### Description

Obtains layer priority, where 0 is normal (not set). Priority can range from 1 (highest) to 255 (lowest).

Depending on the argument value, the function operates in two modes:

* if`t_layer` is layer name (class / subclass), returns priority of that layer as an integer

* if`t_layer` is class name then returns the mapped layer

**Note:** Mapped layer groupings may change from release to release (e.g. future releases may choose to break up some class groupings).

#### Argument

|  |
| --- | ---
| `t_layer` | layer name (`<class>/<subclass>`) or class name (`<class>`)
#### Value Returned

* `x_priority` - priority of layer (0 layer draws at normal priority)

* `t_mapClass` - class name used as lead group for provided class

* `nil` - error in layer name

#### See Also

[axlLayerPrioritySet](#1110972 "3")

#### Examples

* Get and fetch priority

> `axlLayerPrioritySet("BOARD GEOMETRY/OUTLINE" 1)`

> `prior = axlLayerPriorityGet("BOARD GEOMETRY/OUTLINE")`

* Get group class mapping of class Ref Des

> `axlLayerPrioritySet("REF DES") -> "COMPONENT VALUE"`

### axlLayerPriorityRestoreAll

`axlLayerPriorityRestoreAll() -> t/nil`

#### Description

Restores previously saved layer priority information. This function only works if a call to[axlLayerPrioritySaveAll](#1110848 "3") has been done already.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t:` | success
| `nil:` | nothing to restore.
#### See Also

[axlLayerPrioritySaveAll](#1110848 "3"), [axlLayerPriorityClearAll](#1110678 "3")

### axlLayerPrioritySaveAll

`axlLayerPrioritySaveAll() -> t/nil`

#### Description

Saves all layer priority information to be restored later. Until a[axlLayerPriorityRestoreAll](#1110767 "3") is called, any subsequent calls to this function are no-op.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t:` | success
| `nil:` | this function has been called already but axlLayerPriorityRestoreAll has not been called yet.
#### See Also

[axlLayerPriorityClearAll](#1110678 "3"), [axlLayerPriorityRestoreAll](#1110767 "3")

### axlLayerPrioritySet

`axlLayerPrioritySet(t_layerx_priority) -> t/nil`

#### Description

This changes the drawing priority of given layer. Priority is from 1 (highest) to 255 (lowest). Layers without priority in standard drawing order below all priority layers. The active layer is always drawn first.

Only one layer may be at a priority level, thus adding a new layer at a priority replaces the existing layer at that priority. For example, executing following line of code results in just the ASSEMBLY\_TOP being drawn at priority 1 and OUTLINE returning to normal drawing order.

> > `axlLayerPrioritySet( "BOARD GEOMETRY/OUTLINE" 1)`

> > `axlLayerPrioritySet( "PACKAGE GEOMETRY/ASSEMBLY_TOP" 1)`

From priority level 1 each level must be set for lower priority levels to be enabled. For example, if you set a layer to priority level 2 but leave level 1 empty then level 2 is disabled until level 1 is assigned.

Classes may be grouped together in a class group with one class being the lead of that group. For example, all etch layers (ETCH, PIN, etc.) are mapped together into the stack-up group with class ETCH the lead. You can set the priority using class names but you cannot prioritized the different stack-up layers individually. This interface automatically maps a class name to its class group (see[axlLayerPriorityGet](#1120655 "3") to determine groupings).

You should do a[axlVisibleUpdate](19cmdctl.html#984586 "20") after changing layer priority to have the display updated.

**Note:** Priority value of 0 means remove layer priority of the layer.

#### Arguments

|  |
| --- | ---
| `x_layer` | layer name (i.e. "ETCH/TOP")
| `x_priority` | priority value in the range of 1-255 and 0 means remove.
#### Value Returned

|  |
| --- | ---
| `t` | success
| `nil` | error in one of the arguments
#### Examples

Set priority for class BOARD GEOMETRY and subclass OUTLINE:

> `axlLayerPrioritySet("BOARD GEOMETRY/OUTLINE" 1)`

To temporarily force a set of layers to display on top, you should take the following steps:

* save existing layer table,

* clear existing layer priorities

* set your layer priorities

* draw objects

* restore old layer priority:

> > `axlLayerPrioritySaveAll()`

> > `axlLayerPriorityClearAll()`

> > `axlLayerPrioritySet() -- multiple times if needed`

> > `axlLayerPriorityRestoreAll()`

#### See Also

[axlLayerPriorityClearAll](#1110678 "3"), [axlLayerPrioritySaveAll](#1110848 "3"), [axlLayerPriorityRestoreAll](#1110767 "3"), [axlLayerPriorityGet](#1120655 "3"), [axlMapClassName](23utils.html#911688 "24"), [axlVisibleUpdate](19cmdctl.html#984586 "20")

### axlIsCustomColored

`axlIsCustomColored (o_dbid)==> x_customColor/nil`

#### Description

If object has custom color, will return the object custom color, otherwise nil.

#### Arguments

|  |
| --- | ---
| `o_dbid` | An dbid for which custom color information is desired.
Value Returned

|  |
| --- | ---
| `x_customColor` | custom color or nil if object has no custom color or object does not support custom color.
#### See Also

[axlCustomColorObject](#1110302 "3")

Database Layer Management
-------------------------

These functions allow easier access to layer attributes.

### axlClasses

`axlClasses() -> lt_classes`

#### Description

Return list of classes.The is actually just:

> `axlGetParam("paramLayerGroup")->groupMembers`

#### Arguments

Nothing

#### Value Returned

list of class strings

#### See Also

[axlSubclasses](#1107319 "3"), [axlGetParam](#1126060 "3"), [axlMapClassName](23utils.html#911688 "24")

#### Examples

`axlClasses()`

### axlDBGetLayerType

`axlDBGetLayerTypet_layerName)⇒ t_layertype/nil`

#### Description

Retrieves the cross-section type of a given layer. This may be (Layer Type in define xsection form):`CONDUCTOR`, `DIELECTRIC`, `PLANE`, `SURFACE`, `DIESTACK` or `MASK`.

> **Note:** See crosssection dialog for a current list.

#### Arguments

|  |
| --- | ---
| `t_layername` | Layername is*<class>*/*<subclass>*.
#### Value Returned

|  |
| --- | ---
| `t_layertype` | Layer type string.
| `nil` | Layer is invalid.
#### See Also

[axlXSectionGet](#1169585 "3")

#### Example

`axlDBGetLayerType("ETCH/TOP") => "CONDUCTOR"`

### axlGetXSection

`axlGetXSection()==> ll_layers/nil`

#### Description

* This is obsolete, use new axlXSectionGet() family of APIs. The command will be maintained for older SKILL code but it will not be enhanced to support new dataReturns a list of all layers in the cross section found in the current drawing.

#### Values Returned

An ordered skill list of layers in the board's cross section. A list of the following format defines each layer:

`(t_name t_type t_material t_thickness t_thermalCond t_elecCond`

`t_dielectricConst y_artworkNeg y_shield t_lossTangent`

`t_usage t_SignalDieConstant t_SignalLossTangent g_freqDepFileName)`

where:

|  |
| --- | ---
| `t_name` | Layer name.
| `t_type` | Layer type.
| `t_material` | Layer material.
| `t_thickness` | Layer thickness.
| `t_thermalCond` | Layer thermal conductivity.
| `t_elecCond` | Layer electrical conductivity.
| `t_dielectricConst` | Layer dielectric constant.
| `y_artworkNeg` | Indicates whether the artwork for the layer is negative.
| `y_shield` | Indicates whether the layer is a shield layer.
| `t_lossTangent` | Layer loss tangent (valid for dielectrics only).
| `t_usage` | obsolete ("")
| `t_SignalDieConstant` | Dielectric between traces on interior signal layers (or`nil`).
| `t_SignalLossTangent` | Dielectric between traces on interior signal layers (or`nil`).
| `g_freqDepFileName` | Defines the name of the frequency-dependent data file for the file;`nil` if no file name is defined for this layer.
| `t_etchFactor` | Defines the etch factor for this layer which is in degrees.
**Note:** The`t_SignalDieConstant` and `t_SignalLossTangent` are `nil`on PLANE and dielectric layers.

### axlIsEtchLayer

`axlIsEtchLayer(t_layer)=> t/nil`

#### Description

Determines if a layer is associated with the ETCH layers. Returns`t` if layer is associated with any of te ETCH layers -- `ETCH`, `PIN`,`VIA`, `DRC`, `VIA_KEEPOUT`, `ROUTE_KEEPOUT`, `ANTI_ETCH`, `BOUNDARY`, `CONSTRAINT_REGION`, `ROUTER_PLAN`, and `CAVITY`

#### Arguments

|  |
| --- | ---
| `t_layer` | Layer name (e.g. "ETCH/TOP") or just class name ("ETCH")
#### Value Returns

|  |
| --- | ---
| `nil` | Not an etch associated layer
| `t` | Is an etch associated layer
#### Examples

`axlIsEtchLayer("PIN/TOP")`

`axlIsEtchLayer("ETCH")`

### axlIsLayer

`axlIsLayer(t_layer)⇒ t/nil`

#### Description

Determines if the`t_layer` exists. `t_layer` is a fully qualified layer name.

#### Arguments

|  |
| --- | ---
| `t_layer` | Name of layer in format "*<class>/<subclass>*."
#### Value Returned

|  |
| --- | ---
| `t` | Layer exists.
| `nil` | Layer does not exist.
### axlIsVisibleLayer

`axlIsVisibleLayer(t_layer)⇒ t/nil`

#### Description

Returns the visibility (`t/nil`) of a fully qualified layer.

#### Arguments

|  |
| --- | ---
| `t_layer` | Name of layer in format "<`class`>/<`subclass`>".
#### Value Returned

|  |
| --- | ---
| `t` | Layer is visible.
| `nil` | Layer is invisible or not present.
#### Example

> `axlIsVisibleLayer("pin/top") ⇒ t`

### axlLayerCreateCrossSection

```
axlLayerCreateCrossSection(t_Prev_layerNamet_layerTypet_materialType[t_subclassName][t_planeType])⇒ t/nil
```

#### Description

This is obsolete, use[axlXSectionCreate](#1168694 "3").

Adds a new cross-section layer to the design.

If`t_subclassName` is `nil` then an unnamed dielectric layer is created. It is suggested that you create unnamed dielectric layers if they are only required for signal analysis and board thickness calculations since using a name will create ETCH layer in the design.

#### Arguments

