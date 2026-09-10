### axlPolyFromDB

`axlPolyFromDB( o_dbid/r_path ?endCapType s_endCapType ?layer t_layer ?padType s_padType ?holes t/nil ?line2poly t/nil ?xhatch t/nil ) => lo_polygon/nil`

#### Description

Creates a list of `o_polygon` objects from the `dbid`or an `r_path`. Use the `lo_polygon` list to get the poly attributes or to perform logical operations on these polys. In the case of r_path option, we expect a path that reflects a closed shape with no intersections. It is important that the first and last point be the same. The width option of `r_path` is ignored as well as the '?' arguments to `axlPolyFromDB.`

Polygon Attributes

| Name | Description |
|---|---|
| area | (float) Area of polygon in design units. If a hole this is negative. If a polygon is not a hole then the area is the sum of the base poly area minus any of its holes. |
| bBox | (bBox) bounding box of polygon |
| holes | (list of o_polys/nil) list of any holes in poly |
| isHole | (t/nil) is this a hole (void) or a shape |
| objType | (t_string) "polygon" |
| vertices | (list of coords). This always describes a closed shape.<br><br>Format for each coord is: `(xy f_radius)`<br><br>Where `xy` - vertice point in design units `f_radius` - 0 if previous point and this point forms a segment else points form a arc with radius. The sign of the radius indicates for positive the arc is to the left of the y-axis and a negative indicates arc is the right.<br><br>If arcs are present a polygon typically may contain more segments then the underlying shape dbid. This is due to the polygon arcs cannot cross a quadrant so are broken along quadrant boundaries. |

NOTES

- A polygon is NOT a dbid.

- Comparing two polys using Skill functions:

- equal function: geometrically compares that two polys are the same thus slightly slower then the eq function.

- eq function compares that the poly ids are the same.

This is different from the dbid comparison where both the `equal` and `eq` return the same results.

What this means from a programming standpoint, is that if you have two identical shapes in Allegro PCB Editor, the '`equal`' comparison on the shape dbids returns that they are NOT equal but converting these shapes to polys via `axlPolyFromDB` and doing a 'equal' of the resulting polygons will return '`t`' while the 'eq' comparison will return 'nil'.

#### Arguments

| Name | Description |
|---|---|
| `o_dbid` | axl `dbid` for one of the following: path (line and cline), shape, rect, frect, pin, via, void, arc and line from which to construct the poly. Note: Arc and line are segments reported by `show element.` |
| `r_path` | Path construct from the `axlPath` API family. This is not an Allegro PCB Editor database object and is a much more efficient method for creating an Allegro PCB Editor shape, than converting it to a Poly. Note `axlDBCreateOpenShape` also supports an `r_path`. For more details, see Description.ZSee `line2poly`. `r_path` must describe a closed non-intersecting shape unless the line2poly is `t` (see below). |
| `s_endCapType` | Keyword string specifying the end cap type to use for the polygon, one of `'SQUARE`, `'OCTAGON`, or `'ROUND`. Used in case of line or cline only, otherwise ignored. Default is `'SQUARE`. |
| `t_layer` | Keyword string specifying the layer of the pad to retrieve, for example, `"ETCH/TOP"`. Used in the case of pin or via only, otherwise ignored. Default is `"ETCH/TOP"`. |
| `s_padType` | Keyword string specifying the type of the pad to be retrieved, one of `'REGULAR`, `'ANTI`, or `'THERMAL`. Used for pins, vias, or if `r_path` is based with the `line2poly` option, otherwise ignored. Default is `'REGULAR`. |
| `holes` | Default value is `t`. By default, for shapes with voids returns any voids as holes. If the value is set to `nil`, does not return the holes. |
| `line2poly` | Applicable only if first argument is an `r_path`. By default, an `r_path` describes a closed path. When this option is `t`, the `r_path` itself is converted to a poly in a manner similar to line dbids. It is strongly recommended that the `r_path` has width otherwise the artwork undefined line width is used.Typically one poly is returned for each segment in the `r_path`. |
| `xhatch` | If t and the dbid is a cross-hatch shape returns a poly of the cross-hatching. By default, cross-hatch shapes are treated as solid shapes with respect to poly generation. For complex shapes (>500 edges; this includes both outline and voids) generateing a poly of the cross-hatching can take a considerable amount of time and memory.If this option is `t`, the holes option for cross-hatch shapes is assumed to be `t`. |

