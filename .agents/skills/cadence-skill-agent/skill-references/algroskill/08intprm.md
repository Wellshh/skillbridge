### axlClearDynamics

`axlClearDynamics( ) => t`

#### Description

Clears the dynamic cursor buffer. Call this function each time before you start setting up rubberband and dynamic cursor graphics.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See dynamic cursor examples in the section AXL-SKILL Interface Function Examples.

### axlAddSimpleRbandDynamics

`axlAddSimpleRbandDynamics( l_fixed_point t_type ?origin l_origin ?var_point l_var_point ?lastPath l_lastPath ?width f_width ?color g_color ) => t/nil`

#### Description

Loads rubber band dynamics buffer with an element. If dynamics buffer is already loaded, the new element is simply added to the existing buffer. Dynamics buffer is not cleared until axlClearDynamics is called.

Rubber band dynamics means stretching of elements to the cursor from an anchor point called the fixed_point.

- This works in conjunction with the axl<Event> APIs. In particular, no grid snapping, only works when these APIs are called. Do not use this in the axlUIWTimerAdd or with axlTriggerSet callbacks.

#### Arguments

| Name | Description |
|---|---|
| `l_fixed_point` | Fixed point of rubber band. Anchor point from which the dynamic rubberband stretches. The rubberband cursor stretches dynamically from `fixed_point` to current position of the cursor, as moved by the user. The next argument, `type`, specifies the shape of the rubberband--part of a path, direct, z-line (a combination of horizontal and vertical), arc, circle, or box. |
| `t_type` | String specifying type of dynamic rubberband to be drawn. Can be one of the following:`path, directline, horizline, vertline, arc, circle, or box`. `directline`: add a single line to buffer between `fixed_point` and `var_point`.
 origin and variable point of var_point `horizline`: A single horizontal line. `vertline`: A single vertical line `arc`: Arc between fixed_point and var_point. Radius varies as cursor moves
 "circle": Circle, fixed_point is center and var_point is initial radius. 
 "box": Add a box, fixed point is one corner and the var_point is the opposite corner.
 "path": Add two segments whose behavior is controlled by the line lock attributes (axlSetLineLock).
 "fixedline": Adds a constant line to cursor buffer, fixed_point and var_point are the two endpoints. |
| `l_origin` | Cursor origin. Useful only if you plan on rotating the object, this is the center of its rotation. Also on arcs to control tangency. In most cases this should be nil. |
| `l_var_point` | Variable point for rubberbanding. |
| `l_lastPath` | Previous path structure. Needed to calculate tangent point if rubberbanding starts at the end of an existing path. |
| `f_width` | Optional database width of the rband. Default is 0.0. |
| `g_color` | Optional arg for defining the dynamics' color. Possible choices are: |

- A layer string (i.e. class/subclass) for the layer to be used for deriving the color.

- 'ratsnestColor - the color used for ratsnest lines will be used.

- 'activeSubclassColor - the color for the active class/subclass is used. If this changes, the color for this rband also changes.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Successfully added data. |
| `nil` | No data added. |

#### Examples

A file, demo_dynamics.il, in `<cdsroot>``/share/pcb/examples/skill` demonstrates the various t_type options.

This example loads two circular pad and, the outline of a resistor, and rubberband connections from its pins, one with a "path" rubberband, the other a "directline" rubberband into the dynamic cursor buffer:

`axlClearDynamics() ; Clean out any existing cursor data`

`mypath = axlPathStart(list( -350:0)) ; Start circular pad`

`axlPathArcCenter(mypath, 0., -350:0, nil, -300:0)`

`; Load the first pad into the dynamic cursor buffer`

`axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)`

`mypath = axlPathStart(list( 350:0)) ; Start circular pad`

`axlPathArcCenter(mypath, 0., 350:0, nil, 300:0)`

`; Load the other pad into the dynamic cursor buffer`

`axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)`

`mypath = axlPathStart( ; Start resistor body outline`

`list( -200:-100 200:-100 200:100 -200:100 -200:-100))`

`; Loads the resistor body outline in the dynamic cursor buffer`

`axlAddSimpleMoveDynamics(0:0 mypath "path" ?ref_point 0:0)`

`; Ask user to pick angle of rotation about (8500:4500):`

`axlEnterAngle(8500:4500)`

See dynamic cursor examples in the section AXL-SKILL Interface Function Examples.

#### See Also

axlEnterPoint, axlEnterEvent

### axlAddSimpleMoveDynamics

`axlAddSimpleMoveDynamics( l_origin r_path t_type ?ref_point l_ref_point ?color g_color ) => t/nil`

#### Description

Loads cursor buffer dynamics buffer with an element. If dynamics buffer is already loaded, the new element is simply added to the existing buffer. Dynamics buffer is not cleared until axlClearDynamics is called.

