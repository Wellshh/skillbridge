### axlDegToRad

`axlDegToRad( n_angle ) => f_angle`

#### Description

Converts an angle in degrees to radians.

#### Arguments

| Name | Description |
|---|---|
| `n_angle` | Angle in degrees |

#### Value Returns

| Name | Description |
|---|---|
| `f_angle` | Angle in radians |

#### Examples

`axlDegToRad(45.0)`

`=> 0.7853982`

#### See Also

axlRadToDeg, axlMathConstants

### axlDistance

`axlDistance( l_point1 l_point2 ) => f_distance`

#### Description

Returns the distance between two points. You may use floating point.

#### Arguments

| Name | Description |
|---|---|
| `l_point` | A point. |
| `ll_line` | Two points at the ends of a line. |

#### Value Returns

| Name | Description |
|---|---|
| `f_distance` | Distance between two points in floating point form. |

#### Examples

`axlDistance(10:20 5:20) = 5.0`

### axlGeo2Str

`axlGeo2Str( f_dbrep/point ) => t_result/nil`

#### Description

When converting floating point numbers to strings you may find the number printed is slightly differently then the value Allegro reports. This is difference is due to how floating point numbers are represented in the computer. The following article is an excellent paper on the subject: What Every Computer Scientist Should Know About Floating-Point Arithmetic by David Goldberg.

http://docs.sun.com/source/806-3568/ncg_goldberg.html

This article also explains why sometimes the comparison of two floating numbers that appear the same results in a non-equal result. The results only differ from printf when a "5" exists at the location one place more then the database accuracy. The behavior is as follows for rounding:

- if digit at db accuracy is odd and then 5 round up

- if digit at db accuracy is even and then 5 round down

See examples below. This supports two modes, a single floating point number and a point (a list of two floating point numbers).

#### Arguments

| Name | Description |
|---|---|
| `dbrep` | a floating point number |
| `point` | a xy point |

#### Value Returns

Returns a string with Allegro rounding. If a point is passed then the return format is: `"<x> <xy>"`

`nil:` not a legal argument

#### Examples

Assume database is two decimal places

`procedure( testit( f)`

`printf("printf=%.2f\taxlGeo2Str=%s \toriginal value %.3f\n"`

`f axlGeo2Str(f) f)`

`)`

`testit(1.115)`

`testit(1.125)`

`testit(-1.115)`

`testit(-1.125)`

`Results:`

`printf=1.11 axlGeo2Str=1.12 original value 1.115`

`printf=1.12 axlGeo2Str=1.12 original value 1.125`

`printf=-1.11 axlGeo2Str=-1.12 original value -1.115`

`printf=-1.12 axlGeo2Str=-1.12 original value -1.125`

Using a point

`axlGeo2Str(100.124:123.345)`

#### See Also

axlGeoEqual

### axlGeoArcCenterAngle

`axlGeoArcCenterAngle( l_startPoint l_endPoint f_angle [g_clockwise] ) => l_center/nil`

#### Description

Calculates the center of an arc given the angle between its endpoints. Uses the arguments depending on `g_clockwise` as shown in Figure 25-1.

Figure 25-1 
 Center of Arc Calculation

#### Arguments

| Name | Description |
|---|---|
| `l_startPoint` | Start point of the arc |
| `l_endPoint` | End point of the arc |
| `f_angle` | Included angle of the arc |
| `g_clockwise` | Rotational sense of the arc: `t` is clockwise. `nil` is counterclockwise (the default). |

#### Value Returns

| Name | Description |
|---|---|
| `l_center` | Center of the arc as a list: (`X Y`). |
| `nil` | Cannot calculate the center from the given arguments. |

#### Examples

`print axlGeoArcCenterAngle( 7500:5600 8000:4700 68.5 t)``mypath = axlPathStart(list( 7500:5600))``axlPathArcAngle(mypath, 0., 8000:4700, t, 68.5)``axlDBCreatePath( mypath, "etch/bottom")``⇒ (7089.086 4782.826)`

Prints the center for the clockwise arc going through the points (7500:5600) and (8000:4700) using `axlGetArcCenterAngle`, then adds the arc through those points using `axlPathArcAngle`, and compares their centers.

The arc is shown in the following figure.

Do Show Element on the arc to show its center coordinate. The arc lists: `"center-xy (7089,4783)"` which agrees with the (7089.086 4782.826) printed by `axlGeoArcCenterRadius`.

