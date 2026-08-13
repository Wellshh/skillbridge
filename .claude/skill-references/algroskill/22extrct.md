### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

23
==

Reports and Extract Functions
=============================

AXL-SKILL Data Extract Functions
--------------------------------

The chapter describes the AXL-SKILL functions that extract data from an Allegro layout and write it to an ASCII file for external processing.

### axlExtractToFile

`axlExtractToFile(t_viewFilelt_resultFiles[lt_options])⇒ t/nil`

#### Description

Extracts data from the current design into an ASCII file. Performs the same process as the Allegro batch command`a_extract`.

#### Arguments

* Name of the extract command file (view file).
* List of file names for the extract output. If one file is specified, output is string instead of list. Maximum of 24 files are supported. If more then 24 views are required, use multiple view files.
* `"mcm":`Output MCM terminology.
* `"crosshatch":`Generate crosshatch lines when extracting crosshatched shapes.
* `"ok":`Unknown field names are OK. Useful when the extract command file has property names not defined for the design being extracted.
* `"short":`Extract data in the short format
* `"quiet":`Do not print progress messages on `stdout`.

#### Value Returned

|  |
| --- | ---
| `t` | Extract complete.
| `nil` | Failed to complete the extract. See the file`extract.log` for explanatory error messages.
#### Example

`axlExtractToFile( "cmp_rep_view" "my_comp_data")    ⇒ t`

Extracts the component data from the current layout. Writes the data to the file`my_comp_data.txt`.

### axlExtractMap

`axlExtractMap(t_viewFile[s_applyFunc][g_userData])⇒ t/l_dbid/nil`

#### Description

Takes a set of Allegro database objects you select using the Allegro extract command file and applies to each object a SKILL function you have chosen. The extract command file (the *view*) selects the objects and also sets any filters. Ignores the output data fields listed in the extract command file, since it does not create an output file.

Applies to each object that passes the selection and filter criteria in`s_applyFunc`, the SKILL function you supplied. SKILL calls `s_applyFunc` with two arguments--the `dbid` of the object and the variable `g_userData` that you supply as an argument. `g_userData` may be `nil`. If not, it normally is a defstruct or disembodied property list so that the called routine can update it destructively.

If`s_applyFunc` returns `nil`, then *axlExtractMap* stops execution, writes the message,`User CANCEL received` to the extract log file, and returns `nil`. If the callback function returns non `nil` then execution continues.

If`s_applyFunc` is `nil`, then `axlExtractMap` simply returns `l_dbid`, a list of `dbids` of the objects that pass the filter criteria. Use `l_dbid` to perform a `foreach` to operate on each object. (See examples below.)

Behaves slightly differently from a standard extract to a file. Provides`s_applyFunc` with the `dbid` of the parent (rotated) rectangle or shape, and not individual line/arc segments. Returns the attached text in the `FULL GEOMETRY` view.

Allegro "pseudoviews" (DRC, ECL, ECS, ECL\_NETWORK, PAD\_DEF, and so on) may not be used with*axlExtractMap*. The callback function is never called.

**Note:** `axlExtractMap` extracts only objects AXL-SKILL can model. For example, it does not extract function instances and unplaced components.

#### Arguments

|  |
| --- | ---
| `t_viewFile` | Name of the extract command file (view file).
| `s_applyFunc` | SKILL function to call for each selected object.
| `g_userData` | Data to pass to`s_applyFunc`. May be `nil`. Ignores `g_userData` if `s_applyFunc` is `nil`.
#### Value Returned

|  |
| --- | ---
| `t` | `s_applyFunc` is non `nil`. Applied SKILL functions to specified objects.
| `l_dbid` | List of`dbids` of the specified objects.
| `nil` | Failed to apply SKILL functions to specified objects. See the file`extract.log` for explanatory error messages.
#### Example

```
; user callback provided - function declared; with the (lambda) function; returns a list of the names of all nets    (defun get_netnames ()        ; byReference is disembodied prop list        ; with property 'nets to be used to store        ; the net names        (let ((byReference (list nil 'nets nil)))         (axlExtractMap "net_baseview"            ; function created right here            (lambda (dbid netRef)            ; add the name of this net to            ; the list of names                (putprop netRef                (cons (get dbid 'name)                    (get netRef 'nets)) 'nets)                t)      ; success return            byReference)        (get byReference 'nets))) ; return list of names
```