Cursor buffer dynamics means no stretching of elements. The loaded is attached to the cursor and moves with it.

#### Arguments

| Name | Description |
|---|---|
| `l_origin` | Cursor origin. (see axlAddSimpleRbandDynamics) |
| `r_path` | Path structure containing display objects. |
| `t_type` | String specifying type of path: either `path` or `box`. Note that lines and arcs are represented as path. Circle is a special case of arc where the start, end points are the same. |
| `l_ref_point` | Element rotation reference point. |
| `g_color` | Optional argument for defining the dynamics' color. Possible choices are:
 
 A layer string (class/subclass) for the layer to be used for deriving the color. `'ratsnestColor` - the color used for ratsnest lines will be used. `'activeLayerColor` - the color for the active class/subclass is used. If this changes, the color for this rband also changes. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Returned if the data is successfully added. |
| `nil` | No data added. |

#### Examples

See dynamic cursor examples, Example 1: Dynamic Rubberband and Example 2: Dynamic Cursor Rotation, in the section AXL-SKILL Interface Function Examples.

### axlDesignFlip

`axlDesignFlip( g_flip ) => t/nil`

#### Description

Visually flips the design in the 'y' axis. Maintains current xy view.

Note: This command not available if OpenGL is disabled.

#### Arguments

| Name | Description |
|---|---|
| t | flipped on y axis |
| nil | unflip |

#### Value Returns

Old flip state. If t flipped (y) if nil normal top view state

#### Examples

Syntax to implement toggle flipping

#### See Also

axlWindowFit

### axlEnterPoint

`axlEnterPoint( ?prompts l_prompts ?points l_points ?gridSnap g_gridSnap ) => l_point/nil`

#### Description

`axlDesignFlip( !axlDesignFlip())` Prompts for and receives user-selected point. Returns the point data to the calling function.

#### Arguments

| Name | Description |
|---|---|
| `l_prompts` | List containing one prompt message to display. |
| `l_points` | List of points. Returns one of these as the return value. `l_point's` only use is, if passed a point, to immediately return with the point snapped to the nearest grid. |
| `g_gridSnap` | Flag to function: `t` means snap the point according to the current grid. |

#### Value Returns

| Name | Description |
|---|---|
| `l_point` | List of coordinates, if entered. If selected, this is a list of one point. |
| `nil` | User did not select a point. |

#### Examples

See Example 1 in the section AXL-SKILL Interface Function Examples.

#### See Also

axlGetLastEnterPoint, axlEnterEvent

### axlEnterString

`axlEnterString( ?prompts l_prompts ) => t_string/nil`

#### Description

Displays a dialog box that requires first entering a string, and then pressing Return on the keyboard or clicking OK or Cancel. Default prompt in the dialog box is `"Enter String."`You can supply a prompt string with the `?prompts` keyword. The function returns the string entered, if any. Otherwise it returns `nil`.

Note: This function is a blocker. Allegro PCB Editor will not respond to any user input until the data requested by the dialog box is provided.

#### Arguments

| Name | Description |
|---|---|
| `l_prompts` | List containing one prompt message. Displays only the first string if the list contains more than one string. |

#### Value Returns

| Name | Description |
|---|---|
| `t_string` | String entered. |
| `nil` | No string entered, dialog box dismissed by clicking Cancel, or the command failed. |

#### Examples

`user_name = axlEnterString(``?prompts list("Please enter your name:"))`

`⇒``"user name"`

Prompts for name and collects the response in `user_name`.

Typing the name, then pressing the Return key returns the string entered:

### axlEnterAngle

`axlEnterAngle( origin ?prompts l_prompts ?refPoint l_refPoint ?angle f_angle ?lockAngle g_lockAngle ) => f_angle/nil`

#### Description

Optionally prompts the user. Returns the angle value entered.

#### Arguments

| Name | Description |
|---|---|
| `origin` | Fixed point where two lines making up the angle meet. |
| `l_prompts` | List containing one prompt message. |
| `l_refPoint` | End point of a line from the `origin` that acts as the fixed line of the angle. |
| `f_angle` | Angle value in. If non-`nil`, does not prompt for a user-selected point. |
| `g_lockAngle` | Initial lock angle for dynamic rotation. |

#### Value Returns

| Name | Description |
|---|---|
| `f_angle` | Selected angle expressed in degrees. |
| `nil` | No angle selected. |

#### Examples

See Example 1 in the section AXL-SKILL Interface Function Examples.

### axlCancelEnterFun

`axlCancelEnterFun() => t/nil`

#### Description

Terminates the wait for a user-selected point. Waiting function returns no data.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Terminates wait for user-selected point. Cancel succeeds. |
| `nil` | Fails to terminate wait for user-selected point. |

#### Examples

See the Enter Function Example.

