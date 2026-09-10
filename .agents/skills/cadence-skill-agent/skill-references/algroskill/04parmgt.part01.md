<!--
source: algroskill/04parmgt.md
part: 1/2
estimated_tokens: 13006
-->

### axlcreate

axlcreate

#### Description

This interface is obsolete. It is kept to support existing SKILL code.

Use axlFilmCreate.

#### Arguments

None

#### Value Returns

The name of the film record created, or `nil` if command fails.

### axlDBGetTextBlockCount

`axlDBGetTextBlockCount() => x_textBlockCount`

#### Description

Returns a count of the number of text blocks defined.

#### Arguments

NA

#### Value Returns

| Name | Description |
|---|---|
| `x_textBlockCount` | A count of the number of text blocks defined. |

### axlDBGridGet

`axlDBGridGet( nil) => lt_grids`

or

`axlDBGridGet( t_gridName) => og_grid`

#### Description

`numTextBlocks = axlDBGetTextBlockCount() printf("This database has %d text blocks\n" numTextBlocks)` This command returns current grid values. Function has two modes:

- if gridname is nil returns list of names

- If given a grid name return its grid characteristics (see below)

Note: Reserved grid name is "non-etch" otherwise grid names follow Allegro ETCH subclass names.

Use axlDBDisplayControl to control grid color and visibility.

Grids have the following attributes:

| Name | Description |
|---|---|
| Name | Type; Description |
| `objType` | string; Name of the object - grids |
| readOnly | nil; can modify object |
| name | string; Name of grid |
| xOrigin | dbrep; X origin of grid |
| yOrigin | dbrep; Y origin of grid |
| xMajor | dbrep; Major X spacing of grid (read-only) |
| yMajor | dbrep; Major Y spacing of grid (read-only) |
| xGrids | l_dbrep; Spacings X of grid (always a list of dbreps) |
| yGrids | l_dbrep; Spacings Y of grid (always a list of dbreps) |

#### Arguments

| Name | Description |
|---|---|
| `t_gridName` | name of grid or `nil` to get all grid names |

#### Value Returns

- `lt_gridds` - list of grids

- `og_grid` - disembodied property list containing grid settings

#### Examples

Run the following code to get all grids and print them.

#### See Also

axlDBGridSet

### axlDBGridSet

`axlDBGridSet( og_grid) => t/nil`

#### Description

`grids = axlDBGridGet(nil) foreach(g grids grd = axlDBGridGet(g) printf("GRID name=%s values=%L\n", grd->name, grd))` This command modifies the grid settings in the design.

In addition to the grid names (see axlDBGridGet), two symbolic grid names are available:

- `'all` - sets all grid values

- `'etch` - sets all ETCH grid values

As a convenience when setting a single the xGrids or yGrids attribute, you can use a float.

Both xMajor and yMajor values are automatically determined by the sum of the spacings in xGrids and yGrids respectively.

Notes:

- Non etch grids may not have multiple spacings. We only use the first grid seen.

- Setting grids is not undo-able (this may change in the future).

- Etch grids names are the same as ETCH layer names. This may change in the future.

- Origin values must be within drawing extents or 0.

- If Grid dialog is open it will not be updated when you change the grid settings using this API command.

#### Arguments

| Name | Description |
|---|---|
| `og_grid` | a grid disembodied property list from axlDBGridGet |

#### Value Returns

`t` if the command is successful and the grid is changed, `nil` in case of failure.

#### Examples

| Name | Description |
|---|---|
| 1. | Modify TOP grid settings |

`grid = axlDBGridGet("TOP")`

`grid = axlDBG`

| Name | Description |
|---|---|
| 2. | Modify all grids (note allow xGrids and yGrids to NOT be list) |

`grid = axlDBGridGet("TOP")`

`grid->name = 'all`

`grid->xGrids = 5.0`

`grid->yGrids = 5.0`

`axlDBGridSet(grid)`

| Name | Description |
|---|---|
| 3. | Modify all etch grids |

`grid = axlDBGridGet("TOP")`

`grid->name = 'etch`

`grid->xGrids = '(5.0 7.0)`

`grid->yGrids = '(5.0 6.0)`

`axlDBGridSet(grid)`

#### See Also

axlDBGridGet, axlDBDisplayControl

### axlDBTextBlockCreate

`axlDBTextBlockCreate( x_blockTemplate ?width f_width ?height f_height ?lineSpace f_lineSpace ?charSpace f_charSpace ?photoWidth f_photoWidth ) => x_textBlock/nil`

#### Description

Creates a new text block from the template block number provided. By providing optional text block characteristics, you can get available text blocks by:

#### Arguments

`lst = axlGetParam("paramTextBlock") x_blockTemplate`

`f_XXX`

#### Value Returns

- `x_textBlock` - new text block

- `nil` - Returned if the command fails. Typically, this happens when you have exhausted the number block Allegro provides, or one of the parameters is not of the correct data type.

#### Examples

Create a new text block based upon text block 1 but change width and height

#### See Also

axlGetParam, axlSetParam, axlDBTextBlockCompact

### axlDBTextBlockFindName

`axlDBTextBlockFindName( t_textBlockName ) => x_textBlockNumber/nil`

#### Description

`blockNum = axlDBTextBlockCreate(1 ?width 15.0 ?height 16.0)` Finds a text block based on its name.

#### Arguments

| Name | Description |
|---|---|
| `t_textBlockName` | The name of the text block to be found. |

#### Value Returns

| Name | Description |
|---|---|
| `x_textBlockNumber` | Number of the text block found. |
| `nil` | No text block found with the given name. |

#### Examples

- Find the text block with the name "Refdes".

### axlDBTextBlockGetName

`axlDBTextBlockGetName( x_textBlockNumber ) => t_name/nil`

#### Description

`textBlockNumber = axlDBTextBlockName("Refdes") if(textBlockNumber then printf("Text block Refdes is number %d\n" textBlockNumber) else printf("There is no text block named Refdes\n") )` Returns the name associated with the given text block. Same as attribute `userName` in `axlGetParam("paramTextBlock:<number>")`.

#### Arguments

| Name | Description |
|---|---|
| `x_textBlockNumber` | The index of the text block whose name it to be returned. Text blocks use a 1-based indexing. |

#### Value Returns

| Name | Description |
|---|---|
| `t_name` | The text block name |
| `nil` | This text block has no name |

### axlDBTextBlockSetName

`axlDBTextBlockSetName( x_textBlockNumber t_name ) => t/nil`

#### Description

`textBlockName = axlDBTExtBlockGetName(textBlockNumber)` Defines a name for a given text block.

