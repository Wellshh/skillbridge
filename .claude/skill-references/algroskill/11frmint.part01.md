<!--
source: algroskill/11frmint.md
part: 1/2
estimated_tokens: 13012
-->

### Programming

#### Description

It is best to look at the two form demo.

- basic controls -- `axlform.il/axlform.form`

- grid control - `fgrid.il/fgrid.form`

- multi-select grid control - `fgrid-msel.il/fgrid.form`

The first step is to create form file. Use `axlFormTest` to ensure fields are correctly positioned.

The following procedure is generally used.

| Name | Description |
|---|---|
| 1. | Open form (`axlFormCreate`) |

| Name | Description |
|---|---|
| 2. | Initialize fields (`axlFormSetField`) |

| Name | Description |
|---|---|
| 3. | Display Form (`axlFormDisplay`) |

| Name | Description |
|---|---|
| 4. | Interactive with user (`axlFormCallback`) |

| Name | Description |
|---|---|
| 5. | Close Form (`axlFormClose`) |

- Many users find that it is easier to distribute their programusing a form if they embed the form file in their Skill code.In this case use Skill to open a temporary file and printthe statements, open for form, then delete the file.

- Use `axlFormTest`("<form file>") to interactively adjust of fields.

- You can use "`ifdef`", "`ifndef`", and Allegro environment variables(`axlSetVariable`) to control appearance of items in the form file.

### Field / Control

#### Description

Most interaction to the controls are via axlFormSetField, axlFormGetField, axlFormSetFieldEditable, and axlFormSetFieldVisible.Certain controls have additional APIs which are noted in the description for the control.

Most controls support setting their background and foreground colors. See `axlColorDoc` and `axlFormColorize` for more information.

Following is a list of fields and their capabilities.

#### Examples

These examples, especially the basic one, help you understand how the forms package works:

| Name | Description |
|---|---|
| basic | Demonstrates basic form capabilities. |
| grid | Demonstrates grid control capabilities. |
| wizard | Demonstrates use of a form in Wizard mode. |

Use the examples located in `<``cdsroot``>/share/pcb/examples/form` as follows:

| Name | Description |
|---|---|
| 1. | Copy all the files from one of the directories to your computer. |

| Name | Description |
|---|---|
| 2. | Start Allegro PCB Editor. |

| Name | Description |
|---|---|
| 3. | From the Allegro PCB Editor command line, change to the directory to which you copied the files as shown: |

`cd <``directory``>`

| Name | Description |
|---|---|
| 4. | Load the SKILL file in the directory. |

Note: The SKILL file has the `.il` extension.

`skill load "<``filename``>"`

| Name | Description |
|---|---|
| 5. | Start the demo by typing on the Allegro PCB Editor command line as shown: |

For basic demo:

`skill formtest`

For grid demo:

`skill gridtest`

| Name | Description |
|---|---|
| 6. | Examine the SKILL code and form file. |

- Setting the Allegro PCB Editor environment variable `TELSKILL` opens a SKILL interpreter window that is more flexible than the Allegro PCB Editor command area. On UNIX, if you set this variable before starting the tool then the SKILL type-in area is the X terminal you used to start Allegro PCB Editor. See the enved tool to configure the width and height of the window.

Using Forms Specification Language

Backus Naur Form (BNF) is a formal notation used to describe the syntax of a language. Form File Language Description is the BNF grammar for the Forms Specification Language. Forms features in new versions are not backwards compatible.

The following table shows the conventions used in the form file grammar:

| Name | Description |
|---|---|
| Convention | Description |
| `[ ]` | Optional |
| `{ }` | May repeat one or more times |
| `< >` | Supplied by the user |
| `|` | Choose one or the other |
| `:` | Definition of a token |
| `CAPS` | Items in caps are keywords |

The BNF format definition follows.

`BNF:`

`form:`

`FILE_TYPE=FORM_DEFN VERSION=2`

`FORM [form_options]`

`formtype`

`PORT w h`

`HEADER "text"`

`form_header`

`{tile_def}`

`ENDFORM`

`formtype: FIXED | VARIABLE`

`- FIXED forms have one unlabeled TILE stanza`

`- VARIABLE forms have one or more label TILE stanzas`

`- Skill only supports FIXED form types.`

`PORT:`

`- Width and height of the form. Height is ignored for fixed forms which auto-calculate required height.Width must be in character units.`

`HEADER:`

`- Initial string used in the title bar of the form. This may be overridden by the application.`

`form_header:`

`[{default_button_def}]`

`[{popup_def}]`

`[{message_def}]`

`default_button_def:`

`DEFAULT <label>`

`- Sets the default button to be <label>. If not present, the form sets the default button to be one of the following: ok (done), close, or cancel.`

`- Label must be of type MENU BUTTON.`

`popup_def:`

`POPUP <<popupLabel>> {"<display>","<dispatch>"}.`

`- Popups may be continued over several lines by using the backslash (\) as the last character on a line.`

`message_def:`

`MESSAGE messageLabel messagePriority "text"`

`form_options:`

`[TOOLWINDOW]`

`- This makes a form a toolwindow which is a floating toolbar. It is typically used as a narrow temp window to display readouts.`

`[FIXED_FONT]`

`- By default, forms use a variable width font. This option sets the form to use a fixed font. Allegro PCB Editor uses mostly variable width while SPECCTRAQuest and SigXP use fixed width fonts.`

`[AUTOGREYTEXT]`

`- When a fillin or enum control is greyed, grey static text to the left of it.`

`[UNIXHGT]`

`- Works around a problem with Mainsoft in 15.0 where a button is sandwiched vertically between 2 combo/fillin controls. The button then overlaps these controls. This adds extra line spacing to avoid this. You should only use this option as a last resort. In a future release, it may be treated as a Nop. On Windows, this is ignored.`

`tile_def:`

`TILE [<tileLabel>]`

`[TPANEL tileType]`

`[{text_def}]`

`[{group_def}]`

`[{field_def}]`

`[{button_def}]`

`[{grid_def}]`

`[{glex_def}]`

