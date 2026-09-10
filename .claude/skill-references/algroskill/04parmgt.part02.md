<!--
source: algroskill/04parmgt.md
part: 2/2
estimated_tokens: 5755
-->

### axlMaterialGet

`axlMaterialGet( nil ) => lt_materials`

or

`axlMaterialGet( t_materialName ) => og_material`

or

`axlMaterialGet( 'all ) => log_materials`

or

`axlMaterialGet( 'file ) => t_file`

or

`axlMaterialGet( 'path ) => t_pathToFile`

#### Description

Returns various infomation about materials file. Depending on the argument passed, command works in different modes to retrieve the following.

- List of materials

- Number of material file entries

- Name of material file being used; this differ between PCB and ICP products

- Path to material file

- actual attributes of a material file entry

Material attributes as a disembodied property list:

| Name | Description |
|---|---|
| NAME | TYPE; DESCRIPTION |
| dielectric | double; Dielectric Constant |
| freqDepFile | string; name of frequent dependant file or "" |
| electricalConductivity | string; electrical Conductivity in mho/cm |
| lossTangent | double; Loss Tangent |
| name | string; Name of material |
| objType | string; "material" |
| readOnly | t; cannot modify object |
| thermalConductivity | string; Thermal Conductivity in w/cm-degC |
| thickness | string; layer thickness with design units |
| tolPlus | string; layer thickness tolerance plus with design units |
| tolMinus | string; layer thickness tolerance minus with design units |

- On Windows, performance may be slow, when accessing individual material entries in material file is stored on the network.

#### Arguments