#### Arguments

| Name | Description |
|---|---|
| `x_textBlockNumber` | The index of the text block whose name is to be defined. Text blocks use a 1 based indexing. |
| `t_name` | The name being defined for the text block. A `nil` indicates that there is no name. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Success |
| `nil` | Error |

#### Examples

Define a name of "Refdes" for text block #3.

`axlDBTextBlockSetName(3 "Refdes")`

### axlExportXmlDBRecords

`axlExportXmlDBRecords( t_fileName lt_parmGroups/nil ) => t/nil`

or

`axlExportXmlDBRecords( nil ) => lt_parmGroups`

#### Description

This exports an Allegro Parameter file from the current design. It offers the same capability as (File - Import - Parameter). Side effect is creation of a `param_write.log` file.

#### Arguments

| Name | Description |
|---|---|
| `t_fileName` | Name of parameter file. Default extension is `.prm` and if not given a path component will locate the file via PARAMPATH. If filename is `nil` report back as a list the supported parameter groups. |
| `lt_parmGroups` | List of parameter groups to export or nil to export all. |

#### Value Returns

`t` if command is successfully executed, `nil` in case of an error

#### Examples

| Name | Description |
|---|---|
| 1. | In an existing dump, save all its settings and load into a new design |

`axlExportXmlDBRecords("myparam" nil)`

`axlOpenDesign(?design "newDesign")`

`axlImportXmlDBRecords("myparam")`

| Name | Description |
|---|---|
| 2. | Dump current parameter groups |

`axlExportXmlDBRecords(nil)`

#### See Also

axlImportXmlDBRecords

### axlFilmCreate

`axlFilmCreate( t_filmname ?negative t/nil ?undefineLineWidth f_width ?sequence x_number ?rotation x_angle ?xOffset f_x ?yOffset f_y ?shapeBoundingBox f_value ?mirrored t/nil ?fullContact t/nil ?suppressUnconnectPads t/nil ?drawMissingPadApertures t/nil ?useApertureRotation t/nil ?suppressShapeFill t/nil ?vectorBasedPad t/nil ?drawHolesOnly t/nil ?layers lt_layers ?domains lt_domains ?ipc2581 lt_ipcDomains ?polyCutLayer t/nil ) => t/nil`

#### Description

Creates a new artwork film or replaces an existing artwork film.

The terminology used matches the artwork dialog box. For more information on how each field is used, see the dialog box help.

- Defaults for all boolean entiess is `nil`.

- Due to Valor issue suppressShapeFill is always `nil` when using Gerber 4x or 6x.

- If the value of the `drawHolesOnly` parameter is set to `t`, drill holes are drawn for all pads defined on the VIA and PIN CLASS for the film.

- polyCutLayer declares the film as a cut film for poly vias. Film should only have pin and via from the etch family and those layers are utilized to output if any cuts on poly vias exist on the adjacent dielectric layer.

- Enanble `axlDebug` for additional error messages.

#### Arguments

| Name | Description |
|---|---|
| `t_filmname` | Film name |
| `f_width` | Undefined line width, default is 0. |
| `x_number` | For PDF output ordering. Default is 1, range is 1 to 255. If films have the same number, their database order will determine output. |
| `x_angle` | Film rotations, values are 0, 90, 180 or 270, Default is 0. |
| `f_x, f_y` | Film offset in design units, Default is 0,0 |
| `f_value` | Shape bounding box in design units. Default is 0. |
| `lt_layers` | List of Allegro layers to apply to film. Default is none.Layer names are fully qualified (include both class and subclass)Example: "ETCH/TOP"A mode exists where if you specify the class name all subclasses of that class are listed in the film. Example: "MANUFACTURING" |
| `lt_domains` | List of domains where film should be visible. Values are ipc2581, pdf, artwork and visibility. Default is all. |
| `lt_ipcDomains` | List of domains where film should be used in IPC2581. Valid values are `inner`, `outer`, `misc`, `doc`, and `soldermask`. |

#### Value Returns

`t` if film is created, `nil` in case of an error.

#### Examples

- Add/Change

To understand how to add films, right-click on the artwork dialog to save a film to film (FILM_SETUP.txt)

- Get all films:

`p = axlGetParam("artwork")`

`p->groupMembers`

- Get a single film (where format is "artwork:<film name>"):

`s = axlGetParam("artwork:top")`

`s->??`

- Delete a film (in this case top):

`axlDeleteObject(s)`

#### See Also

axlGetParam, axlDeleteObject, axlDebug

### axlImportXmlDBRecords

`axlImportXmlDBRecords( t_fileName ) => t/nil`

#### Description

This command imports an Allegro Parameter file into the current design. It offers the same capability as (File - Import - Parameter). A side effect is creation of `param_read.log` file.

- For new releases, the `prm` files may require updating to support new parameter records or additions to current records.

- You can create your own custom parameter files and load them with this interface. While the export interface typically groups several Allegro parameters together, you can custom craft a `prm` file with a single parameter record or just a single parameter from one record (see example below). The only prm file requirements are:

- prm file xml header

- parameter header and trailer

- revision number per parameter (currently these are all 1)

#### Arguments

| Name | Description |
|---|---|
| `t_fileName` | Name of parameter file. Default extension is `.prm`. If filename is not provided component will located the file via PARAMPATH. |

#### Value Returns

`t` if success, `nil` an error

#### Examples

See axlExportXmlDBRecords

Example of a parameter file with setting just the dynamic shape min area to 75.0:

`<?xml version="1.0" encoding="UTF-8" standalone="no" ?> <CadenceAllegroParameter xmlns=""> <dynfill_parm_type> <rev>1</rev> <min_area>75.0 MIL</min_area> </dynfill_parm_type> </CadenceAllegroParameter>`

#### See Also

axlExportXmlDBRecords

### axlMiniStatusReset

`axlMiniStatusReset( ) => t/nil`

#### Description

This resets the Option panel settings and find filter settings to a new design's default.

- Do not run this unless advise by Cadence.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `nil` | a command is active |
| `t` | panel is reset settings |

#### Examples

`axlMiniStatusReset()`

### axlPadSuppressGet

`axlPadSuppressGet( nil ) => ll_LayerPadSuppress`

or

`axlPadSuppressGet( t_layer/x_layerNumber ) => l_LayerPadSuppress`

#### Description

Returns pad suppress layer characteristic for a layer or design. Pad suppression is not available in symbol editor.

Name dielectric layers will appear in the list unlike the pad suppress dialog.

#### Arguments

