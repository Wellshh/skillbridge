<!--
source: algroskill/06intedt.md
part: 2/2
estimated_tokens: 2999
-->

### axlPadstackEdit

`axlPadstackEdit( nil nil ) => l_attributes`

or

`axlPadstackEdit( o_dbidPadstack/t_Padstack s_name g_value ) => t/nil`

or

`axlPadstackEdit( o_dbidPadstack/t_Padstack [[s_name g_value] ... ] ) => t/nil`

#### Description

Inquire and set display options. Edits global settings of an existing padstack.

This edits the padstack definition, this means that any changes made applies to all instances of the padstacks (pins and vias) in the design.

Supports the following modes:

- If first two arguments are `nil`, command returns a list of all editable attributes.

- If padstack, attribute, and new value are provided, changes one attribute of padstack.

- If padstack, and a list of attributes with new values are provided change all the items specified in the padstack. This is the most efficient method for changing multiple items on a single padstack.

- Order is important, so if you are changing a CIRCULAR drill to a slot then you must provide the holeType, then drillSizeWidth then drillSizeHeight.For best performance if changing multiple items in a single padstack use the list mode to change all items in one call.

Currently only global padstack settings are supported. Editing pad layer characteristics in not allowed. Certain changes set DRC out of date and dynamic shapes out of date.

Attributes currently supported (all Equivalent items are field names in pad_designer):

Table 5-2 
 Supported Controls

| Name | Description |
|---|---|
| usage | symbol or string with possible values as: `'Smd 'Through 'Through_pin``'Surface_pin``'Bbvia``'Through_via``'uvia 'Bond_finger``'Die_pad``'Fiducial 'Mechanical_hole``'Mounting_hole``'Slot`; Changes classification of padstacks. In some cases the use of the padstack may override the actual padstack usage type.
 Note: `Smd` and `Surface_pin` are identical but future releases will check that `Surface_pin` is only used for pins. Similarly, `Through`, `Through_via` and `Through_pin` are the same but future releases will support a check.
 
 Transition rules(types can be switched amoung themselves):
 Single layer: `Smd,`Surface_pin, Die_pad, Bond_finger, Fiducial
 Multi layer:Through, Through_pin, Through_via, Bbvia, uvia, Mechanical_hole, Mounting_hole, Slot
 Note: Future releases may tighten the transition rules.; Padstack Usage type or `'usage` attribute in the padstack dbid; DRC is out of date and dynamic shapes are disabled |
| drillDiameter | dbrep; Changes the drill diameter. Value must be a positive number and holeType must not be a slot. For multi-drill applies to all drills.; Drill diameter field; DRC is out of date and dynamic shapes are disabled |
| drillSizeWidth | dbrep; Changes the slot size width (x direction). Value must be a positive number and holeType must be a slot type. Usually done in association with drillSizeHeight.; Slot size X; DRC is out of date and dynamic shapes are disabled. |
| drillSizeHeight | dbrep; Changes the slot size width (y direction). Value must be a positive number and holeType must be a slot type. Usually done in association with drillSizeWidth.; Slot size Y; DRC is out of date and dynamic shapes are disabled. |
| drillToolSize | string; Sets the Drill tool size name. Not applicable if padstack does not have a drill.; Drill tool size; None |
| holeType | string; One of `"CIRCLE_DRILL"`, `"SQUARE_DRILL"`, `"OVAL_SLOT"` or `"RECTANGLE_SLOT"`. Changes hole type of padstack. If changing fundamental types:
 
 slot to drill; drillDiameter inherits drillSizeWidth.
 
 
 drill to slot; both drillSizeWidth and drillSizeHeight inherit drillDiameter
 
 For slots drillFigureName takes on figure for slot type selected and its width and height are the same as the slot width and height.; Hole type; DRC is out of date and dynamic shapes are disabled. |
