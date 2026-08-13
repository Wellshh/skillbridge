<!--
source: algroskill/04parmgt.md
part: 2/2
estimated_tokens: 7940
-->

|  |
| --- | ---
| `t_Prev_layerName` | Name of the layer above which the new layer is to be added
| `t_layerType` | Type of layer to be added, such as Conductor or Surface.
| `t_materialType` | Material of the layer.
| `t_subclassName` | Optional parameter. Name of the new layer.
| `t_planeType` | Optional parameter. Type of plane, either`Positive` or `Negative`. The default is `Positive`.
#### Value Returned

|  |
| --- | ---
| `t` | Layer is created or already exists.
| `nil` | Layer does not exist and could not be created.
#### See Also

[axlLayerCreateNonConductor](#1173941 "3"), [axlLayerGet](#1173865 "3"), and [axlXSectionGet](#1169585 "3")

### axlLayerCreateNonConductor

`axlLayerCreateNonConductor(t_layerName)⇒ t/nil`

#### Description

Creates a new subclass for non-etch subclasses. AXL-SKILL restricts you from creating etch subclasses.

#### Arguments

|  |
| --- | ---
| `t_layerName` | *<*`class`*>*/*<*`subclass`*>*
#### Value Returned

|  |
| --- | ---
| `t` | New subclass is created or, subclass already exists.
| `nil` | New subclass is not created.
#### Example

`axlLayerCreateNonConductor("BOARD GEOMETRY/MYSUBCLASS")`

Creates a new subclass named`MYSUBCLASS`.

### axlLayerDelete

`axlLayerDelete(t_layerName/x_layerNumber) => t/nil`

#### Description

This command deletes a cross section layer. While[axlDeleteObject](06intedt.html#832160 "5") can be used to delete empty named layers, this API can delete both named and unnamed cross-section layers.The cross section has both ETCH layers and unnamed dielectric layers.The order of the cross section is returned by [axlGetXSection](#1151911 "3"), The `x_layerNumber` is the order within the cross-section with the first index number (e.g AIR) starting at 0.

The command can fail in the following scenarios.

* Deleting a named layer containing geometries (excluding pins or vias)

* Deleting top or bottom dielectric or TOP or BOTTOM etch layers

* Layer name does not exist

* Layer number is less then 0 or greater or equal to`length(axlGetXSection('count))`

#### Arguments

ETCH layer string or cross section index

#### Value Returned

`t` if layer is deleted, `nil` if failure

#### Examples

* The command to delete a layer named empty is:

> `axlLayerDelete("EMTPY")`

* Delete the third cross section layer. On most designs this is an unnamed dielectric layer between TOP and the next etch layer.

> `axlLayerDelete(3)`

#### See Also

[axlLayerCreateNonConductor](#1173941 "3"), [axlDeleteByLayer](25dbmisc.html#1095212 "26"), [axlDeleteObject](06intedt.html#832160 "5"), [axlGetXSection](#1151911 "3"), [axlXSectionDelete](#1169205 "3")

### axlLayerGet

`axlLayerGet(t_layer)⇒ o_dbid/nil`

#### Description

Gets the layer parameter given the shortcut notation of*<*`class`*>*/*<*`subclass`*>*. This is an ease of use function that does:

> `axlGetParam("paramLayerGroup:<class>/paramLayer:<subclass>)`

This does NOT allow access to the cross section data (example material or thickness). It allows easier access to color and visiblity of a layer.

* You can use the groupMembers attribute of result --`result=axlGetParam("paramLayerGroup:<class>")` -- to iterate over all subclass of a class.

#### Arguments

|  |
| --- | ---
| `t_layer` | Name of layer in format "<`class`>/<`subclass`>".
#### Value Returned

|  |
| --- | ---
| `o_dbid` | Layer parameter`dbid`.
| `nil` | Layer is not present.
#### Example

Changes color of top etch layer.

> `q = axlLayerGet("ETCH/TOP")`

> `q->color = 7`

> `axlLayerSet(q)`

> `axlVisibleUpdate(t)`

#### See Also

[axlGetParam](#1126060 "3")

### axlLayerViaLabel

`axlLayerViaLabel(t_layerName/x_layerNumber) => t_viaLabel/nil`

#### Description

Reports via label for a layer. A via label either defaults to the layer number, or can be assigned by the user through the cross section. You can query the cross section for an override.

#### Arguments

ETCH layer string or cross section index

#### Value Returned

Via label name; or`nil`, in case of an error

#### Examples

* To return the via label of a layer called TOP

`axlLayerViaLabel("TOP")-> 1`

#### See Also

[axlXSectionGet](#1169585 "3")

### axlMaterialGet

`axlMaterialGet(nil)==> lt_materials`

`axlMaterialGet(t_materialName)==> og_material`

`axlMaterialGet('all)==> log_materials`

`axlMaterialGet('file)==> t_file`

`axlMaterialGet('path)==> t_pathToFile`

#### Description

Returns various infomation about materials file. Depending on the argument passed, command works in different modes to retrieve the following.

* List of materials

* Number of material file entries

* Name of material file being used; this differ between PCB and ICP products

* Path to material file

* actual attributes of a material file entry

Material attributes as a disembodied property list:

|  |  |
| --- | --- | ---
| **NAME** | **TYPE** | **DESCRIPTION**
| dielectric | double | Dielectric Constant
| freqDepFile | string | name of frequent dependant file or ""
| electricalConductivity | string | electrical Conductivity in mho/cm
| lossTangent | double | Loss Tangent
| name | string | Name of material
| objType | string | "material"
| readOnly | t | cannot modify object
| thermalConductivity | string | Thermal Conductivity in w/cm-degC
| thickness | string | layer thickness with design units
| tolPlus | string | layer thickness tolerance plus with design units
| tolMinus | string | layer thickness tolerance minus with design units
* ***On Windows, performance may be slow, when accessing individual material entries in material file is stored on the network.***

#### Arguments

|  |
| --- | ---
| `nil` | List of material names
| `t_materialName` | Name of material
| `'all` | Get all material data
| `'filename` | Get name of material file (allegro uses material and ICP products use mcmmat
| `'path` | Return location of file on disk
#### Value Returned

|  |
| --- | ---
| `nil` | An error was detected
| `lt_materialNames` | A list of the material names
| `og_materials` | Disembodied property list of material charactustics (see above)
| `log_materials` | A list of disembodied property lists
| `t_file` | Name of material file in use
| `t_pathToFile` | Path to material file in use
#### Examples

* Get info about FR-4

> `mat = axlMaterialGet("FR-4")`

> `printf("Thicknesss %L\n" mat->thickness)`

* Get all material defined in materials.dat

> `names = axlMaterialGet(nil)`

* Get path of file

> `path = axlMaterialGet('path)`

### axlVisibleDesign

`axlVisibleDesign(g_makeVis)⇒ t/nil`

#### Description

Makes entire design visible or invisible. This command does not visually change the display, since it can also be used in conjunction with the`axlSelect` command family to provide additional filtering of the database objects. If you wish to visually update the display, call `axlUIWUpdate(nil)` after changing the visibility.

**Note:** This routine along with`axlVisibleGet` and `axlVisibleSet` allows you to temporarily change the visibility of the design to provide additional filtering capability when finding objects via the selection set. The programming model is:

> `saveVis = axlVisibleGet()`

> `axlVisibleDesign(nil)`

> `; set desired layers visible via one or more calls to`

> `axlVisibleLayer(...)`

> `; set find filter for objects to find`

> `axlSetFindFilter(...)`

> `; find objects by using one of the Select APIs .. example`

> `axlAddSelectAll()`

> `objs = axlGetSelSet()`

> `; restore visiblility`

> `axlVisibileSet(saveVis)`

> `; note no need to make a call to axlVisibileUpdate because`

> `; the visisbility changes are a wash`

#### Arguments

|  |
| --- | ---
| `g_makeVis` | Either`t`or `nil`.  `t` = make entire design visible  `nil` = make entire design invisible
#### Value Returned

|  |
| --- | ---
| `t` | Design made visible or invisible as specified.
| `nil` | Should never be seen.
#### See Also

[axlVisibleUpdate](19cmdctl.html#984586 "20") and [axlIsVisibleLayer](#1067336 "3")

**Note:** This command does not visually change the display. To visually update the display, call`axlUIWUpdate (nil)` after changing the visibility.

### axlVisibleGet

`axlVisibleGet()⇒ l_visList/nil`

#### Description

Returns the visibility of the entire design - which layers are visible/invisible.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `l_visList` | List of lists. The format is for each class:
> ```
> (nil class <t_className> visible t/nil/-1subclassinfo <l_subclass>)....)l_subclass format:((<t_subclass> t/nil) ....)where t/nil/-1t - visiblenil - invisible-1 - class has both visible and invisible components.
> ```

**Note:** Any change in the structure of`l_vislist` affects `axlVisibleSet`, this function's complementary function.

#### Example

> `visList = axlVisibleGet()`

> `(`

> `(nil class "BOARD GEOMETRY" visible nil subclassinfo nil)`

> `(nil class "COMPONENT VALUE" visible nil subclassinfo nil)`

> `(nil class "DEVICE TYPE" visible nil subclassinfo nil)`

> `(nil class "DRAWING FORMAT" visible nil subclassinfo nil)`

> `(nil class "DRC ERROR CLASS" visible t subclassinfo nil)`

> `(nil class "ETCH" visible -1`

> `subclassinfo`

> `(("TOP" t)`

> `("TRACE_2" nil)`

> `("TRACE_3" nil)`

> `("BOTTOM" t)`

> `))`

> `(nil class "MANUFACTURING" visible nil subclassinfo nil)`

> `(nil class "ANALYSIS" visible nil subclassinfo nil)`

> `(nil class "PACKAGE GEOMETRY" visible nil subclassinfo nil)`

> `(nil class "PACKAGE KEEPIN" visible t subclassinfo nil)`

> `(nil class "PACKAGE KEEPOUT" visible nil subclassinfo nil)`

> `(nil class "PIN" visible t subclassinfo nil)`

> `(nil class "REF DES" visible nil subclassinfo nil)`

> `(nil class "ROUTE KEEPIN" visible t subclassinfo nil)`

> `(nil class "ROUTE KEEPOUT" visible nil subclassinfo nil)`

> `(nil class "TOLERANCE" visible nil subclassinfo nil)`

> `(nil class "USER PART NUMBER" visible nil subclassinfo nil)`

> `(nil class "VIA CLASS" visible nil subclassinfo nil)`

> `(nil class "VIA KEEPOUT" visible nil subclassinfo nil)`

> `)`

Returns the visibility of the entire design.

### axlVisibleLayer

`axlVisibleLayer(t_layerg_makeVis)⇒ t/nil`

#### Description

Sets a given layer to visible or invisible. If given only a class name, sets the entire layer to visible or invisible. If you want to update the display, call`axlVisibleUpdate` when finished with your layer visibility updates.

#### Arguments

|  |
| --- | ---
| `t_layer` | Name of the layer. Either a fully qualified layer name in the format*<*`class`*>*/*<*`subclass`*>* or a class name in the format *<*`class`*>*.
| `g_makeVis` | Either`t` or `nil`*.*  `t`= make visible  `nil` = make invisible.
#### Value Returned

|  |
| --- | ---
| `t` | Layer set to visible or invisible as specified.
| `nil` | Layer does not exist.
#### See Also

[axlVisibleUpdate](19cmdctl.html#984586 "20")

**Note:** This command does not visually change the display. To visually update the display, call`axlUIWUpdate (nil)` after changing the visibility.

### axlVisibleSet

`axlVisibleSet( l_visList)⇒ t/nil`

#### Description

Sets the visibility of the entire design.

#### Arguments

|  |
| --- | ---
| `l_visList` | List with visibility attributes.
#### Value Returned

|  |
| --- | ---
| `t` | Set the visibility of the design as specified.
| `nil` | Incorrect format for`l_visList`.
#### See Also

[axlVisibleUpdate](19cmdctl.html#984586 "20") and [axlVisibleLayer](#1068430 "3")

**Note:** This command does not visually change the display. To visually update the display, call`axlUIWUpdate (nil)` after changing the visibility.

### axlConductorBottomLayer

`axlConductorBottomLayer()⇒ t_name`

#### Description

Returns the name of the bottom conductor layer.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `t_name` | Name of the bottom conductor layer.
#### Example

> `axlConductorBottomLayer()⇒ "BOTTOM"`

### axlConductorTopLayer

`axlConductorTopLayer()⇒ t_name`

#### Description

Returns the name of the top conductor layer.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `t_name` | Name of the top conductor layer.
#### Example

> `axlConductorTopLayer()⇒ "TOP"`

### axlDBCreateFilmRec

`axlDBCreateFilmRec()`

#### Description

This interface is obsolete. It is kept to support existing Skill code.

Instead, use[axlFilmCreate](#1148038 "3")

### axlSetPlaneType

`axlSetPlaneType(t_subclassNamet_planeType)⇒ t/nil`

#### Description

This changes the photoplot type of a conductor or plane type layer between positive or negative artwork. Changing a layer already containing data will require re-voiding existing shapes and updating DRC.

#### Arguments

|  |
| --- | ---
| `t_subclassName` | Subclass name whose plane type is to be changed.
| `t_planeType` | Plane type ("Positive", "Negative")
#### Value Returned

|  |
| --- | ---
| `t` | Plane type changed.
| `nil` | Plane type is not changed.
#### See Also

[axlGetParam](#1126060 "3"), [axlSetParam](#1109729 "3")

### axlSubclasses

`axlSubclasses(t_class?field s_name?value g_value) -> lt_subclasses`

#### Description

Lists subclasses that make up a class. This function is supported in both, APD and Allegro name space. The field and value options provide additional filtering based upon the characteristics of the layer.

The information about the attributes and values permitted on a layer, can be obtained using the following function.

`axlLayerGet("MANUFACTURING/PROBE_TOP")->??`

You should map the class name via axlMapClassName if you are writing code for both PCB and APD/SIP as certain class names are different in these products.

The base call is actually just:

`axlGetParam("paramLayerGroup:ETCH")->groupMembers`

#### Arguments

|  |
| --- | ---
| `t_class` | Class name.
| `field` | Optional field for filtering. If value option is not present filters on basis of a non-nil value.
| `value` | Optional value of field to use for filtering. Requires field option to be passed.
#### Values Returned

|  |
| --- | ---
| `lt_subclasses` | A list of subclass strings.
#### See Also

[axlSubclassRoute](#1119179 "3"), [axlGetParam](#1126060 "3"), [axlMapClassName](23utils.html#911688 "24"), [axlClasses](#1140503 "3")

#### Example

* get all subclasses on class

> `axlSubclasses( axlMapClassName("MANUFACTURING"))`

* get user defined subclasses

> `axlSubclasses("MANUFACTURING" ?field 'userDefined)`

* all allegro defined

> `axlSubclasses("MANUFACTURING" ?field 'userDefined ?value nil)`

### axlSubclassRoute

`axlSubclassRoute(?field s_name?value g_value) -> lt_subclasses`

#### Description

Lists subclasses that make up class ETCH.

If no arguments are passed to the function, it returns a list of subclasses in the ETCH class, or CONDUCTOR class, in case of non-PCB product.

The field and value options provide additional filtering based upon the characteristics of the layer. For information on layer parameters, see the section Layer Parameter Attributes (Allegro Subclasses).

The information about the attributes and values permitted on a layer can be obtained using the following command.

> `axlLayerGet("ETCH/TOP")->??`

The base call is actually just:

`axlGetParam("paramLayerGroup:ETCH")->groupMembers`

#### Arguments

|  |
| --- | ---
| `field` | Optional field for filtering. Uses the value specified by the`value` argument to filter subclasses.
| `value` | Optional value of field to use for filtering. Requires field option to be passed.
#### Values Returned

List of subclass as strings.

#### See Also

[axlSubclasses](#1107319 "3"), [axlGetParam](#1126060 "3")

#### Example

* all etch subclasses

> `axlSubclassRoute() -> ("TOP" "GND" "VCC" "BOTTOM")`

* all subclasses that are of type etch

> `axlSubclassRoute(?field 'isEtch)`

* all subclasses that are not etch (e.g dielectric)

> `axlSubclassRoute(?field 'isEtch ?value nil)`

* all subclasses with material FR-4

> `axlSubclassRoute(?field 'material ?value "FR-4")`

### axlXSectionCopy

`axlXSectionCopy(o_xsectionDBID) => g_xsectionDefstruct/nil`

#### Description

This copies dbid xsection to an xsection Skill defstruct.It can be used to duplicate the charactistics of an existing xsection layer to a new layer for use with axlXSectionCreate. Alternatively, it can be used to modify an existing layer via axlXSectionSet, although axlXSectionModify might be a better fit for changing a layer.

This creates a new defstruct using`make_axlXSection()`.The name attribute is never copied.

* ***If using this to copy named layers, you need to set the name attribute in the defstruct returned by this function.***

#### Arguments

|  |
| --- | ---
| `o_xsectionDBID` | a xsection dbid
#### Value Returned

|  |
| --- | ---
| `g_xsectionDefstruct` | a defstruct with its attribute data copied from dbid
#### Examples

* See <cdsroot>/share/pcb/examples/skill/dbcreate/xsection.il

#### See Also

[axlXSectionCreate](#1168694 "3"), [axlXSectionModify](#1172362 "3")

### axlXSectionCreate

`axlXSectionCreate(nilg_option[g_xsectionDefStruct]) => o_xsectionDBID/nil`

#### Description

Creates a new cross section entry.

The three critical create items in`g_xsectionDefStruct` are:

* name - a string which is a name of the layer

* layerType - a string (see`axlXSectionLayerTypes()` for supported of types) that describes the type of layer.

> > Popular types are CONDUCTOR, PLANE, DIELECTRIC or MASK. If no value is specified, DIELECTRIC is used as the default value.

* material - a string that describes substance making up the xsection entry. Default is FR-4 for dielectrics and COPPER for conductor/plane.

> If no attributes are provided, an unnamed xsection entry of type DIELECTRIC, with material FR-4 is created.

You can set other xsection entries, see`axlXSectionGet` for a description of the other available attributes. If material is provided it will auto-fill additional based upon the materials file.

For named xsection layers, it creates a class/subclass on the etch layers, it does not set the color and visibility for those layers. You need to use`axlLayerSet` for those attributes.

Allegro PCB does not allow name layers above top or below bottom.

RESTRICTION - Currently, it is not possible to create manage multiple stackups via Skill. This restriction will be removed in a future release.

#### PROGRAMMING TIPS

* For populating multiple internal layers, use the`'bottom` option and build the stackup from bottom to top.

* Ensure that there is at least one dielectric layer between each CONDUCTOR or PLANE layer type. Adjacent routing layers are allowed, but this results in incorrect signal analysis.

* Do not name dielectric layers unless you want to physically add and edit objects to those layers. In Allegro PCB Editor, every named layers creates an entry in the class/subclass table on ETCH related classes.

* Material names that are not contained in the`materials.dat` file, can also be specified. Setting environment variable "`xsection_material_warning`" prints a warning. When unknown materials are specified the thickness and other associated data are not populated.

* Changing the material also updates its associated data. This is only an issue with the`axlXSectionSet` API.

* layerId defaults to the layer number.

* When creating MASK layers, you must provide the`?name` option. If you provide both, a `?name` and `?maskLayer` option, then `?maskLayer` name wins.

* MASK layers added between TOP and BOTTOM do not effect connectivity.

* Constraint Manager removes the '\_' in pretty printing layerFunction.This interface requires them (see types returned by`axlXSectionLayerFunctions` API). Mask and dielectric have different allowed function types.

* Use`axlXSectionModify` or [axlXSectionCopy](#1168597 "3") to create the `axlXSection` defstruct. Do not directly call `make_axlXSection`.

* DRC is marked out of date with cross section changes.

#### Arguments

|  |  |
| --- | --- | ---
| `nil` | First argument must always be nil |
| `g_option` |  |
|  | `'top` | insert layer above top. For PCB designs this can only be a unnamed dielectric or MASK layers.
|  | `'bottom` | insert layer above bottom
|  | `'afterBottom` | insert layer after bottom. For PCB Designs this can only be unnamed dielectrics or MASK layers.
|  | `t_etchSubclass` | sublass name, insert layer above this name
|  | `x_position` | insert above xsection position. This is the position attribute and an xsection dbid. You cannot insert above 0 (Surface).
| `g_xsectionDefStruct` or `nil` | A Skill defstruct with all possible attributes for xsection entry |
|  | `make_axlXSection` | creates a new entry
|  | `copy_axlXSection` | copies an existing entry
|  | `axlXSectionCopy` | copies contents of an existing xsection dbid to a new deftruct.
#### Value Returns

|  |
| --- | ---
| `o_xsectionDBID` | if successful
| `nil` | failed.
#### Examples

> `see <cdsroot>/share/pcb/examples/skill/dbcreate/xsection.il`

#### See Also

[axlXSectionGet](#1169585 "3"), [axlXSectionSet](#1172523 "3"), [axlXSectionDelete](#1169205 "3"), [axlXSectionLayerTypes](#1172321 "3"), `axlXSectionCopy`, `axlXSectionModify`, `axlXSectionLayerFunctions`

### axlXSectionDelete

`axlXSectionDelete(g_option) => lt_types`

#### Description

Deletes a cross section layer. If layer is associated with an ETCH layer, the associated layer is also deleted. Associated ETCH layers must not have objects. See[axlLayerDelete](#1150567 "3") for other reasons for failure.

#### Arguments

|  |
| --- | ---
| `g_option` |
| `o_xsectionDBID` | delete layer by XSection dbid
| `t_etchSubclass` | delete layer by this name
| `x_position` | delete layer by position. This is the position attribute in the xsection dbid.
#### Value Returned

|  |
| --- | ---
| `t` | if successful
| `nil` | failed.
#### Examples

See`<cdsroot>/share/pcb/examples/skill/dbcreate/xsection.il`

#### See Also

[axlXSectionCreate](#1168694 "3"), axlLayerCreate, [axlDeleteByLayer](25dbmisc.html#1095212 "26")

### axlXSectionGet

`axlXSectionGet(g_stackup/nilg_option)==> g_data/nil`

#### Description

Returns data about the cross-section entry for a design.

Supports multiple access options (see Arguments).

Allegro design color and visibility query needs are satisfied by the[axlLayerGet](#1173865 "3") API.

#### Arguments

* for cross sections with a single stackup this returns the standard stackup. For Rigid-Flex designs this returns All Stackups.
* name of stackup. From zone groups it is the name in zoneDbid -> stackup or available stackups are return by`axlXSectionGet(nil 'stackups)`
* return a list of stacks. g\_xsection is ignored and should be nil
* return number of cross section entries for provided stackup. g\_data is x\_entries
* return maximum number of individual stackups database supports
* return provided stackup thickness in user units g\_data is f\_thickness design units, accuracy is not restricted to current design accuarcy. This is the total thickness with masks.
* return cross entry for top layer of design
* return cross entry for bottom layer of design
* return cross entry for given position in "All stackups". This is the number field in a xsection dbid. (0 is the 1st layer -- air)
* name of etch subclass. g\_data is a o\_xsection DBID
* return entire stackup. g\_data must be a lo\_xsectionDBID
* '`layer`: add or delete layers
* '`value`: cannot edit values

* The name of the stackup can be obtained from the zone dbid by zoneDbi->stackup

* If using a single stackup in a design pass`nil` as the first argument.

* If a multi-stackup design, a nil returns all of the xsection dbids (e.g. "All Stackups"). If you need the main stackup, typically called "primary", use its name.

* Except for`'stackups` and `'locked` all other options take into account the stackup argument.

* Thickness if`g_xsection` is we return the all stackup thickness which can be overridden by the TEXT\_BOARD\_THICKNESS property assigned at the design level. Otherwise if a stackup (`g_xsection`) name is provided returns the calculated thickness of the indicated stackup.

#### XSection Attributes:

Attributes that have Yes under Modify column can be set with APIs[axlXSectionCreate](#1168694 "3") and axlXSectionSet.

|  |  |  |
| --- | --- | --- | ---
| **NAME** | **TYPE** | **Modify** | **DESCRIPTION**
| objType | string | No | "xsection"
| readOnly | t | No | Cannot directly modify entry
| constraint | string | Yes | (Optional) Techfile generic layer support (max 1023 chars).
| conductor | t/nil | Yes | Is layer of conductor or plane?
| layerType | string | Yes | Type of xsection layer.
| layerFunction | string | Yes | Layer function of a layer. This is a superset of layer types for dielectric and mask layers. Conductor, plane and surface layers cannot have their layerFunction changed. When creating a layer, Allegro automatically assigns a default function based on the layer type. Can be nil (surface layers).
| layerId | string | Yes | Override of via label id (max 3 characters)
| material | string | Yes | Layer material (max 250 chars)
| maskLayer | string | Yes | Mask layer associated with this cross section entry.  This is`nil` unless the layerType is type MASK. If a string is present it will have the same name as the name field.
| mfg | string | Yes | (Optional) Stackup layer grouping for IPC2581 (max 255 chars)
| name | string/nil | Yes | Name of xsection/etch layer (max 47 chars).
| negativeArtwork | t/nil | Yes | Layout is a negative image.
| polyCutLayer | t/nil | Yes | Layer is a cut layer for poly vias. Only dielectric layers between the surface layers may be cut layers. You cannot unset a cut layer that is being used by a poly via.
| position | integer | No | Position of xsection layer in stackup. This is relative to the stackup. (starts at 0 for SURFACE).
| prop | l\_dbid | Yes | List of properties on object.
| thickness | float | Yes | layer thickness in design units, stored with more accuracy then design
| tolMinus | float | Yes | thickness tolerance - in design units, stored with more accuracy then design
| tolPlus | float | Yes | thickness tolerance + in design units, stored with more accuracy then design
| Pad suppression: |  |  |
| `unusedPin` | t/nil | Yes | suppress unused pads of pins on this layer
| `unusedVia` | t/nil | Yes | suppress unused pads of vias on this layer
| Embedded support: |  |  |
| `embedded` | string | Yes | Type of embedded layer (default NOT\_EMBEDDED)  Values:  nil, NOT\_EMBEDDED, BODY\_UP, BODY\_DOWN PROTRUDING\_ALLOWED
| `embeddedAttach` | string | Yes | Type of attachment if embedded layer.  Values:  nil, DIRECT\_ATTACH, INDIRECT\_ATTACH
| Electrical paramters: |  |  |
| `diffCouplingType` | string | Yes | Diffpair routing on layer (Values: nil or EDGE)
| `diffSpacing` | float | Yes | Typical diffpair spacing on this layer in design units (only if coupling type is set)
| `conductivity` | string | Yes | Layer conductivity (MKS in mho/cm)
| `dielectricConst` | string | Yes | Dielectic constant
| `etchFactor` | integer | Yes | Vertical geomety of etch (angle 45-135 or 225-315 degrees)
| `freqDepFile` | string | Yes | (optional) Frequent dependant file for this layer (max 255 chars)
| `lossTangent` | string | Yes | Loss tangent value
| `shield` | t/nil | Yes | Is this a shield layer
| `width` | float | Yes | Typical layer width for Impedance what-ifs in design units
| `siIgnore` | t/nil | Yes | SI should ignore this layer
#### Value Returned

|  |
| --- | ---
| `nil` | an error
| `g_data` | depends on g\_option, see**Arguments** section
#### Examples

* Get design thickness

> `thick = axlXSectionGet(nil 'thickness)`

* Fetch entire cross section

> `stackup = axlXSectionGet(nil 'all)`

* Fetch just the top layer

> `xs = axlXSectionGet(nil 'top)`

* Fetch dielectric below top

> `xs = axlXSectionGet(nil 'top)`

> `dielectric = axlXSectionGet(nil xs->number +1)`

> `axlPrintDbid(dielectric)`

* Get all stackups (even with one stackup will return PRIMARY)

> `stackups = axlXSectionGet(nil 'stackups)`

* get stackup called FLEX2

> `zoneStackup = axlXSectionGet("FLEX2" 'all)`

* get number of layers in FLEX2 (includes etc, dielectric and layers above surface)

> `zoneStackup = axlXSectionGet("FLEX2" 'count)`

* See`<cdsroot>``/share/pcb/examples/skill/dbcreate/xsection.il`

### axlXSectionLayerFunctions

`axlXSectionLayerFunctions() => lt_types`

#### Description

Return list of supported layer function types.Layer functions are a super set of layer types.

#### Arguments

None

#### Value Returned

* List of strings of supportted layer types.

#### Examples

> `only use types = axlXSectionLayerFunctions()`

#### See Also

[axlXSectionCreate](#1168694 "3")

### axlXSectionLayerTypes

`axlXSectionLayerTypes() => lt_types`

#### Description

Return list of supported layer types. This is used withlayerType attribute when adding or modifing xsection layers.

#### Arguments

None

#### Value Returned

* List of strings of supportted layer types.

#### See Also

[axlXSectionCreate](#1168694 "3")

#### Examples

> `only use types = axlXSectionLayerTypes()`

### axlXSectionModify

```
axlXSectionModify(<list of defstruct attributes and values>) => g_xsectionDefstruct/nil
```

#### Description

This is a wrapper for`make_axlXSection()` function to createa new defstruct. For certain fields (e.g. boolean and some string fields) a `'none` symbol is used to indicate that the field should not be changed, other fields can use the default `nil` symbol.

#### Arguments

Same as`make_axlXSection()`.

#### Value Returned

|  |
| --- | ---
| `g_xsectionDefstruct` | a defstruct with its attribute data copied from provided arguments
#### Examples

* Modify a layer to be negative artwork assume a layer named GND exists. All other layer characturistics will remain the same

> ```
> xs = axlXSectionGet(nil "GND")negative = axlXSectionModify(?negativeArtwork t)ret = axlXSectionSet(xs negative)
> ```

* See <cdsroot>`/share/pcb/examples/skill/dbcreate/xsection.il`

#### See Also

[axlXSectionCreate](#1168694 "3")

### axlXSectionSet

`axlXSectionSet(g_option[g_xsectionDefStruct]) => t/nil`

`axlXSectionSet('lockednil/l_lockType) => t/nil`

#### Description

Modifies an existing cross section entry. Use[axlXSectionModify](#1172362 "3") to create a xsection defstruct with the attributes you wish to modify.

See[axlXSectionGet](#1169585 "3") for a description of the other available attributes. If changing material, it also updates the material characteristics to values of the new material.

Allegro PCB editor does not allow name layers above top or below bottom.

**PROGRAMM TIPS**:

* See tips in[axlXSectionCreate](#1168694 "3").

* In Allegro PCB Editor, you cannot rename TOP or BOTTOM.

* Cannot unname a layer with data on the ETCH layers.

* DRC is marked out of date.

#### Arguments

* first argument must always be`nil`
* delete layer by XSection dbid
* modify by sublass name
* modify by xsection position. This is the number attribute in the xsection dbid.
* update user inteface layer locking
* A SKILL defsruct with all possible attributes for xsection entry
* creates a new entry
* copies an existing entry
* copies contents of an existing xsection dbid to a new deftruct.
* list of both
* may be nil to unlock
* `'layer`- prevent layer addition or deletion
* `'value` - prevent changing values

#### Value Returned

|  |
| --- | ---
| `t` | if successful
| `nil` | failed.
#### See Also

[axlXSectionCreate](#1168694 "3"), [axlXSectionCopy](#1168597 "3")

#### Examples

* See`<cdsroot>/share/pcb/examples/skill/dbcreate/xsection.il`

* lock layer values

> `axlXSectionSet('locked 'layer)`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