| Name | Description |
|---|---|
| `nil` | Return all layers |
| `t_layer` | Get suppress characteristics of named layer |
| `x_layerNumber` | Layer number (1st layer is 0) |

#### Value Returns

- `ll_LayerPadSuppress` - list of l_LayerPadSuppress for all etch layers. Layers are ordered from top to bottom.

- `l_LayerPadSuppress` - suppress characteristics of named layer. The symbols pin and via are optional and if present indicate pin and/or vias will be suppressed on that layer.

`(<t_layer> [<s_pin>] [<s_via>])`

#### Examples

- Get and print suppress state of all layers

- Get settings for layer "GND"

`suppress = axlPadSuppressGet(nil) foreach(item suppress printf("Layer=%s what= %L\n", car(item) cdr(item))) suppress = axlPadSuppressGet("GND")`

- Get settings for layer 1

`suppress = axlPadSuppressGet(1)`

#### See Also

axlPadSuppressSet, axlPadSuppressOkLayer, axlDBControl, axlSubclassRoute, axlPadOnLayer

### axlPadSuppressOkLayer

`axlPadSuppressOkLayer( t_layer/x_layerNumber ) => t/nil`

#### Description

Indicates if layer can be set for pad suppression. Only internal conductor and shape layers that are not set for negative artwork, support pad suppression.

#### Arguments

| Name | Description |
|---|---|
| `t_layer` | name of layer (e.g. "TOP") |
| `x_layerNumber` | layer number (starts at 0); |

#### Value Returns

`t` if layer can allows pad suppress; `nil` otherwise

#### Examples

The following are the same in the PCB tool but may not be in APD or SiP Layout:

`axlPadSuppressOkLayer("TOP")`

`axlPadSuppressOkLayer(0)`

#### See Also

axlPadSuppressGet

### axlPadSuppressSet

`axlPadSuppressSet( g_mode ll_LayerPadSuppress/'all/'none/nil ) => t/nil`

or

`axlPadSuppressSet( g_mode t_layer/x_layerNumber ls_options ) => t/nil`

#### Description

This modifies the pad suppression settings in the design. Allows control of both dynamic suppression setting (g_mode) and the individual layer options (subsequent arguments).

Notes:

- If passing a list of suppression layers then any errors in the list are ignored.

- Will mark dynamic shapes and DRC out of date.

- If enabling dynamic mode and no suppression layers are enabled the dynamic mode will be left disabled.

- Unlike the dynamic it will not automatically enable the display of padless holes.

- Pad suppression dialog should not be open when using this API.

#### Arguments

| Name | Description |
|---|---|
| `g_mode` | The possible values are: `nil` - maintain current pad suppression mode `'on` - turn pad suppression on `'off` - turn pad suppression off |

In the first format, second argument can have one of the following values.

| Name | Description |
|---|---|
| `'all` | Enable suppress on all supported layers |
| `'none` | Clear suppression on all supported layers |
| `nil` | leave suppression layers allow (typically used to toggle global mode) |
| `ll_LayerPadSuppress` | List of layers using same form as axlPadSuppressGet. |

Alternatively, use the second format to set suppression on single layers.

| Name | Description |
|---|---|
| `t_layer` | Layer name |

or

| Name | Description |
|---|---|
| `x_layerNumber` | Layer number when first layer is 0 |
| `ls_options` | May be `nil` or a list of `'via` and/or `'pin` |

#### Value Returns

`t` if success, `nil` a failure

#### Examples

- Enable dynamic suppression setting

`axlPadSuppressSet('on nil)`

- Enable all layers and dynamic mode

`axlPadSuppressSet('on 'all)`

- Delete suppression layer settings and turn off dynamic mode

`axlPadSuppressSet('off 'none)`

- Turn on via suppression on layer GND

`axlPadSuppressSet(nil "GND" '(via))`

- Turn on via & pin suppression on layer GND

`axlPadSuppressSet(nil "GND" '(via pin))`

- Turn off suppression on a layer GND

`axlPadSuppressSet(nil "GND" nil)`

- Turn on suppression for GND and VCC layers

`axlPadSuppressSet(nil '(("GND" via pin) ("VCC" via pin)))`

#### See Also

axlDBGridGet, axlDRCUpdate, axlDBDynamicShapes

### axlParamFilletDoc

p = axlGetParam("fillet")

axlSetParam(p)

#### Description

This function supports access to the fillet parameter record. The database is updated when axlSetParam is called.

| Name | Description |
|---|---|
| 1. | This parameter is not avaible in certain tiers of Allegro PCB Editor. |

| Name | Description |
|---|---|
| 2. | If dynamic is enabled, or if a parameter is changed while dynamic fillet is in effect, when axlSetParam is called, all fillet/tapes are updated. |

| Name | Description |
|---|---|
| 3. | If one of the min/max attributes is changed, the opposite value may be updated to enfoce the min <= max rule. |

#### Arguments

| Name | Description |
|---|---|
| `axlGetParam` | Requires "fillet" |
| `axlSetParam` | Requires return of axlGetParam |

#### Value Returns

- axlGetParam returns fillet parameter record

- axlSetParam returns parameter dbid if successful, nil otherwise

#### Examples

Enable dynamic fillet

#### See Also

`p = axlGetParam("param") p->dynamic = t axlSetParam(p)` axlGetParam, axlSetParam

### axlGetParam

`axlGetParam ( t_parm_name ) => ﬁo_paramDbid/nil`

or

`axlGetParam ( nil ) => lt_params`

#### Description

Gets the parameter `dbid` for a named object. Supported parameter names are shown below. For descriptions of attributes of a parameter, see are Chapter 2, "The Allegro PCB Editor Database User Model."

#### Arguments

| Name | Description |
|---|---|
| `nil` | Returns list of parameters supported |
| `t_parm_name` | Name of the parameter to seek. The legal naming conventions follow: `paramTextBlock`:`<#>` -- where `#` is 1-<N> (Example: `paramTextBlock:1`) where N is number of text blocks. `paramDesign paramDisplay paramLayerGroup`:`<name`- where name is a legal Allegro class name `paramLayerGroup:ETCH` - is obsolete for getting the cross-section layers, use new `axlXSectionGet()` family of APIs. If the design does not contain multiple cross-sections, this will still return the list of ETCH layers, and if there are no mask layers, this will be the list of all layers. It will be maintained for older Skill code to continue to work in single stackup designs with no mask layers.
 
 Note: Note in IC packaging products a pseudo class called WIRE with a single subclass called WIRE exists. This supports bondwires and is typically not displayed in the Options panel drop-down.
 Also, predefined ETCH subclasses BOND_TOP and BOND_BOTTOM, used for wirebond bondpads on chip-on-board components, are not included as they are not layers available for shapes, lines or routing. See switch `includeNonLayers` that controls this. `paramLayerGroup`:`<name>/paramLayer:<name> paramLayerGroup:name>/includeNonLayers` - ETCH class includes all non-mask layers of the cross-section. By default, `paramLayerGroup:ETCH` includes only those ETCH subclasses that are also cross-section layers. In order to get additional ETCH subclasses that are not layers, such as BOND_TOP and BOND_BOTTOM for chip-on-board, add switch `includeNonLayers`. `artwork`- List of film names `artwork:<filmName>`- A film given by `filmName testprep` - See `axlParamTestPrepDoc Fillet`- See `axlParamFilletDoc shapeStatic` and `shapeDynamic` - See `axlParamShapeDoc` |