### axlGeoArcCenterRadius

`axlGeoArcCenterRadius( l_startPoint l_endPoint f_radius [g_clockwise] [g_bigArc] ) => l_center/nil`

#### Description

Calculates center of an arc given its radius. Calculates `l_center` either for one arc or another depending on the arguments, as shown.

#### Arguments

| Name | Description |
|---|---|
| `l_startPoint` | Start point of the arc |
| `l_endPoint` | End point of the arc |
| `f_radius` | Radius of the arc |
| `g_clockwise` | Rotational sense of the arc: `t` is clockwise. `nil` (default) is counterclockwise. |
| `g_bigArc` | Flag telling whether the arc extends as the larger or the smaller of the two arcs possible between the start and endpoints. |

#### Value Returns

| Name | Description |
|---|---|
| `l_center` | Center of the arc as a list: (`X Y`). |
| `nil` | Cannot calculate the center from the given arguments. |

#### Examples

`print axlGeoArcCenterRadius( 7500:5600 8000:4700 1000)``⇒ (8499.434 5566.352)``mypath = axlPathStart(list( 7500:5600))``axlPathArcRadius(mypath, 0., 8000:4700, t, nil, 1000)``axlDBCreatePath( mypath, "etch/bottom")``print axlGeoArcCenterRadius( 7500:5600 8000:4700 1000 t)``⇒ (7000.566 4733.648)``mypath = axlPathStart(list( 7500:5600))``axlPathArcRadius(mypath, 0., 8000:4700, nil, nil, 1000)``axlDBCreatePath( mypath, "etch/top")`

Prints the two possible centers for the arcs going through the points (7500:5600) and (8000:4700), then adds arcs through those points using `axlPathArcRadius`, and compares the centers.

The arcs are shown in the following figure.

Do Show Element on each arc to show its center coordinate.The solid arc on the left lists: `"center-xy (8499,5566)"` which agrees with the (8499.434 5566.352) printed by `axlGeoArcCenterRadius`. The dotted arc on the right lists: `"center-xy (7001, 4734)"`, which agrees within rounding with `(7000.566 4733.648)`printed for the other arc.

### axlGeoEqual

`axlGeoEqual( f_one f_two ) => t/nil`

#### Description

Performs an equal comparison between two floating point numbers and determines if they are equal within plus or minus the current database accuracy.

Useful for comparing floating point numbers converted from strings (example - using `atof` function) with those obtained from an AXL database id. Since the conversion of these numbers takes different paths (string to float versus integer to float, in the case of the database) you can have different numbers.

Note: To understand the basis of why a simple equal (==) comparison cannot always be used with floating point numbers see David Goldberg's paper on "What Every Computer Scientist Should Know About Floating-Point Arithmetic." Wikipedia also has a good article: http://en.wikipedia.org/wiki/Floating_point

Floating point numbers can be internally represented by using two different formats; `float` (4 bytes) and `double` (8 bytes). All AXL interfaces use 8 bytes. Skill interfaces depend upon the use so:

`sscanf( "0.2" "%g" n) ; skill float sscanf( "0.2" "%lg" nd) ; skill double` Whereever possible, use the double representation as it has more accuracy.

#### Arguments

Two floating point numbers.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Given numbers are equal within the current database accuracy. |
| `nil` | Given numbers are not equal within the current database accuracy. |

#### Examples

axlGeoEqual(2.0 2.0)

#### See Also

axlGeo2Str, axlGeoPointsEqual

### axlGeoRotatePt

`axlGeoRotatePt( f_angle l_xy l_origin/nil [mirror] ) => l_xyResult/nil`

#### Description

Rotates xy about an origin by angle. Optionally applies mirror on the x axis.

#### Arguments

| Name | Description |
|---|---|
| `f_angle` | Angle 0 to 360 degrees (support for 1/1000 of a degree); rotation is counter-clockwise for positive numbers. |
| `l_xy` | xy point to rotate in user units. |
| `l_origin` | Origin to rotate about; if `nil` uses (0, 0) mirror: optional mirror flag (`t` perform mirror). |

#### Value Returns

| Name | Description |
|---|---|
| `l_xyResult` | Rotated result. |
| `nil` | Error in arguments or rotation results in return being outside of the database extents. |

#### Examples

Rotate:

`axlGeoRotatePt(45.0 10:200 5:2) -> (-131.4716 145.5427)`

Rotate and mirror:

`axlGeoRotatePt(45.0 10:200 5:2 t) -> (-138.5427 138.4716)`

Rotate about 0,0:

`axlGeoRotatePt(90.0, 100:0 nil) -> (0.0 100.0)`

### axlGeoPointsEqual

`axlGeoPointsEqual( l_point1 l_point2 ) => t/nil`

#### Description

This performs an equal comparison between two xy points and determines if they are equal within db accuracy.

#### Arguments

two xy points

#### Value Returns

- `t` if they are equal within current database accuracy.

- `nil` not equal

#### Examples

`pt1 = '(2.0 1.1)`

`pt2 = '(2.0 1.1)`

`axlGeoPointsEqual(pt1 pt2)`

#### See Also

axlGeoEqual

### axlIsBetween

`axlIsBetween( l_testPoint l_pt1, l_pt2 ) => t/nil`

#### Description

Used to check if a given point lies between two specified points. Returns `t` if the point is in between the two points or on one of the points.

#### Arguments

| Name | Description |
|---|---|
| `l_testPoint` | test point |
| `l_pt1, l_pt2` | two test points |

#### Value Returns

`t` if test point specified by `l_testPoint` is between or on the test points specified by `l_pt1` and `l_pt2`, else `nil.`

#### See Also

axlIsPointInsideBox

### axlIsPointInsideBox

`axlIsPointInsideBox( l_point l_box ) => t/nil`

#### Description

Returns `t` if a point is inside or on the edge of a box. Also see axlGeoPointInShape for `dbid`-based tests. You may use floating point.

#### Arguments

| Name | Description |
|---|---|
| `l_point` | A point. |
| `l_box` | A bounding box. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Point is inside or on edge of box |
| `nil` | Point is outside of box. |

#### Examples

`axlIsPointInsideBox(10:20 list(5:20 15:30)) = t`

`axlIsPointInsideBox(0:20 list(5:20 15:30)) = nil`

`axlIsPointInsideBox(15:20 list(5:20 15:30)) = t`

### axlIsPointOnLine

`axlIsPointOnLine( l_point ll_line [f_nearNess] ) => t/nil`

#### Description

Returns `t` if point is on a given line or `nil` if not on the line.

If f_nearNess value is provided, it is used as a tolerance so if a point is within the tolerance value.

In either case, an epsilon of axlEpsilonFloat (see axlMathConstants) is applied.

#### Arguments

| Name | Description |
|---|---|
| `l_point` | A point. |
| `ll_line` | Two end points. |
| [f_nearNess] | (optional) A tolerance value |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Point is on the specified line. |
| `nil` | Point is not on the specified line. |

#### Examples

`axlIsPointOnLine(10:20 list(5:20 15:30)) = nil`

`axlIsPointOnLine(10:30 list(5:20 15:30)) = t`

`axlIsPointOnLine(10:20 list(5:20 15:30) 2.5) = t`

#### See Also

axlIsBetween

### axlLineSlope

`axlLineSlope( ll_line ) => f_slope`

#### Description

Returns the slope of a line. You may use floating point.

#### Arguments

| Name | Description |
|---|---|
| `ll_line` | Two end points. |

#### Value Returns

| Name | Description |
|---|---|
| `f_slope` | Slope of the line. |
| `nil` | Line is vertical. |

#### Examples

`axlLineSlope(list(5.0:20.10 15.4:30.2)) = 0.9711538`

`axlLineSlope(list(5:20 5:40)) = nil`

### axlLineXLine

`axlLineXLine( l_seg1 l_seg2 ) => t`

#### Description

This function is no longer required, but is kept for backward compatibility.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Returns `t` always. |

### axlMathConstants

sstatus(fullPrecision t)

printf("%5.18\n" axlPI)

#### Description

Provides predefined set of high accuracy math constants. They are:

- `axlPI` - PI

- `axlPI_2` - PI/2.0

- `axlPI_4` - PI/4.0

- `axlSQRT2` - sqrt(2)

- `axlSQRT1_2` - 1/sqrt(2)

- `axlEpsilonFloat` - epsilon for floating point numbers (32 bit)

- `axlEpsilonDouble` - epsilon for doubles (64 bit)

- `axlDegPerRad` - Degrees per radian

- `axlRadPerDeg` - Radians per degree

