### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

10
==

Flow Control Functions
======================

### case

`case( g_keyForm l_clause1 [ l_clause2 ... ] ) => g_result | nil`

#### Description

Branches to one of the clauses depending on the value of the given expression. caseq()evaluates g\_keyForm and matches the resulting value sequentially against the clauses until it finds a match. Once a match is found it stops searching the clauses, evaluates the forms in the matching clause, and returns the resulting value. This is a syntax function.

Each l\_clause is in turn a list of the form (g\_keys g\_expr1 [g\_expr2 ...]) in which the firstelement, that is g\_keys, is either an atom (that is, a scalar) of any data type or a list of keys (to be compared with the given expression). If any of the keys matches the value from g\_keyForm, that clause is selected. Keys are always treated as constants and are never evaluated.

The symbol t has special meaning as a key in that it matches anything. It acts as a catch-alland should be handled last to serve as a default case when no other match is found. To match the value t, use a list of t as the key.

#### Arguments

|  |
| --- | ---
| `g_keyForm` | An expression whose value is evaluated and tested for equalityagainst the keys in each clause. A match occurs when either the selector is equal to the key or the selector is equal to one of the elements in the list of keys.
|  |
| --- | ---
|  | If a match is found, the expressions in that clause and that clauseonly (that is, the first match) are executed. The value of case is then the value of the last expression evaluated (that is, the last expression in the clause selected).
|  |
| --- | ---
|  | If there is no match, case returns nil.
|  |
| --- | ---
| `l_clause1` | An expression whose first element is an atom or list of atoms tobe compared against the value of `g_keyForm`. The remainder of the `l_clause` is evaluated if a match is found.
|  |
| --- | ---
|  | **Note**: Do not put quotes or use the list() function when specifying the lists in a clause.
|  |
| --- | ---
| `l_clause2` | Zero or more clauses of the same form as`l_clause1`.
#### Value Returned

|  |
| --- | ---
| `g_result` | Returns the value of the last expression evaluated in thematched clause, or `nil` if there is no match.
|  |
| --- | ---
| `nil` | If there is no match.
#### Example 1

`nameofmonth = "February"`

`month = case( nameofmonth`

`("January" 1)`

`("February" 2)`

`(t 'Other))`

`=> 2`

#### Example 2

`listofnums = list(2 4 6)`

`case( listofnums`

`(( (1 2 3) ) 'onetwothree)`

`(( (1 3 5)`

`(7 9 11) ) 'odd)`

`(( (2 4 6)`

`(8 10 12) ) 'even)`

`(t 'unknown))`

`=> even`

#### Example 3

`case( myBool`

`(nil 'never) ; this will never match, it is a list of no keys`

`(( nil ) nil) ; matches nil`

`(( t ) t) ; matches t`

`(t (error "Expected t or nil"))`

`)`

#### Example 4

`shapeType="line"`

`rectCount=0`

`labelOrLineCount=0`

`miscount=0`

`case( shapeType`

`("rect" ++rectCount println( "Shape is a rectangle" ))`

`(( "label" "line" ) ++labelOrLineCount println( "Shape is a line or a label" ))`

`(t ++miscount println( "Shape is miscellaneous" ))`

`) ; case`

`=> Shape is a line or a label`

#### Example 5

`procedure(migrateShape(shape "d")`

> `case(list(shape->layerName shape->purpose)`

> > `((("POLY" "test1"))`

> > `shape->layerName = "CPO"    shape->purpose = "drawing"`

> > ```
> > )((("Oxide" "drawing") ("abcd" "efgh"))    println(shape->layerName))((("M1" "net"))    shape->purpose = "label")((("M2" "net"))    shape->purpose = "label")((("M3" "net"))    shape->purpose = "label")((("M4" "net"))    shape->purpose = "label"))) ;
> > ```

#### Reference