#### Value Returns

| Name | Description |
|---|---|
| `lo_polygon` | Object representing the resulting geometry. |
| `nil` | Cannot get polys. |

#### Examples

- Create a poly from a via

`polyList = axlPolyFromDB(via_dbid, ?layer "ETCH/BOTTOM" ?padType 'ANTI)`

- Create a rectangle poly (one corner at 0,0 with a width 1000 and height of 500) using `r_path` method

`; note first and last points are the same`

`myPath = axlPathStart( list(0:0 1000:0 1000:500 0:500 0:0) 0)`

`pathPoly = axlPolyFromDB(myPath )`

`poly = car(pathPoly)`

`poly->??`

#### See Also

Other APIs that support or generate polygons:

- axlPolyOperation - performs various logical operations on 2 lists of polygon

- axlPolyExpand - expands or contracts polygon

- axlIsPolyType - is object a polygon object

- axlPolyErrorGet - return last error from axlPolyOperation

- axlPolyFromDB - convert an allegro dbid to a polygon

- axlPolyMemUse - debug function to return memory use of polygon sub-system

- axlPolyOffset - move a polygon

- axlPolyFromHole - converts a hole polygon to a positive polygon

- axlDBCreateShape - create a shape

See documentation for individual use.

### axlPolyMemUse

`axlPolyMemUse ( ) => lx_polyCounts`

#### Description

This returns a list of integers reflecting the internal memory use of the `axlPoly` interfaces. If you assign Poly objects to global handles (instead of assigning to locals, e.g `let` or `prog` statements) then you need to insure all of global data is `nil`-ed at the end of your program. The example below shows how to check that you have written your program correctly.

Description of 5 integers. Integers 2 through 5 are for Cadence use.

1 - Most important and shows number of Skill Polys still in use.

2 - Number of Allegro Polys in use. This is always >= to Skill Polys. The additional polys are voids (holes) in the Skill polys.

3 - Number of edges in all Allegro polys.

4 - Number of Allegro Floating Point Polys (should be 0).

5 - Number of edges in all Allegro Floating Point Polys (should be 0).

#### Arguments

None

#### Value Returns

`lx_polyCounts` A list of 5 integers reflecting Poly memory usage.

#### Examples

Verify at end of your program you have no hanging Poly memory in use.

#### See Also

axlPolyOperation

### axlPolyOffset

`axlPolyOffset ( o_polygon/lo_polygon l_xy [g_copy] ) => o_polygon`

#### Description

`gc() ; requires Skill development licenses axlPolyMemUse() ;; should return all 0's` This offsets the entire poly by the provided xy coordinate. Optionally if `g_copy` is `t`it will copy the poly, default is to offset the provided poly.

Note: The offseted polygon must be entirely within the extents of the drawing.

#### Arguments

`o_polygon o_polygon` on which the operation is to be done.

`lo_polygon` Optionally pass a list of polys.

`l_xy` Coordinates in user units for offset.

`g_copy` Optional, if `t` does the offset on a copy.

#### Value Returns

`lo_polygon/`

`o_polygon` In place offset (`g_copy nil`) or offseted copy of polygon	(`g_copy` is `t`). If passed a list of polys returns a list otherwise	return a poly.

#### Examples

See the following.

`<cdsroot>/share/pcb/examples/skill/axlcore/ashpoly.il`

#### See Also

axlPolyFromDB

### axlPolyOperation

`axlPolyOperation( o_polygon1 / lo_polygon1 o_polygon2 / lo_polygon2 s_operation ) => lo_polygon/nil`

#### Description