#### Value Returns

| Name | Description |
|---|---|
| `o_paramDbid` | `dbid` for the requested parameter. |
| `lt_params` | Returns list of parameter names supported. |
| `nil` | Parameter requested not found. |

#### Examples

1) Return all param types supported

`axlGetParam(nil)` 2) Get etch layer (to find all members of the etch class).

`Skill> etch_parm = axlGetParam("paramLayerGroup:ETCH") param:123456 Skill> etch_parm->?? (objType "paramLayerGroup" name "ETCH" visible -1 nChildren 4 groupMembers ("TOP" "GND" "VCC" "BOTTOM") color -1 ) Skill> etch_parm->color -1 Skill> etch_parm->groupMembers ("TOP" "GND" "VCC" "BOTTOM")` 3) Access artwork records:

A) Get list of all possible records.

`Skill> p = axlGetParam("artwork") Skill> p->?? (objType "artwork" nChildren 4 groupMembers ("TOP" "GND" "VCC" "BOTTOM")` B) Get information on film record "VCC".

`r = axlGetParam("artwork:VCC") Skill> r->?? (objType "artwork" groupMembers ("ETCH/VCC" "PIN/VCC" "VIA CLASS/VCC") vectorBasedPad t suppressShapeFill t useApertureRotation nil drawMissingPadApertures nil suppressUnconnectPads t fullContact nil mirrored nil shapeBoundingBox 100.0 offset (0.0 0.0) rotation 0 undefineLineWidth 0.0 negative t name "VCC" )` C) Delete a TOP parameter record.

`axlDeleteObject(axlGetParam("artwork:TOP"))` 4) Design (`paramDesign`) modification.

`axlDBChangeDesignOrigin: change design origin axlDBChangeDesignExtents: change extents axlDBChangeDesignUnits: change units and/or accuracy` Also see `axlParamDesignDoc`

#### See Also

axlSetParam, and axlIsParamType

### axlSetParam

`axlSetParam ( od_paramDbid ) => rd_paramDbid/nil`

#### Description

This allows applications to modify certain aspects of Allegro parameters. After a parameter has been retrieved, attributes of it can be changed locally. Those changes can then be put back into the database using `axlSetParam`.

#### Arguments

| Name | Description |
|---|---|
| `od_paramDbid` | Parameter id returned from axlGetParam. Modify the parameters to be changed then call axlSetParam function to update the database. |

#### Value Returns

| Name | Description |
|---|---|
| `rd_paramDbid` | Returns the input parameter id if successful |
| `nil` | Database was not modified. |

#### Examples

| Name | Description |
|---|---|
| 1. | Change visibility (note it is easier to use axlVisibleSet to do this) |

`(setq etch_top (axlGetParam "paramLayerGroup:ETCH/paramLayer:TOP"))`

`=>param:123456`

; is layer visible ?

`etch->visible`

`t`

; blank it

`etch_top->visible = nil`

`t`

`(axlSetParam etch_top)`

`=>param:123456`

; layer is now invisible

`etch_top->visible`

`nil`

| Name | Description |
|---|---|
| 2. | Change accuracy |

`p = axlGetParam("paramDesign")`

`p->accuracy = 3`

`axlSetParam(p)`

Color Access

### axlColorDoc

#### Description

axlColorDoc

Allegro supports two color access methods: pre-defined colors and Allegro database colors. Not all Allegro based programs support access to Allegro database colors. (This is only supported by the graphics editors.)

Pre-defined colors are set and accessed by their symbols:

- `'black`

- `'white`

- `'red`

- `'green`

- `'yellow`

- `'blue`

- `'multivalue` - use `dfor` fields where value not the same

- `'button` - current color of button faces (grey)

In addition, graphics editors support access to the colors used for Allegro layers. These are integer numbers.

AXL API calls such as `axlLayerGet("class/subclass")` or its primitive form

`axlGetParm("paramLayerGroup:<class>/paramLayer:<subclass>")`

return the current color setting of a layer via the color attribute call.

#### Arguments

none

#### Value Returns

none

#### Examples

`p = axlLayerGet("etch/top") p->color -> 2` These colors currently range between 1 and 24 with 0 reserved for the background color.

Interfaces supporting setting color are mostly form based. For there interfaces see:

- `axlFormDoc`

- `axlFormColorize`

- `axlFormGridDoc`

- `axlGRPDoc`

### axlColorGet

`axlColorGet( x_number/background ) => lx_rgb/nil`

or

`axlColorGet( 'count) => x_count`

or

`axlColorGet( 'all) => llx_rgb`

or

`axlColorGet( 'pattern ) => x_count`

#### Description

Get color palette. Supports the following modes:

- If passed, an index less the color count returns a list containing the red, green, blue palette values for that color index. These are integer values between `0` (no color and `255` (maximum color). For example, a value of `255 255 255` is white. Or if passed, '`background` returns the palette for the background.

- If given `'count` returns the current size of the database palette (currently always 24).

- If passed 'all returns a list of list (red, green, blue) for all entire database palette EXCEPT the background.

- Returns number of patterns supported (includes default solid).

The color index is the number assigned to each layer in Allegro PCB Editor. (see `axlVisibleGet`).

#### Arguments

| Name | Description |
|---|---|
| `x_number` | Color number. |
| `'background` | Get background color. |
| ``count` | Query current database color palette size. |
| ``all` | Get entire database color palette (except background). |

#### Value Returns

| Name | Description |
|---|---|
| `x_count` | Size of database palette. |
| `nil` | Error. |
| `lx_rgb` | A palette. |
| `llx_rgb` | The entire database palette. |

#### Examples

Get red/green/blue of color 2:

`clr = axlColorGet(2)`

Get background color:

`bground = axlColorGet(`background)`

Get number of colors:

`cnt = axlColorGet(`count)`

Get all red/green/blue color settings except background:

`all = axlColorGet(`all)`

Get number of display patterns supported

`cnt = axlColorGet(`pattern)`

#### See Also

axlColorSet, axlVisibleGet

### axlColorShadowGet

`axlColorShadowGet( g_option ) => t/nil/x_percent`

#### Description

Provides the options of shadow mode.

#### Arguments

| Name | Description |
|---|---|
| `g_option` |  |
| `'mode` | Shadow mode status (`t` is on, `nil` is off). |
| `'activeLayer` | Active layer dimming enabled (`t`). This is called "Dim active layer in Options panel. |
| `'highlight` | This is called "Dim color assignments" in the Options panel |
| `'percent` | Current brightness percentage (0 to 100). |
| `'custom` | Custom colors, these are not shadowed. |

#### Value Returns

| Name | Description |
|---|---|
| `t/nil` | Shadow or active layer mode on or off. |
| `x_percent` | Brightness percentage. |

#### Examples

Is shadow mode on:

`axlColorShadowGet('mode)`

Is shadow mode percent:

`axlColorShadowGet('percent)`

#### See Also

axlColorSet, axlColorShadowSet

### axlColorShadowSet

`axlColorShadowSet( g_mode t/nil ) => t/nil`

or

`axlColorShadowSet( 'percent x_percentage ) => t/nil`

#### Description

Sets the shadow mode options. These are equivalent to the color commands in the shadow mode box under the Display group.

The Mode Options are:

- The mode option is either `t` or `nil` to turn shadow mode on or off.

- The activeLayer option is either `t` or `nil` to automatically dim the active layer. This is called "Dim active layer in Options panel.

- The highlight can be `t` or `nil` to dim highlighted objects. This is called Dim color assignments in the Options panel.

- The percent option sets the dimness (`0`) to brightness (`100`) percentage.

Note: On graphics or display combinations, shadow values of less than 40 percent disappear into the background. For example, you have what appears to be black on black.

After you finish all the color changes, call `axlVisibleUpdate` to update the display.

This interface is disabled if you set the display_noshadow environment variable.

#### Arguments

| Name | Description |
|---|---|
| `g_mode` | The possible values are: `'mode` - Enable or disable shadow mode. `'highlighted` - Enable or disable shadow mode for highlighted objects. `'activeLayer` - Enable or disable active layer dimming. `'percent` - Set shadow mode percentage (0 to 100) |

#### Value Returns

| Name | Description |
|---|---|
| `t` | If successful. |
| `nil` | An argument error. |

#### Examples

Is shadow mode on:

`axlColorShadowSet('mode t)`

Is shadow mode percent:

`axlColorShadowSet('percent 20)`

#### See Also

axlColorSet, axlColorShadowSet, axlVisibleUpdate

### axlColorLoad

`axlColorLoad( t_file/nil ) => t/nil`

#### Description

Loads an Allegro PCB Editor color file (default .`col` file). Master color file is located at `<cdsroot>/share/pcb/text/lallegro.col`.

File format is:

`#``Comment if in first column.`

`#N``Next line with a number is number of colors (currently only 24 is supported). This should appear first in the file.`

`Number format`

`#Number`

`24`

`#B - next line with a number is background color. This should appear after color number. Format of color line must be:`

`(name is currently ignored):`

`0 <red> <green> <blue> [<name>]`

`EXAMPLE of background format setting it to black`

`#Background Color`

`0 0 0 0`

`#I - next set of lines sets the colors. These should always appear last in the file. We will read until the first color number that exceeds the color number (currently hardcoded as 24) or the end of file is reached. The order the colors appear in the file determines the initial color [priority (highest (first) to lowest (last)].`

`Format is:`

`<color number> <pen number> <red> <green> <blue> [<name>]`

`EXAMPLE:`

`1 1 255 255 255 White`

`2 2 14 210 255 LtBlue`

`<color number>: entry in color table. This is the color number referenced by the allegro subclass (axlLayerGet)`

`<pen number>: Used by Allegro plot (UNIX) to control what pen to use during plotting. Not applicable on Windows.`

`<red> intensity of red to blend into color 0 to 255`

`<green> intensity of green to blend into color 0 to 255`

`<blue> intensity of blue to blend into color 0 to 255`

`<name> (optional) name of color, currently not used by Allegro but sigxp takes advantage of the name to auto-assign colors.`

Call `axlVisibleUpdate` to update the display after you finish manipulating the colors.

In Allegro PCB Editor, you need the color file to start a new design. Opening existing databases uses the color table stored in that database. A new database created, when Allegro PCB Editor is already running, copies the color table from the previous database.

#### Arguments

| Name | Description |
|---|---|
| `s_file` | Color file name to load. |
| `nil` | Uses `lallegro.col`. If no directory path, Allegro PCB Editor uses the LOCALPATH environment variable to find the file. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | If loaded file. |
| `nil` | File not found or error in loading file. |

#### Examples

Load user-defined default color. Overriding and setting current board values:

`axlColorLoad(nil)`

`axlVisibleUpdate(t)`

#### See Also

axlColorSave, axlColorSet.

### axlColorOnGet

`axlColorOnGet( g_item ) => t`

#### Description

This function is obsolete. Due to change in display model, switching off colors is no longer supported.

#### Arguments

Ignored

#### Value Returns

always `t`

### axlColorOnSet

`axlcolorOnSet( g_item g_state ) => t`

#### Description

This is an obsolete command. Due to changes in the viewing model, now you cannot turn off a color in Allegro PCB Editor.

#### Arguments

Items are ignored.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Success always. |

### axlColorPriorityGet

`axlColorPriorityGet( g_item [g_item2] ) => nil`

#### Description

Due to the changes in color model of Allegro PCB Editor, this command is now obsolete. Instead of this command, use axlLayerPriorityGet.

#### Arguments

Items are ignored.

#### Value Returns

`nil`

#### See Also

axlColorSet

### axlColorPrioritySet

`axlColorPrioritySet( g_item [g_item2] ) => t`

#### Description

Due to the changes in color model of Allegro PCB Editor, this command is now obsolete. Instead of this command, use axlLayerPrioritySet.

#### Arguments

Items are ignored.

#### Value Returns

`t`

#### See Also

axlColorSet

### axlColorSave

`axlColorSave( t_file/nil ) => t/nil`

#### Description

Saves current design colors to specified file.

#### Arguments

| Name | Description |
|---|---|
| `t_file` | File name. If `nil`; saves to `<HOME>/pcbenv/lallegro.col.` If no extension, uses .`col` extension. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Successful. |
| `nil` | Failed to save. |

#### Examples

Save current design color settings:

`axlColorSave("mycolor")`

#### See Also

axlColorSave,axlColorSet

### axlColorSet

`axlColorSet( x_number/'background l_rbg ) => t/nil`

or

`axlColorSet( 'all ll_rgb ) => t/nil`

#### Description

Sets red, green, blue palette for a color number or background.

Modes supported:

- Color number (`x_number`) and red/green/blue list. `x_number` must be between one and `axlColorGet('count)`, or '`background` sets red/green/blue as the background color.

- `'all` takes a list of red/green/blue values and sets colors starting at one to the end of the list. Intended to use with `axlColorGet('all)` to save or restore color values.

Red/green/blue colors are values between `0` (least intensity) to `255` (maximum intensity).

After color changes are made, call `axlVisibleUpdate` to update the display.

Color model:

A color (or colorNumber) in Allegro PCB Editor has the following attributes:

- A palette of red, green and blue values between `0` and `255`. `0` adds none of the primary color to the mixture while `255` adds the maximum. For example, `0,0,0` is black and `255,255,255` is white. The color mixture is controlled using the palette section of the color command.

- Each color number can be assigned to a layer. Multiple layers will have the same color number, because there are more layers than colors.

- Allegro PCB Editor supports setting a background palette value. Grids, ratsnest, temporary highlight can have a color number assigned via `axlDBControl`.

Color services:

| Name | Description |
|---|---|
| `axlColorSet` | This routine. |
| `axlColorGet` | Get red, green, or blue of one or more color numbers. |
| `axlColorShadowGet` | Shadow mode options. |
| `axlColorShadowSet` | Set shadow mode options. |
| `axlLayerPrioritySet` | set a layer to a display priority |
| `axlLayerPriorityGet` | get a layer's current priority |
| `axlLayerPriorityClearAll` | clear all layer priorities (restore to default) |
| `axlLayerPrioritySaveAll` | save existing priority table |
| `axlLayerPriorityRestoreAll` | restore saved priority table |
| `axlColorSave` | Save color values to file. |
| `axlColorLoad` | Load color values from file. |
| `axlUIColorDialog` | Standard color chooser dialog box. |
| `axlDBControl` | Miscellaneous color number assignments (for example, highlight). |
| `axlLayerGet` | Get layer (class/subclass) attributes (control color) number and visibility for individual layers. |
| `axlLayerSet` | Set color number or visibility for a layer. |
| `axlVisibleLayer` | Set visibility of layer. |
| `axlIsVisibleLayer` | Provides the layer visibility. |
| `axlVisibleGet` | Get visibility set for design. |
| `axlVisibleSet` | Set visibility set for design. |
| `axlVisibleDesign` | Global design visibility control. |
| `axlVisibleUpdate` | Update windows with color changes. |

#### Arguments

| Name | Description |
|---|---|
| `x_number` | Color index. |
| `'background` | Set background color. |
| `'all` | Set colors based upon a list starting at color number one. |
| `l_rgb` | Red/green/blue lists; three integers. |
| `ll_rgb` | Lists of red/green/blue values. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Successful. |
| `nil` | An error; wrong arguments: color number is less then one or greater than maximum. |

#### Examples

Set color number three same as color two:

`clr = axlColorGet(2)`

`axlColorSet(3 clr)`

`axlVisibleUpdate(nil)`

Set first three colors:

`axlColorSet('all '((10 10 10) (40 40 40) (100 100 100)))`

### axlCVFColorChooserDlg

`axlCVFColorChooserDlg( [x_color_index] [g_show_hilite] [x_hilite_flag] [x_bitmap_index] ) => t/nil`

#### Description

Displays color palette modal dialog. Color wells reflect current design colors.

#### Arguments

| Name | Description |
|---|---|
| `x_color_index` | Color index to initialize palette dialog. Values 0 to 191. |
| `g_show_hilite` | Specifies whether or not the highlight check box is to be displayed. If the value is set to:
 t - displays the highlight check box. `nil/default` - highlight check box is not displayed. |
| `x_hilite_flag` | Highlight state to initialize highlight check box (if displayed). Pass 1 or 0. |
| `x_bitmap_index` | Bitmap index to initialize palette dialog. Values 0 to 15. |

#### Value Returns

| Name | Description |
|---|---|
| `list` | containing one or two int values for user color palette selection and highlight check box selection. if `g_show_hilite` is not `nil`, list contains the two values, or else list contains color index only. |
| `nil` | if user cancels the form or error occurred. |

### axlClearObjectCustomColor

`axlClearObjectCustomColor( [lo_dbid] ) => t/nil`

#### Description

Clear custom color of dbids

#### Arguments

| Name | Description |
|---|---|
| `lo_dbid:` | List of dbids to clear custom color. |

#### Value Returns

| Name | Description |
|---|---|
| `t/nil:` | Returns `t` if at least one object custom color was cleared. 
 Returns `nil` otherwise. |

#### Examples

See axlCustomColorObject for examples

#### See Also

axlCustomColorObject

### axlCustomColorObject

`axlCustomColorObject( [lo_dbid] [g_custom_color] ) => t/nil`

#### Description

Custom color the provided dbid or list of dbids. Objects supported are nets, symbol instances, pins, and external DRCs.

The color index is between 1 and `axlColorGet(`count)`. The index references a RGB value in the Allegro Color table. The RGB values can be viewed or modifed via axlColorGet.

Custom colors need to be enabled (see axlDBDisplayControl) to be viewed.

#### Arguments

| Name | Description |
|---|---|
| `od_dbid` | list of DBIDS or one DBID |
| `g_custom_color` | Color index to be used to set custom color. If the value is `nil`, perm highlight will be used. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Something was custom colored. |
| `nil` | No valid dbids. |

#### Examples

The example covered in this section uses `axlCustomColorObject` and `axlClearObjectCustomColor` functions to respectively, set and clear custom color of database elements during interactive commands.

The following example does the following:

- Defines the function highlight Loop.

- Loops on the function axlSelect gathering user selections to set/clear custom color.

- Custom colors objects using color 4.

- Waits then clears custom color.

The command can be stopped at any time by selecting Cancel or Done from the pop-up menu.

#### See Also

axlClearObjectCustomColor, axlDBDisplayControl, axlIsCustomColored

### axlLayerPriorityClearAll

`axlLayerPriorityClearAll( ) => t/nil`

#### Description

`(defun customColorLoop () axlSetFindFilter( ?enabled '("noall" "alltypes" "nameform") ?onButtons "alltypes") while( axlSelect() axlCustomColorObject( axlGetSelSet() 4) checkColor = axlIsCustomColored( car(axlGetSelSet()) ) axlSleep(1) axlClearObjectCustomColor( axlGetSelSet()) ) )` Clears all layer priority information in Allegro database. Use axlLayerPrioritySet for usage.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t:` | success |

#### See Also

axlLayerPrioritySaveAll, axlLayerPriorityRestoreAll

### axlLayerPriorityGet

`axlLayerPriorityGet( t_layer ) => x_priority/t_mapClass/nil`

#### Description

get layer's priority

Obtains layer priority, where 0 is normal (not set). Priority can range from 1 (highest) to 255 (lowest).

Depending on the argument value, the function operates in two modes:

- if `t_layer` is layer name (class / subclass), returns priority of that layer as an integer

- if `t_layer` is class name then returns the mapped layer

Note: Mapped layer groupings may change from release to release (e.g. future releases may choose to break up some class groupings).

#### Arguments

| Name | Description |
|---|---|
| `t_layer` | layer name (`<class>/<subclass>`) or class name (`<class>`) |

#### Value Returns

- `x_priority` - priority of layer (0 layer draws at normal priority)

- `t_mapClass` - class name used as lead group for provided class

- `nil` - error in layer name

#### Examples

- Get and fetch priority

`axlLayerPrioritySet("BOARD GEOMETRY/OUTLINE" 1)`

`prior = axlLayerPriorityGet("BOARD GEOMETRY/OUTLINE")`

- Get group class mapping of class Ref Des

`axlLayerPrioritySet("REF DES") -> "COMPONENT VALUE"`

#### See Also

axlLayerPrioritySet

### axlLayerPriorityRestoreAll

`axlLayerPriorityRestoreAll( ) => t/nil`

#### Description

Restores previously saved layer priority information. This function only works if a call to axlLayerPrioritySaveAll has been done already.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t:` | success |
| `nil:` | nothing to restore. |

#### See Also

axlLayerPrioritySaveAll, axlLayerPriorityClearAll

### axlLayerPrioritySaveAll

`axlLayerPrioritySaveAll( ) => t/nil`

#### Description

Saves all layer priority information to be restored later. Until a axlLayerPriorityRestoreAll is called, any subsequent calls to this function are no-op.

#### Arguments

None

#### Value Returns

| Name | Description |
|---|---|
| `t:` | success |
| `nil:` | this function has been called already but axlLayerPriorityRestoreAll has not been called yet. |

#### See Also

axlLayerPriorityClearAll, axlLayerPriorityRestoreAll

### axlLayerPrioritySet

`axlLayerPrioritySet( t_layer x_priority ) => t/nil`

#### Description

This changes the drawing priority of given layer. Priority is from 1 (highest) to 255 (lowest). Layers without priority in standard drawing order below all priority layers. The active layer is always drawn first.

Only one layer may be at a priority level, thus adding a new layer at a priority replaces the existing layer at that priority. For example, executing following line of code results in just the ASSEMBLY_TOP being drawn at priority 1 and OUTLINE returning to normal drawing order.

`axlLayerPrioritySet( "BOARD GEOMETRY/OUTLINE" 1)`

`axlLayerPrioritySet( "PACKAGE GEOMETRY/ASSEMBLY_TOP" 1)`

From priority level 1 each level must be set for lower priority levels to be enabled. For example, if you set a layer to priority level 2 but leave level 1 empty then level 2 is disabled until level 1 is assigned.

Classes may be grouped together in a class group with one class being the lead of that group. For example, all etch layers (ETCH, PIN, etc.) are mapped together into the stack-up group with class ETCH the lead. You can set the priority using class names but you cannot prioritized the different stack-up layers individually. This interface automatically maps a class name to its class group (see axlLayerPriorityGet to determine groupings).

You should do a axlVisibleUpdate after changing layer priority to have the display updated.

Note: Priority value of 0 means remove layer priority of the layer.

#### Arguments

| Name | Description |
|---|---|
| `x_layer` | layer name (i.e. "ETCH/TOP") |
| `x_priority` | priority value in the range of 1-255 and 0 means remove. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | success |
| `nil` | error in one of the arguments |

#### Examples

Set priority for class BOARD GEOMETRY and subclass OUTLINE:

`axlLayerPrioritySet("BOARD GEOMETRY/OUTLINE" 1)`

To temporarily force a set of layers to display on top, you should take the following steps:

- save existing layer table,

- clear existing layer priorities

- set your layer priorities

- draw objects

- restore old layer priority:

`axlLayerPrioritySaveAll()`

`axlLayerPriorityClearAll()`

`axlLayerPrioritySet() -- multiple times if needed`

`axlLayerPriorityRestoreAll()`

#### See Also

axlLayerPriorityClearAll, axlLayerPrioritySaveAll, axlLayerPriorityRestoreAll, axlLayerPriorityGet, axlMapClassName, axlVisibleUpdate

### axlIsCustomColored

`axlIsCustomColored ( o_dbid ) => x_customColor/nil`

#### Description

If object has custom color, will return the object custom color, otherwise nil.

#### Arguments

| Name | Description |
|---|---|
| `o_dbid` | An dbid for which custom color information is desired. |

#### Value Returns

| Name | Description |
|---|---|
| `x_customColor` | custom color or nil if object has no custom color or object does not support custom color. |

#### See Also

axlCustomColorObject

Database Layer Management

These functions allow easier access to layer attributes.

### axlClasses

`axlClasses( ) => lt_classes`

#### Description

Return list of classes.The is actually just:

`axlGetParam("paramLayerGroup")->groupMembers`

#### Arguments

Nothing

#### Value Returns

list of class strings

#### See Also

axlSubclasses, axlGetParam, axlMapClassName

### axlDBGetLayerType

`axlDBGetLayerType( t_layerName ) => t_layertype/nil`

#### Description

`axlClasses()` Retrieves the cross-section type of a given layer. This may be (Layer Type in define xsection form): `CONDUCTOR`, `DIELECTRIC`, `PLANE`, `SURFACE`, `DIESTACK` or `MASK`.

Note: See crosssection dialog for a current list.

#### Arguments

| Name | Description |
|---|---|
| `t_layername` | Layername is <class>/<subclass>. |

#### Value Returns

| Name | Description |
|---|---|
| `t_layertype` | Layer type string. |
| `nil` | Layer is invalid. |

#### Examples

`axlDBGetLayerType("ETCH/TOP") => "CONDUCTOR"`

#### See Also

axlXSectionGet

### axlGetXSection

`axlGetXSection( ) => ll_layers/nil`

#### Description

- This is obsolete, use new axlXSectionGet() family of APIs. The command will be maintained for older SKILL code but it will not be enhanced to support new dataReturns a list of all layers in the cross section found in the current drawing.

### axlIsEtchLayer

`axlIsEtchLayer( t_layer ) => t/nil`

#### Description

Determines if a layer is associated with the ETCH layers. Returns `t` if layer is associated with any of te ETCH layers -- `ETCH`, `PIN`,`VIA`, `DRC`, `VIA_KEEPOUT`, `ROUTE_KEEPOUT`, `ANTI_ETCH`, `BOUNDARY`, `CONSTRAINT_REGION`, `ROUTER_PLAN`, and `CAVITY`

#### Arguments

| Name | Description |
|---|---|
| `t_layer` | Layer name (e.g. "ETCH/TOP") or just class name ("ETCH") |

#### Value Returns

| Name | Description |
|---|---|
| `nil` | Not an etch associated layer |
| `t` | Is an etch associated layer |

### axlIsLayer

`axlIsLayer( t_layer ) => t/nil`

#### Description

`axlIsEtchLayer("PIN/TOP") axlIsEtchLayer("ETCH")` Determines if the `t_layer` exists. `t_layer` is a fully qualified layer name.

#### Arguments

| Name | Description |
|---|---|
| `t_layer` | Name of layer in format "<class>/<subclass>." |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Layer exists. |
| `nil` | Layer does not exist. |

### axlIsVisibleLayer

`axlIsVisibleLayer( t_layer ) => t/nil`

#### Description

Returns the visibility (`t/nil`) of a fully qualified layer.

#### Arguments

| Name | Description |
|---|---|
| `t_layer` | Name of layer in format "<`class`>/<`subclass`>". |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Layer is visible. |
| `nil` | Layer is invisible or not present. |

#### Examples

`axlIsVisibleLayer("pin/top")``⇒` t

### axlLayerCreateCrossSection

`axlLayerCreateCrossSection( t_Prev_layerName t_layerType t_materialType [t_subclassName] [t_planeType] ) => t/nil`

#### Description

This is obsolete, use axlXSectionCreate.

Adds a new cross-section layer to the design.

If `t_subclassName` is `nil` then an unnamed dielectric layer is created. It is suggested that you create unnamed dielectric layers if they are only required for signal analysis and board thickness calculations since using a name will create ETCH layer in the design.

#### Arguments

| Name | Description |
|---|---|
| `t_Prev_layerName` | Name of the layer above which the new layer is to be added |
| `t_layerType` | Type of layer to be added, such as Conductor or Surface. |
| `t_materialType` | Material of the layer. |
| `t_subclassName` | Optional parameter. Name of the new layer. |
| `t_planeType` | Optional parameter. Type of plane, either `Positive` or `Negative`. The default is `Positive`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Layer is created or already exists. |
| `nil` | Layer does not exist and could not be created. |

#### See Also

axlLayerCreateNonConductor, axlLayerGet, and axlXSectionGet

### axlLayerCreateNonConductor

`axlLayerCreateNonConductor( t_layerName ) => t/nil`

#### Description

Creates a new subclass for non-etch subclasses. AXL-SKILL restricts you from creating etch subclasses.

#### Arguments

| Name | Description |
|---|---|
| `t_layerName` | <`class`>/<`subclass`> |

#### Value Returns

| Name | Description |
|---|---|
| `t` | New subclass is created or, subclass already exists. |
| `nil` | New subclass is not created. |

#### Examples

`axlLayerCreateNonConductor("BOARD GEOMETRY/MYSUBCLASS")`

Creates a new subclass named `MYSUBCLASS`.

### axlLayerDelete

`axlLayerDelete( t_layerName/x_layerNumber ) => t/nil`

#### Description

This command deletes a cross section layer. While axlDeleteObject can be used to delete empty named layers, this API can delete both named and unnamed cross-section layers.The cross section has both ETCH layers and unnamed dielectric layers.The order of the cross section is returned by axlGetXSection, The `x_layerNumber` is the order within the cross-section with the first index number (e.g AIR) starting at 0.

The command can fail in the following scenarios.

- Deleting a named layer containing geometries (excluding pins or vias)

- Deleting top or bottom dielectric or TOP or BOTTOM etch layers

- Layer name does not exist

- Layer number is less then 0 or greater or equal to `length(axlGetXSection('count))`

#### Arguments

ETCH layer string or cross section index

#### Value Returns

`t` if layer is deleted, `nil` if failure

#### Examples

- The command to delete a layer named empty is:

`axlLayerDelete("EMTPY")`

- Delete the third cross section layer. On most designs this is an unnamed dielectric layer between TOP and the next etch layer.

`axlLayerDelete(3)`

#### See Also

axlLayerCreateNonConductor, axlDeleteByLayer, axlDeleteObject, axlGetXSection, axlXSectionDelete

### axlLayerGet

`axlLayerGet( t_layer ) => o_dbid/nil`

#### Description

Gets the layer parameter given the shortcut notation of <`class`>/<`subclass`>. This is an ease of use function that does:

`axlGetParam("paramLayerGroup:<class>/paramLayer:<subclass>)`

This does NOT allow access to the cross section data (example material or thickness). It allows easier access to color and visiblity of a layer.

- You can use the groupMembers attribute of result -- `result=axlGetParam("paramLayerGroup:<class>")` -- to iterate over all subclass of a class.

#### Arguments

| Name | Description |
|---|---|
| `t_layer` | Name of layer in format "<`class`>/<`subclass`>". |

#### Value Returns

| Name | Description |
|---|---|
| `o_dbid` | Layer parameter `dbid`. |
| `nil` | Layer is not present. |

#### Examples

Changes color of top etch layer.

`q = axlLayerGet("ETCH/TOP")`

`q->color = 7`

`axlLayerSet(q)`

`axlVisibleUpdate(t)`

#### See Also

axlGetParam

### axlLayerViaLabel

`axlLayerViaLabel( t_layerName/x_layerNumber ) => t_viaLabel/nil`

#### Description

Reports via label for a layer. A via label either defaults to the layer number, or can be assigned by the user through the cross section. You can query the cross section for an override.

#### Arguments

ETCH layer string or cross section index

#### Value Returns

Via label name; or `nil`, in case of an error

#### Examples

- To return the via label of a layer called TOP

#### See Also

`axlLayerViaLabel("TOP")-> 1` axlXSectionGet

