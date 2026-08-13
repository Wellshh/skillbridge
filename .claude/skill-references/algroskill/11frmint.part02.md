<!--
source: algroskill/11frmint.md
part: 2/3
estimated_tokens: 13486
-->

[{default\_button\_def}]
 [{popup\_def}]
 [{message\_def}]

#### *default\_button\_def*

DEFAULT <label>
 - sets the default button to be <label>. If not present form sets default button to
 one of the following:
 ok (done), close, cancel.
 - label must be of type MENU\_BUTTON.

#### *popup\_def*

* POPUP <<popupLabel>> {"<display>","<dispatch>"}.
* popups may be continued over several lines by using the backslash (\) as the last character on line.
* popups work slightly differently when applied to fillin versus other supporting fields, such as, ENUMs and BUTTONs. With Fillin fields, such as, Strings and long, the display portion is always sent back to the application while other supporting field types, such as, ENUMs, send the dispatch portion.

#### *message\_def*

MESSAGE messageLabel messagePriority "text".

#### *form\_options*

[TOOLWINDOW]
 - this makes a form to be a tool window which is a floating toolbar. It is typically
 used as a narrow temp window to display readouts.

[FIXED\_FONT]
 - by default forms use a variable width font, this sets this form to use a fixed
 font. Allegro PCB Editor uses mostly variable width while Allegro PCB SI and
 SigXplorer use fixed width fonts.

[AUTOGREYTEXT]
 - when a fillin or enum control is greyed, grey static text to the left of it.

[NOFOCUS]

- when a form opens focus is set to form window which allows you to immediately enter data. If you create a form with no editable fields or don't wish to have the form grab focus set this option.

[UNIXHGT]
 - works around a problem with Mainsoft in 15.0 where a button is sandwiched
 vertically between 2 combo/fillin controls. The button then overlaps these
 controls. This adds extra line-2-line spacing to avoid this. You should only use
 this option as a last resort. In a future release it may be treated as a Nop.
 On Windows this is ignored.

#### *tile\_def*

TILE [<tileLabel>] (4)
 [TPANEL tileType]
 [{text\_def}]
 [{group\_def}]
 [{list\_def}]
 [{field\_def}]
 [{button\_def}]
 [{grid\_def}]
 [{flex\_def}]
 ENDTILE

#### *tabset\_def*

TABSET [label]
 [OPTIONS tabsetOptions]
 FLOC x y
 FSIZE w h
 {tab\_def}
 ENDTABSET

#### *tab\_def*

TAB "<display>" [<label>] (10)
 [{text\_def}]
 [{group\_def}]
 [{field\_def}]
 [{grid\_def}]
 ENDTAB

#### *text\_def*

TEXT "display" [label] (9)
 FLOC x y
 [FSIZE w h] (8)
 text\_type
 [OPTIONS textOptions]
 ENDTEXT

#### *text\_type*

