<!--
source: algroskill/11frmint.md
part: 1/3
estimated_tokens: 13490
-->

### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

11
==

Form Interface Functions
========================

Overview
--------

This chapter describes the control types and functions you use to create Allegro PCB Editor forms (dialogs) and interact with users through them.

Allegro PCB Editor AXL forms support a variety of field types. See[Callback Procedure: formCallback](#428663 "11") and [Using Forms Specification Language](#480398 "11") for a complete description of field types.

The Skill implementation of the forms package does not support the all functionality present in the core form package; short fields and variable tile forms.

#### See Also

[axlFormCreate](#414342 "11") - open a form

[axlFormCallback](#469106 "11") - callback model for interaction with user

[axlFormBNFDoc](#472343 "11") - Backus Naur Form, form file syntax, demos

[axlFormTest](#477426 "11")

### Programming

It is best to look at the two form demo.

* basic controls --`axlform.il/axlform.form`

* grid control -`fgrid.il/fgrid.form`

* multi-select grid control -`fgrid-msel.il/fgrid.form`

The first step is to create form file. Use`axlFormTest` to ensure fields are correctly positioned.

The following procedure is generally used.

* Open form (`axlFormCreate`)

* Initialize fields (`axlFormSetField`)

* Display Form (`axlFormDisplay`)

* Interactive with user (`axlFormCallback`)

* Close Form (`axlFormClose`)

* Many users find that it is easier to distribute their program
  using a form if they embed the form file in their Skill code.
  In this case use Skill to open a temporary file and print
  the statements, open for form, then delete the file.

* Use`axlFormTest`("<form file>") to interactively adjust of fields.

* You can use "`ifdef`", "`ifndef`", and Allegro environment variables
  (`axlSetVariable`) to control appearance of items in the form file.

### Field / Control

Most interaction to the controls are via axlFormSetField, axlFormGetField, axlFormSetFieldEditable, and axlFormSetFieldVisible.Certain controls have additional APIs which are noted in the description for the control.

Most controls support setting their background and foreground colors. See`axlColorDoc` and `axlFormColorize` for more information.

Following is a list of fields and their capabilities.

#### *TABSET / TAB*

A property sheet control. Provides the ability to organize and nest many controls on multiple tabs.

Unlike other form controls you nest other form controls within TAB/ENDTAB keywords. The size of the tab is control is specified by the FLOC and FSIZE keywords used as part of the TABSET definition. The single option provided to the TAB keyword serves the dual purpose of being both the display name and the tab label name. The TABSET has a single option which is the fieldLabel of the TABSET.

The TABSET has a single option - tabsetDispatch.

When a user picks on a TAB, by default, it is dispatched to the application as the with the fieldLabel set to the name of the tab and the fieldValue as a 't'. With this option we use the fieldLabel defined with the TABSET keyword and the fieldValue as the tab name. In most cases you do not need to handle tab changes in your form dispatch code but when you do each dispatch method has its advantages.

**Note:** TABSETs cannot be nested.

#### *GROUP*

A visible box around other controls. As such, you give it a width, height and optional text. If width or height is 0, we draw the appropriate horizontal or vertical line. Normally the group text is static but you can change it at run-time by assigning a label to the group.

#### *TEXT*

Static text, defined in the form file with the keyword "TEXT". The optional second field (use double quotes if more then one word) is any text string that should appear in the field. An optional third field can be use to define a label for run-time control. In addition the label INFO can be used to define the field label and text width.

Multi-line text can be specified by using the FSIZE label with a the height greater then 2. If no FSIZE label is present then a one-line text control is assumed where the field width is specified in the INFO label.

OPTIONS include (form file)

> any of:

> > bold - text is displayed in bold font

> > underline - text is displayed with underline

> > border - text is displayed with a sunken border

> > prettyprint - make text more read-able using upper/lower case

> and one of justification:

> > left - left justified (default)

> > center - center text in control

> > right - right justify text

#### *STRFILLIN*

Provides a string entry control. The STRFILLIN keyword takes two required arguments, width of control in characters and string length (which may be a larger or smaller value then the width of the control).

There are three variations of the fillin control.

* single line text

* single line text with a drop-down (use POP keyword).
  The drop-down provides the ability to have pre-defined values for the user.

* multi-line text control. Use a FSIZE keyword to indicate field width and height.

#### *INTFILLIN*

Similar to a STRFILLIN except input data is checked to be an integer (numbers 0 to 9 and + and -). Use the LONGFILLIN keyword with two arguments; field width and string length.

It only supports variations 1 and 2 of STRFILLIN.

It also supports a minimum and maximum data verification. This can be done via the form file with the MIN and MAX keywords or at run-time via`axlFormSetFieldLimits`.

#### *INTSLIDEBAR*

This is a special version of the INTFILLIN, it provides an up/down control to the right of the field that allows the user to change the value using the mouse. You should use MIN/MAX settings to limit the allowed value.

#### *REALFILLIN*

Similar to INTFILLIN except supports floating point numbers. Edit checks are done to only allow [0 to 9 .+-]. If addition to min/max support you can also provide number of decimals via the DECIMAL keyword or at run-time via`axlFormSetDecimal`.

#### *MENUBUTTON*

Provides a button control. Buttons are stateless. The MENUBUTTON keyword takes two options; width and height.

A button has one option - multiline.

If button text cannot fit on one line wrap it. Otherwise text is centered and restricted to a single line.

A button can have a popup by inserting the "POP" label.

With no popup pressing the button dispatches a value of 1. If it is a button with a popup then the dispatch is the dispatch entry of the popup.

Standards:

> - use "..." if button brings up a file browser

> - append "..." to text of button if button brings up another window

> - use these labels for:

> > > close - to Close dialog without

> > > done/ok - to store changes and close dialog

> > > cancel - to cancel dialog without making any changes

> > > help - The is reserved for cdsdoc help

> > > print - do not use (will get changed to Help).

#### *CHECKLIST*

Provides a check box control (on/off). Two variants are supported:

* a check box

* a radio box

For both types the CHECKLIST control takes an argument for the text that should appear to the right of the checkbox.

A radio box allows you to several checkboxes to be grouped together. The form package insures only one radio box be set. To enable a radio grouping provide a common text string as a third argument to the CHECKLIST keyword. An idiosyncrasy of a radio box is that you will be dispatched for both the field being unset and also for the field being set.

#### *ENUM(sometimes called combo box)*

Provides a drop-down to present the user a fixed set of choices. The drop-down can either be pre-defined in the form file via the POPUP keyword or at run-time with`axlFormBuildPopup`. Even if you choose to define the popup at run-time, you must provide a POPUP placeholder in the form file.

POPUP entries are in the form of display/dispatch pairs. Your setting and dispatching of this field must be via the dispatch item of the popup (you can always make both the same). This technique allows you to isolate what is displayed to the user from what your software uses. The special case of nil as a value to axlFormSetField will blank the control.

Two forms of ENUM field are supported, the default is single line always has the drop-down hidden until the user requests it. In this case only define the ENUMSET with the width parameter. A multi-line version is available where the drop-down is always displayed. To enable the multi-line version specify both the width and height in ENUMSET keyword.

* FILLIN fields also offer ENUM capability, see below.

OPTIONS include (form file)

* prettyprint - make text more read-able using upper/lower case.

* ownerdrawn - provided to support color swatches next.to subclass names. See axlSubclassFormPopup.

* dispatchsame - Normally if user selects same entry that is currently shown it will not dispatch.

#### *LIST*

A list box is a control that displays multiple items. If the list box is not large enough to display all the list box items at once, the list box provides the required horizontal or vertical scroll bar.

We support two list box types; single (default) and multi-selection. You define a multi-select box in form file with a "OPTIONS multiselect" List boxes have a width and height specified by the second and third options to the LIST keyword. The first option to the LIST keyword is ignored and should always be an empty string ("").

List box options are:

> SORT - alphabetical sort.

> ALPHANUMSORT - takes in account trailing numbers so a NET2 appears before a NET10 in the list.

> PRETTYPRINT - case is ignored and items are reformatted for readability.

Special APIs for list controls are:`axlFormListOptions`, `axlFormListDeleteAll`, `axlFormListSelect`, `axlFormListGetItem`, `axlFormListAddItem`, `axlFormListDeleteItem`, `axlFormListGetSelCount`, `axlFormListGetSelItems`, `axlFormListSelAll`.

For best performance in loading large lists consider passing a list of items to`axlFormSetField`.

#### *THUMBNAIL*

Provides a rectangular area for bitmaps or simple drawings. You must provide a FSIZE keyword to specify the area occupied by the thumbnail.

In bitmap mode, you can provide a bitmap as an argument to the THUMBNAIL keyword or at run time as a file to`axlFormSetField`. In either case, BMPPATH and a `.bmp` extension is used to locate the bitmap file. The bitmap should be 256 colors or less.

For bitmaps one OPTION is supported:

> stretch - draw bitmap to fill space provided. Default is to center bitmap in the thumbnail region.

In the drawing mode you use the APIs provided by`axlGRPDoc` to perform simple graphics drawing.

#### *TREEVIEW*

Provides a hierarchical tree selector. See[axlFormTreeViewSet](#520741 "11").

#### *GRID*

This provides a simple spreadsheet like control. See axlFormGridDoc for more info.

#### *COLOR*

Provides a COLOR swatch. Can be used to indicate status (for example: red, yellow, green). The size of the color swatch is controlled by a width and height option the COLOR keyword.

Add the INFO\_ONLY keyword to have a read-only color swatch. Without INFO\_ONLY the color swatch provides CHECKBOX like functionality via its up/down appearance.

With COLOR swatches you can use predefine colors or Allegro database colors. See axlColorDoc.

#### *TRACKBAR*

Provides a slider bar for setting integer values. The TRACKBAR keyword takes both a width and height and the bar may be either horizontal or vertical.

The length of step of the trackbar can be set in the form file where MIN is the tick mark interval and MAX is the length of the trackbar. The minimum tick mark is 1 and is usually indicated by setting MIN to 0 in the form file.

You can change the length and tick mark interval at run-time through`axlFormSetFieldLimits`

The trackbar indicator can be moved through`axlFormSetField`.

#### *PROGRESS*

Provides a progress bar usually used to indicate status of time consuming operations. For setting options to the progress meter pass of list of 3 items to axlFormSetField which are (<step value> <number of steps> <initial position>). A subsequent nil passed to axlFormSetField will step the meter by the<step value>.

PROGRESS keyword provides for both a width and height of the bar. Bar should be horizontal.

You get information from the user using forms that support the following modes:

****Table 11-1****
**Form Modes**

|  |
| --- | ---
| **Form Mode** | **Description**
| Blocking with no callback | Easy to program. Limited to user interaction, such as checking that the information entered for each field uses syntax acceptable to the form's package. Your program calls`axlUIWBlock` after displaying the form. The user can close a form that has the standard *OK* or *Cancel* button.  After*OK* or *Cancel* is selected, `axlUIBlock` returns allowing you to query field values using `axlFormGetField`.  **Note:** Use this programming model only with simple forms.
| Blocking with callback | Prevents use of Allegro PCB Editor until the user enters information in the dialog. The form callback you provide lets your interactive program accept the data entered.
| Callback with no blocking | Works like many native Allegro PCB Editor forms. The user can work with both the form and other parts of Allegro PCB Editor.  With Allegro PCB Editor database transactions, the programming is more complex. You can use transactions while the form is open by declaring your command interactive. You end your command when another Allegro PCB Editor command starts by using`axlEvent`.
| Options form | Allegro PCB Editor window to the left of the canvas. The options (ministatus) form is non-blocking and restricted to the Options panel size. See`axlMiniStatusLoad` for details.
Do not attempt to set the Button field (except*Done*, *Cancel* and *Help*), as it is designed to initiate actions. Consequently, having buttons in a form without a callback function registered renders those buttons useless.

**Note:** AXL-SKILL does not support the short fields and variable tiles which are part of the Allegro PCB Editor core form package.

You can set background and foreground color on many form fields. For more information, see[axlFormColorize](#463432 "11"). For information on color specific to grids, see [Using Grids](#461722 "11").

#### Examples

These examples, especially the basic one, help you understand how the forms package works:

|  |
| --- | ---
| basic | Demonstrates basic form capabilities.
| grid | Demonstrates grid control capabilities.
| wizard | Demonstrates use of a form in Wizard mode.
Use the examples located in`<``cdsroot``>/share/pcb/examples/form` as follows:

* Copy all the files from one of the directories to your computer.

* Start Allegro PCB Editor.

* From the Allegro PCB Editor command line, change to the directory to which you copied the files as shown:

> `cd <directory>`

* Load the SKILL file in the directory.

> **Note:** The SKILL file has the`.il` extension.

> `skill load "<filename>"`

* Start the demo by typing on the Allegro PCB Editor command line as shown:

> For basic demo:

> > `skill formtest`

> For grid demo:

> > `skill gridtest`

* Examine the SKILL code and form file.

* Setting the Allegro PCB Editor environment variable`TELSKILL` opens a SKILL interpreter window that is more flexible than the Allegro PCB Editor command area. On UNIX, if you set this variable before starting the tool then the SKILL type-in area is the X terminal you used to start Allegro PCB Editor. See the enved tool to configure the width and height of the window.

Using Forms Specification Language
----------------------------------

*Backus Naur Form* (BNF) is a formal notation used to describe the syntax of a language. Form File Language Description is the BNF grammar for the Forms Specification Language. Forms features in new versions are not backwards compatible.

The following table shows the conventions used in the form file grammar:

|  |
| --- | ---
| **Convention** | **Description**
| `[ ]` | Optional
| `{ }` | May repeat one or more times
| `< >` | Supplied by the user
| `|` | Choose one or the other
| `:` | Definition of a token
| `CAPS` | Items in caps are keywords
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

`formtype:            FIXED | VARIABLE`

`- FIXED forms have one unlabeled TILE stanza`

`- VARIABLE forms have one or more label TILE stanzas`

`- Skill only supports FIXED form types.`

`PORT:`

```
-    Width and height of the form. Height is ignored for fixed forms which auto-calculate required height.Width must be in character units.
```

`HEADER:`

```
-    Initial string used in the title bar of the form. This may be overridden by the application.
```

`form_header:`

`[{default_button_def}]`

`[{popup_def}]`

`[{message_def}]`

`default_button_def:`

`DEFAULT <label>`

```
-    Sets the default button to be <label>. If not present, the form sets the default button to be one of the following: ok (done), close, or cancel.
```

`-    Label must be of type MENU BUTTON.`

`popup_def:`

`POPUP <<popupLabel>> {"<display>","<dispatch>"}.`

```
-    Popups may be continued over several lines by using the backslash (\) as the last character on a line.
```

`message_def:`

`MESSAGE messageLabel messagePriority "text"`

`form_options:`

`[TOOLWINDOW]`

```
-    This makes a form a toolwindow which is a floating toolbar. It is typically used as a narrow temp window to display readouts.
```

`[FIXED_FONT]`

```
-    By default, forms use a variable width font. This option sets the form to use a fixed font. Allegro PCB Editor uses mostly variable width while SPECCTRAQuest and SigXP use fixed width fonts.
```

`[AUTOGREYTEXT]`

```
-    When a fillin or enum control is greyed, grey static text to the left of it.
```

`[UNIXHGT]`

```
-    Works around a problem with Mainsoft in 15.0 where a button is sandwiched vertically between 2 combo/fillin controls. The button then overlaps these controls. This adds extra line spacing to avoid this. You should only use this option as a last resort. In a future release, it may be treated as a Nop. On Windows, this is ignored.
```

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

`-    Sets field to be read-only`

`[POP "<popupName>"]`

`-    Assigns a popup with the field.`

`-    A POPUP definition by the same name should exist.`

`-    Supported by field_types: xxxFILLIN, INTSLIDEBAR, MENUBUTTON,and ENUMSET.`

`[MIN <value>]`

`[MAX <value>]`

`-    Assigns a min and/or max value for the field.`

`-    Both supported by field types: LONGFILLIN, INTSLIDEBAR, REALFILLIN.`

`-    Value either an integer or floating point number.`

`[DECIMAL <accuracy>]`

`-    Assigns a floating min and/or max value for the field.`

`-    Assigns the number of decimal places the field has (default is 2)`

`-    Both supported by field_types: REALFILLIN`

`[VALUE "<display>"]`

`-    Initial field value.`

`-    Supported by field_types: xxxFILLIN`

`[SORT]`

`-    Alphanumeric sorted list (default order of creation)`

`-    Supported by field_type: LIST`

`[OPTIONS dispatchsame]`

`-    For enumset fields only`

```
-    If present, will dispatch to application drop-down selection even if the same as current. By default, the form's package filters out any user selection if it is the same as what is currently displayed.
```

`[OPTIONS prettyprint]`

`-    For enumset fields only.`

`-    Displays contents of ENUM field in a visually pleasing way.`

`[OPTIONS ownerdrawn]`

`-    For enumset fields only.`

`-    Used to display color swatches in an ENUM field. See axlFormBuildPopup.`

`x:`

`y:`

`w:`

`h:`

`-    Display geometry (integers)`

```
-    All field, group and text locations are relative to the start of the tile they belong or to the start of the form in the case of FIXED forms.
```

`-    x and h are in CHARHEIGHT/2 units.`

`-    y and w are in CHARWIDTH units.`

`button_options:`

`[MULTILINE]`

```
-    Wraps button text to multiple lines if text string is too long for a single line.
```

`dispatch:`

`-    String that is dispatched to the code.`

`display:`

`-    String that is shown to the user.`

`bitmapFile:`

`-    Name of a bmp file. Finds the file using BITMAPPATH`

`resource:`

```
-    Integer resource id (bitmap must be bound in executable via the resource file). '#' indicates it is a resource id.
```

`-    Not supported in AXL forms.`

`fieldLength:`

```
-    Maximum width of field. Field scrolls if larger than the field display width.
```

`label:`

`-    Name used to access a field from code. All fields should have unique names.`

`-    Labels should be lower case.`

`messageLabel:`

`-    Name used to allow code to refer to messages.`

`-    Case insensitive.`

`messagePriority:`

```
-    Message priority 0 - (not in journal file), 1 - information, 2 - warning, 3 - error, 4 - fatal (display in message box)
```

`radioLabel:`

```
-    Name used to associate several CHECKLIST fields as a radio button set. All check fields should be given the same radioLabel.
```

`-    Should use lower case.`

`textOptions:`

`[RIGHT | CENTER | BORDER | BOLD | UNDERLINE]`

`-    TEXT/INFO field type`

`-    text justification, default is left`

`-    BORDER: draw border around text`

`[STRETCH]`

`-    THUMBNAIL field type`

`-    Stretch bitmap to fit thumbnail rectangle, default is center bitmap.`

`tabsetOptions:`

`[tabsetDispatch]`

```
-    By default, tabsets dispatch individual tabs as seperate events. This is not always convenient for certain programming styles. This changes the dispatch mode to be upon the tabset where a selection of a tab causes the event:
```

`field=tabsetLabel value=tabLabel`

`The default is:`

`field=tabLabel value=t`

`Script record/play remains based upon tab in either mode.`

`tileLabel:`

`-    Name used to allow code to refer to this tile.`

`-    Should use lower case.`

`-    Only applies to VARIABLE forms.`

`-    Not supported with AXL forms.`

`tileType        [0|1|2]`

`-    0 top tile, 1 scroll tile, 2 bottom tile`

`-    Only applies to VARIABLE FORMS.`

```
-    Region where tile will be instantiated. Forms have the following regions: top, bottom, and scroll (middle).
```

`-    Not supported with AXL forms.`

`flex_def:        Rule based control sizing upon form resize (see axlFormFlex)`

`[FLEXMODE <autorule>]`

`[FLEX <label> fx fy fw fh]`

`FLEXMODE <autoRule>`

`FLEX        fx fy fw fz`

`-    see axlFormFlexDoc`

`autorule:        -    Generic sizing placement rule.`

`fx:`

`fy:`

`fh:`

`-    Floating value between 0 and 1.0`

* Follow these rules when using BNF format:

* `FILE_TYPE` line must always appear as the first line of the form file in the format shown.

* Form files must have a`.form` extension.

* There may only be one`FORM` in a form file.

* There must be one and only one`TILE` definition in a `FIXED` form file. <`tileLabel`> and `TPANEL` are not required.

* Unless otherwise noted, character limits are as follows:
  labels - 128
  title - 1024
  display - 128 except for`xxx``FILLIN` types which are 1024

* Additional items may appear in existing form files (`FGROUP`) but they are obsolete and are ignored by the form parser. `REALMIN` and `REALMAX` are obsolete and replaced by `MIN` and `MAX` respectively. They will still be supported and are mapped to `MIN` and `MAX`.

* For`grid_def`, two headers (side and top) are maximum.

* `FSIZE` - Most controls determine the size from the text string.
  You must provide `FSIZE` for `GROUP`, `GRID`, `TREEVIEW` and `LIST` controls. For `TEXT` controls, if `FSIZE` is provided, it overrides the width calculated by the text length and, if present, the `INFO` width. If using the `INFO` line, put the `FSIZE` line after it.

* Both`TEXT` and `GROUP` support the optional label on their definition line. This was added as a convenience in supporting `FLEX` capability. If the application wishes to dynamically modify the text, the `INFO` keyword is normally used. When both are present, the `INFO` keyword takes precedence.

* If the optional label for`TABS` is not provided, the field display name is used. Any spaces within the field display name are replaced by underscores (`"_"`).

* The height ([`h`]) for `ENUMSET` is optional. When not set (the default), the drop-down is only presented under user control. When height is greater than 1, the drop-down is always visible (Microsoft SIMPLE drop-down). Only use this feature in forms that can afford the space consumed by the drop-down.

The forming syntaxes are NOT supported by the form editor.

This syntax is supported and may be placed anywhere in the form file to support conditional processing of the form file:

> `#ifdef <variable>`

> `{}`

> `{ #elseif <variable>`

> `}`

> `{    #else`

> `{}    }`

Moving and Sizing Form Controls During Form Resizing
----------------------------------------------------

You can use the axlFormFlexDoc command to move and size controls within a form based on rules described in the form file. Rules may either be general (`FLEXMODE`) or specific to a single control (`FLEX`.) Flex adjusting of the controls is adjusting the form larger than its base size. Sizing the form smaller than the base size disables flex sizing.

Controls are divided into the following classes:

* Containers
  Containers can have other controls as members, including other containers. To be a container member is automatic; the control's`xy` location must be within the container. Container controls of the form are `TABSET`s and `GROUP`s.

* All others, including containers

All controls except`TABS`, which are locked to their `TABSET`, may be moved when a form is resized. Sizing width or height is control dependent as shown:

****Table 11-2****
**Controls - Resizing Options**

| **Control** | **Resizing Options**
| `REALFILLIN` | width
| `LONGFILLIN` | width
| `STRFILLIN` | width
| `INTSLIDEBAR` | width
| `ENUMSET` | width
| `PROGRESS` | width
| `TRACKBAR` | width
| `LIST` | width and height
| `GRID` | width and height
| `TREEVIEW` | width and height
| `THUMBNAIL` | width and height
| `GROUP` | width and height
| `TABSET` | width and height
| `<``others``>` | no change in size
#### Using Global Modes or FLEXMODE

`FLEXMODE` represents the general rules that apply to all controls in the form except those with specific overrides (`FLEX`). Only a single `FLEXMODE` is supported per form. The last encountered in the form file is used. The following rules are supported:

* EdgeGravity
  All controls have an affinity to the closest edge of their immediate container. Exceptions are:`<``xxx``>FILLIN` and `INTSLIDEBAR` controls. The edge gravity, for these, is based upon a `TEXT` control positioned to the left of the control.

* EdgeGravityOne
  Similar to EdgeGravity except that controls are only locked to the right or bottom edge, but not both. The closest edge is used.

* StandButtons
  Only effects button controls. Uses the same logic as EdgeGravityOne.

FLEXMODE can have an optional pair of additional arguments that specify the minimum form width and height for flexing. The argument values are in character units. Flexing will stop in the given direction when the width/height goes below the specified value.

#### Managing Sizing and Movement of Individual Controls

You use the`FLEX` parameter to manage the sizing and movement of individual controls as shown:

> `FLEX fx fy fw fh`

The`FLEX` parameter overrides any `FLEXMODE` in effect for that control, and is based upon parameters (`fx`, `fy`, `fw`, `fh`). These values, which are floating point numbers between 0.0 and 1.0, control the fraction of the change in container size that the control should move or change in size:

**fx and fy Parameters**

1. Control remains locked to the left or top edge of its container.
2. Control remains locked to the right or bottom edge of its container.

**fw and fh Parameters**

1. Control is not resized.
2. Control is resized in width or height based upon the size change of its container.

A container's position and size effect the container's member controls. Containers are hierarchical. Make sure the container of the control also has a`FLEX` constraint. The sum of the width and height of the immediate controls of a container should not be greater than `1` to prevent overlapping. `TABSETS` are slightly different since sizing of their member controls is also based on the `TAB` they belong to.

* ***It is possible to create FLEX constraints that result in overlapping controls. FLEX does not protect against this.***

#### FLEX Restrictions

* The form must be`FIXED`.

* While`FLEX` rules may appear anywhere in the form file, they should be grouped together immediately before the <`ENDTILE`>

* Range errors for`FLEX` option or applying width or height to controls not supporting them are silently ignored.

#### Example 1

> `FLEXMODE standbuttons`

> `FLEX list 0 0 1 1`

> Simple list-based form with buttons (label of`LIST` is list.) The list gets all of form sizing.

#### Example 2

> `FLEXMODE EdgeGravity`

> `FLEX a 0 0 0.33 1`

> `FLEX b 0.33 0 0.67 1`

> `FLEX c 0.67 0 1 1`

> Form containing 3 lists (`a`, `b`, and `c`) positioned equally across the form. Each list gets the total change in height, but shares in the increase in form width. Thus, if the form changes width, each control gets 1/3 of this change. Since the list's widths change, the list must move to the right.

#### Example 3

> `FLEX l1 0 0 1 0.5`

> `FLEX g1 0 0.5 1 0.5`

> `FLEX l2 0 0 1 1`

> Form has a group (`g1`) containing a list (`l2`). These are at the bottom of another list (`l1`). Both lists share in any change of the form size. The second list (`l2`) is a member of the group container (`g1`), so it moves if the group moves (`0` for `y`) and it gets all of the group resizing (`h` is `1`).

#### Example 4

> `FLEX g1 1 1 0 0`

> `FLEX l1 0 0 1 1`

> Form has a group (`g1`) with a list member (`l1`), but the list doesn't resize because the list is a member of the group which has `0:0` sizing. Though the list has `1:1` sizing, it never changes in size because its container never changes in size. Both the group and its member list move because the group has a `1:1` `x/y` factor.

#### Example 5

> `FLEX t1 0 0 1 1`

> `FLEX l1 0 0 1 1`

> `FLEX l2 0 0 1 1`

> Form is a tabset (`t1`) with 2 tabs. Each tab controls a list (`l1` and `l2`) that accommodates the maximum change in the form size.

* Use`axlFormTest`(*<*`formname`*>*) to experiment with your form.

Using Grids
-----------

Grids offer tabular support and the following features:

* Optional side and top headers

* Several data types on a per column basis: Text (info), Checkbox with optional text, Enum (Drop-drop) and Fillin (text box with built-in types: string, integer, and real.)

* Row and column indexing which is 1-based

Grids have the following limits:

* Maximum of 200 columns

* Maximum rows of 1,000,000

* Maximum field string length per column of 256 characters

* Column creation only at grid initialization time.

#### Form File Support for Grids

The following defines the form file structure relating to grids.

`GRID`

`Standard items`

`FLOC    -    x, y location`

`FSIZE    -    width and height including headers if used`

```
POP    -    Optional right button popup for body. Also requires application to set the GEVENT_RIGHTPOPUP option.
```

`OPTIONS:`

`INFO    -    Entire grid is info-only even if it contains typeable fields`

`HLINES    -    Draw horizontal lines between columns`

`VLINES    -    Draw vertical lines between rows`

`USERSIZE    -    Allow user to resize columns.`

```
MULTISELROW        allows multi-row select (also set via Skill API, axlFormGridEvents)
```

`HEADERS (GHEAD)`

`-    Specified within GRID section.`

`-    TOP and SIDE header (only one per type allowed in a grid)`

`HEADSIZE    -    Height (TOP) or width (SIDE) for the header.`

`OPTIONS:`

`3D    -    Display raised.`

```
NUMBER    -    For side header, display row number if application does not provide text.
```

```
POP    -    Optional right mouse button popup. One per header. Requires application to set GEVENT_RIGHTPOPUP for the header.
```

#### Programming Support for Grids

The following Grid APIs are available:

|  |
| --- | ---
| `axlFormGridInsertCol` | Insert a column.
| `axlFormGridInsertRows` | Insert one or more rows.
| `axlFormGridDeleteRows` | Delete one or more rows.
| `axlFormGridEvents` | Set grid events.
| `axlFormGridOptions` | Miscellaneous grid options.
| `axlFormGridNewCell` | Obtain structure for setting a cell.
| `axlIsGridCellType` | Is item a cell data type.
| `axlFormGridSetBatch` | For setting multiple cells.
| `axlFormGridGetCell` | For getting cell data.
| `axlFormGridBatch` | Used with`axlFormGridSetBatch`
| `axlFormGridUpdate` | Update display after changes.
| `make_formGridCol` | For defstruct`formGridCol`
| `copy_formGridCol` | For defstruct`formGridCol`
In addition, the following standard form APIs may be used:

|  |
| --- | ---
| `axlFormSetFieldVisible` | Set grid visibility
| `axlFormIsFieldVisible` | Is field visible
| `axlFormSetFieldEditable` | Set grid editability
| `axlFormIsFieldEditable` | Is field editable
| `axlFormBuildPopup` | Change a popup
| `axlFormSetField` | Set individual cell.
| `axlFormRestoreField` | Restore last cell changed.Restore supports undoing last*change* event.Adding, deleting, or right mouse event reset restore.
***Multi-row select support functions:***

|  |
| --- | ---
| `axlFormGridSetSelectRows` | control selection of rows
| `axlFormGridSelectedCnt` | number of rows selected
| `axlFormGridSelected` | list of rows selected
#### Data Structures

|  |
| --- | ---
| `r_cell` | User data type for cell update (see[axlFormGridNewCell](#459451 "11"))
| `r_formGridCol` | Defstruct to describe column (see[axlFormGridInsertCol](#459328 "11"))
#### Column Field Types

Grids support the assignment of data types by column. You may change an editable cell into a read-only cell by assigning it a`s_noEdit` or `s_invisible` attribute. See `axlFormGridInsertCol` for a complete description of column attributes and `axlFormGridSetBatch` for a discussion of cell attributes.

|  |
| --- | ---
| `TEXT` | Column is composed of display only text.
| `STRING` | Column supports editable text. See edit-combo.
| `LONG` | Column supports numeric data entry cells. See edit-combo.
| `REAL` | Column supports numeric floating point entry cells.  See edit-combo.
| `ENUMSET` | Column supports combo-box (drop-down) cells. Must have a popup attribute on the column.
| `CHECKITEM` | Column has checkbox cells with optional text.
| `EDIT-COMBO` | By assigning a popup attribute at the column and/or at the cell level, you can change STRING, LONG, and REAL types to support the original text editing field with the addition of a drop-down.
#### Initializing the Grid

Once a grid is defined in the form file, you can initialize the grid as follows:

* Create required columns using`axlFormGridInsertCol`

* Create initial set of rows using`axlFormGridInsertRows`

* Create initial grid cells and headers using`axlFormGridSetBatch`,
  then on callback, use:

|
| ---
|
 **a.** | `axlFormGridNewCell`
|
| ---
|
 **b.** | `axlFormGridSetBatch`
* Set event filters using`axlFormGridOptions`.

* Display the grid using`axlFormGridUpdate`.

See`grid.il` and `grid.form` for a programming example. You can find these in the AXL Shareware area:

> `<CDS_INST_DIR>/share/pcb/etc/skill/examples/ui`

#### Dispatching Events

Unlike other form controls, an application can specify what events are dispatched. You control this using the`axlFormGridEvents` API which documents the usage. Also, the form callback structure has new fields for grids (see [axlFormGridEvents](#459032 "11").)

By default, you create a grid with the*'*rowselect enabled which is typically appropriate for a multi-column table.

#### Multi-row Selection

A super-set of row selection is the multi-row selection option. With this option the user can select multiple rows. Grids running in this mode do now support cell select or change options.

This is set in Skill via:

`axlFormGridEvents(<form> <grid> '(mrowselect))`

or from the formfile by adding the`MULTISELROW` option to the grid's `OPTION` line.

Standard selection model is supported (not extended). This means:

* left click selects a row

* shift-left click selects all rows between the initial and current row

* ctrl-left click on to selection of row that is currently selected, it de-selects

* control-a selects all rows

APIs are provided (see above) to get current selected rows and set or clear row selections.

Finally, since multiple rows may be selected the standard form callback mechanism only informs you of a selection event. You need to utilize[axlFormGridSetSelectRows](#495777 "11") to determine the current selection.

#### Using Scripting with Grid Controls

Unlike most other form controls where the programmer needs no concern over scripting, grid programmers should address scripting. By default, the grid uses the event type and
row/column number for scripting. Depending on your application, this may create scripts that do not replay given different starting data. Grids support assigning script labels to rows, to columns, and on a per cell basis.

You label by setting the`scriptLabel` attribute from the application code with the `axlFormGridInsertCol`function for a column or the `axlFormGridNewCell`function for a row, column, or per cell basis. You can also change this dynamically. Note that (`row=0`, `col=``n`) sets the `scriptLabel` for the column using `axlFormGridNewCell` and (`row=``n`, col=0) allows setting for row script labels.

The grid script line format extends upon the standard form scripting as shown:

> `FORM <formname> [tileLabel] <fieldLabel> <event> <glabel> [<value>]`

> where

> `FORM <formname> [tileLabel] <fieldLabel>`

> `-    standard form script form fieldLabel is the grid label`

> `<event> is the grid event. Grid events include:`

> `rowselect    := GEVENT_ROWSELECT`

> `cellselect    := GEVENT_CELLSELECT`

> `change    := GEVENT_CELLCHANGE`

> `rpopup    := GEVENT_RIGHTPOPUP`

> `rprepopup    := GEVENT_RIGHTPOPUPPRE`

> `lprepopup    := GEVENT_LEFTPOPUPPRE`

> ```
> <glabel> label corresponds to the location in the grid the event        occurred.
> ```

> `[<value>] optional value depending upon event.`

> `Depending on the event, the rest of the script line appears as follows:`

> `rowselect    <glabel:=row>`

> `cellselect    <glabel:=cell>`

> `change    <glabel:=cell> <value>`

> `rpopup    <glabel:=cell> <popup value>`

> `rprepopup    <glabel:=cell>`

> `lprepopup    <glabel:=cell>`

The`glabel` has several format options depending on the event:

|  |
| --- | ---
| `row` | If the row has a*scriptLabel*, it is used, otherwise the row number is used.
| `cell` | If the cell has a label, that is used. If the cell does not have a label, the row and /or column labels are used. If either the row or column does not have labels, the row and/or column number is used.
When you set a`scriptLabel` to `row`, `col`, or `cell`, the following character set is enforced: case insensitive, no white space or comma or $. Labels with these characters are replaced by an underscore (\_). You may use pure numeric strings, but if you do not label everything, scripts may fall back and use the row/grid number to resolve a number not found as a script label string.

**Notes**

* If you use`row` and `col` as the `glabel`, use a comma `(,)`to delineate between the row and column name and number.

* Do not turn on events that you do not plan to process since scripts record them. For instance, if you only process on`rowselect` (no editable cells), then only enable `rowselect`. As a side benefit, you do not have to label columns or cells since row label is sufficient.

* If you use a row and/or column heading, you may use that for assigning`scriptLabels`.

**Examples**

* If grids replace the text parameter form, you need not label the columns. A column number is sufficient. You can label the columns for script readability. This application does not require cell labeling.

* If grids replace the color form for certain color grids, like stackup, you would need to label each cell. Each class grouped in the stackup grid is not row consistent. For example, depending on design, subclasses are not the same going across the rows. Other groupings require labeling on class for`col` and `subclass` for `row` since it is orthogonal.

See[Using Grids](#461722 "11") for a grid overview.

**Headers**

You can set column (top) headers either using`axlFormGridInsertCol` at column creation time, or using `axlFormGridSetBatch` if you need to change the header using row number `0`.

Row (side) headers default to automatic run numbers with this option set in the form file. Using`axlFormGridSetBatch`, you can set the text for individual rows using col number `0`.

#### AXL Forms: Example 1

> > ```
> > FILE_TYPE=FORM_DEFN VERSION=2FORMFIXEDPORT 50 11HEADER "Extract Selector"TILETEXT "Select View File to Extract"TLOC 12 1ENDTEXTTEXT "View File:"TLOC 1 12ENDTEXTFIELD view_fileFLOC 12 12STRFILLIN 24 24ENDFIELDFIELD file_listFLOC 5 3LIST "" 40 5ENDFIELDFIELD cancelFLOC 5 15MENUBUTTON "Cancel" 8 3ENDFIELDFIELD doneFLOC 15 15MENUBUTTON "Done" 9 3ENDFIELDFIELD printFLOC 25 15MENUBUTTON "Print" 9 3ENDFIELDFIELD scriptFLOC 35 15MENUBUTTON "Script" 11 3ENDFIELDENDTILEENDFORM
> > ```

* Uses a form file (expected to be in the current directory) that can display a selection list.

* Gets the list of available extract definition (view) files pointed to by the`TEXTPATH` environment variable.

* Displays the list in the form.

> The user can then select any filename listed, and the name displays in the*View File* field.

> Selecting the*Done* button causes the form to call `axlExtractToFile`with the selected extract filename as the view file, and `myextract.dat`as the extract output filename, and closes the form. Selecting *Cancel* cancels the command and closes the form.

> The form file has`FIELD` definitions for the selection list, the *View File* field, and each of the buttons (*Cancel*, *Done*, *Print* and *Script*).

> > ```
> > ; myExtractViews.il;            -- Displays a form with a selection list of;                 the available extract definition files;            -- Lets the user select any of the files on;                 the list as the "View file";            -- Starts Allegro extract process with the;                 user-selected View file when;                the user picks Done from the form.; Function to extract user selected view to the output file.(defun myExtractViews (viewFile outFile)     axlExtractToFile( viewFile outFile)); defun myExtractViews; Function to start the view extraction(defun _extract () myExtractViews(buildString(list(cadr(parseString(    axlGetVariable("TEXTPATH"))) selectedFile) "/")            "myextract.dat")); defun _extract; Form callback function to respond(defun _formAction (form)     (case form->curField         ("done"             (axlFormClose form)             (axlCancelEnterFun)             (_extract)             t)         ("cancel"             (axlFormClose form)             (axlCancelEnterFun)             nil)         ("view_file"             (if form->curValue                 (progn                     ; Accept user input only if on list                     if(member( form->curValue fileList)                        then axlFormSetField( form                             "view_file" form->curValue)                         else axlFormRestoreField(                                form "view_file"))))             t)         ("file_list"             (axlFormSetField form "view_file"                form->curValue)             selectedFile = form->curValue             t)); case); defun _formAction; User-callable function to set up and;        display the Extract Selector form(defun myExtract ()    fileList = (cdr (cdr (getDirFiles    cadr( parseString( axlGetVariable("TEXTPATH"))))))    form = axlFormCreate( (gensym)         "extract_selector.form" '("E" "OUTER")            '_formAction t) axlFormTitle( form "Extract Selector") axlFormSetField( form "view_file" (car fileList)) selectedFile = (car fileList) foreach( fileName fileList        axlFormSetField( form "file_list" fileName))     axlFormDisplay( form)); defun myExtract
> > ```

* Creates a form named`form` with the callback function`_formAction` that analyzes user action stored in `form->curField` and responds appropriately.

* Loads the example AXL program shown.

* Enters the command`myExtract()`.

> SKILL displays the**Extract Selector** form, as specified in the form file `extract_selector.form` that this code created when it first loaded. This is a non-blocking form--you can enter other SKILL and Allegro PCB Editor commands while the form displays.

The program shows how to analyze the user selection when control passes to the callback function*\_*`formAction`. Name of the field selected by the user is in `form->curField`. In this case, that is one of the strings `done`, `cancel`, `view_file`, or `file_list`. The value of the field is in`form->curValue`. This has a value for the `view_file` and`file_list` fields.

The actions in the`callback``_formAction` are

|  |
| --- | ---
| `"done"` | The user selected the*Done* button. Closes the form, clears input using `axlCancelEnterFun`, and calls the \_extract function to execute the data extract.
| `"cancel"` | The user selected the*Cancel* button. Closes the form, clears input using `axlCancelEnterFun`, and calls the \_extract function to execute the data extract.
| `"view_file"` | The user selected the*View File* field, possibly typed an entry, and pressed *Return*. Sets the `view file` name to the current value of the *View File* field, letting the user type in a name. Name must be a name on the list displayed.
| `"file_list"` | The user picked a name from the displayed list of view file names. Name picked is`form->curValue`, and the program sets `selectedFile` (the name of the currently selected extract file) to the new value, and displays it in the *View File* field.
The*Print* and *Script* buttons have pop-ups that call predefined Allegro PCB Editor functions.

#### AXL Forms: Example 2

The form file`popup.form` for this is shown:

```
FILE_TYPE=FORM_DEFN VERSION=2FORMFIXEDPORT 50 5HEADER "Popup Selector"POPUP <PRINTP>    "to File""0","to Printer""1","to Script""2".POPUP <SCRIPTP>    "Record""record","Replay""replay","Stop""stop".POPUP <MYPOPUP>    "MyPopup1""myPopup1","MyPopup2" "myPopup2".TILETEXT "My Popup Here:"TLOC 1 1ENDTEXTFIELD my_popupFLOC 12 3ENUMSET 24POP "MYPOPUP"ENDFIELDFIELD change_popFLOC 5 6MENUBUTTON "Change" 8 3ENDFIELDFIELD doneFLOC 15 6MENUBUTTON "Done" 9 3ENDFIELDFIELD printFLOC 25 6MENUBUTTON "Print" 9 3POP "PRINTP"ENDFIELDFIELD scriptFLOC 35 6MENUBUTTON "Script" 11 3POP "SCRIPTP"ENDFIELDENDTILEENDFORM
```

Uses a form file (expected to be in the current directory) to create a pop-up. The sample program also displays in the pop-up field the value returned whenever the user selects a pop-up.

The form field`my_popup` originally has the popup values specified by the file `popup.form`(*MyPopup1* and *MyPopup2*). The AXL program responds to the *Change* button by building the pop-up display and returning the values.

> `list( list( "MyPop 1" "myPopValue1")         list( "MyPop 2" "myPopValue2"))`

A list of lists of display and dispatch string pairs.

> `list( list( "MyPop 12" 12) list( "MyPop 5" 5))`

A list of lists of display and dispatch pairs, where the display value is a string, and the dispatch value is an integer.

> `list( "MyPopValue1" "MyPopValue2")`

A list of strings, which means that each string represents both the display and dispatch values of that popup selection.

```
; formpop.il - Create and display a form with a popup; Form call back function to respond to user selection of any field in the form(defun _popAction (form)     (case form->curField         ("done"             (axlFormClose form)             (axlCancelEnterFun)             t)         ("change_pop"             (case already_changed                  (0;Use display/dispatch string pairs                     axlFormBuildPopup(form "my_popup"                      list(                     list("NewPopup A" "mynewpopup_a")                     list("NewPopup B" "mynewpopup_b")))                      axlFormSetField(form "my_popup"                        "My First Popups")                )                 (1;Display string/dispatch integer pairs                     axlFormBuildPopup(form "my_popup"                      list( list("NewPopup 12" 12)                         list("NewPopup 5" 5)))                          axlFormSetField(form "my_popup"                            "My Second Popups")                )                 (t;String is both display and dispatch                     axlFormBuildPopup(form "my_popup"                      list( "MyPopNValue1"                                 "MyPopNValue2"))                      axlFormSetField(form "my_popup"                            "My Third Popups")                     )                     )                     already_changed++                t)            ("my_popup"                 printf( "Got my_popup event:                    form->curValue %s", form->curValue)                 if( form->curValue                    (progn                     axlFormSetField( form "my_popup"                        form->curValue)))             t)         ); case    ); defun _popAction; User-callable function to set up and;    display the Extract Selector form(defun myPop ()    form = axlFormCreate( (gensym) "popup.form"        '("E" "OUTER") '_popAction t)     if( axlIsFormType(form)        then (print "Created form successfully.")         else (print "Error! Could not create form."))     axlFormTitle( form "Try My Popup")     mypopvalue = "my_start_popup"    axlFormSetField( form "my_popup" mypopvalue)     axlFormDisplay( form)    already_changed = 0); defun myPop
```

Sets the field`my_popup` to the value selected by the user and prints it.

* Enter `myPop()` on the SKILL command line to display the **Try My Popup** form.

* Press the middle mouse button over the pop-up field to display the original pop-up specified by the file`popup.form`.

* Click*Change*.

> The form displays the first set of pop-up values set by the program. The first pop-up values also display when you press the middle mouse button over the field.

* Make a selection.

> If, for example, you selected*NewPopup B*, the program prints the following on the SKILL command line:

`Got my_popup event: form->curValue mynewpopup_b`

> The following form is displayed.

* ClickChange.

> The program displays the third set of pop-ups.

AXL-SKILL Form Interface Functions
----------------------------------

This section lists the form interface functions.

### axlFormBNFDoc

This is the BNF grammar for the Forms Specification Language. New options and field types are added every release. Form files are always upwards compatible but may NOT be backwards compatible if you take advantage of a new feature. Thus, a form file created in 12.0 Allegro works in 13.0 Allegro. However, if you take advantage of the TAB control (13.0) or the RIGHT justification of TEXT (13.5), you will have a form file that will not function with 12.0 of Allegro.

The following outlines the conventions used in the grammar:

[] Optional
{} May repeat one or more times.
<> Supplied by user.
| Choose one or the other.
: Definition of a token.
CAPS Items in caps are keywords (note form parser is case insensitive)
(#) Note: See number at end of this documentation.

#### BNF

#### *form*

FILE\_TYPE=FORM\_DEFN VERSION=2 (1)
 FORM [form\_options] (3)
 formtype
 PORT w h
 HEADER "text"
 form\_header
 {tile\_def}
 ENDFORM

#### *formtype FIXED | VARIABLE*

- FIXED forms have a one unlabeled TILE stanza
 - VARIABLE forms have one or more label TILE stanzas
 - Skill only supports FIXED form types.

#### PORT

- width and height of form. Height is ignored for fixed forms which auto-calculates required height. Width must be in character units.

#### HEADER

- initial string used in title bar of form (may be overridden by application).

#### *form\_header*

