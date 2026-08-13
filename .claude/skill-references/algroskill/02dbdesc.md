### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

2
=

The Allegro PCB Editor Database User Model
==========================================

Overview
--------

This chapter describes each AXL database object type, listing each type's attributes and relationships to other object types.

**Object Types**

* Figure objects

* Arcs ([Table 2-3](#603813 "2"))

* Branches ([Table 2-4](#603895 "2"))

* Design Files ([Table 2-5](#619351 "2"))

* DRCs ([Table 2-6](#619953 "2"))

* Lines ([Table 2-12](#620208 "2"))

* Paths ([Table 2-15](#603607 "2"))

* Polygons ([Table 2-17](#452097 "2"))

* Pins ([Table 2-16](#610509 "2"))

* Shapes ([Table 2-19](#604105 "2"))

* Symbols ([Table 2-20](#604789 "2"))

* Tees ([Table 2-22](#604909 "2"))

* Vias ([Table 2-24](#605063 "2"))

* Pads ([Table 2-13](#608961 "2"))

* Padstacks ([Table 2-14](#624011 "2"))

* Symdefs ([Table 2-21](#609305 "2"))

* Logical objects

* Components ([Table 2-27](#460883 "2"))

* Functions ([Table 2-29](#605432 "2"))

* Function Pins ([Table 2-30](#605494 "2"))

* Nets ([Table 2-32](#605564 "2"))

* Property dictionary objects ([Table 2-41](#608499 "2"))

* Parameter objects

* Design ([Table 2-44](#597057 "2"))

* Display ([Table 2-45](#597099 "2"))

* Layer Group ([Table 2-47](#621012 "2"))

* Layer ([Table 2-48](#621110 "2"))

* Textblock Group ([Table 2-49](#605971 "2"))

* Textblock ([Table 2-50](#606032 "2"))

Description of Database Objects
-------------------------------

Although a database object type can have dozens of attributes, you need only learn the semantics of a few attributes to get useful information from the Allegro PCB Editor database. Requesting an attribute not applicable to an object, or a property not existing on the object, causes the access function to return`nil`.

#### AXL Database Rules

The Allegro PCB Editor database interacts with AXL functions as specified in the following rules. Changes to the Allegro PCB Editor database made using AXL functions can affect both the database references (`dbids`) and the attributes of the Allegro PCB Editor database objects that the AXL program has already accessed.

* Invoking the`axlShell` function or editing a new Allegro PCB Editor database invalidates all `dbids`.

> Accessing the object's attributes with an out-of-scope`dbid` yields unreliable values. The `axlDBRefreshId` function returns `nil` for any out-of-scope `dbid`.

* An AXL function that modifies one attribute of an object may cause a related attribute of that object to become out-of-date.

> A parent's attribute may become out-of-date when you modify one of its children's attributes. For example, changing path width might affect the bounding box attribute of both a child and its parent.

* Operations you perform on an object affect the attributes of other objects if they refer to the changed object either directly or indirectly.

> An example of direct reference is deleting a segment from a path. An example of indirect reference is changing the width of a single segment in a path. These can cause`isSameWidth` to be incorrect.

* Accessing an out-of-date`dbid` does not cause the AXL program to crash or corrupt the Allegro PCB Editor database.

* The AXL function,`axlDBRefreshId`, updates an object.

> AXL does not update objects asynchronously.

* Allegro PCB Editor maintains properties across operations for all objects that support properties.

* DRC objects are volatile.

> By changing Allegro PCB Editor database objects, you can create or destroy DRCs.

> You cannot*directly* change a DRC object.

The following Allegro PCB Editor rule for treating non-etch figures applies only to paths or path segments:

* Path`dbids` on non-etch layers are more stable than those on etch layers.

> Deleting a segment from a path breaks the segment into two paths with separate`dbids`. Non-etch paths never merge, even if they touch.

The Allegro PCB Editor database treats etch figures differently from non-etch figures. The following are the etch figure rules.[Figure 2-1](#451877 "2") shows the connectivity model used by Allegro PCB Editor.

* Path, line and arc`dbids` are volatile on etch layers.

> Allegro PCB Editor merges and breaks these objects to maintain connectivity.

* Deleting a segment from a path so it detaches from a pin, via, tee, or shape causes the etch to be classed as*floating*.

> That means the etch is not a member of any net. A floating etch has a`nil` netname.

* Tees and branches are volatile.

> Changes in paths or path segments can cause tees to disappear or branches to combine or break into multiple branches.

****Figure 2-1****
**Allegro PCB Editor Connectivity Model**

#### Data Types

AXL database objects can have the following data types:

|  |
| --- | ---
| **Type** | **Meaning**
| bbox | Boundary box (list of two points, lower left and upper right of a rectangular area that encloses the object)
| integer | Signed integer number
| float | Floating-point number
| string | A string. For attributes with a list of possible string values, the attribute description lists the allowed values.
| t/nil | Either true (`t`) or false (`nil`)
| dbid | Allegro PCB Editor object identifier
| l\_dbid | List of`dbids`
| point | A point--a list of two floats denoting a coordinate pair
| l\_propid | A list of properties accessed by`axlDbGetProperties`
| l\_fill | `t` = solid; `nil` = polygon; `r_fill` = crosshatch type
#### Generic Allegro PCB Editor Object Attributes

The following attributes are generic to all Allegro PCB Editor database objects. All Allegro PCB Editor database objects have at least these attributes.

****Table 2-1****
**Generic Object Attributes**

| **Attribute Name** | **Type** | **Description**
| objType | string | Name of the object type
| prop | propid | Attached properties
| parentGroups | l\_dbid | List of groups to which the object belongs
| readOnly | `t`/`nil` | `t` = cannot modify object with AXL function
`propid` refers to properties attached to the object. When a `dbid` is returned to an AXL program, the properties attached to that object are not immediately returned. You access the property value by referencing the property name via the prop attribute. The `axlDBGetProperties` function returns the property names/value pairs as an "assoc" list to allow easier processing by applications.

Figure Database Types
---------------------

Figures, in Allegro PCB Editor, also share a common set of attributes. However, "figure" is not actually an attribute of any object.[Table 2-2](#608667 "2") lists the common figure attributes. In Allegro PCB Editor, figures are sometimes called geometries.

Among other attributes, figures have a bounding box called`bBox`. `bBox` is an orthogonal rectangle that defines the geometrical extents of the figure.

****Table 2-2****
**Common Figure Attributes**

| **Attribute Name** | **Type** | **Description**
| bBox | bbox | Figure's bounding box
| branch | dbid | For etch, the figure's branch parent
| layer | t\_layer | Layer of figure,`nil` if object is multi-layer
| parent | dbid | Nonconnective owner
| net | dbid | Net object if figure is associated with a net
**Note:** The`"net"` attribute is an empty string `""` for all figures that are on a dummy net.

#### Attributes for Each Figure Type

The following tables list the attributes specific to each Allegro PCB Editor object type. The Common Figure attributes (see[Table 2-2](#608667 "2")) and the Generic Allegro PCB Editor Object attributes (see [Table 2-1](#608677 "2")) also apply to these figure types.

The tables are in alphabetical order by figure type name. The attributes in each table are in alphabetical order by attribute name.

****Table 2-3****
**Arc Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| isCircle | t/nil | `t` = circle; `nil` = unclosed arc
| isClockwise | t/nil | `t` = clockwise; `nil` = counterclockwise
| isEtch | t/nil | `t` = a CLINE; `nil` = a LINE
| objType | string | Type of object, in this case`"arc"`.
| parent | dbid | Path, polygon or shape
| radius | float | Radius
| startEnd | l\_point | Start and end points of arc
| width | float | Width of arc
| font | symbol/nil | Line font, etch and solid is`nil`.  Other types are`'HIDDEN` `'PHANTOM` `'DOTTED` `'CENTER`
| xy | point | Location of arc center
****Table 2-4****
**Branch Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| children | l\_dbid | List of`dbids` of the objects that make up branch: paths, tees, vias, pins and shapes
| objType | string | Type of object, in this case`"branch"`
| parent | dbid | Always`nil`
****Table 2-5****
**Design Attributes  Represents the design root, axlDBGetDesign()**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| bus | l\_dbid | List of busses
| compdefs | l\_dbid | List of component definitions
| components | l\_dbid | List of components
| designOutline | dbid | Design outline shape/rect, nil if none (layer BOARD GEOMETRY/DESIGN\_OUTLINE)
| diffpair | l\_dbid | List of differential pairs
| drcs | l\_dbid | List of DRCs
| drcState | symbol | State of DRC`t` = up to date `nil` = out-of-date `batch` = batch out-of-date
| ecsets | l\_dbid | List of Electrical Csets
| groups | l\_dbid | List of groups
| keepinPlace | dbid | Place shape/rect keepin, nil if none (layer PACKAGE KEEPIN/ALL)
| keepinRoute | dbid | Route shape/rect keepin, nil if none (layer ROUTE KEEPIN/ALL)
| matchgroup | l\_dbid | List of match groups in the design
| module | l\_dbid | List of module instances in the design
| nets | l\_dbid/nil | List of nets
| netclass | l\_dbid | List of netclass constraints group
| netgroup | l\_dbid | List of netgroups in the design
| objType | string | Type of object, in this case`"design"`
| region | l\_dbid | List of regions
| padstacks | l\_dbid | List of padstacks
| pins | l\_dbid | If a`.dra`, list of pins, else `nil`
| symbols | l\_dbid | List of symbol instances
| symdefs | l\_dbid | List of symbol definitions
| text | l\_dbid | List of unattached text in design. These are not associated with any other object.
| waived | l\_dbid | List of waived DRCs
| xnet | l\_dbid | List of Xnets (no nets with VOLTAGE property)
* **Description**
* Actual value (user units)
* Expected value (user units)
* `t` = Allegro PCB Editor generated DRC
  `nil` = user defined DRC
* Name of constraint that was violated
* Type of object, in this case`"drc"`
* Design`dbid`
* DRC source (property or constraint set name)
* "EXTERNAL REFERENCE"
* "NET SPACING CONSTRAINTS"
* "PHYSICAL CONSTRAINTS"
* "DESIGN"
* "NET ELECTRICAL CONSTRAINTS"
* "SAME NET CONSTRAINTS"
* List of figures causing error (2 max)
* `t` = waived drc
  `nil` = regular
* Location of DRC marker

****Table 2-7****
**FUNCDEF Attributes: Function definition (logic element)
 Component definition has a list of funcdef (functions)**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| objType | string | "funcdef"
| parent | dbid | compdef (Component Definition)
| pins | l\_dbid | list of funcdefPin (Function definition pins)
| slot | string | Name of Slot (function def name)
| type | string | Type of function
****Table 2-8****
**FUNCDEFPIN Attributes: Function definition pin (logic element)**

| **Attribute Name** | **Type** | **Description**
| Function definition has a list of these pins each with point has a link to the component def pin  Also includes generic object attributes | |
| objType | string | `"funcdefPin"`
| parent | dbid | pin (component pin definition)
| name | string | Name of the pin
| swapCode | integer | The swap code (pins with common codes can be swapped)
| use | string | Use of pin (e.g. UNSPEC)
****Table 2-9****
**FIGURE Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic and figure object attributes | |
| corners | string | Rnd Rect and Rect pad only: corners chamfered, dash seperated:  |  |  |  | | --- | --- | --- | |  |  | UR - upper right |  |  |  |  | | --- | --- | --- | |  |  | UL - upper left |  |  |  |  | | --- | --- | --- | |  |  | LR - lower right |  |  |  |  | | --- | --- | --- | |  |  | LL - lower left |  `nil` if pad type does not support
| drillChar | string | drill characters (max 3)
| figureName | string | figure type
| fill | t/nil | is figure filled (usually t)
| inside | float | Donut pad only: inside diameter, 0 otherwise  **Note:** Outside diameter needs to be obtained form the bBox attribute (maxX - minX);
| height | float | height of figure
| objType | string | "figure"
| radius | float | Rnd Rect and Rect pad only: corner radius, 0 otherwise
| rotation | float | rotation absolute
| width | float | width of figure
| xy | point | Figure placement location
****Table 2-10****
**Group Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| groupMembers | l\_dbid | List of members of the group
| name | string | Name of the group
| objType | string | Type of object, in this case`"group"`
| type | string | Predefined group type.  **Note:** This cannot be defined in SKILL. User defined groups are considered "GENERIC."
****Table 2-11****
**Module Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| bBox | bBox | Bounding box of all physical members of group
| groupMembers | l\_dbid | List of members of the module
| name | string | Name of the module
| objType | string | Type of object, in this case`"group"`
| placeReplicate | t/nil | `t` if module is from Place Replicate, `nil` if a basic module
| type | string | "`MODULE`"
****Table 2-12****
**Line Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic and figure object attributes | |
| isEtch | t/nil | t = a CLINE;`nil` = a LINE
| lineType | s\_type | a symbol: horizontal, vertical, odd
| objType | string | Type of object, in this case`"line"`
| parent | dbid | Path, polygon, or shape
| startEnd | l\_point | Start and end points
| thermal | t/nil | Cline is a thermal relief.
| width | float | Width of line
| font | symbol/nil | Line font, etch and solid is nil.  Other types are 'HIDDEN 'PHANTOM 'DOTTED 'CENTER
* **Description**
* Bounding box. Coordinates are always relative.
* List of`r_paths` defining pad's boundary `lr_path` always contains at most one `r_path` `nil` denotes a null pad
* Type of pad figure.

  Examples are "CIRCLE", "SQUARE", "SHAPE", "NULL". May be nil if drill. Use axlPadFigureTypes() to obtain list of figures
* If of type`FLASH`, name of flash symbol otherwise an empty string ""

  (Obsolete; use name attribute)
* Pad layer

  For regular layers and mask layers this is a string. For composite, internal, adjacent, backdrill layers this is a symbol
* If type is a`SHAPE` or `FLASH,` name of symbol.
* Type of object, in this case`"pad"`
* Offset of pad (relative to pin/via origin)
* Padstack`dbid`
* Cannot be modified.
* Pad type is one of:`REGULAR`, `ANTI`, `THERMAL, or KEEPOUT`
* Octagon pad only: Number of sides, 0 otherwise

  Ranges between 6 and 64 as an even integer.
* Donut pad only: inside diameter, 0 otherwise

  **Note:** Outside diameter needs to be obtained form the bBox attribute (maxX - minX);
* Rnd Rect and Rect pad only: corner radius, 0 otherwise
* LL - lower left
* UR - upper right
* UL - upper left
* LR - lower right

* **Description**
* (see isPadRef) Points to padstack definition if this is padReference otherwise`nil`
* if a dervived padstack name of original padstack, else nil
* drill characters (max 3)
* Drill hole diameter
* width of slot, diameter if hole and extents of multidrill
* height of slot, diameter if hole and extents of multidrill
* Name of drill to use (optional)
* offset of drill hole
* type of drill symbol (circle, square, and so on.
* Width of drill symbol
  (for slots same as drillSizeWidth)
* Height of drill symbol
  (for slots same as drillSizeHeight)
* Type of drill (nil is standard)
  (not supported by slots)
* Description of actual drill. This field was introduced in 17.0 to describe the drill used. It should NOT be treated as a number.

  Is optional and may be an empty string.
* If counter sink reports angle of sink with range 0 to 90.
* If counter bore report depth of sink in user units.

  This is maintained with an accuracy greater than the design
* Diameter of counter bore/sink in user units
* If counter bore/sink a list of two design units reporting the + and - tolerance of bore/sink
* If counter bore reports "bore"

  If counter sink reports "sink" else is nil
* A list of two numbers reporting the + and - drill hole tolerance.
* If slot is list of two design units reporting the + and - 'Y' drill hole tolerance. This is the routing drill tolerance.
* If not multidrill then nil otherwise list of:

  (`rows columns clearanceX clearanceY staggered`)

  Both clearances are in`dbreps` and staggered is `t/nil`
* Type of hole (CIRCLE\_DRILL, OVAL\_SLOT, etc.)
* This is obsolete for 17.0.

  Use routekeep layer for padstacks
* `t` = padstack is a padstack reference.

  This means that the actual padstack is a template and the start and end layers of the padstack are dynamically mapped, depending upon its use with a pin or a via.
* `t` = through padstack
* Padstack name
* Type of object, in this case`"padstack"`
* List of pads
* Design
* Does padstack have Pad Suppression enabled. This is for the legacy artwork based pad suppression.

  The dynamic pad suppression ignores this option.
* One of "Plated" or "Non-Plated".

  In 17.0 "Plating-Optional" is obsolete.
* Always`nil`, padstacks do not support properties
* Reports non-zero if padstack will not expand, if new layers are added or deleted.

  0 if padstack will exapnd (this is the default).

  In the future, this may report the number of layers the padstack covers in lock layer span mode.
* Start and end layer of padstack
* uvia
* through
* smd
* bbvia
* mounting\_hole
* through
* smd
* bbvia
* uvia
* die\_pad\_legacy
* through\_pin
* surface\_pin
* through\_via
* die\_pad
* bond\_finger
* fiducial
* slot
* mechanical\_hole
* tooling\_hole
* A sub-type of bbvias, to differentiate in constraint system.
* Diameter of backdrill
* type of drill symbol (circle, square, and so on.)
* Backdrill characters (max of 3)
* Height of backdrill figure
* Width of backdrill figure

****Table 2-15****
**Path Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| branch | dbid/nil | Branch owner
| hasArcs | t/nil | `t` = path has one or more arcs
| isSameWidth | t/nil | `t` = all segments in path have same width
| isEtch | t/nil | t = a CLINE; nil = a LINE
| nSegs | integer | Number of segments in path
| objType | string | Type of object, in this case`"path"`
| parent | dbid | Branch, symbol, shape or`nil`
| segments | l\_dbid | List of arc and line figures in this path
| symbolEtch | dbid | Symbol owner if etch.
| startEnd | lt\_layer | If bond-wire start and end layers;  nil if not bondwire.  If bondwire has a disconnected end, then the start and/or end will be`nil`
****Table 2-16****
**Pin Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| branch | dbid/nil | Branch owner
| component | dbid/nil | Component owner of pin  `nil` if unassigned symbol pin
| definition | dbid/nil | Padstack definition  `nil` if unplaced component pin
| fixedByTestPoint | t/nil | OBSOLETE - kept for backwards compatibility. Use`axlDBIsFixed(`<`dbid`>`)` or `axlDBControl(?testPointFixed)` instead.
| functionPins | l\_dbid/nil | List of function pins  `nil` if unassigned symbol pin
| isExploded | t/nil | `t` = pin is instance edited
| isMech | t/nil | `t` = pin is mechanical
| isMirrored | t/nil | `t` = pin is mirrored
| isThrough | t/nil | `t` = pin is a throughhole
| mirrorType | string | Type of mirror.
| name | string | Padstack name of this pin  `nil` if unplaced component pin
| number | string | Pin number
| objType | string | Type of object, in this case`"pin"`
| pads | l\_dbid | Unordered list of pads.1 To access a particular pad, use `axlDBGetPad`.
| parent | dbid | `dbid` of symbol owning this pin2  `nil` if pin is standalone (as it is in a symbol drawing)
| relRotation | float | Pin rotation (relative to symbol)
| relxy | point | Location (relative to symbol)
| rotation | float | Pin rotation (absolute)
| startEnd | lt\_layer | Range of layers spanned by pin2
| testPoint | t\_layer/nil | `t_layer`, denotes layer of testpoint `nil` = pin is not a testpoint
| use | string | Pin use as shown by show element
| xy | point | Location of pin in absolute coordinates
1. May be`nil` if component is unplaced.

2. Will say etch/(unknown) if unplaced component.

**Note:** Ppins straddle the line between physical and logical elements. They have attributes that are conditional on their owners. If the padstack definition is`nil`, then the pin is purely logical. If the component attribute is `nil`, then the pin is purely physical. If both are non-`nil`, then the pin is fully instantiated.

****Table 2-17****
**Polygon Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| area | float | Area of the polygon in drawing units.
| bBox | bBox | Bounding box.
| holes | list | List of`o_polygons`.
| isHole | t/nil | `t` = polygon is a hole
| isRect | t/nil | `t` = polygon is a rectangle
| nSegs | integer | Number of segments in polygon
| objType | string | Type of object, in this case`"polygon"`
| parent | dbid | Symbol, shape (for voids), or`nil`
| segments | l\_dbid | Path describing boundary of shape. Boundary consists of line and arc segments.
| symbolEtch | dbid | Symbol owner if etch
| vertices | list | Outer boundary available as a list containing a point, which is the vertex of a polygon, and a floating point number, which is the radius of the edge from the previous to the present vertex.
****Table 2-18****
**Rat\_T Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| name | string | Name of T to T-<n>
| net | dbid | Net of Rat-T
| objType | string | Type of object, in this case`"rat_t"`
| parent | dbid | Net
| xy | point | Location of T
****Table 2-19****
**Shape Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| bBox | bBox | Bounding box
| cavity | t/nil | If a boundary shape is for cavity generation (embedded design). Cavity shapes are generated automatically based on the rki.
| branch | dbid/nil | Branch owner
| children | l\_dbid | Used when a Boundary Shape points to a list of dynamic shapes
| connect | l\_dbid/nil | List of connected figures
| fill | g\_fill/t/nil | Fill pattern (see[axlDBCreateOpenShape](03dbcre8.html#438449 "15")).  `t` = filled; `nil` = unfilled  Each`axlFillType` has spacing width, origin, and angle.
| fillet | t/nil | shape is a fillet (teardrop)
| fillOOD | t/nil | Dynamic fill is out of date.  `t` = shape needs fill updating   (Only dynamic shapes can be `t`)  `nil` = shape does not refill
| voids | list | List of o\_polygons
| isHole | t/nil | `t` = polygon is a hole  `nil` = polygon is not a hole
| isRect | t/nil | `t` = shape is a rectangle
| nSegs | integer | Number of segments in polygon
| objType | string | Type of object, in this case`"shape"`
| parent | dbid | Branch (if etch shape), Symbol, shape (for voids)  `nil` = no parent
| priority | integer/nil | If shape is a dynamic shape boundary this is an integer voiding priority. For all other shapes this is`nil`. The priority is relative to other dynamic shapes on the same layer. If two dynamic shapes are coincident, the shape with the higher priority wins in voiding. This number is re-calculated as needed, so use only for comparison purposes.
| region | l\_dbid/nil | Region owner if a region shape.
| segments | l\_dbid | Path boundary of shape
| shapeAuto | l\_dbid/nil | If dynamic shape list of generated shapes on the matching auto-gen ETCH or CAVITY layer
| shapeBoundary | dbid/nil | If this shape is generated from a dynamic shape, this points to that shape.  Boundary shapes may either be used for ETCH or CAVITY (see state of cavity attribute)
| shapeIsBoundary | t/nil | This shape is a dynamic shape, for example, on BOUNDARY class.
| taper | t/nil | shape is used for tapering
| dynamicGroup | t/nil | If this a dynamic shape (BOUNDARY class) return its dynamic group object. This is where voiding instance overrides are stored.
| symbolEtch | dbid | Symbol owner, if etch
| vertices | list | outer boundary available as a list containing a point (vertex of a polygon) and a floating point number (radius of the edge from the previous to the present vertex).
| voids | l\_dbid | List of polygon boundaries defining voids in this shape
**Note:** You cannot manipulate (move, add property, delete and more) auto-generated shapes (shapeBoundary != nil). You should modify the dynamic shape (shapeBoundary). You can use`axlSetFindFilter` to set the find filter to auto-select the boundary shape when the user selects one of the auto-generated children.

****Table 2-20****
**Symbol Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| children | l\_dbid/nil | List of figures other than pins making up symbol
| component | dbid | Component owner of symbol
| definition | dbid | Symbol definition
| isMirrored | t/nil | `t` = symbol is mirrored
| mirrorType | string | Type of mirror.
| name | string | Symbol name
| objType | string | Type of object, in this case`"symbol"`
| parent | dbid | Design (no other parent possible for symbols)
| pins | l\_dbid/nil | List of pins
| refdes | string/nil | Reference designator
| rotation | float | Symbol rotation
| type | string | Symbol type is one of:`PACKAGE`, `MECHANICAL`, `FORMAT`, `SHAPE or DRAFTING`
| xy | point | Symbol location
| embedded | t/nil | symbol placed on embedded layer
| embeddedLayer | string | layer of placed symbol or nil if external
| embeddedMethod | string | method (CHIP\_UP or CHIP\_DOWN)
| embeddedAttach | string | attachment method (DIRECT\_ATTACH or INDIRECT\_ATTACH)
****Table 2-21****
**Symdef (Symbol Definition) Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| children | l\_dbid/nil | List of figures other than pins making up shape
| instances | l\_dbid | Symbol instances
| name | string | Name of symbol definition
| objType | string | Type of object, in this case`"symdef"`
| parent | dbid | Design
| pins | l\_dbid/nil | List of pins
| type | string | Symbol type is one of the following:`PACKAGE`, `MECHANICAL`, `FORMAT`, or `SHAPE`
****Table 2-22****
**Tee Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| branch | dbid | Branch owner
| objType | string | Type of object, in this case`"tee"`
| parent | dbid | Branch
| readOnly | t | User cannot directly modify
| xy | point | Location
****Table 2-23****
**Text Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| isMirrored | t/nil | `t` = text mirrored
| justify | string | `"left"`, `"right"` or `"center"`
| mirrorType | string | Type of mirror.
| objType | string | Type of object, in this case`"text"`
| parent | dbid | Symbol or`nil`
| rotation | float | Rotation angle
| text | string | The text itself
| textBlock | string | Text block type
| xy | point | Location of text origin
****Table 2-24****
**Via Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object and figure attributes | |
| branch | dbid/nil | Branch owner
| definition | dbid | Padstack definition
| isMirrored | t/nil | `t` = via mirrored
| isThrough | t/nil | `t` = through via
| mirrorType | string | Type of mirror.
| relations | list | List of relations of via  Currently supports return path capability  Format is one of the following:  `nil`  `('ground l_dbidVia)`  `('signal l_dbidVia)`
| name | string | Padstack name
| objType | string | Type of object, in this case`"via"`
| pads | l\_dbid | Unordered list of pads.  To access a specific pad, use`axlDBGetPad`.
| parent | dbid | Symdef or`nil`
| rotation | float | Via rotation
| startEnd | lt\_layer | Start and end layer of via
| testPoint | t\_layer/nil | Via test point state is one of: ETCH/TOP or ETCH/BOTTOM
| xy | point | Location of via
Logical Database Types
----------------------

Allegro PCB Editor logical database objects have these generic attributes (see[Description of Database Objects](#452619 "2")): objType, prop, and readOnly. Logical database objects do not have other attributes in common. The tables below list the attributes for each Allegro PCB Editor logical type.

****Table 2-25****
**Bus Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| groupMembers | l\_dbid | List of xnets of the bus
| name | string | Name of the bus
| objType | string | "`group`"
| type | string | "`BUS`"
| lock | t/nil | Is locked for editing (vector buses)
****Table 2-26****
**Compdef Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| class | string | Component classification
| components | l\_dbid | List of component instances of this definition.
| deviceType | string | Device type of the component
| functions | l\_dbid | List of functions.
| objType | string | Type of object, in this case`"compdef"`
| pins | l\_dbid | List of pins comprising the component.
****Table 2-27****
**Component Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| class | string | Component classification
| compdef | dbid | dbid of component definition (`COMPDEF`)
| deviceType | string | Device type of component (see`COMPDEF`)
| functions | l\_dbid | List of functions
| name | string | Reference designator
| objType | string | Type of object, in this case`"component"`
| package | string | Package name
| pins | l\_dbid | List of pins comprising component
| symbol | dbid/nil | `dbid` of the placed symbol of this component, `nil` if unplaced
****Table 2-28****
**Diffpair Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| groupMembers | l\_dbid | List of xnets of the differential pair
| name | string | Name of the differential pair
| objType | string | "`group`"
| type | string | "`DIFFPAIR`"
| userDefined | t/nil | If you create`t`, can be modified. `Nil` indicates creation by SigNoise models and cannot be changed.
****Table 2-29****
**Function Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| name | string | Function designator
| objType | string | Type of object, in this case`"function"`
| parent | dbid | `dbid` of component owning this function
| pins | l\_dbid | List of function pins composing function
| slot | string | Slot name
| type | string | Function type
****Table 2-30****
**Function Pin Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| name | string | Function pin name
| objType | string | Type of object, in this case`"functionPin"`
| parent | dbid | `dbid` of function owning this pin
| pin | dbid | Pin owner of function pin
| swap code | integer | Swap code of function pin
| use | string | Pin usage description, one of  `UNSPECIFIED`, `POWER`, `GROUND`, `NC`,  `LOADIN`, `LOADOUT`, `BI`, `TRU`, `OCA`, `OCL`
****Table 2-31****
**MATCH\_GROUP Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| groupMembers | l\_dbid | List of xnets, nets and pinpairs making up this group.
| name | string | Name of the match group.
| objType | string | "`group`"
| pinpair | l\_dbid | List of pinpairs associated with xnet
| type | string | "`MATCH_GROUP`"
**Note:** For more information, see`axlMatchGroupCreate`.

****Table 2-32****
**Net Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| branches | l\_dbid | List of branches
| name | string | Net name
| bus | dbid | Bus dbid if part of a bus
| nBranches | integer | Number of branches (when exactly one, net is fully connected)  **Note:** Island shapes causes the count to be not one, even if all pins are connected.
| objType | string | Type of object, in this case`"net"`
| pinpair | l\_dbid | List of pinpairs associated with net (`1`)  **Note:** If a net is a member of an xnet, all pinpairs appear on the xnet.
| ratsnest | l\_dbid | List of ratsnest for net.
| ratsnest On | t/nil | State of ratsnest display for the net.
| ratT | l\_dbid | List of rat\_T's. If none exist, this is NULL.
| rpd | l\_rpd | List of lists for each member net of a match group (`mg_dbid t_relatePropDelay`).  For more information, see`axlMatchGroupCreate`
| isBundled | t/nil | `t` = net contains at least one bundled ratsnest.
| scheduleLocked | t/nil | `t` = net schedule cannot be changed
| unconnected | integer | Number of remaining connections. This does not include connections to unplaced symbols.
| unplaced | integer | Number of unplaced pins.
**Note:**

1) If net is a member of an xnet then all pinpairs will appear on the xnet.

2) For more information on the rpd attribute see axlMatchGroupCreate

****Table 2-33****
**NETCLASS Attributes: NetClass objects for constraint grouping**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| groupMembers | l\_dbid | List of nets, xnets, buses or differential pairs.
| name | string | Name of the net class
| objType | string | "group"
| type | string | "NETCLASS"
| electrical | t/nil | If part of the electrical and same net domain
| physical | t/nil | If part of the physical and same net domain
| spacing | t/nil | If part of the spacing and same net domain
| **Note:** | |
| |  | | --- | |  | | | | **a.** | A NetClass can be a member of one or more domains but its name must be unique across all domains.
|
| ---
|
 **b.** | Constraint overrides can be added to netclass via properties. ||  |  |
****Table 2-34****
**REGION Attribute: Region objects for constraint grouping**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| groupMembers | l\_dbid | List of constraint area shapes.
| name | string | Name of the region
| objType | string | "group"
| type | string | "REGION"
****Table 2-35****
**CLASS Table Attribute**

| **Attribute Name** | **Type** | **Description**
| name | string | Name of ecset
| netclass1 | dbid | net class entry
| netclass2 | dbid | second net class entry (may be nil)
| region | dbid | region class for table entry (may be nil)
| physical | dbid | physical cset associated with entry or nil
| spacing | string | spacing cset associated with entry or nil
| sameNet | string | sameNet cset associated with entry or nil
| assembly | string | physical assembly cset associated with entry (SIP/APD only)
| objType | string | "classTable"
| readOnly | t/nil | Cannot be modified
| prop | l\_dbid | List of properties on table entry. Typically where constraint overrides on entry exist. Also duplicates the cset names.
**Note:** These are the class-class, class-class-region and class-region constraint table entries. See`axlCnsClassTableCreate`.

****Table 2-36****
**Pinpair Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| ecsetDerived | t/nil | If`t,` pinpair was created from an ECset. `Nil` indicates pinpair created due to net override property.
| groupMembers | l\_dbid | List of two pins making up pinpair.
| name | string | Name of the pinpair (`<refdes>. <pin#>: <refdes>. <pin#>`)
| objType | string | "`group`"
| parent | l\_dbid | Net or xnet owning the pinpair.
| parentGroups | l\_dbid | Lists match groups that have this pinpair. May also list other parent groups.
| rpd | l\_rpd | For each match group that has this pinpair as a member, will list as a list of lists. (`mg_dbid t_relatePropDelay`)
| type | string | "`PIN_PAIR`"
**Note:** For nets that are part of an xnet, the pinpair always has the xnet as the pinpair owner. For more information on the rpd attribute, see`axlMatchGroupCreate`.

****Table 2-37****
**NET\_GROUP Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| groupMembers | l\_dbid | members of the group (net\_groups, nets, xnets, diffpairs, buses)
| name | string | Name of group
| objType | string | "group"
| type | string | "NET\_GROUP"
| isInterfaceTop | t/nil | If`t`, group is the top of a definition-driven interface instance.
**Note:** Use`axlDBCreateGroup` family of commands to add, delete and modify these groups.

****Table 2-38****
**PORT\_GROUP Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| groupMembers | l\_dbid | members of the group (port\_groups, pins, function pins)
| name | string | Name of group
| objType | string | "group"
| type | string | "PORT\_GROUP"
| isInterfaceTop | t/nil | If`t`, group is the top of a definition-driven interface instance.
**Note:** PORT\_GROUPs are groupings of Allegro pin objects.

****Table 2-39****
**RATSNEST Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| bus | t/nil | Currently being shown with bus routes option
| objType | string | Type of object, in this case "ratsnest"
| pinsConnected | t/nil | Ratsnest not displayed (both pins on same branch)
| pins | l\_dbid | The two pins (or ratTs) that the rats connect
| pwrAndGnd | t/nil | Net is power and ground scheduled
| ratnest | t/nil | Two dbids of the next ratsnest for dbid's of the pins attribute.
| ratsPlaced | t/nil | User defined rats only, one or more pins unplaced
| userDefined | t/nil | Ratsnest is user defined
****Table 2-40****
**XNET Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| bus | dbid | Bus dbid if part of a bus.
| diffpair | dbid | differential pair dbid if part of a differential pair.
| groupMembers | l\_dbid | List of nets of the xnet.
| name | string | Name of the xnet.
| objType | string | "`group`"
| pinpair | l\_dbid | List of pinpairs associated with xnet.
| rpd | l\_rpd | For each match group that has this xnet as a member, lists as a list of lists (`mg_dbid t_relatePropDelay`).
| type | string | "`XNET`".
**Note:** 1) This attribute can only be defined indirectly from the SigNoise model assignment.
           2) For more information on rpd, see`axlMatchGroupCreate`.

Property Dictionary Database Types
----------------------------------

The following section contains tables listing the attributes of Allegro PCB Editor property dictionary objects. You must enter a dictionary object with a particular name in the property dictionary before you attach properties by that name to Allegro PCB Editor objects.

#### Object Types Allowing Attachment of Properties

You can attach properties to the database object types listed here. Each property type has a list of the objects types to which it can be attached. Attempting to attach a non-qualified property to an object returns`nil`.

|  |  |  |
| --- | --- | --- | ---
| `NETS` | `COMPONENTS` | `FUNCTIONS` | `PINS`
| `VIAS` | `SHAPES` | `SYMBOLS` | `CLINES`
| `LINES` | `DRCS` | `FIGURES` | `DESIGNS`
| `COMPDEFS` | `PINDEFS` | `FUNCDEFS` |
#### Allowed Property Data Types

An Allegro PCB Editor property value can be one of the data types listed. The right column shows the checks you can optionally apply to user input for that data type. Pre-defined properties have pre-defined range checks. You define your own range checks for user-defined properties.

**Note:** The right column includes default units for that property data type, however, you can set the units of these standard data types in the`<``tools``>/text/units.dat`file.

|  |
| --- | ---
| **Data Type** | **Data Check Available  (default units)**
| STRING | N/A
| INTEGER | range and units
| REAL | range and units
| DESIGN\_UNITS | range (units of current design)
| BOOLEAN | N/A
| ALTITUDE | range (meters)
| CAPACITANCE | range (pF)
| DISTANCE | range (cm)
| ELEC\_CONDUCTIVITY | range (mho/cm)
| LAYER\_THICKNESS | range (mil)
| IMPEDANCE | range (ohm)
| INDUCTANCE | range (nH)
| PROP\_DELAY | range (nS)
| RESISTANCE | range (ohm)
| TEMPERATURE | range (degC)
| THERM\_CONDUCTANCE | range (w/cm-degC)
| THERM\_CONDUCTIVITY | range (w/cm-degC)
| VOLTAGE | range (mV)
| VELOCITY | range (m/sec)
****Table 2-41****
**Property Dictionary Attributes**

| **Attribute Name** | **Type** | **Description**
| Also includes generic object attributes | |
| dataType | string | Data type for property value (see[Allowed Property Data Types](#453837 "2"))
| name | string | Name of property
| objType | string | Type of object, in this case`"propDict"`
| range | lf\_range | Optional limits for value
| units | string | Optional value units
| useCount | integer | Number of objects using property
| write | t/nil | `t` = writable or user defined `nil` = read-only or Allegro PCB Editor pre-defined
Parameter Database Types
------------------------

The following Allegro PCB Editor parameter types, which are critical to the function of interactive commands, are modeled:

* `drawing`

* `layer`

* `text block`

* `display`

Only drawing parameters support attached properties.

You can access and change parameters with`axlParamGetByName` and `axlSetParam`,respectively. See [Chapter 3, "Parameter Management Functions"](04parmgt.html#1069532 "3") for functions that provide easier access to layers and other parameter objects.

Unlike other Allegro PCB Editor objects these attributes contain a column,`Set?`, that shows whether you can modify this field via the `axlSetParam` function.

****Table 2-42****
**Artwork Parameter Attributes**

| **Attribute Name** | **Type** | **Description**
| Includes no generic object attributes | |
| groupMembers | l\_string | List of film names
| nChildren | number | Number of films
| objType | string | Type of object, in this case`"artwork"`
****Table 2-43****
**Artwork Film Parameter Attributes**

| **Attribute Name** | **Type** | **Description**
| Includes no generic object attributes | |
| domains | l\_string | List of domains where film is visible.  Supported values are`ipc2581`, `pdf`, `artwork`, and `visibility`.
| drawHolesOnly | t/nil | For pins and vias draw only the holes.
| drawMissingPadApertures | t/nil | Specifies the apertures you can use to draw (fillin) the shape of any pad for which there is no matching pad aperture in`art_aper.txt`. Not selecting this option means that you cannot draw such pads.
| fullContact | t/nil | Applies to negative film. When`t`, a pin or via that is connected to a shape uses no flash, causing a solid mass of copper to cover the pad. When you do not select this field, a pin or via connected to a shape uses a thermal-relief flash.
| groupMembers | l\_string | List of layers comprising film
| ipc2581 | l\_string | List of IPC2581 Layer mappings.  Indicates where film should be used in IPC25281 output. Supported values are inner, outer, misc, doc, and soldermask.
| mirrored | t/nil | Specifies whether to mirror the photoplot output.
| name | string | Name of film
| negative | t/nil | Is film positive (`nil`) or negative (`t`)
| objType | string | Type of object, in this case "`artwork`"
| offset | point | Specifies the x and y offset to add to each photoplot coordinate. If you enter positive x and y offsets, all photoplotted lines shift in the positive direction on the film.
| rotation | integer | Rotation of the plotted film image. Choices are:`0`, `90`, `180`, and `270` degrees.
| sequence | integer | Sequance number for PDF ordering.  Range is 0 to 255. If two films share the same number, the database ordering determines ties.
| shapeBoundingBox | float | Applies to negative film. Adds another outline around the design outline, extending the shape boundary of the filled area. This new artwork outline extends, by default, 100 mils in all directions beyond the design outline.
| suppressShapeFill | t/nil | Area outside the shapes is not filled on a negative film. You must replace the filled areas with separation lines before running artwork.
| suppressUnconnectPads | t/nil | Specifies that the pads of pins and vias with no connection to a connect line in a gerber data file are not plotted. This option applies only to internal layers and to pins whose padstack flags the pads as optional.  Selecting this button also suppresses donut antipads in raster based negative artwork.
| undefineLineWidth | float | Determines the width of any line that is 0.
| useApertureRotation | t/nil | Specifies whether or not to use the aperture rotation raster. Artwork uses gerber behavior to determine which type of pad to flash.
| vectorBasedPad | string | Extracts information about vector based pad behavior from the artwork control dialog box.
****Table 2-44****
**Design Parameter Attributes**

| **Attribute Name** | **Set?** | **Type** | **Description**
| Includes generic object attributes | | |
| accuracy | no | integer | Number of decimal places of accuracy
| bBox | no | bbox | The design's bounding box
| height | no | float | Height in user units
| objType | no | string | Type of object, in this case`"paramDesign"`
| units | no | string | Type of user units (`mils`, `inch`, `micron`, `millimeter` and `centimeter`)
| width | no | float | Width in user units
| xy | no | point | Lower left corner of design
**Notes:**

* To avoid harmful side effects, such as rounding errors, do not toggle between English and metric.

* Changes to accuracy are very time consuming since all objects in the design must be changed.

  Setting drawing accuracy to a value greater than Allegro PCB Editor supports is an error. Typical range is 0 to 4.

* Change units and accuracy at the same time to avoid loss of accuracy.

* The size (width and height) may not be decreased where it will leave some objects outside of the drawing extents.

****Table 2-45****
**Display Parameter Attributes**

| **Attribute Name** | **Set?** | **Type** | **Description**
| Includes no generic object attributes | | |
| activeLayer | yes | string | Active layer name
| altLayer | yes | string | Alternative layer name which must be of group`"etch"`
| objType | no | string | Type of object, in this case`"paramDisplay"`
****Table 2-46****
**ECset Parameter Attributes**

| **Attribute Name** | **Set?** | **Type** | **Description**
| Includes generic object attributes | | |
| locked |  | t/nil | Cset locked from UI based editing
| members |  | l\_dbid | List of electrical constraints in set
| name |  | string | Name of ECset
| objType |  | string | Type of object, in this case`"ecset"`
| prop |  | l\_dbid | List of user defined properties on ECset
| readOnly |  | t/nil | Cannot be modified, always`t`
| topology |  | t/nil | This is derived from a topology file, and may contain constraints that have restrictions on how they can be modified.
| prop |  | l\_dbid | List of user-defined properties on an ECset.
****Figure 2-2****
**Allegro PCB Editor Class/Subclass to AXL Layer Model**

****Table 2-47****
**Layer Group Parameter Attributes (Allegro Classes)**

| **Attribute Name** | **Set?** | **Type** | **Description**
| Includes no generic object attributes | | |
| color | yes | integer | Layer color index; -1 if all child layers are not the same color
| groupMember | no | l\_string | List of subclasses belonging to this class
| isEtch | no | t/nil | Is an etch layer
| name |  | string | Name of this class
| nChildren | no | integer | Number of subclasses in class
| objType | no | string | Type of object, in this case`"paramLayerGroup"`
| pattern | yes | integer | Pattern for layer; -1 if all child layers not the same pattern (see[Layer Parameter Attributes (Allegro Subclasses)](#621110 "2") [table](#621110 "2")  )
| visible | yes | t/nil | All subclasses of this class are visible
****Table 2-48****
**Layer Parameter Attributes (Allegro Subclasses)**

| **Attribute Name** | **Set?** | **Type** | **Description**
| Includes no generic object attributes | | |
| color | yes | integer | Subclass color number
| drcPhotoType | no | string | `"Positive"` or `"negative"` (applies only to etch)
| isEtch | no | t/nil | Is an etch layer
| material | NO | string | Layer material (etch only)
| name | no | string | Name of this subclass
| number | no | integer | Layer number, while this is reported for both etch and non-etch layers it is only meaningful for etch layers where it shows the stackup order.
| nextLayer | no | string | Name of next layer in stackup (etch only)
| objType | no | string | Type of object, in this case`"paramLayer"`
| parentname | no | string | Name of owning class
| pattern | yes | integer | Pattern of layer where 0 is default solid pattern. For maximum patterns, see[axlColorGet](04parmgt.html#1093245 "3")('pattern). Pattern style for each pattern number can be found in the color192 dialog.
| thickness | no | string | Layer thickness (etch only)
| type | no | string | "Postive" or Negative (etch only)
| userDefined | No | t/nil | Is layer user defined. User defined layers could have been added by the user.  Note for etch layers -- all are user-defined, but you typically cannot delete or rename the TOP or BOTTOM.
| visible | yes | t/nil | All subclasses of this class are visible
**Note:** The Allegro PCB Editor class/subclass system is modeled in AXL as layers. The previous drawing figure shows how AXL layers are mapped to Allegro PCB Editor class/subclasses. The define etch form in Allegro PCB Editor does not match this model. AXL does not support access to the dielectric pseudo-layers nor does it support analysis layer attributes such as material and thickness. To access these records, use Allegro PCB Editor's technology file feature.

****Table 2-49****
**Textblock Group Parameter Attributes**

| **Attribute Name** | **Set?** | **Type** | **Description**
| Includes no generic object attributes | | |
| groupMembers | no | l\_string | Names of members in this group
| nChildren | no | integer | Number of children
| objType | no | string | Type of object, in this case`"paramTextGroup"`
****Table 2-50****
**Textblock Parameter Attributes**

| **Attribute Name** | **Set?** | **Type** | **Description**
| Includes no generic object attributes | | |
| charSpace | Yes | float | Spacing between characters in design units
| height | Yes | float | Character height in design units (includes descender)
| lineSpace | Yes | float | character line to line space in design units
| name | no | string | Character block number
| objType | no | string | Type of object, in this case`"paramTextBlock"`
| photoWidth | Yes | float | character line width in design units
| width | Yes | float | character width in design units
****Table 2-51****
**Testprep Parameter Attributes**

| **Attribute Name** | **Set?** | **Type** | **Description**
| Includes no generic object attributes | | |
| allowUnderComp | yes | t/nil | Allows test pads under components.
| autoInsert | yes | t/nil | Allows automatic generation of test points as needed.
| bareBoard | yes | t/nil | If`nil`, you can only test component pins on non-component design side. If `t`, then you can check pins on either side of the design, as long as padstack is defined on that side.
| directTest | yes | t/nil | Allows pins to be selected as test point.
| executeInc | yes | t/nil | If`t`, returns in incremental mode where you can analyze only nets without test points. If `nil`, removes all test points at beginning of run.
| layer | yes | symbol | Layer for test:`top`, `bottom` or `either`.
| maxTestDisplacement | yes | float | Maximum distance from pin or via where you can place the test point.
| minPadSize | yes | float | Minimum padstack size. Works with replaceVias to upscale padstacks.
| minTestDisplacement | yes | float | Minimum distance from pin or via where you can place a test point. A value of 0 indicates DRC distance you should use.
| minTestSpacing | yes | float | Minimum spacing between test points.
| objectType | no | string | Type of object, in this case`"testprep"`
| pinType | yes | symbol | Type of pin selectable for testing:`input`, `output`, `pin`, `via`, or `point`.
| replaceVias | yes | t/nil | If`t`, replaces vias that are too small with a larger via.
| testGridX | yes | float | Testprep grid.
| testGridY | yes | float | Testprep grid.
| testMethod | yes | symbol | Method used for test:`single`, `node`, or `flood`.
| testPad | yes | nil/string | Padstack that you use for test pads on the probe side of the design. Must meet criteria specified in the`testPadType` attribute. If relative name is given, uses database then `PSMPATH` to find pad.
| testPadDB | no | dbid | `dbid` of the testPad
| testPadType | yes | symbol | Type of padstacks for probes:`smd`, `through`, or `either`.
| testVia | yes | nil/string | Padstack that you use for testpads on the probe side of the design. Must be through hole. If relative name is given, uses database then`PSMPATH` to find pad.
| testViaDB | no | dbid | `dbid` of testVia.
| unusedPins | yes | t/nil | Allows test points on pins, not on a net.
| The following are Text Controls | | |
| alpha | yes | t/nil | If`t`, use Alphabetic extension, `nil` use numeric extension.
| displayText | yes | t/nil | Displays text for each test point.
| textOffsetX | yes | float | X offset of text from pad center.
| textOffsetY | yes | float | Y offset of text from pad center.
| textRotation | yes | integer | Rotation of text labels: values are`0`, `90`, `180`, or `270` degrees. Other values are moduled and truncated.
**Note:** Specifying testVia or testPad loads them into the current database if they are not already loaded. Changing to another padstack does not delete the old padstack from the database.

#### Example

> `p = axlGetParam("testprep")`

> `p->displayText = t`

> `p->testMethod = 'flood`

> `axlSetParam(p)`

Turns on text display and sets test method to flood.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