[INFO label w]
 [THUMBNAIL [<bitmapFile>|#<resource>] ]

#### *group\_def*

GROUP "display" [label] (9)
 FLOC x y
 FSIZE w h (8)
 [INFO label]
 ENDGROUP

#### *list\_def*

FIELD label
 FLOC x y
 LIST "" w h
 list\_options
 ENDFIELD

#### *field\_def*

FIELD label
 FLOC x y
 [FSIZE w h] (8)
 [HELPTIP "tip"] (12)
 field\_type
 field\_options
 ENDFIELD

#### *button\_def*

FIELD label
 FLOC x y
 [FSIZE w h] (8)
 MENUBUTTON "display" w h
 [OPTION button\_options
 [button\_bitmap]

ENDFIELD

#### *grid\_def*

```
GRID fieldName	FLOC x y	FSIZE w h               (8)	[OPTIONS INFO | HLINES | VLINES | USERSIZE | MULTISELROW ]	[POP "<popupName>"]
```

```
[GHEAD TOP|SIDE]		[HEADSIZE h|w]	[OPTION 3D|NUMBER|MULTI]	[POP "<popupName>"]	[ENDGREADH]	ENDGRID
```

#### *field\_type*

REALFILLIN w fieldLength
 LONGFILLIN w fieldLength
 STRFILLIN w fieldLength
 INTSLIDEBAR w fieldLength
 ENUMSET w [h] | (11)
 CHECKLIST "display" ["radioLabel"]
 LIST "" w h
 TREEVIEW w h
 COLOR w h
 THUMBNAIL [<bitmapFile>|#<resource>]
 PROGRESS w h
 TRACKBAR w h

#### *field\_options*

The OPTIONS line permits multiple options

[INFO\_ONLY]
 - sets field to be read only.

[POP "<popupName>"]
 - assigns a popup with the field.
 - a POPUP definition by the same name should exist.
 - supported by field\_types: xxxFILLIN, INTSLIDEBAR, MENUBUTTON,
 ENUMSET

[MIN <value>]
 [MAX <value>]
 - assigns a min and/or max value that field might have.
 - both supported by field\_types: LONGFILLIN, INTSLIDEBAR, REALFILLIN.
 - value by either by an integer or floating point number.

[DECIMAL <accuracy>]
 - assigns a floating min and/or max value that field might have.
 - assigns number of decimal places field has (default is 2)
 - both supported by field\_types: REALFILLIN

[VALUE "<display>"]
 - initial field value.
 - supported by field\_types: xxxFILLIN

[SORT]
 - alphanumberic sorted list (default order of creation)
 - supported by field\_type: LIST

[OPTIONS dispatchsame]
 - for enumset fields only.
 - if present will dispatch to application drop-down selection even if the same
 as current. By default, the form's package filters out any user selection if it is
 the same as what is currently displayed.

[OPTIONS prettyprint]
 - for enumset fields only
 - displays contents of ENUM field in a visually pleasing way

[OPTIONS ownerdrawn]
 - for enumset fields only
 - used to display color swatches in an ENUM field. See`axlFormBuildPopup.`

|  |
| --- | ---
|  | [OPTIONS space]
|  | - string type only  - preserves leading and trailing white space. By default this is stripped.
|  | [OPTIONS dropfile]
|  | - string and multiline types only  - Allows a file to be dropped into the field (Windows drag and drop)    Shortcuts are not resolved.
#### *list\_options*

[OPTIONS`sort|alphanumsort|prettyprint|multiselect`]
 sort - convertion alphabetical sort
 alphanumsort - sort so NET10 appears after NET2
 prettyprint - make more readable, convert case.
 All dispatch entries will be upper case multiselect - multi-select list box.
 User can select more then one item (follows Microsoft selection model).

#### *x y w h*

- display geometry (integers).
 - all field, group and text locations are relative to the start of the tile they
 belong or to the start of the form in the case of FIXED forms.
 - x & h are in CHARHEIGHT/2 units.
 - y & w are in CHARWIDTH units.

#### *button\_options*

[MULTILINE]
 - wraps button text to multiple lines if text string is too long for a single line.

#### *button\_bitmap*

> > `[BITMAP [<bitmapFile>|#<resource>] ]`

> > > - display a bitmap for this button.

#### *dispatch*

- string that is dispatched to the code.

#### *display*

- string that is shown to user

#### *bitmapFile*

- name of a bmp file. Can be found via BMPPATH. Bitmap should be static. Animation should not be used.

- #<resource> only available for Cadence applications. It is obsolete.

#### *resource*

- integer resource id (bitmap must be bound in executable via the resource
 file). '#' indicates it is a resource id.
 - not support in AXL forms.

#### *fieldLength*

- maximum width of field. Field will scroll if larger then field display width.

#### *label*

- named used to access field from code. All fields should have unique names.
 - should use lower case.

#### *messageLabel*

- name used to allow code to refer to messages.
 - case insensitive

#### *messagePriority*

- message priority 0 - info (not in journal file), 1 - info, 2 - warning, 3 - error, 4
 fatal (display in message box).

#### *radioLabel*

- named used to associate several CHECKLIST fields as a radio button set.
 All check fields should be given the same radioLabel.
 - should use lower case.

#### *textOptions*

|  |
| --- | ---
|  |
 RIGHT | CENTER | BORDER | BOLD | UNDERLINE]  - TEXT/INFO field type.  - text justification, default is left.  - BORDER: draw border around text.
|  |
| --- | ---
|  | [INVISIBLE]  field by default is not displayed
|  |
| --- | ---
|  |
 [STRETCH]  - THUMBNAIL field type.  - stretch bitmap to fit thumbnail rectangle, default is center bitmap.
|  |
| --- | ---
|  |
 [MAP3DCOLORS] THUMBNAIL field type.  - search the color table of the`.bmp` and replace the following shades of gray with corresponding 3D color:
dk gray RGB(128,128,128) - COLOR\_3DSHADOW

gray RGB(192,192,192) - COLOR\_3DFACE

lt gray RGB(223,223,223) - COLOR\_3DLIGHT

This option is typically used to blend the`.bmp`'s background color with the user's dialog background. If using this option, don't reserve these 3 gray colors for background only.

#### *tabsetOptions*

tabsetDispatch]
 - By default tabsets dispatch individual tabs as separate events. This is not
 always convenient for certain programming styles. This changes the dispatch
 mode to be upon the tabset where a selection of a tab causes the event`field=tabsetLabel value=tabLabel`.
 The default is:
 `field=tabLabel value=t` Script record/replay remains based upon tab in either mode.

#### *gridOptions:*

Several of these options can also be controlled at run-time via UIFGridVarEvents or UIFGridVarOptions:

|  |  |
| --- | --- | ---
|  |  | INFO - grid is for info only; can be scrolled but items cannot be selected
|  |  |
| --- | --- | ---
|  |  | HLINES - display horizontal separator lines
|  |  |
| --- | --- | ---
|  |  | VLINES - display vertical separator lines
|  |  |
| --- | --- | ---
|  |  | USERSIZE - user can resize columns
|  |  |
| --- | --- | ---
|  |  | MULTISELROW - grid is opened in multi-select row mode
#### *gHeadOptions:*

|  |  |
| --- | --- | ---
|  |  | 3D - display header in 3d mode
|  |  |
| --- | --- | ---
|  |  | NUMBER - auto-number side header (default is blank)
|  |  |
| --- | --- | ---
|  |  | MULTI - display top header as multiple lines (default single line with clipping)
#### *tileLabel*

- name used to allow code to refer to this tile.
 - should use lower case.
 - only applies to VARIABLE forms.
 - not support with AXL forms.

#### *tileType [0|1|2]*

- 0 top tile, 1 scroll tile, 2 bottom tile.
 - only applies to VARIABLE FORMS.
 - region where tile will be instantiated. Forms have 3 regions top, bottom and scroll (middle).
 - not support with AXL forms.

#### *flex\_def- rule based control sizing upon form resize (see axlFormFlex)*

[FLEXMODE <autorule> [minWidth minHeight]]
 [FLEX <label> fx fy fw fh]

#### FLEXMODE <autoRule> [minWidth minHeight] FLEX fx fy fw fz- see [`axlFormFlexDoc`](#461527 "11")

#### *autorule- generic sizing placement rule*

fx
fy
fw
fh

- floating value between 0 and 1.0

#ifdef:

#ifndef:

#else:

#endif:

* - Conditionally read portions of the form file based upon the settings of Allegro environment variables
  - These statements may be nested.

|
| ---
|
  | - Note the negation character '!' was added in 15.7. Forms using this capability will not function correctly in earlier releases.
Use #ifdef/#endif and #ifndef/#endif to make items conditionally appear in the menu depending on whether a specified environment variable is set.

An #ifdef causes the form item(s) to be ignored unless the environment variable is set. You must have one #endif for each #ifdef or #ifndef to end the block of conditional menu items. Also, the #ifdef, #ifndef and #endif must start at the first column of its line in the formfile. The #ifndef is the negation of #ifdef.

The #else statement may be inserted between the #if/#endif statements.

The condition syntax supports multiple variables with OR '||' or AND '&&' conditions. Also the negation character '!' is supported for the variables:

The simple syntax is:

#ifdef <env variable name>

[form items which appear if the env variable is set]

#endif

#ifndef <env variable name>

[form items which appear if the env variable is NOT set]

#endif

# logically equivalent to above state using negation character

#ifdef !<env variable name>

[form items which appear if the env variable is not set]

#endif

#ifdef <env variable name>

[form items which appear if the env variable is set]

#else

[form items which appear if the env variable is set]

#endif

Also logical statements:

1) if variable1 and variable2 are both set do the included statement

#ifdef <var1> && <var2>

[form items which appear if both variables are set]

#endif

2) if either variable1 or variable2 is do the included statement

#ifdef <var1> || <var2>

[form items which appear if either variable is set]

#endif

**Note:**

* FILE\_TYPE line must always appear as the first line of form file in format shown.

* Form files must have a .form extension.

* There may only be one FORM in a form file.