### axlFinishEnterFun

`axlFinishEnterFun() => t/nil`

#### Description

Terminates the wait for a user-selected point. Waiting function returns no data. For a one-point function (for example, `axlEnterPoint`) behaves the same as `axlCancelEnterFun`.

#### Arguments

None.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Terminates wait for a user-selected point. |
| `nil` | Fails to terminate wait for a user-selected point. |

#### Examples

See the Enter Function Example.

### axlGetDynamicsSegs

`axlGetDynamicsSegs( l_point1 l_point2 r_lastPath/nil ) =>`

#### Description

Normally used with dynamics to calculate arc tangency of two picks to a current `r_path`. Passed coordinates may be modified to preserve tangency. Depends on the current line lock state that you set or `axlSetLineLock`.

#### Arguments

| Name | Description |
|---|---|
| `point1` | First pick before dynamics started. |
| `point2` | Second pick, after dynamics completes. |
| `lastPath` | Previous path to use for tangency calculations. Can pass `nil` if not applicable. |

#### Value Returns

`l_pointList`

`nil`

#### Examples

`q = axlGetDynamicsSegs(10:10 100:100 nil)`

`-> (((10.0 10.0) (100.0 100.0) nil))`

#### See Also

axlAddSimpleRbandDynamics, axlMakeDynamicsPath, axlSetLineLock

### axlGetLineLock

`axlGetLineLock( s_name [g_value] ) => g_currentValue/ls_names`

#### Description

Gets the current settings of the line lock or dynamic control options. Equivalent items is the option control panel for "add" commands. Items currently supported:

- Name: arcEnableValue: t/nilDescription: If t Lock Mode is arc, nil is line.

- Name: lockAngleValue: 0, 45, 90Description: In degrees where 0 is off (no lock).

- Name: minRadiusValue: floatDescription: Minimum Radius in user units.

- Name: length45Value: floatDescription: Fixed 45 Length value in user units.

- Name: fixed45Value: t/nilDescription: If t Fixed 45 length is enabled.

- Name: lengthRadiusValue: floatDescription: Fixed radius value in user units.

- Name: fixedRadiusValue: t/nilDescription: If t in Fixed Radius mode

- Name: lockTangentValue: t/nilDescription: If t tangent mode is on.

#### Arguments

| Name | Description |
|---|---|
| `s_name` | symbol name of control. `nil` returns all possible names |

#### Value Returns

See above.

`ls_names`, If name is `nil` then returns a list of all controls.

#### Examples

- Return current lock tangent setting

- Get all names supported by this interface

`axlGetLineLock('lockTangent) listOfNames = axlGetLineLock(nil)`

#### See Also

axlSetLineLock

### axlEnterBox

`axlEnterBox( ?prompts l_prompts ?points l_points ) => l_box/nil`

#### Description

Takes two points that define a box and returns them in `l_box`. Optionally prompts the user, if `l_prompts` contains no more than two strings. If `l_points` is `nil`, prompts for two points. If `l_points` contains one point, prompts only for the second point. If `l_points` contains both points, simply returns them as `l_box`.

#### Arguments

| Name | Description |
|---|---|
| `l_prompts` | List that should contain two prompt messages. If list is `nil`, uses default Allegro PCB Editor prompts for soliciting a box. (`"Enter first point of box"` and `"Enter second point of box"`) If list contains two strings, the first string prompts for the first point, and the second string prompts for the second point. If the list has only one string, the string prompts for both the first and the second points. |
| `l_points` | List of none, one, or two points. Solicits missing points interactively using the prompts given in `l_prompts` in order. |

#### Value Returns

| Name | Description |
|---|---|
| `l_box` | List of the lower left and upper right coordinates of the box. |
| `nil` | Failed to get box data. |

#### Examples

`axlDBCreateRectangle(``axlEnterBox(?prompts``list("First rectangle point, please..."``"Second rectangle point, please..."))``t "etch/top")``⇒ (dbid:12134523 nil)`

Asks for box input to create a filled rectangle on layer `"etch/top".`

#### See Also

axlEnterEvent, axlEnterPoint

### axlEnterPath

`axlEnterPath( ?prompts l_prompts ?points l_points ?lastPath r_path ) => r_path/nil`

#### Description

Gets the start point and subsequent points for a path, interactively with optional prompting, or from the optional argument `l_points`. Sets the start point to the first value of `l_points`, if any, and the second point to the second value, if any. If `r_path` is given, connects the dynamic rubberband to its most recent segment. Use `axlEnterPath` recursively to build up the coordinates of a path interactively.

#### Arguments

| Name | Description |
|---|---|
| `l_prompts` | List containing one prompt message to display. |
| `l_points` | List of none, one, or two coordinates to be used as input to `axlEnterPath`. |
| `r_path` | The previously gathered part of the path. Used to calculate the tangent point for the dynamic cursor. |

