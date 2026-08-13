<!--
source: algroskill/06intedt.md
part: 2/2
estimated_tokens: 4204
-->

|  |
| --- | ---
| `usage` | (string) padstack usage. See[axlPadstackUsageTypes](#877499 "5")(). If this parameter is not provided, code determines type based on padstack characteristics.
| `fixed` = | `(t/nil)` internal fixed flag
| `spanLockCount` | `(t/nil` Default value is `nil`. If `t`, padstack does not expand or contract if layers are added or deleted. Default it expands/contracts.
| `uvia` | `(t/nil)` if padstack is of type `bbvia` set as sub-type micro-via. Superseeded by usage type.
| `keepout` | `(t/nil)`. Obsolete for 17.0. Use new 'KEEPOUT pad layer type
| `pluralVia` | `(t/nil)`. Create padstack as a plural via (multi-net). Only through hole padstacks can have this setting.
| `holeType` | (symbol) the hole type. Allowed symbols are 'CIRCLE\_DRILL, 'SQUARE\_DRILL, 'OVAL\_SLOT, 'RECTANGLE\_SLOT.  Defaults to CIRCLE\_DRILL if drill diameter is provided.
| `plating` | (symbol) plate status of drill hole Symbols are: 'PLATED, 'NON\_PLATED or nil
| `drillDiameter` | (float) drill hole finished diameter.
| `drillToolSize` | (string) Drill tool size, which is used as an identifier. Default is blank.
| `slotSize` | ((f\_width f\_height)) size of slot hole. Use this instead of drillDiameter for SLOT types.   The f\_width or "Y size" is the drill size.  The f\_height or "X size" or drill travel.
| `holeTolerance` | ( (f\_pos f\_neg) ) +/- hole tolerance  When a slot defines the X tolerance or route tolerance
| `holeToleranceY` | ( (f\_pos f\_neg) ) +/- hole tolerance  Applies only to slots and defines the Y or drill tolerance.
| `offset` | ( (f\_x f\_y) ) drill hole offset
| `multiDrillData` | list for multiple drill data which is:  ( (x\_num\_rows nx\_um\_columns f\_clearance\_x   [f\_clearance\_y ["staggered"]]) )   data type is (int int float [float])
| `drillNonStandard` | (symbol) non-standard drill hole.   Supported symbols are:  'LASER\_DRILL, 'PLASMA\_DRILL, 'PUNCH\_DRILL, 'PHOTO\_DRILL, 'COND\_INK\_DRILL, 'WET\_DRY\_DRILL, 'OTHER\_DRILL.
| `figure` | `(symbol)` the drill figure. Allowed symbols are NULL, CIRCLE, SQUARE, HEXAGON, HEXAGON\_X, HEXAGON\_Y, OCTAGON, CROSS, DIAMOND, TRIANGLE, OBLONG\_X, OBLONG\_Y, RECTANGLE.   Note nil is treated as NULL.
| `figureSize` | ( (f\_width f\_height) ) size of drill figure
| `drillChar` | (string) drill characters. Maximum 3 characters.
| `holeCounterType` | (string) Counter hole type: "bore", "sink" or nil
| `holeCounterAngle` | (integer) Applies to Counter sink and indicates an angle between 1 and 90 degrees.
| `holeCounterDiameter (float`) | Counter hole diameter in design units
| `holeCounterDepth` | (float) Applies to Counter bore and indicates depth of the bore. Accuracy is maintained at a higher level then the current design.
| `holeCounterTolerance` | ( (f\_pos f\_neg) ) +/- counter hole tolerance.
| `backdrillDiameter` | (float) diameter in design units of backdrill finished hole
| `backdrillFigureName` | (symbol) the drill figure (see figure for allowed types)
| `backdrillFigureChar` | (string) backdrill characters (3 max)
| `backdrillFigureWidth` | (float) width of backdrill figure in design units
| `backdrillFigureHeight` | (float) height of backdrill figure in design units
Pad`(l_pad)` structure (up to 4 for each layer indicated by attribute type)

