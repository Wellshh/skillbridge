<!--
source: sklangref/funcprog.md
part: 2/2
estimated_tokens: 3804
-->

The`@optional` option gives you another way to specify a flexible number of arguments. With `@optional`, each argument on the actual argument list is matched up with an argument on the formal argument list. If you place `@optional` in the argument list of a procedure definition, any argument following it is considered optional.

You can provide any optional argument with a default value. Specify the default value using adefault form. The default form is a two-member list. The first member of this list is the optional argument's name. The second member is the default value.

The default value is assigned only if no value is assigned when the function is called. If theprocedure does not specify a default value for a given argument, `nil` is assigned.

The following is an outline of a procedure that builds a box of a certain length and width.

```
procedure(buildbox(length width @optional (xcoord 0)    (ycoord 0) color)    .    .)
```

Both`length` and `width` must be specified when this function is called. However, the color and the coordinates of the box are declared as optional parameters. If only two parameters are specified, the optional parameters are given their default values. For `xcoord` and `ycoord`, those values are 0. Since no value is specified for `color`, `color`'s default value is `nil`.

Examine the following calls to`buildbox` and their return values:

```
buildbox(1 2); Builds a box of length 1, width 2     ; at the coordinates (0,0) with the default color nil
```

```
buildbox(3 4 5.5 10.5); Builds a box of length 3, width 4     ; at coordinates (5.5,10.5) with the default color nil
```

```
buildbox(3 4 5 5 'red); Builds a box of length 3, width 4     ; at coordinates (5,5) with the default color red.
```

As illustrated in the above examples,`@optional` relies on order to determine what actual arguments are assigned to each formal argument. When relying on order is too lengthy or inconvenient, another "at" sign parameter, `@key`, provides an alternative.

#### @key Option

`@key` and `@optional` are mutually exclusive; they cannot appear in the same argument list. The `@key` option lets you specify the expected arguments in any order.

For example, examine the following function:

```
procedure(setTerm(@key (deviceType 'unknown)    (baudRate 9600)    keyClick )    .    .)
```

If you call`setTerm` without arguments (that is, `setTerm()`), `deviceType` is set to unknown, `baudRate` to 9600, and *keyClick* to `nil`. Default forms work the same as they do for `@optional.` To specify a keyword for an argument (for example, `deviceType`, `baudRate`, and `keyClick` in the above function), precede the keyword with a question mark (?).

To set the`baudRate` to 4800 and the `keyClick` to `ON`, the call is:

```
setTerm(?baudRate 4800 ?keyClick 'ON)     ; This sets baudRate and keyClick. Because nothing    ; was specified for deviceType, it is set to its default,     ; unknown.setTerm(?keyClick 'ON ?baudRate 4800) ; Does exactly                                     ; the same as above.
```

In summary, there are two standard forms that procedure argument lists follow:

```
procedure(functionname([var1 var2 ...]    [@optional opt1 opt2 ...]    [@rest r])    .    .)
```

```
procedure(functionname([var1 var2 ...]    [@key key1 key2 ...]    [@rest r])    .    .)
```

#### Example

```
procedure( cube(x) x**3 )    ; Defines a function to compute the=> cube                      ; cube of a number using procedure.
```

`cube( 3 ) => 27`

```
defun( cube (x) x**3 )       ; Defines a function to compute the => cube                      ; cube of a number using defun.
```

The following function computes the factorial of its positive integer argument by recursivelycalling itself.

```
procedure( factorial(x)    if( (x == 0) then 1    else x * factorial(x - 1)))=> factorial
```

```
defun( factorial (x)    if( (x == 0) then 1    else x * factorial( x - 1)))=> factorial
```

`factorial( 6 )=> 720`

#### Reference

