### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

21
==

Polygon Operation Functions
===========================

This chapter describes the AXL/SKILL Polygon Operation functions and includes the following sections:

* About Polygon Operations

* AXL-SKILL Polygon Operation Attributes

* AXL-SKILL Polygon Operation Functions

* Use Models

About Polygon Operations
------------------------

A*poly* is a set of points linked so that the start and end point are the same. A poly is always non-intersecting and may contain *holes*. A hole is a non-intersecting closed loop enclosed within a poly.

****Figure 21-1****
**Poly with Holes**

**Note:** These polys refer to the`o_polygon` object in AXL-SKILL. Polys are different from the AXL Skill Database *polygon* object which represents an Allegro PCB Editor unfilled shape.

These functions, which perform geometric operations on polys, are called logical operations and do the following:

* Create route keepouts based on the board outline, offset by a pre-determined distance.

* Create split planes from route-keepin and Anti-etch.

* Automatically generate a package keepout surrounding a package and its pins, contoured around the package.

Logical operations in AXL-SKILL enable SKILL programmers to do the following:

* Create logical operation objects (`lo_polygon`) from these Allegro PCB Editor database objects:

* pins

* lines

* clines

* vias

* shapes

* rectangles

* frectangles (filled rectangles)

* voids

* Create`o_polygon` from holes in a poly (`o_polygon`)

* Create an Allegro PCB Editor database shape from an`o_polygon`

* Perform geometric operations on`lo_polygons`, resulting in the creation of other `lo_polygons`.

* Logical AND - The intersection of two polys.

* Logical OR - The union of two polys.

* Logical ANDNOT - Subtracting one poly from another.

* Logical EXPAND (CONTRACT is expand in the opposite direction.)

* Perform query operations on a`o_polygon`, including the following:

* The area of the poly

* The bounding box around the poly

* The holes and vertices of a poly

* If the`o_polygon` is a hole

* Access path data and holes from an`o_polygon`

* Locate a point respective to the poly

#### Error Handling

Return values for each function are specified along with the description of the function, in case of error.

AXL-SKILL Polygon Operation Attributes
--------------------------------------

The following are the attributes of the`o_polygon` type:

|  |  |
| --- | --- | ---
| **Attribute Name** | **Type** | **Description**
| `area` | float | Area of the poly in the same units as the drawing.
| `bBox` | bBox | Poly's bounding box.
| `vertices` | list | Path-like data of the outer boundary of the poly available as a list of lists where each of the sublists will contain a point representing a vertex of the poly and a floating point number representing radius of the edge from the previous vertex to the present vertex.  No arcs spanning across quadrants or greater than 90 degrees.  Radius of 0.0 indicates a straight line edge between the two vertices.  Positive radius value indicates that the arc lines to the left of the center and negative radius imply that the arc lies to the right of the center of the arc.
| `holes` | list | `lo_polygon`
| `isHole` | boolean | `t` = hole, `nil` = poly
The following figures illustrate the attributes described.

* Attributes

`vertices    (((9775.0 775.0)    0.0)`

`((9100.0 1075.0)    0.0)`

`((8350.0 950.0)    0.0))`

`holes    (poly:20199696 poly:20199896`

`poly:22204476)`

`isHole nil`

**Note:** All the 3 polys representing holes of the above poly have their isHole attribute set to`t`.

* Attributes

`vertices    (((5975.0 976.0)       0.0)`

`((5787.0 788.0)     188.0)`

`((7225.0 599.0)       0.0)`

`((7413.0 787.0)    -188.0)`

`((7225.0 975.0    -188.0))`

`holes nil`

`isHole nil`

AXL-SKILL Polygon Operation Functions
-------------------------------------

This section lists the polygon operation functions.

### axlPolyFromDB

```
axlPolyFromDB(o_dbid/r_path?endCapType    s_endCapType?layer    t_layer?padType     s_padType?holes      t/nil?line2poly  t/nil)?xhatch t/nil)⇒ lo_polygon/nil
```

#### Description

Creates a list of`o_polygon` objects from the `dbid`or an `r_path`. Use the `lo_polygon` list to get the poly attributes or to perform logical operations on these polys. In the case of r\_path option, we expect a path that reflects a closed shape with no intersections. It is important that the first and last point be the same. The width option of `r_path` is ignored as well as the '?' arguments to `axlPolyFromDB.`

***Polygon Attributes***