axlRad0, axlRad45, axlRad90, axlRad135, axlRad180, axlRad225, axlRad270, axlRad315, axlRad360 - radians values for popular degrees values

Note: Skill, by default, limits the number of decimal places printed but these constants are still stored and used at the full precision. To see the full precision of the constant you can do:

### axlMathDotProduct

`axlMathDotProduct( l_ptA1 l_ptA2 l_ptB1 l_ptB2 ) => f_dotProduct`

#### Description

This calculates the dot or scaler product.

Dot Product:

`(ptB1.y - ptA1.y)*(ptB2.y - ptA2.y) + (ptB1.x - ptA1.x)*(ptB2.x - ptA2.x)` Line are perpendicular when return is 0.0

#### Arguments

Four coordinates describing 2 lines.

#### Value Returns

Dot product result.

#### See Also

`axlMidPointLine(list(5:20 15:30)) = (10.0 25.0)` axlDistance

### axlMidPointArc

`axlMidPointArc( ll_endPoints l_center f_radius g_clockwise ) => l_midPoint`

#### Description

Returns mid-point on a arc. Note mid-point may not be on a database coordinate. All parameters may be obtained from a arc dbid.

#### Arguments

| Name | Description |
|---|---|
| `ll_line` | arc end points |
| `l_center` | center of arc |
| `f_radius` | arc radius |
| `g_clockwise` | Is arc in clockwise (`t`) or counter clockwise direction (`nil`) |

#### Value Returns

| Name | Description |
|---|---|
| `l_midPoint` | mid-point of line |
| `nil` | error in arguments |

#### Examples

- try clockwise

`axlMidPointArc(list(20:0 0:20) 0:0 20 t) = (-14.14214 -14.14214)`

- try counter-clockwise

`axlMidPointArc(list(20:0 0:20) 0:0 20 nil) = (14.14214 14.14214)`

#### See Also

axlMidPointLine

### axlMidPointLine

`axlMidPointLine( ll_line ) => l_midPoint`

#### Description

Returns mid-point of line. Note mid-point might not be a database coordinate.

#### Arguments

| Name | Description |
|---|---|
| `ll_line` | Two end points |

#### Value Returns

| Name | Description |
|---|---|
| `l_midPoint` | mid-point of line |
| `nil` | error in arguments |

#### See Also

`axlMidPointLine(list(5:20 15:30)) = (10.0 25.0)` axlMidPointArc

### axlMPythag

`axlMPythag( l_pt1 l_pt2 ) => f_distance/nil`

#### Description

Calculates distance between two points using pythagoras. This is faster then building this code in Skill.

The `l_ptN` is an x:y coordinate.

#### Arguments

| Name | Description |
|---|---|
| l_pt1, l_pt2 | Two xy points. |

#### Value Returns

| Name | Description |
|---|---|
| `f_distance` | Distance between points. |
| `nil` | Arguments were not xy points. |

#### See Also

axlMXYAdd

### axlMUniVector

`axlMUniVector( l_pt1 l_pt2 [f_length] ) => l_uniPt1`

#### Description

`axlMPythag(1263.0:1062.0 1338.0:1137.0) -> 106.066` This calculates a unit-vector. A unit vector allows one to calculate points additional points along that line.

It has two modes of operation:

- Without a length returns a unit vector to use in other operations like `axlMXYMult`. Use this mode if you need to calculate several points from the same unit vector.

- With a length, calculates a new `xy` location f_length from l_pt1 along the vector specified by `pt1` and `pt2`.

This provides optimized solution over the traditional trigonometric approach.

#### Arguments

| Name | Description |
|---|---|
| `l_pt1, l_pt2:` | 2 xy points |
| `f_length:` | optional length to project |

#### Value Returns

Returns a unit-vector, xy point

`nil:` arguments were not xy points

#### Examples

Found a point 5 units along a line from 1263.0:1062.0 to 1338.0:1137.0

`origin = 1263.0:1062.0 uniVec = axlMUniVector(origin 1338.0:1137.0) res = axlMXYMult(uniVec, 5.0 origin)` Same as example 1 except have `uni vec` do all the work

### axlMXYAdd

`axlMXYAdd( l_pt1 l_pt2 ) => l_pt/nil`

#### Description

`res = axlMUniVector(origin 1338.0:1137.0 5.0)` This does a `l_pt1 + lpt2` and returns the result.

The `l_ptN` is an x:y coordinate.