`ENDTILE`

`tabset_def:`

`TABSET [label]`

`[OPTIONS tabsetOptions]`

`FLOC x y`

`FSIZE w h`

`{tab_def}`

`ENDTABSET`

`tab_def:`

`TAB "<display>" [<label>]`

`[{text_def}]`

`[{group_def}]`

`[{field_def}]`

`[{grid_def}]`

`ENDTAB`

`text_def:`

`TEXT "display" [label]`

`FLOC x y`

`[FSIZE w h]`

`text_type`

`[OPTIONS textOptions]`

`ENDTEXT`

`text_type:`

`[INFO label w] |`

`[THUMBNAIL [<bitmapFile>|#<resource>] ]`

`group_def:`

`GROUP "display" [label]`

`FLOC x y`

`[INFO label]`

`FSIZE w h`

`ENDGROUP`

`field_def:`

`FIELD label`

`FLOC x y`

`[FSIZE w h]`

`field_type`

`field_options`

`ENDFIELD`

`button_def:`

`FIELD label`

`FLOC x y`

`[FSIZE w h]`

`MENUBUTTON "display" w h`

`button_options`

`ENDFIELD`

`grid_def:`

`GRID fieldName`

`FLOC x y`

`FSIZE w h`

`[OPTIONS INFO | HLINES | VLINES | USERSIZE ]`

`[POP "<popupName>"]`

`[GHEAD TOP|SIDE]`

`[HEADSIZE h|w]`

`[OPTION 3D|NUMBER]`

`[POP "<popupName>"]`

`[ENDGRID]`

`ENDGRID`

`field_type:`

`REALFILLIN w fieldLength |`

`LONGFILLIN w fieldLength |`

`STRFILLIN w fieldLength |`

`INTSLIDEBAR w fieldLength |`

`ENUMSET w [h] |`

`CHECKLIST "display" ["radioLabel"] |`

`LIST "" w h |`

`TREEVIEW w h |`

`COLOR w h |`

`THUMBNAIL [<bitmapFile>|#<resource>] |`

`PROGRESS w h`

`TRACKBAR w h`

`field_options:`

`[INFO_ONLY]`

`- Sets field to be read-only`

`[POP "<popupName>"]`

`- Assigns a popup with the field.`

`- A POPUP definition by the same name should exist.`

`- Supported by field_types: xxxFILLIN, INTSLIDEBAR, MENUBUTTON,and ENUMSET.`

`[MIN <value>]`

`[MAX <value>]`

`- Assigns a min and/or max value for the field.`

`- Both supported by field types: LONGFILLIN, INTSLIDEBAR, REALFILLIN.`

`- Value either an integer or floating point number.`

`[DECIMAL <accuracy>]`

`- Assigns a floating min and/or max value for the field.`

`- Assigns the number of decimal places the field has (default is 2)`

`- Both supported by field_types: REALFILLIN`

`[VALUE "<display>"]`

`- Initial field value.`

`- Supported by field_types: xxxFILLIN`

`[SORT]`

`- Alphanumeric sorted list (default order of creation)`

`- Supported by field_type: LIST`

`[OPTIONS dispatchsame]`

`- For enumset fields only`

`- If present, will dispatch to application drop-down selection even if the same as current. By default, the form's package filters out any user selection if it is the same as what is currently displayed.`

`[OPTIONS prettyprint]`

`- For enumset fields only.`

`- Displays contents of ENUM field in a visually pleasing way.`

`[OPTIONS ownerdrawn]`

`- For enumset fields only.`

`- Used to display color swatches in an ENUM field. See axlFormBuildPopup.`

`x:`

`y:`

`w:`

`h:`

`- Display geometry (integers)`

`- All field, group and text locations are relative to the start of the tile they belong or to the start of the form in the case of FIXED forms.`

`- x and h are in CHARHEIGHT/2 units.`

`- y and w are in CHARWIDTH units.`

`button_options:`

`[MULTILINE]`

`- Wraps button text to multiple lines if text string is too long for a single line.`

`dispatch:`

`- String that is dispatched to the code.`

`display:`

`- String that is shown to the user.`

`bitmapFile:`

`- Name of a bmp file. Finds the file using BITMAPPATH`

`resource:`

`- Integer resource id (bitmap must be bound in executable via the resource file). '#' indicates it is a resource id.`

`- Not supported in AXL forms.`

`fieldLength:`

`- Maximum width of field. Field scrolls if larger than the field display width.`

`label:`

`- Name used to access a field from code. All fields should have unique names.`

`- Labels should be lower case.`

`messageLabel:`

`- Name used to allow code to refer to messages.`

`- Case insensitive.`

`messagePriority:`

`- Message priority 0 - (not in journal file), 1 - information, 2 - warning, 3 - error, 4 - fatal (display in message box)`

`radioLabel:`

`- Name used to associate several CHECKLIST fields as a radio button set. All check fields should be given the same radioLabel.`

`- Should use lower case.`

`textOptions:`

`[RIGHT | CENTER | BORDER | BOLD | UNDERLINE]`

`- TEXT/INFO field type`

`- text justification, default is left`

`- BORDER: draw border around text`

`[STRETCH]`

`- THUMBNAIL field type`

`- Stretch bitmap to fit thumbnail rectangle, default is center bitmap.`

`tabsetOptions:`

`[tabsetDispatch]`

`- By default, tabsets dispatch individual tabs as seperate events. This is not always convenient for certain programming styles. This changes the dispatch mode to be upon the tabset where a selection of a tab causes the event:`

`field=tabsetLabel value=tabLabel`

`The default is:`

`field=tabLabel value=t`

`Script record/play remains based upon tab in either mode.`

`tileLabel:`

`- Name used to allow code to refer to this tile.`

`- Should use lower case.`

`- Only applies to VARIABLE forms.`

`- Not supported with AXL forms.`

`tileType [0|1|2]`

`- 0 top tile, 1 scroll tile, 2 bottom tile`

`- Only applies to VARIABLE FORMS.`

`- Region where tile will be instantiated. Forms have the following regions: top, bottom, and scroll (middle).`

