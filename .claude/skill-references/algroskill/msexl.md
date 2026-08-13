### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

27
==

Microsoft Excel Integration Functions
=====================================

### axlSpreadsheetClose

`axlSpreadsheetClose() ==> t`

#### Description

Releases the spreadsheet document in memory. All information is freed. This function should be called whenever you have completed working with the active spreadsheet document.

Once the spreadsheet information is released, you cannot access any data about it. This includes retrieving style information, cell contents, lists of worksheets, etc. Any such information that you need to reference after the spreadsheet is freed should be retrieved prior to this call.

If there is no active spreadsheet, this function does nothing.

#### Arguments

Nothing

#### Values Returned

|  |
| --- | ---
| `t` | Spreadsheet information successfully freed.
#### Example

The following example creates a simple spreadsheet, adds information to the first cell ("Hello"), writes the spreadsheet, and closes it.

`axlSpreadsheetInit()==> t`

`axlSpreadsheetSetWorksheet("First")==> t`

`axlSpreadsheetDefineCell(1 1 "Default" "String" "Hello")==> t`

`axlSpreadsheetWrite("example.xml")==> t`

`axlSpreadsheetClose()==> t`

#### See Also

[axlSpreadsheetInit](#1068036 "27"), [axlSpreadsheetRead](#1069134 "27"), [axlSpreadsheetWrite](#1068304 "27")

### axlSpreadsheetDefineCell

`axlSpreadsheetDefineCell(x_rowx_colt_stylet_typet_value)==> t / nil`

#### Description

Completely defines a single cell in the active worksheet. This function is more efficient than calling[axlSpreadsheetSetCell](#1068101 "27") with multiple [axlSpreadsheetSetCellProp](#1075986 "27") calls afterwards.

#### Arguments

|  |
| --- | ---
| x\_`row` | Row index (1-based) for the desired cell.
| x\_`col` | Column index (1-based) for the desired cell.
| t\_`style` | Style name to apply to this cell / nil for default.
| t\_`type` | Type definition for this cell / nil for default (string).
| `t_value` | Value for cell / nil for empty.
#### Value Returned

|  |
| --- | ---
| `t` | Cell successfully defined.
| `nil` | Cell not defined. See console for reason.
#### Example

The following example sets the contents of cell 1, 1 in the active worksheet to be the string "Hello" using the default style.

`axlSpreadsheetDefineCell(1 1 "Default" "String" "Hello")==> t`

#### See Also

[axlSpreadsheetGetCell](#1067927 "27"), [axlSpreadsheetSetCell](#1068101 "27"), [axlSpreadsheetSetCellProp](#1075986 "27")

### axlSpreadsheetDoc

#### Description

The axlSpreadsheet family of functions allow you to read and write Microsoft's open XML-based spreadsheet format from within skill. You can create a spreadsheet from data within your active Allegro tool, or you can read a spreadsheet and extract information from it to update your database.

Documentation for individual functions is separately available. This entry provides an overview, as well as a small example of how to use the API routines together.

#### Example

The following is a simple example which creates a small, two-worksheet spreadsheet with a few formatting style definitions and cells which use those styles to format their contents when the spreadsheet is viewed with a tool such as Microsoft's Excel.

`procedure( spreadsheetExample() ; Initialize an empty spreadsheet.`

`; Note that you do not need to provide a name until you`

`; wish to write the spreadsheet to disk.`

`axlSpreadsheetInit()`

`; Define inital, default style.`

`; Styles may be defined at any point during the spreadsheet's`

`; construction, but must be defined before they are referenced`

`; by any row, column, or cell.`

`axlSpreadsheetSetStyle("Default" nil)`

`axlSpreadsheetSetStyleProp("Alignment" "Vertical" "Top")`

`axlSpreadsheetSetStyleProp("Alignment" "Horizontal" "Left")`

`axlSpreadsheetSetStyleProp("Alignment" "WrapText" "1")`

`; Define a second style, derived from the Default style, which`

`; will include a thin border outline and specifies a red`

`; background fill.`

`axlSpreadsheetSetStyle("Red" "Red Cell")`

`axlSpreadsheetSetStyleParent("Default")`

`axlSpreadsheetSetStyleBorder("Left" nil "Continuous" "2")`

`axlSpreadsheetSetStyleBorder("Right" nil "Continuous" "2")`

`axlSpreadsheetSetStyleBorder("Top" nil "Continuous" "2")`

`axlSpreadsheetSetStyleBorder("Bottom" nil "Continuous" "2")`

```
axlSpreadsheetSetStyleProp("Fill" "Color"   axlSpreadsheetGetRGBColorString(255 0 0))
```

`axlSpreadsheetSetStyleProp("Fill" "Pattern" "Solid")`

`; Define the first worksheet in the spreadsheet.`

`axlSpreadsheetSetWorksheet("First")`

`; With a wider first column`

`axlSpreadsheetSetColumnProp(1 "Width" "500")`

`axlSpreadsheetDefineCell(1 1 "Default" "String" "Default formatted cell")`

`axlSpreadsheetDefineCell(1 2 "Red" "String" "Red background cell")`

`; Write the compiled spreadsheet to XML file on disk.`

`axlSpreadsheetWrite("spreadsheet.xml")`

`; Close and release the compiled spreadsheet's data.`

`axlSpreadsheetClose()`

`)`

### axlSpreadsheetGetCell

`axlSpreadsheetGetCell(x_rowx_col)==> g_cellData/ nil`

#### Description

Retrieves the data from the specified cell.

#### Arguments

|  |
| --- | ---
| `x_row` | Row index (1-based) of cell to look up.
| `x_col` | Column index (1-based) of cell to look up.
#### Value Returned

|  |
| --- | ---
| g\_cellData | Structure defining the contents cell
| `nil` | Cell contents are currently empty or undefined.
#### Example

The following example reads a spreadsheet into memory, then gets the contents of one cell from the first worksheet.

`axlSpreadsheetRead("example.xml")==> t`

`axlSpreadsheetSetWorksheet("First")==> t`

`g_cell = axlSpreadsheetGetCell(1 1)`

`g_cell->??==> (column 4row 1data "a" type "String"style "Default")`

`axlSpreadsheetClose()==> t`

#### See Also

[axlSpreadsheetSetCell](#1068101 "27"), [axlSpreadsheetSetCellProp](#1075986 "27"), [axlSpreadsheetDefineCell](#1065096 "27")

### axlSpreadsheetGetRGBColorString

`axlSpreadsheetGetRGBColorString(x_redx_greenx_blue) ==> t_rgb / nil`

#### Description

Given red, green, and blue color values, return an RGB string for use in spreadsheet style definitions in format required for Microsoft open spreadsheet format.

#### Arguments

|  |
| --- | ---
| `x_red` | Integer red value (0-255)
| `x_green` | Integer green value (0-255)
| `x_blue` | Integer blue value (0-255)
#### Value Returned

|  |
| --- | ---
| t\_rgb | String denoting the color value for the RGB value passed in.
| nil | Illegal values passed (outside legal range).
#### Example

The following example get the RGB string value associated with pure red.

`axlSpreadsheetGetRGBColorString(255 0 0)==> "#ff0000"`

#### See Also

[axlSpreadsheetGetRGBColorString](#1067947 "27")

### axlSpreadsheetGetRGBForNamedColor

`axlSpreadsheetGetRGBForNamedColor(t_name) ==> t_rgb / nil`

#### Description

Spreadsheets have a small set of known, pre-defined color values. To retrieve the RGB value for a specific named color, pass that color name to this function.

#### Arguments

|  |
| --- | ---
| `t_name` | Name of color to retrieve RGB value for.
#### Value Returned

|  |
| --- | ---
| `t_rgb` | String denoting RGB value for the color value passed in.
| `nil` | Color name was not found in list of standard colors.
#### Example

The following example get the RGB string value associated with the predefined color name "cyan".

`axlSpreadsheetGetRGBForNamedColor("cyan")==> "#00FFFF"`

#### See Also

[axlSpreadsheetGetRGBColorString](#1067947 "27")

### axlSpreadsheetGetStyles

`axlSpreadsheetGetStyles()==> l_styles / nil`

#### Description

Retrieves a list of all the styles defined for the active spreadsheet. If no worksheets currently exist,`nil` is returned.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `l_styles` | List of style names and IDs as pairs (ID, name)).
| `nil` | No worksheets current defined / no spreadsheet active.
#### EXAMPLES

The following example reads a spreadsheet into memory, then gets the list of defined styles for that spreadsheet.

`axlSpreadsheetRead("example.xml")==> t`

```
axlSpreadsheetGetStyles()==> (("Default" "DEFAULT") ("Title" "TITLE") ("Data" "DATA"))
```

`axlSpreadsheetClose()==> t`

#### See Also

[axlSpreadsheetSetWorksheet](#1068285 "27")

### axlSpreadsheetGetWorksheets

`axlSpreadsheetGetWorksheets()==> l_worksheets / nil`

#### Description

Retrieves a list of all the worksheets defined in the active spreadsheet. If no worksheets currently exists,`nil` is returned.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `l_worksheets` | List of worksheet names (as ordered in the spreadsheet).
| `nil` | No worksheets current defined / no spreadsheet active.
#### Example

The following example reads a spreadsheet into memory, then gets the list of defined worksheets in the file.

`axlSpreadsheetRead("example.xml")==> t`

`axlSpreadsheetGetWorksheets()==> ("First" "Second")`

`axlSpreadsheetClose()==> t`

#### See Also

[axlSpreadsheetSetWorksheet](#1068285 "27")

### axlSpreadsheetGetWorksheetSize

`axlSpreadsheetGetWorksheetSize()==> l_rowsColumns/nil`

#### Description

Return the "size" of the current worksheet, in terms of the highest row and column which have data.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `l_rowsColumns` | (maxRow, maxColumn).
| `nil` | No worksheets current defined / no spreadsheet active.
#### Example

The following example reads a spreadsheet into memory, then gets the size of the workbook named "First" before closing the file.

`axlSpreadsheetRead("example.xml")==> t`

`axlSpreadsheetSetWorksheet("First")==> t`

`axlSpreadsheetGetWorksheetSize()==> (5 5)`

`axlSpreadsheetClose()==> t`

#### See Also

[axlSpreadsheetSetWorksheet](#1068285 "27")

### axlSpreadsheetInit

`axlSpreadsheetInit() ==> t / nil`

#### Description

Initializes an empty spreadsheet document to begin filling it with worksheets, styles, and cell data. A new spreadsheet, when first initialized, does not include any of this information. It is completely empty.

If there is a spreadsheet already active in memory, it will be closed. Only one spreadsheet may be active at a time.

#### Arguments

none

#### Value Returned

|  |
| --- | ---
| `t` | Spreadsheet successfully initialized.
| `nil` | Unable to initialize empty spreadsheet. Reason printed to console.
#### Example

The following example creates a simple spreadsheet, adds information to the first cell ("Hello"), writes the spreadsheet, and closes it.

`axlSpreadsheetInit() ==> t`

`axlSpreadsheetSetWorksheet("First") ==> t`

`axlSpreadsheetDefineCell(1 1 "Default" "String" "Hello") ==> t`

`axlSpreadsheetWrite("example.xml") ==> t`

`axlSpreadsheetClose() ==> t`

#### See Also

[axlSpreadsheetClose](#1065095 "27"), [axlSpreadsheetRead](#1069134 "27"), [axlSpreadsheetWrite](#1068304 "27")

### axlSpreadsheetRead

`axlSpreadsheetRead(t_fileName)==> t / nil`

#### Description

Read a spreadsheet file on disk into memory for data access and manipulation. File is expected to be in Microsoft XML open spreadsheet format. For text-delimited files, use[axlSpreadsheetReadDelimited](#1068081 "27").

#### Arguments

|  |
| --- | ---
| `t_fileName` | Name of spreadsheet file on disk to be read.
#### Value Returned

|  |
| --- | ---
| `t` | Spreadsheet successfully read; ready for querying.
| `nil` | Unable to read spreadsheet file.
#### Example

The following example reads a spreadsheet into memory, after which it can be queried for cells' contents, and finally closed.

`axlSpreadsheetRead("example.xml")==> t`

...

`axlSpreadsheetGetCell(1 1)`

`...`

`axlSpreadsheetClose()==> t`

#### See Also

[axlSpreadsheetClose](#1065095 "27"), [axlSpreadsheetInit](#1068036 "27"), [axlSpreadsheetWrite](#1068304 "27"), [axlSpreadsheetReadDelimited](#1068081 "27")

### axlSpreadsheetReadDelimited

`axlSpreadsheetReadDelimited(t_fileName, t_delimiter) ==> t / nil`

#### Description

Read a text file on disk into memory for data access and manipulation as a spreadsheet. File is expected to be a delimited text file, with cell delimiters as specified in the`t_delimiter` argument. For XML spreadsheets, use [axlSpreadsheetRead](#1069134 "27").

#### Arguments

|  |
| --- | ---
| `t_fileName` | Name of text file on disk to be read.
| `t_delimited` | Delimiter character used to separate "cells" in text file.
#### Value Returned

|  |
| --- | ---
| `t` | File successfully read; ready for querying.
| `nil` | Unable to read spreadsheet file.
#### Example

The following example reads a csv file into memory, after which it can be queried for cells' contents, and finally closed.

`axlSpreadsheetRead("example.txt", ",")    ==> t`

`...`

`axlSpreadsheetGetCell(1 1)`

`...`

`axlSpreadsheetClose()`

`==> t`

#### See Also

[axlSpreadsheetRead](#1069134 "27")

### axlSpreadsheetSetCell

`axlSpreadsheetSetCell(x_rowx_col)==> t / nil`

#### Description

Make the active row/column of the current worksheet active.

#### Arguments

|  |
| --- | ---
| `x_row` | Row index (1-based) of cell to activate.
| `x_col` | Column index (1-based) of cell to activate.
#### Value Returned

|  |
| --- | ---
| `t` | Cell successfully activated.
| `nil` | Cell not activated. See console for reason.
#### Example

The following example sets the active cell to be cell 1,1 in the active worksheet.

`axlSpreadsheetSetCell(1 1)==> t`

`**/`

`/*INDENT ON*/`

`list axlSpreadsheetSetCell(list l_row, list l_col)`

```
{long status = SUCCESS;if(sgp_doc && sgp_worksheet){    int row = 0;    int col = 0;    row = ilGetInt(l_row);    col = ilGetInt(l_col);
```

`if(row > 0 && col > 0)`

```
{    excelCell* p_cell = excelCellFind(sgp_worksheet, row, col);    if(!p_cell)        {            p_cell = excelCellDefine(sgp_worksheet, row, col, "Default", "String", "");        }        if(p_cell)        {            sgp_cell = p_cell;        }        else        {            status = ICPEXCELMSG_SKILL_NOT_DEFINED_1;            icp_messagePrint(ICP_MESSAGE_CONSOLE, status, "cell");        }    }    else    {        status =ICPEXCELMSG_SKILL_BAD_CELLPOS_2;        icp_messagePrint(ICP_MESSAGE_CONSOLE, status, row, col);    }}else{    status = ICPEXCELMSG_SKILL_NOT_ACTIVE_1;    icp_messagePrint(ICP_MESSAGE_CONSOLE, status, "worksheet");}return(SUCCESS == status ? ilcT : ilcNil);}
```

`/*INDENT OFF*/`

`/*-`

`#ifdef DOC_C`

#### See Also

[axlSpreadsheetGetCell](#1067927 "27"), [axlSpreadsheetSetCellProp](#1075986 "27"), [axlSpreadsheetDefineCell](#1065096 "27")

### axlSpreadsheetSetCellProp

`axlSpreadsheetSetCellProp(t_propNamet_propVal)==> t / nil`

#### Description

Sets a property on the active cell in the spreadsheet.

#### Arguments

|  |
| --- | ---
| `t_propName` | Property to set. Allowable values are: STYLE, TYPE, FORMULA, or VALUE
| `t_propVal` | Value to set this property to.
#### Value Returned

|  |
| --- | ---
| `t` | Cell property successfully set.
| `nil` | Property not set (no active cell or invalid property). See console for further details.
Values supported for:

* STYLE - String value giving theID of style already defined in active spreadsheet.

* TYPE - Number, DateTime, Boolean, String, or Error.

* FORMULA - Any string representing a properly-formatted spreadsheet formula for evaluation.

> > **Note:**

> > Formulas are NOT VERIFIED by this interface for correctness.

* VALUE - Any string providing contents of the cell.

#### Example

Following example sets the contents of the active cell to the string "New Value".

`axlSpreadsheetSetCell(1 1)==> t`

`axlSpreadsheetSetCellProp("VALUE" "New Value")==> t`

#### See Also

[axlSpreadsheetSetCell](#1068101 "27"), [axlSpreadsheetGetCell](#1067927 "27"), [axlSpreadsheetDefineCell](#1065096 "27")

### axlSpreadsheetSetColumnProp

`axlSpreadsheetSetColumnProp(x_columnt_propNamet_propVal)==> t / nil`

#### Description

Sets a property for the given column of the active worksheet.

#### Arguments

|  |
| --- | ---
| `x_column` | Column index to set property for.
| `t_propName` | Property to set. Allowable values are:`AUTO_WIDTH`, `WIDTH`, and `STYLE`.
| `t_propVal` | Value to set this property to.
> > Values supported for:

|  |  |
| --- | --- | ---
|  |  | AUTO\_WIDTH - Boolean value (0 or 1).
|  |  |
| --- | --- | ---
|  |  | WIDTH - Positive integer value in font points.
|  |  |
| --- | --- | ---
|  |  | STYLE - Style ID name currently defined in active document.
These statements, along with any others, are NOT evaluated by the skill API. They will be evaluated by the spreadsheet tool which opens the document. That tool may treat either the AUTO\_WIDTH or the WIDTH tag as having priority of evaluation at its discretion, for instance. The SKILL API will NOT evaluate the AUTO\_WIDTH or other instructions.

#### Value Returned

|  |
| --- | ---
| `t` | Property set on column.
| `nil` | Property not set. Reason printed to console.
#### Example

The following example sets the AUTO\_WIDTH attributed on column 1 of the active worksheet.

`axlSpreadsheetSetRowProp(1 "AUTO_WIDTH" "1")`

#### See Also

[axlSpreadsheetSetRowProp](#1068177 "27")

### axlSpreadsheetSetDocProp

`axlSpreadsheetSetDocProp(t_propNamet_propVal)==> t / nil`

#### Description

Sets a property on the document (spreadsheet) itself.

#### Arguments

|  |
| --- | ---
| `t_propName` | Property to set. Allowable values are: AUTHOR, LAST\_AUTHOR, DATE, COMPANY, or VERSION.
| `t_propVal` | Value to set this property to.
#### Value Returned

|  |
| --- | ---
| `t` | Document property successfully set.
| `nil` | Property not set (no active spreadsheet or invalid property). See console for further details.
#### Example

The following example sets the the Author's name for this spreadsheet to be "John Doe".

`axlSpreadsheetInit()==> t`

`axlSpreadsheetSetDocProp("AUTHOR" "John")==> t`

`axlSpreadsheetSetDocProp("AUTHOR" "Doe") ==> t`

`axlSpreadsheetWrite("example.xml")==> t`

`axlSpreadsheetClose()==> t`

### axlSpreadsheetSetRowProp

`axlSpreadsheetSetRowProp(x_rowt_propNamet_propVal)==> t / nil`

#### Description

Sets a property for the given row of the active worksheet.

#### Arguments

|  |
| --- | ---
| `x_row` | Row index to set property for.
| `t_propName` | Property to set. Allowable properties are, AUTO\_HEIGHT, HEIGHT, and STYLE.  Values supported for these properties are:  AUTO\_HEIGHT -- Boolean value (0 or 1)  HEIGHT -- Positive integer value in font points  STYLE -- Style ID name currently defined in active document
|
|
|
|
| `t_propVal` | Value to set this property to.  AUTO\_HEIGHT -- Boolean value (0 or 1)  HEIGHT -- Positive integer value in font points  STYLE -- Style ID name currently defined in active document
These statements, along with any others, are NOT evaluated by the skill API. They will be evaluated by the spreadsheet tool which opens the document. That tool may treat either the AUTO\_HEIGHT or the HEIGHT tag as having priority of evaluation at its discretion, for instance. The skill API will NOT evaluate the AUTO\_HEIGHT or other instructions.

#### Value Returned

|  |
| --- | ---
| `t` | Property set on row.
| `nil` | Property not set. Reason printed to console.
#### Example

The following example set the auto fit attributed on row 1 of the active worksheet.

`axlSpreadsheetSetRowProp(1 "AUTO_HEIGHT" "1")`

#### See Also

[axlSpreadsheetSetColumnProp](#1068141 "27")

### axlSpreadsheetSetStyle

`axlSpreadsheetSetStyle(t_idt_name)==> t / nil`

#### Description

Defines or activates the specified style in the active spreadsheet. Styles may be referenced in any worksheet of the spreadsheet. You do not need to redefine the style for each new worksheet you create.

#### Arguments

|  |
| --- | ---
| `t_id` | The spreadsheet ID for this style.
| `t_name` | The user "name" for this style / nil. This is the name that is displayed for this style in the Excel style editor and selection pull-down.
#### Value Returned

|  |
| --- | ---
| `t` | Style successfully activated / defined.
| `nil` | Style not activated. Reason written to console.
#### Example

The following example activates the Default style in the active spreadsheet and sets its vertical alignment style to Top-justified.

`axlSpreadsheetSetStyle("Default" nil)==> t`

`axlSpreadsheetSetStyleProp("Alignment" "Vertical" "Top")==> t`

#### See Also

[axlSpreadsheetSetCell](#1068101 "27"), [axlSpreadsheetSetWorksheet](#1068285 "27")

### axlSpreadsheetSetStyleBorder

`axlSpreadsheetSetStyleBorder(t_positiont_colort_lineStylet_weight)==> t / nil`

#### Description

Sets the cell border properties for a active style definition.

#### Arguments

|  |
| --- | ---
| `t_position` | Position must be one of the accepted Microsoft positions (Left, Right, Top, Bottom, etc).
| `t_color` | Microsoft color name or RGB value (e.g. "BLACK" or #FF00AA).
| `t_lineStyle` | Line style to use (normally "Continuous" for a solid line).
| `t_weight` | The thickness of the line, in font points. Must be a positive integer.
Following table lists the values supported for different arguments.

|  |
| --- | ---
| **Argument** | **Supported Values**
| POSITION | Left, Top, Right, Bottom, DiagonalLeft, or DiagonalRight
| COLOR | RGB Value in format "#RRGGBB" or color name from pre-defined names table
| LINE\_STYLE | None, Continuous, Dash, Dot, DashDot, DashDotDot, SlashDashDot, or Double
| WEIGHT | Positive integer value in font points
#### Value Returned

|  |
| --- | ---
| `t` | Border style successfully set.
| `nil` | Border style not set (no active style or invalid parameters). See console for further details.
#### Example

The following example defines a new style, "Second", which inherits its settings from the "Default" style, but with a thin border defined.

`axlSpreadsheetSetStyle("Second" "Second Style")==> t`

`axlSpreadsheetSetStyleParent("Default")==> t`

`axlSpreadsheetSetStyleBorder("Left" nil "Continuous" "2")==> t`

`axlSpreadsheetSetStyleBorder("Right" nil "Continuous" "2")==> t`

`axlSpreadsheetSetStyleBorder("Top" nil "Continuous" "2")==> t`

`axlSpreadsheetSetStyleBorder("Bottom" nil "Continuous" "2")==> t`

#### See Also

[axlSpreadsheetSetStyle](#1068196 "27"), [axlSpreadsheetSetStyleProp](#1068263 "27"), [axlSpreadsheetSetStyleParent](#1070391 "27"), [axlSpreadsheetGetRGBColorString](#1067947 "27")

### axlSpreadsheetSetStyleParent

`axlSpreadsheetSetStyleParent(t_parent)==> t / nil`

#### Description

Sets the active style's parent. Style will inherit default properties from its parent style, therefore only changes need to be specified in the child style. Parent must already be defined for spreadsheet.

#### Arguments

|  |
| --- | ---
| `t_parent` | Style ID of parent to link to. Note that the parent must already be defined before it can be referenced by children.
#### Value Returned

|  |
| --- | ---
| `t` | Style parent successfully set.
| `nil` | Parent not set (no active style or parent style doesn't exist). See console for further details.
**Note:** PARENT value must be a style ID defined in the active spreadsheet document.

#### Example

The following example defines a new style, "Second", which inherits its settings from the "Default" style, but with text centered in the cell.

`axlSpreadsheetSetStyle("Second" "Second Style")==> t`

`axlSpreadsheetSetStyleParent("Default")==> t`

`axlSpreadsheetSetStyleProp("Alignment" "Horizontal" "Center")==> t`

#### See Also

[axlSpreadsheetSetStyle](#1068196 "27"), [axlSpreadsheetSetStyleBorder](#1070205 "27"), [axlSpreadsheetSetStyleProp](#1068263 "27")

### axlSpreadsheetSetStyleProp

`axlSpreadsheetSetStyleProp(t_typet_propNamet_propVal) ==> t / nil`

#### Description

Sets a specific style property in the active style definition.

#### Arguments

|  |
| --- | ---
| `t_type` | Type of property being set. Must be one of: ALIGNMENT, FONT, FILL, NUMBER\_FORMAT, PROTECTION.
| `t_propName` | Name of the property being set (varies by type).
| `t_propVal` | Value to set the property to.
#### Value Returned

|  |
| --- | ---
| `t` | Style attribute successfully set.
| `nil` | Attribute not set (no active style or invalid parameters). See console for further details.
ALIGNMENT properties and values supported are listed in the following table.

|  |
| --- | ---
| ****Property**** | **Values Supported...**
| Horizontal | Automatic, Left, Center, Right, Fill, Justify, CenterAcrossSelection, JustifyDistributed, or Distributed.
| Indent | Positive integer value in characters widths to indent.
| ReadingOrder | RightToLeft, LeftToRight, or Context
| Rotate | Rotation angle in degrees
| ShrinkToFit | Boolean value (0 or 1).
| Vertical | Automatic, Top, Bottom, Center, Justify, JustifyDistributed, or Distributed
| VerticalText | Boolean value (0 or 1).
| WrapText | Boolean value (0 or 1).
****Table 27-1****
**FONT properties and values supported**

| **Property** | **Values Supported...**
| Bold | Boolean value (0 or 1).
| CharSet | Integer value
| Color | RGB Value in format "#RRGGBB" or color name from pre-defined names table
| Family | Automatic, Decorative, Modern, Roman, Swiss, or Script.
| Italic | Boolean value (0 or 1).
| Outline | Boolean value (0 or 1).
| Shadow | Boolean value (0 or 1).
| Size | Positive integer value in font size points..
| StrikeThrough | Boolean value (0 or 1).
| Underline | None, Single, Double, SingleAccounting, or DoubleAccounting.
| VerticalAlign | None, Subscript, or SuperScript
****Table 27-2****
**FILL properties and values supported**

| **Property** | **Values Supported...**
| Color | RGB Value in format "#RRGGBB" or color name from pre-defined names table
| Pattern | None, Solid, Gray75, Gray50, Gray25, Gray125, Gray0625, HorzStripe, VertStripe, ReverseDiagStripe, DiagStripe, DiagCross, ThickDiagCross, ThinHorzStripe, ThinVertStripe, ThinReverseDiagStripe, ThinDiagStripe, ThinHorzCross, or ThinDiagCross.
| PatternColor | RGB Value in format "#RRGGBB" or color name from pre-defined names table
****Table 27-3****
**NUMBER\_FORMAT properties and values supported**

| **Property** | **Values Supported...**
| Format | String defining format of number in cell
****Table 27-4****
**PROTECTION properties and values supported**

| **Property** | **Values Supported...**
| Protected | Boolean value (0 or 1).
| HideFormula | Boolean value (0 or 1).
#### Examples

The following example defines a new style, "Second", which inherits its settings from the "Default" style, but with text centered in the cell.

`axlSpreadsheetSetStyle("Second" "Second Style")==> t`

`axlSpreadsheetSetStyleParent("Default")==> t`

`axlSpreadsheetSetStyleProp("Alignment" "Horizontal" "Center")==> t`

#### See Also

[axlSpreadsheetSetStyle](#1068196 "27"), [axlSpreadsheetSetStyleBorder](#1070205 "27"), [axlSpreadsheetSetStyleParent](#1070391 "27"), [axlSpreadsheetGetRGBColorString](#1067947 "27")

### axlSpreadsheetSetWorksheet

`axlSpreadsheetSetWorksheet(t_name)==> t / nil`

#### Description

Makes the specified worksheet the active one for future cell references. If the worksheet does not exist, it is created as the new last worksheet in the document.

#### Arguments

|  |
| --- | ---
| `t_name` | The name of the worksheet to activate.
#### Value Returned

|  |
| --- | ---
| `t` | Worksheet successfully activated / defined.
| `nil` | Worksheet not activated. Reason written to console.
#### Examples

The following example activates the worksheet named "First" in the active spreadsheet, then sets the first column to have a width of 500.

> `axlSpreadsheetSetWorksheet("First")    ==> t`

> `axlSpreadsheetSetColumnProp(1 "Width" "500")    ==> t`

#### See Also

[axlSpreadsheetSetCell](#1068101 "27"), [axlSpreadsheetSetStyle](#1068196 "27")

### axlSpreadsheetWrite

`axlSpreadsheetWrite(t_fileName)==> t / nil`

#### Description

Write the spreadsheet in memory to file on disk. File will be written compliant with Microsoft's open spreadsheet XML format.

#### Arguments

|  |
| --- | ---
| `t_fileName` | Name of file to be written to, including path if not to be written to current working directory.
#### Value Returned

|  |
| --- | ---
| `t` | File successfully written.
#### Examples

* The following example creates a simple spreadsheet, adds information to the first cell ("Hello"), writes the spreadsheet, and closes it.

`axlSpreadsheetInit()`

`==> t`

`axlSpreadsheetSetWorksheet("First")`

`==> t`

`axlSpreadsheetDefineCell(1 1 "Default" "String" "Hello")`

`==> t`

`axlSpreadsheetWrite("example.xml")`

`==> t`

`axlSpreadsheetClose()`

`==> t`

#### See Also

[axlSpreadsheetClose](#1065095 "27"), [axlSpreadsheetInit](#1068036 "27"), [axlSpreadsheetRead](#1069134 "27")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