|  |
| --- | ---
| area | (float) Area of polygon in design units. If a hole this is negative. If a polygon is not a hole then the area is the sum of the base poly area minus any of its holes.
| bBox | (bBox) bounding box of polygon
| holes | (list of o\_polys/nil) list of any holes in poly
| isHole | (t/nil) is this a hole (void) or a shape
| objType | (t\_string) "polygon"
| vertices | (list of coords). This always describes a closed shape.
|  | Format for each coord is:  `(xy f_radius)`
|  | Where  `xy` - vertice point in design units  `f_radius` - 0 if previous point and this point forms a segment else points form a arc with radius. The sign of the radius indicates for positive the arc is to the left of the y-axis and a negative indicates arc is the right.
|  | If arcs are present a polygon typically may contain more segments then the underlying shape dbid. This is due to the polygon arcs cannot cross a quadrant so are broken along quadrant boundaries.
NOTES

* A polygon is NOT a dbid.

* Comparing two polys using Skill functions:

|  |  |
| --- | --- | ---
|  |  | equal function: geometrically compares that two polys are the same thus slightly slower then the eq function.
|  |  |
| --- | --- | ---
|  |  | eq function compares that the poly ids are the same.
This is different from the dbid comparison where both the`equal` and `eq` return the same results.

What this means from a programming standpoint, is that if you have two identical shapes in Allegro PCB Editor, the '`equal`' comparison on the shape dbids returns that they are NOT equal but converting these shapes to polys via `axlPolyFromDB` and doing a 'equal' of the resulting polygons will return '`t`' while the 'eq' comparison will return 'nil'.

#### Arguments

|  |
| --- | ---
| `o_dbid` | axl`dbid` for one of the following: path (line and cline), shape, rect, frect, pin, via, void, arc and line from which to construct the poly. **Note**: Arc and line are segments reported by `show element.`
| `r_path` | Path construct from the`axlPath` API family. This is not an Allegro PCB Editor database object and is a much more efficient method for creating an Allegro PCB Editor shape, than converting it to a Poly. Note `axlDBCreateOpenShape` also supports an `r_path`. For more details, see ***Description***.ZSee `line2poly`. `r_path` must describe a closed non-intersecting shape unless the line2poly is `t` (see below).
| `s_endCapType` | Keyword string specifying the end cap type to use for the polygon, one of`'SQUARE`, `'OCTAGON`, or `'ROUND`. Used in case of line or cline only, otherwise ignored. Default is `'SQUARE`.
| `t_layer` | Keyword string specifying the layer of the pad to retrieve, for example,`"ETCH/TOP"`. Used in the case of pin or via only, otherwise ignored. Default is `"ETCH/TOP"`.
| `s_padType` | Keyword string specifying the type of the pad to be retrieved, one of`'REGULAR`, `'ANTI`, or `'THERMAL`. Used for pins, vias, or if `r_path` is based with the `line2poly` option, otherwise ignored. Default is `'REGULAR`.
| `holes` | Default value is`t`. By default, for shapes with voids returns any voids as holes. If the value is set to `nil`, does not return the holes.
| `line2poly` | Applicable only if first argument is an`r_path`. By default, an `r_path` describes a closed path. When this option is `t`, the `r_path` itself is converted to a poly in a manner similar to line dbids. It is strongly recommended that the `r_path` has width otherwise the artwork undefined line width is used.Typically one poly is returned for each segment in the `r_path`.
| `xhatch` | If t and the dbid is a cross-hatch shape returns a poly of the cross-hatching. By default, cross-hatch shapes are treated as solid shapes with respect to poly generation. For complex shapes (>500 edges; this includes both outline and voids) generateing a poly of the cross-hatching can take a considerable amount of time and memory.If this option is`t`, the holes option for cross-hatch shapes is assumed to be `t`.
#### Value Returned

|  |
| --- | ---
| `lo_polygon` | Object representing the resulting geometry.
| `nil` | Cannot get polys.
#### See Also

Other APIs that support or generate polygons:

* [axlPolyOperation](#1077319 "21") - performs various logical operations on 2 lists of polygon

* [axlPolyExpand](#1076223 "21") - expands or contracts polygon

* [axlIsPolyType](#1076291 "21") - is object a polygon object

* [axlPolyErrorGet](#1076347 "21") - return last error from axlPolyOperation

* [axlPolyFromDB](#1076123 "21") - convert an allegro dbid to a polygon

* [axlPolyMemUse](#1077325 "21") - debug function to return memory use of polygon sub-system

* [axlPolyOffset](#1077718 "21") - move a polygon

* [axlPolyFromHole](#1076322 "21") - converts a hole polygon to a positive polygon

* [axlDBCreateShape](03dbcre8.html#367593 "15") - create a shape

See documentation for individual use.

#### Examples

* Create a poly from a via

> `polyList = axlPolyFromDB(via_dbid, ?layer "ETCH/BOTTOM" ?padType 'ANTI)`

* Create a rectangle poly (one corner at 0,0 with a width 1000 and height of 500) using`r_path` method

> `; note first and last points are the same`

> `myPath = axlPathStart( list(0:0 1000:0 1000:500 0:500 0:0) 0)`

> `pathPoly = axlPolyFromDB(myPath )`

> `poly = car(pathPoly)`

> `poly->??`

### axlPolyMemUse

`axlPolyMemUse () -> lx_polyCounts`

#### Description

This returns a list of integers reflecting the internal memory use of the`axlPoly` interfaces.
If you assign Poly objects to global handles (instead of assigning to locals, e.g `let` or `prog` statements) then you need to insure all of global data is `nil`-ed at the end of your program. The example below shows how to check that you have written your program correctly.

Description of 5 integers. Integers 2 through 5 are for Cadence use.

1 - Most important and shows number of Skill Polys still in use.

2 - Number of Allegro Polys in use. This is always >= to Skill Polys. The additional polys are voids (holes) in the Skill polys.

3 - Number of edges in all Allegro polys.

4 - Number of Allegro Floating Point Polys (should be 0).

5 - Number of edges in all Allegro Floating Point Polys (should be 0).

#### Arguments

None

#### Value Returned

`lx_polyCounts` A list of 5 integers reflecting Poly memory usage.

#### See Also

[axlPolyOperation](#1077319 "21")

#### Example

Verify at end of your program you have no hanging Poly memory in use.

`gc() ; requires Skill development licenses`

`axlPolyMemUse()`

`;; should return all 0's`

### axlPolyOffset

`axlPolyOffset (o_polygon/lo_polygonl_xy[g_copy])=> o_polygon`

#### Description

This offsets the entire poly by the provided xy coordinate. Optionally if`g_copy` is `t`it will copy the poly, default is to offset the provided poly.

**Note:** The offseted polygon must be entirely within the extents of the drawing.

#### Arguments

`o_polygon` `o_polygon` on which the operation is to be done.

`lo_polygon` Optionally pass a list of polys.

`l_xy` Coordinates in user units for offset.

`g_copy` Optional, if `t` does the offset on a copy.

#### Value Returned

`lo_polygon/`

`o_polygon` In place offset (`g_copy nil`) or offseted copy of polygon
 (`g_copy` is `t`). If passed a list of polys returns a list otherwise
 return a poly.

#### See Also

[axlPolyFromDB](#1076123 "21")

#### Example

See the following.

`<cdsroot>/share/pcb/examples/skill/axlcore/ashpoly.il`

### axlPolyOperation

```
axlPolyOperationo_polygon1 / lo_polygon1o_polygon2 / lo_polygon2s_operation)⇒ lo_polygon/nil
```

#### Description

Performs the logical operation specified on the two sets of polygons. Does not allow hole polygons as input. When holes are passed as input, the following warning is displayed:

> `Invalid polygon id argument -<argument>`

* ***-- This function is provided "as-is". Result, in certain cases, may fail or deliver incorrect results. No commitment can be made to address issues uncovered when using this API.

  -- Underlying polygon operation function fails and returns`nil` in rare dense geometrical situations.

  -- This API may consume a large amount of memory and take a considerable of amount of time to return a result. This is normally only noticeable when the number of polygons provided exceed 10000. The number polygons can be calculated by taking the length of the polygons provided to args 1 and 2 PLUS adding all of the polys holes (poly->holes) in the polygons.

  -- Algorithm has lines take have a width 1 or 0 database units. This means if you have a design with 2 units of accuracy, 1 database unit is .01.***

#### Arguments

|  |
| --- | ---
| `o_polygon1` / `lo_polygon1` | `o_polygon` or list of `o_polygons` on which the operation is to be done.
| `o_polygon2` / `lo_polygon2` | `o_polygon` or the list of `o_polygons` on which the operation is to be done.
| `s_operation` | String specifying the type of logical operation, one of`'AND`, `` `OR ``, or `` `ANDNOT ``.
#### Value Returned

|  |
| --- | ---
| `lo_polygon` | List of`o_polygons` which represent the resulting geometry from performing the operation on the arguments.
| `nil` | Error due to incorrect arguments.
For example:

(`o_polygon_out1` `o_polygon_out2` ...) is returned if the result after performing the operation is a list of polygons.

`nil` is returned if the result after performing the operation is a `nil` polygon. For example, consider performing the `AND` operation on two non-overlapping sets of polys.

`nil` is returned if the operation fails. You can obtain a descriptive error message by calling [axlPolyErrorGet](#1076347 "21").

#### Example

> `poly1_list = (axlPolyFromDB cline dbid)`

> `poly2_list = (axlPolyFromDB shape_dbid)`

> `res_list = (axlPolyOperation poly1_list poly2_list 'OR)`

### axlPolyExpand

`axlPolyExpand(o_polygon1 / lo_polygon1f_expandValues_expandType)⇒ lo_polygon/nil`

#### Description

This function yields a list of polys after expanding them by a specified distance. Use of a negative number causes contraction. Distance is specified in user units. This function does not allow hole polys as input. When holes are passed as input, the following warning is displayed:

> `Invalid polygon id argument -<argument>`

* ***Underlying logical operation function fails and returns`nil` in rare dense geometrical situations. 'ALL\_ARC mode may have round-off issues when shape has very small arc segments.***

Trimming options are (`s_expandType`):

* no corner modifications
* Trim inside acute (less then 90 degrees) line/line corners with arcs and always chamfer spikes. No obtuse or right angle trimming is done.
* Trim acute inside corners and spikes with line segments.
* 90 degree corners are trimmed.
* All acute angles are trimmed.
* Most obtuse angles (more then 135 degrees) are trimmed.

**Note:** Poly expansion with 0 and no trim is returns the input poly NOT a list`axlPolyExpand(poly 0.0 'NONE) -> o_polygon`.

#### Arguments

`o_polygon1` /`lo_polygon1`

`o_polygon`   /  list of `o_polygons` on which the operation is to be done.

|  |
| --- | ---
| `f_expandValue` | Amount of expansion in user units.
| `s_expandType` | Symbol specifying the exterior corners of the geometry during expansion, (see above)
#### Value Returned

|  |
| --- | ---
| `lo_polygon` | List of`o_polygons` which represent the resulting geometry after performing the expansion on the polys passed as arguments.
| `nil` | Failed to expand polys due to incorrect arguments.
To be more specific:

* (`o_polygon_out1` `o_polygon_out2` ...) is returned if the result after performing the operation is a list of polys.

* `nil` is returned if the result after performing the operation is a `nil` poly, for example, consider contracting a 20x30 rectangle by 40 units.

* `nil` is returned if the operation fails. You can get a descriptive error message by calling `axlPolyErrorGet()`.

#### Example

> `poly_list = (axlPolyFromDB shape_dbid)`

> `exp_poly = (axlPolyExpand poly_list 10.0 'ALL_ARC)`

The following sequence of diagrams illustrates the behavior of each of the options.

****Figure 21-2****
**Original Poly**

**ALL\_ARC**

During expansion of the poly boundary, an arc is inserted for the edges in the offset shape that satisfy the following criteria:

* Edges form an*outside* (or convex) point of the poly boundary.
  The reverse is true for the voids.

****Figure 21-3****
**Expanded Using ALL\_ARC**

**ACU\_ARC**

During expansion of the poly boundary, an arc is inserted for the edges in the offset shape that satisfy the following criteria:

* Edges form an*outside* (or convex) point of the poly boundary.

* Edges form an angle sharper than 90 degree.
  The reverse is true for the voids.

****Figure 21-4****
**Expanded Using ACU\_ARC**

**ACU\_BLUNT**

During expansion of the poly boundary, a blunt edge is inserted for the edges in the offset shape that satisfy the following criteria:

* Edges form an*outside* (or convex) point of the poly boundary.

* Edges form an angle sharper than 90 degree.
  The reverse is true for the voids.

****Figure 21-5****
**Expanded Using ACU\_BLUNT**

### axlIsPolyType

`axlIsPolyType (g_polygon)⇒ t/nil`

#### Description

Tests if argument`g_polygon` is a polygon user type.

#### Arguments

|  |
| --- | ---
| `g_polygon` | Object to test, any skill variable
#### Value Returned

|  |
| --- | ---
| `t` | `g_polygon` is a polygon user type.
| `nil` | `g_polygon` is not a polygon user type.
#### See Also

[axlPolyFromDB](#1076123 "21")

#### Example

> `poly = axlPolyFromDB(cline_dbid)`

> `axlIsPolyType(poly) returns t.`

> `axlIsPolyType(cline_dbid) returns nil.`

### axlPolyFromHole

`axlPolyFromHole (o_polygon)⇒ lo_polygon/nil`

#### Description

Creates a new poly from the vertices of the hole, and sets the`isHole` attribute of the resulting poly to `nil`. Function returns `nil` in case of error.

#### Arguments

|  |
| --- | ---
| `o_polygon` | `o_polygon` on which the operation is to be done. Must have `isHole` attribute set to `t` (that is, the argument must be a hole).
#### Value Returned

|  |
| --- | ---
| `lo_polygon` | List of`o_polygons` which represent the resulting geometry after creating poly from the hole argument.
| `nil` | Error due to incorrect argument.
#### Example

> `poly = axlPolyFromDB(shape_dbid)`

> `hole = car(poly->holes)`

> `polyList = axlPolyFromHole(hole)`

### axlPolyErrorGet

`axlPolyErrorGet ()⇒ t_error/nil`

#### Description

Retrieves the error from the logop core. See the following list of error strings returned by the logical operation core:

|  |
| --- | ---
| **Error type** | **String returned**
| problem with arcs | "`Bad arc data in polygon operations.`"
| bad data | "`Data problem inside polygon operations.`"
| internal error in logical op data handling | "`Polygon operation failed because of internal error.`"
| numerical problem in logical op | "`Computational problem while doing polygon operations.`"
| memory problem | "`Out of memory.`"
| no error | `NIL`
#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t_error` | Error from the logical operation core.
| `nil` | No logical operation error.
#### Example

> `l_poly1 = axlPolyFromDB(shape_dbid)`

> `l_poly2 = axlPolyFromDB(cline_dbid ?endCapType 'SQUARE)`

> `l_polyresult = axlPolyOperation(l_poly1 l_poly2 'ANDNOT)`

> `if (null l_polyresult) axlMsgPut(list axlPolyErrorGet())`

Use Models
----------

#### Example 1

The existing Split Plane functionality can use the AXL version of the logical operation.

The objective is to split the route-keepin shape on the basis of the anti-etch information and add the resulting split-shapes to the database.

**Split Plane Usage**

> `; retrieve the route keepin rectangle`

> `startShape = (myGetRouteKeepin)`

> `; retrieve the shapes and lines on the anti-etch subclass`

> `antiEtchGeom = (myGetAntiEtchGeom (axlGetActiveLayer))`

> `; create the polygon for the route-keepin rectangle`

> `startPoly = (axlPolyFromDB startShape)`

> `; create the polygon for all the anti-etch elements`

> `antiEtchPoly = nil`

> `(foreach antiElem antiEtchGeom`

> `antiElmPoly = (axlPolyFromDB antiElem ?endCapType 'ALL_ARC)`

> `antiEtchPoly = (append antiElmPoly antiEtchPoly)`

> `)`

> `; do the LogicalOp operation`

> `splitPolyList = (axlPolyOperation startPoly antiEtchPoly 'ANDNOT)`

> `;check for any error in logop`

> `(if splitPolyList then`

> `(; add the resultant polygons as a set of filled shapes on the`

> `; active class/subclass with no net name.`

> `(foreach resPoly splitPolyList`

> `(axlDBCreateShape resPoly t)`

> `))`

> `else`

> `(axlMsgPut(list axlPolyErrorGet()))`

> `)`

#### **Example 2**

> `; retrieve the polygon corresponding to clock gen`

> `clockPoly = (axlPolyFromDB rect_id)`

> `; get polygon associated with the ground shape`

> `gndPoly = (axlPolyFromDB shp_dbid)`

> `; get the intersection of the two polygons`

> `shieldedPoly = (axlPolyOperation clockPoly gndPoly 'AND)`

> `; check for any error in logop`

> `(if shieldedPoly then`

> `(; get the area of the intersection polygon`

> `shieldedArea = shieldedPoly->area`

> `; get the area associated with clock gen`

> `clockArea = clockPoly->area`

> `;get the ratio of the two areas`

> `ratioArea = shieldedArea / clockArea)`

> `else`

> `(axlMsgPut(list axlPolyErrorGet()))`

> `)`

Gets the shielded area of a clock generator by a ground shape using the rule stating that the ratio of the shielded area to the actual area should be less than a particular threshold.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