* There must be one and only one TILE definition in a FIXED form file. <tileLabel> and TPANEL are not required.

* Unless otherwise noted limits are as follows:
  labels - 128
  title - 1024
  display - 128 except for xxxFILLIN types which are 1024

* Additional items may appear in existing form files (FGROUP) but they are obsolete and are ignored by the form parser. REALMIN & REALMAX are obsolete and replaced by MIN and MAX respectively. They will still be supported and are mapped to MIN and MAX.

* For grid\_def two headers (side and top) are maximum.
  SIZE - most controls determine the size from the text string. You are required to provide FSIZE for GROUP, GRID, TREEVIEW and LIST controls. For TEXT controls if FSIZE is provided after it overrides the width calculated by the text length and if present the INFO width. If the INFO line appears you should put the FSIZE line after it.

* Both TEXT and GROUP support optional label on their definition line. This was added as a convenience in supporting FLEX capability. If application wishes to dynamically modify the text the INFO keyword is normally used. When both are present the INFO keywords takes precedence.

* If the optional label for TABS is not provided, the field display name is used. Any spaces within the field display name are replaced by underscores ("\_").

* The height ([h]) for ENUMSET is option. When not set (the default) the drop-down is only presented under user control. When height greater then 1 then the drop-down is always visible (Microsoft SIMPLE drop-down). You only want to use this feature in forms that can afford the space consumed by the drop-down.

* HELPTIP supports ability to associated short help with the field. You should also define a INFO field with the label helptip somewhere in your form.

* Options should appear after the fieldtype and MULTILINE in button type.

-----------------------------------------------------------------------------------------------------------------------

The forming syntaxes are NOT supported by the formeditor.

This following syntax is supported and may be placed anywhere in the form file to support conditional processing of the form file:

#ifdef <variable>
{ }

{ #elseif <variable>
 }

{ #else
{ } }

### axlFormCallback

`formCallback([r_form])==> t`

#### Description

This is not a function but documents the callback interface for form interaction between a user and Skill code. The Skill program author provides this function.

When the user changes a field in a form the Allegro form processor calls the procedure you specified as the`g_formAction` argument in `axlFormCreate` when you created that form. The form attribute `curField` specifies the name of the field that changed. The form attribute `curValue` specifies the current value of the field (after the user changed it). If you set `g_stringOption` to `t` in your call to `axlFormCreate` when you created that form, then `curValue` is a string. If `g_stringOption` was `nil` (the default), then `curValue` is the type you specified for that field in the form file.

**Note:** The term`formCallback` used in the title of this callback procedure description is a dummy name. The callback function name must match the name or symbol name you used as the `g_formAction` argument in `axlFormCreate` when you created the form.

If you specify the callback name (`g_formAction`) as a string in your call to `axlFormCreate`, SKILL calls that function with no arguments. If you specify `g_formAction` as a symbol, then SKILL calls that function with the form handle as its single argument.

The callback must call`axlFormClose` to close the form and to continue in the main application code if form mode is blocking.

All form information is provided by the`r_form` argument which is a form data type. Applications can extend the data stored on this type by adding their own attributes.
Capitalize the first letter of the attribute name to avoid conflicts with future additions by Cadence to this structure. Tables 1 and 2 show the available field types and how they impact the `r_form` data type.

#### Table 1

#### *Form Field Types:*

Type What the field is commonly known to the user.

Keyword How the field is declared in the form file (see`axlFormBNF`Doc).

curValue The data type seen in the form dispatch and`axlFormGetField` (see
 `axlFormCallback`).

curValueInt If`curValue` can be mapped to an integer. For certain field types provides
 additional information.

|  |  |  |
| --- | --- | --- | ---
| **Type** | **Keyword** | **cuValue** | **curValueInt**
| Button | MENUBUTTON (6) | t | 1
| Check Box | CHECKLIST (1) | t / nil | 1 or 0
| Radio Box | CHECKLIST (1) | t / nil | 1 or 0
| Long (integer) | INTFILLIN | integer | integer
| Real (float) | REALFILLIN | floating point | N/A
| String | STRFILLIN | string | N/A
| Enum (popup) | ENUMSET | string | integer (2)
| List | LIST | string | index
| Color well | COLOR | t / nil | 1 or 0
| Tab | TABSET/TAB | string or t (3) | N/A or 1/0
| Tree | TREEVIEW | string | See: axlFormTreeViewSet
| Text | INFO (4) | N/A | N/A
| Graphics | THUMBNAIL (5) | N/A | N/A
| Trackbar | TRACKBAR | integer | integer
| Grid | GRID | See: axlFormGridDoc |
**Note:**

* What distinguishes between a radio button and check box is that radio buttons are a group of check boxes where only one can be set. To relate several check boxes as a set of radio buttons, use supply the same label name as the third field (groupLabel) in the form file description:

`CHECKLIST <fieldLabel> <groupLabel>`

When a user sets a radio button the button be unset will dispatch to the app's callback with a value`nil`.

* Enum will only set`curValueInt` on dispatch when the dispatch value of their popup uses an integer. Otherwise this field is `nil`.

* Tabs can dispatch in two methods:

|  |  |
| --- | --- | ---
|  |  | default when a tab is selected your dispatcher receives the tab name in the`curField` and `curValue` is `t`.
|  |  |
| --- | --- | ---
|  |  | If`OPTIONS tabsetDispatch` is set in the TABSET of the form file then when a tab is selected your app dispatcher receives the TABSET as the `curField` and the `curValue` being the name of the TAB that was selected.
* INFO fields can be static where the text is declared in the form file or dynamic where you can set the text via the application at run-time. To achieve dynamic access enter the following in the form file:

`TEXT "<optional initial text>"`

`INFO <fieldLabel>`

... reset of TEXT section ...

* Thumbnails support three methods:

|  |  |
| --- | --- | ---
|  |  | Static bitmap declared via form file.
|  |  |
| --- | --- | ---
|  |  | Bitmaps that can by changed by the application at run-time.
|  |  |
| --- | --- | ---
|  |  | Basic drawing canvas (see`axlGRPDoc`).
* Buttons are stateless. The application cannot set the button to the depressed state. You can only use`axlFormSetField` to change the text in the button. Several button fieldLabels are reserved. Use them only as described:

   *Done* or *Ok* Do action and close form.
  *Cancel* Cancel changes and close form.
  *Print* Print form; do not use.
  *Help* Call cdsdoc for help about form. Do not use.

#### Table 2