#### Arguments

`l_pt1, l_pt2` Two xy points.

#### Value Returns

`l_pt` Returns coordinate that is result of addition.

`nil` Arguments are not coordinates.

#### See Also

axlMXYSub

### axlMXYMult

`axlMXYMult( l_uniVec f_factor [l_origin] ) => l_pt/nil`

#### Description

`axlMXYAdd(1263.0:1063.0 1338.0:1137.0) -> (2601.0 2200.0)` This is a convenience function that does a `l_pt.x * f_factor` and `lpt.y * factor` and returns the result. If provided an origin, it adds the origin.

`(l_uniVec * f_factor) + l_origin` It is normally used in conjunction with `axlMUniVector` to project a point along a vector.

#### Arguments

| Name | Description |
|---|---|
| `l_uniVec:` | xy point |
| `f_factor:` | multiplication factor |
| `l_origin:` | additive point |

#### Value Returns

| Name | Description |
|---|---|
| `l_pt:` | Returns resultant coordinate |
| `nil:` | Arguments are not coordinates |

#### See Also

`axlMXYMult(1263.0:1063.0 2.0) -> (2526.0 2126.0)` axlMUniVector

### axlMXYSub

`axlMXYSub( l_pt1 l_pt2 ) => l_pt/nil`

#### Description

This does a `l_pt1 - lpt2` and returns the result.

The `l_ptN` is an x:y coordinate.

#### Arguments

`l_pt1, l_pt2` Two xy points.

#### Value Returns

`l_pt` Returns coordinate that is result of subtraction.

`nil` Arguments are not coordinates.

#### See Also

axlMXYAdd

### axlRadToDeg

`axlRadToDeg( n_angle ) => f_angle`

#### Description

`axlMXYSub('(1263.0 1063.0) '(1338.0 1137.0)) -> (-75.0 -74.0)` Converts an angle in radians to degrees.

#### Arguments

| Name | Description |
|---|---|
| `n_angle` | The angle in radians |

#### Value Returns

| Name | Description |
|---|---|
| `f_angle` | The angle in degrees |

#### Examples

`axlRadToDeg(0.7853982) => 45.0`

#### See Also

axlDegToRad, axlMathConstants

### axl_ol_ol2

`axl_ol_ol2( l_seg1 l_seg2 ) => l_result`

#### Description

Finds the intersection point of two lines. If the lines intersect, returns the intersection point with a distance of 0. If the lines do not intersect, the distance is not zero and the function returns `t`.

#### Arguments

| Name | Description |
|---|---|
| `l_seg1` | 1st line segment (list `x1`:`y1 x2`:`y2`) |
| `l_seg2` | 2nd line segment (list `x1`:`y1 x2`:`y2`) |

#### Value Returns

| Name | Description |
|---|---|
| `nil` | Error due to incorrect argument. |
| (`car l_result`) | Intersect or nearest point on seg1 |
| (`cadr l_result`) | Intersect or nearest point on seg2 |
| (`caddr l_result`) | Distance between the two intersect points. |

#### Examples

Data for examples

`a=list(1:5 5:5)`

`b=list(2:5 4:2)`

`c=list(0:0 5:0)`

`d=list(4:5 7:5)`

Example 1

`axl_ol_ol2(a b)`

`⇒ ((2.0 5.0) (2.0 5.0) 0.0)`

Intersects line, returns intersection point, note distance of 0.

Example 2

`axl_ol_ol2(a c)`

`⇒ ((3.0 5.0) (3.0 0.0) 5.0)`

Lines don't intersect, returns closest point on each line and distance.

Example 3

`axl_ol_ol2(a d)`

`⇒ ((4.5 5.0) (4.5 5.0) 0.0)`

Lines overlap, distance of 0 and selects mid-point of the overlap.

### bBoxAdd

`bBoxAdd( l_bBox1 l_bBox2 ) => l_bBox_result`

#### Description

Adds two bounding boxes together and returns the result.

#### Arguments

2 bBox values

#### Value Returns

Resulting bounding box.

#### Examples

Expand bounding box by 100.

`orig = '((200 100) (400 500)) res = bBoxAdd(orig '((-100 -100) (100 100))) -> ((100 0) (500 600))`

Example 2

`res = bBoxAdd('((200 100) (400 500)) '((0 0) (200 100)))`

`-> ((200 100) (600 600))`

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

