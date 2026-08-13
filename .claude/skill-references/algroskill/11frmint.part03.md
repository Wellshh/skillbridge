<!--
source: algroskill/11frmint.md
part: 3/3
estimated_tokens: 11428
-->

|  |
| --- | ---
| `'background` | Set background of control
| `'text` | Set text of control
The`g_color` argument is either a color symbol (for non DB options), a number for DB color options, or `nil` (for restoring to system default). See [Accessing Allegro PCB Editor Colors with AXL-SKILL](01ovrvew.html#105118 "1") for the allowed values.

Other form controls support color as a fundamental part of their interface. These are`COLOR` (See [Accessing Allegro PCB Editor Colors with AXL-SKILL](01ovrvew.html#105118 "1")) and `GRID` (See [Using Grids](#461722 "11")) controls.

* Please note the following restrictions:

* Setting the same or close text and background colors can cause readability issues.

* Setting the background of`CHECKLIST` controls is not supported on UNIX.

* Dialog boxes with popups do not correctly show color.

* ***If setting the background of a ENUM field on Windows, you must set the OPTION color in the form file as in the following example.`FIELD enum_controlFLOC 16 12ENUMSET 41OPTIONS colorPOP "enum_popup"ENDFIELD`
  This is the same option as the '`ownerdrawn`'. The color option is ignored on UNIX which does not support themes. For theming purposes, Microsoft takes the background color so setting this option disables Microsoft themes for this control.***

#### Arguments

|  |
| --- | ---
| `o_form` | Form handle*.*
| `t_field` | Field name.
| `g_option` | Option (see above)
| `g_color` | Color (see`axlColorDoc`) or `nil`
#### Value Returned

|  |
| --- | ---
| `t` | Color changed.
| `nil` | Error due to an incorrect argument.
#### Example 1

You can find an example in`axlform.il`.

> `axlFormColorize(f1s "string" 'text 'red)`

Sets text of string control to red.

#### Example 2

> `axlFormColorize(f1s "string" 'background 'green)`

Sets background of string control to green.

#### Example 3

> `axlFormColorize(f1s "string" 'text nil)`

> `axlFormColorize(f1s "string" 'background nil)`

Sets control back to default.

#### Example 4

> `axlFormColorize(f1s "string" 'background 1)`

Sets control background to Allegro PCB Editor database color 1

### axlFormGetActiveField

`axlFormGetActiveField(r_form)⇒ t/nil`

#### Description

Gets the form's active field.

#### Arguments

|  |
| --- | ---
| `r_form` | Form's`dbid`.
| `t_field` | Form field name (string).
#### Value Returned

|  |
| --- | ---
| `t_field` | Active field name.
| `nil` | No active field.
### axlFormGridBatch

`axlFormGridBatch(r_cell`

`)`

`⇒ t/nil`

#### Description

Always used with`axlFormGridSetBatch`. Sets many grid cells efficiently.

#### Arguments

|  |
| --- | ---
| `r_cell` | Obtained from`axlFormGridNewCell`.
#### Value Returned

|  |
| --- | ---
| `t` | Grid cells set.
| `nil` | No grid cells set.
### axlFormGridCancelPopup

`axlFormGridCancelPopup(r_formt_field)⇒ t/nil`

#### Description

After any change to grid content, the application must tell the grid that the changes are complete. The grid then updates itself to the user. Changes include: adding or deleting columns and changing cells.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name.
#### Value Returned

|  |
| --- | ---
| `t` | Success.
| `nil` | Failure due to incorrect arguments.
### axlFormGridDeleteRows

`axlFormGridDeleteRows(r_formt_fieldx_rowx_number)⇒ t/nil`

#### Description

Deletes`x_number` rows at `x_row` number. `x_row``=`,`n`>, `x_number``=-1` deletes the entire grid. `x_row``=-1`, `x_number``-1` may be used to delete the last row in the grid.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name.
| `x_row` | Row number to start delete.
| `x_number` | Number of rows to delete.
#### Value Returned

|  |
| --- | ---
| `t` | Rows deleted.
| `nil` | No rows deleted.
### axlFormGridEvents

`axlFormGridEvents(r_formt_fields_event/(s_event1 s_event2 ...))⇒ t/nil`

#### Description

Sets user events of interest. It is critical for your application to only set the events that you actually process since enabled events are scripted.

Grid events include the following:

|  |
| --- | ---
| `'rowselect` | Puts grid into row select mode. This is mutually exclusive with`cellselect`.
| `'mrowselect` | Puts grid into multi-row select mode. This is mutually exclusive with`cellselect`. Use [axlFormGridSelected](#495999 "11") to determine what rows are selected.
| `'cellselect` | Puts grid into cell select mode. This is mutually exclusive with`rowselect` and `mrowselect`.
| `'change` | Enables cell change events. Use this option if you have check box and text box type cells.
| `'rightpopup` | Enables right mouse button popup. A popup must have been specified in the form file.
| '`rightpopupPre` | Enables callback to application before a right mouse popup is displayed. This allows the user to modify the popup shown. Also requires`'rightpopup` be set.
| `'leftpopupPre` | Enables callback to application before a left mouse popup is displayed. This allows the user to modify the popup shown. Left mouse popups are only present in the drop down cell type.
By default, the grid body has`rowselect` enabled while the headers have nothing enabled.

The form callback structure (`r_form`) has the following new attributes that are only applicable for grid field types:

|  |  |  |
| --- | --- | --- | ---
| **Event** | **Row** | **Col** | **<Data Fields>**
| `rowselect` | <`row`> | 1 | No
| `cellselect` | <`row`> | <`col`> | Yes (1)
| change | <`row`> | <`col`> | Yes (1)
| `rightpopup` | <`row`> | <`col`> | Yes
| `rightpopupPre` | <`row`> | <`col`> | No (2) (3)
| `leftpopupPre` | <`row`> | <`col`> | No (2) (3)
where:

|  |
| --- | ---
| <`row`> | Row number (1 based)
| <`col`> | Column number (1 based)
| <`Data fields`> | Setting of the`r_form` attributes `curValue`, `curValueInt` and `isValueString`.
* Communicates the value of the data*before* the field is changed. The change event sends the value *after* the field is changed.

* Events are sent immediately before a popup is displayed so the application has the opportunity to modify it. See[axlFormGridEvents](#459032 "11") to set this and other event options.

* If using events`rightpopupPre` or `leftpopupPre`, the popup may be cancelled by calling `axlFormGridCancelPopup` when you receive one of these events.

See[Using Grids](#461722 "11") for a grid overview.

**Note:** Assigning events to a grid overrides the previous assignment. Therefore, Following do not work:

> `axlFormGridEvents(fw "grid 'change)axlFormGridEvents(fw "grid 'cellselect)`

> Instead, use the following command.

> `axlFormGridEvents(fw "grid '(cellselect change) )`

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name.
| `s_events` | See above.
#### Value Returned

|  |
| --- | ---
| `t` | User event set.
| `nil` | No user event set.
#### See Also

[axlFormGridNewCell](#459451 "11")

### axlFormGridGetCell

`axlFormGridGetCell(r_formt_fieldr_cell`

`)`

`⇒ r_cell/nil`

#### Description

Returns grid cell data for a given row and column. All associated data for the cell is returned.

**Note:** The cell value is always returned as a string except for REAL and LONG data types which are returned in their native format.

If row or cell number of 0 is used then top or side heading data is returned (if present.)

**Note:** For best performance, reuse the cell if accessing multiple cells.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name.
| `r_cell` | Grid cell from`axlFormGridNewCell()`.
#### Value Returned

|  |
| --- | ---
| `r_cell` | Cell data.
| `nil` | Invalid form id, field label or cell doesn't exist in the grid.
#### Example

> `cell = axlFormGridNewCell()`

> `cell->row = 3`

> `cell->col = 1`

> `axlFormGridInsertRows(form, "grid" cell)`

> `printf("cell value = %L\n", cell)`

Returns the value of cell - (1,3).

### axlFormGridInsertCol

`axlFormGridInsertCol(r_formt_fieldr_formGridCol)⇒ t/nil`

#### Description

Adds a column with the indicated options (`g_options`) to a grid field. The `g_options` parameter is based on the type `formGridCol`. The`formGridCol` structure has default behavior for all settings.

**Note:** For more information on using this function, see[Using Grids](#461722 "11") for an overview.

[Table 11-6](#465514 "11") describes the `FormGridCol` attributes.

****Table 11-6****
**FormGridCol Attributes**

| **Attribute** | **Type** | **Default** | **Description**
| fieldType | symbol | TEXT | Field types include: TEXT, STRING, LONG, REAL, ENUMSET, and CHECKITEM.
| fieldLength | integer | 16 | Maximum data length.
| colWidth | integer | 0 | Width of column.
| headText | n/a | n/a | If the grid has a top heading, sets the heading text. Can also set using`axlFormGridSet`.
|  |  |  |
| Alignment Types (left, right, and center): | | |
| align | symbol | Left | Column alignment.
| topAlign | symbol | Center | Column header alignment.
| scriptLabel | string | <`row number`> | Column scripting name. If the column entry can be edited, you can provide a name which is recorded to the script file. For fieldTypes of TEXT, this option is ignored. Case is ignored and text should not have white space or the symbol '`!`'.
| popup | string | n/a | Name of the associated popup. May be applied to columns or cells of types ENUMSET, STRING, LONG, or REAL.
| **Note:** Accuracy support is only applicable for LONG and REAL column types. If used, you must set both min and max values. | | |
| decimals | integer | n/a | Number of decimal places.
| max | integer or float | n/a | Maximum value.
| min | integer or float | n/a | Minimum value.
**Note:** You can add columns to a grid field only at creation time. Once rows have been added to a grid, no new columns may be added. This is true, even if you delete all rows in the grid.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name.
| `r_formGridCol` | Instance of type`formGridCol`.
#### Value Returned

|  |
| --- | ---
| `t` | Column added.
| `nil` | Failure due to a nonexistent form or field, field not of type`GRID`, errors in the `g_options` defstruct, or grid already had a row added.
#### Examples

For a complete grid programming example, see:`<``cdsroot``>/share/pcb/examples/skill/form/grid`.

#### Example 1

> `options = make_formGridCol`

> `options->fieldType = 'TEXT`

> `options->align = 'center`

> `axlFormGridInsertCol(r_form "grid" options)`

Adds the first column of type`TEXT` (non-editable) with center alignment.

#### Example 2

> `options->fieldType = 'ENUMSET`

> `options->popup = "grid2nd"`

> `options->colWidth = 10`

> `options->scriptLabel = "class"`

> `axlFormGridInsertCol (r_form "grid" options)`

Adds the second column of type`ENUM` (non-editable) with column width of 10 and center alignment, assuming that the form file has a popup definition of `grid2nd`.

### axlIsGridCellType

`axlIsGridCellType(r_cell)⇒ t/nil`

#### Description

Tests the passed symbol to see if its user type is of the form`"grid cell".`

#### Arguments

|  |
| --- | ---
| `r_cell` | Symbol
#### Value Returned

|  |
| --- | ---
| `t` | Symbol is of the type form grid cell.
| `nil` | Symbol is not of the type form grid cell.
### axlFormGridInsertRows

`axlFormGridInsertRows(r_formt_fieldx_rowx_number)⇒ t/nil`

#### Description

Inserts`x_number`rows at `x_row` number location. Rows are inserted empty. A -1 may be used as `x_row` to add to end of the grid. Since grids are 1 based, a 1 inserts at the top of the grid.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name.
| `x_row` | Row number of insertion point.
| `x_number` | Quantity of rows to add.
#### Value Returned

|  |
| --- | ---
| `t` | One or more rows inserted.
| `nil` | No rows inserted.
### axlFormGridNewCell

`axlFormGridNewCell()⇒ r_cell`

#### Description

Creates a new instance of`r_cell` which is required as input to [axlFormGridBatch](#458963 "11") or [axlFormSetField](#425442 "11") for form grid controls. As a convenience, the consuming APIs do not modify the cell attributes. You need not reset all attributes between API calls.

See axlFormGridDoc for grid overview.

See[axlFormGridSetBatch](#459633 "11") for a complete description of cell attributes.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `r_cell` | New list gridcell handle.
#### See Also

[axlIsGridCellType](#467799 "11"), [axlFormGridInsertRows](#459407 "11"), [axlFormGridDeleteRows](#459010 "11"), [axlFormGridCancelPopup](#458986 "11"), [axlFormGridEvents](#459032 "11"), [axlFormGridOptions](#460054 "11"), [axlFormGridSetBatch](#459633 "11"), [axlFormGridBatch](#458963 "11"), [axlFormGridGetCell](#459256 "11"), [axlFormGridReset](#459504 "11"), [axlFormGridSelected](#495999 "11"), [axlFormGridSelectedCnt](#495786 "11"), [axlFormGridSetSelectRows](#495777 "11")

### axlFormGridReset

`axlFormGridReset(r_formt_field)⇒ t/nil`

#### Description

Resets grid to its unloaded state. Application should then set the columns, then rows, to the same state as when they initially loaded the windows.

Changes the number of columns after the grid has already been initialized.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name.
#### Value Returned

|  |
| --- | ---
| `t` | Grid reset.
| `nil` | Grid not reset.
#### Example

For a programming example, see`fgrid.il` in `<``cdsroot``>/share/pcb/examples/skill/`

Pseudo code:

> `axlFormGridReset(fg "grid")`

> `initCols()`

> `initRows()`

> `axlFormGridUpdate(fg "grid")`

### axlFormGridSetBatch

`axlFormGridSetBatch(r_formt_fields_callbackg_pvtData)⇒ t/nil`

#### Description

Changes grid cells much faster than`axlFormSetField` when changing multiple cells. Both APIs require a grid cell data type (`axlFormGridNewCell`.)

Grid performs single callback using`s_callback` to populate the grid. You must call `axlFormGridBatch` in the callback in order to update grid cells.

See the programming example,`fgrid.il`at `<``cdsroot``>/share/pcb/examples/skill/form/grid`. Create rows and columns before calling this batch API.

Within the callback, use only`axlFormNewCell` and `axlFormGridBatch` from the `axlForm` API.

After changing cells, update the display using`axlFormGridUpdate` outside of the callback.

**Grid Cell Data Type (r\_cell) Attributes**

|  |
| --- | ---
| `x_row` | Row to update.
| `x_col` | Column to update.
| `g_value` | Value (may be string, integer, or float) if`nil`, preserve current grid setting for the cell.
| `s_backColor` | Optional background color.
| `s_textColor` | Optional text color.
| `s_check` | Set or clear check mark for`CHECKITEM` cells. Ignored for non-check cells. Value may be `t` or `nil`.
| `s_noEdit` | If cell is editable, disables edit. Ignored for`TEXT` columns since they are not editable. Current settings are preserved.
| `s_invisible` | Make cell invisible. Current cell settings are preserved by the grid.
| `s_popup` | Use popup name in the form file to set this, or "" to unset. If enum, string, long, or real cell, then overrides column popup, else restores back to popup of the column. Ignored for all other cell types.
| `t_objType` | Object name`"r_cell"` (read-only)
**Note:** Previous grid cell settings are overridden by values in`s_noEdit` and `s_invisible`.

Column and Row access:

Rows and columns are 1 based. To set the cell in the first column and row, you set the row and col number to 1.

You can control header and script text with reserved row and column values as follows:

|  |
| --- | ---
| (<`row`>, 0) | Set side header display text.
| (<`row`>, -1) | Set side header scripting text.
**Note:** Case is ignored, and text must not contain spaces or the '`!`'

|  |
| --- | ---
| (0, <`col`>) | Set top header display text. You may also set the top header at column creation time using`axlFormGridInsertCol`.
| (0, 0) | Setting not supported.
For headers and script text,`g_value` is the only valid attribute other than `row` and `col`.

Colors available for`s_backColor` and `s_textColor`:

* nil - use system defaults for color, typically white for background and black for text

* black

* white

* red

* green

* yellow

* button - use the current button background color

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name.
| `t_callback` | Function to callback. Takes a single argument:`g_pvtData`
| `g_pvtData` | Private data (Pass`nil` if not applicable.)
#### Value Returned

|  |
| --- | ---
| `t` | Grid cell changed.
| `nil` | No grid cell changed, or application callback returned`nil`.
### axlFormGridUpdate

`axlFormGridUpdate(`

`r_form`

`t_field`

`) -> t/nil`

#### Description

Unlike the form lists control you must manually notify the grid control that it must update itself. You should use this call in the following situations:

* Inserting a row or rows

* Deleting a row or rows

* Changing cell(s)

You should make the call at the end of all of changes to the grid.

* ***Do not make this call inside the function you use with axlFormGridSetBatch. Make it after axlFormGridSetBatch returns.***

#### Arguments

`r_form` Standard form handle.

`t_field` Standard field name.

#### Value Returned

Returns`t`for success, `nil` for failure.

#### See Also

[axlFormGridNewCell](#459451 "11")

### axlFormInvalidateField

`axlFormInvalidateField(r_formt_field)⇒ t/nil`

#### Description

Invalidates the form's field. Allows Windows to send a redraw message to the field's redraw procedure.

Use only for thumbnail fields.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name.
#### Value Returned

|  |
| --- | ---
| `t` | Field invalidated.
| `nil` | No field invalidated.
### axlFormIsFieldEditable

`axlFormIsFieldEditable(r_formt_field)⇒ t/nil`

#### Description

Checks whether the given form field is editable. If the field is editable,`t` is returned. If the field is greyed, then `nil` is returned.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
#### Value Returned

|  |
| --- | ---
| `t` | Field is editable.
| `nil` | Field is greyed, or not editable.
### axlFormListAddItem

`axlFormListAddItem(r_formt_fieldt_listItem/lt_listItems/nilg_index)⇒ t/nil`

#### Description

Adds an item to a list at position`x`. To add many items efficiently, pass the items as a list.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `t_listItem` | String of items in the list. If adding to list for the first time, you must send a`nil` to display the list.
| `lt_listItems` | List of strings to add.
| `g_index` | 0 = First item in the list. -1 = Last item in the list.
#### Value Returned

|  |
| --- | ---
| `t` | One or more items added to list.
| `nil` | No items added to list due to incorrect arguments.
#### Example 1

> `axlFormListAddItem(f1, "list" "a" -1)`

> `axlFormListAddItem(f1, "list" "b" -1)`

> `axlFormListAddItem(f1, "list" "c" -1)`

> `; since first time, send a nil to display the list`

> `axlFormListAddItem(f1, "list" nil, -1)`

Adds three items to the end of a list.

#### Example 2

> `axlFormListAddItem(f1, "list" '("a" "b" "c"), -1)`

Adds three items to the end of a list (alternate method).

### axlFormListDeleteItem

```
axlFormListDeleteItem(r_formt_fieldt_listItem/x_index/lt_listItem/nil)⇒ t/x_index/nil
```

#### Description

Deletes indicated item in the list. You can delete by a string or by position. Deleting by string works best if all items are unique. Position can be problematic if you have the list sort the items that you add to it.

To quickly delete multiple items, call this interface with a list of items.

**Note:** Delete by list only supports a list of*strings*.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `x_index` | Position of the item to be deleted. 0 is the first item in the list, -1 is the last item in the list.
| `t_listItem` | String of item to delete.
| `lt_listItems` | List of items to delete.
| `nil` | Deletes the last item.
#### Value Returned

|  |
| --- | ---
| `x_index` | If using strings (`t_listItem`) to delete items, returns the index of strings deleted. Useful for allowing the code to automatically select the next item in the list.
| `t` | If deleting by index (`x_index`), it returns `t` if successful in deleting the item.
| `nil` | Failed to delete the item.
### axlFormListGetItem

`axlFormListGetItem(r_formt_fieldx_index)⇒ t_listItem/nil`

#### Description

Returns the item in the list at index (`x_index`.) Lists start at index 0. If -1 is passed as an index, returns the last item in the list.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `x_index` | Offset into the list. 0 = First item in the list. -1 =Last item in the list.
#### Value Returned

|  |
| --- | ---
| `t_listItem` | String of item in the list.
| `nil` | Index not valid, or no item at that index.
### axlFormListGetSelCount

`axlFormListGetSelCount(`

`r_form`

`t_field`

`)==> x_count/nil`

#### Description

This only applies to a multi-select list box (OPTIONS multiselect in form file).
Returns a count of number of items selected in a multi-select list box.

#### Arguments

`r_form` Form control.

`t_field` Name of the field.

#### Values Returned

`nil` If not a multi-list box.

`x_count` Number of items selected.

#### See Also

[axlFormListGetSelItems](#468467 "11")

#### Example

See`axlform.il` example.

### axlFormListGetSelItems

`axlFormListGetSelItems(r_formt_field)==> lt_selected/nil`

#### Description

This only applies to a multi-select list box (OPTIONS multiselect in form file).

For a multi-select list box returns list of strings for items selected. If no items selected or this is not appropriate for control returns`nil`.

#### Arguments

`r_form` Form control.

`t_field` Name of the field.

#### Value Returned

`lt_selected` List of strings for items selected.

`nil` Error or nothing selected.

#### See Also

[axlFormListGetSelCount](#468183 "11"), [axlFormListSelAll](#468774 "11")

#### Example

See`axlform.il` example.

### axlFormListOptions

`axlFormListOptions(r_formt_fields_option/(s_option1 s_option2 ...))⇒ t/nil`

#### Description

Sets options for a list control. The following options are supported:

|  |
| --- | ---
| '`doubleClick` | Enable double-click selection. Passing a`nil` for an option sets default list behavior. Default is single click.
Double-click events are handled as follows:

* Receive the first click as an event with the item selected and the result is:`doubleClick = nil`.

* Receive the second click as an event with the item selected and the result is:`doubleClick = t`.

Suggested use model:

On first click do what would normally happen if the user clicks only once. The second click is a natural extension. For example, on a browser the first click selects the file. The second click does what the*OK* button would do: send the file to the application and close the form.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `s_option` | Sets option for list control.`nil` resets to default.
#### Value Returned

|  |
| --- | ---
| `t` | Options set.
| `nil` | No options set due to incorrect arguments.
#### Example 1

> `axlFormListOptions(form "list" 'doubleClick)`

Enables double-click for a list.

#### Example 2

> `axlFormListOptions(form "list" nil)`

Disables double-click for a list.

### axlFormListSelAll

`axlFormListSelAll(r_formt_fieldg_set)==> t/nil`

#### Description

This only applies to a multi-select list box (OPTIONS multiselect in form file).

This either selects or deselects all items in list box.

#### Arguments

`r_form` Form control.

`t_field` Name of the field.

`g_set` `t` to select all; `nil` to deselect all.

#### Value Returned

`t` if successful, `nil` field is not a mutli-select list box

#### See Also

[axlFormListGetSelItems](#468467 "11")

#### Examples

Select all items in multi-list control;`mlistfield`.

`axlFormListSelAll(fw "mlistfield" t)`

De-Select all items in multi-list control;`mlistfield`.

`axlFormListSelAll(fw "mlistfield" nil)`

### axlFormMsg

`axlFormMsg(r_formt_messageLabel[g_arg1 ...])⇒ t_msg/nil`

#### Description

Retrieves and prints a message defined in the form file by message label (`t_messageLabel`.) Form file allows definitions of messages using the "`MESSAGE`" keyword (see [Using Forms Specification Language](#480398 "11").) Use this to give a user access to message text, but no access to your SKILL code.

Messages are only printed in the status area of the form owning the message (`r_form`.) You cannot access message ids from one form file and print to another. The main window is used for forms with no status lines.

You use standard formatting and argument substitution (see`printf`) for the message.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_messageLabel` | Message label defined in form file by the MESSAGE keyword.
| `g_arg1` ... | Substitution parameters (see`printf`)
#### Value Returned

|  |
| --- | ---
| `t_msg` | Message that prints.
| `nil` | No message with the given name found in this form file.
#### Examples

> ```
> Form file (level: 0 is info, 1 is info with no journal entry, 2 is warning, 3 is error, and 4 is fatal.);
> ```

> `MESSAGE drccount 0 "Drc Count of %d for %s"`

> `MESSAGE drcerrors 2 "Drc Errors"`

> `axlFormMsg(fw "drccount" 10 "spacing")`

> `axlFormMsg(fw "drcerrors")`

### axlFormGetFieldType

`axlFormGetFieldType(r_formt_field)⇒ g_fieldType/nil`

#### Description

Returns the control type for a form field. See the keywords in[Callback Procedure: formCallback](#428663 "11") for a list of supported field types.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_field` | Field name.
#### Value Returned

|  |
| --- | ---
| `g_fieldType` | One of the control types.
| `nil` | Field does not exist or is not one of the types supported.
### axlFormDefaultButton

`axlFormDefaultButton(r_formt_field/g_mode)⇒ t/nil`

#### Description

Forms normally automatically set a*default* *button* in a form with the `DEFAULT` section in the form file or with the *OK* and *DONE* labels. When the user hits a carriage return, the *default* *button* is executed.

A form can have, at most, one default button. Only a field of type`BUTTON` can have the default button attribute.

**Note:** If default buttons are disabled in a form, then attempts to establish a new default button are ignored. You can only change the default button if the capability in the form is enabled.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_field` | Field name to establish as new button default.
| `g_mode` | `t` to enable the default button in the form, `nil` to disable it.
#### Value Returned

|  |
| --- | ---
| `t` | Default button set.
| `nil` | Field does not exist.
#### Example 1

> `axlFormDefaultButton(form nil)`

Sets no default button in form.

#### Example 2

> `axlFormDefaultButton(form "cancel")`

Sets the default button to be`Cancel` instead of the default `OK`.

### axlFormGridOptions

`axlFormGridOptions(r_formt_fields_name[g_value])⇒ t/nil`

#### Description

Miscellaneous grid options. See[Using Grids](#461722 "11") for a grid overview.

#### Arguments

|  |
| --- | ---
| `r_form` | Form handle.
| `t_field` | Field name.
| `s_name`/`g_value` | Supported options shown.
#### s\_name/g\_value Supported Options

|  |
| --- | ---
| [`'goto``x_row``]` | Puts the indicated row on display, scrolling the grid if necessary.
**Note:** -1 signifies the last row.

|  |
| --- | ---
| [`'goto``x_row``:``x_col`] | Sends grid to indicated row and column.
**Note:** -1 signifies the last row or column.

|  |
| --- | ---
| [`'select``x_row`] | Selects (highlights) indicated row.
| [`'select``x_row``:``x_col``]` | Selects (highlights) indicated cell. Grid must be in cell select mode else row is selected instead of cell. See`axlFormGridEvents` for more information.
| ['`deselectAll`] | Deselect any selected grid cells or rows.
#### Value Returned

|  |
| --- | ---
| `t` | Selected grid option performed.
| `nil` | Selected grid option not performed.
#### Example 1

> `axlFormGridOption(fw, "mygrid" 'goto 10)`

Makes row 10 visible.

#### Example 2

> `axlFormGridOption(fw, "mygrid" 'goto 5:2)`

Makes row 5 column 2 visible.

#### Example 3

> `axlFormGridOption(fw, "mygrid" 'deselectAll)`

Deselects anything highlighted in the grid.

### axlFormSetActiveField

`axlFormSetActiveField(r_formt_field)⇒ t/nil`

#### Description

Makes the indicated field the active form field.

**Note:** If you do an`axlFormRestoreField`in your dispatch handler on the field passed to your handler, then that field remains active.

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_field` | Field name.
#### Value Returned

|  |
| --- | ---
| `t` | Field set active.
| `nil` | Failed to set the field active.
### axlFormSetDecimal

`axlFormSetDecimal(o_formg_fieldx_decimalPlaces)⇒ t/nil`

#### Description

Sets the decimal precision for real fill-in fields in the form. If`g_field` is `nil`, sets the precision for all real fill-in fields in the form.

#### Arguments

|  |
| --- | ---
| `o_form` | Form handle.
| `g_field` | Field label, or`nil` for all fields.
| `x_decimalPlaces` | Number of decimal places - must be a positive integer.
#### Value Returned

|  |
| --- | ---
| `t` | Successfully set new decimal precision.
| `nil` | Error due to invalid arguments.
### axlFormSetFieldEditable

`axlFormSetFieldEditable(r_formt_fieldg_editable)⇒ t/nil`

#### Description

Sets individual form fields to editable (`t)` or greyed (`nil`).

#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_field` | Field name.
| `g_editable` | Editable (`t`) or greyed (`nil`).
#### Value Returned

|  |
| --- | ---
| `t` | Set form field to editable or greyed.
| `nil` | Failed to set form field to editable or greyed.
### axlFormSetFieldLimits

`axlFormSetFieldLimits(o_formt_fieldg_ming_max)⇒ t/nil`

#### Description

Sets the minimum or maximum values a user can enter in an integer or real fill-in field. If a`nil` value is provided, that limit is left unchanged.

For a`REAL` field, the type for `g_min` and `g_max` may be `int`, `float`, or `nil`. For an `INT` or `LONG`, the type must be `int` or `nil`.

TRACKBAR: When used for a trackbar field type. If either of the argument is`0,` then the current setting for that option is maintained. Both `g_min` and `g_max` must be integer numbers. `g_min` is the interval of the tickmarks (default is 1). Tickmarks may not be shown in all user interfaces. This is the interval size when moving the trackbar to the next tick mark via axlFormSetField. `g_max` is the the number of steps in the trackbar (default is 100).

#### Arguments

|  |
| --- | ---
| `o_form` | Form handle.
| `t_field` | Field label.
| `g_min` | Minimum value for field.
| `g_max` | Maximum value for field.
#### Value Returned

|  |
| --- | ---
| `t` | Set max or min.
| `nil` | Error, indicating a problem with one of the input parameters.
### axlFormTreeViewAddItem

```
axlFormTreeViewAddItem(r_formt_fieldt_labelg_hParentg_hInsertAfter[g_multiSelectF][g_hLeafImage][g_hOpenImage][g_hClosedImage])⇒ g_hItem/nil
```

#### Description

Adds an item to a treeview under*parent* and after *insertAfter* sibling. If sibling is `nil`, the item is added as the last child of a parent. If parent is `nil`, item is created as the root of the tree.

**Note:** This is the only interface for adding an item to a tree.`axlFormSetField` is disabled for Tree controls.

Applications must keep the returned handle`l_hItem` since a handle will be passed as `form->curValueInt` when the item is selected from tree view. The string associated with the selected item is also passed as `form->curValue`, however the string value may not be unique and cannot be used as a reliable identifier for the selected treeview item.

The tree view defaults to single selection mode. There is no checkbox associated with items in the tree view to make multiple selections. To make a tree view item multi select, pass one of the following values for`t_multiSelectF`:

* `nil` or `'TVSELECT_SINGLE` for no selection state checkbox

* `t` or '`TVSELECT_2STATE` for 2 state checkbox

* `'TVSELECT_3STATE` for 3 state checkbox

If an item is defined as multi select, a check box appears as part of the item. The user can check/uncheck (2 state) this box to indicate selection or select checked/unchecked/disabled modes for a 3 state checkbox. When the user makes any selection in the checkbox, its value is passed to application code in`form->treeViewSelState`. In this case,
`form->curValue` is `nil`.

#### **Callback Values**

In the callback function for the form, the first argument form, has the following properties relevant to treeviews:

|  |
| --- | ---
| `form->curValue` | Contains the label of a treeview item. This is set in single select mode and in multi select mode when the user selects the item. In this case, the`result->tree.selectState` is -1.
| `form->curValueInt` | Contains id of the selected treeview item.
| `form->selectState` | In multi select mode, when the user picks the selection checkbox, this field will contain:  0 if selection checkbox is not checked  1 if selection checkbox is checked  2 if selection checkbox is disabled ((3 state mode only)  In this case the`result->string` is empty.  In all other cases the value is -1.
| `form->event` | If event property is set to`"rightpopup"`, treeview control has a popup and the user has selected an item in the popup. In this case, `form->curValue` is set to the popup index selected, and `form->selectState` is set to `-1`. `form->curValueInt` is set to the treeview item id.You add popups to treeview fields in a form like you add any other field in a form.  For all non-popup operations, event is set to`"normal."`
|
#### Arguments

|  |
| --- | ---
| `r_form` | Form`dbid`.
| `t_field` | Field name.
| `t_label` | String of item in the treeview.
| `g_hParent` | Handle of the parent. If`null`, item created as the root of the tree.
| `g_hInsertAfter` | Handle of the sibling to add the item after. If`null`, item added at the end of siblings of the parent.
| `t_multiSelectF` | If`t`, the item has a checkbox for multi selection.
| `g_hLeafImage` | Handle of the image to use whenever this item is a leaf node in the tree view. If`nil` or not supplied, the default pink diamond image is used.
| `g_hOpenImage` | Handle of image to be used whenever this item is an expanded parent node in the tree view. If`nil`or not supplied, the default open folder image is used.
| `g_hClosedImage` | Handle of image to use whenever the item is an unexpanded parent node in the tree view. If`nil` or not supplied, the default closed folder image is used.
#### Value Returned

|  |
| --- | ---
| `g_hItem` | Item is added to the tree view control.
| `nil` | No item is added to the tree view control due to an error.
#### Example

see`<cdsroot>``/share/pcb/examples/skill/form/basic/axlform.il`

### axlFormTreeViewChangeImages

```
axlFormTreeViewChangeImages(r_formt_fieldg_hItem[g_hLeafImage][g_hOpenImage][g_hClosedImage])⇒ t/nil
```

#### Description

Modifies various bitmap images associated with a given tree view item.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `g_hItem` | Handle of item in tree view. Handle was returned as a result of the call to`axlFormTreeViewAddItem` when item was initially added.
| `g_hLeafImage` | Handle of the image to use whenever item is a leaf node in the tree view. If`nil` or not supplied, the default pink diamond image is used.
| `g_hOpenImage` | Handle of image to use whenever item is an expanded parent node in the tree view. If`nil` or not supplied, the default open folder image is used.
| `g_hClosedImage` | Handle of image to use whenever item is an unexpanded parent node in the tree view. If`nil` or not supplied, the default closed folder image is used.
#### Value Returned

|  |
| --- | ---
| `t` | Tree view item's images are modified.
| `nil` | Failed to modify tree view item's images.
#### See Also

[axlFormTreeViewLoadBitmaps](#460771 "11")

### axlFormTreeViewChangeLabel

`axlFormTreeViewChangeLabel(r_formt_fieldg_hItemt_label)⇒ t/nil`

#### Description

Modifies text of a given treeview item.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `g_hItem` | Handle of item in the tree view. This handle was returned as a result of the call to`axlFormTreeViewAddItem`.
| `t_label` | New label.
#### Value Returned

|  |
| --- | ---
| `t` | Tree view item's label is modified.
| `nil` | Failed to modify tree view item's label.
### axlFormTreeViewGetImages

`axlFormTreeViewGetImages(r_formt_fieldg_hItem)⇒ l_hImage/nil`

#### Description

various bitmap image handles that refer to images used by a specified item in the tree view.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `g_hItem` | Handle of item in the tree view. This handle was returned as a result of the call to`axlFormTreeViewAddItem` when this item was initially added.
#### Value Returned

|  |
| --- | ---
| `l_hImage` | List of three image handles. The first is the handle of the image used when this item is a leaf node. The second is the handle of the image used when this item is an expanded parent node. The third is the handle of the image used when this item is an unexpanded parent node.
| `nil` | Error due to invalid arguments.
### axlFormTreeViewGetLabel

`axlFormTreeViewGetLabel(r_formt_fieldg_hItem)⇒ t_label/nil`

#### Description

Returns text of a given treeview item.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `g_hItem` | Handle of item in the tree view. This handle was returned as a result of the call to`axlFormTreeViewAddItem` when this item was initially added.
#### Value Returned

|  |
| --- | ---
| `t_label` | Text of given tree view item.
| `nil` | Failed to get text of given tree view item due to invalid arguments.
### axlFormTreeViewGetParents

`axlFormTreeViewGetParents(r_formt_fieldg_hItem)⇒ lg_hItem/nil`

#### Description

Returns a list of all the ancestors of a treeview control item, starting from the root of the tree. Helps in search operations in SKILL. Applications can traverse their tree list following parent lists to a given item instead of searching the whole tree for an item.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `g_hItem` | Handle of item in the tree view. This handle was returned as a result of the call to`axlFormTreeViewAddItem` when this item was initially added.
#### Value Returned

|  |
| --- | ---
| `lg_hItem` | List containing all parents, starting from the root.
| `nil` | Failed to obtain list due to invalid arguments.
### axlFormTreeViewGetSelectState

`axlFormTreeViewGetSelectState(r_formt_fieldg_hItem)⇒ x_selectState`

#### Description

In multi select mode, returns the select state of a treeview item. This is different than the current selected item in single select tree views. In multi select mode, users can change the select state by clicking on the select checkbox associated with each item.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `g_hItem` | Handle of item in the tree view. This handle was returned as a result of the call to`axlFormTreeViewAddItem` when this item was initially added.
#### Value Returned

In multi select mode:

1. Checkbox is unchecked.
2. Checkbox is checked.
3. Checkbox is disabled.
4. Single select mode or failure due to invalid arguments.

### axlFormTreeViewLoadBitmaps

`axlFormTreeViewLoadBitmaps(r_formt_fieldlt_bitmaps)⇒ l_hImage/nil`

#### Description

Allows an application to load one or more bitmaps into Allegro PCB Editor for use in specified tree view.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name.
| `lt_bitmaps` | Either a string containing the name of the bitmap file to load, or a list of strings, each of which is the name of a bitmap file to load.
**Notes:**

* Bitmap is found using BMPPATH variable.

* Uses file extension .bmp

* Bitmap images must be 16 x 16 pixels.

* A bitmap file can contain more than one image provided they are appended horizontally (i.e. a bitmap file containing n images will be (16\*n) x 16 pixels).

* The color RGB(255,0,0) is reserved for the transparent color.

* Any pixel with this color is displayed using the background color.

#### Value Returned

|  |
| --- | ---
| `l_hImage` | List of image handles that the caller will use to reference the images in subsequent`axlFormTreeViewAddItem` calls. List is ordered to correspond with the order that the images were listed in the `lt_bitmaps` parameter.
| `nil` | One or more of the bitmap files could not be found, or an error was encountered while adding images.
#### See Also

[axlFormTreeViewChangeImages](#460588 "11"), [axlFormTreeViewAddItem](#460322 "11")

#### Example

* File`myBmp1.bmp` is a 16 x 16 bitmap and `myBmp2.bmp` is a 32 x 16 bitmap:

`tree = axlFormTreeViewAddItem(fw "tree" "one" nil nil 'TVSELECT_3STATE)`

`l = axlFormTreeViewLoadBitmaps(fw "tree" list("myBmp1" "myBmp2"))`

`axlFormTreeViewChangeImages(fw "tree" tree car(l) cadr(l) nil)`

axlFormTreeViewLoadBitmaps may return (6 7 8) into variable l.

This mean sthat the image handle 6 would refer to the bitmap contained in myBmp1.bmp, the image handle 7 would refer to the left half of myBmp2.bmp, and the image handle 8 would refer to the right half of myBmp2.bmp.

### axlFormTreeViewSet

`axlFormTreeViewSet(r_formt_fields_optiong_hItem[g_data])⇒ t/nil`

#### Description

Allows an application to change global and individual items in a tree view control.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | Field name as a string
| `s_option` | `s_option` is one of the symbols listed.
| `g_hItem` | Tree view user data type.
| `[s_data]` | `optional symbol`
Each`s_option`is paired with `g_hItem`, the handle of an item in the tree view control. If the option you are setting is global, you use `nil` in place of `g_hItem`. The pairs of different values of `s_option` with `g_hItem` is in the following manner.

|  |  |
| --- | --- | ---
|  | ***s\_option*** | ***g\_hItem***
|  | `TV_REMOVEALL` | `nil`
|  | `TV_DELETEITEM` | `g_hItem`
|  | `TV_ENSUREVISIBLE` | `g_hItem`
|  | `TV_EXPAND` | `g_hItem(4)`
|  | `TV_EXPAND_TOP` | `nil (5)`
|  | `TV_COLLAPSE` | `g_hItem(4)`
|  | `TV_COLLAPSE_TOP` | `nil (5)`
|  | `TV_SELECTITEM` | `g_hItem (2) (3)`
|  | `TV_SORTCHILDREN` | `g_hItem`
|  | `TV_NOEDITLABEL` | `nil` - disables in place label editing
|  | `TV_NOSELSTATEDISPATCH` | `nil` -check box selection not dispatched
|  | `TV_ENABLEEDITLABEL` | `nil` - enable in place label editing
|  | `TV_MULTISELTYPE` | `g_hItem (1)`
|  | `TV_NOSHOWSELALWAYS` | `nil`
|  | `TV_SHOWSELALWAYS` | `nil`
**Notes:**

* For`TV_MULTISELTYPE`, you can also use the option `g_data` which is one of the following: `TVSELECT_SINGLE`, `TVSELECT_2STATE`, `TVSELECT_3STATE`. Default is `TVSELECT_SINGLE`.

* `g_hItem`is the Handle of item in the tree view control. Its value can be received in the following ways:

|  |  |
| --- | --- | ---
|  |  | Call`axlFormTreeViewAddItem`.
|  |  |
| --- | --- | ---
|  |  | Call`axlFormTreeViewGetParents`.
|  |  |
| --- | --- | ---
|  |  | Change a tree control that causes a form dispatch. Then the form User Type attributes`curValue` and `curValueInt` are the `g_hItem`.
* You can pass`nil` for `g_hItem` in some cases. Pass `nil` for `TV_SELECTITEM` option to deselect the item that is currently selected.

* If nil is passed for TV\_EXPAND or TV\_COLLAPSE then all levels (including) children are expanded or collapse.

* The two \_TOP options, TV\_EXPAND\_TOP and TV\_COLLAPSE\_TOP, respectively, expand and collapse all top level tree items. Children tree item states are preserved.

#### Value Returned

|  |
| --- | ---
| `t` | Changed one or more items in tree view control.
| `nil` | Failed to change items in tree view control.
#### Example

* Delete selected treeview item in a form.

> `(axlFormTreeViewSet form form->curField 'TV_DELETEITEM form->curValue)`

* Expand all levels including children:

> `axlFormTreeViewSet(form "tree" 'TV_EXPAND nil)`

* Collapses all expanded top levels:

> `axlFormTreeViewSet(form "tree" 'TV_COLLAPSE_TOP nil)`

For more examples see`<``cdsroot``>/share/pcb/examples/skill/form/basic`

### axlFormTreeViewSetSelectState

`axlFormTreeViewSetSelectState(r_formt_fieldg_hItemg_state)⇒ t/nil`

#### Description

In multi select mode, sets the select state. This is different than the current selected item in single select tree views. In multi select mode, users can change the select state by clicking on the select checkbox associated with each item.

#### Arguments

|  |
| --- | ---
| `r_form` | Form id.
| `t_field` | The name of the field.
| `g_hItem` | Handle of the item in the tree view. This handle was returned as a result of the call to`axlFormTreeViewAddItem` when this item was initially added.
| `g_state` | Select state to set.
* Select state is unchecked if`g_state` is `nil` or `'TVSTATE_UNCHECKED`

* Select state is checked if`g_state` is `t` or `'TVSTATE_CHECKED`

* Select state is disabled if`g_state` is `'TVSTATE_DISABLED`

#### Value Returned

|  |
| --- | ---
| `t` | Set select state.
| `nil` | Failed to set select state.
For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