`- Not supported with AXL forms.`

`flex_def: Rule based control sizing upon form resize (see axlFormFlex)`

`[FLEXMODE <autorule>]`

`[FLEX <label> fx fy fw fh]`

`FLEXMODE <autoRule>`

`FLEX fx fy fw fz`

`- see axlFormFlexDoc`

`autorule: - Generic sizing placement rule.`

`fx:`

`fy:`

`fh:`

`- Floating value between 0 and 1.0`

- Follow these rules when using BNF format:

- `FILE_TYPE` line must always appear as the first line of the form file in the format shown.

- Form files must have a `.form` extension.

- There may only be one `FORM` in a form file.

- There must be one and only one `TILE` definition in a `FIXED` form file. <`tileLabel`> and `TPANEL` are not required.

- Unless otherwise noted, character limits are as follows:labels - 128title - 1024display - 128 except for `xxx``FILLIN` types which are 1024

- Additional items may appear in existing form files (`FGROUP`) but they are obsolete and are ignored by the form parser. `REALMIN` and `REALMAX` are obsolete and replaced by `MIN` and `MAX` respectively. They will still be supported and are mapped to `MIN` and `MAX`.

- For `grid_def`, two headers (side and top) are maximum.

- `FSIZE` - Most controls determine the size from the text string.You must provide `FSIZE` for `GROUP`, `GRID`, `TREEVIEW` and `LIST` controls. For `TEXT` controls, if `FSIZE` is provided, it overrides the width calculated by the text length and, if present, the `INFO` width. If using the `INFO` line, put the `FSIZE` line after it.

- Both `TEXT` and `GROUP` support the optional label on their definition line. This was added as a convenience in supporting `FLEX` capability. If the application wishes to dynamically modify the text, the `INFO` keyword is normally used. When both are present, the `INFO` keyword takes precedence.

- If the optional label for `TABS` is not provided, the field display name is used. Any spaces within the field display name are replaced by underscores (`"_"`).

- The height ([`h`]) for `ENUMSET` is optional. When not set (the default), the drop-down is only presented under user control. When height is greater than 1, the drop-down is always visible (Microsoft SIMPLE drop-down). Only use this feature in forms that can afford the space consumed by the drop-down.

The forming syntaxes are NOT supported by the form editor.

This syntax is supported and may be placed anywhere in the form file to support conditional processing of the form file:

`#ifdef <``variable``>`

`{}`

`{ #elseif <``variable``>`

`}`

`{ #else`

`{} }`

Moving and Sizing Form Controls During Form Resizing

You can use the axlFormFlexDoc command to move and size controls within a form based on rules described in the form file. Rules may either be general (`FLEXMODE`) or specific to a single control (`FLEX`.) Flex adjusting of the controls is adjusting the form larger than its base size. Sizing the form smaller than the base size disables flex sizing.

Controls are divided into the following classes:

- ContainersContainers can have other controls as members, including other containers. To be a container member is automatic; the control's `xy` location must be within the container. Container controls of the form are `TABSET`s and `GROUP`s.

- All others, including containers

All controls except `TABS`, which are locked to their `TABSET`, may be moved when a form is resized. Sizing width or height is control dependent as shown:

Table 11-2 
 Controls - Resizing Options

| Name | Description |
|---|---|
| Control | Resizing Options |
| `REALFILLIN` | width |
| `LONGFILLIN` | width |
| `STRFILLIN` | width |
| `INTSLIDEBAR` | width |
| `ENUMSET` | width |
| `PROGRESS` | width |
| `TRACKBAR` | width |
| `LIST` | width and height |
| `GRID` | width and height |
| `TREEVIEW` | width and height |
| `THUMBNAIL` | width and height |
| `GROUP` | width and height |
| `TABSET` | width and height |
| `<``others``>` | no change in size |

- If grids replace the text parameter form, you need not label the columns. A column number is sufficient. You can label the columns for script readability. This application does not require cell labeling.

- If grids replace the color form for certain color grids, like stackup, you would need to label each cell. Each class grouped in the stackup grid is not row consistent. For example, depending on design, subclasses are not the same going across the rows. Other groupings require labeling on class for `col` and `subclass` for `row` since it is orthogonal.

See Using Grids for a grid overview.

Headers

You can set column (top) headers either using `axlFormGridInsertCol` at column creation time, or using `axlFormGridSetBatch` if you need to change the header using row number `0`.

Row (side) headers default to automatic run numbers with this option set in the form file. Using `axlFormGridSetBatch`, you can set the text for individual rows using col number `0`.

### axlFormBNFDoc

#### Description

This is the BNF grammar for the Forms Specification Language. New options and field types are added every release. Form files are always upwards compatible but may NOT be backwards compatible if you take advantage of a new feature. Thus, a form file created in 12.0 Allegro works in 13.0 Allegro. However, if you take advantage of the TAB control (13.0) or the RIGHT justification of TEXT (13.5), you will have a form file that will not function with 12.0 of Allegro.

The following outlines the conventions used in the grammar:

[] Optional{} May repeat one or more times.<> Supplied by user.| Choose one or the other.: Definition of a token.CAPS Items in caps are keywords (note form parser is case insensitive)(#) Note: See number at end of this documentation.

### axlFormCallback

`axlFormCallback( [ r_form ] ) => t`

#### Description

This is not a function but documents the callback interface for form interaction between a user and Skill code. The Skill program author provides this function.

When the user changes a field in a form the Allegro form processor calls the procedure you specified as the `g_formAction` argument in `axlFormCreate` when you created that form. The form attribute `curField` specifies the name of the field that changed. The form attribute `curValue` specifies the current value of the field (after the user changed it). If you set `g_stringOption` to `t` in your call to `axlFormCreate` when you created that form, then `curValue` is a string. If `g_stringOption` was `nil` (the default), then `curValue` is the type you specified for that field in the form file.

Note: The term `formCallback` used in the title of this callback procedure description is a dummy name. The callback function name must match the name or symbol name you used as the `g_formAction` argument in `axlFormCreate` when you created the form.

If you specify the callback name (`g_formAction`) as a string in your call to `axlFormCreate`, SKILL calls that function with no arguments. If you specify `g_formAction` as a symbol, then SKILL calls that function with the form handle as its single argument.

The callback must call `axlFormClose` to close the form and to continue in the main application code if form mode is blocking.

All form information is provided by the `r_form` argument which is a form data type. Applications can extend the data stored on this type by adding their own attributes. Capitalize the first letter of the attribute name to avoid conflicts with future additions by Cadence to this structure. Tables 1 and 2 show the available field types and how they impact the `r_form` data type.

#### Arguments

`r_form` Form dbid.

#### Value Returns

`t`Always returns `t`.

#### Examples

See `axlFormCreate` and `axlFormBuildPopup` examples.

### axlFormCreate

`axlFormCreate( s_formHandle t_formfile/(t_formName t_contents)/(t_formName (t_contents)) [lt_placement] g_formAction g_nonBlock [g_stringOption] ) => r_form/nil`

#### Description

Creates a dialog based on the form descriptive file `t_formfile`. This call only supports forms of type `"fixed"` and fails if `t_formfile` contains any variable tiles. This function does not display the form. Use `axlFormDisplay` to display a form.

An alternative interface is supported that allows embedding the contents of the form file in the skill code. Instead of passing the external form file name provide the name (t_formName) for scripting purposes and form file contents (t_contents) as string. The packaged skill code has a example of this method at the end of the `<cdsroot>``/share/pcb/examples/form/finline.il` file. This method has the advantage of only distributing one file.

Rules to remember when creating this form content string:

- Every non-blank line must have a tab character

Example:

`FILE_TYPE=FORM_DEFN VERSION=2`

- Any embedded quotes must be escaped (use backslash '\')

Example:

`MENUBUTTON \"Ok\" 10 3\n`

- Any paraenthesis '()' must be escaped '\'

Note: If `s_formHandle` is an existing `r_form`, then `axlFormCreate` does not create a new form, but simply exposes and displays the existing form, `s_formHandle`, and returns `nil`.

#### Arguments

| Name | Description |
|---|---|
| `s_formHandle` | Global SKILL symbol used to reference form.Note: Do not use the same symbol to reference different form instances. |
| `t_formfile` | Filename of the form file to be used to define this form. `axlFormCreate` uses the Allegro PCB Editor environment variable, `FORMPATH`, to find the file, if `t_formfile` is not a full path. The filename, by convention, should use the `.form` extension.Alternative interface to embed form file into Skill code: `t_formName`: Name of form (used for scripting) `(t_contents)`: Contents of form file. This may be a string or a list containing or a string. The string format is obsolete and you should use `t_contents t_contents`: the list with string format |
| `lt_placement` | Form placement. Allegro PCB Editor uses its default placement if this argument is `nil`. See Window Placement |
| `g_formAction` | Specifies the SKILL commands (callbacks) to be executed after every field change (Note that this is very different from Cadence IC forms). You can set this to one of the formats shown: |
| `g_form` | `Action` Options |

| Name | Description |
|---|---|
| Option | Description |
| `t_callback` | String representation of the SKILL command to be executed. |
| `s_callback` | Symbol of the SKILL function to be called (passes the `r_form` returned from `axlFormCreate` as its only parameter.) |
| `nil` | `axlFormDisplay` blocks until the user closes the form.You must place a Done button (field name `done`) and optionally a Cancel button (field name `cancel`) in the form for `g_formAction` to function properly. The user can access all of the fields and values using the `r_form` user type. |

| Name | Description |
|---|---|
| `g_nonBlock` | If `g_nonBlock` is `t`, the form runs in non-blocking mode. In blocking mode (the default), `axlFormDisplay` blocks until the user closes the form. Blocking is an easier programming mode but might not be appropriate for your application. If the callback (`g_formAction`) is `nil`, then `axlFormDisplay` ignores `g_nonBlock`, and the form runs in blocking mode. 
 Use of blocking mode blocks the progress of the SKILL code, but does not prevent other Allegro PCB Editor events from occurring. For example, if blocked, users can start the Add Line command from Allegro PCB Editor menus. |
| `g_stringOption` | If`t,` the form returns and accepts all values as strings. By default, it returns and accepts values in the format declared in the form file. |

#### Value Returns

| Name | Description |
|---|---|
| `r_form` | `dbid` of form created. |
| `nil` | No form created. |

#### Examples

See `<cdsroot>/share/pcb/examples/form`

basic: demostrates basic form capabilities

finline.il shows correct inline method

grid: demostrates grid control capabilites

wizard: form when used in a Wizard mode

finline: demostrates inline option to avoid having a .form file

See AXL Forms: Example 1.

#### See Also

- axlFormIntroDoc: Introduction to the Allegro Form Package.

- axlFormBNFDoc: Form file language description

- axlFormCallback: Methods and structures for interacting with user.

### axlFormClearMouseActive

`axlFormClearMouseActive( r_form ) => t/nil`

#### Description

Clears the option to dispatch the MouseActive event on a form.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Handle for the form |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Option was cleared |
| `nil` | r_form does not reference a valid form |

### axlFormClose

`axlFormClose( r_form ) => t/nil`

#### Description

Closes the form `r_form`. Unless the form is running without a callback handler, you must make this call to close the form. Without a registered dispatch handler, Allegro PCB Editor closes the form automatically before returning to the application from `axlFormDisplay`.

Note: `axlUIWClose` also performs the same function.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form `dbid`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Closed the form. |
| `nil` | Form was already closed. |

#### Examples

See AXL Forms: Example 1 :

`(case form->curField``("done"``(axlFormClose form)``(axlCancelEnterFun)``(_extract)``t)`

### axlFormDisplay

`axlFormDisplay( r_form ) => t/nil`

#### Description

Displays the form `r_form` already created by `axlFormCreate`. For superior display appearance, set all the field values of the form before calling this function. A form in blocking mode blocks until the user closes the form.

If a form is already displayed, this function simply exposes it.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form `dbid`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Successfully opened or exposed the form. |
| `nil` | Failed to open or expose the form. |

#### Examples

See AXL Forms: Example 1.

`axlFormDisplay( form)`

### axlFormBuildPopup

`axlFormBuildPopup( r_form t_field l_pairs ) => t/nil`

#### Description

This provides the ability to dynamically change popups of fields that have them. These fields are enum (or pop-up) and other fields that have a popup icon. Buttons, optionally, may also have a popup if they have a right arrow. Attempting this call on a field without a popup is an error.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | a form handle |
| `t_field` | Name of form field. |
| `l_pairs` | May be one of four formats where each element is a single popup entry. A maximum of 256 popup entries are allowed.<br><br>normal `( (t_display t_dispatch) ... )` alternative normal `( t_displayNdispatch ... )` for enum field types `( (t_display x_dispatch) ... ) ( (t_display t_dispatch/x_dispatch options) ... )` Options can be 1 or 2 additional list options that are `S_color/x_color` for enum field types with color; bold or underline for bold or underlined items. |

Note:

All entries in an `l_pairs` argument must be the same type of format. That is, you cannot have a list containing, for example, both display/dispatch strings and display/enum types, or display/dispatch and single-string entries.

Must be one of the formats described. Each list object defines a single popup entry.

Table 11-3 
 l_pairs Format Options

| Name | Description |
|---|---|
| Option | Description; Example |
| List of lists of string pairs | The first member of each string pair list is the display value-the string displayed in the pop-up. The second member of each string pair is the dispatch value-the string value returned as `form->curValue` when the user selects that pop-up entry.; `(list (list "MyPop A" "myvalue_a") list("MyPop B" "myvalue_b"))` |
| List of lists of pairs | List of lists of pairs where the first member of each pair is a string giving the display value, and the second member is an integer that is the dispatch value, returned as `form - curValue` when the user selects that pop-up entry. 
 You can use the return value as an index into an array.; `(list (list "MyPop A" 5)``list("MyPop B" 7))` |
| List of strings | Uses each string both for display value and the return value.; `(list "MyPop A" "MyPop B")` |
| Optional field | Specifies a color swatch. This is currently only supported by ENUM field types (it is ignored by other field types). With an ENUM you need to add `OPTIONS ownerdrawn` in the form file for the FIELD in question to see the color swatch in the popup. You can use either pre-defined color names (see `axlColorDoc`) or Allegro board colors (see `axlLayerGet`).; You can't mix this color type in a single popup. `'(("Green" 1 green) ("Red" 2 red) ("Yellow" 3 yellow)) '(("Top" "top" 2) ("Gnd "gnd" 4) ("Bottom" "btm" 18))` If instead of a color or Allegro color number, you provide a `nil,` then that popup entry will not have a color swatch. `'("(None" 0 nil) ("Green" 1 green) ("Red" 2 red) ("Yellow" 3 yellow))` Font type of bold or underline can be specified via: `'(("Top" "top" bold) ("Gnd "gnd" underline) ("Bottom" "btm"))` When font type is combined with color it looks like: `'(("Top" "top" "Green" bold) ("Gnd "gnd" "Red" underline)` |

Notes:

- Allows a maximum of 1000 pop-up entries in one pop-up.

- If creating a dynamic popup (entries created under program control) a dummy entry must exist in the form file or build popup will fail. Example:

`<popupname> """".`

- The field name is actually a search mechanism. We first search the fields for the field name with a popup and then search the popup names. Since the only way to change grid column or cell based popups is by popup name you may run into failures if that popup name has the same name as another field in the form.

#### Value Returns

| Name | Description |
|---|---|
| `t` | Field set. |
| `nil` | Field not set. |

#### Examples

See AXL Forms: Example 2.

### axlFormGetField

`axlFormGetField( r_form t_field ) => g_value/nil`

#### Description

Gets the value of `t_field` in the open form `r_form`. The value is a string if `g_stringOption` was set in `axlFormCreate`. Otherwise the value is in the field type declared in the form file.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form `dbid`. |
| `t_field` | Name of field. |

#### Value Returns

| Name | Description |
|---|---|
| `g_value` | Current value of the field. |
| `nil` | Field does not exist, or false if boolean field such as check box or radio button. |

#### Examples

| Name | Description |
|---|---|
| 1. | Load the example code given in AXL Forms: Example 1. |

| Name | Description |
|---|---|
| 2. | Enter the command `myExtract()` on the SKILL command line. |

The command displays the Extract Selector form, listing all available extract view files.

| Name | Description |
|---|---|
| 3. | Select any file in the list, or type a name into the View File field. |

`allegro2rlb_view.txt` is entered.

`axlFormGetField( form "view_file")``⇒ "allegro2rlb_view.txt"`

Examines the value of "`view_file`" .

### axlFormGridSelected

`axlFormGridSelected( r_form t_field ) => lx_selected/nil`

#### Description

This returns the selected item in a multi-select grid control. This should only be used if grid is running with the multi-select row option.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | standard form handle |
| `t_field` | standard field name |

#### Value Returns

Returns list of selected items in a multi-select grid or nil if not the correct control.

#### Examples

See `fgrid.il` in `<CDSROOT>``/share/pcb/examples/skill/form/grid`

Pseudo code:

#### See Also

axlFormGridNewCell

### axlFormGridSelectedCnt

`axlFormGridSelectedCnt( r_form t_field ) => x_cnt/nil`

#### Description

`axlFormGridEvents(fg "grid" 'mrowselect) ;; select items selected = axlFormGridSelected(fg "grid") ; if form select rows 5,6,7 (click on 5, then Shift click on 7) ;; select items selected = axlFormGridSelected(fg "grid") -> (5 6 7)` This returns the count of rows selected in a multi-select grid control. This should only be used if grid is running with the multi-select row option.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | standard form handle |
| `t_field` | standard field name |

#### Value Returns

Returns count of selected items or `nil` if wrong type of control

#### Examples

See `fgrid.il` in `<CDSROOT>``/share/pcb/examples/skill/form/grid`

Pseudo code:

`axlFormGridEvents(fg "grid" 'mrowselect)`

`; if form select rows all rows (Ctrl-A in grid)`

`;; select items`

`selected = axlFormGridSelectedCnt(fg "grid")`

`-> 16`

#### See Also

axlFormGridNewCell

### axlFormGridSetSelectRows

`axlFormGridSetSelectRows( r_form t_field x_min x_max g_option ) => x_cnt/nil`

#### Description

This allows setting, clearing or toggling of selection state for a grid in multi-select row mode.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | standard form handle |
| `t_field` | standard field name |
| `x_min` | min row number |
| `x_max` | max row number |
| `g_option` | what to do<br><br>`t` - set row as selected<br><br>`nil` - clear row as selected<br><br>`'toggle` - toggle selected state of row |

#### Value Returns

`t` if succeeded, `nil` if not a grid field or not in multi-row select mode

#### Examples

See `fgrid.il` in `<CDSROOT>``/share/pcb/examples/skill/form/grid`

Pseudo code:

`axlFormGridEvents(fg "grid" 'mrowselect)`

- set row 4 as selected

`axlFormGridSetSelectRows(fg "grid" 4 4 t)`

- clear rows 4 thru 8 being selected

`axlFormGridSetSelectRows(fg "grid" 4 8 t)`

- clear all rows

`axlFormGridSetSelectRows(fg "grid" -1 -1 nil)`

- toggle state of row 1

`axlFormGridSetSelectRows(fg "grid" 1 1 'toggle)`

#### See Also

axlFormGridNewCell

### axlFormListDeleteAll

`axlFormListDeleteAll( r_form t_field ) => t/nil`

#### Description

Deletes all the items from the form list field, `t_field`. Use `axlFormListDeleteAll` to clear an entire list field to update it using `axlFormSetField`, then display it using `axlFormSetField` on the field with a `nil` field value.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form `dbid`. |
| `t_field` | Name of field. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | All items deleted properly. |
| `nil` | All items not deleted. |

#### Examples

In this example you do the following:

| Name | Description |
|---|---|
| 1. | Use the `axlFormCreate` examples to create and display the Extract Selector dialog box shown in Figure 11-1. |

| Name | Description |
|---|---|
| 2. | On the SKILL command line, enter: |

`axlFormListDeleteAll(form "file_list")`

`==> nil`

The list is removed from the dialog box as shown in Figure 11-2.

| Name | Description |
|---|---|
| 3. | On the SKILL command line, enter: |

`axlFormSetField(form "file_list" "fu")`

`axlFormSetField(form "file_list" "bar")`

`axlFormSetField(form "file_list" nil)`

`==> t`

The Extract Selector dialog box is displayed with new list as shown in Figure 11-3.

Figure 11-1 
 Extract Selector Dialog Box

Figure 11-2 
 Extract Selector Dialog Box - List removed

Figure 11-3 
 The Extract Selector dialog box - Displayed with a new list

### axlFormListSelect

`axlFormListSelect( r_form t_field t_listItem/nil ) => t/nil`

#### Description

Highlights, and if not visible in the list, shows the designated item. Since Allegro PCB Editor forms permit only one item to be visible, it deselects any previously selected item. If `nil` is passed for `t_listItem` the list is reset to top and the selected list item is deselected.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form id |
| `t_field` | Name of field. |
| `t_listItem``/nil` | String of item in the list. Send `nil` to deselect any selected item and set list back to top. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Highlights item. Arguments are valid. |
| `nil` | Arguments are invalid. |

### axlFormSetEventAction

`axlFormSetEventAction( r_form g_callback ) => t/nil`

#### Description

This function allows the user to register a callback function to be called whenever the user changes to a new active cell in the form. The callback registered during axlFormCreate dispatches events only when the user modifies a field value on the form (on exit from the field). This function allows the caller to receive an event when a field is first entered.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form `dbid` |
| `g_callback` | Specifies the SKILL command(s) (callback(s)) to be executed whenever a new field is activated. The setting can be one of two formats: `t_callback`: the string representation of the SKILL command(s) to be executed `s_callback`: the symbol of the SKILL function to be called (the function is passed the `r_form` returned from `axlFormCreate` as its only parameter). |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Field set to desired value. |
| `nil` | Field not set to the desired value due to invalid arguments. |

#### Examples

`form = axlFormCreate( MyForm`

`"extract_selector.form" '("E" "OUTER")`

`'_formAction t)`

`axlFormSetEventAction( form '_formEventAction)`

#### See Also

axlFormBNFDoc and axlFormCreate

### axlFormSetField

`axlFormSetField( r_form t_field g_value/nil ) => t/nil`

#### Description

Sets `t_field` to value `g_value` in open form `r_form`. Must pass the correct type, matching the entry in the form value or string type. Value type is dependent upon type of field type. For a complete discussion of field types, see the discussion at the front of this section.

Special notes for certain controls:

- LIST TYPE

Value may be a string, integer or real. Items are converted to strings before being displayed. A `nil` is needed to display the list.

Alternatively, value may be a list of strings. This results in better performance when you have many items to display.

- COLOR TYPE

`g_value` parameter may have several types:

`s_colorSymbol` Set field to predefined color

`x_number` Set field to product color

`t` or `nil` Depress or raise field

`l_both` A list allows setting both check and value; pass a list of the color set

`s_colorSymbol`may be black, white, red, green, yellow.

`x_number`is an integer between 1 and 24 with 0 being background.

- CHECKBOX

The values that unset the checkbox are: `nil`, `0`, `"nil"`, `"false"` and `"no"`. All other values set the checkbox.

- TRACKBAR

If the field is a trackbar, two modes are supported.

- g_value = t

Moves the slider to the next position.

- g_value = integer

Absolutely sets trackbar to the indicated position.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form `dbid`. |
| `t_field` | Name of field. Field name is a string or symbol. |
| `g_value` | Desired value of field. may be a string, boolean, integer or floating point number or a list; function of field type. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Field set to desired value. |
| `nil` | Field not set to the desired value due to invalid arguments. |

#### Examples

See AXL Forms: Example 1.

`axlFormSetField( form "file_list" fileName)`

List Field (field is named `"list"`)

`;; display 3 items in list`

`axlFormSetField(fw, "list", "a")`

`axlFormSetField(fw, "list", "b")`

`axlFormSetField(fw, "list", "c")`

`; nil required first time list is displayed`

`axlFormSetField(fw, "list", nil)`

`;; display 3 items in list - alternative`

`axlFormSetField(fw, "list", '("a" "b" "c"))`

Color field (field is named `"color"`)

`;; sets the color field to pre-defined color "red"`

`axlFormSetField(fw, "color", `red)`

`;; sets the color field to product color 1`

`axlFormSetField(fw, "color", 1)`

`;; visually depresses the color field if not greyed`

`axlFormSetField(fw, "color", t)`

`;; visually depresses the color field and set to`

`;; pre-defined green color`

`axlFormSetField(fw, "color", '(green t))`

Tab field (field is named `"tab"`)

`;; puts the tab on top`

`axlformSetField(fw, "tab", nil)`

### axlFormSetInfo

`axlFormSetInfo( r_form t_field t_value ) => t/nil`

#### Description

Sets info `t_field` to value `t_value` in open form `r_form`. Unlike `axlFormSet`, user cannot change an info field.

Note: You can also use `axlFormSetField` for this function.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form `dbid`. |
| `t_field` | Name of field. |
| `t_value` | Desired value of field. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Field was set to desired value. |
| `nil` | Field not set to desired value due to invalid arguments. |

#### Examples

See the use of `axlFormSetField` in the "AXL Forms: Example 1".

`axlFormSetInfo( form "file_list" fileName)`

### axlFormSetMouseActive

`axlFormSetMouseActive( r_form ) => t/nil`

#### Description

Sets the option to dispatch the MouseActive event on a form.

While this can be use to display dynamic help on a per field basis (this is what the example code does) a better method exists called the "helptip" which is driven from the form file. See the axlFormBNFDoc (note 12).

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Handle for the form |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Option was set |
| `nil` | `r_form` does not reference a valid form |

#### Examples

See `<cdsroot>/share/pcb/examples/form/basic`

### axlFormTest

`axlFormTest( t_formName ) => r_form/nil`

#### Description

This is a development function for test purposes. Given a form file name this opens a form file to check for placement of controls. If form uses standard button names (for example, ok, done, close, cancel), you can close it be clicking the button. Otherwise, use the window control. If form is currently open, exposes form and returns.

#### Arguments

| Name | Description |
|---|---|
| `t_formName` | Name of form. |

#### Value Returns

Form handle if successfully opens.

#### Examples

Open Allegro PCB Editor drawing parameter form:

`axlFormTest("status")`

### axlFormRestoreField

`axlFormRestoreField( r_form t_field ) => t/nil`

#### Description

Restores the `t_field` in the open form `r_form` to its previous value. The previous value is only from the last user change and not from the form set field functions. This is only useful in the form callback function.

Use in the `form callback` to restore the previous value when you detect the user has entered an illegal value in the field.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form `dbid`. |
| `t_field` | Name of field. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Field restored. |
| `nil` | Field not restored and may not exist. |

#### Examples

See "AXL Forms: Example 1" where the callback function checks that the user has entered a filename that is on the list of available extract view filenames. If the user-entered value is not on the list, then the program calls `axlFormRestoreField` to restore the field to its previous value.

### axlFormTitle

`axlFormTitle( r_form t_title ) => t/nil`

#### Description

`(case form->curField ("view_file" (if form->curValue (progn ; Accept user input only if on list if(member( form->curValue fileList) then axlFormSetField( form "view_file" form->curValue) else axlFormRestoreField( form "view_file")))) t)` Overrides title of the form.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form `dbid`. |
| `t_title` | String to be used for new form title |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Changed form title. |
| `nil` | No form title changed. |

#### Examples

See "AXL Forms: Example 1".

`axlFormTitle( form "Extract Selector")`

### axlIsFormType

`axlIsFormType( g_form ) => t/nil`

#### Description

Tests if argument `g_form` is a form `dbid`.

#### Arguments

| Name | Description |
|---|---|
| `g_form` | `dbid` of object to test. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | `r_form` is the `dbid` of a form. |
| `nil` | `r_form` is not the `dbid` of a form. |

#### Examples

`form = axlFormCreate( (gensym)``"extract_selector.form" '("E" "OUTER")``'_formAction t)``if( axlIsFormType(form)``then (print "Created form successfully.")``else (print "Error! Could not create form."))`

Checks that the form you create is truly a form.

### axlFormSetFieldVisible

`axlFormSetFieldVisible( r_form t_field x_value ) => t/nil`

#### Description

Sets a form field to visible or invisible.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form id. |
| `t_field` | Form field name (string). |
| `x_value` | 1 - set field visible or 0 - Set field invisible |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Form field set visible. |
| `nil` | Form field set invisible. |

### axlFormIsFieldVisible

`axlFormIsFieldVisible( r_form t_field ) => t/nil`

#### Description

Determines whether a form field is visible.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form id. |
| `t_field` | Form field name (string). |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Form field is visible. |
| `nil` | Form field is not visible. |

### Callback Procedure: formCallback

formCallback( [r_form] ) => t

#### Description

This is not a function but documents the callback interface for form interaction between a user and SKILL code. The SKILL programmer provides this function.

When the user changes a field in a form, the Allegro PCB Editor form processor calls the procedure you specified as the `g_formAction` argument in `axlFormCreate` when you created that form. The form attribute `curField` specifies the name of the field that changed. The form attribute `curValue` specifies the current value of the field (after the user changed it). If you set `g_stringOption` to `t` in your call to `axlFormCreate` when you created that form, then `curValue` is a string. If `g_stringOption` was `nil` (the default), then `curValue` is the type you specified for that field in the form file.

Note: The term `formCallback` used in the title of this callback procedure description is a dummy name. The callback function name must match the name or symbol name you used as the `g_formAction` argument in `axlFormCreate` when you created the form.

If you specify the callback name (`g_formAction`) as a string in your call to `axlFormCreate`, SKILL calls that function with no arguments. If you specify `g_formAction` as a symbol, then SKILL calls that function with the form handle as its single argument.

The callback must call `axlFormClose` to close the form and to continue in the main application code if form mode is blocking.

All form information is provided by the `r_form` argument which is a form data type. Applications can extend the data stored on this type by adding their own attributes. Please capitalize the first letter of the attribute name to avoid conflicts with future additions by Cadence to this structure. Table 11-4 and Table 11-5 show the available field types and how they impact the `r_form` data type.

Table 11-4 describes Form Field Types using the following:

| Name | Description |
|---|---|
| Type | What the user calls the field |
| Keyword | What the form file calls the field |
| curValue | Data type seen in the form dispatch and axlFormGetField. See Callback for more information. |
| curValueInt | Additional information for certain field types that can be mapped to integers. |

Table 11-4 
 Form Field Types

| Name | Description |
|---|---|
| Type | Keyword; curValue; curValueInt |
| Button | `MENUBUTTON`; dispatch action only (t); 1 |
| Check Box | `CHECKLIST`; `t/nil`; 0 or 1 |
| Radio Button | `CHECKLIST`; `t/nil`; 0 or 1 |
| Long (integer) | `INTFILLIN`; integer number; Integer |
| Real (float) | `REALFILLIN`; float number; n/a |
| String | `STRFILLIN`; string; n/a |
| Enum (popup) | `ENUMSET`; string; Possible integer1 |
| List | `LIST`; string; Offset from start of list (`0` = first entry). |
| Color well | COLOR; `t/nil`; `1` or `0` |
| Tab | TABSET/TAB; string or `t`; n/a or `1`/`0` |
| Tree | TREEVIEW; string; see `axlFormTreeViewSet` |
| Text | INFO; n/a; n/a |
| Graphics | THUMBNAIL; n/a; n/a |
| GRID | GRID; see Using Grids |

| Name | Description |
|---|---|
| 1 | Integer if the dispatch value of the pop-up is an integer. |

Notes:

- What distinguishes between a radio button and a check box is that radio buttons are a group of boxes where only one can be set. To relate several check boxes as radio buttons, supply the same label name as the third field (groupLabel) in the form file description:

`CHECKLIST <fieldLabel> <groupLabel>`

When a user sets a radio button, the button being unset will dispatch to the application's callback with a value of nil.

- Enum will only set curValueInt on dispatch when their dispatch value of their popup uses an integer. Otherwise this field is `nil`.

- Tabs can dispatch in two methods:

- Default when a tab is selected, your dispatcher receives the tab name in the curField and curValue is t.

- If "OPTIONS tabsetDispatch" is set in the TABSET of the form file, then when a tab is selected your application dispatcher receives the TABSET as the curField and the curValue being the name of the TAB that was selected.

- INFO fields can be static where the text is declared in the form file or dynamic where you can set the text via the application at run-time. To achieve dynamic access, enter the following in the form file:

`TEXT "<optional initial text>"`

`INFO <fieldLabel>`

`... reset of TEXT section ...`

- Thumbnails support the following methods:

- static bitmap declared via the form file

- bitmaps that can be changed by the application at run-time

- basic drawing canvas -- see Chapter 12, "Simple Graphics Drawing Functions"

- Buttons are stateless. The application cannot set the button to the depressed state. You can only use axlFormSetField to change the text in the button. Several button fieldLabels are reserved. Use them only as described:

| Name | Description |
|---|---|
| done or OK | Do action and close the form. |
| cancel | Cancel changes and close the form. |
| print | Print the form -- do not use. |
| help | Call cdsdoc for help about the form -- do not use. |

Table 11-5 
 Form Attributes

| Name | Description |
|---|---|
| Attribute Name | Set?; Type*; Description |
| `curField` | no; string; Name of form field just changed |
| `curValue` | no; See -->; Depends on value of `curField` (`string`, `int`, `float`, `boolean`) |
| `curValueInt` | no; See -->; Depends on value of `curField` field |
| `doneState` | no; int; `0` = action; `1` = done; `2` = cancel; `3` = abort |
| `form` | no; string; Name of this form |
| `isChanged` | no; `t/nil`; `t` = user has changed one or more fields in form. |
| `isValueString` | no; `t/nil`; `t` = all field values are strings`nil` = one or more fields are not strings |
| `objType` | no; string; Type of object, in this case `"form"` |
| `type` | no; string; Form type, always `"fixed"` |
| fields | no; list of strings; All fields in the form. |
| infos | no; list of strings; All info fields in the form. |
| event | no; symbol; Grid control only -- see Using Grids |
| row | no; integer; Grid control only |
| col | no; integer; Grid control only |
| treeViewSelState | no; integer; Tree control only |
| *	You can add your own attribute types to the form type. It is recommended you capitalize the first letter of the name to avoid conflict with future Allegro PCB Editor releases. |  |

Notes:

- The doneState shows 0 for most actions. Selecting a Done or OK button sets the done state. Selecting a Cancel button sets the cancel state. With the done or cancel state set, you use `axlFormClose` to close the form. Setting the abort state closes the form, even if you do not issue an `axlFormClose` command.

- Data type is dependant on the field type. See Table 11-4 for more information on Form Field Types.

- The infos list is different from the fields list. The infos list comprises static text strings that the program can change at run-time. The fields list comprises all other labels which can be changed by the user including even those on buttons and tabs, greyed and hidden fields.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form `dbid`. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Always returns `t`. |

#### Examples

See axlFormCreate and axlFormBuildPopup for examples.

### axlFormAutoResize

`axlFormAutoResize( r_form ) => t/nil`

#### Description

Resizes a form to fit its controls. Recalculates the required width and height and resizes the form based on the current visibility of the form's fields.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Form handle. |
| `t_field` | Form field name (string). |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Form resized. |
| `nil` | `r_form` does not reference a valid form. |