Performs the logical operation specified on the two sets of polygons. Does not allow hole polygons as input. When holes are passed as input, the following warning is displayed:

`Invalid polygon id argument -<argument>`

- -- This function is provided "as-is". Result, in certain cases, may fail or deliver incorrect results. No commitment can be made to address issues uncovered when using this API.-- Underlying polygon operation function fails and returns `nil` in rare dense geometrical situations.-- This API may consume a large amount of memory and take a considerable of amount of time to return a result. This is normally only noticeable when the number of polygons provided exceed 10000. The number polygons can be calculated by taking the length of the polygons provided to args 1 and 2 PLUS adding all of the polys holes (poly->holes) in the polygons. -- Algorithm has lines take have a width 1 or 0 database units. This means if you have a design with 2 units of accuracy, 1 database unit is .01.

#### Arguments

| Name | Description |
|---|---|
| `o_polygon1` / `lo_polygon1` | `o_polygon` or list of `o_polygons` on which the operation is to be done. |
| `o_polygon2` / `lo_polygon2` | `o_polygon` or the list of `o_polygons` on which the operation is to be done. |
| `s_operation` | String specifying the type of logical operation, one of `'AND`, ``OR`, or ``ANDNOT`. |

#### Value Returns

| Name | Description |
|---|---|
| `lo_polygon` | List of `o_polygons` which represent the resulting geometry from performing the operation on the arguments. |
| `nil` | Error due to incorrect arguments. |

For example:

(`o_polygon_out1 o_polygon_out2` ...) is returned if the result after performing the operation is a list of polygons.

`nil` is returned if the result after performing the operation is a `nil` polygon. For example, consider performing the `AND` operation on two non-overlapping sets of polys.

`nil` is returned if the operation fails. You can obtain a descriptive error message by calling axlPolyErrorGet.

#### Examples

`poly1_list = (axlPolyFromDB cline dbid)`

`poly2_list = (axlPolyFromDB shape_dbid)`

`res_list = (axlPolyOperation poly1_list poly2_list 'OR)`

### axlPolyExpand

`axlPolyExpand( o_polygon1 / lo_polygon1 f_expandValue s_expandType ) => lo_polygon/nil`

#### Description

This function yields a list of polys after expanding them by a specified distance. Use of a negative number causes contraction. Distance is specified in user units. This function does not allow hole polys as input. When holes are passed as input, the following warning is displayed:

`Invalid polygon id argument -<argument>`

- Underlying logical operation function fails and returns `nil` in rare dense geometrical situations. 'ALL_ARC mode may have round-off issues when shape has very small arc segments.

Trimming options are (`s_expandType`):

| Name | Description |
|---|---|
| 'NONE | no corner modifications |
| 'ACU_ARC | Trim inside acute (less then 90 degrees) line/line corners with arcs and always chamfer spikes. No obtuse or right angle trimming is done. |
| 'ACU_BLUNT | Trim acute inside corners and spikes with line segments. |
| 'ALL_ARC | Trim inside and outside line/line, line/arc and arc/arc corners with respect to these angle rules:
 
 All acute angles are trimmed.
 
 
 Most obtuse angles (more then 135 degrees) are trimmed.
 
 
 90 degree corners are trimmed.
 
 Finally always chamfer spikes. |

Note: Poly expansion with 0 and no trim is returns the input poly NOT a list `axlPolyExpand(poly 0.0 'NONE) -> o_polygon`.

#### Arguments

`o_polygon1` /`lo_polygon1`

`o_polygon` / list of `o_polygons` on which the operation is to be done.

| Name | Description |
|---|---|
| `f_expandValue` | Amount of expansion in user units. |
| `s_expandType` | Symbol specifying the exterior corners of the geometry during expansion, (see above) |

#### Value Returns

| Name | Description |
|---|---|
| `lo_polygon` | List of `o_polygons` which represent the resulting geometry after performing the expansion on the polys passed as arguments. |
| `nil` | Failed to expand polys due to incorrect arguments. |

To be more specific:

- (`o_polygon_out1 o_polygon_out2` ...) is returned if the result after performing the operation is a list of polys.