[eq](logicalrel.html#1038850 "Logical and Relational Functions"), [equal](logicalrel.html#1038894 "Logical and Relational Functions")

### caseq

`caseq( g_keyForm l_clause1 [ l_clause2 ... ] ) => g_result | nil`

#### Description

Works exactly like the case() function, but uses eq() to find a matching clause instead of theequal() function. The keys used with caseq() should therefore not be strings or lists. In case you want to use a string value or a list, SKILL recommends using the case() function. See [eq](logicalrel.html#1038850 "Logical and Relational Functions") for details on the difference between the eq() and equal() functions.

#### Arguments

|  |
| --- | ---
| `g_keyForm` | An expression whose value is evaluated and tested for equalityagainst the comparators in each clause. A match occurs when either the selector is equal to the comparator or the selector is equal to one of the elements in the list given as the comparator.
|  |
| --- | ---
|  | If a match is found, the expressions in that clause and that clauseonly (that is, the first match) are executed. The value of case is then the value of the last expression evaluated (that is, the last expression in the clause selected).
|  |
| --- | ---
|  | If there is no match, case returns nil.
|  |
| --- | ---
| `l_clause1` | An expression whose first element is an atom or list of atoms tobe compared against the value of `g_keyForm`. The remainder of the `l_clause` is evaluated if a match is found.
|  |
| --- | ---
| `l_clause2` | Zero or more clauses of the same form as`l_clause1`.
#### Value Returned

|  |
| --- | ---
| `g_result` | Returns the value of the last expression evaluated in thematched clause, or `nil` if there is no match.
|  |
| --- | ---
| `nil` | If there is no match.
#### Example

`caseq(value`

`((nil) printf("Failed.\n"))`

`(indeterminate printf("Indeterminate.\n"))`

`((t) printf("Succeeded.\n"))`

`(t printf("Default.\n"))`

`))`

### catch

`catch(s_tagg_form) => g_result`

#### Description

Establishes a control transfer or a return point for the `throw` and `err` functions. The return point is identified with a `s_tag`. So, when a particular tag/exception is caught, `catch` evaluates `g_form`. If the forms execute normally (without error), the value of the last body form is returned from the `catch`. There can also be nested `catch` blocks and `s_tag` can be `t` (the value `t` the `catch` function catch any condition thrown by `throw`).

#### Arguments

|  |
| --- | ---
| `s_tag` | Identifies the return point for the`throw` and `err` functions
|  |
| --- | ---
| `g_form` | Specifies the forms that are evaluated
#### Value Returned

|  |
| --- | ---
| `g_result` | Returns the value of the last form if the forms exit normally,otherwise, returns the values that are thrown if a `throw` or `err` occurs
#### Example

The following example describes a nested catch. The tag, '`wrongPlat`, is caught by the default handler `catch(t . . .).`

`catch(t`

```
catch('issue1        printf("Hello ")            catch('issue2                when(cdsPlat() == "lnx86"                    throw('wrongPlat printf("\n") nil); no exception is thrown on non-lnx86 platforms                    )                    printf("world\n")                )
```

`)`

`)`

`Hello`

`=> nil`

### cond

`cond( l_clause1 ... ) => g_result`

#### Description

Examines conditional clauses from left to right until either a clause is satisfied or there are nomore clauses remaining. This is a syntax function.

Each clause has the form`(``g_condition g_expr1``... )`. `cond` examines a clause by evaluating the condition associated with the clause. The clause is said to be "satisfied" if `g_condition` evaluates to non-`nil`, in which case expressions in the rest of the clause are evaluated from left to right, and the value returned by the last expression in the clause is returned as the value of the `cond` form. If `g_condition` evaluates to `nil`, however, `cond` skips the rest of the clause and moves on to the next clause.

#### Arguments

|  |
| --- | ---
| `l_clause1` | Each clause should be of the form (`g_condition g_expr1``...`) where if `g_condition` evaluates to non-`nil` then all the succeeding expressions are evaluated.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of the last expression of the satisfied clause, or`nil` if no clause is satisfied.
#### Example

```
procedure( test(x)    cond(((null x) (println "Arg is null"))            ((numberp x)(println "Arg is a number"))            ((stringp x)(println "Arg is a string"))            (t (println "Arg is an unknown type"))))
```

test( nil )          => nil; Prints "Arg is null".
test( 5 )            => nil; Prints "Arg is a number".
test( 'sym )         => nil; Prints "Arg is an unknown type".

### do

```
do( ( ( s_var1 g_initExp1 [ g_stepExp1 ] )( s_var2 g_initExp2 [ g_stepExp2 ] ) ... )( g_terminationExp g_terminationExp1 ... )            g_loopExp1             g_loopExp2 ... )=> g_value
```

#### Description

Iteratively executes one or more expressions. Used in SKILL++ mode only.

Use`do` to iteratively execute one or more expressions. The `do` expression provides a `do-``while` facility allowing multiple loop variables with arbitrary variable initializations and step expressions. You can declare

* One or more loop variables, specifying for each variable both its initial value and how itgets updated each time around the loop.

* A termination condition which is evaluated before the body expressions are executed.

* One or more termination expressions to be evaluated upon termination to determine areturn value.

**A do Expression Evaluates in Two Phases**

* **Initialization phase**

> The initialization expressions`g_initExp1`, `g_initExp2`, ... are evaluated in an unspecified order and the results bound to the local variables `var1`, `var2`, ...

* **Iteration phase**

> This phase is a sequence of steps, informally described as going around the loop zeroor more times with the exit determined by the termination condition.

More formally stated:

* Each iteration begins by evaluating the termination condition.

> If the termination condition evaluates to a non-`nil` value, the `do` expression exits with a return value computed as follows:

* The termination expressions`terminationExp1`, `terminationExp2`, ... are evaluated in order. The value of the last termination condition is returned as the value of the `do` expression.

> Otherwise, the`do` expression continues with the next iteration as follows.

* The loop body expressions`g_loopExp1`, `g_loopExp2`, ... are evaluated in order.

* The step expressions`g_stepExp1`, `g_stepExp2`, ..., if given, are evaluated in an unspecified order.

* The local variables`var1`, `var2`, ... are bound to the above results. Reiterate from step one.

#### Example

By definition, the sum of the integers*1*, ..., *N* is the *Nth* triangular number. The following example finds the first triangular number greater than a given limit.

```
procedure( trTriangularNumber( limit )    do(        (                   ;;; start loop variables            ( i 0 i+1 )            ( sum 0 )       ;;; no step expression                            ;;; same as ( sum 0 sum )        )                   ;;; end loop variables        ( sum > limit       ;;; test            sum             ;;; return result            )         sum = sum+i         ;;; body        )                     ; do    )                         ; proceduretrTriangularNumber( 4 ) => 6trTriangularNumber( 5 ) => 6trTriangularNumber( 6 ) => 10
```

#### Reference

[while](#1039449 "Flow Control Functions")

### exists

```
exists( s_formalVar l_valueList g_predicateExpr )=> g_resultexists( s_key o_table g_predicateExpr )=> t | nil
```

#### Description

Returns the first tail of`l_valueList` whose `car` satisfies a predicate expression. Also verifies whether an entry in an association table satisfies a predicate expression. This is a syntax form.

This process continues to apply the`cdr` function successively through `l_valueList` until it finds a list element that causes `g_predicateExpr` to evaluate to non-`nil`. It then returns the tail that contains that list element as its first element.

This function can also be used to verify whether an entry in an association table satisfies`g_predicateExpr`.

#### Arguments

|  |
| --- | ---
| `s_formalVar` | Local variable that is usually referenced in`g_predicateExpr`.
|  |
| --- | ---
| `l_valueList` | List of elements that are bound to`s_formalVar`, one at a time.
|  |
| --- | ---
| `g_predicateExpr` | SKILL expression that usually uses the value of`s_formalVar`.
|  |
| --- | ---
| `s_key` | Key portion of an association table entry.
|  |
| --- | ---
| `o_table` | Association table containing the entries to be processed.
#### Value Returned

|  |
| --- | ---
| `g_result` | First tail of`l_valueList` whose `car` satisfies `g_predicateExpr`.
|  |
| --- | ---
| `nil` | If none of the elements in`l_valueList` can satisfy it.
|  |
| --- | ---
| `t` | Entry in an association table satisfies`g_predicateExpr`.
#### Example

`exists( x '(1 2 3 4) (x > 1) )  => (2 3 4)exists( x '(1 2 3 4) (x > 4) ) => nil`

`exists( key myTable (and (stringp key)             (stringp myTable[key])))=> t`

Tests an association table and verifies the existence of an entry where both the key and itscorresponding value are of type `string`.

#### Reference

`car, cdr`

### existss

```
existss( s_formalVar l_valueList g_predicateExpr )=> g_resultexistss( s_key o_table g_predicateExpr )=> t/nil
```

#### Description

Returns the first tail of`l_valueList` whose `car` satisfies a predicate expression. Also verifies whether an entry in an association table satisfies a predicate expression. In the SKILL++ mode, this function always locally wraps the loop or iterator local variable (`s_formalVar`) in a `let` block while compiling the code. Local wrapping preserves the lexical scope of the loop variable. This function may work slower than its non-wrapped counterpart `exists`. This is a syntax form.

This process continues to apply the`cdr` function successively through `l_valueList` until it finds a list element that causes `g_predicateExpr` to evaluate to non-`nil`. It then returns the tail that contains that list element as its first element.

This function can also be used to verify whether an entry in an association table satisfies`g_predicateExpr`.

#### Arguments

|  |
| --- | ---
| `s_formalVar` | Local variable that is usually referenced in`g_predicateExpr`.
|  |
| --- | ---
| `l_valueList` | List of elements that are bound to`s_formalVar`, one at a time.
|  |
| --- | ---
| `g_predicateExpr` | SKILL expression that usually uses the value of`s_formalVar`.
|  |
| --- | ---
| `s_key` | Key portion of an association table entry.
|  |
| --- | ---
| `o_table` | Association table containing the entries to be processed.
#### Value Returned

|  |
| --- | ---
| `g_result` | First tail of`l_valueList` whose `car` satisfies `g_predicateExpr`.
|  |
| --- | ---
| `nil` | If none of the elements in`l_valueList` can satisfy it.
|  |
| --- | ---
| `t` | Entry in an association table satisfies`g_predicateExpr`.
#### Example

```
(defun test_exists (x)    existss( x (list x x+1 x+9) println(x))    println(x)    )
```

`test_exists(9)`

=> 9
10
18
9
nil

### for

`for( s_loopVarx_initialValuex_finalValueg_expr1[ g_expr2 ... ])=> t`

#### Description

Evaluates the sequenceg\_expr1, g\_expr2 ... for each loop variable value, beginning with x\_initialValue and ending with x\_finalValue. This is a syntax form.

First evaluates the initial and final values, which set the initial value and final limit for the localloop variable named s\_loopVar. Both x\_initialValue and x\_finalValue must be integer expressions. During each iteration, the sequence of expressions g\_expr1, g\_expr2 ... is evaluated and the loop variable is then incremented by one. If the loop variable is still less than or equal to the final limit, another iteration is performed. The loop terminates when the loop variable reaches a value greater than the limit. The loop variable must not be changed inside the loop. It is local to the for loop and would not retain any meaningful value upon exit from the for loop.

#### Arguments

|  |
| --- | ---
| s\_loopVar | Name of the local loop variable that must not be changed insidethe loop.
|  |
| --- | ---
| x\_initialValue | Integer expression setting the initial value for the local loopvariable.
|  |
| --- | ---
| x\_finalValue | Integer expression giving final limit value for the loop.
|  |
| --- | ---
| g\_expr1 | Expression to evaluate inside loop.
|  |
| --- | ---
| g\_expr2 | Additional expression(s) to evaluate inside loop.
#### Value Returned

|  |
| --- | ---
| t | This construct always returnst.
#### Example

```
sum = 0for( i 1 10    sum = sum + i    printf("%d\n" sum))=> t                          ; Prints 10 numbers and returns t.
```

#### Reference

`foreach`

### fors

`fors( s_loopVarx_initialValuex_finalValueg_expr1[ g_expr2 ... ])=> t`

#### Description

Evaluates the sequence g\_expr1, g\_expr2 ... for each loop variable value, beginning withx\_initialValue and ending with x\_finalValue. In the SKILL++ mode, this function always locally wraps the loop or iterator local variable (s\_loopVar) in a let() block while compiling the code. Local wrapping preserves the lexical scope of the loop variable. This function may work slower than its non-wrapped counterpart `for`. This is a syntax form.

First evaluates the initial and final values, which set the initial value and final limit for the localloop variable named s\_loopVar. Both x\_initialValue and x\_finalValue must be integer expressions. During each iteration, the sequence of expressions g\_expr1, g\_expr2 ... is evaluated and the loop variable is then incremented by one. If the loop variable is still less than or equal to the final limit, another iteration is performed. The loop terminates when the loop variable reaches a value greater than the limit. The loop variable must not be changed inside the loop. It is local to the for loop and would not retain any meaningful value upon exit from the for loop.

#### Arguments

|  |
| --- | ---
| `s_loopVar` | Name of the local loop variable that must not be changed insidethe loop
|  |
| --- | ---
| `x_initialValue` | Integer expression setting the initial value for the local loopvariable
|  |
| --- | ---
| `x_finalValue` | Integer expression giving final limit value for the loop
|  |
| --- | ---
| `g_expr1` | Expression to evaluate inside loop
|  |
| --- | ---
| `g_expr2` | Additional expression(s) to evaluate inside loop
#### Value Returned

|  |
| --- | ---
| t | This construct always returns t
#### Example

`(defun test_for (x)`

`fors( x x+1 x+9 println(x))`

`println(x)`

`)`

`test_for(9)`

`=> 10`

`11`

`12`

`13`

`14`

`15`

`16`

`17`

`18`

`9`

`nil`

### forall

```
forall(s_formalVarl_valueListg_predicateExpr)=> t / nilforall(s_keyo_tableg_predicateExpr)=> t / nil
```

#### Description

Checks ifg\_predicateExpr evaluates to non-nil for every element in l\_valueList. This is a syntax form.

Verifies that an expression remains true for every element in a list. Theforall function can also be used to verify that an expression remains true for every key/value pair in an association table. The syntax for association table processing is provided in the second syntax statement.

#### Arguments

|  |
| --- | ---
| s\_formalVar | Local variable usually referenced ing\_predicateExpr.
|  |
| --- | ---
| l\_valueList | List of elements that are bound tos\_formalVar one at a time.
|  |
| --- | ---
| g\_predicateExpr | A SKILL expression that usually uses the value ofs\_formalVar.
|  |
| --- | ---
| s\_key | Key portion of the table entry.
|  |
| --- | ---
| o\_table | Association table containing the entries to be processed.
#### Value Returned

|  |
| --- | ---
| t | Ifg\_predicateExpr evaluates to non-nil for every element in l\_valueList or for every key in an association table.
|  |
| --- | ---
| nil | Otherwise.
#### Example

`forall( x '(1 2 3 4) (x > 0) )=> tforall( x '(1 2 3 4) (x < 4) )=> nil`

`forall(key myTable (and (stringp key)(stringp myTable[key])))=> t`

Returnst if each key and its value in the association table are of the type string.

#### Reference

### foralls

```
foralls( s_formalVarl_valueListg_predicateExpr)=> t / nilforalls(s_keyo_tableg_predicateExpr)=> t / nil
```

#### Description

Checks if`g_predicateExpr` evaluates to non-nil for every element in l\_valueList. In the SKILL++ mode, this function always locally wraps the loop or iterator local variable (s\_formalVar) in a let block while compiling the code. Local wrapping preserves the lexical scope of the loop variable. This function may work slower than its non-wrapped counterpart forall. This is a syntax form.

Verifies that an expression remains true for every element in a list.The forall function can also be used to verify that an expression remains true for every key/value pair in an association table. The syntax for association table processing is provided in the second syntax statement.

#### Arguments

|  |
| --- | ---
| `s_formalVar` | Local variable usually referenced in g\_predicateExpr.
|  |
| --- | ---
| `l_valueList` | List of elements that are bound to s\_formalVar one at a time.
|  |
| --- | ---
| `g_predicateExpr` | A SKILL expression that usually uses the value of s\_formalVar.
|  |
| --- | ---
| `s_key` | Key portion of the table entry.
|  |
| --- | ---
| `o_table` | Association table containing the entries to be processed.
#### Value Returned

|  |
| --- | ---
| t | If g\_predicateExpr evaluates to non-nil for every element inl\_valueList or for every key in an association table.
|  |
| --- | ---
| nil | Otherwise.
#### Example

```
(defun test_forall (x)    foralls( x (list x x+1 x+9) println(x))    println(x)    )
```

`test_forall(9)`

`=> 99nil`

### foreach

```
foreach( s_formalVar g_exprList g_expr1 [ g_expr2 ... ] )=> l_valueList / l_resultforeach( ( s_formalVar1... s_formalVarN ) g_exprList1... g_exprListN g_expr1 [ g_expr2 ... ] )=> l_valueList / l_resultforeach( s_formalVar g_exprTable g_expr1 [ g_expr2 ... ] )=> o_valueTable | l_result
```

#### Description

Evaluates one or more expressions for each element of a list of values. This is a syntax form.

foreach(s\_formalVar g\_exprList g\_expr1 [ g\_expr2 ... ] )
=> l\_valueList / l\_result

The first syntax form evaluatesg\_exprList, which returns a list l\_valueList. It then assigns the first element from l\_valueList to the formal variable s\_formalVar and executes the expressions g\_expr1, g\_expr2 ... in sequence. The function then assigns the second element from l\_valueList and repeats the process until l\_valueList is exhausted.

foreach( (s\_formalVar1...s\_formalVarN ) g\_exprList1... g\_exprListN g\_expr1 [ g\_expr2 ... ] )
=> l\_valueList / l\_result

The second syntax form offoreach can iterate over multiple lists to perform vector operations. Instead of a single formal variable, the first argument is a list of formal variables followed by a corresponding number of expressions for value lists and the expressions to be evaluated.

foreach(s\_formalVar g\_exprTable g\_expr1 [ g\_expr2 ... ])
=> o\_valueTable / l\_result

The third syntax form offoreach can be used to process the elements of an association table. In this case, s\_formalVar is assigned each key of the association table one by one, and the body expressions are evaluated each iteration. The syntax for association table processing is provided in this syntax statement.

#### Arguments

|  |
| --- | ---
| s\_formalVar | Name of the variable.
|  |
| --- | ---
| s\_mappingFunction | One ofmap, mapc, mapcan, mapcar, or maplist.
|  |
| --- | ---
| g\_exprList | Expression whose value is a list of elements to assign to theformal variable s\_formalVar.
|  |
| --- | ---
| g\_expr1, g\_expr2 | Expressions to execute.
|  |
| --- | ---
| g\_exprTable | Association table whose elements are to be processed.
#### Value Returned

|  |
| --- | ---
| l\_valueList | Value of the second argument,g\_exprList.
|  |
| --- | ---
| l\_result | The result of the last expression evaluated.
|  |
| --- | ---
| o\_valueTable | Value ofg\_exprTable.
#### Example

`foreach( x '(1 2 3 4) println(x))`

```
1                   ; Prints the numbers 1 through 4.234=> (1 2 3 4)        ; Returns the second argument to foreach.
```

The next example showsforeach accessing an association table and printing each key and its associated data.

`foreach(key myTable printf("%L : %L\n" key myTable[key]))`

Example with more than one loop variable:

`(foreach (x y) '(1 2 3) '(4 5 6) (println x+y))579=> (1 2 3)`

#### Errors and Warnings

The error messages fromforeach might at times appear cryptic because some foreach forms get expanded to call the mapping functions mapc, mapcar, mapcan, and so forth.

#### Advanced Usage

Theforeach function typically expands to call mapc; however, you can also request that a specific mapping function be applied by giving the name of the mapping function as the first argument to foreach. Thus, foreach can be used as an extremely powerful tool to construct new lists.

Mapping functions are not accepted when this form is applied to association tables.

```
foreach( mapcar x '(1 2 3) (x >1))=> (nil t t) foreach( mapcan x '(1 2 3) if((x > 1) ncons(x))) => (2 3)foreach( maplist x '(1 2 3) length(x)) => (3 2 1)
```

### foreachs

```
foreachs( s_formalVar g_exprList g_expr1 [ g_expr2 ... ] )=> l_valueList/l_resultforeachs( ( s_formalVar1... s_formalVarN ) g_exprList1... g_exprListN g_expr1 [ g_expr2 ... ] )=> l_valueList/l_resultforeachs( s_formalVar g_exprTable g_expr1 [ g_expr2 ... ] )=> o_valueTable/l_result
```

#### Description

Evaluates one or more expressions for each element of a list of values. In the SKILL++ mode, this function always locally wraps the loop or iterator local variable, `s_formalVar,`in a `let` block while compiling the code. Local wrapping preserves the lexical scope of the loop variable. This function may work slower than its non-wrapped counterpart `foreach`. This is a syntax form.

The first form shown in the syntax above evaluates`g_exprList`, which returns a list `l_valueList`. It then assigns the first element from `l_valueList` to the formal variable `s_formalVar` and executes the expressions`g_expr1`*,* `g_expr2 ...` in sequence. The function then assigns the second element from `l_valueList` and repeats the process until `l_valueList` is exhausted.

The second form shown in the syntax above can iterate over multiple lists to perform vectoroperations. Instead of a single formal variable, the first argument is a list of formal variables followed by a corresponding number of expressions for value lists and the expressions to be evaluated.

The third form shown in the syntax above can be used to process the elements of anassociation table. In this case, `s_formalVar` is assigned each key of the association table one by one, and the body expressions are evaluated each iteration. The syntax for association table processing is provided in this syntax statement.

#### Arguments

|  |
| --- | ---
| `s_formalVar` | Name of the local loop variable that must not be changed insidethe loop
|  |
| --- | ---
| `s_mappingFunction` | One of`map`, `mapc`, `mapcan`, `mapcar`, or `maplist`
|  |
| --- | ---
| `g_exprList` | Expression whose value is a list of elements to assign to theformal variable `s_formalVar`
|  |
| --- | ---
| `g_expr1`, `g_expr2` | Expressions to execute
|  |
| --- | ---
| `g_exprTable` | Association table whose elements are to be processed
#### Value Returned

|  |
| --- | ---
| `l_valueList` | Value of the second argument,`g_exprList`
|  |
| --- | ---
| `l_result` | The result of the last expression evaluated
|  |
| --- | ---
| `o_valueTable` | Value of`g_exprTable`
#### Example

```
toplevel('ils)(defun test_foreach (x)    foreachs( x (list x x+1 x+9) println(x))    println(x)
```

`)`

`test_foreach(9)`

`=> 910189nil`

### if

```
if( g_condition g_thenExpression [ g_elseExpression ] ) => g_resultif( g_condition then g_thenExpr1 ... [ else g_elseExpr1 ... ] ) => g_result
```

#### Description

Selectively evaluates two groups of one or more expressions. This is a syntax form.

`if( g_condition g_thenExpression [ g_elseExpression ] ) => g_result`

The`if` form evaluates `g_condition`, typically a relational expression, and executes `g_thenExpression` if the condition is true (that is, its value is non-`nil`); otherwise, `g_elseExpression` is executed. The value returned by `if` is the value of the corresponding expression evaluated. The `if` form can therefore be used to evaluate expressions conditionally.

`if( g_condition then g_thenExpr1 ... [ else g_elseExpr1 ... ] ) => g_result`

The second form of`if` uses the keywords `then` and `else` to group sequences of expressions for conditional execution. If the condition is true, the sequence of expressions between `then` and `else` (or the end of the `if` form) is evaluated, with the value of the last expression evaluated returned as the value of the form. If the condition is `nil` instead, the sequence of expressions following the `else` keyword (if any) is evaluated instead. Again, the value of the last expression evaluated is returned as the value of the form.

#### Arguments

|  |
| --- | ---
| `g_condition` | Any SKILL expression.
|  |
| --- | ---
| `g_thenExpression` | Any SKILL expression.
|  |
| --- | ---
| `g_elseExpression` | Any SKILL expression.
#### Value Returned

|  |
| --- | ---
| `g_result` | The value of`g_thenExpression` if `g_condition` has a non-`nil` value. The value of `g_elseExpression` is returned if the above condition is not true.
#### Example

```
x = 2if( (x > 5) 1 0)=> 0                     ; Returns 0 because x is less than 5.
```

```
a = "polygon"if( (a == "polygon") print(a) ) "polygon"                 ; Prints the string polygon.=> nil                    ; Returns the result of print.
```

```
x = 5if( x "non-nil" "nil" )=> "non-nil"              ; Returns "non-nil" because x was not                          ; nil. If x was nil then "nil" would be                          ; returned.
```

```
x = 7if( (x > 5) then 1 else 0)=> 1                      ; Returns 1 because x is greater than 5.
```

```
if( (x > 5)    then println("x is greater than 5")        x + 1    else print("x is less ")        x - 1)
```

```
x is greater than 5       ; Printed if x was 7.=> 8                      ; Returned 8 if x was 7.
```

#### Reference

[cond](#1038931 "Flow Control Functions"), [foreach](#1039950 "Flow Control Functions"), [unless](#1039335 "Flow Control Functions"), [while](#1039449 "Flow Control Functions")

### go

`go( s_label )`

#### Description

Transfers control to the statement following the label argument. This is a syntax form.

The`go` statement is only meaningful when it is used inside a `prog` statement. Control can be transferred to any labelled statement inside any `progs` that contain the `go` statement, but cannot be transferred to labelled statements in a `prog` that is not active at the time the `go` statement is executed. Generally, using `go` is considered poor programming style when higher level control structures such as `foreach` and `while` can be used.

#### Arguments

|  |
| --- | ---
| `s_label` | Label you want to transfer control to inside a`prog`.
#### Value Returned

|  |
| --- | ---
| None |
#### Example

The following example demonstrates how to use the`go` function form in a simple loop structure.

```
procedure( testGo( data )    prog( ()    start        print( car( data ))        data = cdr( data )        if( data go( start )) ; go statement to jump to start.))
```

```
testGo( '(a b c))abc                           ; Prints the variable data.=> nil                        ; Returns nil.
```

#### Reference

[foreach](#1039950 "Flow Control Functions"), [return](#1039235 "Flow Control Functions"), [while](#1039449 "Flow Control Functions")

### map

`map( u_func l_arg1 [ l_arg2 ... ] ) => l_arg1`

#### Description

Applies the given function to successive*sublists* of the argument lists and returns the first argument list. All of the lists should have the same length. This function is not the same as the standard Scheme `map` function. To get the behavior of the standard Scheme map function, use `mapcar` instead.

**Note:** This function is usually used for its side effects, not its return value (see`mapc`).

* ***This function is not the same as the standard Scheme map function. Toget the behavior of the standard Scheme map function, use mapcar instead.***

#### Arguments

|  |
| --- | ---
| `u_func` | Function to apply to successive sublists. Must be a function thataccepts lists as arguments.
|  |
| --- | ---
| `l_arg1` | Argument list.
|  |
| --- | ---
| `l_arg2` | Additional argument lists, which must be the same length as`l_arg1`.
#### Value Returned

|  |
| --- | ---
| `l_arg1` | The first argument list.
#### Example

`map( 'list '(1 2 3) '(9 8 7) )=> (1 2 3)`

No interesting side effect.

```
map( '(lambda (x y) (print (append x y))) '(1 2 3) '(9 8 7) )(1 2 3 9 8 7) (2 3 8 7) (3 7) => (1 2 3)
```

Prints three lists as a side effect and returns the list`(1 2 3)`.

#### Reference

`apply, foreach, mapc, mapcar, mapcan, maplist`

### mapc

`mapc( u_func l_arg1 [ l_arg2 ... ] ) => l_arg1`

#### Description

Applies a function to successiveelements of the argument lists and returns the first argument list. All of the lists should have the same length. `mapc` returns `l_arg1`.

`mapc` is primarily used with a `u_func` that has side effects, because the values returned by the `u_func` are not preserved. `u_func` must be an object acceptable as the first argument to apply and it must accept as many arguments as there are lists. It is first passed the `car` of all the lists given as arguments. The elements are passed in the order in which the lists are specified. The second elements are passed to `u_func`, and so on until the last element.

#### Arguments

|  |
| --- | ---
| `u_func` | Function to apply to argument lists.
|  |
| --- | ---
| `l_arg1` | Argument list.
|  |
| --- | ---
| `l_arg2` | Additional argument lists, which must be the same length as`l_arg1`.
#### Value Returned

|  |
| --- | ---
| `l_arg1` | The first argument list.
#### Example

`mapc( 'list '(1 2 3) '(9 8 7) ) => (1 2 3)`

```
mapc( '(lambda (x y) (print (list x y))) '(1 2 3) '(9 8 7) )(1 9) (2 8) (3 7) => (1 2 3)
```

Prints three lists as a side effect and returns the list`(1 2 3)`.

#### Reference

`foreach, map, mapcar, mapcan, maplist`

### mapcan

`mapcan( u_func l_arg1 [ l_arg2 ... ] ) => l_result`

#### Description

Applies a function to successive*elements* of the argument lists and returns the result of appending these intermediate results. All of the lists should have the same length.

Specifically, a function is applied to the `car` of all the argument lists, passed in the same order as the argument lists. The second elements are processed next, continuing until the last element is processed. The result of each call to `u_func` must be a list. These lists are concatenated using `nconc` and the resulting list of all the concatenations is the result of `mapcan`. The argument `u_func` must accept as many arguments as there are lists.

#### Arguments

|  |
| --- | ---
| `u_func` | Function to apply to argument lists.
|  |
| --- | ---
| `l_arg1` | Argument list.
|  |
| --- | ---
| `l_arg2` | Additional argument lists, which must be the same length as`l_arg1`.
#### Value Returned

|  |
| --- | ---
| `l_result` | List consisting of the concatenated results.
#### Example

```
mapcan( 'list '(1 2 3) '(a b c) )=> (1 a 2 b 3 c)mapcan( (lambda (n) (and (plusp n) (list n))) '(1 -2 3 -4 5))=> (1 3 5)
```

#### Reference

`map, mapc, mapcan, mapcar, maplist, nconc`

### mapcar

`mapcar( u_func l_arg1 [ l_arg2 ... ] ) => l_result`

#### Description

Applies a function to successive*elements* of the argument lists and returns the list of the corresponding results.

The values returned from successive calls to `u_func` are put into a list using the `list` function. If the argument lists are of different lengths, the `mapcar` function iterates till the end of the shortest list.

#### Arguments

|  |
| --- | ---
| `u_func` | Function to be applied to argument lists. The result of each callto `u_func` can be of any data type.
|  |
| --- | ---
| `l_arg1` | Argument list.
|  |
| --- | ---
| `l_arg2` | Additional argument lists.
#### Value Returned

|  |
| --- | ---
| `l_result` | A list of results from applying`u_func` to successive elements of the argument list.
#### Example

`mapcar( 'plus '(1 2 3) '(9 8 7) )=> (10 10 10)`

`mapcar( 'plus '(1 2 3 4) '(4 5) '(1 2 3 4 5 6) '(1 2 3))=> (7 11)`

`mapcar( 'list '(a b c) '(1 2 3) '(x y z) )=> ((a 1 x) (b 2 y) (c 3 z))`

`mapcar( lambda( (x) plus( x 1 )) '(2 4 6) )=> (3 5 7)`

#### Reference

`map, mapc, mapcan, mapcon, maplist, nconc`

### mapcon

`mapcon( u_func l_arg1 [l_arg2] ) => l_result`

#### Description

Applies the function`u_func` to successive sublists of the lists and returns a concatenated list.

#### Arguments

|  |
| --- | ---
| `u_func` | Specifies the function to be applied to the given list. Must acceptlists as arguments. The result of calling `u_func` can be of any data type.
|  |
| --- | ---
| `l_arg1` | Specifies the argument list to be processed
|  |
| --- | ---
| `l_arg2` | Additional argument lists, which must be the same length as`l_arg1`
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns a concatenated list that results from calling the`u_func` on the cons cells of the given list
#### Example

```
mapcon((lambda (x)(printf "x = %L\n" x)(list (car x) (add1 (car x)))) '(1 2 3 4)); lambda: (u_func) with one argument
```

`x = (1 2 3 4)`

`x = (2 3 4)`

`x = (3 4)`

`x = (4)`

`result: (1 2 2 3 3 4 4 5)`

`mapcon((lambda (x y) (printf "x = %L y = %L\n" x y)`

`(list (car x) (add1 (car y))))`

`'(1 2 3 4)`

`'(4 3 2 1)`

`) ; lambda: (u_func) is with 2 arguments`

`x = (1 2 3 4) y = (4 3 2 1)`

`x = (2 3 4) y = (3 2 1)`

`x = (3 4) y = (2 1)`

`x = (4) y = (1)`

`result : (1 5 2 4 3 3 4 2)`

### mapinto

`mapinto( l_resultSequence g_function ({l_sequences}*)) => l_resultSequence`

#### Description

Applies`g_function` to the elements of `l_sequences` and destructively modifies the `l_resultSequence`. The first argument is a sequence that receives the results of the mapping. If `l_resultSequence` and the other argument sequences are not all of the same length, the mapping stops when the shortest of `l_resultSequence` or `l_sequences` is exhausted.

If`l_resultSequence` is longer than `l_sequences`, extra elements at the end of `l_resultSequence` are unchanged.

**Note:** If you specify`nil` as the `l_resultSequence`, no mapping is performed since `nil` is a sequence of length zero.

#### Arguments

|  |
| --- | ---
| `l_resultSequence` | A sequence that receives the results of the mapping.
|  |
| --- | ---
| `g_function` | Function (`symbol` or `funobj`) that takes as many arguments as there are sequences.
|  |
| --- | ---
| `l_sequences` | Several lists. Each element of these lists is used as an argumentof `g_function`.
#### Value Returned

|  |
| --- | ---
| `l_resultSequence` | Updated first argument list.
#### Example

`mapinto ('(1 2 3 4) 'plus )`

`=>(1 2 3 4)`

`mapinto (' (1 2 3 4) 'plus ())`

`=>(1 2 3 4)`

`a = '(1 2 3 4 5)`

`mapinto ( a 'plus '(1 1 1) '(1 1))`

=>(2 2 3 4 5)

### maplist

`maplist( u_func l_arg1 [ l_arg2 ... ] ) => l_result`

#### Description

Applies a function to successive*sublists* of the argument lists and returns a list of the corresponding results. All of the lists should have the same length.

The returned values of the successive function calls are concatenated using the function`list`.

#### Arguments

|  |
| --- | ---
| `u_func` | Function to be applied to argument lists. Must accept lists asarguments. The result of calling `u_func` can be of any data type.
|  |
| --- | ---
| `l_arg1` | Argument list.
|  |
| --- | ---
| `l_arg2` | Additional argument lists, which must be the same length as`l_arg1`.
#### Value Returned

|  |
| --- | ---
| `l_result` | A list of the results returned from calling`u_func` on successive sublists of the argument list.
#### Example

`maplist( 'length '(1 2 3) )=> (3 2 1)`

`maplist( 'list '(a b c) '(1 2 3) )=> (((a b c)(1 2 3))((b c)(2 3))((c)(3)))`

#### Reference

`map, mapc, mapcan, mapcar, nconc`

### not

`not( g_obj ) => t | nil`

#### Description

Same as the`!` operator. Returns `t` if the object is `nil`, and returns `nil` otherwise.

#### Arguments

|  |
| --- | ---
| `g_obj` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_obj` is `nil`.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`(not nil)        => t(not 123)        => nil(not t)          => nil`

#### Reference

[null](logicalrel.html#1039423 "Logical and Relational Functions")

### regExitAfter

`regExitAfter( s_name ) => t | nil`

#### Description

Registers the action to be taken after the`exit` function has performed its bookkeeping tasks but before it returns control to the operating system.

#### Arguments

|  |
| --- | ---
| `s_name` | Name of the function that is to be added to the head of the list offunctions to be performed after the `exit` function.
#### Value Returned

|  |
| --- | ---
| `t` | The function is added to the list of functions.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

```
procedure( foo( @rest args)             println( "After proc being executed"))regExitAfter( 'foo) => t
```

#### Reference

[clearExitProcs](funcprog.html#1039045 "Function and Program Structure"), [exit](environment.html#1039176 "Environment Functions"), [regExitBefore](#1039127 "Flow Control Functions"), [remExitProc](#1039183 "Flow Control Functions")

### regExitBefore

`regExitBefore( s_name ) => t`

#### Description

Registers the action to be taken before the`exit` function is executed. If the function registered returns the `ignoreExit` symbol, the exit is aborted.

#### Arguments

|  |
| --- | ---
| `s_name` | Name of the function that is to be added to the head of the list offunctions to be executed before the `exit` function.
#### Value Returned

|  |
| --- | ---
| `t` | Always.
#### Example

```
procedure( foo() println( "Aborting exit") 'ignoreExit) => fooregExitBefore('foo) => texit                                ;Does not exit."Aborting exit"procedure( foo() println( "Exiting"))=> fooexit                                ;Exits program."Exiting"
```

#### Reference

[clearExitProcs](funcprog.html#1039045 "Function and Program Structure"), [exit](environment.html#1039176 "Environment Functions"), [regExitBefore](#1039127 "Flow Control Functions"), [remExitProc](#1039183 "Flow Control Functions")

### remExitProc

`remExitProc( s_name ) => t`

#### Description

Removes a registered exit procedure.

When SKILL exits, the function is not called.

#### Prerequisites

The exit procedure must have been previously registered with the`regExitBefore` or `regExitAfter` function.

#### Arguments

|  |
| --- | ---
| `s_name` | Name of the registered exit procedure to be removed.
#### Value Returned

|  |
| --- | ---
| `t` | Always.
#### Example

`remExitProc( 'endProc) => t`

#### Reference

[exit](environment.html#1039176 "Environment Functions"), [regExitBefore](#1039127 "Flow Control Functions"), [regExitAfter](#1039077 "Flow Control Functions")

### return

`return( [ g_result ] ) => g_result | nil`

#### Description

Forces the enclosing`prog` to exit and returns the given value. The `return` statement has meaning only when used inside a `prog` statement.

Both`go` and `return` are not purely functional in the sense that they transfer control in a non-standard way. That is, they don't return to their caller.

#### Arguments

|  |
| --- | ---
| `g_result` | Any SKILL object.
#### Value Returned

The enclosing`prog` statement exits with the value given to `return` as the `prog`'s value. If `return` is called with no arguments, `nil` is returned as the enclosing `prog`'s value.

#### Example

```
procedure( summation(l)    prog( (sum temp)        sum = 0        temp = l        while( temp            if( null(car(temp))            then                return(sum)            else                sum = sum + car(temp)                temp = cdr(temp)            )        )    ))
```

Returns the summation of previous numbers if a`nil` is encountered.

```
summation( '(1 2 3 nil 4)) => 6                  ; 1+2+3summation( '(1 2 3 4)) => nil                ; prog returns nil if no explicit return)
```

#### Reference

[nlambda](funcprog.html#1040927 "Function and Program Structure"), [go](#1038977 "Flow Control Functions")

### setof

```
setof( s_formalVar l_valueList g_predicateExpression )=> l_resultsetof( s_formalVar o_table g_predicateExpression )=> l_result
```

#### Description

Returns a new list containing only those elements in a list or the keys in an association tablethat satisfy an expression. This is a syntax form.

The`setof` form can also be used to identify all keys in an association table that satisfy the specified expression.

#### Arguments

|  |
| --- | ---
| `s_formalVar` | Local variable that is usually referenced in`g_predicateExpression`.
|  |
| --- | ---
| `l_valueList` | List of elements that are bound to`s_formalVar` one at a time.
|  |
| --- | ---
| `g_predicateExpression` | SKILL expression that usually uses the value of `s_formalVar`.
|  |
| --- | ---
| `o_table` | Association table whose keys are bound to`s_formalVar` one at time.
#### Value Returned

|  |
| --- | ---
| `l_result` | New list containing only those elements in`l_valueList` that satisfy `g_predicateExpression`, or list of all keys that satisfy the specified expression.
#### Example

```
setof( x '(1 2 3 4) (x > 2) )    => (3 4)setof( x '(1 2 3 4) (x < 3) )    => (1 2)
```

```
myTable = makeTable("atable" 0)  => table:atablemyTable["a"]="first"             => "first"myTable["b"]=2                   => 2setof(key myTable (and (stringp key)(stringp myTable[key])))                                 => ("a")
```

### setofs

```
setofs( s_formalVar l_valueList g_predicateExpression )=> l_resultsetofs( s_formalVar o_table g_predicateExpression )=> l_result
```

#### Description

Returns a new list containing only those elements in a list or the keys in an association tablethat satisfy an expression. In the SKILL++ mode, this function always locally wraps the loop or iterator local variable (`s_formalVar`) in a `let` block while compiling the code. Local wrapping preserves the lexical scope of the loop variable. This function may work slower than its non-wrapped counterpart `setof`. This is a syntax form.

The`setof` form can also be used to identify all keys in an association table that satisfy the specified expression.

#### Arguments

|  |
| --- | ---
| `s_formalVar` | Local variable that is usually referenced in`g_predicateExpression`.
|  |
| --- | ---
| `l_valueList` | List of elements that are bound to`s_formalVar` one at a time.
|  |
| --- | ---
| `g_predicateExpression` | SKILL expression that usually uses the value of `s_formalVar`.
|  |
| --- | ---
| `o_table` | Association table whose keys are bound to`s_formalVar` one at time.
#### Value Returned

|  |
| --- | ---
| `l_result` | New list containing only those elements in`l_valueList` that satisfy `g_predicateExpression`, or list of all keys that satisfy the specified expression.
#### Example

```
(defun test_setof (x)    setofs( x (list x x+1 x+9) println(x))    println(x)    )
```

`test_setof(9)`

=> 9
10
18
9
nil

### throw

`throw(s_tagg_value) =>`

#### Description

Transfers the control back to the return point established in a catch block. The argument value is used as the value to be passed. The `throw` function should always be used inside `catch(. . . g_form . . .).`

#### Arguments

|  |
| --- | ---
| `s_tag` | Specifies the return point in a catch block
|  |
| --- | ---
| `g_value` | Evaluates forms and saves the results. If the form producesmultiple values, then all the values are saved. The saved results are returned as the value or values of catch.
#### Value Returned

Transfers the control back to the return point in a catch block

#### Example

```
catch( 'problem    begin(        throw( 'problem                let( nil                printf( "Caught %L\n" 1) 1             )
```

`)            2        )`

`)`

`Caught 1 ; message is printed . . .`

= > 1 ; value returned by throw()

### unless

`unless( g_condition g_expr1 ... ) => g_result | nil`

#### Description

Evaluates a condition.If the result is true (non-`nil`), it returns `nil`; otherwise evaluates the body expressions in sequence and returns the value of the last expression. This is a syntax form.

The semantics of this function can be read literally as "unless the condition is true, evaluatethe body expressions in sequence".

#### Arguments

|  |
| --- | ---
| `g_condition` | Any SKILL expression.
|  |
| --- | ---
| `g_expr1` | Any SKILL expression.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of the last expression of the sequence`g_expr1` if `g_condition` evaluates to `nil`.
|  |
| --- | ---
| `nil` | If`g_condition` evaluates to non-`nil`.
#### Example

```
x = -123unless( x >= 0 println("x is negative") -x)=> 123            ;Prints "x is negative" as side effect.
```

`unless( x < 0 println("x is positive") x)=> nil`

#### Reference

[cond](#1038931 "Flow Control Functions"), [if](#1042019 "Flow Control Functions"), [when](#1039395 "Flow Control Functions")

### when

`when( g_condition g_expr1 ... ) => g_result | nil`

#### Description

Evaluates a condition. If the result is non-`nil`, evaluates the sequence of expressions and returns the value of the last expression. This is a syntax form.

If the result of evaluating`g_condition` is `nil`, `when` returns `nil`.

#### Arguments

|  |
| --- | ---
| `g_condition` | Any SKILL expression.
|  |
| --- | ---
| `g_expr1` | Any SKILL expression.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of the last expression of the sequence`g_expr1` if `g_condition` evaluates to non-`nil`.
|  |
| --- | ---
| `nil` | If the`g_condition` expression evaluates to `nil`.
#### Example

```
x = -123when( x < 0    println("x is negative")   -x)=> 123            ;Prints "x is negative" as side effect.
```

`when( x >= 0    println("x is positive")    x)=> nil`

#### Reference

[cond](#1038931 "Flow Control Functions"), [if](#1042019 "Flow Control Functions"), [unless](#1039335 "Flow Control Functions")

### while

`while( g_condition g_expr1 ... ) => t`

#### Description

Repeatedly evaluates a condition and sequence of expressions until the condition evaluatesto false. This is a syntax form.

Repeatedly evaluates`g_condition` and the sequence of expressions `g_expr1 ...` if the condition is true. This process is repeated until `g_condition` evaluates to false (`nil`). Note that because this form always returns `t`, it is principally used for its side-effects.

#### Arguments

|  |
| --- | ---
| `g_condition` | Any SKILL expression.
|  |
| --- | ---
| `g_expr1` | Any SKILL expression.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

`i = 0while( (i <= 10) printf("%d\n" i++) ) => t`

Prints the digits 0 through 10.

#### Reference

[foreach](#1039950 "Flow Control Functions")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