| drillNonStandard | string; Changes type of type of non-standard drill. Hole type must be a circular drill. Types are `"LASER_DRILL"`, `"PLASMA_DRILL"`, `"PUNCH_DRILL"`, `"PHOTO_DRILL"`, `"COND_INK_DRILL"`, `"WET-DRY_DRILL"`, and `"OTHER_DRILL"`. Use `nil` if you want to unset this field.; Non-standard drill; None |
| drillOffset | `point/dbrep`; Changes the drill offset. Must be a xy point or a single dbrep, which applies to both, x and y.; Offset X and Y; DRC is out of date and dynamic shapes are disabled. |
| holeTolerance | `point/dbrep`; Changes the hole tolerance. Point values are taken to be a list of (+tolerance -tolerance) or a single dbrep which applies to both + and -. Both must be a positive number.; Tolerance + and -; None |
| holeToleranceY | `point/dbrep`; Changes the the slot Y tolerance. point values are taken to be a list of (+tolerance -tolerance) or a single dbrep which applies to both + and -. Both must be a positive number.; Y Tolerance + and - for slots; None |
| plating | string; Sets the plating type, must be one of `"NON_PLATED"`, `"OPTIONAL"`, or `"PLATED"`.; Plating; None |
| pluralVia | t/nil; Sets padstack to have a plural via; Plural Via; Can only be set for through hole padstacks. Padstack cannot be in use in the design |
| drillChar | string; Sets the drill characters. A maximum string of 3 is supported. Longer strings are truncated. Use a `nil` to remove the string.; Characters; None |
| drillFigureName | string; Sets the drill figure type. Not supported for slots. Value must be a string that matches one of the drop-down items in the pad_designer "Figure" field.; Figure; None |
| drillFigureHeight | dbrep; Changes the figure height, value must be a positive number. Option not available for slots. Used in conjunction with drillFigureWidth.; Height (under Drill/Slot symbol); None |
| drillFigureWidth | dbrep; Changes the figure width, value must be a positive number. This is not available for slots. Used in conjunction with drillFigureHeight.; Width (under Drill/Slot symbol); None |
| backdrillDiameter | float; Changes the backdrill diameter. Value must be a positive number and holeType must be a regular hole.; Secondary Drill tab; None |
| backdrillFigureChar | string; Sets the drill characters. A maximum string of three is supported.
 Longer strings are truncated. Use a nil to remove the string.; Secondary Drill tab; None |
| backdrillFigureName | string; Sets the backdrill figure type. Value must be a string that matches one of the drop-down items in the pad_designer "Figure" field.; Secondary Drill tab; None |
| backdrillFigureHeight | dbrep; Changes the backdrill figure height, value must be a positive number. 
 Used in conjunction with backdrillFigureWidth.; Secondary Drill tab; None |
| backdrillFigureWidth | dbrep; Changes the backdrill figure width, value must be a positive number. 
 Used in conjunction with backdrillFigureHeight.; Secondary Drill tab; None |
| spanLockCount | t/nil; Prevents non-through hole padstacks from exapnding (or contracting) when layers are added (or deleted). Default is for these padstacks to maintain their original start/stop layers.; Lock layer span; padstacks with this options may create disconnects when new layers are added |
| uvia | t/nil; Sets the type of via to bbvia (nil) or micro via (t). 
 Padstack must be a bbvia; This is kept for backwards compatibility.
 Use the `'type` option.; DRC is out of date and dynamic shapes are disabled. |
| keepout | nil; Obsolete in 17.0. 
 Use new route keepout pad layer type.; none |

#### Arguments

| Name | Description |
|---|---|
| `o_dbidPadstack` | dbid of a padstack (note VIA and PIN dbids are not supported) |
| `t_Padstack` | Name of padstack |
| `s_name` | Symbol name of attribute to change |
| `g_value` | New value |
| `[[s_name g_value] .. ]` | list of name/value pairs |

#### Value Returns

- `ls_names` - If name is nil then returns a list of all controls.

- `t`/`nil` - if t successful in updating padstack, nil an error

#### Examples

Finds a padstack using the ashOne share ware skill. Note that selection will return a pin or via and you must get the padstack from the definition attribute.

`p = ashOne()`

`padstack = p->definiton`

- Set drill characters

`ret = axlPadstackEdit(padstack 'drillChar "abc")`