| Name | Description |
|---|---|
| `nil` | List of material names |
| `t_materialName` | Name of material |
| `'all` | Get all material data |
| `'filename` | Get name of material file (allegro uses material and ICP products use mcmmat |
| `'path` | Return location of file on disk |

#### Value Returns

| Name | Description |
|---|---|
| `nil` | An error was detected |
| `lt_materialNames` | A list of the material names |
| `og_materials` | Disembodied property list of material charactustics (see above) |
| `log_materials` | A list of disembodied property lists |
| `t_file` | Name of material file in use |
| `t_pathToFile` | Path to material file in use |

#### Examples

- Get info about FR-4

`mat = axlMaterialGet("FR-4")`

`printf("Thicknesss %L\n" mat->thickness)`

- Get all material defined in materials.dat

`names = axlMaterialGet(nil)`

- Get path of file

`path = axlMaterialGet('path)`

### axlVisibleDesign

`axlVisibleDesign( g_makeVis ) => t/nil`

#### Description

Makes entire design visible or invisible. This command does not visually change the display, since it can also be used in conjunction with the `axlSelect` command family to provide additional filtering of the database objects. If you wish to visually update the display, call `axlUIWUpdate(nil)` after changing the visibility.

Note: This routine along with `axlVisibleGet` and `axlVisibleSet` allows you to temporarily change the visibility of the design to provide additional filtering capability when finding objects via the selection set. The programming model is:

`saveVis = axlVisibleGet()`

`axlVisibleDesign(nil)`

`; set desired layers visible via one or more calls to`

`axlVisibleLayer(...)`

`; set find filter for objects to find`

`axlSetFindFilter(...)`

`; find objects by using one of the Select APIs .. example`

`axlAddSelectAll()`

`objs = axlGetSelSet()`

`; restore visiblility`

`axlVisibileSet(saveVis)`

`; note no need to make a call to axlVisibileUpdate because`

`; the visisbility changes are a wash`

#### Arguments

| Name | Description |
|---|---|
| `g_makeVis` | Either `t` or `nil`. `t` = make entire design visible `nil` = make entire design invisible |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Design made visible or invisible as specified. |
| `nil` | Should never be seen. |

#### See Also

axlVisibleUpdate and axlIsVisibleLayer

Note: This command does not visually change the display. To visually update the display, call `axlUIWUpdate (nil)` after changing the visibility.

### axlVisibleGet

`axlVisibleGet( ) => l_visList/nil`

#### Description

Returns the visibility of the entire design - which layers are visible/invisible.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `l_visList` | List of lists. The format is for each class: |

`(nil class <``t_className``> visible t/nil/-1``subclassinfo <``l_subclass``>)``....)``l_subclass``format:``((<``t_subclass``> t/nil) ....)``where t/nil/-1``t - visible``nil - invisible``-1 - class has both visible and invisible components.`

Note: Any change in the structure of `l_vislist` affects `axlVisibleSet`, this function's complementary function.

#### Examples

`visList = axlVisibleGet()`

`(`

`(nil class "BOARD GEOMETRY" visible nil subclassinfo nil)`

`(nil class "COMPONENT VALUE" visible nil subclassinfo nil)`

`(nil class "DEVICE TYPE" visible nil subclassinfo nil)`

`(nil class "DRAWING FORMAT" visible nil subclassinfo nil)`

`(nil class "DRC ERROR CLASS" visible t subclassinfo nil)`

`(nil class "ETCH" visible -1`

`subclassinfo`

`(("TOP" t)`

`("TRACE_2" nil)`

`("TRACE_3" nil)`

`("BOTTOM" t)`

`))`

`(nil class "MANUFACTURING" visible nil subclassinfo nil)`

`(nil class "ANALYSIS" visible nil subclassinfo nil)`

`(nil class "PACKAGE GEOMETRY" visible nil subclassinfo nil)`

`(nil class "PACKAGE KEEPIN" visible t subclassinfo nil)`

`(nil class "PACKAGE KEEPOUT" visible nil subclassinfo nil)`

`(nil class "PIN" visible t subclassinfo nil)`

`(nil class "REF DES" visible nil subclassinfo nil)`

`(nil class "ROUTE KEEPIN" visible t subclassinfo nil)`

`(nil class "ROUTE KEEPOUT" visible nil subclassinfo nil)`

`(nil class "TOLERANCE" visible nil subclassinfo nil)`

`(nil class "USER PART NUMBER" visible nil subclassinfo nil)`

`(nil class "VIA CLASS" visible nil subclassinfo nil)`

`(nil class "VIA KEEPOUT" visible nil subclassinfo nil)`

`)`

Returns the visibility of the entire design.

### axlVisibleLayer

`axlVisibleLayer( t_layer g_makeVis ) => t/nil`

#### Description

Sets a given layer to visible or invisible. If given only a class name, sets the entire layer to visible or invisible. If you want to update the display, call `axlVisibleUpdate` when finished with your layer visibility updates.

#### Arguments

| Name | Description |
|---|---|
| `t_layer` | Name of the layer. Either a fully qualified layer name in the format <`class`>/<`subclass`> or a class name in the format <`class`>. |
| `g_makeVis` | Either `t` or `nil`. `t` = make visible `nil` = make invisible. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Layer set to visible or invisible as specified. |
| `nil` | Layer does not exist. |

#### See Also

axlVisibleUpdate

Note: This command does not visually change the display. To visually update the display, call `axlUIWUpdate (nil)` after changing the visibility.

### axlVisibleSet

`axlVisibleSet( l_visList ) => t/nil`

#### Description

Sets the visibility of the entire design.

#### Arguments

| Name | Description |
|---|---|
| `l_visList` | List with visibility attributes. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Set the visibility of the design as specified. |
| `nil` | Incorrect format for `l_visList`. |

#### See Also

axlVisibleUpdate and axlVisibleLayer

Note: This command does not visually change the display. To visually update the display, call `axlUIWUpdate (nil)` after changing the visibility.

### axlConductorBottomLayer

`axlConductorBottomLayer( ) => t_name`

#### Description

Returns the name of the bottom conductor layer.

#### Arguments

none

#### Value Returns

| Name | Description |
|---|---|
| `t_name` | Name of the bottom conductor layer. |

#### Examples

`axlConductorBottomLayer()``⇒ "BOTTOM"`

### axlConductorTopLayer

`axlConductorTopLayer() => t_name`

#### Description

Returns the name of the top conductor layer.

#### Arguments

none

#### Value Returns

| Name | Description |
|---|---|
| `t_name` | Name of the top conductor layer. |

#### Examples

`axlConductorTopLayer()``⇒ "TOP"`

### axlDBCreateFilmRec

axlDBCreateFilmRec()

#### Description

This interface is obsolete. It is kept to support existing Skill code.

Instead, use axlFilmCreate

### axlSetPlaneType

`axlSetPlaneType( t_subclassName t_planeType ) => t/nil`

#### Description

This changes the photoplot type of a conductor or plane type layer between positive or negative artwork. Changing a layer already containing data will require re-voiding existing shapes and updating DRC.

#### Arguments

| Name | Description |
|---|---|
| `t_subclassName` | Subclass name whose plane type is to be changed. |
| `t_planeType` | Plane type ("Positive", "Negative") |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Plane type changed. |
| `nil` | Plane type is not changed. |

#### See Also

axlGetParam, axlSetParam

### axlSubclasses

`axlSubclasses( t_class ?field s_name ?value g_value ) => lt_subclasses`

#### Description

Lists subclasses that make up a class. This function is supported in both, APD and Allegro name space. The field and value options provide additional filtering based upon the characteristics of the layer.

The information about the attributes and values permitted on a layer, can be obtained using the following function.

`axlLayerGet("MANUFACTURING/PROBE_TOP")->??` You should map the class name via axlMapClassName if you are writing code for both PCB and APD/SIP as certain class names are different in these products.

The base call is actually just:

#### Arguments

| Name | Description |
|---|---|
| `t_class` | Class name. |
| `field` | Optional field for filtering. If value option is not present filters on basis of a non-nil value. |
| `value` | Optional value of field to use for filtering. Requires field option to be passed. |

#### Examples

- get all subclasses on class

`axlSubclasses( axlMapClassName("MANUFACTURING"))`

- get user defined subclasses

`axlSubclasses("MANUFACTURING" ?field 'userDefined)`

- all allegro defined

`axlSubclasses("MANUFACTURING" ?field 'userDefined ?value nil)`

#### See Also

`axlGetParam("paramLayerGroup:ETCH")->groupMembers` axlSubclassRoute, axlGetParam, axlMapClassName, axlClasses

### axlSubclassRoute

`axlSubclassRoute( ?field s_name ?value g_value ) => lt_subclasses`

#### Description

Lists subclasses that make up class ETCH.

If no arguments are passed to the function, it returns a list of subclasses in the ETCH class, or CONDUCTOR class, in case of non-PCB product.

The field and value options provide additional filtering based upon the characteristics of the layer. For information on layer parameters, see the section Layer Parameter Attributes (Allegro Subclasses).

The information about the attributes and values permitted on a layer can be obtained using the following command.

`axlLayerGet("ETCH/TOP")->??`

The base call is actually just:

#### Arguments

| Name | Description |
|---|---|
| `field` | Optional field for filtering. Uses the value specified by the `value` argument to filter subclasses. |
| `value` | Optional value of field to use for filtering. Requires field option to be passed. |

#### Examples

- all etch subclasses

`axlSubclassRoute() -> ("TOP" "GND" "VCC" "BOTTOM")`

- all subclasses that are of type etch

`axlSubclassRoute(?field 'isEtch)`

- all subclasses that are not etch (e.g dielectric)

`axlSubclassRoute(?field 'isEtch ?value nil)`

- all subclasses with material FR-4

`axlSubclassRoute(?field 'material ?value "FR-4")`

#### See Also

axlSubclasses, axlGetParam

### axlXSectionCopy

`axlXSectionCopy( o_xsectionDBID ) => g_xsectionDefstruct/nil`

#### Description

This copies dbid xsection to an xsection Skill defstruct.It can be used to duplicate the charactistics of an existing xsection layer to a new layer for use with axlXSectionCreate. Alternatively, it can be used to modify an existing layer via axlXSectionSet, although axlXSectionModify might be a better fit for changing a layer.

This creates a new defstruct using `make_axlXSection()`.The name attribute is never copied.

- If using this to copy named layers, you need to set the name attribute in the defstruct returned by this function.

#### Arguments

| Name | Description |
|---|---|
| `o_xsectionDBID` | a xsection dbid |

#### Value Returns

| Name | Description |
|---|---|
| `g_xsectionDefstruct` | a defstruct with its attribute data copied from dbid |

#### Examples

- See <cdsroot>/share/pcb/examples/skill/dbcreate/xsection.il

#### See Also

axlXSectionCreate, axlXSectionModify

### axlXSectionCreate

`axlXSectionCreate( nil g_option [g_xsectionDefStruct] ) => o_xsectionDBID/nil`

#### Description

Creates a new cross section entry.

The three critical create items in `g_xsectionDefStruct` are:

- name - a string which is a name of the layer

- layerType - a string (see `axlXSectionLayerTypes()` for supported of types) that describes the type of layer.

Popular types are CONDUCTOR, PLANE, DIELECTRIC or MASK. If no value is specified, DIELECTRIC is used as the default value.

- material - a string that describes substance making up the xsection entry. Default is FR-4 for dielectrics and COPPER for conductor/plane.

If no attributes are provided, an unnamed xsection entry of type DIELECTRIC, with material FR-4 is created.

You can set other xsection entries, see `axlXSectionGet` for a description of the other available attributes. If material is provided it will auto-fill additional based upon the materials file.

For named xsection layers, it creates a class/subclass on the etch layers, it does not set the color and visibility for those layers. You need to use `axlLayerSet` for those attributes.

Allegro PCB does not allow name layers above top or below bottom.

RESTRICTION - Currently, it is not possible to create manage multiple stackups via Skill. This restriction will be removed in a future release.

#### Arguments

| Name | Description |
|---|---|
| `nil` | First argument must always be nil |
| `g_option` | <br><br>`'top`; insert layer above top. For PCB designs this can only be a unnamed dielectric or MASK layers.<br><br>`'bottom`; insert layer above bottom<br><br>`'afterBottom`; insert layer after bottom. For PCB Designs this can only be unnamed dielectrics or MASK layers.<br><br>`t_etchSubclass`; sublass name, insert layer above this name<br><br>`x_position`; insert above xsection position. This is the position attribute and an xsection dbid. You cannot insert above 0 (Surface). |
| `g_xsectionDefStruct` or `nil` | A Skill defstruct with all possible attributes for xsection entry<br><br>`make_axlXSection`; creates a new entry<br><br>`copy_axlXSection`; copies an existing entry<br><br>`axlXSectionCopy`; copies contents of an existing xsection dbid to a new deftruct. |

#### Value Returns

| Name | Description |
|---|---|
| `o_xsectionDBID` | if successful |
| `nil` | failed. |

#### Examples

`see <cdsroot>/share/pcb/examples/skill/dbcreate/xsection.il`

#### See Also

axlXSectionGet, axlXSectionSet, axlXSectionDelete, axlXSectionLayerTypes, `axlXSectionCopy`, `axlXSectionModify`, `axlXSectionLayerFunctions`

### axlXSectionDelete

`axlXSectionDelete( g_option/o_xsectionDBID/t_etchSubclass/x_position ) => lt_types`

#### Description

Deletes a cross section layer. If layer is associated with an ETCH layer, the associated layer is also deleted. Associated ETCH layers must not have objects. See axlLayerDelete for other reasons for failure.

#### Arguments

| Name | Description |
|---|---|
| `g_option` |  |
| `o_xsectionDBID` | delete layer by XSection dbid |
| `t_etchSubclass` | delete layer by this name |
| `x_position` | delete layer by position. This is the position attribute in the xsection dbid. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | if successful |
| `nil` | failed. |

#### Examples

See `<cdsroot>/share/pcb/examples/skill/dbcreate/xsection.il`

#### See Also

axlXSectionCreate, axlLayerCreate, axlDeleteByLayer

### axlXSectionGet

`axlXSectionGet( g_stackup/nil g_option ) => g_data/nil`

#### Description

Returns data about the cross-section entry for a design.

Supports multiple access options (see Arguments).

Allegro design color and visibility query needs are satisfied by the axlLayerGet API.

#### Arguments

| Name | Description |
|---|---|
| g_stackup | <br><br>nil; for cross sections with a single stackup this returns the standard stackup. For Rigid-Flex designs this returns All Stackups.<br><br>str; name of stackup. From zone groups it is the name in zoneDbid -> stackup or available stackups are return by `axlXSectionGet(nil 'stackups)` |
| g_option | <br><br>'stackups; return a list of stacks. g_xsection is ignored and should be nil<br><br>'count; return number of cross section entries for provided stackup. g_data is x_entries<br><br>'number; return maximum number of individual stackups database supports<br><br>'thickness; return provided stackup thickness in user units g_data is f_thickness design units, accuracy is not restricted to current design accuarcy. This is the total thickness with masks.<br><br>'top; return cross entry for top layer of design<br><br>'bottom; return cross entry for bottom layer of design<br><br>x_position; return cross entry for given position in "All stackups". This is the number field in a xsection dbid. (0 is the 1st layer -- air)<br><br>t_etchSubcalss; name of etch subclass. g_data is a o_xsection DBID<br><br>'all; return entire stackup. g_data must be a lo_xsectionDBID<br><br>'locked; lock status
 nil - not locked
 list of lock status. This is a user interface lock only. axl and techfile can make changes.
 
 '`value`: cannot edit values
 
 
 '`layer`: add or delete layers |

- The name of the stackup can be obtained from the zone dbid by zoneDbi->stackup

- If using a single stackup in a design pass `nil` as the first argument.

- If a multi-stackup design, a nil returns all of the xsection dbids (e.g. "All Stackups"). If you need the main stackup, typically called "primary", use its name.

- Except for `'stackups` and `'locked` all other options take into account the stackup argument.

- Thickness if `g_xsection` is we return the all stackup thickness which can be overridden by the TEXT_BOARD_THICKNESS property assigned at the design level. Otherwise if a stackup (`g_xsection`) name is provided returns the calculated thickness of the indicated stackup.

#### Value Returns

| Name | Description |
|---|---|
| `nil` | an error |
| `g_data` | depends on g_option, see Arguments section |

#### Examples

- Get design thickness

`thick = axlXSectionGet(nil 'thickness)`

- Fetch entire cross section

`stackup = axlXSectionGet(nil 'all)`

- Fetch just the top layer

`xs = axlXSectionGet(nil 'top)`

- Fetch dielectric below top

`xs = axlXSectionGet(nil 'top)`

`dielectric = axlXSectionGet(nil xs->number +1)`

`axlPrintDbid(dielectric)`

- Get all stackups (even with one stackup will return PRIMARY)

`stackups = axlXSectionGet(nil 'stackups)`

- get stackup called FLEX2

`zoneStackup = axlXSectionGet("FLEX2" 'all)`

- get number of layers in FLEX2 (includes etc, dielectric and layers above surface)

`zoneStackup = axlXSectionGet("FLEX2" 'count)`

- See `<cdsroot>``/share/pcb/examples/skill/dbcreate/xsection.il`

### axlXSectionLayerFunctions

`axlXSectionLayerFunctions( ) => lt_types`

#### Description

Return list of supported layer function types.Layer functions are a super set of layer types.

#### Arguments

None

#### Value Returns

- List of strings of supportted layer types.

#### Examples

`only use types = axlXSectionLayerFunctions()`

#### See Also

axlXSectionCreate

### axlXSectionLayerTypes

`axlXSectionLayerTypes( ) => lt_types`

#### Description

Return list of supported layer types. This is used withlayerType attribute when adding or modifing xsection layers.

#### Arguments

None

#### Value Returns

- List of strings of supportted layer types.

#### Examples

`only use types = axlXSectionLayerTypes()`

#### See Also

axlXSectionCreate

### axlXSectionModify

`axlXSectionModify( <list of defstruct attributes and values> ) => g_xsectionDefstruct/nil`

#### Description

This is a wrapper for`make_axlXSection()` function to createa new defstruct. For certain fields (e.g. boolean and some string fields) a `'none` symbol is used to indicate that the field should not be changed, other fields can use the default `nil` symbol.

#### Arguments

Same as `make_axlXSection()`.

#### Value Returns

| Name | Description |
|---|---|
| `g_xsectionDefstruct` | a defstruct with its attribute data copied from provided arguments |

#### Examples

- Modify a layer to be negative artwork assume a layer named GND exists. All other layer characturistics will remain the same

`xs = axlXSectionGet(nil "GND")``negative = axlXSectionModify(?negativeArtwork t)``ret = axlXSectionSet(xs negative)`

- See <cdsroot>`/share/pcb/examples/skill/dbcreate/xsection.il`

#### See Also

axlXSectionCreate

### axlXSectionSet

`axlXSectionSet( g_option [g_xsectionDefStruct] ) => t/nil`

or

`axlXSectionSet( 'locked nil/l_lockType ) => t/nil`

#### Description

Modifies an existing cross section entry. Use axlXSectionModify to create a xsection defstruct with the attributes you wish to modify.

See axlXSectionGet for a description of the other available attributes. If changing material, it also updates the material characteristics to values of the new material.

Allegro PCB editor does not allow name layers above top or below bottom.

PROGRAMM TIPS:

- See tips in axlXSectionCreate.

- In Allegro PCB Editor, you cannot rename TOP or BOTTOM.

- Cannot unname a layer with data on the ETCH layers.

- DRC is marked out of date.

#### Arguments

| Name | Description |
|---|---|
| `nil` | first argument must always be `nil` |
| `g_option` | <br><br>`o_xsectionDBID`; delete layer by XSection dbid<br><br>`t_etchSubclass`; modify by sublass name<br><br>`x_position`; modify by xsection position. This is the number attribute in the xsection dbid.<br><br>`'locked`; update user inteface layer locking |
| `g_xsectionDefStruct` | A SKILL defsruct with all possible attributes for xsection entry<br><br>`make_axlXSection`; creates a new entry<br><br>`copy_axlXSection`; copies an existing entry<br><br>`axlXSectionCopy`; copies contents of an existing xsection dbid to a new deftruct. |
| `l_lockType` | change user interface locking
 
 may be nil to unlock `'layer`- prevent layer addition or deletion `'value` - prevent changing values
 
 
 list of both |

#### Value Returns

| Name | Description |
|---|---|
| `t` | if successful |
| `nil` | failed. |

#### Examples

- See `<cdsroot>/share/pcb/examples/skill/dbcreate/xsection.il`

- lock layer values

`axlXSectionSet('locked 'layer)`

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

#### See Also

axlXSectionCreate, axlXSectionCopy