### axlReportList

`axlReportRegister() -> ll_reportList/nil`

#### Description

Lists all the SKILL reports registered to the Allegro PCB Editor report interface. Even if you do not register any reports, Allegro PCB Editor registers default reports written in SKILL.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `ll_reportList` | List of lists of reports register.
Each sub-list has the following format:

`(g_reportCallback t_description t_title)`

|  |
| --- | ---
| `nil` | No reports registered.
#### See Also

[axlReportRegister](#675451 "23")

### axlReportRegister

`axlReportRegister(g_reportCallbackt_descriptiont_title) ==> t/nil`

#### Description

Allows registration of user reports using the Allegro PCB Editor report dialog box. You provide a report name, title, and a report-generating callback function. Callback function format is:`g_reportCallback(t_outfile).`The callback should, if it generates the report, should return a `t` from the function. If it does not generate a report return a `nil` .

If you provide a`nil` `t_description` then the current report is unregistered. You can disregard the `t_title` in the unregister mode. You can register only one report per callback function (`g_reportCallback`). To delete an existing report, pass the callback function assigned to the report, a `nil` for the `t_description`, `abd` an empty string for the `_title`.

**Note:** Only applicable if you enable the*HTML-style reports*.

You can generate the report file in two formats: text or HTML.

Text:

* File is text based.

* Conversions include inserting links when following keywords are encountered:

> (http://) - add an HTML link

> (num <,> num) - XY coordinate; add a cross-probe link to zoom center on that coordinate

HTML:

* File starts with an <HTML>

* To enable xy zoom center, decorate all xy coordinates as follows:

> `<a href="xprobe:xy:<x>,<y>">(x y)</a>`

> Example: xy coordinate is (310 140)

> `<a href="xprobe:xy:310.0,140.0">(310.0 140.0)</a>`

Suggestions and restrictions:

* Your report description string should start with your company name or some other standard to keep all your reports together in the report dialog. Keep the description short to fit within the space provided in the dialog box.

* The report dialog is blocking. Do not use the following:

> APIs:

* any user pick or selection API,`axlSelect`, `axlEnter`.

* `axlShell`

* save or open a drawing.

* You can invoke your own form within the report callback but make sure it is blocking (use`axlUIWBlock(<formhandle>)`)

* The provided Skill callback function must return a

* 't' if you want to the report to display.

* A 'nil' if there is no report to display.

* If building a context where your report function is stored, you cannot make the`axlReportRegister` inside the context.The `axlReportRegister` must be placed in `allegro.ilinit` or the .`ini` file (if building autoload contexts). This is the same rule that applies to `axlCmdRegister`.

#### Arguments

|  |
| --- | ---
| `g_reportCallback` | Symbol or string of a SKILL function.
| `t_name` | Name of report (shown in reports dialog box); if`nil` will delete the report associated with `g_reportCallback`.
| `t_title` | Name in title bar when displaying report.
#### Value Returned

|  |
| --- | ---
| `t` | Arguments correct. A report is registered.
| `nil` | Illegal argument.
#### Examples

The following registers the report My Hello. The optional keyword in MyReport lets a direct call to MyReport generate a report to a fixed name file,`helloWorld.rpt`. otherwise it takes the name from the report dialog box.

> `axlReportRegister('MyReport, "XYZ Inc. Hello" "Hello World")`

> `; optional keyword allows a you to call MyReport with a nil where`

> `; the report file generated will be helloWorld.rpt. Otherwise if`

> `; called from report dialog, it will be passed a temporary filename`

> `procedure( MyReport(@optional (reportName "helloWorld"))`

> `let( (fp)`

> `fp = axlDMOpenFile("ALLEGRO_REPORT" reportName "w")`

> `axlLogHeader(fp "This is my report")`

> `fprintf(fp, "\nHello World\n")`

> `close(fp)`

> `t`

> `))`

Unregister above report:

> `axlReportRegister('MyReport, nil nil)`

#### See Also

[axlReportList](#672158 "23") [axlLogHeader](23utils.html#911489 "24")

####




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