or its equivalent

`ret = axlPadstackEdit(padstack '((drillChar "abc")))`

- Set tolerance

`ret = axlPadstackEdit(padstack 'holeTolerance '(1.2 1.3))`

- Set tolerance same for + and -

`ret = axlPadstackEdit(padstack 'holeTolerance 1.5)`

- Set drill symbol data

`data = '((drillFigureName "RECTANGLE") (drillFigureHeight 20) (drillFigureWidth 10) (drillChar A))`

`ret = axlPadstackEdit(padstack data)`

- Get list of all editable padstack parameters

`lst = axlPadstackEdit(nil nil)`

#### See Also

axlDBCreatePadStack, axlLoadPadstack, axlDBCopyPadstack, axlReplacePadstack

### axlPadstackSetType

`axlPadstackSetType( o_padstack/t_padstack g_uviaBbvia ) => t/nil`

or

`axlPadstackSetType( o_padstack/t_padstack g_type g_value ) => t/nil`

#### Description

Changes a padstack type. In its 2 argument mode is the same as:

`axlPadstackSetType(padstack 'type g_uviaBbvia)`

Permits changing the type of via.

`'type`

Changes a bbvia padstack to a micro via and vice versa. Uvia types can be managed separately in the constraints system.This has no effect if the padstack is used with Pins. Values are '`bbvia` or '`uvia`.

`'keepout`

Obsolete in 17.0. Create a keepout pad layer type of KEEPOUT.

Marks DRC out-of-date if successful.

#### Arguments

| Name | Description |
|---|---|
| `o_padstack` | padstack dbid |
| `t_padstack` | padstack name |
| `g_type` | mode (either 'type or 'keepout) |
| `g_value` | appropriate setting (see above) |

#### Value Returns

| Name | Description |
|---|---|
| `t` | change successful |
| `nil` | failed. Not a padstack, padstack not in database, type not recognized or padstack not a bbvia or uvia. |

#### Examples

Change padstack named VIA to a micro via

`axlPadstackSetType("VIA" 'type 'uvia)`

#### See Also

axlDBCreatePadStack, axlPadstackEdit

### axlPadstackUsageTypes

`axlPadstackUsageTypes( ) => lt_names`

#### Description

Returns list of strings of supported padstack usage types. This is a documentation support function.

#### Arguments

None

#### Value Returns

- List of strings

#### Examples

`axlPadstackUsageTypes()`

### axlPadUserMaskLayers

`axlPadUserMaskLayers( ['max] ) => lt_names/x_cnt`

or

`axlPadUserMaskLayers( 'create t_user_mask_layer ) => t/nil`

#### Description

Supports following modes:

- if argument returns list of user mask layers in design

- `'max` symbol option reports the maximum number that we support.

- `'create` adds a new user mask layer; requires a name

User mask naming:

If you use _TOP and _BOTTOM suffixes, then you will get mirror support. This means if you mirror a VIA with a user mask defined on xxx_TOP then it will be mirrored to the bottom. See axlDBControl('mirrorUserMask). With the mirror mask option enabled, the opposite side mask is auto-created.

#### Arguments

| Name | Description |
|---|---|
| ``max` | Optional. If provided, returns the maximum number of mask layers supported. |
| `'create` | Create a new user mask layer, requires `t_user_mask_layer` |
| `t_user_mask_layer` | Name of user mask layer |

#### Value Returns

| Name | Description |
|---|---|
| lt_names | List of user mask names |
| x_cnt | Maximum number permitted to be defined |

| Name | Description |
|---|---|
| t/nil | In create mode, returns `t` if layer was created or exists, `nil` if failed to create. Failure can be due to: |

- exhausted number of user mask layers available

- name is illegal

#### Examples

| Name | Description |
|---|---|
| 1. | Typical use to get all layers defined |

`axlPadUserMaskLayers()`

| Name | Description |
|---|---|
| 2. | Return max that can be defined |

`axlPadUserMaskLayers('max) -> 32`

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

#### See Also

axlDBCreatePadStack, axlDBControl

