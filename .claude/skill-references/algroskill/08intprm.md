### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

7
=

Allegro PCB Editor Interface Functions
======================================

Overview
--------

This chapter describes the AXL/SKILL functions that give access to the Allegro PCB Editor interface. These include display control, cursor setup, and soliciting user input, such as text and mouse picks.

AXL-SKILL Interface Function Examples
-------------------------------------

This section gives examples of the following:

* Dynamic cursor functions used with the`axlEnter` functions

* `axlCancelEnterFun` and `axlFinishEnterFun` used with the popup functions in a command looping on the `axlEnterPath` command

* `axlHighlightObject` and `axlDehighlightObject`

#### Dynamic Cursor Examples

You use the AXL-SKILL dynamic cursor functions to build up and display Allegro PCB Editor database objects during interactive commands. Using dynamic cursor shows the effects of a command in use. For example, you can display a symbol and the etch lines connected to it, constantly showing where they would be in the drawing if the user clicked at their current position.

The two examples that follow show how to set up the dynamic cursor:

* A package symbol image with pins connected to other etch, with rubberband lines from its connected pins to the points where they had originally connected

* A package symbol image dynamically rotating enabling you to select an angle of rotation

Both examples use the`axlPath` functions described in [Chapter 15, "Database Create Functions,"](03dbcre8.html#854400 "15") and the`axlAddSimpleXXXDynamics` functions described in this chapter.

#### Example 1: Dynamic Rubberband

This example loads two circular pads and, the outline of a resistor, and rubberband connections from its pins, one with a "path" rubberband, the other a "directline" rubberband into the dynamic cursor buffer.

> `axlClearDynamics() ; Create cross markers to show rubberband origins:`

> `axlDBCreateLine(list(9150:4450 9050:4550) 0.`

> `"board geometry/dimension")`

> `axlDBCreateLine(list(9150:4550 9050:4450) 0.`

> `"board geometry/dimension")`

> `axlDBCreateLine(list(8550:4450 8450:4550) 0.`

> `"board geometry/dimension")`

> `axlDBCreateLine(list(8550:4550 8450:4450) 0.`

> `"board geometry/dimension")`

> `mypath = axlPathStart(list( -350:0)) ; Start circular pad`

> `axlPathArcCenter(mypath, 0., -350:0, nil, -300:0)`

> `; Load the first pad into the dynamic cursor buffer`

> `axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)`

> `mypath = axlPathStart(list( 350:0)) ; Start circular pad`

> `axlPathArcCenter(mypath, 0., 350:0, nil, 300:0)`

> `; Load the other pad into the dynamic cursor buffer`

> `axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)`

> `mypath = axlPathStart( ; Start resistor body outline`

> `list( -200:-100 200:-100 200:100 -200:100 -200:-100))`

> `; Load the resistor body outline in the dynamic cursor buf`

> `axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)`

> `; Load a "path" rubberband to the first pad`

> `axlAddSimpleRbandDynamics(8500:4500 "path"`

> `?origin 8500:4500 ?var_point -300:0)`

> `; Load a "directline" rubberband to the second pad`

> `axlAddSimpleRbandDynamics(9100:4500 "directline"`

> `?origin 9100:4500 ?var_point 300:0)`

> `;`

> `mypoint = axlEnterPoint() ; Ask user for point`

Loads two circular pads, the outline of a resistor, and rubberband connections from its pins
(one with a`"path"` rubberband, the other a `"directline"` rubberband) into the dynamic cursor buffer.

The following illustration shows the cursor in a typical position as`axlEnterPoint` waits for selection of a point.

#### Example 2: Dynamic Cursor Rotation

> > ```
> > axlClearDynamics() ; Clean out any existing cursor datamypath = axlPathStart(list( -350:0)) ; Start circular padaxlPathArcCenter(mypath, 0., -350:0, nil, -300:0); Load the first pad into the dynamic cursor bufferaxlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)mypath = axlPathStart(list( 350:0)) ; Start circular padaxlPathArcCenter(mypath, 0., 350:0, nil, 300:0); Load the other pad into the dynamic cursor bufferaxlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)mypath = axlPathStart( ; Start resistor body outline    list( -200:-100 200:-100 200:100 -200:100 -200:-100)); Load the resistor body outline in the dynamic cursor bufaxlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0); Ask user to pick angle of rotation about (8500:4500):axlEnterAngle(8500:4500)
> > ```

Loads two circular pads, the outline of a resistor, and rubberband connections from its pins, one with a "path" rubberband, the other a "directline" rubberband into the dynamic cursor buffer.

The following illustration shows the dynamically rotating cursor in a typical position as`axlEnterAngle` waits for a user-selected point.

#### Enter Function Example

You use the AXL-SKILL`axlCancelEnterFun` and `axlFinishEnterFun` functions when you create an interactive command that loops on input, providing the option to end the command.

```
(defun axlMyCancel ()    axlClearDynamics()    axlCancelEnterFun()    axlUIPopupSet(nil))(defun axlMyDone ()    axlClearDynamics()    axlFinishEnterFun()    axlUIPopupSet(nil))mypopup = axlUIPopupDefine( nil    (list (list "MyCancel" 'axlMyCancel)    (list "MyDone" 'axlMyDone)))axlUIPopupSet( mypopup); Clear the dynamic bufferaxlClearDynamics(); Clear mypath to nil, then loop gathering user picks:mypath = nilwhile( (mypath = axlEnterPath(?lastPath mypath))    progn(        axlDBCreatePath(mypath, "etch/top")))
```

The Enter Function example does the following:

* Defines the functions`axlMyCancel` and `axlMyDone`.

* Defines a pop-up with those functions as the callbacks for user selections*Cancel* and *Done* from the pop-up.

* Loops on the function`axlEnterPath` gathering user input to create a multi-segment line on `"etch/top".`

Selecting*Cancel* or *Done* from the pop-up ends the command.

You gather one user-selected point and extend the database path by that selection each time through thewhile loop. Selecting Done from the pop-up terminates the loop. Selecting Cancel at any time cancels. Segments added become permanent in the database when the loop ends.

#### axlHighlightObject and axlDehighlightObject Examples

You use the AXL-SKILL`axlHighlightObject` and `axlDehighlightObject` functions to highlight database elements during interactive commands.

**Example 1**

> > ```
> > (defun highlightLoop ()mypopup = axlUIPopupDefine( nil        (list (list "Done" 'axlFinishEnterFun)             (list "Cancel" 'axlCancelEnterFun)))axlUIPopupSet( mypopup)axlSetFindFilter( ?enabled '("noall" "alltypes" "nameform")                    ?onButtons "alltypes")    (while (axlSelect)        progn(             axlHighlightObject( axlGetSelSet())            ; Just a dummy delay to see what happens            sum = 0            for( i 1 10000 sum = sum + i)            axlDehighlightObject( axlGetSelSet())))
> > ```

Example 1 does the following:

* Defines the function`highlightLoop`*.*

* Defines a popup with`axlFinishEnterFun` and `axlCancelEnterFun` as the callbacks for user selections Done and Cancel from the pop-up.

* Loops on the function`axlSelect` gathering user selections to highlight.

* Waits in a simple delay loop, then dehighlights.

Selecting*Cancel* or *Done* from the pop-up ends the command.

**Example 2**

> > `axlDBControl('highlightColor 4)`

> > `axlHighlightObject(axlGetSelSet() t)`

Permanently highlights an object using color`4`.

Allegro PCB Editor Interface Functions
--------------------------------------

This section lists Allegro PCB Editor interface functions.

### axlClearDynamics

`axlClearDynamics()⇒ t`

#### Description

Clears the dynamic cursor buffer. Call this function each time before you start setting up rubberband and dynamic cursor graphics.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

See dynamic cursor examples in the section[AXL-SKILL Interface Function Examples](#571950 "7").

### axlAddSimpleRbandDynamics

```
axlAddSimpleRbandDynamics(l_fixed_pointt_type?origin            l_origin?var_point            l_var_point?lastPath            l_lastPath?width            f_width?color            g_color)⇒ t/nil
```

#### Description

Loads rubber band dynamics buffer with an element. If dynamics buffer is already loaded, the new element is simply added to the existing buffer. Dynamics buffer is not cleared until[axlClearDynamics](#627949 "7") is called.

Rubber band dynamics means stretching of elements to the cursor from an anchor point called the fixed\_point.

* ***This works in conjunction with the axl<Event> APIs. In particular, no grid snapping, only works when these APIs are called. Do not use this in the axlUIWTimerAdd or with axlTriggerSet callbacks.***

#### Arguments

|  |
| --- | ---
| `l_fixed_point` | Fixed point of rubber band. Anchor point from which the dynamic rubberband stretches. The rubberband cursor stretches dynamically from`fixed_point` to current position of the cursor, as moved by the user. The next argument, `type`, specifies the shape of the rubberband--part of a path, direct, z-line (a combination of horizontal and vertical), arc, circle, or box.
| `t_type` | String specifying type of dynamic rubberband to be drawn. Can be one of the following:`path, directline, horizline, vertline, arc, circle, or box`.  `directline`: add a single line to buffer between `fixed_point` and `var_point`.  origin and variable point of var\_point  `horizline`: A single horizontal line.  `vertline`: A single vertical line  `arc`: Arc between fixed\_point and var\_point. Radius varies as cursor moves  "circle": Circle, fixed\_point is center and var\_point is initial radius.  "box": Add a box, fixed point is one corner and the var\_point is the opposite corner.  "path": Add two segments whose behavior is controlled by the line lock attributes (axlSetLineLock).  "fixedline": Adds a constant line to cursor buffer, fixed\_point and var\_point are the two endpoints.
| `l_origin` | Cursor origin. Useful only if you plan on rotating the object, this is the center of its rotation. Also on arcs to control tangency. In most cases this should be nil.
| `l_var_point` | Variable point for rubberbanding.
| `l_lastPath` | Previous path structure. Needed to calculate tangent point if rubberbanding starts at the end of an existing path.
| `f_width` | Optional database width of the rband. Default is 0.0.
| `g_color` | Optional arg for defining the dynamics' color. Possible choices are:
|  |  |
| --- | --- | ---
|  |  | A layer string (i.e. class/subclass) for the layer to be used for deriving the color.
|  |  |
| --- | --- | ---
|  |  | 'ratsnestColor - the color used for ratsnest lines will be used.
|  |  |
| --- | --- | ---
|  |  | 'activeSubclassColor - the color for the active class/subclass is used. If this changes, the color for this rband also changes.
#### Value Returned

|  |
| --- | ---
| `t` | Successfully added data.
| `nil` | No data added.
#### Example

A file, demo\_dynamics.il, in`<cdsroot>``/share/pcb/examples/skill` demonstrates the various t\_type options.

This example loads two circular pad and, the outline of a resistor, and rubberband connections from its pins, one with a "path" rubberband, the other a "directline" rubberband into the dynamic cursor buffer:

> `axlClearDynamics() ; Clean out any existing cursor data`

> `mypath = axlPathStart(list( -350:0)) ; Start circular pad`

> `axlPathArcCenter(mypath, 0., -350:0, nil, -300:0)`

> `; Load the first pad into the dynamic cursor buffer`

> `axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)`

> `mypath = axlPathStart(list( 350:0)) ; Start circular pad`

> `axlPathArcCenter(mypath, 0., 350:0, nil, 300:0)`

> `; Load the other pad into the dynamic cursor buffer`

> `axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)`

> `mypath = axlPathStart( ; Start resistor body outline`

> `list( -200:-100 200:-100 200:100 -200:100 -200:-100))`

> `; Loads the resistor body outline in the dynamic cursor buffer`

> `axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)`

> `; Ask user to pick angle of rotation about (8500:4500):`

> `axlEnterAngle(8500:4500)`

See dynamic cursor examples in the section[AXL-SKILL Interface Function Examples](#571950 "7").

#### See Also

[axlEnterPoint](#572013 "7"), [axlEnterEvent](#616446 "7")

### axlAddSimpleMoveDynamics

```
axlAddSimpleMoveDynamics(l_originr_patht_type?ref_point l_ref_point?color g_color)⇒ t/nil
```

#### Description

Loads cursor buffer dynamics buffer with an element. If dynamics buffer is already loaded, the new element is simply added to the existing buffer. Dynamics buffer is not cleared until[axlClearDynamics](#627949 "7") is called.

Cursor buffer dynamics means no stretching of elements. The loaded is attached to the cursor and moves with it.

#### Arguments

* Cursor origin. (see[axlAddSimpleRbandDynamics](#600852 "7"))
* Path structure containing display objects.
* String specifying type of path: either`path` or `box`. Note that lines and arcs are represented as path. Circle is a special case of arc where the start, end points are the same.
* Element rotation reference point.
* `'activeLayerColor` - the color for the active class/subclass is used. If this changes, the color for this rband also changes.
* A layer string (class/subclass) for the layer to be used for deriving the color.
* `'ratsnestColor` - the color used for ratsnest lines will be used.

#### Value Returned

|  |
| --- | ---
| `t` | Returned if the data is successfully added.
| `nil` | No data added.
#### Example

See dynamic cursor examples,[Example 1: Dynamic Rubberband](#575257 "7") and [Example 2: Dynamic Cursor Rotation](#575270 "7"), in the section [AXL-SKILL Interface Function Examples](#571950 "7").

### axlDesignFlip

`axlDesignFlip(g_flip) t/nil`

#### Description

Visually flips the design in the 'y' axis. Maintains current xy view.

**Note:** This command not available if OpenGL is disabled.

#### Arguments

|  |
| --- | ---
| t | flipped on y axis
| nil | unflip
#### Value Returned

Old flip state. If t flipped (y) if nil normal top view state

#### See Also

[axlWindowFit](#643396 "7")

#### Example

Syntax to implement toggle flipping

`axlDesignFlip( !axlDesignFlip())`

### axlEnterPoint

```
axlEnterPoint(?prompts            l_prompts?points             l_points?gridSnap             g_gridSnap)⇒ l_point/nil
```

#### Description

Prompts for and receives user-selected point. Returns the point data to the calling function.

#### Arguments

|  |
| --- | ---
| `l_prompts` | List containing one prompt message to display.
| `l_points` | List of points. Returns one of these as the return value.  `l_point's`only use is, if passed a point, to immediately return with the point snapped to the nearest grid.
| `g_gridSnap` | Flag to function:`t` means snap the point according to the current grid.
#### Value Returned

|  |
| --- | ---
| `l_point` | List of coordinates, if entered. If selected, this is a list of one point.
| `nil` | User did not select a point.
#### Example

See Example 1 in the section[AXL-SKILL Interface Function Examples](#571950 "7").

#### See Also

[axlGetLastEnterPoint](06intedt.html#861744 "5"), [axlEnterEvent](#616446 "7")

### axlEnterString

`axlEnterString(?prompts            l_prompts)⇒ t_string/nil`

#### Description

Displays a dialog box that requires first entering a string, and then pressing*Return* on the keyboard or clicking *OK*or *Cancel.* Default prompt in the dialog box is `"Enter String."`You can supply a prompt string with the `?prompts` keyword. The function returns the string entered, if any. Otherwise it returns `nil`.

**Note:** This function is a blocker. Allegro PCB Editor will not respond to any user input until the data requested by the dialog box is provided.

#### Arguments

|  |
| --- | ---
| `l_prompts` | List containing one prompt message. Displays only the first string if the list contains more than one string.
#### Value Returned

|  |
| --- | ---
| `t_string` | String entered.
| `nil` | No string entered, dialog box dismissed by clicking*Cancel*, or the command failed.
#### Example

> `user_name = axlEnterString(            ?prompts list("Please enter your name:"))`

> `⇒ "user name"`

Prompts for name and collects the response in`user_name`.

Typing the name, then pressing the*Return* key returns the string entered:

### axlEnterAngle

```
axlEnterAngle(origin?prompts            l_prompts?refPoint            l_refPoint?angle            f_angle?lockAngle            g_lockAngle)⇒ f_angle/nil
```

#### Description

Optionally prompts the user. Returns the angle value entered.

#### Arguments

|  |
| --- | ---
| `origin` | Fixed point where two lines making up the angle meet.
| `l_prompts` | List containing one prompt message.
| `l_refPoint` | End point of a line from the`origin` that acts as the fixed line of the angle.
| `f_angle` | Angle value in. If non-`nil`, does not prompt for a user-selected point.
| `g_lockAngle` | Initial lock angle for dynamic rotation.
#### Value Returned

|  |
| --- | ---
| `f_angle` | Selected angle expressed in degrees.
| `nil` | No angle selected.
#### Example

See Example 1 in the section[AXL-SKILL Interface Function Examples](#571950 "7").

### axlCancelEnterFun

`axlCancelEnterFun()⇒ t/nil`

#### Description

Terminates the wait for a user-selected point. Waiting function returns no data.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | Terminates wait for user-selected point. Cancel succeeds.
| `nil` | Fails to terminate wait for user-selected point.
#### Example

See the[Enter Function Example](#575281 "7").

### axlFinishEnterFun

`axlFinishEnterFun()⇒ t/nil`

#### Description

Terminates the wait for a user-selected point. Waiting function returns no data. For a
one-point function (for example,`axlEnterPoint`) behaves the same as `axlCancelEnterFun`.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | Terminates wait for a user-selected point.
| `nil` | Fails to terminate wait for a user-selected point.
#### Example

See the[Enter Function Example](#575281 "7").

### axlGetDynamicsSegs

`axlGetDynamicsSegs(l_point1l_point2r_lastPath/nil) ->`

#### Description

Normally used with dynamics to calculate arc tangency of two picks to a current`r_path`. Passed coordinates may be modified to preserve tangency. Depends on the current line lock state that you set or `axlSetLineLock`.

#### Arguments

|  |
| --- | ---
| `point1` | First pick before dynamics started.
| `point2` | Second pick, after dynamics completes.
| `lastPath` | Previous path to use for tangency calculations. Can pass`nil` if not applicable.
#### Value Returned

`l_pointList`

`nil`

#### See Also

[axlAddSimpleRbandDynamics](#600852 "7"), [axlMakeDynamicsPath](#617484 "7"), [axlSetLineLock](19cmdctl.html#954384 "20")

#### Example

> `q = axlGetDynamicsSegs(10:10 100:100 nil)`

> `-> (((10.0 10.0) (100.0 100.0) nil))`

### axlGetLineLock

`axlGetLineLock(s_name[g_value])==> g_currentValue/ls_names`

#### Description

Gets the current settings of the line lock or dynamic control options. Equivalent items is the option control panel for "add" commands. Items currently supported:

* Name: arcEnable
  Value: t/nil
  Description: If t Lock Mode is arc, nil is line.

* Name: lockAngle
  Value: 0, 45, 90
  Description: In degrees where 0 is off (no lock).

* Name: minRadius
  Value: float
  Description: Minimum Radius in user units.

* Name: length45
  Value: float
  Description: Fixed 45 Length value in user units.

* Name: fixed45
  Value: t/nil
  Description: If t Fixed 45 length is enabled.

* Name: lengthRadius
  Value: float
  Description: Fixed radius value in user units.

* Name: fixedRadius
  Value: t/nil
  Description: If t in Fixed Radius mode

* Name: lockTangent
  Value: t/nil
  Description: If t tangent mode is on.

#### Arguments

|  |
| --- | ---
| `s_name` | symbol name of control.`nil` returns all possible names
#### Value Returned

See above.

`ls_names`, If name is `nil` then returns a list of all controls.

#### See Also

axlSetLineLock

#### Example

* Return current lock tangent setting

`axlGetLineLock('lockTangent)`

* Get all names supported by this interface

`listOfNames = axlGetLineLock(nil)`

### axlEnterBox

`axlEnterBox(?prompts            l_prompts?points            l_points)⇒ l_box/nil`

#### Description

Takes two points that define a box and returns them in`l_box`. Optionally prompts the user, if `l_prompts` contains no more than two strings. If `l_points` is `nil`, prompts for two points. If `l_points` contains one point, prompts only for the second point. If `l_points` contains both points, simply returns them as `l_box`.

#### Arguments

|  |
| --- | ---
| `l_prompts` | List that should contain two prompt messages. If list is`nil`, uses default Allegro PCB Editor prompts for soliciting a box. (`"Enter first point of box"` and `"Enter second point of box"`) If list contains two strings, the first string prompts for the first point, and the second string prompts for the second point. If the list has only one string, the string prompts for both the first and the second points.
| `l_points` | List of none, one, or two points. Solicits missing points interactively using the prompts given in`l_prompts` in order.
#### Value Returned

|  |
| --- | ---
| `l_box` | List of the lower left and upper right coordinates of the box.
| `nil` | Failed to get box data.
#### Example

> ```
> axlDBCreateRectangle(    axlEnterBox(?prompts     list("First rectangle point, please..."         "Second rectangle point, please..."))            t "etch/top")⇒ (dbid:12134523 nil)
> ```

Asks for box input to create a filled rectangle on layer`"etch/top".`

#### See Also

[axlEnterEvent](#616446 "7"), [axlEnterPoint](#572013 "7")

### axlEnterPath

```
axlEnterPath(?prompts            l_prompts?points            l_points?lastPath            r_path)⇒ r_path/nil
```

#### Description

Gets the start point and subsequent points for a path, interactively with optional prompting, or from the optional argument`l_points`. Sets the start point to the first value of `l_points`, if any, and the second point to the second value, if any. If `r_path` is given, connects the dynamic rubberband to its most recent segment. Use `axlEnterPath` recursively to build up the coordinates of a path interactively.

#### Arguments

|  |
| --- | ---
| `l_prompts` | List containing one prompt message to display.
| `l_points` | List of none, one, or two coordinates to be used as input to`axlEnterPath`.
| `r_path` | The previously gathered part of the path. Used to calculate the tangent point for the dynamic cursor.
#### Value Returned

|  |
| --- | ---
| `r_path` | Path containing segments constructed from the combined points in`l_points` and the interactive input to `axlEnterPath`.
| `nil` | Failed to get points.
#### Example

See the[Enter Function Example](#575281 "7").

### axlHighlightObject

`axlHighlightObject([lo_dbid][g_permHighlight])⇒ t/nil`

#### Description

Highlights the figures whose`dbids` are in `lo_dbid`.

Fewer objects support permanent highlighting than support temporary highlighting.

**Note:** Setting`axlDebug(t)` enables additional informational messages.

#### Arguments

|  |
| --- | ---
| `od_dbid` | List of the`dbids` of figures to be highlighted.
| `g_permHighlight` | Distinguishes temporary highlighting from permanent highlighting using color.  `t`     - use PERM highlight color  `nil` - use TEMP highlight color  The default is`nil`.
#### Value Returned

|  |
| --- | ---
| `t` | Highlighted at least one figure.
| `nil` | Highlighted no figures due to invalid`dbids` or objects already being highlighted.
#### Examples

You can use the AXL-SKILL`axlHighlightObject` and `axlDehighlightObject` functions to highlight database elements during interactive commands.

This example does the following:

|
| ---
|
 **a.** | Defines the function`highlightLoop`.
|
| ---
|
 **b.** | Loops on the function axlSelect gathering user selections to highlight.
|
| ---
|
 **c.** | Waits in a simple delay loop, then dehighlights.
You can stop the command at any time by selecting*Cancel* or *Done* from the pop-up.

`(defun highlightLoop ()`

`mypopup = axlUIPopupDefine( nil`

`(list (list "Done" 'axlFinishEnterFun)`

`(list "Cancel" 'axlCancelEnterFun)))`

`axlUIPopupSet( mypopup)`

`axlSetFindFilter( ?enabled '("noall" "alltypes" "nameform")`

`?onButtons "alltypes")`

`(while (axlSelect)`

`progn(`

`axlHighlightObject( axlGetSelSet())`

`; Just a dummy delay to see what happens`

`sum = 0`

`for( i 1 10000 sum = sum + i)`

`axlDehighlightObject( axlGetSelSet())))`

This example permanently highlights an object using color 4:

`axlDBControl('highlightColor 4)`

`axlHighlightObject(axlGetSelSet() t)`

Also see the[axlHighlightObject and axlDehighlightObject Examples](#578049 "7").

### axlDehighlightObject

`axlDehighlightObject(lo_dbid/g_mode[g_permHighlight])⇒ t/nil`

#### Description

Use this command to turn off highlighting on an object. Dehighlights the objects whose`dbids` are in `lo_dbid`. If 'all option is used then g\_permHighlight is treated as t (true).

#### Arguments

|  |
| --- | ---
| `lo_dbid` | List of`dbids` of figures to be dehighlighted.
| `g_mode` | `'all` to dehighlight entire design  `'nets` dehighlight all nets.
| `g_permHighlight` | Distinguishes temporary highlighting from permanent highlighting using color.  `t`     - use PERM highlight color  `nil` - use TEMP highlight color (The default value is `nil`.)
#### Value Returned

|  |
| --- | ---
| `t` | Dehighlighted at least one figure.
| `nil` | Failed to dehighlight any figures.
#### Example

See[axlHighlightObject](#572099 "7") for examples.

#### See Also

[axlHighlightObject](#572099 "7")

### axlMiniStatusLoad

```
axlMiniStatusLoad (s_formHandlet_formFile/(t_formName t_contents)g_formAction[g_StringOption][t_restrict])⇒ r_form/nil
```

#### Description

Loads the Ministatus form with the form file provided in this call. Replaces the current Ministatus form contents. This function is a special case of`axlForms`. See [Chapter 11, "Form Interface Functions,"](11frmint.html#414284 "11") for details on how AXL forms work.

When the command is finished, Allegro PCB Editor restores the Ministatus contents to the default values. Once the form is opened, you use normal`axlForm` functions to set or retrieve fields.

You typically use this to write a command requiring user interaction such as "swap component."

Two reserved field names are available:
 class -- enumerated list of CLASS layers
 subclass -- enumerated list of SUBCLASS layers for the current active class.

If you make use of these fields use support changing the active class and subclass you also get (for free) color swatch support. The Form file fragment shown below can be added to you ministatus form file to get that support. The "subcolor" field is optional. You should adjust the position (FLOC) of the fields to suite your form layout.

* ***For scripting and performance always use the same t\_formfile name for an application.***

**Note:** Using these reserved names also causes axlGetActiveLayer to update when user changes the layer.

`TEXT "Active Class and Subclass:"`

`FLOC 1 1`

`ENDTEXT`

`FIELD class`

`FLOC 5 4`

`ENUMSET 19`

`OPTIONS prettyprint`

`POP "class"`

`ENDFIELD`

# option

`FIELD subcolor`

`FLOC 2 7`

`COLOR 2 1`

`ENDFIELD`

`FIELD subclass`

`FLOC 5 7`

`ENUMSET 19`

`OPTIONS prettyprint ownerdrawn`

`POP "subclass"`

`ENDFIELD`

#### Arguments

A description of the in-line [(t\_formName t\_contents)] is contained in the function axlFormCreate.

t\_restrict This optional argument is a string that indicates class and subclass
 restrictions if the form contains "class" and "subclass" popup fields that have
 not been overridden with calls to axlFormBuildPopup.
 Possible values are:

"NONE" - no restrictions
 "TEXT" - only layers that allow text
 "SHAPES" - only layers that allow shapes
 "RECTS" - only layers that allow rectangles
 "ETCH" - only etch layers
 "ETCH\_PIN\_VIA" - only etch, pin, and via layers
 "ETCH\_NO\_WIREBOND" - only non-wirebond etch layers

#### Value Returned

|  |
| --- | ---
| `r_form` | Upon success,`r_form` is returned.
| `nil` | Failure due to one of the following:  No interactive command is active or the active command is not of the type AXL registered interactive.  AXL Forms code encounters an error.
#### Example

See swap component example:

`<install_dir>/share/pcb/etc/skill/examples/swap`

#### See Also

[axlFormCreate](11frmint.html#414342 "11") for further details.

### axlDrawObject

`axlDrawObject(lo_dbid)⇒ t/nil`

#### Description

Processes a list of`dbids`.

Redraws any objects that were erased by`axlEraseObject`.

#### Arguments

|  |
| --- | ---
| `lo_dbid` | List of`dbids` or one `dbid`.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects drawn.
| `nil` | No valid`dbids` or all objects already at desired display state.
### axlDynamicsObject

`axlDynamicsObject (lo_dbid [l_ref_point])⇒ t/nil`

#### Description

Adds list of objects to the cursor buffer. These objects are attached to the cursor in xor mode. Origin point establishes cursor position relative to objects in the dynamics buffer.

**Note:** Adding too many objects to the cursor buffer dramatically affects performance.

* If you load a symbol definition via`axlLoadSymbol` but does not place the symbol, the definition will, at some time, be deleted from the database.

#### Arguments

|  |
| --- | ---
| `lo_dbid` | List of AXL`dbids` or single `dbid`.
| `l_ref_point` | Optional origin point (takes cursor position if not provided).
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects added to the cursor buffer.
| `nil` | No objects added to the cursor buffer.
#### Example

Adds a symbol to the cursor buffer with the symbol origin as a reference point:

> `axlDynamicsObject(symbol_id, symbol_id->xy)`

Add a symbol definition to cursor buffer:

> `axlDynamicsObject(symbol_id->defintion, symbol_id->xy)`

Load a symbol and add to cursor buffer to the current cursor location:

> `def = axlLoadSymbol("PACKAGE" "dip14")`

> `when(def axlDynamicsObject(def))`

### axlEraseObject

`axlEraseObject(lo_dbid)⇒ t/nil`

#### Description

Processes a list of`dbids` and erases them. Typically used with `axlDynamicsObject` to erase objects before attaching them to the cursor. Any objects erased are restored to their visibility when calling AXL shell or terminating the SKILL program.

#### Arguments

|  |
| --- | ---
| `lo_dbid` | List of`dbids` or one `dbid`.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects erased.
| `nil` | No valid`dbids` or all objects already at desired display state.
### axlControlRaise

`axlControlRaise(g_option)⇒ t/nil`

#### Description

Raises a tab in the control panel to the top. If you use this at the start of an interactive command, you override the environment variable,`control_auto_raise`.

#### Arguments

|  |
| --- | ---
| `g_option` | Supported symbols are:`'options`, `'find`, `'visibility`, and `nil`. `nil` returns a list of supported symbols.
#### Value Returned

|  |
| --- | ---
| `t` | Tab raised to top in control panel.
| `nil` | Unknown symbol.
#### Example

`axlControlRaise('options)`

Raises the option panel to the top.

### axlEnterEvent

`axlEnterEvent(l_eventMaskt_promptg_snap)⇒ r_eventId`

#### Description

A lower level event manager than other`axlEnter` functions. Provides a Skill program with more user event details. See [Table 7-2](#617555 "7") for a list of events with descriptions.

Returns event structure containing the attributes described in[Table 7-1](#617545 "7"). Event occurrence controls what attributes are set by all event types, and sets the `objType` and `time` attributes.

****Table 7-1****
**Event Attributes**

| **Attribute Name** | **Type** | **Description**
| objType | string | Type of object, in this case*event*
| type | symbol | Event occurrence
| xy | point | Location of mouse
| xySnap | point | Location of mouse snapped to grid.
| command | int/symbol | Returns the callback item of`axlUIPopupDefine`
| time | float | time stamp (seconds.milliseconds)
**Note:** Do not put a default handler in your case statement since the event model will change in future releases.

****Table 7-2****
**Events**

| **Event** | **Description** | **Attributes/Mask**
| `PICK` | User has selected a point (equal to`axlEnterPoint`) |
| PICK\_EXTEND | Same as`PICK` except has `extend` keyboard modifier. |
| PICK\_TOGGLE | Same as`PICK` except has `toggle` keyboard modifier. | xy, xySnap
| DBLPICK | User has double picked at a location. |
| DBLPICK\_EXTEND | Same as`DBLPICK` except has `extend` keyboard modifier. |
| DBLPICK\_TOGGLE | Same as`DBLPICK` except has`toggle` keyboard modifier. | xy, xySnap
| MOVE | Mouse is moving. Depending upon the amount of time spent in your callback, the system may sum mouse movements to minimize falling behind in processing mouse events. |
| STARTDRAG | User starts a drag operation. |
| STARTDRAG\_EXTEND | Same as`STARTDRAG` except has `extend` keyboard modifier. |
| STARTDRAG\_TOGGLE | Same as`STARTDRAG` except has `toggle` keyboard modifier. | xy, xySnap
| STOPDRAG | User terminates the drag operation. |
| STOPDRAG\_EXTEND | Same as`STOPDRAG` except has `extend` keyboard modifier. |
| STOPDRAG\_TOGGLE | Same as`STOPDRAG` except has `toggle` keyboard modifier. | xy, xySnap, command
| DONE | User requests the command to complete. | This event cannot be masked.
| CANCEL | Respond to this event by terminating your Skill program (don't call any more*axlEnter* functions.) | This event cannot be masked.
#### Notes

* You will get`PICK` before `DBLPICK` events. To differentiate between a `PICK` and `DBLPICK`, highlight the selected object. Do not output informational messages or perform time consuming processing.

* Never prompt user for a double click. Instead, format prompts for the next expected event.

* Events dispatched from`axlEnterEvent` are scripted by the system if scripts are enabled.

* The*done* and *cancel* callbacks optionally defined in `axlCmdRegister` are called before the`DONE` and `CANCEL` events are returned.

* The`extend` keyboard modifier is obtained by holding the `Shift`key while performing the mouse operation.

* The`toggle` keyboard modifier is obtained by holding the `Control` key while performing the mouse operation.

* You can program more easily by providing a single mask set for your command and by not attempting to change the mask set after each event.

* When*Snap to Object* right mouse button menus are present and the user selects a snap operation:

* both the xy and xySnap return the snap result

* the snap argument is ignored

* normal pick events function normally

* Use`axlSnapDisableAtRMB` if you do not want to snap the menu items.

#### Arguments

|  |
| --- | ---
| `l_eventMask`/`nil` | List of events to expect.
| `t_prompt`/`nil` | User prompt. If`nil`, the default prompt is used.
| `g_snapGrid` | If`t`, grid snapping is enabled while the function is active. Otherwise no grid snapping is allowed. This affects the `xySnap` value that is returned as well as dynamics and the `xy` readout. If `nil`,`xySnap` is not snapped to the grid and is the same as `xy`.
#### Value Returned

|  |
| --- | ---
| `r_eventId` | Event structure containing attributes.
#### See Also

[axlEnterPoint](#572013 "7") and axlSnapEnableAtRMB

#### Example

A complete example is contained in:`<cdsroot>/share/pcb/examples/skill/axlcore/EnterEvent.il`

`let( (eventMask event, loop)`

> > `eventMask = '( PICK DBLPICK )`

> `loop = t`

> `while( loop`

> > `event = axlEnterEvent(eventMask, nil t)`

> > `case(event->type`

> > `('PICK`

> > `... )`

> > `('DBLPICK`

> > `... )`

> > `('DONE`

> > `; cleanup`

> > `loop = nil)`

> `)`

> > `)`

`)`

### axlEventSetStartPopup

`axlEventSetStartPopup([s_callback])⇒ t/nil`

#### Description

Sets a SKILL callback function called prior to a popup being displayed on the screen. Allows AXL applications to reset the popup (see`axlUIPOPUPSetsee`), thus providing context sensitive popups support.

The callback function is passed a list structure the same as the return list in`axlEnterEvent`. Use this function with `axlEnterEvent`.

The callback function is removed when an AXL application is finished. Set this at the application start, if needed.

#### Arguments

|  |
| --- | ---
| `s_callback` | AXL callback function.
| none | Unsets the callback function which disables the callback mechanism.
#### Value Returned

|  |
| --- | ---
| `t` | Set SKILL callback function.
| `nil` | Failed to set SKILL callback function.
#### Example

`(defun startpopupcallback (event)`

`...`

`newpopup = get a new popup based on event x,y values`

`axlUIPopupSet(newpopup)`

`)`

`axlEventSetStartPopup('startpopupcallback)`

`...`

`let( (eventMask event, loop)`

`eventMask = list( 'PICK 'DBLPICK )`

`loop = t`

`while( loop`

`event = axlEnterEvent(eventMask, nil)`

`case(event->type`

`('PICK`

`... )`

`('DBLPICK`

`... )`

`('DONE`

`loop = nil)`

`('CANCEL`

`loop = nil)`

`)`

`)`

`...`

`axlEventSetStartPopup()`

Typically used in conjunction with`axlEnterEvent`.

### axlGetTrapBox

`axlGetTrapBox(l_point)⇒ l_window/nil`

#### Description

Returns coordinates of the*Find* window.

#### Arguments

|  |
| --- | ---
| `l_point` | Listing of the`x` and `y`coordinates
#### Value Returned

|  |
| --- | ---
| `l_window` | `((x_l y_l) (x_u y_u))` - List of corner coordinates of the *Find* window.  `(x_l y_l)` - List containing *x* and *y* coordinates of the lower left corner.  `(x_u y_u)` - List of the *x* and *y* coordinates of the upper right corner.
| `nil` | `l_point` is `null` or in an incorrect format.
### axlRatsnestBlank

`axlRatsnestBlank(rd_net)⇒ t/nil`

#### Description

Blanks all ratsnest lines in a net.

#### Arguments

|  |
| --- | ---
| `rd_net` | `dbid` of a net
#### Value Returned

|  |
| --- | ---
| `t` | Ratsnest lines are blanked.
| `nil` | Ratsnest lines are not blanked.
### axlRatsnestDisplay

`axlRatsnestDisplay(rd_net)⇒ t/nil`

#### Description

Displays all ratsnest lines in a net.

#### Arguments

|  |
| --- | ---
| `rd_net` | `dbid` of a net
#### Value Returned

|  |
| --- | ---
| `t` | Ratsnest lines are displayed.
| `nil` | Ratsnest lines are not displayed.
### axlSetDynamicsMirror

sets mirror option for dynamics

`axlSetDynamicsMirror(g_mirror) ==> g_oldmirror`

#### Description

Sets the Dynamics mirroring.

#### Arguments

* `t:`mirror
* `GEOMETRY:`mirror geometry only (same layer)
* `nil:`mirror none

#### Value Returned

old mirror value

#### See Also

[axlAddSimpleMoveDynamics](#572000 "7")

#### Example

`axlSetDynamicsMirror(t`)

### axlSetDynamicsRotation

`axlSetDynamicsRotation(f_angle/nil) ==> f_oldangle`

#### Description

Sets the Dynamics rotation. If angle is nil then returns current rotation.

Arguments

|  |
| --- | ---
| `f_angle` | Floating point number
#### Value Returned

old angle

#### See Also

[axlAddSimpleMoveDynamics](#572000 "7")

#### Example

`axlSetDynamicsRotation(45.0)`

### axlShowObjectToFile

`axlShowObjectToFile(lo_dbid[t_file_name])⇒ (t_file_name x_width x_line_count)`

#### Description

Creates a temporary file with show element information on`dbids` specified in `lo_dbid`.

#### Arguments

|  |
| --- | ---
| `lo_dbid` | List of`dbids` or a single `dbid`.
| `t_file_name` | File name to use instead of a temporary file.
#### Value Returned

List of items describing the file created`(``t_file_name x_width x_line_count``)`:

|  |
| --- | ---
| `t_file_name` | Name of the temporary file.
| `x_width` | Width, in characters, of the widest text line.
| `x_line_count` | Number of lines in the file.
| `nil` | Could not create file.
### axlUICmdPopupSet

`axlUICmdPopupSet(r_popup)⇒ r_prevPopup`

#### Description

Sets up a popup menu with all menu items required throughout the execution of the command. Call during the command's initialization process. Use of this procedure modifies the behavior of`axlUIPopupSet`so that it makes unavailable all popup items not in the defined popup.

Adds a`cmdPopupId` property to AXL user data which restores popup entries whenever the AXL command state is restored. The command popup is cleared when the Skill command ends.

#### Arguments

|  |
| --- | ---
| `r_popup` | Popup handle, obtained by calling`axlUIPopupDefine`. A `nil` value turns off this popup.
#### Value Returned

|  |
| --- | ---
| `r_prevPopup` | Popup set previously defined.
**Note:** This procedure does the same as`axlCmdPopupSet` for non-WXL UI's.

### axlWindowFit

`axlWindowFit()⇒ l_bBox`

#### Description

Zooms in to (or out of) a design fitting it fully on the window. For the Allegro PCB Editor in layout mode, performs a fit on the outline. For the Allegro PCB Editor symbol mode, performs a fit such that all visible objects occupy maximum window area. Returns the bounding box of the window after the fit has been performed.

#### Arguments

`none`

#### Value Returned

|  |
| --- | ---
| `l_bBox` | The bounding box of the window after zooming (in user units).
**Note:** This is available as the Allegro PCB Editor command*window fit**.*

### axlZoomBbox

`axlZoomBbox (x_window) => bBox`

#### Description

x\_window: window id or nil to currently active window. nil is the activewindow and 0 is the primary canvas. Allegro currently onlysupports one additional canvas so the value 1 indicates thatcanvas.

#### Arguments

Returns bounding box (bBox) of window.

#### Value Returned

|  |
| --- | ---
| `bBox` | a list of two xy coordinates indicating upper right and lowerleft. These are in design units.
#### See Also

axlZoomControl

#### Examples

* BBox of active window

`axlZoomBbox(nil)=> ((100 120) (300 320))`

### axlZoomCenter

`axlZoomCenter (x_windowxy)-=> t/nil`

#### Description

Zoom centers on the provided coordinate. It may adjust the point if centering results in the display bounding extents are outside thedesign extents.

* If you wish to zoom and center use axlZoomInOut.

#### Arguments

|  |
| --- | ---
| `x_window` | window id or nil to currently active window (see[axlZoomBbox](#642159 "7"))
| `xy` | Coordiante in design units for centering
#### Value Returns

|  |
| --- | ---
| `t` | if successful
| `nil` | an error
#### See Also

axlZoomControl

#### Examples

* Create a seconday window and center it

> `axlZoomControl('create)axlZoomCenter(1 4000:4000)`

### axlZoomControl

`axlZoomControl (s_option[g_arg])-=> g_return`

#### Description

Manages the multi-canvas feature. Requires OpenGL to be enabled.Id 0 is the main Allegro canvas.

Supported options are:

|  |
| --- | ---
| 'create | creates a new canvas. Currently only 1 supported.  Return - If success returns canvas id, if max canvases already exist or multi-window not supported returns nil
| 'remove | removes secondary canvas. Cannot remove primarycanvas (id=0). Requires a canvas id for g\_arg.  Return -`t` if canvas removed, `nil` if error
| 'supported | Is multi-window supported.  Return -`t` if supported, nil not supported
| 'list | available canvases
| 'active | returns the active window id. This impacts the Allegro menu Zoom commands and if you pass nil to the axlZoom APIs  Return: integer indicating active window
| 'swap | swaps the primary and secondary window contents.  Return: t did the swap, nil failed
#### Arguments

|  |
| --- | ---
| `s_option` | see above
| `g_arg` | addition argument some options require, see above
#### Value Returned

|  |
| --- | ---
| `g_return` | depends upon the option, See above
#### See Also

[axlZoomBbox](#642159 "7") axlZoomPoints [axlZoomCenter](#642227 "7") axlZoomWorld

#### Examples

* Create secondary canvas

> `axlZoomControl('create)`

* Remove secondary canvas

> `axlZoomControl('remove 1)`

### axlZoomFit

`axlZoomFit (x_windows_option) => t/nil`

#### Description

Zoom fits the window. Depending upon the design type fit is define as:

* logic design (brd, mcm, mdd, etc)

> > > Fit to board outline, package and route keepin

* partition (dps, dpf)

> > > Fit to partition boundary

* symbol (dra) - all visible objects

#### Arguments

|  |
| --- | ---
| `x_window` | window id or nil to currently active window (see[axlZoomBbox](#642159 "7"))
| `s_option(visible)` | if logic or parition design fit to visible objects
#### Value Returned

|  |
| --- | ---
| `t` | if successful
| `nil` | an error
#### See Also

[axlZoomControl](#642299 "7")

#### Examples

* Fit primary window to visible objects

> `axlZoomFit(0 visible)'`

### axlZoomInOut

`axlZoomInOut (x_windowx_factor[xy]) => t/nil`

#### Description

Zooms window in or out by provided factor around optional coordinate.

#### Arguments

|  |
| --- | ---
| `x_window` | window id or nil to currently active window (see[axlZoomBbox](#642159 "7"))
| `x_factor` | factor to zoom, a positive number zooms in while negative zooms out. 1 is 2x, 2 is 4x, 3 is 8x etc.
| `xy` | optional coordinates to zoom around. If not provided uses center of current window
#### Value Returns

|  |
| --- | ---
| `t` | if successful
| `nil` | an error
#### See Also

[axlZoomControl](#642299 "7")

#### Examples

* zoom in by 2x primary window

`axlZoomInOut(0 1)`

### axlZoomPoints

`axlZoomPoints (x_windowupperLeft_xylowerRight_xy) => t/nil`

#### Description

Zoom windows by points. The zoom maintains a 1:1 aspect ratio,the coordinates provided will be fitted into the active window size.

#### Arguments

|  |
| --- | ---
| `x_window` | window id or nil to currently active window (see axlZoomBbox)
| `upperLeft_xy` | upper left coordiante
| `lowerRight_xy` | lower right coordiante
#### Value Returns

|  |
| --- | ---
| `t` | if successful
| `nil` | an error
#### See Also

axlZoomControl

#### Examples

* zoom by points on the primary window

`axlZoomPoints(0 100:120 4000:4000)`

### axlZoomToDbid

`axlZoomToDbid(o_dbid/lo_dbidg_always[x_window])⇒ t/nil`

#### Description

Processes a list of`dbids` and centers and zooms the display around them. Zoom is done so objects extents fill about 20% of the display. You should highlight the objects.

**Note:** If more than 20 objects are passed no zoom is done.

#### Arguments

|  |
| --- | ---
| `o_dbid` | List of`dbids` or one `dbid`.
| `g_always` | If`t,` then ignores `NO_ZOOM_TO_OBJECT` environment variable.
| *x\_window* | Optional window ID or`nil` to currently active window (see [axlZoomBbox](#642159 "7")). If no value is provided active window is used.
#### Value Returned

|  |
| --- | ---
| `t` | One or more objects zoomed.
| `nil` | No valid`dbids` or all objects are already at desired display state.
#### Example

* Zoom to U1

> `sym = axlDBFindByName('refdes "U1")`

> `axlZoomToDbid(sym t)`

#### See Also

axlZoomManage

### axlZoomWorld

`axlZoomWorld (x_window) => t/nil`

#### Description

Zoom world a drawing window

#### Arguments

|  |
| --- | ---
| `x_window` | window id or nil to currently active window (see[axlZoomBbox](#642159 "7"))
#### Value Returns

|  |
| --- | ---
| `t` | if successful
| `nil` | an error
#### See Also

[axlZoomControl](#642299 "7")

#### Examples

* world the active window

`axlZoomWorld (nil)`

### axlMakeDynamicsPath

`axlMakeDynamicsPath(l_formatedList)⇒ r_path/nil`

Description

This is a convenience function to construct an`r_path` from a formatted list. `axlDBCreate` and `axlPoly` require an `r_path.`

**Note:** A circle is an arc segment with same end points.

**Note:** Caution: Passing an illegal format may result in a bad return.

#### Arguments

|  |
| --- | ---
| `( l_seg1 l_seg2 ...) g_clockwise` | Each`l_seg` is:  (`l_startPoint l_endPoint [f_width] [l_center] [f_radius])`  `l_startPoint:`Start point of path.  `l_endPoint:`End point of path.  `f_width:` Optional width (default of 0).  `l_center:`Optional center point if `r_path` is an arc.  `f_radius:`Optional radius if `r_path` is an arc.  If an arc`r_path,` both`l_center` and `f_radius` must be provided.
| `g_clockwise` | Direction to create arc:  t⇒ create arc clockwise from start to endpoint.  nil⇒ create counterclockwise. Default is counterclockwise.
#### Value Returned

|  |
| --- | ---
| `r_path` | `dbid` of `r_path`.
| `nil` | No`r_path` constructed due to incorrect arguments.
#### Example

Simple`r_path` segment with a width of 20.

`a = axlMakeDynamicsPath(list(list( 10:10 100:100 20)))`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