[defun](#1039449 "Function and Program Structure"), [let](#1047251 "Function and Program Structure"), ,

### procedurep

`procedurep( g_obj ) => t | nil`

#### Description

Checks if an object is a procedure, or function, object.

A procedure may be a function object defined in SKILL or SKILL++, or system primitives. Notethat symbols are not considered procedures even though they may have function bindings.

#### Arguments

|  |
| --- | ---
| `g_obj` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | The argument is a procedure, or function, object.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

```
(procedurep 123 )            => nil(procedurep (getd 'plus))    => t(procedurep 'plus)           => nil
```

#### Reference

[defun](#1039449 "Function and Program Structure"), , ,

### prog

`prog( l_localVariables [ [ s_label ] g_expr1 ] ... )=> g_result | nil`

#### Description

Allows for local variable bindings and permits abrupt exits on control jumps. This is a syntaxform.

The first argument to`prog` is a list of variables declared to be local within the context of the `prog`. The expressions following the `prog` are executed sequentially unless one of the control transfer statements such as `go` or `return` is encountered. A `prog` evaluates to the value of `nil` if no `return` statement is executed and control simply "falls through" the `prog` after the last expression is executed. If a `return` is executed within a `prog`, the `prog` immediately returns with the value of the argument given to the `return` statement.

Any statement in a`prog` can be preceded by a symbol that serves as a label for the statement. Unless multiple return points are necessary or you are using the `go` function, a faster construct for binding local variables, `let`, should be used over `prog`.

#### Arguments

|  |
| --- | ---
| `l_localVariables` | List of variables local to`prog`.
|  |
| --- | ---
| `s_label` | Labels a statement inside a`prog`; labels can be defined only for statements at the top level. Statements nested inside another statement cannot be labelled unless the surrounding statement is itself a `prog`.
|  |
| --- | ---
| `g_expr1` | Any SKILL expression to be evaluated inside the`prog`.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of the`return` statement if one is used.
|  |
| --- | ---
| `nil` | Otherwise always returns`nil`.
#### Example

`x = "hello"=> "hello"`

```
prog( (x y)                ; Declares local variables x and y.    x = 5                  ; Initialize x to 5.    y = 10                 ; Initialize y to 10.    return( x + y ))=> 15
```

`x=> "hello"                ; The global x keeps its original value.`

#### Reference

`let, , , progn`

### prog1

`prog1( g_expr1 [ g_expr2 ... ] ) => g_result`

#### Description

Evaluates expressions from left to right and returns the value of the*first* expression. This is a syntax form.

#### Arguments

|  |
| --- | ---
| `g_expr1` | Any SKILL expression.
|  |
| --- | ---
| `g_expr2` | Any SKILL expression.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of the first expression,`g_expr1`.
#### Example

`prog1(    x = 5    y = 7 )=> 5`

Returns the value of the first expression.

#### Reference

`, prog2, progn`

### prog2

`prog2( g_expr1 g_expr2 [ g_expr3... ] ) => g_result`

#### Description

Evaluates expressions from left to right and returns the value of the*second* expression. This is a syntax form.

#### Arguments

|  |
| --- | ---
| `g_expr1` | First SKILL expression.
|  |
| --- | ---
| `g_expr2` | Second SKILL expression.
|  |
| --- | ---
| `g_expr3` | Additional SKILL expressions.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of the second expression,`g_expr2`.
#### Example

`prog2(     x = 4     p = 12    x = 6 )=> 12`

Returns the value of the second expression.

#### Reference

`, prog1, progn`

### progn

`progn( g_expr1 ... ) => g_result`

#### Description

Evaluates expressions from left to right and returns the value of the last expression. This is asyntax form.

`progn` is useful for grouping a sequence of expressions into a single expression. As a shorthand notation for `progn`, use braces ({ }) to group multiple expressions into a single expression.

#### Arguments

|  |
| --- | ---
| `g_expr1` | Any SKILL expression.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of the last expression evaluated.
#### Example

`progn(     println("expr 1")     println("expr 2") )"expr 1" "expr 2"=> nil`

The value of`println` is `nil`. The following example uses braces.

`{   println("expr 1")     println("expr 2")    2 + 3}"expr 1" "expr 2"5`

#### Reference

,[let](#1047251 "Function and Program Structure"), , [prog1](#1041321 "Function and Program Structure"), [prog2](#1041348 "Function and Program Structure")

### putd

`putd( s_functionName u_functionDef ) => u_functionDef`

#### Description

Assigns a new function binding, which must be a function, a `lambda` expression, or `nil`, to a function name. If you just want to define a function, use `procedure` or `defun`.

Assigns the function definition of `u_functionDef` to `s_functionName`. This is different from `alias`, which does a macro expansion when evaluated. You can undefine a function name by setting its function binding to `nil`. A function name can be write-protected by the system to protect you from unintentional name collisions, in which case you cannot change the function binding of that function name using `putd`.

**Note:** If you just want to define a function, use`procedure` or `defun`.

#### Arguments

|  |
| --- | ---
| `s_functionName` | Name of the function.
|  |
| --- | ---
| `u_functionDef` | New function binding, which must be a binary function, a`lambda` expression, or `nil`.
#### Value Returned

|  |
| --- | ---
| `u_functionDef` | Function definition, which is either a binary function or a SKILLexpression.
#### Example

`putd( 'mySqrt getd( 'sqrt )) => lambda:sqrt`

Assigns the function`mySqrt` the same definition as `sqrt`.

`putd( 'newFn lambda( () println( "This is a new function" )))=> funobj:0x3cf088`

Assigns the symbol`newFn` a function definition that prints the string`This is a new``function` when called.

#### Reference

, ,

### setFnWriteProtect

`setFnWriteProtect( s_name ) => t | nil`

#### Description

Prevents a named function from being redefined.

If`s_name` has a function value, it can no longer be changed. If it does not have a function value but does have an autoload property, the autoload is still allowed. This is treated as a special case so that all the desired functions can be write-protected first and autoloaded as needed.

#### Arguments

|  |
| --- | ---
| `s_name` | Name of the function.
#### Value Returned

|  |
| --- | ---
| `t` | The function is now write protected.
|  |
| --- | ---
| `nil` | If the function is already write protected.
#### Example

Define a function and set its write protection so it cannot be redefined.

```
procedure( test() println( "Called function test" ))setFnWriteProtect( 'test ) => t
```

`procedure( test() println( "Redefine function test" ))`

`*Error* def: function name already in use and cannot be     redefined - test`

`setFnWriteProtect( 'plus ) => nil`

Returns`nil` because the `plus` function is already write protected.

#### Reference

,

### setVarWriteProtect

`setVarWriteProtect( s_name ) => t | nil`

#### Description

(SKILL mode only) Sets the write-protection on a variable to prevent its value from beingupdated. Does not work in SKILL++ mode.

Use this function in SKILL mode only when the variable and its contents are to remainconstant.

* If the variable has a value, it can no longer be changed.

* If the variable does not have a value, it cannot be used.

* If the variable holds a list or other data structure as its value, it is assumed that thecontents will not be changed. If you try to update the contents, the behavior is unspecified.

In SKILL++ mode, use`setFnWriteProtect` instead.

#### Arguments

|  |
| --- | ---
| `s_name` | Name of variable to be write-protected.
#### Value Returned

|  |
| --- | ---
| `t` | Variable is write protected.
|  |
| --- | ---
| `nil` | Variable was already write protected.
#### Example

```
y = 5                                ; Initialize the variable y.setVarWriteProtect( 'y )=> t         ; Set y to be write protected.setVarWriteProtect( 'y )=> nil       ; Already write protected.
```

```
y = 10                               ; y is write protected.*Error* setq: Variable is protected and cannot be                     assigned to - y
```

### unalias

`unalias( s_aliasName1 ... )=> l_result`

#### Description

Undefines the aliases specified in an argument list and returns a list containing the aliasesundefined by the call. This is `nlambda` function also works in SKILL++ mode.

* ***Use alias for interactive command entry only and never in programs.***

#### Arguments

|  |
| --- | ---
| `s_aliasName1` | Symbol name of the alias.
#### Value Returned

|  |
| --- | ---
| `l_result` | List of the aliases removed.
#### Example

`alias path getSkillPath => path`

Aliases`path` to the `getSkillPath` function.

`unalias path => (path)`

`Removes path as an alias.`

### unwindProtect

`unwindProtect( [ g_protectedForm ] [ g_cleanupForm ]) => g_result`

#### Description

Evaluates the function`g_protectedForm` and executes the SKILL expression in `g_cleanupForm` before exit.

#### Arguments

|  |
| --- | ---
| `g_protectedForm` | Name of the function to be evaluated.
| `g_cleanupForm` | Any valid SKILL expression.
#### Value Returned

|  |
| --- | ---
| `g_result` | Result of the expression evaluated.
#### Example

```
(unwindProtect (undefFun) (printf "cleanup form called here\n"))*Error* eval: undefined function - undefFun cleanup form called here
```

### warn

`warn( t_formatString [ g_arg1 ... ] ) => nil`

#### Description

Buffers a warning message with given arguments inserted using the same formatspecification as `sprintf`, `printf`, and `fprintf`.

After a function returns to the top level, the buffered warning message is printed in theCommand Interpreter Window. Arguments to `warn` use the same format specification as `sprintf`, `printf`, and `fprintf`.

This function is useful for printing SKILL warning messages in a consistent format. You canalso suppress a message with a subsequent call to `getWarn`.

#### Arguments

|  |
| --- | ---
| `t_formatString` | Characters to print verbatim in the warning message with formatspecifications prefixed by the percent (%) sign.
|  |
| --- | ---
| `g_arg1 ...` | Optional arguments following the format string, which are printedaccording to their corresponding format specifications.
#### Value Returned

|  |
| --- | ---
| `nil` | Always returns`nil`.
#### Example

```
arg1 = 'failwarn( "setSkillPath: first argument must be a string or list of strings - %s\n" arg1)=> nil*WARNING* setSkillPath: first argument must be a string or list of strings - fail
```

#### Reference

, , ,




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