|  |  |  |
| --- | --- | --- | ---
| **Attribute Name** | **Set?** | **Type\*** | **Description**
| curField | no | string | Name of form field (control) that just changed.
| curValue | no | See-> | Value dependant upon field type (2).
| curValueInt | no | See-> | Value dependant upon field type (2).
| doneState | no | int | 0 = action; 1 = done; 2 = cancel; 3 = abort (1)
| form | no | string | Name of this form (form file name).
| isChanged | no | `t` / `nil` | `t`= user has changed one or more fields.
| isValueString | no | `t` / `nil` | `t` all field values are strings. `nil`one or more fields are not strings.
| objType | no | string | Type of object; in this case`form.`
| type | no | string | Always`fixed.`
| fields | no | list of strings | All fields in the form (3).
| infos | no | list of strings | All info. fields in form (3).
| event | no | symbol | List, tree and grid control only. See`axlFormGridDoc` for grid info, otherwise see bullets 4 and 5 in the following ***Note*** section.
| row | no | integer | Grid control only.
| col | no | integer | Grid control only.
| treeViewSelState | no | integer | Tree control only.
**Note:**

* The`doneState` shows 0 for most actions. If a button with *Done* or *Ok* is pushed, then the done state is set. A button with the *Cancel* label sets the cancel state.
  In either the Done or Cancel state, you need to close the form with `axlFormClose`. If the abort state is set, the form closes even if you do not issue an `axlFormClose`.

* Data type is dependant upon the field type, see Table 1.

* The difference between the fields and infos list is that items appearing in the infos list are static text strings that can be changed by the program at the run-time. All other labels appear in the fields list and can be changed by the user (even buttons, tabs, greyed and hidden fields).

* Event for list box is`t`if item is selected, `nil` if deselected. This is always `t` for single select list box while the multi-select option can have both states.

* Event and treeViewSelState for a tree control see`axlFormTreeViewAddItem`.

#### Arguments

`r_form` Form dbid.

#### Value Returned

`t`Always returns `t`.

#### Examples

See`axlFormCreate` and `axlFormBuildPopup` examples.

### axlFormCreate

```
axlFormCreate(s_formHandlet_formfile/(t_formName t_contents)/(t_formName (t_contents))[lt_placement]g_formActiong_nonBlock[g_stringOption])⇒ r_form/nil
```

#### Description

Creates a dialog based on the form descriptive file`t_formfile`. This call only supports forms of type `"fixed"` and fails if `t_formfile` contains any variable tiles. This function does not display the form. Use `axlFormDisplay` to display a form.

An alternative interface is supported that allows embedding the contents of the form file in the skill code. Instead of passing the external form file name provide the name (t\_formName) for scripting purposes and form file contents (t\_contents) as string. The packaged skill code has a example of this method at the end of the`<cdsroot>``/share/pcb/examples/form/finline.il` file. This method has the advantage of only distributing one file.

Rules to remember when creating this form content string:

* Every non-blank line must have a tab character

> Example:

> > `FILE_TYPE=FORM_DEFN VERSION=2`