|  |
| --- | ---
| `layer` | = (string) etch layer name (e.g. "TOP") or "DEFAULT\_INTERNAL" if you want one pad layer to map to all internal layers between the top and bottom of the padstack.
| `type` | = (symbol) pad type. Allowed symbols are: KEEPOUT, ANTIPAD, THERMAL or REGULAR. nil is treated as REGULAR.
| `figure` | = (symbol) the pad figure For allowed symbols, see axlPadFigureTypes API.  If NULL we check the figureSize and automatically assign a figure type. If you assign a type the figureSize must match that type. For example, a SQUARE must have both width and height of the same value.  For shape symbol use the name of the ssm (minus extension and path) to figure.  For example, if you have a shape symbol called "`myshape`" then it would be `'?figure "myshape"'`.  For an Anti-pad shape (fsm) assign the symbol 'FLASH and assign the fsm file (minus extension and path to the flash name. For example, symbol "myflash" would be: `'?figure 'FLASH ?flash "myflash"'` For either a shape or flash, the symbol must be located via PADPATH. Also the `?figureSize` attribute must be the extents of the symbol or larger.
| `flash` | = (string) the pad aperture flash name.  Reference a flash shape symbol name or nil for no flash (fsm file).
| `figureSize` | = ( (f\_width f\_height) ) height and width of the figure. For a circle, you only need to assign diameter to either height/width, the other can be 0.
| `offset` | = ( (f\_x f\_y) ) offset from the padstack origin sides. Octagon pad only: Number of sides. Ranges between 6 and 64 as an even integer.  inside Donut pad only: inside dimension as a floating point user unit  radius ROUNDED\_RECTANGLE and CHAMFERED\_RECTANGLE pad only, corner radius as a floating point user unit.  corners ROUNDED\_RECTANGLE and CHAMFERED\_RECTANGLE pad only, a dash separated string indicating corners chamfered:  UR - upper right  UL - upper left  LR - lower right  LL - lower left  `nil` if pad type does not support  Example:`"UR-LR"` means chamfer Upper Right and Lower Left corners.
#### PROGRAMMING NOTES:

* N\_SIDED\_POLY - figureSize uses the smaller of width and height and this maps to diameter. Requires sides and if not present pad is turned into a circle. Sides must be an even number between 6 and 64. If sides is 0 a CIRCLE pad is created.

* ROUNDED\_RECTANGLE CHAMFERED\_RECTANGLE - Requires radius and corners string. Radius cannot be larger than half the smaller of height or width. If radius is 0 or corners string does not match any corners then a RECTANGLE pad is created.

* DONUT - figureSize uses the smaller of width and height and this maps to outside diameter. Requires an inside diameter that must be smaller then the outside diameter. If inside diameter is zero then a CIRCLE pad is created

* To create an adjacent layer route keep-out pad, use the following options for make\_axlPadStackPad

* `?layer 'adjacent`

* `?type 'KEEPOUT`

* To create create Coverlay pad layers

* use strings for ?layer "COVERLAY\_TOP" or "COVERLAY\_BOTTOM"

* ?type is ignored

* To create backdrill pad layers use:

* ?layer 'backdrillStart

|  |  |
| --- | --- | ---
|  |  | ?type "REGULAR" - larger pad for drill start layer (positive)
|  |  |
| --- | --- | ---
|  |  | ?type "ANTI" - larger pad for drill start layer (negative layers)
* ?layer 'backdrillClearance

|  |  |
| --- | --- | ---
|  |  | ?type "ANTI" - pad size for internal backdrill layers for negative layers
|  |  |
| --- | --- | ---
|  |  | ?type "KEEPOUT" - generate a KEEPOUT for positive layers for backdrill layers.
* ?layer 'backdrillSoldermask - soldermask pad to substitute for drill

* Shapes and flash assignment symbol rules:

|  |  |
| --- | --- | ---
|  |  | 'REGULAR - shape symbols (flash symbol name can be set of legacy Gerber support)
|  |  |
| --- | --- | ---
|  |  | 'THERMAL - flash symbols
|  |  |
| --- | --- | ---
|  |  | 'ANTIPAD - shape symbol (flash symbol name can be set of legacy Gerber support)
|  |  |
| --- | --- | ---
|  |  | 'KEEPOUT - shape symbol
|  |  |
| --- | --- | ---
|  |  | Mask layers - either flash or shape symbols
> A shape symbol can contain one shape with NO voids.

> A flash symbol supports multiple shapes with voids.

* User mask layer support requires a call to axlPadUserMaskLayers with the 'create option to insure a user mask layer exists in the design. If you know that the user mask layer already exists, you do not need to make the call.

* Backdrill data can be seeded by the global design parameters. Padstacks with their backdrill data obtained this way show these values but they are not saved to the disk padstack file (.pad).

#### Arguments