#### Value Returns

| Name | Description |
|---|---|
| `r_path` | Path containing segments constructed from the combined points in `l_points` and the interactive input to `axlEnterPath`. |
| `nil` | Failed to get points. |

#### Examples

See the Enter Function Example.

### axlHighlightObject

`axlHighlightObject( [lo_dbid] [g_permHighlight] ) => t/nil`

#### Description

Highlights the figures whose `dbids` are in `lo_dbid`.

Fewer objects support permanent highlighting than support temporary highlighting.

Note: Setting `axlDebug(t)` enables additional informational messages.

#### Arguments

| Name | Description |
|---|---|
| `od_dbid` | List of the `dbids` of figures to be highlighted. |
| `g_permHighlight` | Distinguishes temporary highlighting from permanent highlighting using color. `t` - use PERM highlight color `nil` - use TEMP highlight color
 The default is `nil`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Highlighted at least one figure. |
| `nil` | Highlighted no figures due to invalid `dbids` or objects already being highlighted. |

#### Examples

You can use the AXL-SKILL `axlHighlightObject` and `axlDehighlightObject` functions to highlight database elements during interactive commands.

This example does the following:

- a.; Defines the function `highlightLoop`.

- b.; Loops on the function axlSelect gathering user selections to highlight.

- c.; Waits in a simple delay loop, then dehighlights.

You can stop the command at any time by selecting Cancel or Done from the pop-up.

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

Also see the axlHighlightObject and axlDehighlightObject Examples.

### axlDehighlightObject

`axlDehighlightObject( lo_dbid/g_mode [g_permHighlight] ) => t/nil`

#### Description

Use this command to turn off highlighting on an object. Dehighlights the objects whose `dbids` are in `lo_dbid`. If 'all option is used then g_permHighlight is treated as t (true).

#### Arguments

| Name | Description |
|---|---|
| `lo_dbid` | List of `dbids` of figures to be dehighlighted. |
| `g_mode` | `'all` to dehighlight entire design `'nets` dehighlight all nets. |
| `g_permHighlight` | Distinguishes temporary highlighting from permanent highlighting using color. `t` - use PERM highlight color `nil` - use TEMP highlight color (The default value is `nil`.) |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Dehighlighted at least one figure. |
| `nil` | Failed to dehighlight any figures. |

#### Examples

See axlHighlightObject for examples.

#### See Also

axlHighlightObject

### axlMiniStatusLoad

`axlMiniStatusLoad ( s_formHandle t_formFile/(t_formName t_contents) g_formAction [g_StringOption] [t_restrict] ) => r_form/nil`

#### Description

Loads the Ministatus form with the form file provided in this call. Replaces the current Ministatus form contents. This function is a special case of `axlForms`. See Chapter 11, "Form Interface Functions," for details on how AXL forms work.

When the command is finished, Allegro PCB Editor restores the Ministatus contents to the default values. Once the form is opened, you use normal `axlForm` functions to set or retrieve fields.

You typically use this to write a command requiring user interaction such as "swap component."

Two reserved field names are available:	class -- enumerated list of CLASS layers	subclass -- enumerated list of SUBCLASS layers for the current active class.

If you make use of these fields use support changing the active class and subclass you also get (for free) color swatch support. The Form file fragment shown below can be added to you ministatus form file to get that support. The "subcolor" field is optional. You should adjust the position (FLOC) of the fields to suite your form layout.

- For scripting and performance always use the same t_formfile name for an application.

Note: Using these reserved names also causes axlGetActiveLayer to update when user changes the layer.

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

A description of the in-line [(t_formName t_contents)] is contained in the function axlFormCreate.

t_restrict	This optional argument is a string that indicates class and subclass	restrictions if the form contains "class" and "subclass" popup fields that have	not been overridden with calls to axlFormBuildPopup. Possible values are:

"NONE"	- no restrictions	"TEXT" - only layers that allow text	"SHAPES"	- only layers that allow shapes	"RECTS" - only layers that allow rectangles	"ETCH"	- only etch layers	"ETCH_PIN_VIA"	- only etch, pin, and via layers	"ETCH_NO_WIREBOND"	- only non-wirebond etch layers

#### Value Returns

| Name | Description |
|---|---|
| `r_form` | Upon success, `r_form` is returned. |
| `nil` | Failure due to one of the following:
 No interactive command is active or the active command is not of the type AXL registered interactive.
 AXL Forms code encounters an error. |

#### Examples

See swap component example:

`<install_dir>/share/pcb/etc/skill/examples/swap`

#### See Also

axlFormCreate for further details.

### axlDrawObject

`axlDrawObject( lo_dbid ) => t/nil`

#### Description

Processes a list of `dbids`.

Redraws any objects that were erased by `axlEraseObject`.