- `nil` is returned if the result after performing the operation is a `nil` poly, for example, consider contracting a 20x30 rectangle by 40 units.

- `nil` is returned if the operation fails. You can get a descriptive error message by calling `axlPolyErrorGet()`.

#### Examples

`poly_list = (axlPolyFromDB shape_dbid)`

`exp_poly = (axlPolyExpand poly_list 10.0 'ALL_ARC)`

The following sequence of diagrams illustrates the behavior of each of the options.

Figure 21-2 
 Original Poly

ALL_ARC

During expansion of the poly boundary, an arc is inserted for the edges in the offset shape that satisfy the following criteria:

- Edges form an outside (or convex) point of the poly boundary.The reverse is true for the voids.

Figure 21-3 
 Expanded Using ALL_ARC

ACU_ARC

During expansion of the poly boundary, an arc is inserted for the edges in the offset shape that satisfy the following criteria:

- Edges form an outside (or convex) point of the poly boundary.

- Edges form an angle sharper than 90 degree.The reverse is true for the voids.

Figure 21-4 
 Expanded Using ACU_ARC

ACU_BLUNT

During expansion of the poly boundary, a blunt edge is inserted for the edges in the offset shape that satisfy the following criteria:

- Edges form an outside (or convex) point of the poly boundary.

- Edges form an angle sharper than 90 degree.The reverse is true for the voids.

Figure 21-5 
 Expanded Using ACU_BLUNT

### axlIsPolyType

`axlIsPolyType ( g_polygon ) => t/nil`

#### Description

Tests if argument `g_polygon` is a polygon user type.

#### Arguments

| Name | Description |
|---|---|
| `g_polygon` | Object to test, any skill variable |

#### Value Returns

| Name | Description |
|---|---|
| `t` | `g_polygon` is a polygon user type. |
| `nil` | `g_polygon` is not a polygon user type. |

#### Examples

`poly = axlPolyFromDB(cline_dbid)`

`axlIsPolyType(poly) returns t.`

`axlIsPolyType(cline_dbid) returns nil.`

#### See Also

axlPolyFromDB

### axlPolyFromHole

`axlPolyFromHole ( o_polygon ) => lo_polygon/nil`

#### Description

Creates a new poly from the vertices of the hole, and sets the `isHole` attribute of the resulting poly to `nil`. Function returns `nil` in case of error.

#### Arguments

| Name | Description |
|---|---|
| `o_polygon` | `o_polygon` on which the operation is to be done. Must have `isHole` attribute set to `t` (that is, the argument must be a hole). |

#### Value Returns

| Name | Description |
|---|---|
| `lo_polygon` | List of `o_polygons` which represent the resulting geometry after creating poly from the hole argument. |
| `nil` | Error due to incorrect argument. |

#### Examples

`poly = axlPolyFromDB(shape_dbid)`

`hole = car(poly->holes)`

`polyList = axlPolyFromHole(hole)`

### axlPolyErrorGet

`axlPolyErrorGet ( ) => t_error/nil`

#### Description

Retrieves the error from the logop core. See the following list of error strings returned by the logical operation core:

| Name | Description |
|---|---|
| Error type | String returned |
| problem with arcs | "`Bad arc data in polygon operations.`" |
| bad data | "`Data problem inside polygon operations.`" |
| internal error in logical op data handling | "`Polygon operation failed because of internal error.`" |
| numerical problem in logical op | "`Computational problem while doing polygon operations.`" |
| memory problem | "`Out of memory.`" |
| no error | `NIL` |

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t_error` | Error from the logical operation core. |
| `nil` | No logical operation error. |

#### Examples

`l_poly1 = axlPolyFromDB(shape_dbid)`

`l_poly2 = axlPolyFromDB(cline_dbid ?endCapType 'SQUARE)`

`l_polyresult = axlPolyOperation(l_poly1 l_poly2 'ANDNOT)`

`if (null l_polyresult) axlMsgPut(list axlPolyErrorGet())`

Use Models

