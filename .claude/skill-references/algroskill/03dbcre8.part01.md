<!--
source: algroskill/03dbcre8.md
part: 1/2
estimated_tokens: 13495
-->

### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

15
==

Database Create Functions
=========================

Overview
--------

This chapter describes the AXL functions that add objects to the Allegro PCB Editor database. Some functions require input that you set up using available auxiliary functions, which are also described in this chapter. For example, Allegro PCB Editor paths consist of any number of contiguous line and arc segments. To add this multi-structure to the Allegro PCB Editor database, first create a temporary path, adding each line or arc segment using separate function calls. Once the temporary path contains all required segments, create the Allegro PCB Editor line-object, shape or void by calling the appropriate database create function, giving the path structure as an argument. The chapter shows several examples of the process.

Database create (`DBCreate`) functions modify the active Allegro PCB Editor database in virtual memory and require a database save to make changes permanent in the file.

Supply all coordinates to these functions in user units, unless otherwise noted.

The functions described here do not display the objects immediately as they create them. To display all changes, call an interactive function, exit SKILL, or return control to the Allegro PCB Editor command interpreter.

* To immediately display an object you have just created, do one of the following:

* Call the function`axlDisplayFlush`

> -or-

* Call an interactive function

If you create an object and then delete it without calling`axlDisplayFlush` or calling an interactive function, the object never appears in the display.

The class of geometric objects that`DBCreate` functions create are calledfigures. `DBCreate` functions return, in a list, the `dbids` of any figures they create and a Boolean value `t` if the creation caused any DRCs. The functions return `nil` if they could not create any figures. The exact structure of the data returned differs among the commands. See the individual commands for detailed descriptions.

You can set the active layer (Allegro PCB Editor class/subclass) by calling the`axlSetCurrentLayer` function.This function returns a `nil` if you try to set an invalid layer or if you try to create a figure on a layer that does not allow that figure type.

AXL-SKILL creates a figure as a member of a net only if the figure is on an etch layer. Where a function has a netname as an argument, and the active layer is an etch layer, the function attaches the figure to the net specified by that netname. If the net does not exist, an error occurs. If you specify`nil` for the netname, the function determines the net for the figure by what other figure it touches. If the figure is free standing, that is, touches nothing, the figure becomes a member of the dummy net (no net).

The functions use defaults for all parameters you do not supply. If you do not supply a required parameter (one without a default, for example,`pointList`) the function considers the call an error and returns `nil`.

The database create functions do not add figures to the select set. They leave the select set unchanged.

Path Functions
--------------

An Allegro PCB Editor`line` is a figure consisting of end-to-end straight line and arc segments, each segment having a width you can define separately. Allegro PCB Editor `shapes`and`polygons` are figures that define an area. A shape owns a closed line figure that defines the perimeter of the shape. The shape has an associated fill pattern and can also own internal `voids`. Each void in turn owns a polygon that defines its boundary.

A`path` is a set of contiguous arc and single straight line segments. In AXL, you first create a path consisting of the line and arc segments by adding each segment with a separate AXL function, then creating the actual figure using the appropriate `axlDBCreate` function, with the path as one of the arguments. With AXL convenience functions described later in this chapter, you can create rectangles, circles, and lines consisting only of straight segments.

All coordinate arguments to the path functions are in user units and are absolute to the layout origin.

#### *Example*

This general example shows how to create a path, then use it as an argument in an`axlDBCreate` function. The example creates a path consisting of a straight line segment, then adds an arc and another line segment, and uses it as an argument to create a path that is a member of net `"net1"` on etch subclass `"top"`:

```
path = axlPathStart( (list 100:250))    axlPathLine( path, 0.0, 200:250 )    axlPathArcCenter( path, 0.0, 300:350, nil, 200:350 )    axlPathLine( path, 0.0, 300:450 )    axlDBCreatePath( path, "etch/top", "net1")
```

### axlPathStart

`axlPathStart(l_points[f_width])⇒ r_path/nil`

#### Description

Creates a new path with a startpoint and one or more segments as specified by the list`l_points` and returns the path `dbid`. You can add more straight-line and arc segments to the returned `r_path` using the `axlPathArc` and `axlPathLine` functions described in this section. Once`r_path` has all the segments you require, create the actual database figure using the appropriate `axlDBCreate` function, with `r_path` as one of the arguments.

#### Arguments

#### Value Returned

|  |
| --- | ---
| `l_points` | List of`n` vertices, where `n` > `1`.  If`n` = `1`, `r_path` returns with that single vertex as its startpoint, but with no segments.  You must subsequently add at least one segment before adding it to the database.  If`n` > `1`, `r_path` returns with `n``-1` straight-line segments.
| `f_width` | Width for all segments, if any created, between the`l_points`. `f_width` is the default width for all additional segments added to `r_path` using `axlPath` functions. You can override this default width each time you add a segment using an `axlPath` function by using a `f_width` argument when you invoke the function.
| `r_path``/nil` | Returns the*r\_path* handle.
**Note:** This is a handle object, but is*not* an Allegro PCB Editor `dbid`*.*

#### Example