#### Arguments

| Name | Description |
|---|---|
| `lo_dbid` | List of `dbids` or one `dbid`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects drawn. |
| `nil` | No valid `dbids` or all objects already at desired display state. |

### axlDynamicsObject

`axlDynamicsObject ( lo_dbid [l_ref_point] ) => t/nil`

#### Description

Adds list of objects to the cursor buffer. These objects are attached to the cursor in xor mode. Origin point establishes cursor position relative to objects in the dynamics buffer.

Note: Adding too many objects to the cursor buffer dramatically affects performance.

- If you load a symbol definition via `axlLoadSymbol` but does not place the symbol, the definition will, at some time, be deleted from the database.

#### Arguments

| Name | Description |
|---|---|
| `lo_dbid` | List of AXL `dbids` or single `dbid`. |
| `l_ref_point` | Optional origin point (takes cursor position if not provided). |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects added to the cursor buffer. |
| `nil` | No objects added to the cursor buffer. |

#### Examples

Adds a symbol to the cursor buffer with the symbol origin as a reference point:

`axlDynamicsObject(symbol_id, symbol_id->xy)`

Add a symbol definition to cursor buffer:

`axlDynamicsObject(symbol_id->defintion, symbol_id->xy)`

Load a symbol and add to cursor buffer to the current cursor location:

`def = axlLoadSymbol("PACKAGE" "dip14")`

`when(def axlDynamicsObject(def))`

### axlEraseObject

`axlEraseObject( lo_dbid ) => t/nil`

#### Description

Processes a list of `dbids` and erases them. Typically used with `axlDynamicsObject` to erase objects before attaching them to the cursor. Any objects erased are restored to their visibility when calling AXL shell or terminating the SKILL program.

#### Arguments

| Name | Description |
|---|---|
| `lo_dbid` | List of `dbids` or one `dbid`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects erased. |
| `nil` | No valid `dbids` or all objects already at desired display state. |

### axlControlRaise

`axlControlRaise( g_option ) => t/nil`

#### Description

Raises a tab in the control panel to the top. If you use this at the start of an interactive command, you override the environment variable, `control_auto_raise`.

#### Arguments

| Name | Description |
|---|---|
| `g_option` | Supported symbols are:`'options`, `'find`, `'visibility`, and `nil`. `nil` returns a list of supported symbols. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Tab raised to top in control panel. |
| `nil` | Unknown symbol. |

#### Examples

`axlControlRaise('options)`

Raises the option panel to the top.

### axlEnterEvent

`axlEnterEvent( l_eventMask t_prompt g_snap ) => r_eventId`

#### Description

A lower level event manager than other `axlEnter` functions. Provides a Skill program with more user event details. See Table 7-2 for a list of events with descriptions.

Returns event structure containing the attributes described in Table 7-1. Event occurrence controls what attributes are set by all event types, and sets the `objType` and `time` attributes.

Table 7-1 
 Event Attributes

| Name | Description |
|---|---|
| Attribute Name | Type; Description |
| objType | string; Type of object, in this case event |
| type | symbol; Event occurrence |
| xy | point; Location of mouse |
| xySnap | point; Location of mouse snapped to grid. |
| command | int/symbol; Returns the callback item of `axlUIPopupDefine` |
| time | float; time stamp (seconds.milliseconds) |

Note: Do not put a default handler in your case statement since the event model will change in future releases.

Table 7-2 
 Events