|  |
| --- | ---
| `t_name` | Padstack name.
| `r_drill` | Drill hole data for the padstack.  **Note:** As with all SKILL defstructs, use the constructor function, `make_axlPadStackPad`, to create instances of `axlPadStackPad`. See [Create Shape Interface](03dbcre8.html#367513 "15") for an example.
| `l_pad` | Pad definition data for the padstack.  **Note:** As with all SKILL defstructs, use the constructor function `make_axlPadStackPad` to create instances of `axlPadStackPad`. See [Create Shape Interface](03dbcre8.html#367513 "15") for an example.
| `g_nocheck` | `Optional.` t disables checks of the padstack definition. nil executes the following checks of the padstack definition:   - Contiguous pad definitions - Anti-pad / thermal-relief pad definitions - Existence of two pads with a drilled hole - A drilled hole with the existence of two pads
#### Value Returned

|  |
| --- | ---
| `l_result` | `dbid` of the padstack created.
| `nil` | Nothing is created.
#### See Also

[axlPadstackEdit](#877090 "5"), [axlLoadPadstack](03dbcre8.html#836368 "15"), [axlDBCopyPadstack](14dsnctl.html#706488 "14"), [axlPadstackToDisk](03dbcre8.html#900567 "15"), [axlDBGetPad](07dbaccs.html#700355 "6"), [axlPadUserMaskLayers](#877553 "5"), [axlPadFigureTypes](#877610 "5"), [axlPadstackUsageTypes](#877499 "5"), axlPadDbidDoc

#### Examples

* Surface Mount Padstack Example

* Adds a surface mount padstack having a 25 by 60 rectangular pad.

> ```
> pad_list = cons(make_axlPadStackPad(?layer "TOP", ?type 'REGULAR,?figure 'RECTANGLE, ?figureSize 25:60) nil)
> ```

> `ps_id = axlDBCreatePadStack("smt_pad", nil, pad_list t)`

* Additional examples in:

> `<cdsroot>/share/pcb/examples/skill/dbcreate/pad.il`

### axlPadFigureTypes

`axlPadFigureTypes() => lt_names`

#### Description

Returns list of strings of supported pad figure types.Not all pad types and layers may support a figure type. This is a documentation support function.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `lt_names` | List of permitted pad figure types
#### Examples

> `axlPadFigureTypes()`

### axlPadstackEdit

`axlPadstackEdit(nilnil)==> l_attributes`

`axlPadstackEdit(o_dbidPadstack/t_Padstacks_nameg_value)==> t/nil`

`axlPadstackEdit(o_dbidPadstack/t_Padstack[[s_name g_value] .... ])==> t/nil`

#### Description

Inquire and set display options. Edits global settings of an existing padstack.

This edits the padstack definition, this means that any changes made applies to all instances of the padstacks (pins and vias) in the design.

Supports the following modes:

* If first two arguments are`nil`, command returns a list of all editable attributes.

* If padstack, attribute, and new value are provided, changes one attribute of padstack.

* If padstack, and a list of attributes with new values are provided change all the items specified in the padstack. This is the most efficient method for changing multiple items on a single padstack.

* Order is important, so if you are changing a CIRCULAR drill to a slot then you must provide the holeType, then drillSizeWidth then drillSizeHeight.
  For best performance if changing multiple items in a single padstack use the list mode to change all items in one call.

Currently only global padstack settings are supported. Editing pad layer characteristics in not allowed. Certain changes set DRC out of date and dynamic shapes out of date.

Attributes currently supported (all Equivalent items are field names in pad\_designer):

* **Side Effects**
* DRC is out of date and dynamic shapes are disabled
* DRC is out of date and dynamic shapes are disabled
* DRC is out of date and dynamic shapes are disabled.
* DRC is out of date and dynamic shapes are disabled.
* None
* DRC is out of date and dynamic shapes are disabled.
* slot to drill; drillDiameter inherits drillSizeWidth.
* drill to slot; both drillSizeWidth and drillSizeHeight inherit drillDiameter
* None
* DRC is out of date and dynamic shapes are disabled.
* None
* None
* None
* Can only be set for through hole padstacks. Padstack cannot be in use in the design
* None
* None
* None
* None
* None
* None
* None
* None
* None
* padstacks with this options may create disconnects when new layers are added
* DRC is out of date and dynamic shapes are disabled.
* none

#### Arguments

|  |
| --- | ---
| `o_dbidPadstack` | dbid of a padstack (note VIA and PIN dbids are not supported)
| `t_Padstack` | Name of padstack
| `s_name` | Symbol name of attribute to change
| `g_value` | New value
| `[[s_name g_value] .. ]` | list of name/value pairs
#### Value Returned

* `ls_names` - If name is nil then returns a list of all controls.

* `t`/`nil` - if t successful in updating padstack, nil an error

#### Examples

Finds a padstack using the ashOne share ware skill. Note that selection will return a pin or via and you must get the padstack from the definition attribute.

> `p = ashOne()`

> `padstack = p->definiton`

* Set drill characters

> `ret = axlPadstackEdit(padstack 'drillChar "abc")`

> > > or its equivalent

> `ret = axlPadstackEdit(padstack '((drillChar "abc")))`

* Set tolerance

> `ret = axlPadstackEdit(padstack 'holeTolerance '(1.2 1.3))`

* Set tolerance same for + and -

> `ret = axlPadstackEdit(padstack 'holeTolerance 1.5)`

* Set drill symbol data

> ```
> data = '((drillFigureName "RECTANGLE") (drillFigureHeight 20) (drillFigureWidth 10) (drillChar A))
> ```

> `ret = axlPadstackEdit(padstack data)`

* Get list of all editable padstack parameters

> `lst = axlPadstackEdit(nil nil)`

#### See Also

[axlDBCreatePadStack](#876722 "5"), [axlLoadPadstack](03dbcre8.html#836368 "15"), [axlDBCopyPadstack](14dsnctl.html#706488 "14"), [axlReplacePadstack](#31833 "5")

### axlPadstackSetType

`axlPadstackSetType(o_padstack/t_padstackg_uviaBbvia) -> t/nil`

`axlPadstackSetType(o_padstack/t_padstackg_typeg_value) -> t/nil`

#### Description

Changes a padstack type. In its 2 argument mode is the same as:

`axlPadstackSetType(padstack 'type g_uviaBbvia)`

Permits changing the type of via.

> `'type`

> > Changes a bbvia padstack to a micro via and vice versa. Uvia types can be managed separately in the constraints system.This has no effect if the padstack is used with Pins. Values are '`bbvia` or '`uvia`.

> `'keepout`

> > Obsolete in 17.0. Create a keepout pad layer type of KEEPOUT.

> Marks DRC out-of-date if successful.

#### Arguments

|  |
| --- | ---
| `o_padstack` | padstack dbid
| `t_padstack` | padstack name
| `g_type` | mode (either 'type or 'keepout)
| `g_value` | appropriate setting (see above)
#### Value Returned

|  |
| --- | ---
| `t` | change successful
| `nil` | failed. Not a padstack, padstack not in database, type not recognized or padstack not a bbvia or uvia.
#### Examples

Change padstack named VIA to a micro via

> `axlPadstackSetType("VIA" 'type 'uvia)`

#### See Also

[axlDBCreatePadStack](#876722 "5"), [axlPadstackEdit](#877090 "5")

### axlPadstackUsageTypes

`axlPadstackUsageTypes() => lt_names`

#### Description

Returns list of strings of supported padstack usage types. This is a documentation support function.

#### Arguments

None

#### Value Returned

* List of strings

#### Examples

> `axlPadstackUsageTypes()`

### axlPadUserMaskLayers

`axlPadUserMaskLayers(['max]) =>lt_names/x_cnt`

`axlPadUserMaskLayers('createt_user_mask_layer) =>t/nil`

#### Description

Supports following modes:

* if argument returns list of user mask layers in design

* `'max` symbol option reports the maximum number that we support.

* `'create` adds a new user mask layer; requires a name

User mask naming:

If you use \_TOP and \_BOTTOM suffixes, then you will get mirror support. This means if you mirror a VIA with a user mask defined on xxx\_TOP then it will be mirrored to the bottom. See axlDBControl('mirrorUserMask). With the mirror mask option enabled, the opposite side mask is auto-created.

#### Arguments

|  |
| --- | ---
| `` `max `` | Optional. If provided, returns the maximum number of mask layers supported.
| `'create` | Create a new user mask layer, requires`t_user_mask_layer`
| `t_user_mask_layer` | Name of user mask layer
#### Value Returned

|  |
| --- | ---
| lt\_names | List of user mask names
| x\_cnt | Maximum number permitted to be defined
|  |
| --- | ---
| t/nil | In create mode, returns`t` if layer was created or exists, `nil` if failed to create. Failure can be due to:
* exhausted number of user mask layers available

* name is illegal

#### See Also

[axlDBCreatePadStack](#876722 "5"), [axlDBControl](14dsnctl.html#690074 "14")

#### Examples

* Typical use to get all layers defined

> `axlPadUserMaskLayers()`

* Return max that can be defined

> `axlPadUserMaskLayers('max) -> 32`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