See start of the[Path Functions](#367312 "15").

### axlPathArcRadius

### axlPathArcAngle

### axlPathArcCenter

```
axlPathArcRadius(r_pathf_widthl_end_pointg_clockwiseg_bigarcf_radius)⇒ r_path/nil
```

`axlPathArcAngle(r_pathf_widthl_end_pointg_clockwisef_angle)⇒ r_path/nil`

`axlPathArcCenter(r_pathf_widthl_end_pointg_clockwisel_center)⇒ r_path/nil`

#### Description

Each of these functions provides a way to construct an arc segment from the current endpoint of`r_path` to the given `l_end_point` in the direction specified by the Boolean `g_clockwise`, as described below and shown in [Figure 15-1](#367350 "15").

Attempts to create small arcs using many decimal points of accuracy may fail due to rounding errors.

#### Arguments

****Figure 15-1****
**Effects ofaxlPathArc Arguments**

|  |
| --- | ---
| `r_path` | Handle of an existing`r_path` to receive arc segment.
| `f_width` | Width of an arc segment in user units. Overrides, for this segment only, any width originally given in`axlPathStart`;`nil` = use current width
| `l_end_point` | End point to which an arc is to be constructed. Start point is the last point currently in`r_path` in absolute coordinates.
| `g_clockwise` | Direction to create arc:  `t` → create arc clockwise from start to endpoint  `nil` → create counterclockwise.  Default is counterclockwise (See[Figure 15-1](#367350 "15")).
| `g_bigarc` | `axlPathArcRadius`: Create an arc greater than or equal 180 degrees (See [Figure 15-1](#367350 "15")).
| `f_radius` | `axlPathArcRadius`: Arc radius in user units.
| `f_angle` | `axlPathArcAngle`: Angle in degrees subtended by arc (See [Figure 15-1](#367350 "15")).
| `l_center` | `axlPathArcCenter`: Arc center point in absolute coordinates.
#### Value Returned

|  |
| --- | ---
| `r_path` | Current path handle.
| `nil` | Arc path not created.
#### Example 1

```
mypath = axlPathStart( list( 8900:4400))axlPathArcRadius( mypath, 12., 8700:5300, nil, nil, 500)axlDBCreatePath( mypath, "etch/top")
```

Adds a smaller-than-180 degree counterclockwise arc by radius.

Creates the smaller possible arc:

#### Example 2

```
mypath = axlPathStart( list( 8900:4400))axlPathArcAngle( mypath, 12., 8700:5300, nil, 330)axlDBCreatePath( mypath, "etch/top")
```

Adds a counterclockwise arc subtending 330 degrees.

#### Example of axlPathArcCenter

See[Example](#368719 "15").

### axlPathLine

`axlPathLine(r_pathf_widthl_end_point)⇒ r_path/nil`

#### Description

Adds a single straight line segment to the end of an existing`r_path` structure as specified by the arguments. Start point of the line is the last point in `r_path`.

#### Arguments

|  |
| --- | ---
| `r_path` | Handle of an existing path.
| `f_width` | Width of the segment.  `nil` = segment takes the width given when `r_path` was created.
| `l_end_point` | End point of the line segment in absolute coordinates.
#### Value Returned

|  |
| --- | ---
| `r_path` | Path structure following addition of single straight line segment to end of`r_rath` structure.
| `nil` | No line segment added to`r_path` structure.
#### Example

See start of the[Path Functions](#367312 "15").

### axlPathGetWidth

`axlPathGetWidth(r_path)⇒ f_width/nil`

#### Description

Gets the default width of an existing path structure.

#### Arguments

|  |
| --- | ---
| `r_path` | Handle of an existing path structure.
#### Value Returned

|  |
| --- | ---
| `f_width` | Default width of the path structure.
| `nil` | `r_path` is not a path, or is empty.
#### Example

`axlPathGetWidth` returns the default path width of 173 mils.

> ```
> path = axlPathStart( (list 1000:1250), 173)    axlPathLine( path, 29, 2000:1250)    axlPathLine( path, 33, 3000:3450)    axlDBCreatePath( path, "etch/top")
> ```

> `axlPathGetWidth( path)    ⇒ 173.0`

* Creates a path with width 173 mils

* Adds line segments at widths 29 and 33 mils

### axlPathSegGetWidth

`axlPathSegGetWidth(r_pathSeg)⇒ f_width/nil`

#### Description

Gets the width of a single segment in a path structure.

#### Arguments

|  |
| --- | ---
| `r_pathSeg` | Handle of a segment of a path structure.
#### Value Returned

|  |
| --- | ---
| `f_width` | Returns the width of the segment.
| `nil` | `r_pathSeg` is not a segment.
#### Example

`axlPathSegGetWidth` returns the width of that segment only, 33 mils.

> ```
> path = axlPathStart( (list 1000:1250), 173)    axlPathLine( path, 29, 2000:1250)    axlPathLine( path, 33, 3000:3450)
> ```

> `lastSeg = axlPathGetLastPathSeg(path)`

> `axlPathSegGetWidth( lastSeg)    ⇒ 33.0`

* Creates a path with default width 173 mils

* Adds line segments at widths 29 and 33 mils

* Gets the last segment added with`axlPathGetLastPathSeg`

### axlPathGetPathSegs

`axlPathGetPathSegs(r_path)⇒ r_pathList/nil`

#### Description

Gets a list of the segments of a path structure, in the order they appear in the path.

#### Arguments

|  |
| --- | ---
| `r_path` | Handle of an existing path structure.
#### Value Returned

#### Example

|  |
| --- | ---
| `r_pathList` | Returns a list of the segments of the path.
| `nil` | `r_path` is not a path.
> > ```
> > mypath = axlPathStart( (list 1000:1250), 173)    axlPathLine( mypath, 29, 2000:1250)    axlPathArcCenter( mypath, 12, 3000:2250, t, 3000:2250)
> > ```

> > `mysegs = axlPathGetPathSegs( mypath)`

> > `print mysegs    ⇒(array[6]:1057440 array[6]:1057416 array[6]:1057392)`

* Creates a path

* Gets the segments of the path

* Prints the segments of the path

### axlPathGetLastPathSeg

`axlPathGetLastPathSeg(r_path)⇒ r_pathList/nil`

#### Description

Gets the last segment of a path structure.

#### Arguments

|  |
| --- | ---
| `r_path` | Handle of an existing path structure.
#### Value Returned

#### Example

|  |
| --- | ---
| `r_pathList` | Returns the last segment of the path.
| `nil` | `r_path` is not a path.
`axlPathSegGetWidth` returns the width of that segment only, 33 mils.

> ```
> path = axlPathStart( (list 1000:1250), 173)    axlPathLine( path, 29, 2000:1250)    axlPathLine( path, 33, 3000:3450)
> ```

> `lastSeg = axlPathGetLastPathSeg(path)`

> `axlPathSegGetWidth( lastSeg)    ⇒33.0`

* Creates a path with the default width 173 mils

* Adds line segments at widths 29 and 33 mils

* Gets the last segment added using`axlPathGetLastPathSeg`

### axlPathSegGetEndPoint

`axlPathSegGetEndPoint(r_pathSeg)⇒ l_endPoint/nil`

#### Description

Gets the end point of an existing path structure.

#### Arguments

|  |
| --- | ---
| `r_pathSeg` | Handle of a path segment.
#### Value Returned

|  |
| --- | ---
| `l_endPoint` | List containing the end point of the path structure.
| `nil` | `r_pathSeg` is not the `dbid` of a path segment, or the structure is empty.
#### Example

> ```
> path = axlPathStart( (list 1000:1250), 173)    axlPathLine( path, 29, 2000:1250)    axlPathLine( path, 33, 3000:3450)
> ```

> `lastSeg = axlPathGetLastPathSeg(path)`

> `axlPathSegGetEndPoint( lastSeg)    ⇒(3000 3450)`

* Creates a path with default width 173 mils

* Adds line segments at widths 29 and 33 mils

* Gets the last segment added with`axlPathGetLastPathSeg`

`axlPathSegGetWidth` returns the width of that segment only, 33 mils.

### axlPathSegGetArcCenter

`axlPathSegGetArcCenter(r_pathSeg)⇒ l_point/nil`

#### Description

Gets the center point of a path arc segment.

#### Arguments

|  |
| --- | ---
| `r_pathSeg` | Handle of a path arc segment.
#### Value Returned

|  |
| --- | ---
| `l_point` | List containing the center coordinate of the arc segment.
| `nil` | Segment is not an arc.
#### Example

`axlPathSegGetArcCenter` gets the center of the last arc segment.

> ```
> path = axlPathStart( (list 1000:1250), 173)    axlPathLine( path, 29, 2000:1250)    axlPathArcCenter( path, 12., 3000:2250, nil, 2000:2250)
> ```

> `lastSeg = axlPathGetLastPathSeg(path)`

> `axlPathSegGetArcCenter( lastSeg)    ⇒(2000 2250)`

* Creates a path with a straight line segment and an arc segment

* Gets the last segment added with`axlPathGetLastPathSeg`

### axlPathSegGetArcClockwise

`axlPathSegGetArcClockwise(r_pathSeg)⇒ t/nil`

#### Description

Gets the clockwise flag (`t` or `nil`) of a path segment.

#### Arguments

|  |
| --- | ---
| `r_pathSeg` | Handle of a path segment.
#### Value Returned

|  |
| --- | ---
| `t` | Segment is clockwise.
| `nil` | Segment is counterclockwise.
#### Example

`axlPathSegGetArcCenter` returns `t`, meaning the arc segment is clockwise.

> ```
> path = axlPathStart( (list 1000:1250), 173)    axlPathLine( path, 29, 2000:1250)    axlPathArcCenter( path, 12., 3000:2250, t, 2000:2250)
> ```

> `lastSeg = axlPathGetLastPathSeg(path)`

> `axlPathSegGetArcClockwise( lastSeg)    ⇒ t`

* Creates a path with a straight line segment and a clockwise arc segment

* Gets the last segment added using`axlPathGetLastPathSeg`

### axlPathStartCircle

`axlPathStartCircle(l_locationf_width)⇒ r_path/nil`

#### Description

Creates an`axlPath` structure (`r_path`) for a circle.

#### Arguments

|  |
| --- | ---
| `l_location` | Center and radius as ((X Y) R).
| `f_width` | Edge width of the circle.
#### Value Returned

|  |
| --- | ---
| `r_path` | `r_path` with the circle as the only segment.
| `nil` | `axlPath` structure not created.
**Note:** Width must be specified for this interface (it may be 0.0) and since it uses standard SKILL arg check, it must be a flonum.

#### Example

> `(axlPathStartCircle (list 100:200 20),0) ; no width specified.`

### axlPathOffset

`axlDB2Path(r_pathxy)==> r_path`

#### Description

Adds an offset,`xy`, to all points within a `r_path`.

#### Arguments

|  |
| --- | ---
| `r_path` |
| `offset` | offset xy
#### Value Returned

new`r_path`

#### See Also

[axlPathStart](#435992 "15"), [axlDB2Path](#895808 "15")

#### Examples

Obtain shape outline as a`r_path` and then move if by 10:20.

`p = ashOne("shapes")`

`path = axlDB2Path(p)`

`path1 = axlPathOffset(path 10:20)`

### axlDB2Path

`axlDB2Path(o_dbid)==> r_path`

#### Description

This takes a database id (`od_dbId`) and converts it to an r\_path. This function supports all dbids with a segment attribute. For example, shape, void, path, and line.

**Note:** In AXL-Skill terminology, path and line, refers to cline/line and segments, respectively.

#### Arguments

`od_dbId` The dbid for the line.

#### Value Returned

* `r_path` - if object can be converted

* `nil` - object cannot be converted.

***See Also***: [axlPathStart](#435992 "15")

#### Examples

To obtain shape outline as a r\_path, use following commands.

`p = ashOne("shapes")`

`path = axlDB2Path(p)`

### axlDBCreatePath

```
axlDBCreatePath(r_path[t_layer][t_netName]/[`line}[o_parent][lo_props][s_font])⇒ l_result/nil
```

#### Description

Creates a path figure (line or cline) as specified. Does not add a net name to etch when the etch is not connected to a pin, via, or shape. If etch is added, it ties to the first net it touches, otherwise it remains "not a net" as specified by the arguments described below.

Clines may merge with other clines so that the resulting coordinates may be a superset of the provided coordinates. This is not currently true for line types.

Normally, if you want to attach properties to a newly created object, call`axlDBAddProp` after creating the object. CLINEs may merge with existing CLINEs, so the object you end up adding properties to may not match the one you created. The `lo_props` option deals with this issue. You can add properties when you create the CLINE and if the property list on your CLINE differs from any merged target CLINES, your CLINE will not merge.

LINES with the interface are supported even though lines do not merge.

Allegro restricts the layers that allow fonts (s\_font). ETCH layers may never have fonted lines.

#### Arguments

|  |
| --- | ---
| `r_path` | Existing path consisting of the straight-line and arc segments previously created by`axlPath` functions
| `t_layer` | Layer on which to create a path figure. Default is the active layer.
| `t_netName` | Name of the net to which the path figure is to belong.`axlDBCreatePath` ignores `t_netName` if`t_netName`is non-`nil` and `t_layer` is not an etch layer.  If the net`t_netName` does not exist, `axlDBCreatePath` does not create any path, and returns `nil`.
| `` `line `` | Changes default path created on an etch layer from a cline to a line.
| `o_parent` | `dbid` of object to be the parent of the path figure. Use the symbol instance or use `nil`to specify the design. If you attach etch figures to a symbol parent, the figures are not associated with the symbol, and do not move with it.
| `[lo_props]` | Optional list of property name/value pairs. (See`axlDBAddProp` for format.)
| `[s_font]` | Optional line font, may have values as 'SOLID 'HIDDEN 'PHANTOM 'DOTTED 'CENTER. nil is the same as 'SOLID
#### Value Returned

|  |
| --- | ---
| `l_result` | List:  (car) list of`dbids` of all path figures created or modified  (cadr)`t` if DRCs are created. `nil` if DRCs are not created.
| `nil` | Nothing was created.
#### See Also

#### [axlDBAddProp](#367701 "15")

#### Example

> > `path = axlPathStart( list 100:0 100:500))`

> > `; create path on current default layer`

> > `axlDBCreatePath(path)`

> > `; create a cline path on top etch layer and assisgn to GND`

> > `axlDBCreatePath(path "ETCH/TOP" "gnd")`

> > `;create a line path on top etch layer`

> > `axlDBCreatePath(path "ETCH/TOP" 'line)`

> > `;have user create a two pick path on board geometry outline`

> > `axlDBCreatePath( axlEnterPath() "BOARD GEOMETRY/OUTLINE")`

> > `;create a cline path on top etch layer with properties`

> > `` proplist = list( `(FILLET t) ) ``

> > `axlDBCreatePath(path "ETCH/TOP" "gnd" nil proplist)`

### axlDBCreateLine

```
axlDBCreateLine(l_points[f_width][t_layer][t_netname]/['line][rd_parent][s_font])⇒ l_result/nil
```

#### Description

Create a path of fixed width straight segments, a line with series of provided points. If line is on an ETCH layer a cline will be created unless overridden with the`'line` symbol.

All points are absolute in user units. For <n> points provided, the function creates <n-1> segments.

Allegro restricts the layers that allow fonts. ETCH layers may never have fonted lines.

* The t\_netname option is used as a tie breaker in cases where the cline may want to connect to multiple objects. A cline cannot maintain a net by itself. This connectivity behavioral means if adding multiple clines and vias you must sequence them so that each cline or via is added such that it connects to an object with the desired net already in the database.

  For example, you add 3 clines to drive a connection between 2 pins; where cline 1 and 3 terminate on a pin and cline 2 is in the middle. You should add them as 1 2 then 3. Adding them as 2, 1 and 3 may result in cline 2 being connected to a difference net.

#### Arguments

|  |
| --- | ---
| `l_points` | List of the vertices (at least two) for this path.
| `f_width` | Width for all segments in the path. Default is 0.
| `t_layer` | Layer to which to add the path. Default is the current active layer.
| `t_netname` | Name of the net or`nil`
| `rd_parent` | `dbid` of the object to which to the line is added. Use the symbol instance `dbid`or use `nil` to specify the design itself.
| `s_font` | Optional line font, may have values as`'SOLID`, `'HIDDEN` 'PHANTOM 'DOTTED 'CENTER.  `nil` is the same as 'SOLID
#### Value Returned

|  |
| --- | ---
| `l_result` | List:  (car) list of`dbids` of all paths created or modified  (cadr)`t` if DRCs are created. Otherwise the function returns `nil`.
| `nil` | Nothing is created.
#### See Also

[axlDBCreatePath](#895769 "15")

#### Example

> > ```
> > axlDBCreateLine( (list 1000:1250 2000:2250), 15, "etch/top")    ⇒ ((dbid:122784) t)
> > ```

This example creates a line at width 15 mils from (1000, 1250) to (2000, 2250) on`"etch/top".` The command returns the `dbid` of the line and `t`, indicating that it created DRCs.

### axlDBCreateCircle

`axlDBCreateCircle(l_location[f_width][t_layer][rd_parent])⇒ l_result/nil`

#### Description

Create a circle at indicated location and with indicated diameter.

#### Arguments

|  |
| --- | ---
| `l_location` | Center and radius as (X:Y R).
| `f_width` | Width of circle edge.
| `t_layer` | Layer. Default is the current active layer.
| `rd_parent` | `dbid` of object to add circle to (symbol instance or `nil` for design).
#### Value Returned

|  |
| --- | ---
| `l_result` | List containing:  (`car`) list of circle `dbids`. There is always one `dbid` in the list.  (`cadr`) `t` if any DRCs are created. `nil` if no DRCs are created.
| `nil` | Nothing was created.
#### See Also

[axlDBCreatePath](#895769 "15")

Create Shape Interface
----------------------

You can create shapes using AXL functions as follows:

* To create a simple shape, filled or unfilled, without any voids, first create its boundary path using the`axlPath` functions described earlier. Next, call `axlDBCreateShape` using the path as an argument. `axlDBCreateShape` creates the shape in the database and returns, completing the process.

* To create a shape with voids, first create a shape in "open state" using`axlDBCreateOpenShape`. Next, add voids to the shape as needed using `axlDBCreateVoid` and `axlDBCreateVoidCircle`. Finally, put the shape permanently into the database with `axlDBCreateCloseShape`.

> This final function changes the state of the shape from "open" to "closed," making it a permanent part of the database. Only one shape can be in the "open" state at one time.

You specify both shape and void boundaries with the`r_path` argument, just as you do creating lines and connect lines. `axlDBCreateShape` and `axlDBCreateOpenShape` also check that the following are true:

* All boundary path arguments--shape or void--are closed (equal startPoint endPoint)

* No boundary path segments touch or cross (no "bow ties").

* All void boundaries are completely within the boundary of their parent shape

If you fail to meet one or more of these conditions, the functions do not create the shape or void, and return`nil`*.*

#### Example

* Closes the shape so that it fills and the command does DRC

> ```
> mypath = axlPathStart( list(1000:1250))mypath = axlPathLine( mypath, 0.0, 2000:1250)mypath = axlPathArcCenter(    mypath, 0.0, 2000:3250, nil, 2000:2250)mypath = axlPathLine( mypath, 0.0, 1500:3250)mypath = axlPathLine( mypath, 0.0, 1000:1250)myfill1 = make_axlFill( ?angle 45.0, ?origin 10:20,    ?width 50, ?spacing 80)myfill2 = make_axlFill( ?angle 135.0, ?origin 10:20,    ?width 5, ?spacing 100)myfill = list( myfill1 myfill2)myshape = axlDBCreateOpenShape( mypath, myfill,    "etch/top", "sclkl")if( myshape == axlDBActiveShape()    println( "myshape is the active shape"))axlDBCreateVoidCircle( myshape, list(1600:1700 300))myvoidpath = axlPathStart( list(1600:2300))myvoidpath = axlPathLine( myvoidpath, 0.0, 2400:2100)myvoidpath = axlPathLine( myvoidpath, 0.0, 2600:2700)myvoidpath = axlPathLine( myvoidpath, 0.0, 2100:3000)myvoidpath = axlPathLine( myvoidpath, 0.0, 1600:2300)axlDBCreateVoid(myshape, myvoidpath)axlDBCreateCloseShape( myshape)
> ```

* Creates a closed path

* Creates the fill structures specifying the crosshatch parameters

* Creates the open shape on`"etch/top"` associated with net `"sclkl"` with `axlDBCreateOpenShape`

* Checks that the shape created is the active shape using`axlDBActiveShape` which will print the message

* Creates a circular void and attach it to the shape

* Creates a void shape and attach it to the shape

### axlDBCreateOpenShape

```
axlDBCreateOpenShape(o_polygon/r_path[l_r_fill][t_layer][t_netName/o_netdbid][o_parent])⇒ o_shape/nil
```

#### Description

Creates a shape based on the characteristic of either`o_polygon` or`r_path`. With `r_path`, fills parameters, layer, netname, and parent you specify. Returns the `dbid` of the shape in open state. Open state means you can add and delete voids of the shape. With `o_polygon`, creates a shape with the boundary defined by the boundary of the polygon. The holes in the polygon are added as voids to the shape. (See `axlPolyFromDB`.)

The shape model uses the open/close model for performance reasons. While adding a shape without voids, you can use axlDBCreateShape, which hides the open and close. While adding voids you should do the following:

> `shape = axlDBCreateOpenShape(...)`

> `... add voids ...`

> `axlDBCreateCloseShape(shape).`

You can modify an existing shape by using the axlDBOpenShape command, as follows:

> `axlDBOpenShape(shape <new boundary>)`

> `... add or delete voids ...`

> `axlDBCreateCloseShape(shape).`

Will not allow hole polygons as input. When holes are passed as input, the following warning displays:

`Invalid polygon id argument -<argument>`

A static shape is created if you create shape on class ETCH; dynamic shapes are created if class is BOUNDARY. For example, to create a static shape on the TOP layer, make`t_layer=ETCH/TOP`. To make a dynamic shape, make `t_layer=BOUNDARY/TOP`. The same rule also applies to `axlDBCreateShape`.

fill structure for xhatch shapes is:

|  |
| --- | ---
| l\_fill1 | A fill\_type.
| [l\_fill2] | (optional) A fill\_type. Supplied when more then second xhatch pattern is desired.
| [f\_outlineWidth] | (optional) Width of outline must be greater then or equal to fill width(s). Specified in design units. Default is current board xhatch width. Only supported for`o_polygon` since outline width for `r_path` should be supplied via the `r_path` defstruct.
where fill\_type is a defstruct with members

|  |
| --- | ---
| f\_spacing | spacing between xhatches (design units)
| f\_width | width of xhatch (design units)
| l\_origin | origin of xhatch (absolute to board)
| f\_angle | angle of xhatches
#### Arguments

|  |
| --- | ---
| `o_polygon/r_path` | The outline as an`r_path`from `axlPathXXX` data structure or an `o_polygon` from `axlPolyXXX` interfaces.
| `l_r_fill` | List of fill structures (`r_fill`) for non solid fill shapes or:  `t` → solid fill  `nil` → unfilled
| `t_layer` | Layer name.`nil` uses the default active layer.
| `t_netname` | Name of net. Only allowed for shapes being added to etch layers.
| `o_netdbid` | Can use`DBID` of net instead of the netname. Same restrictions apply as for`t_netname`.
| `o_parent` | `axl``DBID`of the object to add the shape to. Use the symbol instance, or use `nil` to specify the design itself.
#### Value Returned

|  |
| --- | ---
| `o_shape` | `axl``DBID`of the shape*.* AXL-SKILL does not perform DRC on the shape until you close it using `axlDBCreateCloseShape`.
| `nil` | No shape created.
#### Note

An open shape can have voids added to it. It is not DRC checked or filled, until`axlDBCreateCloseShape` is called.

A path starts at`startPoint` and a segment is created for each segment in the `pathList`. If the path does not end at the `startPoint`, it is considered an error.

A list of`o_polygons` is not considered valid input. Only a single `o_polygon` is correct input.

All path segment coordinates are absolute.

Allegro PCB Editor allows only one shape to be in open state at one time.

#### See Also

[axlDBActiveShape](#367559 "15"), [axlDBOpenShape](06intedt.html#832168 "5"), [axlDBCreateVoid](#367581 "15"), [axlShapeDeleteVoids](06intedt.html#823700 "5"), [axlDBCreateCloseShape](#367549 "15"), [axlDBCreateRectangle](#367609 "15"), [axlDBCreateShape](#367593 "15"), [axlDBCreateVoidCircle](#367569 "15"), [axlShapeAutoVoid](06intedt.html#851093 "5"), and axlDBCreateFillet

#### Example

* Create a shape using rpath

`path = axlPathStart( list( 0:0 400:000 600:400 400:600 0:0))`

`shp = axlDBCreateOpenShape(path); defaults to a solid filled shape`

`; unless layer allows unfilled only`

`; This is optional unless you are adding a shape to etch`

`; If you do axlDBCreateShape it automatically closes it for you`

`axlDBCreateCloseShape(car(shp))`

* Create a shape using a poly

`p1 = axlPolyFromDB(inElem)`

`;; add it as an unfilled shape on BOARD GEOMETRY/OUTLINE`

`res = axlDBCreateShape( car(p1) nil "BOARD GEOMETRY/OUTLINE")`

* See examples`axldbctshp.il`.

### axlDBCreateCloseShape

`axlDBCreateCloseShape(o_shape[g_forceShape])⇒ l_result/nil`

#### Description

Closes the current open shape and applies the fill pattern specified in`axlDBCreateOpenShape`. Then performs DRC. If the fill fails, the function returns `nil`.

#### Arguments

|  |
| --- | ---
| `o_shape` | `dbid` of the open shape created by `axlDBCreateOpenShape`.
| `g_forceShape` | By default, Allegro creates a rectangle in its database when an outline is a rectangle. This is for performance and space reasons. To override this behavior, pass the argument value as`t` when closing a shape.
| `r_fill` | Shape can be filled differently then voided. This should only be done with xhatch shapes and should use spacing/width in power of two multiples. We strongly discourage this option. Used in place of g\_forceShape.
#### Value Returned

|  |
| --- | ---
| `l_result` | List:\(`car`) `dbid` of the shape created.  (`cadr`) `t` if DRCs are created.  `nil`if DRCs are not created.
| `nil` | Nothing was created.
#### Example

See[Create Shape Interface](#367513 "15") for an example.

### axlDBActiveShape

`axlDBActiveShape()⇒ o_shape/nil`

#### Description

Returns the`dbid` of the open shape, if any.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `o_shape` | `dbid` of the active shape created by `axlDBCreateOpenShape`*.*
| `nil` | There is no active shape.
#### Example

See[Create Shape Interface](#367513 "15") for an example.

### axlDBCreateVoidCircle

`axlDBCreateVoidCircle(o_shapel_location[f_width])⇒ o_polygon/nil`

#### Description

Creates a circular void in the open shape`o_shape`. Calling this function without an open shape causes an error.

#### Arguments

|  |
| --- | ---
| `o_shape` | `dbid` of the open shape created by `axlDBCreateOpenShape`.
| `l_location` | Center and radius of the circular void to create. The structure of the argument is: (X:Y R).
| `f_width` | Void edge width used by cross-hatch. Default is 0.
#### Value Returned

|  |
| --- | ---
| `o_polygon` | `dbid` of the circular void created.
| `nil` | Error due to calling the function without an open shape. No void is created.
#### Example

See[Create Shape Interface](#367513 "15") for an example.

### axlDBCreateVoid

`axlDBCreateVoid(o_shape/nilr_path/o_polygon)⇒ o_polygon/nil`

#### Description

Adds a void to a shape. To add multiple voids, it is recommended that you either add the voids when creating the shape ([axlDBCreateShape](#367593 "15")) or re-open the shape ([axlDBOpenShape](06intedt.html#832168 "5")) before creating the voids.

Only certain layers, such as ETCH layer, allow voids in a shape. Use[axlOK2Void](07dbaccs.html#719680 "6") to determine if shape supports voids. While adding multiple voids to an etch shape, for best performance, first call [axlDBOpenShape](06intedt.html#832168 "5"), add the voids, and then close the shape ([axlDBCreateCloseShape](#367549 "15")).

Unless you want the void to be permanent, do not add voids to dynamic shapes. User added voids on dynamic shapes must be put on the dynamic shape, with class=BOUNDARY, not on the generated shape, class=ETCH.

#### Arguments

|  |
| --- | ---
| `o_shape` | `dbid` of the open shape. If this value is `nil`, the command uses the open shape
| `r_path` | Existing path structure created by the`axlPath` functions.
#### Value Returned

|  |
| --- | ---
| `o_polygon` | `dbid` of the void created.
| `nil` | Error due to calling the function with no open shape.
#### See Also

[axlDBCreateShape](#367593 "15"), [axlDBOpenShape](06intedt.html#832168 "5"), [axlOK2Void](07dbaccs.html#719680 "6"), [axlDBCreateVoidCircle](#367569 "15")

#### Example

* Create Shape Example

> See[Create Shape Interface](#367513 "15") for an example.

* Add to existing shape

> See`dbc_shp_t10` function in `axldbctshp.il`example code.

### axlDBCreateShape

```
axlDBCreateShape(o_polygon/r_path[l_r_fill][t_layer][t_netName][o_parent])⇒ l_result/nil
```

#### Description

Takes the same arguments as`axlDBCreateOpenShape` and adds the `r_path` shape to the database. The difference is that this function creates the shape and puts it into the closed state immediately, rather than leaving it open for modification. Use `axlDBCreateShape` to add shapes without voids.

`axlDBCreateShape` has the same argument restrictions as `axlDBCreateOpenShape`.

#### ArgumentsZ

|  |
| --- | ---
| `o_polygon/r_path` | Existing path structure created by`axlPath` functions.
| `l_r_fill` | One of three possible values:  `t` → create shape solid filled  `nil` → create shape unfilled  List of structures specifying crosshatch parameters for creating the shape:  (defstruct axlFill:(`r_fill`) - shape crosshatch data  `origin:`a point anywhere on any xhatch line  width:width in user units  `spacing:`spacing in user units  `angle`): angle of the parallel lines  **Note:** As with all SKILL defstructs, use the constructor function `make_axlFill` to create instances of `axlFill`. Use the copy function `copy_``axlFill` to copy instances of `axlFill`.
| `t_layer` | Layer on which to create the shape.
| `t_netName` | Name of the net to which the shape is to belong.
| `o_parent` | `dbid` of the object to be the parent of the shape. The parent is a symbol instance or is `nil` if the design itself.
#### Value Returned

|  |
| --- | ---
| `l_result` | List:  (`car`) `dbid` of the shape created  (`cadr`) `t` if DRCs are created. `nil` if DRCs are not created.
| `nil` | Nothing is created.
#### Example

See[Create Shape Interface](#367513 "15") for an example.

### axlDBCreateRectangle

`axlDBCreateRectangle(l_bBox[g_fill][t_layer][t_netname][o_parent])⇒ l_result/nil`

#### Description

Creates a rectangle with coordinates specified by`l_bBox`. If the rectangle is not created, the function returns `nil`.

If`t_netname`is non-null, the rectangle becomes a member of that net. Ignores `t_netname` if the rectangle is unfilled.

Does not create the rectangle and returns`nil` (error) in these instances:

* Net does not exist.

* Attempt to create a filled rectangle on an Allegro PCB Editor layer requiring an unfilled rectangle.

* Attempt to create an unfilled rectangle on an Allegro PCB Editor layer requiring a filled rectangle.

See[axlDBCreateSymbolSkeleton](#439990 "15") for notes about restrictions on shapes that are part of symbol definitions.

#### Arguments

|  |
| --- | ---
| `l_bBox` | Bounding box of the rectangle: Lower left and upper right corners of rectangle
| `g_fill` | If`t` then the fill is solid. If `nil` (default) then the rectangle is unfilled. It may have optional line font, with possible values as 'SOLID 'HIDDEN 'PHANTOM 'DOTTED 'CENTER. Line fonts can only be used with unfilled shapes.Only certain Allegro layers support fonted unfilled shapes.
| `t_layer` | Layer to which to add the rectangle. Default is the active layer.
| `t_netname` | Name of net to which the rectangle is to belong. This argument is meaningful only if the rectangle is being added on an Etch layer.
| `o_parent` | `dbid` of object of which the rectangle is to be a part. Use either the `dbid` of a symbol instance or use `nil` to specify the design itself.
#### Value Returned

|  |
| --- | ---
| `l_result` | List:  (`car`) rectangle `dbid`  (`cadr`) `t` if DRCs are created. `nil`if DRCs are not created.
| `nil` | Nothing is created.
#### Example

* Unfilled shape indicated layer

> `axlDBCreateRectangle(list(100:100 200:200) nil "BOARD GEOMETRY/OUTLINE")`

* Filled shape on active layer

> `axlDBCreateRectangle(list(200:200 400:300) t)`

* Filled shape on ETCH/TOP assigned to NET\_1 using user supplied picks

> `axlDBCreateRectangle( axlEnterBox() t "ETCH/TOP" "GND")`

* Fonted dotted line shape on indicated layer

> `axlDBCreateRectangle(list(400:100 500:300) 'DOTTED "BOARD GEOMETRY/OUTLINE" )`

Nonpath DBCreate Functions
--------------------------

This section describes the`DBCreate` functions that add nonpath figures to the Allegro PCB Editor database.

### axlCreateBondFinger

```
axlCreateBondFinger(parentSymbolfingerNamelist(fingerLocation fingerRotation fingerPadstack)list(placementStyle ewlLength fingerSnap fingerAlign))==> dbid/nil
```

#### Description

This function adds a valid, fully-instantiated bond finger to the database. Bond fingers created through this interface can be safely manipulated by the wirebond toolset and will also be properly recognized by all aspects of the database (DRC, signal integrity, 3D viewer, and so on).

#### Arguments

* dbid of the symbol (generally a die) with which this finger should be associated when performing operations like a move or delete.
* The optional parameter that specifies the name of the bond finger, as stored in the BOND\_PAD property.
* The physical information about the bond finger being creation, the location is a database coordinate point, the rotation and angle in degrees, and the padstack the dbid of a padstack to use.
* The placement data for the bond finger being created, as follows:
* Free Placement
* Orthogonal
* Equal Wire Length
* On Path
* Length value for Equal Wire Length style, which represents the desired length of the wire.
* Farthest Point
* Center of Finger
* Finger Origin
* Near End
* Far End
* Nearest Point
* Match CCW Neighbor
* Aligned with Wire
* Orthogonal to Die Side
* Orthogonal to Guide
* Pivoting Ortho to Guide
* Average Wire Angle
* Constant Angle
* Match CW Neighbor

#### Value Returned

* `dbid` of newly created bond finger if successful.

* `nil` if an error occurred (message printed to status window).

### axlCreateBondWire

```
axlCreateBondWire(parentSymbollist(wireStartOwner wireStartLocation)list(wireEndOwner wireEndLocation)list(wireDiameter wireProfile))==>dbidt/nil
```

#### Description

This function adds a valid, fully-instantiated bond wire to the database. Bond wires created through this interface can be safely manipulated by the wirebond toolset and will also be properly recognized by all aspects of the database (DRC, signal integrity, 3D viewer, etc).

#### Arguments

|  |
| --- | ---
|  |
| parentSymbol | dbid of the symbol (generally a die) with which this wire should be associated when performing operations like a move or delete.
| wireStartOwner/Location | Optional.  This is a list with the first item being, the dbid of the object to which the start of the wire attaches. If this object is a pin or finger, the location will be derived from the object's origin. If the object is a shape, you must pass the location for the connection as well.
| wireEndOwner/Location | - This is a list with the first item being, the dbid of the object to which the end of the wire attaches. If this object is a pin or finger, the location will be derived from the object's origin. If the object is a shape, you must pass the location for the connection as well.
| wireDiameter/Profile | - This list of two items describes the physical placement of the wire in terms of its 3D profile (a string) and the wire diameter (a number).
|  |
#### Value Returned

* dbid of newly created bond wire if successful.

* nil if an error occurred (message printed to status window).

### axlDBCreateExternalDRC

```
axlDBCreateExternalDRC(t_constraint/lt_constraintl_anchor_point[t_layer][lo_dbid][l_secondPoint][t_actualValue])⇒ l_result/nil
```

#### Description

Creates an externally-defined (by user) DRC containing the values given in the arguments. An externally defined DRC marker always has the two characters "X D" in it.

You may pass the constraint as the traditional argument (`t_constraint`) where this contains both the constraint and expected value in a one string. The downside of this method is that the `show element` and `reports` commands report 0 for the exepctValue. Alternatively, you can pass it as a list containing two strings: constraint name and expected value. This format reports properly in both the `show element` and `reports` commands.

The`t_actualValue` argument is optional and provides an externally-defined actual value with the DRC in design units.

In show element:

|  |  |
| --- | --- | ---
| **Skill Item** | **Show Element** | **Comments**
| l\_anchorPoint | Origin xy | Required Value
| t\_constraint | Constraint set | Required Value
| t\_type | Constraint Type | default "EXTERNAL REFERENCE"
| t\_expectValue | Constraint value | default "None"
| t\_actualValue | Actual Value | default "None"
Property mapping

|  |
| --- | ---
| t\_expectValue | EXTERNAL\_DRC\_VALUE
**Note:** Attempting to create a DRC object on a non-DRC class is an error.You can use this function in the layout editor, but not in the symbol editor.

* `t_type` can be used to group similar DRCs. You might give all of your company written DRC checks your company name.

#### Arguments

|  |
| --- | ---
| `t_constraint` | Name of the violated constraint. String contains the type of constraint and the required value and comparison.
| `lt_constraint` | Alternative method. It is a list of (t\_constraint t\_expectValue)
| `l_anchor_point` | Coordinate of the DRC marker.
| `t_layer` | Layer of the DRC marker. This must either include the "drc error class" or just the subclass name.
| `lo_dbid` | Optional list of the objects that caused the DRC (maximum of two).
| `l_secondPoint` | Second reference point. This is a coordinate on the object of the DRC pair that does not have the DRC marker on it. Using this point, you can identify the second object involved in causing the DRC by reading the DRC data in later processes.
| `t_actualValue` | Actual value that caused the DRC.
#### Value Returned

|  |
| --- | ---
| `l_result` | List:  (car)`dbid` of the DRC created (always only one)  (cadr)`t` (always)
| `nil` | Nothing is created.
#### Example

Creates a user defined DRC marker at x,y (1500, 1800) to mark a violation of user rule:`"Line to Pin--MY SPACING RULE"`with a required value of 12 and an actual value of 10.

* Original method:

> > ```
> > axlDBCreateExternalDRC( "Line to Pin--MY SPACING RULE/    req:12; actual:10", 1500:1800    "drc error/all", nil, nil, "10 MILS")
> > ```

* New method for better`show element` and `reports` command behavior:

`axlDBCreateExternalDRC('("My Spacing Line to Pin" "12")`

`1500:1900 "top", nil nil "10 MILS")`

* Name classifiction

```
axlDBCreateExternalDRC('("My Spacing Line to Pin" "12" "Cadence")1500:2000 "top", nil nil "10 MILS")
```

Adds "X D" DRC markers at (1500 1800) and (1500 1900).

The DRC marker displays the following information with the*Show - Element* command:

> > `LISTING: 1 element(s)`

> > `< DRC ERROR >`

> > `Class: DRC ERROR CLASS`

> > `Subclass: ALL`

> > `Origin xy: (1500,1800)`

> > `CONSTRAINT: Externally Determined Violation`

> > `CONSTRAINT SET: NONE`

> > `CONSTRAINT TYPE: LAYOUT`

> > `Constraint value: 0 MIL`

> > `Actual value: 10 MILS`

> > `Properties attached to drc error`

> > ```
> > EXTERNAL_VIOLATION_DESCRIPTION = Line to Pin--MY SPACING    RULE/req:12; actual:10
> > ```

> > `- - - - - - - - - - - - - - - - - - - -`

### axlDBCreatePin

```
axlDBCreatePin(t_padstack/o_padstackDbidl_anchorPointr_pinText/nil[f_rotation])⇒ l_result/nil
```

#### Description

Adds a pin with padstack`t_padstack`, pin name `r_pinText` at location `l_anchorPoint`, and rotated by `f_rotation` degrees.

> **Notes:**

> 1) This interface may only be used in the Symbol Editor.

> 2) Use`axlDBCreatePin` only in package and mechanical symbol drawings. Creating a pin in any other type of drawing causes errors.

> 3) Use`nil` for `r_pinText` to create a mechanical pin.

#### Arguments

|  |
| --- | ---
| `t_padstack` | Padstack name for the via. If a padstack definition with this name is not already in the layout, the function searches in order the libraries specified by`PADPATH` and loads the definition into the database.
| `o_padstackDbid` | a padstack dbid
| `l_anchorPoint` | Layout coordinates of the location to add the pin.
| `r_pinText` | Pin number text structure:    `(defstruct axlPinText ;(r_pinText) - pin number text data`  `number ;pin number as a text string`  `offset ;offset (X:Y) for pin number text`  `text) ;axlTextOrientation - ;for positioning text`  This requires the axlTextOrientation structure:  `defstruct axlTextOrientation`  `;(r_textOrientation) - description of the orientation of text textBlock`  `;string - text block name`  `rotation ;rotation in floatnum degrees`  `mirrored ;t-->mirrored, nil --> not mirrored`    `` ;`GEOMETRY --> only geometry is mirrored ``  `justify) ;"left", "center", "right"`    **Note:** As with all SKILL defstructs, use constructor functions`make_axlPinText` to create instances of `axlPinText` and `make_axlTextOrientation` for `axlTextOrientation`.  See[Create Shape Interface](#367513 "15") for an example. Use copy functions `copy_axlPinText` to copy instances of `axlPinText` and `copy_axlTextOrientation` for `axlTextOrientation`.
| `f_rotation` | Rotation of pin in degrees.
#### Value Returned

|  |
| --- | ---
| `l_result` | List:  (`car`) `dbid` of the pin  (`cadr`) `t` if DRCs are created. `nil`if DRCs are not created.
| `nil` | Nothing is created.
#### Example

* The following example adds pins "1", "2", "3", and a mechanical to a package symbol drawing. Pin "1" with a square pad is rotated 45 degrees, pins "2" and "3" with round pads, and pin "3" with its pin text mirrored.

`mytext = make_axlTextOrientation(`

`?textBlock 6, ?rotation 60.0`

`?mirrored nil ?justify "center")`

`mypin = make_axlPinText(?number "1",`

`?offset 0:75, ?text mytext)`

`axlDBCreatePin( "pad1" 0:0 mypin 45.0)`

`mytext->justify = "left"`

`mytext->rotation = 0.0`

`mypin->number = 2`

`mypin->offset = -125:0`

`axlDBCreatePin( "pad0" -100:-100 mypin)`

`mytext->rotation = -45.0`

`mytext->justify = "right"`

`mytext->mirror = t`

`mypin->number = 3`

`mypin->offset = 50:0`

`axlDBCreatePin( "pad0" 100:-100 mypin)`

`mypin->mytext = nil`

`axlDBCreatePin( "pad0" 100:100 mypin)`

Adds the three pins in the positions shown:

* 2) Create 8 pins using a loop

> `x=1000.0`

> `y=1000.0`

> `myText = make_axlTextOrientation(?textBlock 6`

> `?justify "center")`

> `myPin= make_axlPinText(?offset 0:0 ?text myText)`

> `for(i 1 8`

> `y=y-100`

> `sprintf(buf "a%d" i)`

> `myPin->number = buf`

> `axlDBCreatePin("VIA" x:y myPin)`

> `)`

> `)`

### axlDBCreateSymbol

```
axlDBCreateSymbol(t_refdesl_anchorPoint[g_mirror][f_rotation][t_embeddedLayer])⇒ l_result/nil
```

```
axlDBCreateSymbol(l_symbolDatal_anchorPoint[g_mirror][f_rotation][t_embeddedLayer])⇒ l_result/nil
```

#### Description

Places a symbol instance in the design. Creates a symbol instance at location`l_anchor_point` with the given mirror and rotation. Examines its first argument to determine what symbol to add, as explained later. Next, searches for the symbol in the symbol definitions, first in the layout, then in the `PSMPATH`. Loads the definition if it is not already in the layout and creates the symbol instance. Returns `nil` a symbol definition is not found.

**Note:** Do not use this function in the symbol editor.

#### Arguments

The first argument can be either`t_refdes` or `l_symbolData`, as described here:

|  |
| --- | ---
| `t_refdes` | Reference designator of the component. If this is the first argument, the function looks for a component in the layout with that refdes, finds the package symbol required for its component device type, adds a package symbol with the symbol name prescribed by the component definition, and assigns that refdes to the symbol (example, refdes U1 requires a`DIP14` package symbol). Returns `nil` if it cannot find the given refdes.
| `l_symbolData` | If this is the first argument, the function looks for the symbol, symbol type, and refdes specified by this structure.  l`_symbolData` is a list (t\_symbolName [[`t_symbolType` [`t_refdes`]]), where:  `t_symbolName` is the name of the symbol (example: `DIP14`)  `t_symbolType` is a symbol type: `"PACKAGE"` (default),`"MECHANICAL"` or `"FORMAT"`  `t_refdes` is an optional refdes; if `t_refdes` is present,  `t_symbolType` must be `"PACKAGE"`.  An example is the list: ("`DIP16`" "`package`" "`U6`")  To create a component with an alternate symbol, that is, a symbol different from the one specified in the component library, use the`l_symbolData` structure. For example, refdes `C7` might be a capacitor requiring the top-mount package "`CAP1206F`". However, your design requires the alternative package "`CAP1206B`" on the bottom side of the layout.  To create the component mirrored, use`axlDBCreateSymbol` with the `l_symbolData` argument:  `"CAP1206B" "package" "C7")`
| `t_refdes` | Reference designator of the component associated with the  symbol to be created.
| `l_symbolData` | List (`t_symbolName` [[`t_symbolType` [`t_refdes`]]). (See  example above.)
| `l_anchorPoint` | Layout coordinates specifying where to create the symbol.
| `g_mirror` | `nil` - create unmirrored. (default)  `t` - create symbol mirrored.  `` `GEOMETRY `` - geometry is mirrored.
| `f_rotation` | Rotation of the symbol in degrees.(default is 0)
| `t_embeddedLayer` | Place on embedded layer. Layer must be enabled for embedded.  Mirror option is ignored. Layer may either be fully qualified  ("ETCH/GND") or just the subclass ("GND"). May not use the top  or bottom layer.
#### Value Returned

|  |
| --- | ---
| `nil` | Nothing is created.
| `l_result` | a list containing:  (`car`) axl `DBID` of the symbol created  (`cadr`) `t` if DRCs are created. `nil` if DRCs are not created.
**Note:** The symbol definition in the drawing is used. If there is none in the drawing, then the symbol library is searched and the definition loaded.

#### Example

> `axlDBCreateSymbol("y29", 5600:4600)    ⇒(dbid:423143 nil)`

Creates a symbol with the assigned refdes.

> `axlDBCreateSymbol( list( "dip14" "package"), 5600:4600)    ⇒(dbid:423144 nil)`

Creates a symbol with the unassigned refdes, just the generic U\*:

* Typical component driven symbol placement:

> `p = axlDBCreateSymbol("U1" 2175:1000)`

* Place an embedded component. Assumes a layer, SIGNAL\_2 is enabled for embedded.

> `p = axlDBCreateSymbol("R1" 2175:1000 nil nil "SIGNAL_2")`

* Place non-logical package symbol with rotation of 90

> `p = axlDBCreateSymbol('("R_0402" "PACKAGE") 2000:800.1 nil 90.0)`

### axlDBCreateSymbolSkeleton

```
axlDBCreateSymbolSkeleton(t_refdesl_anchorPointg_mirrorf_rotationl_pinData[t_embeddedLayer])⇒ l_result/nil
```

or

```
axlDBCreateSymbolSkeleton(l_symbolDatal_anchorPointg_mirrorf_rotationl_pinData[t_embeddedLayer])⇒ l_result/nil
```

#### Description

Places a skeleton or a minimal symbol instance at`l_anchorPoint` with mirror and rotation given but no data in the instance, except the pin data given by `l_pinData`. This is a list of `axlPinData` defstructs defining the data for all pins. The pin count and pin numbers must match that of the library symbol definition. The symbol definition must exist in the database or on `LIBPATH`.

Behaves like`axlDBCreateSymbol`, except that it adds no symbol data except the symbol pins in the instance. Use to create the "foundation" of a symbol. Then build, using `axlDBCreate` functions to add lines, shapes, polygons, and text as required.

Use, for example, to construct symbols when translated from other CAD systems that define symbol instances in different ways than Allegro PCB Editor.

AXL-SKILL applies each`axlPinData` instance in `l_pinData` only to the pin specified by its *number*. (See the description of the `l_pinData` argument below.) A `nil` value for `l_pinData` means `axlDBCreateSkeleton` adds the pins as they are in the library definition of the symbol. You can selectively customize none, one, or any number of the pins of the symbol instance you create.