| Name | Description |
|---|---|
| Event | Description; Attributes/Mask |
| `PICK` | User has selected a point (equal to `axlEnterPoint`) |
| PICK_EXTEND | Same as `PICK` except has `extend` keyboard modifier. |
| PICK_TOGGLE | Same as `PICK` except has `toggle` keyboard modifier.; xy, xySnap |
| DBLPICK | User has double picked at a location. |
| DBLPICK_EXTEND | Same as `DBLPICK` except has `extend` keyboard modifier. |
| DBLPICK_TOGGLE | Same as `DBLPICK` except has`toggle` keyboard modifier.; xy, xySnap |
| MOVE | Mouse is moving. Depending upon the amount of time spent in your callback, the system may sum mouse movements to minimize falling behind in processing mouse events. |
| STARTDRAG | User starts a drag operation. |
| STARTDRAG_EXTEND | Same as `STARTDRAG` except has `extend` keyboard modifier. |
| STARTDRAG_TOGGLE | Same as `STARTDRAG` except has `toggle` keyboard modifier.; xy, xySnap |
| STOPDRAG | User terminates the drag operation. |
| STOPDRAG_EXTEND | Same as `STOPDRAG` except has `extend` keyboard modifier. |
| STOPDRAG_TOGGLE | Same as `STOPDRAG` except has `toggle` keyboard modifier.; xy, xySnap, command |
| DONE | User requests the command to complete.; This event cannot be masked. |
| CANCEL | Respond to this event by terminating your Skill program (don't call any more axlEnter functions.); This event cannot be masked. |

#### Arguments

| Name | Description |
|---|---|
| `l_eventMask`/`nil` | List of events to expect. |
| `t_prompt`/`nil` | User prompt. If `nil`, the default prompt is used. |
| `g_snapGrid` | If`t`, grid snapping is enabled while the function is active. Otherwise no grid snapping is allowed. This affects the `xySnap` value that is returned as well as dynamics and the `xy` readout. If `nil`, `xySnap` is not snapped to the grid and is the same as `xy`. |

#### Value Returns

| Name | Description |
|---|---|
| `r_eventId` | Event structure containing attributes. |

#### Examples

A complete example is contained in: `<cdsroot>/share/pcb/examples/skill/axlcore/EnterEvent.il`

`let( (eventMask event, loop)`

`eventMask = '( PICK DBLPICK )`

`loop = t`

`while( loop`

`event = axlEnterEvent(eventMask, nil t)`

`case(event->type`

`('PICK`

`... )`

`('DBLPICK`

`... )`

`('DONE`

`; cleanup`

`loop = nil)`

`)`

`)`

`)`

#### See Also

axlEnterPoint and axlSnapEnableAtRMB

### axlEventSetStartPopup

`axlEventSetStartPopup( [s_callback] ) => t/nil`

#### Description

Sets a SKILL callback function called prior to a popup being displayed on the screen. Allows AXL applications to reset the popup (see `axlUIPOPUPSetsee`), thus providing context sensitive popups support.

The callback function is passed a list structure the same as the return list in `axlEnterEvent`. Use this function with `axlEnterEvent`.

The callback function is removed when an AXL application is finished. Set this at the application start, if needed.

#### Arguments

| Name | Description |
|---|---|
| `s_callback` | AXL callback function. |
| none | Unsets the callback function which disables the callback mechanism. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Set SKILL callback function. |
| `nil` | Failed to set SKILL callback function. |

#### Examples

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

Typically used in conjunction with `axlEnterEvent`.

### axlGetTrapBox

`axlGetTrapBox( l_point ) => l_window/nil`

#### Description

Returns coordinates of the Find window.

#### Arguments

| Name | Description |
|---|---|
| `l_point` | Listing of the `x` and `y` coordinates |

#### Value Returns

| Name | Description |
|---|---|
| `l_window` | `((x_l y_l) (x_u y_u))` - List of corner coordinates of the Find window. `(x_l y_l)` - List containing x and y coordinates of the lower left corner. `(x_u y_u)` - List of the x and y coordinates of the upper right corner. |
| `nil` | `l_point` is `null` or in an incorrect format. |

### axlRatsnestBlank

`axlRatsnestBlank( rd_net ) => t/nil`

#### Description

Blanks all ratsnest lines in a net.

#### Arguments

| Name | Description |
|---|---|
| `rd_net` | `dbid` of a net |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Ratsnest lines are blanked. |
| `nil` | Ratsnest lines are not blanked. |

### axlRatsnestDisplay

`axlRatsnestDisplay( rd_net ) => t/nil`

#### Description

Displays all ratsnest lines in a net.

#### Arguments

| Name | Description |
|---|---|
| `rd_net` | `dbid` of a net |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Ratsnest lines are displayed. |
| `nil` | Ratsnest lines are not displayed. |

### axlSetDynamicsMirror

`axlSetDynamicsMirror( g_mirror ) => g_oldmirror`

#### Description

sets mirror option for dynamics

Sets the Dynamics mirroring.

#### Arguments

| Name | Description |
|---|---|
| `g_mirror` | g_mirror type.Possible Values are: `GEOMETRY:`mirror geometry only (same layer) `nil:`mirror none `t:`mirror |

#### Value Returns

old mirror value

#### Examples

`axlSetDynamicsMirror(t`)

#### See Also

axlAddSimpleMoveDynamics

### axlSetDynamicsRotation

`axlSetDynamicsRotation( f_angle/nil ) => f_oldangle`

#### Description

Sets the Dynamics rotation. If angle is nil then returns current rotation.

#### Arguments

| Name | Description |
|---|---|
| `f_angle` | Floating point number |

#### Value Returns

old angle

#### Examples

`axlSetDynamicsRotation(45.0)`

#### See Also

axlAddSimpleMoveDynamics

### axlShowObjectToFile

`axlShowObjectToFile( lo_dbid [t_file_name] ) => (t_file_name x_width x_line_count)`

#### Description

Creates a temporary file with show element information on `dbids` specified in `lo_dbid`.

#### Arguments

| Name | Description |
|---|---|
| `lo_dbid` | List of `dbids` or a single `dbid`. |
| `t_file_name` | File name to use instead of a temporary file. |

#### Value Returns

List of items describing the file created `(``t_file_name x_width x_line_count``)`:

| Name | Description |
|---|---|
| `t_file_name` | Name of the temporary file. |
| `x_width` | Width, in characters, of the widest text line. |
| `x_line_count` | Number of lines in the file. |
| `nil` | Could not create file. |

### axlUICmdPopupSet

`axlUICmdPopupSet( r_popup ) => r_prevPopup`

#### Description

Sets up a popup menu with all menu items required throughout the execution of the command. Call during the command's initialization process. Use of this procedure modifies the behavior of `axlUIPopupSet` so that it makes unavailable all popup items not in the defined popup.

Adds a `cmdPopupId` property to AXL user data which restores popup entries whenever the AXL command state is restored. The command popup is cleared when the Skill command ends.

#### Arguments

| Name | Description |
|---|---|
| `r_popup` | Popup handle, obtained by calling `axlUIPopupDefine`. A `nil` value turns off this popup. |

#### Value Returns

| Name | Description |
|---|---|
| `r_prevPopup` | Popup set previously defined. |

Note: This procedure does the same as `axlCmdPopupSet` for non-WXL UI's.

### axlWindowFit

`axlWindowFit( ) => l_bBox`

#### Description

Zooms in to (or out of) a design fitting it fully on the window. For the Allegro PCB Editor in layout mode, performs a fit on the outline. For the Allegro PCB Editor symbol mode, performs a fit such that all visible objects occupy maximum window area. Returns the bounding box of the window after the fit has been performed.

#### Arguments

`none`

#### Value Returns

| Name | Description |
|---|---|
| `l_bBox` | The bounding box of the window after zooming (in user units). |

Note: This is available as the Allegro PCB Editor command window fit.

### axlZoomBbox

`axlZoomBbox ( x_window ) => bBox`

#### Description

x_window: window id or nil to currently active window. nil is the activewindow and 0 is the primary canvas. Allegro currently onlysupports one additional canvas so the value 1 indicates thatcanvas.

#### Arguments

Returns bounding box (bBox) of window.

#### Value Returns

| Name | Description |
|---|---|
| `bBox` | a list of two xy coordinates indicating upper right and lowerleft. These are in design units. |

#### Examples

- BBox of active window

#### See Also

axlZoomControl

### axlZoomCenter

`axlZoomCenter ( x_window xy ) - => t/nil`

#### Description

`axlZoomBbox(nil) => ((100 120) (300 320))` Zoom centers on the provided coordinate. It may adjust the point if centering results in the display bounding extents are outside thedesign extents.

- If you wish to zoom and center use axlZoomInOut.

#### Arguments

| Name | Description |
|---|---|
| `x_window` | window id or nil to currently active window (see axlZoomBbox) |
| `xy` | Coordiante in design units for centering |

#### Value Returns

| Name | Description |
|---|---|
| `t` | if successful |
| `nil` | an error |

#### Examples

- Create a seconday window and center it

`axlZoomControl('create)``axlZoomCenter(1 4000:4000)`

#### See Also

axlZoomControl

### axlZoomControl

`axlZoomControl ( s_option [g_arg] ) - => g_return`

#### Description

Manages the multi-canvas feature. Requires OpenGL to be enabled.Id 0 is the main Allegro canvas.

Supported options are:

| Name | Description |
|---|---|
| 'create | creates a new canvas. Currently only 1 supported.
 Return - If success returns canvas id, if max canvases already exist or multi-window not supported returns nil |
| 'remove | removes secondary canvas. Cannot remove primarycanvas (id=0). Requires a canvas id for g_arg.
 Return - `t` if canvas removed, `nil` if error |
| 'supported | Is multi-window supported.
 Return - `t` if supported, nil not supported |
| 'list | available canvases |
| 'active | returns the active window id. This impacts the Allegro menu Zoom commands and if you pass nil to the axlZoom APIs
 Return: integer indicating active window |
| 'swap | swaps the primary and secondary window contents.
 Return: t did the swap, nil failed |

#### Arguments

| Name | Description |
|---|---|
| `s_option` | see above |
| `g_arg` | addition argument some options require, see above |

#### Value Returns

| Name | Description |
|---|---|
| `g_return` | depends upon the option, See above |

#### Examples

- Create secondary canvas

`axlZoomControl('create)`

- Remove secondary canvas

`axlZoomControl('remove 1)`

#### See Also

axlZoomBbox axlZoomPoints axlZoomCenter axlZoomWorld

### axlZoomFit

`axlZoomFit ( x_window s_option ) => t/nil`

#### Description

Zoom fits the window. Depending upon the design type fit is define as:

- logic design (brd, mcm, mdd, etc)

Fit to board outline, package and route keepin

- partition (dps, dpf)

Fit to partition boundary

- symbol (dra) - all visible objects

#### Arguments

| Name | Description |
|---|---|
| `x_window` | window id or nil to currently active window (see axlZoomBbox) |
| `s_option(visible)` | if logic or parition design fit to visible objects |

#### Value Returns

| Name | Description |
|---|---|
| `t` | if successful |
| `nil` | an error |

#### Examples

- Fit primary window to visible objects

`axlZoomFit(0 visible)'`

#### See Also

axlZoomControl

### axlZoomInOut

`axlZoomInOut ( x_window x_factor [xy] ) => t/nil`

#### Description

Zooms window in or out by provided factor around optional coordinate.

#### Arguments

| Name | Description |
|---|---|
| `x_window` | window id or nil to currently active window (see axlZoomBbox) |
| `x_factor` | factor to zoom, a positive number zooms in while negative zooms out. 1 is 2x, 2 is 4x, 3 is 8x etc. |
| `xy` | optional coordinates to zoom around. If not provided uses center of current window |

#### Value Returns

| Name | Description |
|---|---|
| `t` | if successful |
| `nil` | an error |

#### Examples

- zoom in by 2x primary window

#### See Also

axlZoomControl

### axlZoomPoints

`axlZoomPoints ( x_window upperLeft_xy lowerRight_xy ) => t/nil`

#### Description

`axlZoomInOut(0 1)` Zoom windows by points. The zoom maintains a 1:1 aspect ratio,the coordinates provided will be fitted into the active window size.

#### Arguments

| Name | Description |
|---|---|
| `x_window` | window id or nil to currently active window (see axlZoomBbox) |
| `upperLeft_xy` | upper left coordiante |
| `lowerRight_xy` | lower right coordiante |

#### Value Returns

| Name | Description |
|---|---|
| `t` | if successful |
| `nil` | an error |

#### Examples

- zoom by points on the primary window

#### See Also

axlZoomControl

### axlZoomToDbid

`axlZoomToDbid( o_dbid/lo_dbid g_always [x_window] ) => t/nil`

#### Description

`axlZoomPoints(0 100:120 4000:4000)` Processes a list of `dbids` and centers and zooms the display around them. Zoom is done so objects extents fill about 20% of the display. You should highlight the objects.

Note: If more than 20 objects are passed no zoom is done.

#### Arguments

| Name | Description |
|---|---|
| `o_dbid` | List of `dbids` or one `dbid`. |
| `g_always` | If`t,` then ignores `NO_ZOOM_TO_OBJECT` environment variable. |
| x_window | Optional window ID or `nil` to currently active window (see axlZoomBbox). If no value is provided active window is used. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | One or more objects zoomed. |
| `nil` | No valid `dbids` or all objects are already at desired display state. |

#### Examples

- Zoom to U1

`sym = axlDBFindByName('refdes "U1")`

`axlZoomToDbid(sym t)`

#### See Also

axlZoomManage

### axlZoomWorld

`axlZoomWorld ( x_window ) => t/nil`

#### Description

Zoom world a drawing window

#### Arguments

| Name | Description |
|---|---|
| `x_window` | window id or nil to currently active window (see axlZoomBbox) |

#### Value Returns

| Name | Description |
|---|---|
| `t` | if successful |
| `nil` | an error |

#### Examples

- world the active window

#### See Also

axlZoomControl

### axlMakeDynamicsPath

`axlMakeDynamicsPath( l_formatedList ) => r_path/nil`

#### Description

`axlZoomWorld (nil)` This is a convenience function to construct an `r_path` from a formatted list. `axlDBCreate` and `axlPoly` require an `r_path.`

Note: A circle is an arc segment with same end points.

Note: Caution: Passing an illegal format may result in a bad return.

#### Arguments

| Name | Description |
|---|---|
| `( l_seg1 l_seg2 ...) g_clockwise` | Each `l_seg` is:
 ( `l_startPoint l_endPoint [f_width] [l_center] [f_radius]) l_startPoint:`Start point of path. `l_endPoint:`End point of path. `f_width:` Optional width (default of 0). `l_center:`Optional center point if `r_path` is an arc. `f_radius:`Optional radius if `r_path` is an arc.
 If an arc `r_path,` both`l_center` and `f_radius` must be provided. |
| `g_clockwise` | Direction to create arc:
 t ⇒ create arc clockwise from start to endpoint.
 nil ⇒ create counterclockwise. Default is counterclockwise. |

#### Value Returns

| Name | Description |
|---|---|
| `r_path` | `dbid` of `r_path`. |
| `nil` | No `r_path` constructed due to incorrect arguments. |

#### Examples

Simple `r_path` segment with a width of 20.

`a = axlMakeDynamicsPath(list(list( 10:10 100:100 20)))`

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