* Any embedded quotes must be escaped (use backslash '\')

> Example:

> > `MENUBUTTON \"Ok\" 10 3\n`

* Any paraenthesis '()' must be escaped '\'

**Note:** If`s_formHandle` is an existing `r_form`, then `axlFormCreate` does not create a new form, but simply exposes and displays the existing form, `s_formHandle`, and returns `nil`.

#### Arguments

* Global SKILL symbol used to reference form.**Note:** Do not use the same symbol to reference different form instances.
* `t_contents`: the list with string format
* `t_formName`: Name of form (used for scripting)
* `(t_contents)`: Contents of form file. This may be a string or a list containing or a string. The string format is obsolete and you should use `t_contents`
* Form placement. Allegro PCB Editor uses its default placement if this argument is`nil`. See [Window Placement](10usrint.html#101699 "10")
* Specifies the SKILL commands (callbacks) to be executed after every field change (Note that this is very different from Cadence IC forms). You can set this to one of the formats shown:
* `Action` Options

|  |
| --- | ---
| **Option** | **Description**
| `t_callback` | String representation of the SKILL command to be executed.
| `s_callback` | Symbol of the SKILL function to be called (passes the`r_form` returned from `axlFormCreate` as its only parameter.)
| `nil` | `axlFormDisplay` blocks until the user closes the form.You must place a *Done* button (field name `done`) and optionally a *Cancel* button (field name `cancel`) in the form for `g_formAction` to function properly. The user can access all of the fields and values using the `r_form` user type.
|  |
| --- | ---
| `g_nonBlock` | If`g_nonBlock` is `t`, the form runs in non-blocking mode. In blocking mode (the default), `axlFormDisplay`blocks until the user closes the form. Blocking is an easier programming mode but might not be appropriate for your application. If the callback (`g_formAction`) is `nil`, then `axlFormDisplay` ignores `g_nonBlock`, and the form runs in blocking mode.  Use of blocking mode blocks the progress of the SKILL code, but does not prevent other Allegro PCB Editor events from occurring. For example, if blocked, users can start the*Add Line*command from Allegro PCB Editor menus.
| `g_stringOption` | If`t,` the form returns and accepts all values as strings. By default, it returns and accepts values in the format declared in the form file.
#### Value Returned

|  |
| --- | ---
| `r_form` | `dbid` of form created.
| `nil` | No form created.
#### Example

See`<cdsroot>/share/pcb/examples/form`

> basic: demostrates basic form capabilities

> > finline.il shows correct inline method

> grid: demostrates grid control capabilites

> wizard: form when used in a Wizard mode

> finline: demostrates inline option to avoid having a .form file

See[AXL Forms: Example 1](#461771 "11").

#### See Also

* axlFormIntroDoc: Introduction to the Allegro Form Package.

* axlFormBNFDoc: Form file language description

* axlFormCallback: Methods and structures for interacting with user.

### axlFormClearMouseActive

`axlFormClearMouseActive(r_form)==> t/nil`

#### Description

Clears the option to dispatch the MouseActive event on a form.

#### Arguments

|  |
| --- | ---
| `r_form` | Handle for the form
#### Value Returned

|  |
| --- | ---
| `t` | Option was cleared
| `nil` | r\_form does not reference a valid form
### axlFormClose

`axlFormClose(r_form)⇒ t/nil`

#### Description

Closes the form`r_form`. Unless the form is running without a callback handler, you must make this call to close the form. Without a registered dispatch handler, Allegro PCB Editor closes the form automatically before returning to the application from `axlFormDisplay`.

**Note:** `axlUIWClose` also performs the same function.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
#### Value Returned

|  |
| --- | ---
| `t` | Closed the form.
| `nil` | Form was already closed.
#### Example

See[AXL Forms: Example 1](#461771 "11"):

> ```
> (case form->curField         ("done"             (axlFormClose form)             (axlCancelEnterFun)             (_extract)             t)
> ```

### axlFormDisplay

`axlFormDisplay(r_form)⇒ t/nil`

#### Description

Displays the form`r_form` already created by `axlFormCreate`. For superior display appearance, set all the field values of the form before calling this function. A form in blocking mode blocks until the user closes the form.

If a form is already displayed, this function simply exposes it.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
#### Value Returned

|  |
| --- | ---
| `t` | Successfully opened or exposed the form.
| `nil` | Failed to open or expose the form.
#### Example

See[AXL Forms: Example 1](#461771 "11").

> `axlFormDisplay( form)`

### axlFormBuildPopup

`axlFormBuildPopup(r_formt_fieldl_pairs)⇒ t/nil`

#### Description

This provides the ability to dynamically change popups of fields that have them. These fields are enum (or pop-up) and other fields that have a popup icon. Buttons, optionally, may also have a popup if they have a right arrow. Attempting this call on a field without a popup is an error.

#### Arguments

* a form handle
* Name of form field.
* May be one of four formats where each element is a single popup entry. A maximum of 256 popup entries are allowed.
* normal
* alternative normal
* for enum field types

> > **Note:**

> > All entries in an`l_pairs` argument must be the same type of format. That is, you cannot have a list containing, for example, both display/dispatch strings and display/enum types, or display/dispatch and single-string entries.

> > > Must be one of the formats described. Each list object defines a single popup entry.

****Table 11-3****
**l\_pairs Format Options**

| **Option** | **Description** | **Example**
| List of lists of string pairs | The first member of each string pair list is the display value-the string displayed in the pop-up. The second member of each string pair is the dispatch value-the string value returned as`form->curValue`when the user selects that pop-up entry. | `(list (list "MyPop A" "myvalue_a")`  `list("MyPop B" "myvalue_b"))`
| List of lists of pairs | List of lists of pairs where the first member of each pair is a string giving the display value, and the second member is an integer that is the dispatch value, returned as`form - curValue` when the user selects that pop-up entry.  You can use the return value as an index into an array. | `(list (list "MyPop A" 5)        list("MyPop B" 7))`
| List of strings | Uses each string both for display value and the return value. | `(list "MyPop A" "MyPop B")`
| Optional field | Specifies a color swatch. This is currently only supported by ENUM field types (it is ignored by other field types). With an ENUM you need to add`OPTIONS ownerdrawn` in the form file for the FIELD in question to see the color swatch in the popup. You can use either pre-defined color names (see `axlColorDoc`) or Allegro board colors (see `axlLayerGet`). | You can't mix this color type in a single popup.    `'(("Green" 1 green) ("Red" 2 red) ("Yellow" 3 yellow))`    `'(("Top" "top" 2) ("Gnd "gnd" 4) ("Bottom" "btm" 18))`  If instead of a color or Allegro color number, you provide a`nil,` then that popup entry will not have a color swatch.  `'("(None" 0 nil) ("Green" 1 green) ("Red" 2 red)`  `("Yellow" 3 yellow))`  Font type of bold or underline can be specified via:  `'(("Top" "top" bold) ("Gnd "gnd" underline) ("Bottom" "btm"))`  When font type is combined with color it looks like:  `'(("Top" "top" "Green" bold) ("Gnd "gnd" "Red" underline)`
**Notes:**

* Allows a maximum of 1000 pop-up entries in one pop-up.

* If creating a dynamic popup (entries created under program control) a dummy entry must exist in the form file or build popup will fail. Example:

> > `<popupname> """".`

* The field name is actually a search mechanism. We first search the fields for the field name with a popup and then search the popup names. Since the only way to change grid column or cell based popups is by popup name you may run into failures if that popup name has the same name as another field in the form.

#### Value Returned

|  |
| --- | ---
| `t` | Field set.
| `nil` | Field not set.
#### Example

See[AXL Forms: Example 2](#415159 "11").

### axlFormGetField

`axlFormGetField(r_formt_field)⇒ g_value/nil`

#### Description

Gets the value of`t_field` in the open form`r_form`. The value is a string if `g_stringOption` was set in`axlFormCreate`. Otherwise the value is in the field type declared in the form file.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_field` | Name of field.
#### Value Returned

|  |
| --- | ---
| `g_value` | Current value of the field.
| `nil` | Field does not exist, or false if boolean field such as check box or radio button.
#### Example

* Load the example code given in[AXL Forms: Example 1](#461771 "11").

* Enter the command`myExtract()` on the SKILL command line.

> The command displays the**Extract Selector** form, listing all available extract view files.

* Select any file in the list, or type a name into the*View File* field.

> `allegro2rlb_view.txt` is entered.

> `axlFormGetField( form "view_file")        ⇒ "allegro2rlb_view.txt"`

Examines the value of "`view_file`" .

### axlFormGridSelected

`axlFormGridSelected(r_formt_field) -> lx_selected/nil`

#### Description

This returns the selected item in a multi-select grid control. This should only be used if grid is running with the multi-select row option.

#### Arguments

|  |
| --- | ---
| `r_form` | standard form handle
| `t_field` | standard field name
#### Value Returned

Returns list of selected items in a multi-select grid or nil if not the correct control.

#### See Also

[axlFormGridNewCell](#459451 "11")

#### Examples

See`fgrid.il` in `<CDSROOT>``/share/pcb/examples/skill/form/grid`

Pseudo code:

`axlFormGridEvents(fg "grid" 'mrowselect)`

`;; select items`

`selected = axlFormGridSelected(fg "grid")`

`; if form select rows 5,6,7 (click on 5, then Shift click on 7)`

`;; select items`

`selected = axlFormGridSelected(fg "grid")`

`-> (5 6 7)`

### axlFormGridSelectedCnt

`axlFormGridSelectedCnt(r_formt_field) -> x_cnt/nil`

#### Description

This returns the count of rows selected in a multi-select grid control. This should only be used if grid is running with the multi-select row option.

#### Argument

|  |
| --- | ---
| `r_form` | standard form handle
| `t_field` | standard field name
#### Value Returned

Returns count of selected items or`nil` if wrong type of control

#### See Also

[axlFormGridNewCell](#459451 "11")

#### Examples

See`fgrid.il` in `<CDSROOT>``/share/pcb/examples/skill/form/grid`

Pseudo code:

> `axlFormGridEvents(fg "grid" 'mrowselect)`

> `; if form select rows all rows (Ctrl-A in grid)`

> `;; select items`

> `selected = axlFormGridSelectedCnt(fg "grid")`

> `-> 16`

### axlFormGridSetSelectRows

`axlFormGridSetSelectRows(r_formt_fieldx_minx_maxg_option) -> x_cnt/nil`

#### Description

This allows setting, clearing or toggling of selection state for a grid in multi-select row mode.

#### Arguments

|  |
| --- | ---
| `r_form` | standard form handle
| `t_field` | standard field name
| `x_min` | min row number
| `x_max` | max row number
| `g_option` | what to do
|  | `t` - set row as selected
|  | `nil` - clear row as selected
|  | `'toggle` - toggle selected state of row
#### Value Returned

`t` if succeeded, `nil` if not a grid field or not in multi-row select mode

#### See Also

[axlFormGridNewCell](#459451 "11")

#### Examples

See`fgrid.il` in `<CDSROOT>``/share/pcb/examples/skill/form/grid`

Pseudo code:

> `axlFormGridEvents(fg "grid" 'mrowselect)`

* set row 4 as selected

> `axlFormGridSetSelectRows(fg "grid" 4 4 t)`

* clear rows 4 thru 8 being selected

> `axlFormGridSetSelectRows(fg "grid" 4 8 t)`

* clear all rows

> `axlFormGridSetSelectRows(fg "grid" -1 -1 nil)`

* toggle state of row 1

> `axlFormGridSetSelectRows(fg "grid" 1 1 'toggle)`

### axlFormListDeleteAll

`axlFormListDeleteAll(r_formt_field)⇒ t/nil`

#### Description

Deletes all the items from the form list field,`t_field`*.* Use `axlFormListDeleteAll`to clear an entire list field to update it using `axlFormSetField`, then display it using `axlFormSetField` on the field with a `nil` field value.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_field` | Name of field.
#### Value Returned

|  |
| --- | ---
| `t` | All items deleted properly.
| `nil` | All items not deleted.
#### Examples

In this example you do the following:

* Use the`axlFormCreate` examples to create and display the Extract Selector dialog box shown in [Figure 11-1](#467628 "11").

* On the SKILL command line, enter:

> `axlFormListDeleteAll(form "file_list")`

> `==> nil`

> The list is removed from the dialog box as shown in[Figure 11-2](#467665 "11").

* On the SKILL command line, enter:

`axlFormSetField(form "file_list" "fu")`

`axlFormSetField(form "file_list" "bar")`

`axlFormSetField(form "file_list" nil)`

`==> t`

> The Extract Selector dialog box is displayed with new list as shown in[Figure 11-3](#414432 "11").

****Figure 11-1****
**Extract Selector Dialog Box**

****Figure 11-2****
**Extract Selector Dialog Box - List removed**

****Figure 11-3****
**The Extract Selector dialog box - Displayed with a new list**

### axlFormListSelect

`axlFormListSelect(r_formt_fieldt_listItem/nil)⇒ t/nil`

#### Description

Highlights, and if not visible in the list, shows the designated item. Since Allegro PCB Editor forms permit only one item to be visible, it deselects any previously selected item. If`nil` is passed for `t_listItem` the list is reset to top and the selected list item is deselected.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id
| `t_field` | Name of field.
| `t_listItem``/nil` | String of item in the list. Send`nil` to deselect any selected item and set list back to top.
#### Value Returned

|  |
| --- | ---
| `t` | Highlights item. Arguments are valid.
| `nil` | Arguments are invalid.
### axlFormSetEventAction

`axlFormSetEventAction(r_formg_callback) -> t/nil`

#### Description

This function allows the user to register a callback function to be called whenever the user changes to a new active cell in the form. The callback registered during axlFormCreate dispatches events only when the user modifies a field value on the form (on exit from the field). This function allows the caller to receive an event when a field is first entered.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`
| `g_callback` | Specifies the SKILL command(s) (callback(s)) to be executed whenever a new field is activated. The setting can be one of two formats:  `t_callback`: the string representation of the SKILL command(s) to be executed  `s_callback`: the symbol of the SKILL function to be called (the function is passed the `r_form` returned from `axlFormCreate` as its only parameter).
#### See Also

[axlFormBNFDoc](#472343 "11") and [axlFormCreate](#414342 "11")

#### Value Returned

|  |
| --- | ---
| `t` | Field set to desired value.
| `nil` | Field not set to the desired value due to invalid arguments.
#### Example

`form = axlFormCreate( MyForm`

`"extract_selector.form" '("E" "OUTER")`

`'_formAction t)`

`axlFormSetEventAction( form '_formEventAction)`

### axlFormSetField

`axlFormSetField(r_formt_fieldg_value/nil)⇒ t/nil`

#### Description

Sets`t_field` to value `g_value` in open form `r_form`. Must pass the correct type, matching the entry in the form value or string type. Value type is dependent upon type of field type. For a complete discussion of field types, see the discussion at the front of this section.

Special notes for certain controls:

* LIST TYPE

> Value may be a string, integer or real. Items are converted to strings before being displayed. A`nil` is needed to display the list.

> Alternatively, value may be a list of strings. This results in better performance when you have many items to display.

* COLOR TYPE

> `g_value` parameter may have several types:

> > `s_colorSymbol` Set field to predefined color

> > `x_number` Set field to product color

> > `t` or `nil` Depress or raise field

> > `l_both` A list allows setting both check and value; pass a list of the color set

> `s_colorSymbol`may be black, white, red, green, yellow.

> `x_number`is an integer between 1 and 24 with 0 being background.

* CHECKBOX

> The values that unset the checkbox are:`nil`, `0`, `"nil"`, `"false"` and `"no"`. All other values set the checkbox.

* TRACKBAR

> If the field is a trackbar, two modes are supported.

* g\_value = t

> > Moves the slider to the next position.

* g\_value = integer

> > Absolutely sets trackbar to the indicated position.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_field` | Name of field. Field name is a string or symbol.
| `g_value` | Desired value of field. may be a string, boolean, integer or floating point number or a list; function of field type.
#### Value Returned

|  |
| --- | ---
| `t` | Field set to desired value.
| `nil` | Field not set to the desired value due to invalid arguments.
#### Examples

See[AXL Forms: Example 1](#461771 "11").

> `axlFormSetField( form "file_list" fileName)`

List Field (field is named`"list"`)

> `;; display 3 items in list`

> `axlFormSetField(fw, "list", "a")`

> `axlFormSetField(fw, "list", "b")`

> `axlFormSetField(fw, "list", "c")`

> `; nil required first time list is displayed`

> `axlFormSetField(fw, "list", nil)`

> `;; display 3 items in list - alternative`

> `axlFormSetField(fw, "list", '("a" "b" "c"))`

Color field (field is named`"color"`)

> `;; sets the color field to pre-defined color "red"`

> `` axlFormSetField(fw, "color", `red) ``

> `;; sets the color field to product color 1`

> `axlFormSetField(fw, "color", 1)`

> `;; visually depresses the color field if not greyed`

> `axlFormSetField(fw, "color", t)`

> `;; visually depresses the color field and set to`

> `;; pre-defined green color`

> `axlFormSetField(fw, "color", '(green t))`

Tab field (field is named`"tab"`)

> `;; puts the tab on top`

> `axlformSetField(fw, "tab", nil)`

### axlFormSetInfo

`axlFormSetInfo(r_formt_fieldt_value)⇒ t/nil`

#### Description

Sets info`t_field` to value `t_value` in open form `r_form`. Unlike `axlFormSet`, user cannot change an info field.

**Note:** You can also use`axlFormSetField` for this function.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_field` | Name of field.
| `t_value` | Desired value of field.
#### Value Returned

|  |
| --- | ---
| `t` | Field was set to desired value.
| `nil` | Field not set to desired value due to invalid arguments.
#### Example

See the use of`axlFormSetField` in the ["AXL Forms: Example 1"](#461771 "11").

> `axlFormSetInfo( form "file_list" fileName)`

### axlFormSetMouseActive

`axlFormSetMouseActive(r_form)==> t/nil`

#### Description

Sets the option to dispatch the MouseActive event on a form.

While this can be use to display dynamic help on a per field basis (this is what the example code does) a better method exists called the "helptip" which is driven from the form file. See the axlFormBNFDoc (note 12).

#### Arguments

|  |
| --- | ---
| `r_form` | Handle for the form
#### Value Returned

|  |
| --- | ---
| `t` | Option was set
| `nil` | `r_form` does not reference a valid form
#### Example

See`<cdsroot>/share/pcb/examples/form/basic`

### axlFormTest

`axlFormTest(t_formName) r_form/nil`

#### Description

This is a development function for test purposes. Given a form file name this opens a form file to check for placement of controls. If form uses standard button names (for example,*ok, done, close, cancel*), you can close it be clicking the button. Otherwise, use the window control. If form is currently open, exposes form and returns.

#### Arguments

|  |
| --- | ---
| `t_formName` | Name of form.
#### Value Returned

Form handle if successfully opens.

#### Example

Open Allegro PCB Editor drawing parameter form:

> `axlFormTest("status")`

### axlFormRestoreField

`axlFormRestoreField(r_formt_field)⇒ t/nil`

#### Description

Restores the`t_field` in the open form `r_form` to its previous value. The previous value is only from the last user change and not from the form set field functions. This is only useful in the *form callback* function.

Use in the`form callback` to restore the previous value when you detect the user has entered an illegal value in the field.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_field` | Name of field.
#### Value Returned

|  |
| --- | ---
| `t` | Field restored.
| `nil` | Field not restored and may not exist.
#### Example

See["AXL Forms: Example 1"](#461771 "11") where the callback function checks that the user has entered a filename that is on the list of available extract view filenames. If the user-entered value is not on the list, then the program calls `axlFormRestoreField` to restore the field to its previous value.

```
(case form->curField     ("view_file"         (if form->curValue             (progn                 ; Accept user input only if on list                 if(member( form->curValue fileList)                    then axlFormSetField( form                         "view_file" form->curValue)                     else axlFormRestoreField(                            form "view_file"))))         t)
```

### axlFormTitle

`axlFormTitle(r_formt_title)⇒ t/nil`

#### Description

Overrides title of the form.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_title` | String to be used for new form title
#### Value Returned

|  |
| --- | ---
| `t` | Changed form title.
| `nil` | No form title changed.
#### Example

See["AXL Forms: Example 1"](#461771 "11").

> `axlFormTitle( form "Extract Selector")`

### axlIsFormType

`axlIsFormType(g_form)⇒ t/nil`

#### Description

Tests if argument`g_form` is a form `dbid`.

#### Arguments

|  |
| --- | ---
| `g_form` | `dbid` of object to test.
#### Value Returned

|  |
| --- | ---
| `t` | `r_form` is the `dbid` of a form.
| `nil` | `r_form` is not the `dbid` of a form.
#### Example

> ```
> form = axlFormCreate( (gensym)    "extract_selector.form" '("E" "OUTER")    '_formAction t)if( axlIsFormType(form)    then (print "Created form successfully.")    else (print "Error! Could not create form."))
> ```

Checks that the form you create is truly a form.

### axlFormSetFieldVisible

`axlFormSetFieldVisible(r_formt_fieldx_value)⇒ t/nil`

#### Description

Sets a form field to visible or invisible.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Form field name (string).
| `x_value` | 1 - set field visible or 0 - Set field invisible
#### Value Returned

|  |
| --- | ---
| `t` | Form field set visible.
| `nil` | Form field set invisible.
### axlFormIsFieldVisible

`axlFormIsFieldVisible(r_formt_field`

`)`

`⇒ t/nil`

#### Description

Determines whether a form field is visible.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Form field name (string).
#### Value Returned

|  |
| --- | ---
| `t` | Form field is visible.
| `nil` | Form field is not visible.
### Callback Procedure: formCallback

`formCallback([r_form])⇒ t`

#### Description

This is not a function but documents the callback interface for form interaction between a user and SKILL code. The SKILL programmer provides this function.

When the user changes a field in a form, the Allegro PCB Editor form processor calls the procedure you specified as the`g_formAction` argument in `axlFormCreate` when you created that form. The form attribute `curField` specifies the name of the field that changed. The form attribute `curValue` specifies the current value of the field (after the user changed it). If you set `g_stringOption` to`t` in your call to `axlFormCreate` when you created that form, then `curValue` is a string. If `g_stringOption` was `nil` (the default), then `curValue` is the type you specified for that field in the form file.

**Note:** The term`formCallback` used in the title of this callback procedure description is a dummy name. The callback function name must match the name or symbol name you used as the `g_formAction` argument in `axlFormCreate` when you created the form.

If you specify the callback name (`g_formAction`) as a string in your call to `axlFormCreate`, SKILL calls that function with no arguments. If you specify `g_formAction` as a symbol, then SKILL calls that function with the form handleas its single argument.

The callback must call`axlFormClose` to close the form and to continue in the main application code if form mode is blocking.

All form information is provided by the`r_form` argument which is a form data type. Applications can extend the data stored on this type by adding their own attributes. Please capitalize the first letter of the attribute name to avoid conflicts with future additions by Cadence to this structure. [Table 11-4](#464382 "11") and [Table 11-5](#464559 "11") show the available field types and how they impact the `r_form` data type.

[Table 11-4](#464382 "11") describes Form Field Types using the following:

|  |
| --- | ---
| Type | What the user calls the field
| Keyword | What the form file calls the field
| curValue | Data type seen in the form dispatch and axlFormGetField. See Callback for more information.
| curValueInt | Additional information for certain field types that can be mapped to integers.
****Table 11-4****
**Form Field Types**

| **Type** | **Keyword** | **curValue** | **curValueInt**
| Button | `MENUBUTTON` | dispatch action only (t) | 1
| Check Box | `CHECKLIST` | `t/nil` | 0 or 1
| Radio Button | `CHECKLIST` | `t/nil` | 0 or 1
| Long (integer) | `INTFILLIN` | integer number | Integer
| Real (float) | `REALFILLIN` | float number | n/a
| String | `STRFILLIN` | string | n/a
| Enum (popup) | `ENUMSET` | string | Possible integer[1](#13)
| List | `LIST` | string | Offset from start of list  (`0` = first entry).
| Color well | COLOR | `t/nil` | `1` or `0`
| Tab | TABSET/TAB | string or`t` | n/a or`1`/`0`
| Tree | TREEVIEW | string | see`axlFormTreeViewSet`
| Text | INFO | n/a | n/a
| Graphics | THUMBNAIL | n/a | n/a
| GRID | GRID | see[Using Grids](#461722 "11") |
1. Integer if the dispatch value of the pop-up is an integer.

**Notes:**

* What distinguishes between a radio button and a check box is that radio buttons are a group of boxes where only one can be set. To relate several check boxes as radio buttons, supply the same label name as the third field (groupLabel) in the form file description:

> `CHECKLIST <fieldLabel> <groupLabel>`

> When a user sets a radio button, the button being unset will dispatch to the application's callback with a value of nil.

* Enum will only set curValueInt on dispatch when their dispatch value of their popup uses an integer. Otherwise this field is`nil`.

* Tabs can dispatch in two methods:

* Default when a tab is selected, your dispatcher receives the tab name in the curField and curValue is t.

* If "OPTIONS tabsetDispatch" is set in the TABSET of the form file, then when a tab is selected your application dispatcher receives the TABSET as the curField and the curValue being the name of the TAB that was selected.

* INFO fields can be static where the text is declared in the form file or dynamic where you can set the text via the application at run-time. To achieve dynamic access, enter the following in the form file:

> `TEXT "<optional initial text>"`

> `INFO <fieldLabel>`

> `... reset of TEXT section ...`

* Thumbnails support the following methods:

* static bitmap declared via the form file

* bitmaps that can be changed by the application at run-time

* basic drawing canvas -- see[Chapter 12, "Simple Graphics Drawing Functions"](12draw.html#1037521 "12")

* Buttons are stateless. The application cannot set the button to the depressed state. You can only use axlFormSetField to change the text in the button. Several button fieldLabels are reserved. Use them only as described:

|  |
| --- | ---
| done or OK | Do action and close the form.
| cancel | Cancel changes and close the form.
| print | Print the form -- do not use.
| help | Call cdsdoc for help about the form -- do not use.
****Table 11-5****
****Form Attributes****

| **Attribute Name** | **Set?** | **Type\*** | **Description**
| `curField` | no | string | Name of form field just changed
| `curValue` | no | See --> | Depends on value of`curField` (`string`, `int`, `float`, `boolean`)
| `curValueInt` | no | See --> | Depends on value of`curField` field
| `doneState` | no | int | `0` = action; `1` = done; `2` = cancel; `3` = abort
| `form` | no | string | Name of this form
| `isChanged` | no | `t/nil` | `t` = user has changed one or more fields in form.
| `isValueString` | no | `t/nil` | `t` = all field values are strings `nil` = one or more fields are not strings
| `objType` | no | string | Type of object, in this case`"form"`
| `type` | no | string | Form type, always`"fixed"`
| fields | no | list of strings | All fields in the form.
| infos | no | list of strings | All info fields in the form.
| event | no | symbol | Grid control only -- see[Using Grids](#461722 "11")
| row | no | integer | Grid control only
| col | no | integer | Grid control only
| treeViewSelState | no | integer | Tree control only
| \* You can add your own attribute types to the form type. It is recommended you capitalize the first letter of the name to avoid conflict with future Allegro PCB Editor releases. | | |
**Notes:**

* The doneState shows 0 for most actions. Selecting a*Done* or *OK* button sets the done state. Selecting a *Cancel* button sets the cancel state. With the done or cancel state set, you use `axlFormClose` to close the form. Setting the abort state closes the form, even if you do not issue an `axlFormClose` command.

* Data type is dependant on the field type. See[Table 11-4](#464382 "11") for more information on Form Field Types.

* The infos list is different from the fields list. The infos list comprises static text strings that the program can change at run-time. The fields list comprises all other labels which can be changed by the user including even those on buttons and tabs, greyed and hidden fields.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

See[axlFormCreate](#414342 "11") and [axlFormBuildPopup](#424697 "11") for examples.

### axlFormAutoResize

`axlFormAutoResize(r_form)⇒ t/nil`

#### Description

Resizes a form to fit its controls. Recalculates the required width and height and resizes the form based on the current visibility of the form's fields.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Form field name (string).
#### Value Returned

|  |
| --- | ---
| `t` | Form resized.
| `nil` | `r_form` does not reference a valid form.
### axlFormColorize

`axlFormColorize(o_formt_fieldg_optiong_color)⇒ t/nil`

#### Description

Allows the override of background and/or text color of a control. Only the following controls are supported:

* `STRFILLIN`

* `READFILLIN`

* `LONGFILLIN`

* `INTSLIDEBAR`

* `ENUMSET`

* `CHECKLIST`

* `TEXT`or`INFO`

These names appear in the form BNF file syntax.

These controls use the default system colors:

