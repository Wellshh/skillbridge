### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

18
==

Database Transaction Functions
==============================

This chapter describes the AXL-SKILL Database Transaction functions.

### axlDBCloak

`axlDBCloak(g_func[g_mode]/[lg_mode])⇒ g_return`

#### Description

Improves performance and program memory use while modifying many items in the database. You use`axlDBCloak` to update many etch or package symbols in batch mode. Works like SKILL's `eval` function. You pass it a function and its arguments using the following format:

> `axlDBCloak ('MyFunc( myargs) )`

You can use`axlDBCloak` to do the following:

* Batch any net based DRC updates.

* Batch connectivity update.

* Optionally, batch dynamic shape updates if`g_mode` is `'shape`.

* Optionally, ignores the FIXED property.

* Incorporate an errset around your function so any SKILL errors thrown are caught by`axlDBCloak`.

This function must be used if you need to update many etch or package symbols in a batch fashion.

Do not use`axlDBCloak` in these circumstances:

* If you are adding or deleting non-connectivity database items (for example, loading many lines to a manufacturing layer)

* If you need to interact with the user. Since connectivity is not updated, do not use the`axlEnter``XXX` functions. Instead, get the information from the user first, then do the cloak update.

* If you are reading the database, using cloak does not help and may actually slow performance.

* If making a single change, using Cloak slows performance.

**Note:** Using Cloak sets any database ids to`nil`.

gmode options (if multiple required pass a list of options

|  |
| --- | ---
| `'shape` | Improves performance if changes being made effect any dynamic shapes on the design. Generally you should set this if effecting ETCH layers with your changes.
| `'ignoreFixed` | Have the system ignore the FIXED property (see axlDBIgnoreFixed)
**CAUTIONS:**

* A frequent programming error is to leave of the tick (') mark that allows axlDBCloak to evaluate the function.

> CORRECT MODEL:

> `axlDBCloak( 'MyFunc(myArgs) '(shape ignoreFixed))`

> INCORRECT MODEL:

> `axlDBCloak( MyFunc(myArgs) '(shape ignoreFixed))`

> Both work but in the incorrect case now performance benefit offered by the cloaking function will by applied to MyFunc.

* Database transactions and cloaking (axlDBTransactionStart):

|  |  |
| --- | --- | ---
|  |  | Do NOT start and transaction inside a cloak and then terminate it outside the cloak. Terminate means calling either axlDBTransactionRollback, axlDBTransactionCommit axlDBTransactionOops.
|  |  |
| --- | --- | ---
|  |  | If you start a transaction inside a cloak then complete it before returning.
|  |  |
| --- | --- | ---
|  |  | If you start a transaction outside the cloak then its completion must outside the cloak.
* For effective debugging, first call your function directly from the top level function, then wrap in the cloak call.

#### Arguments

|  |
| --- | ---
| `g_func` | Function with any of its arguments.
| `s_mode` | option
| `ls_mode` | list of options
#### Value Returned

Returns what`g_func` returns.

#### Example

`procedure( DeleteSymbols()`

`let( (listOfSymbols)`

`listOfSymbols = axlDBGetDesign()->symbols`

`when( listOfSymbols`

`axlDBCloak( 'DeleteDoit(listOfSymbols) 'shape ))`

`axlShell("cputime stop"`

`))`

`procedure( DeleteDoit(listOfDatabaseObjects )`

`foreach(c_item listOfDatabaseObjects`

`printf("REFDES %s\n", c_item->refdes)`

`axlDeleteObject(c_item)`

`)`

`nil`

`)`

Deletes all placed symbols in the database.

#### See Also

[axlDBTransactionStart](#1076430 "18")

### axlDBTransactionCommit

`axlDBTransactionCommit(x_mark)⇒ t/nil`

#### Description

Commits a database transaction from the last transaction mark.

#### Arguments

|  |
| --- | ---
| `x_mark` | Database transaction mark returned from`axlDBTransactionStart`.
#### Value Returned

|  |
| --- | ---
| `t` | Database transaction committed.
| `nil` | Database transaction not committed.
#### Example

See`axlDBTransactionStart()` for an example.

### axlDBTransactionMark

`axlDBTransactionMark(x_mark)⇒ t/nil`

#### Description

Writes a mark in the database that you can use with[axlDBTransactionOops](#1076373 "18") to rollback database changes to this mark.

When a transaction mark is committed or rolled back, all`axlDBTransactionMarks` associated with that mark are discarded.

#### Arguments

|  |
| --- | ---
| `x_mark` | Database transaction mark returned from`axlDBTransactionStart`.
#### Value Returned

|  |
| --- | ---
| `t` | Mark written in the database.
| `nil` | No mark written in the database.
#### Example

See`axlDBTransactionStart()` for an example.

### axlDBTransactionOops

`axlDBTransactionOops(x_mark)⇒ t/nil`

#### Description

Undoes a transaction back to the last mark, or to start if there are no marks. Supports the Allegro*oops* model for database transactions.

When a transaction mark is committed or rolled back all, then that mark is no longer valid for*oopsing*.

#### Arguments

|  |
| --- | ---
| `x_mark` | Database transaction mark returned from`axlDBTransactionStart`.
#### Value Returned

|  |
| --- | ---
| `t` | Transaction undo completed.
| `nil` | Transaction is already back to the starting mark and there is nothing left to*oops*.
#### Example

See`axlDBTransactionStart` for an example.

### axlDBTransactionRollback

`axlDBTransactionRollback(x_mark)⇒ t/nil`

#### Description

Undo function for a database transaction.

#### Arguments

|  |
| --- | ---
| `x_mark` | Database transaction mark returned from`axlDBTransactionStart`.
#### Value Returned

|  |
| --- | ---
| `t` | Transaction undo completed.
| `nil` | Transaction undo not completed.
#### Example

See`axlDBTransactionStart` for an example.

### axlDBTransactionStart

`axlDBTransactionStart([g_undoMark])⇒ x_mark/nil`

#### Description

Marks the start of a transaction to the database. Returns a mark to the caller which is passed back to commit, mark, oops or rollback for nested transactions. Only the outermost caller of this function (the first caller) has control to commit or rollback the entire transaction.

You use this function with other`axlDBTransaction` functions.

Allegro cancels any transactions left active when your SKILL code terminates. You cannot start a transaction and keep it active across Allegro commands as an attempt to support*undo*.

Saving or opening a database cancels transactions.

#### Arguments

|  |
| --- | ---
| `g_undoMark` | This should be set to 'undoMark that are for commands that want multiple undo events. For example, place multiple individual symbols, you may want each placement to be an indivdual undo event.  By default, with a undo interactive all operations within the command results in a single undo even. See in axlCmdRegister on how write a Skill command that supports Allegro undo.
#### Value Returned

|  |
| --- | ---
| `x_mark` | Integer mark indicating transaction start.
| `nil` | Failed to mark transaction start.
#### Example 1

> `mark = axlDBTransactionStart()`

> `...#1 do stuff ...`

> `axlDBTransactionMark(mark)`

> `...#2 do stuff ...`

> `axlDBTransactionMark(mark)`

> `...#3 do stuff ...`

> `;; do an oops of the last two changes`

> `axlDBTransactionOops( mark ) ; oops out #3`

> `axlDBTransactionOops( mark ) ; oops out #2`

> `axlDBTransactionOops( topList); commit only #1`

Emulates the Allegro*oops* model.

#### Example 2

> `i = axlDBTransactionStart()`

> `... do stuff ...`

> `j = axlDBTransactionStart()`

> `... stuff ...`

> `axlDBTransactionCommit(j) ;; this is not really commited`

> `j = axlDBTransactionStart()`

> `... do more stuff ...`

> `axlDBTransactionRollback(j) ;; oops out "do more stuff"`

> `axlDBTransactionCommit(i) ;; commit changes to database`

Multiple Start marks.

**Note:** Database transaction functions do NOT mark select sets. The application handles select set management.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
