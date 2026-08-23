<!--
source: sklangref/funcprog.md
part: 1/2
estimated_tokens: 13479
-->

### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

13
==

Function and Program Structure
==============================

### addDefstructClass

`addDefstructClass( s_name ) => u_classObject`

#### Description

Creates a class for the`defstruct`.

By default, an instance of a`defstruct` does not have a class. You cannot use `Instance` to instantiate this class. Use the instantiation function created by `defstruct`.

Using`addDefstructClass` to create a class for a `defstruct` allows you to define methods for a `defstruct`.

#### Arguments

|  |
| --- | ---
| `s_name` | The name of the`defstruct`.
#### Value Returned

|  |
| --- | ---
| `u_classObject` | The class object.
#### Example

`defstruct( card rank suit ) => t`

```
x = _card( ?rank 8 ?suit "spades" )=> array[4]:3897312type( x )                    => cardfindClass( 'card )           => nilclassOf( x )                 => niladdDefstructClass( card )    => funobj:0x1c98f8className( classOf( x ))     => card
```

#### Reference

`Instance`

### alias

`alias( s_aliasName s_functionName )=> s_aliasName`

#### Description

Defines a symbol as an alias for a function. This is an `nlambda` function.

Defines the`s_aliasName` symbol as an alias for the `s_functionName` function, which must already have been defined. The `alias` function does not evaluate its arguments.

* ***Use alias only to speed up interactive command entry and never inprograms.***

#### Arguments

|  |
| --- | ---
| `s_aliasName` | Symbol name of the alias.
|  |
| --- | ---
| `s_functionName` | Name of the function you are creating an alias for.
#### Value Returned

|  |
| --- | ---
| `s_aliasName` | Name of the alias.
#### Example

`alias path getSkillPath => path`

Aliases`path` to the `getSkillPath` function.

`alias e edit => e`

Aliases`e` to the `edit` function.

### apply

`apply( slu_func [g_arg ...]l_args)=> g_result`

#### Description

Applies the given function to the given argument list.

`apply` takes two or more arguments. The first argument must be the name of a function, or a function object, or a list containing a `lambda`/`nlambda`/`macro` expression. The remainder of the arguments are used to construct the list of arguments passed to the function specified by the first argument; the `g_arg` arguments are individual arguments, which are prepended to the `l_args` argument to create a combined list of arguments.

**Note:** The last argument to apply must always be a list.

The argument list`l_args` is bound to the formal arguments of `slu_func` according to the type of function. For `lambda` functions the length of `l_args` should match the number of formal arguments, unless keywords or optional arguments exist. For `nlambda` and `macro` functions, `l_args` is bound directly to the single formal parameter of the function.

**Note:** If`slu_func` is a macro, `apply` evaluates it only once, that is, it expands it and returns the expanded form, but does not evaluate the expanded form again (as `eval` does).

#### Arguments

|  |
| --- | ---
| `slu_func` | Name of the function.
|  |
| --- | ---
| `g_arg` | Optional arguments that are prepended to`l_args` to create a combined list of arguments.
|  |
| --- | ---
| `l_args` | Argument list to apply to the function.
#### Value Returned

|  |
| --- | ---
| `g_result` | Returns the result of applying the function to the givenarguments.
#### Example

`apply('plus (list 1 2) )          ; Apply plus to its arguments.=> 3`

```
procedure( sumTail(l) apply( 'plus cdr(l))) => sumTail                        ;Define a proceduresumTail( '(1 2 3))=> 5
```

`apply('plus list(1 2 3 4)) ; adds 1, 2, 3 and 4`

`=> 10`

`apply('plus 1 2 list(3 4)) ; adds 1, 2, 3 and 4.`

`=> 10`

#### Reference

,

### argc

`argc() => n | 0 | -1 | -2`

#### Description

Returns the number of arguments passed to a SKILL script. Used to enhance the SKILLscript environment. Note that this function works only for scripting with SKILL standalone executable (skill).

#### Value Returned

|  |
| --- | ---
| `n` | `n`arguments were passed (`n` is an integer).
1. No arguments were passed, but`argv(0)` has a value.

|  |
| --- | ---
| `-1` | Argument list is`nil` (no arguments passed, and `argv(0)`is `nil`). This can occur when using SKILL interactively.
|  |
| --- | ---
| `-2` | Error caused by a problem with the argument list property.
#### Example

Assume that arguments passed to a SKILL script file are`(`"`my.il`""`1st`""`2nd`""`3rd`"`):`

`argc() => 3`

An example using a SKILL executable:

`$ skill -V`

> `@(#)$CDS: skill version 07.02 09/19/2007 09:08 (cat61lnx) $`

`$ cat /tmp/foo.il`

> `(printf "argc is %d, argv[0] is %s, argv is %L\n" (argc) (argv 0) (argv))`

`$ skill /tmp/foo.il -someArg -someArg2`

> `argc is 2, argv[0] is /tmp/foo.il, argv is ("-someArg" "-someArg2")`

#### Reference

`argv`

### argv

`argv( [ x_int ] ) => g_result`

#### Description

Returns the arguments passed to a SKILL script. Used to enhance the SKILL scriptenvironment. Note that this function works only for scripting with SKILL standalone executable (skill).

#### Arguments

|  |
| --- | ---
| `x_int` | Optional argument; it must be a positive integer.
#### Value Returned

|  |
| --- | ---
| `g_result` | The return value depends on the arguments passed.
.

|  |
| --- | ---
| Argument | Returned
| `argv( )` | List of all arguments (list of strings or`nil`).
| `argv(0)` | Name of the calling script.
| `argv(``n``)` | `n`th argument as a string or `nil` if there is no `n`th argument.
#### Example

Assume that arguments passed to a SKILL script file are`("my.il" "1st" "2nd"``"3rd")`:

`argv()  => ("1st" "2nd" "3rd")argv(0) => "my.il" argv(1) => "1st"argv(4) => nil`

An example using a SKILL executable:

`$ skill -V`

> `@(#)$CDS: skill version 07.02 09/19/2007 09:08 (cat61lnx) $`

`$ cat /tmp/foo.il`

> `(printf "argc is %d, argv[0] is %s, argv is %L\n" (argc) (argv 0) (argv))`

`$ skill /tmp/foo.il -someArg -someArg2`

> `argc is 2, argv[0] is /tmp/foo.il, argv is ("-someArg" "-someArg2")`

#### Reference

### begin

```
SKILL modebegin( g_exp1 [ g_exp2 ... g_expN ] ) => g_resultSKILL++ modebegin(     def1     [ def2 ...         defN ] ) => g_result
```

#### Description

In the SKILL mode,`begin` is a syntax form used to group a sequence of expressions. Evaluates expressions from left to right and returns the value of the last expression. Equivalent to `progn`. This expression type is used to sequence side effects such as input and output. Whereas, in the SKILL++ mode, `begin` is a syntax form used to group either a sequence of expressions or a sequence of definitions.

`begin( exp1 [exp2 ... expN] )`

The expressions are evaluated sequentially from left to right, and the value of the lastexpression is returned. This expression type is used to sequence side effects such as input and output.

`begin( [def1 def2 ... defN] )`

This form is treated as though the set of definitions is given directly in the enclosing context.It is most commonly found in macro definitions.

#### Arguments

|  |
| --- | ---
| `g_exp1`, `g_exp2`, `g_expN`Arbitrary expressions. |
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of the last expression,`g_expN`.
#### Example 1

The following example describes the begin function in the SKILL mode.

`begin( x = 1 y = 2 z = 3 )=> 3`

#### Example 2

The following example describes the begin function in the SKILL++ mode.

```
begin( x = 1 y = 2 z = 3 ) => 3begin( define( x 1 ) define( y 2 ) define( z 3 ) ) => z
```

#### Reference

`progn`

### clearExitProcs

`clearExitProcs( ) => t`

#### Description

Removes all registered exit functions (takes no arguments).

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `t` | Always returns `t`.
#### Example

clearExitProcs( )=> t

### declareLambda

`declareLambda( s_name1 ... s_nameN ) => s_nameN`

#### Description

Tells the evaluator that certain (forward referenced) functions are of`lambda` type (as opposed to `nlambda` or `macro`).

Declares`s_name1 ... s_nameN` as procedures (`lambdas`) to be defined later. This is much like C's "extern" declarations. Because the calling sequence for `nlambdas` is quite different from that of `lambdas`, the evaluator needs to know the function type in order to generate more efficient code. Without the declarations, the evaluator can still handle things properly, but with some performance penalty. The result of evaluating this form is the last name given (in addition to the side-effects to the evaluator).

This (and`declareNLambda`) form has effect only on undefined function names, otherwise it is ignored. Also, when the definition is provided later, if it is of a different function type (for example, declared as `lambda` but defined as `nlambda`) a warning will be given and the definition is used regardless of the declaration. In this case (definition is inconsistent with declaration), if there is any code already loaded that made forward references to these names, that part of code should be reloaded in order to use the correct calling sequence.

#### Arguments

|  |
| --- | ---
| `s_name1` | One or more function names.
#### Value Returned

|  |
| --- | ---
| `s_nameN` | The last name in the arguments.
#### Example

`declareLambda(fun1 fun2 fun3) => fun3`

#### Reference

### declareNLambda

`declareNLambda( s_name1 ... s_nameN ) => s_nameN`

#### Description

Tells the evaluator that certain (forward referenced) functions are of`nlambda` type (as opposed to `lambdas` or `macros`).

Declares`s_name1 ... s_nameN` as nprocedures (`nlambdas`) to be defined later. This is much like C's "extern" declarations. Because the calling sequence for `nlambdas` is quite different from that of `lambdas`, the evaluator needs to know the function type in order to generate more efficient code. Without the declarations, the evaluator can still handle things properly, but with some performance penalty. The result of evaluating this form is the last name given (in addition to the side-effects to the evaluator).

#### Arguments

|  |
| --- | ---
| `s_name1` | One or more function names.
#### Value Returned

|  |
| --- | ---
| `s_nameN` | The last name in the arguments.
#### Example

`declareNLambda(nfun1 nfun2 nfun3) => nfun3`

#### Reference

### declareSQNLambda

`declareSQNLambda( s_functionName ... ) => nil`

#### Description

Declares the given nlambda functions to be*solely-quoting nlambdas*.

This is an`nlambda` function. The named functions are defined as `nlambdas` only to save typing the explicit quotes to the arguments.

The compiler has been instructed to allow the calling of these kinds of`nlambdas` from SKILL++ code without giving a warning message.

All the debugging commands have been declared as`SQNLambdas` already.

#### Arguments

|  |
| --- | ---
| `s_functionName` | Function to be declared as a*solely-quoting* *nlambda*.
#### Value Returned

|  |
| --- | ---
| `nil` | Always. This function is for side-effects only.
#### Example

declareSQNLambda( step next stepout ) => nil

### defglobalfun

`defglobalfun( s_funcName ( l_formalArglist ) g_expr1 ... )=> s_funcName`

#### Description

Defines a global function with the name and formal argument list you specify.

**Note:** The functions that you define using`defglobalfun` are defined within a lexical scope, but are globally accessible.

For`defglobalfun` there must be white space between `s_funcName` and the open parenthesis. Expressions within the function can reference any variable on the formal argument list or any global variable defined outside the function. If necessary, local variables can be declared using the `let` function.

#### Arguments

|  |
| --- | ---
| `s_funcName` | Name of the function you are defining.
|  |
| --- | ---
| `l_formalArglist` | Formal argument list.
|  |
| --- | ---
| `g_expr1` | Expression or expressions to be evaluatedwhen `s_funcName` is called.
#### Value Returned

|  |
| --- | ---
| `s_funcName` | The name of the function being defined.
#### Example

Define two global functions,`test_set` and `test_get` using `defglobalfun` and that reference a lexical variable `secret_val:`

```
toplevel 'ilsILS-<2> (let ((secret_val 1))(defglobalfun test_set (x) secret_val  = x)(globalProc test_get() secret_val))
```

`ILS-<2> test_get()=> 1`

`ILS-<2> test_set(2)=> 2`

ILS-<2> test\_get()
=> 2

### define

```
define( s_var g_expression ) => s_vardefine( ( s_var [ s_formalVar1 ... ] ) g_body ... ) => s_var
```

#### Description

(SKILL++ mode only) Is a syntax form used to provide a definition for a global or local variable.The `define` syntax form has two variations.

Definitions are allowed only at the top-level of a program and at the beginning or within thebody of following syntax forms: `define` (another call to `define`), `lambda`, `let`, `letrec`, `defun`, and `letseq`. If occurring within a body, the `define`'s variable is local to the body.

* Top Level Definitions

> A definition occurring at the top level is equivalent to an assignment statement to a globalvariable.

* Internal Definitions

> A definition that occurs within the body of a syntax form establishes a local variablewhose scope is the body.

* **define(**`s_var``g_expression` **)**

> This is the primary variation. The other variation can be rewritten in this form. Theexpression is evaluated in enclosing lexical environment and the result is assigned or bound to the variable.

* **define( (**`s_var` **[**`s_formalVar1` **...] )** `g_body` **)**

> In this variation, body is a sequence of one or more expressions optionally preceded byone or more nested definitions. This form is equivalent to the following define

`define( s_var         lambda(( [sformalVar1 ...] ) g_body ...)`

#### Example

* First variation

> `define( x 3 ) => xdefine( addTwoNumbers lambda( ( x y ) x+y ) ) => addTwoNumbers`

* Second variation

> `define( ( addTwoNumbers x y ) x+y ) => addTwoNumbers`

* Local definition using second variation

> ```
> let( (( x 3 ))    define( ( add y ) x+y ) ; define    add( 5 )    )                       ; let => 8
> ```

> Defines a local function`add`, then invokes it.

> ```
> let( ()        define( ( f n )            if( n > 0 then n*f(n-1) else 1 ) ; if            )                                ; define        f( 5 )    )                                        ; let => 120
> ```

> Declares a single recursive local function`f` that computes the factorial of its argument. The `let` expression returns the factorial of 5.

#### Reference

,[let](#1047251 "Function and Program Structure"), [letrec](#1047309 "Function and Program Structure"),[letseq](#1040628 "Function and Program Structure")

### defmacro

`defmacro( s_macroName ( l_formalArglist ) g_expr1 ... )=> s_macroName`

#### Description

Defines a macro which can take a list of formal arguments including`@optional`, `@key`, and `@rest` (instead of the more restrictive format as required by using `mprocedure`).

The actual arguments will be matched against the formals before evaluating the body.

#### Arguments

|  |
| --- | ---
| `s_macroName` | Name of the macro you are defining.
|  |
| --- | ---
| `l_formalArglist` | Formal argument list.
|  |
| --- | ---
| `g_expr1` | Expression or expressions to be evaluated.
#### Value Returned

|  |
| --- | ---
| `s_macroName` | Returns the name of the macro being defined.
#### Example

`` defmacro( whenNot (cond @rest body)    `(if ! ,cond then ,@body) )=> whenNot ``

```
expandMacro( '(whenNot x > y z = f(y) x*z) )=> if(!(x > y) then (z = (f y))(x * z))
```

`whenNot(1 > 2 "hello" 1+2)=> 3`

#### Reference

, ,

### defun

`defun( s_funcName ( l_formalArglist ) g_expr1 ... )=> s_funcName`

#### Description

Defines a function with the name and formal argument list you specify. This is a syntax form.

The body of the procedure is a list of expressions to be evaluated one after another when`s_funcName` is called. There must be no white space between `defun` and the open parenthesis that follows.

However, for`defun` there must be white space between `s_funcName` and the open parenthesis. This is the only difference between the `defun` and `procedure` forms. `defun` has been provided principally so that you can your code appear more like other LISP dialects.

Expressions within a function can reference any variable on the formal argument list or anyglobal variable defined outside the function. If necessary, local variables can be declared using the `let` function.

#### Arguments

|  |
| --- | ---
| `s_funcName` | Name of the function you are defining.
|  |
| --- | ---
| `l_formalArglist` | Formal argument list.
|  |
| --- | ---
| `g_expr1` | Expression or expressions to be evaluatedwhen `s_funcName` is called.
#### Value Returned

|  |
| --- | ---
| `s_funcName` | The name of the function being defined.
#### ARGUMENT LIST PARAMETERS

Several parameters provide flexibility in procedure argument lists. These parameters arereferred to as @ ("at" sign) options. The parameters are `@rest`, `@optional`, `@key`, and `@aux`. See [`procedure`](#procedure "Function and Program Structure") for a detailed description of these argument list parameters.

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
procedure( factorial(x)    if( (x == 0) then 1    else x * factorial(x - 1))) => factorial
```

```
defun( factorial (x)    if( (x == 0) then 1    else x * factorial( x - 1))) => factorial
```

`factorial( 6 )=> 720`

#### Reference

[let](#1047251 "Function and Program Structure")

### defUserInitProc

```
defUserInitProc( t_contextName s_procName [ autoInit ])=> ( t_contextName s_procName )
```

#### Description

Registers a user-defined function that the system calls immediately after autoloading acontext.

Lets you customize existing Cadence contexts. In the general case, most Cadence-suppliedcontexts have internally defined an initialization function through the `defInitProc` function. This function defines a second initialization function, called after the internal initialization function, thereby allowing you to customize on top of Cadence supplied contexts. This is best done in the `.cdsinit` file.

#### Arguments

|  |
| --- | ---
| `t_contextName` | Name of context file to load.
|  |
| --- | ---
| `s_procName` | Function to be called when context file is loaded.
|  |
| --- | ---
| `[autoInit]` |
#### Value Returned

|  |
| --- | ---
| `((``t_contextName s_procName``))`Always returns an association list when set up. Note that the function is not actually called at this point, but is called when the `t_contextName` context is loaded. |
#### Example

`defUserInitProc( "myContext" 'initMyContext)=> (("myContext" initMyContext))`

#### Reference

[`defInitProc`](../skdevref/context.html#defInitProc), `callIni``tProc`

### destructuringBind

`destructuringBind( l_lambdaList l_expression [g_body] ) => g_result`

#### Description

Enables you to bind variables in a lambda-list to the values of these variables. The list ofvalues is obtained by evaluating the `l_expression`. The `destructuringBind` macro then evaluates the `g_body` form.

**Note:** `destructuringBind` does not check the correctness of `l_lambdaList`.

#### Arguments

|  |
| --- | ---
| `l_lambdaList` | A lambda list.
| `l_expression` | An expression that is evaluated and its result is assigned orbound to the variables in the lambda list.
| `g_body` | A sequence of one or more expressions.
#### Value Returned

|  |
| --- | ---
| `g_result` | Result of evaluation.
#### Example

(destructuringBind (a b @optional (c 1)) '(1 2)
        printf("a=%L b=%L c=%L\n" a b c))
=> a=1 b=2 c=1

### err

`err( [ g_value ] ) => none`

#### Description

Causes an error.

If this error is caught by an`errset`*,* `nil`is returned by that `errset`. However, if the optional `g_value` argument is given then `g_value` is returned from the `errset` and can be used to identify which `err` signaled the error. The `err` function never returns a value.

#### Arguments

|  |
| --- | ---
| `g_value` | SKILL object that becomes the return value for`errset`.
#### Value Returned

|  |
| --- | ---
| Never returns a value. |
#### Example

```
errset( err( 'ErrorType))        => (ErrorType)errset.errset                    => nil
```

```
procedure( test( x )    if( (equal errset( foo( x )) '(throw))        then println( "Throw caught" )        else if( errset.errset println( "Error: divide by                    zero"))))=> testprocedure( foo( x )    if( (equal (4 / x) 1)         then err( 'throw )         else println( x )))=> foo
```

```
test( 4 ) => nil         ; Prints Throw caughttest( 2 ) => nil         ; Prints 2test( 0 ) => nil         ; Prints Error: divide by zero
```

#### Reference

`, error`

### error

`error( [ S_message1 [ S_message2 ] ... ] ) => none`

#### Description

Prints error messages and calls`err`.

Prints the`S_message1` and `S_message2` error messages if they are given and then calls `err`, causing an error. The first argument can be a format string, which causes the rest of the arguments to be printed in that format.

#### Arguments

|  |
| --- | ---
| `S_message1` | Message string or symbol.
|  |
| --- | ---
| `S_message2` | More message strings or symbols. Note that more than twoarguments should be given only if the first argument is a format string.
#### Value Returned

Prints the`S_message1` and `S_message2` error messages if they are given and then calls `err`, causing an error. `error` never returns.

#### Example

`error( "myFunc" "Bad List")`

Prints`*Error* myFunc: Bad List`

`error( "bad args - %s %d %L" "name" 100 '(1 2 3) )`

Prints`*Error* bad args - name 100 (1 2 3)`

`errset( error( "test" ) t) => nil`

Prints out`*Error* test` and returns `nil`.

### errset

`errset( g_expr [ g_errprint ] ) => l_result | nil`

#### Description

Encapsulates the execution of an expression in an environment safe from the errormechanism. This is a syntax form.

If an error occurs in the evaluation of the given expression, control always returns to thecommand following the `errset` instead of returning to the nearest toplevel. If `g_errprint` is non-`nil`, error messages are issued; otherwise they are suppressed. In either case, information about the error is placed in the `errset` property of the `errset` symbol. Programs can therefore access this information with the `errset.errset` construct after determining that `errset` returned `nil`.

#### Arguments

|  |
| --- | ---
| `g_expr` | Expression to be evaluated; while evaluating it, any errors causeimmediate return from the `errset`.
|  |
| --- | ---
| `g_errprint` | Flag to control the printout of error messages. If`t` then prints the error message encountered in `errset`, defaults to `nil`.
#### Value Returned

|  |
| --- | ---
| `l_result` | List with value from successful evaluation of`g_expr`.
|  |
| --- | ---
| `nil` | An error occurred.
#### Example

```
errset(1+2)          => (3)errset.errset        => nilerrset(sqrt('x))     => nil
```

Because`sqrt` requires a numerical argument.

`errset.errset=> ("sqrt" 0 t nil ("*Error* sqrt: can't handle sqrt(x)...))`

#### Reference

`, error`

### errsetstring

`errsetstring( t_string [ g_errprint ] [ s_langMode ] ) => l_value | nil`

#### Description

Reads and evaluates an expression stored in a string. Same as`evalstring` except that it calls `errset` to catch any errors that might occur during the parsing and evaluation.

If an error has occurred,`nil` is returned, otherwise a list containing the value of the evaluation is returned. Should an error occur, it is stored in `errset.errset`. If `errprint` is non-`nil`, error messages are printed out; otherwise they are suppressed.

#### Arguments

|  |
| --- | ---
| `t_string` | String to be evaluated.
|  |
| --- | ---
| `g_errprint` | Flag for controlling the printout of error messages. If`t`, then prints the error message encountered in `errset`. Defaults to `nil`.
|  |
| --- | ---
| `s_langMode` | Must be a symbol. Valid values:
|  |
| --- | ---
| `'ils` | Evaluates the given string in SKILL++ mode.
| `'il` | Evaluates the given string in SKILL mode. This is thedefault.
#### Value Returned

|  |
| --- | ---
| `l_value` | List with the value from successful evaluation of`t_string`.
|  |
| --- | ---
| `nil` | An error occurs.
#### Example

`errsetstring("1+2")               => (3)errsetstring("1+'a")              => nil`

Returns*nil* because an error occurred.

`errsetstring("1+'a" t)         => nil`

Prints out error message:

\*Error\* plus: can't handle (1+a)...

#### Reference

,[error](#1039618 "Function and Program Structure"), , [evalstring](#1039846 "Function and Program Structure")

### eval

`eval( g_expression [ e_environment ] ) => g_result`

#### Description

Evaluates an argument and returns its value. If an environment argument is given,`g_expression` is treated as SKILL++ code, and the expression is evaluated in the given (lexical) environment. Otherwise `g_expression` is treated as SKILL code.

This function gives you control over evaluation. If the optional second argument is notsupplied, it takes `g_expression` as SKILL code. If an environment argument is given, it treats `g_expression` as SKILL++ code, and evaluates it in the given (lexical) environment.

For SKILL++'s`eval`, if the given environment is not the top-level one, the effect is like evaluating `g_expression` within a `let` construct for the bindings in the given environment, with the following exception:

If`g_expression` is a definitional form (such as `(define ...)`), it is treated as a global definition instead of local one. Therefore any variables defined will still exist after executing the `eval` form.

#### Arguments

|  |
| --- | ---
| `g_expression` | Any SKILL expression.
|  |
| --- | ---
| `e_environment` | If this argument is given, SKILL++ semantics is assumed. Theforms entered will be evaluated within the given (lexical) environment.
#### Value Returned

|  |
| --- | ---
| `g_result` | Result of evaluating`g_expression`.
#### Example

`eval( 'plus( 2 3 ) )    => 5`

Evaluates the expression`plus(2 3)`.

`x = 5                    => 5eval( 'x )               => 5`

Evaluates the symbol`x` and returns the value of symbol `x`.

`eval( list( 'max 2 1 ) ) => 2`

`Evaluates the expression max(2 1).`

#### Reference

`evalstring,`

### evalstring

`evalstring( t_string [ s_langMode ] ) => g_value | nil`

#### Description

Reads and evaluates an expression stored ina string.

The resulting value is returned. Notice that`evalstring` does not allow the outermost set of parentheses to be omitted from the evaluated expression, as in `load` or in the top level.

#### Arguments

|  |
| --- | ---
| `t_string` | String containing the SKILL expression to be evaluated.
|  |
| --- | ---
| `s_langMode` | Must be a symbol. Valid values:
|  |
| --- | ---
| `'ils` | Evaluates the given string in SKILL++ mode.
| `'il` | Evaluates the given string in SKILL mode. This isthe default.
#### Value Returned

|  |
| --- | ---
| `g_value` | The value of the argument expression after evaluation.
|  |
| --- | ---
| `nil` | No form is read.
#### Example

`evalstring("1+2") => 3`

The`1+2` infix notation is the same as `(plus 1 2)`.

`evalstring("cons('a '(b c))") => (a b c)car '(1 2 3)                 => 1`

`evalstring("car '(1 2 3)")`

Signals that`car` is an unbound variable.

### expandMacro

`expandMacro( g_form ) => g_expandedForm`

#### Description

Expands one level of macro call for a form.

Checks if the given form `g_form` is a macro call and returns the expanded form if it is. Otherwise it returns the original argument. The macro expansion is done only once (one level). That is, if the expanded form is another macro call, it is not further expanded (unless another `expandMacro` is called with the expanded form as its argument).

#### Arguments

|  |
| --- | ---
| `g_form` | Form that can be a macro call.
#### Value Returned

|  |
| --- | ---
| `g_expandedForm` | Expanded form or the original form if the given argument is not amacro call.
#### Example

```
mprocedure( testMsg(args)    `(printf "test %s -- %L\n" ,(cadr args)progn(,@(cddr args))) )=> testMsg
```

```
expandMacro( '(testMsg "alpha1" y = f(x) g(y 100)) )=> printf("test %s -- %L\n" "alpha1"        progn((y = (f x)) (g y 100)))
```

#### Reference

,[defmacro](#1039383 "Function and Program Structure")

### fboundp

`fboundp( s_functionName ) => t | nil`

#### Description

Returns true (that is, some non-`nil` value) if the given name has a function binding.

This function returns a non-`nil` (that is, true) value if the given name has a function binding and returns `nil` otherwise. Note that `fboundp` examines the current function binding only and does not check for any potential definitions from autoloading. `fboundp` can be considered as an alias to `getd`.

#### Arguments

|  |
| --- | ---
| `s_functionName` | Name to check for function binding.
#### Value Returned

|  |
| --- | ---
| `t` | If there is a function binding for the given name.
|  |
| --- | ---
| `nil` | If no function binding exists currently for the name.
#### Example

```
fboundp( 'xyz ) => nil ;assuming there is no function named xyzfboundp( 'defstruct) => funobj:0x261108 ;a non-nil result
```

### flet

`flet( l_bindings [g_body] ) => g_result`

#### Description

Enables you to define local functions with LET semantics.

The names of functions defined by`flet` retain their local definitions only within the body of `flet`. Also, the function definition bindings are visible only in the body of `flet`. This helps in defining a local version of function which in turn calls the global version of the function with the same name but with different arguments.

**Note:** `flet` can only be used in Scheme mode.

#### Arguments

|  |
| --- | ---
| `l_bindings` | A list of variables or a list of the form`(s_variable``g_value)`.
| `g_body` | A sequence of one or more expressions.
#### Value Returned

|  |
| --- | ---
| `g_result` | Result of evaluation.
#### Example

`(flet ((foo (x) (list x)))(foo 1))`

=> (1)

### funcall

`funcall( slu_func [ arg ... ] ) => g_result`

#### Description

Applies the given function to the given arguments.

The first argument to`funcall` must be either the name of a function or a `lambda/``nlambda/macro` expression or a function object. The rest of the arguments are to be passed to the function.

The arguments`arg ...`are bound to the formal arguments of `s1u_func` according to the type of function. For `lambda` functions the length of `arg` should match the number of formal arguments, unless keywords or optional arguments exist. For `nlambda` and `macro` functions, `arg` are bound directly to the single formal parameter of the function.

**Note:** If`s1u_func` is a macro, `funcall` evaluates it only once, that is, it expands it and returns the expanded form, but does not evaluate the expanded form again (as `eval` does).

#### Arguments

|  |
| --- | ---
| `slu_func` | Name of the function.
|  |
| --- | ---
| `arg` | Arguments to be passed to the function.
#### Value Returned

|  |
| --- | ---
| `g_result` | The result of applying the function to the given arguments.
#### Example

`funcall( 'plus 1 2 )            ; Apply plus to its arguments.=> 3`

```
procedure( sum3(x y z) funcall( 'plus x y z) => sum3                         ;Define a proceduresum3(1 2 3)=> 6
```

### getd

`getd( s_functionName ) => g_definition | nil`

#### Description

Returns the function binding for a function name.

**Note:** This function is not needed in SKILL++ because functions are treated as regularvalues. Therefore you can simply use variable reference syntax to access any function binding.

#### Arguments

|  |
| --- | ---
| `s_functionName` | Name of the function.
#### Value Returned

|  |
| --- | ---
| `g_definition` | If the function is defined in SKILL, returns the function object thatthe procedure function associates with a symbol.
|  |
| --- | ---
|  | If the function is primitive, the binary definition is printed (seeexample below).
|  |
| --- | ---
| `nil` | No function definition exists.
#### Example

`getd( 'alias ) => nlambda:alias`

The function is primitive.

`getd( 'edit ) => funobj:0x24b478`

The function is written in SKILL.

### getFnWriteProtect

`getFnWriteProtect( s_name ) => t | nil`

#### Description

Checks if the given function is write-protected.

The value is`t` if `s_name` is write-protected; `nil` otherwise.

#### Arguments

|  |
| --- | ---
| `s_name` | Name of the function.
#### Value Returned

|  |
| --- | ---
| `t` | The function is write protected.
|  |
| --- | ---
| `nil` | The function is not write protected.
|  |
| --- | ---
|  | Signals an error if the function is not defined.
#### Example

getFnWriteProtect( 'strlen ) => t

### getFunType

`getFunType( u_functionObject ) => s_functionObject_type`

#### Description

Returns a symbol denoting the function type for a given function object.

Possible function types include`lambda`, `nlambda`, `macro`, `syntax`, or `primop`.

#### Arguments

|  |
| --- | ---
| `u_functionObject` | A function object.
#### Value Returned

|  |
| --- | ---
| `s_functionObject_type`Possible return values include `lambda`, `nlambda`, `macro`, `syntax`, or `primop`. |
#### Example

```
getFunType( getd( 'sin ))        => lambdagetFunType( lambda( (x y) x+y )) => lambdagetFunType( getd( 'breakpt ))    => nlambdagetFunType( getd( 'if ))         => syntaxgetFunType( getd( 'plus ))       => primop
```

#### Reference

[defmacro](#1039383 "Function and Program Structure"), , , , ,

### getVarWriteProtect

`getVarWriteProtect( s_name ) => t | nil`

#### Description

(SKILL mode only) Checks if a variable is write-protected. Does not work in SKILL++ mode.In SKILL++ mode, use `getFnWriteProtect` instead.

#### Arguments

|  |
| --- | ---
| `s_name` | Name of the variable to check.
#### Value Returned

|  |
| --- | ---
| `t` | The variable is write-protected.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`x = 5getVarWriteProtect( 'x ) => nil`

Returns`nil` if the variable `x` is not write protected.

#### Reference

,

### globalProc

`globalProc( s_funcName( l_formalArglist ) g_expr1 ... )=> s_funcName`

#### Description

Defines a global function using a formal argument list.

**Note:** The functions that you define using`globalProc` are defined within a lexical scope, but are globally accessible.

The body of`globalProc` is a list of expressions to be evaluated one after another when `s_funcName` is called. There must be no white space between `globalProc` and the open parenthesis that follows, nor between `s_funcName` and the open parenthesis of `l_formalArglist`. However, for `defglobalfun` there must be white space between `s_funcName` and the open parenthesis. This is the only difference between the two functions.

Expressions within a function can reference any variable on the formal argument list or anyglobal variable defined outside the function. If necessary, local variables can be declared using the `let` or `prog` functions.

#### Arguments

|  |
| --- | ---
| `s_funcName` | Name of the function you are defining.
|  |
| --- | ---
| `l_formalArglist` | Formal argument list.
|  |
| --- | ---
| `g_expr1` | Expression or expressions to be evaluated when `s_funcName` is called.
#### Value Returned

|  |
| --- | ---
| `s_funcName` | Name of the function being defined.
#### Example

Define two global functions,`test_set` and `test_get` using and `globalProc`that reference a lexical variable `secret_val:`

```
toplevel 'ilsILS-<2> (let ((secret_val 1))(defglobalfun test_set (x) secret_val  = x)(globalProc test_get() secret_val))ILS-<2> test_get()=> 1
```

`ILS-<2> test_set(2)=> 2`

ILS-<2> test\_get()
=> 2

### isCallable

`isCallable( s_function ) => t | nil`

#### Description

Checks if a function is defined or is autoloadable from a context.

#### Arguments

|  |
| --- | ---
| `s_function` | Name of a function.
#### Value Returned

|  |
| --- | ---
| `t` | The specified function is defined or is autoloadable.
|  |
| --- | ---
| `nil` | The specified function is not defined or is not autoloadable.
#### Example

```
isCallable( 'car) => t procedure( myFunction( x ) x+1)isCallable('myFunction) => t
```

#### Reference

, , ,

### isMacro

`isMacro( s_symbolName ) => t | nil`

#### Description

Checks if the given symbol denotes a macro.

#### Arguments

|  |
| --- | ---
| `s_symbolName` | Symbol to check.
#### Value Returned

|  |
| --- | ---
| `t` | The given symbol denotes a macro.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`(isMacro 'plus)     => nil(isMacro 'defmacro) => t`

#### Reference

[defmacro](#1039383 "Function and Program Structure")

### labels

`labels( l_bindings [g_body] ) => g_result`

#### Description

Enables you to define local functions with LET semantics.

`labels` is similar to the `flet` function except that in `labels`, the scope of name bindings for the functions defined by `labels` encompasses the function body as well as the function definitions themselves.

**Note:** `labels` can only be used in Scheme mode.

#### Arguments

|  |
| --- | ---
| `l_bindings` | A list of variables or a list of the form`(s_variable``g_value)`.
| `g_body` | A sequence of one or more expressions.
#### Value Returned

|  |
| --- | ---
| `g_result` | Result of evaluation.
#### Example

`(labels ((sum (x)`

`(if (plusp x)`

`x + (sum (sub1 x))`

`0)))`

`(sum 10))`

=> 55

### lambda

`lambda( ( s_formalArgument ) g_expr1 ... ) => U_result`

#### Description

Defines a function without a name. This is a syntax form.

The keywords`lambda` and `nlambda` allow functions to be defined without having names. This is useful for writing temporary or local functions. In all other respects `lambda` is identical to the `procedure` form.

#### Arguments

|  |
| --- | ---
| `s_formalArgument` | Formal argument for the function definition.
|  |
| --- | ---
| `g_expr1` | SKILL expression to be evaluated when the function is called.
#### Value Returned

|  |
| --- | ---
| `U_result` | A function object.
#### Example

`(lambda( (x y) x + y ) 5 6)=> 11`

### let

```
SKILL modelet( l_bindings g_expr1 ... ) => g_result SKILL++ modelet( [ s_var ]    (        ( s_var1 s_initExp1 )        ( s_var2 s_initExp2 )    ...    )body)=> g_result
```

#### Description

In the SKILL mode, this function provides a faster alternative to`prog` for binding local variables only. This is a `syntax` form. In the SKILL++ mode, this function declares a lexical scope. This includes a collection of local variables, as well as body expressions to be evaluated. This becomes a `named let` if the optional `s_var` is given.

The SKILL mode argument`l_bindings` is either a list of variables or a list of the form (`s_variable g_value`). The bindings list is followed by one or more forms to be evaluated. The result of the `let` form is the value of the last `g_expr`.

`let` is preferable to `prog` in all circumstances where a single exit point is acceptable, and where the `go` and `label` constructs are not required.

Whereas, the functions,`let`, `letseq`,and `letrec` give SKILL++ a block structure. The syntax of the three constructs is similar, but they differ in the regions they establish for their variable bindings.

* In a`let` expression, the initial values are computed before any of the variables become bound.

* In a`letseq` expression, the bindings and evaluations are performed sequentially.

* In a`letrec` expression, all the bindings are in effect while their initial values are being computed, thus allowing mutually recursive definitions.

Use the`let` form to declare a collection of local variables. You can provide an initialization expression for each variable. The order of evaluation of the initialization expressions is unspecified. Each variable has the body of the `let` expression as its lexical scope. This means that the initialization expressions should not cross-references to the other local variables.

In SKILL++ mode, local`defines` can appear at the beginning of the body of a `let`, `letseq`, or `letrec`form.

#### Arguments

|  |
| --- | ---
| `l_bindings` | (SKILL mode) Local variable bindings, can either be bound to avalue or `nil` (the default).
|  |
| --- | ---
| `g_expr1` | (SKILL mode) Any number of expressions.
|  |
| --- | ---
| `s_var` | (SKILL++ mode) When the optional`s_var` is given, this becomes a `named let`. A `named let` is just like an ordinary `let` except that `s_var` is bound within the body to a function whose formal arguments are the bound variables and whose body is `body`.
|  |
| --- | ---
| `s_var1` | (SKILL++ mode) Name of local variable. The variables are boundto fresh locations holding the result of evaluating the corresponding `initExp`.
|  |
| --- | ---
| `s_initExp` | (SKILL++ mode) Expression evaluated for the initial value. The`initExps` are evaluated in the current environment (in some unspecified order).
|  |
| --- | ---
| `body` | (SKILL++ mode)A sequence of one or more expressions. The expressions in (`body`) are evaluated sequentially in the extended environment. Each local variable binding has `body` as its scope.
#### Value Returned

|  |
| --- | ---
| `g_result` | The result of the last expression evaluated.
#### Example 1

The following example describes the use of the`let` function in the SKILL mode.

```
x = 5let( ((x '(a b c)) y)    println( y )               ; Prints nil.    x)=> (a b c)                     ; Returns the value of x.
```

```
procedure( test( x y )    let( ((x 6) (z "return string"))        if( (equal x y)            then z             else nil)))test( 8 6 )                    ; Call function test.=> "return string"             ; z is returned because 6 == 6.
```

#### Example 2

The following example describes the use of the`let` function in the SKILL++ mode.

`let( ( ( x 2 ) ( y 3 ) )    x*y     ) => 6`

```
let( ( ( x 2 ) ( y 3 ) )    let( (( z 4 ))        x + y + z         ) ; let    ) ; let=> 9
```

```
let( ( ( x 2 ) ( y 3 ) )    let( (( x 7 ) ( foo lambda( ( z ) x + y + z ) ) )        foo( 5 )        ) ; let    ) ; let=> 10                                              ;not 15
```

`let( ((x 2) (y 3))    define( f(z) x*z+y)    f(5)    )=> 13`

#### Reference

`letrec, letseq`

### letrec

```
letrec(    (        ( s_var1 s_initExp1 )        ( s_var2 s_initExp2 )    ...     )body) => g_result
```

#### Description

(SKILL++ mode) A`letrec` expression can be used in *SKILL++ mode only*. All the bindings are in effect while their initial values are being computed, thus allowing mutually recursive definitions. Use `letrec` to declare recursive local functions.

Recursive`let` form. Each binding of a variable has the entire `letrec` expression as its scope, making it possible to define mutually recursive procedures.

Use`letrec` when you want to declare recursive local functions. Each initialization expression can refer to the other local variables being declared, with the following restriction: each initialization expression must be executable without actually accessing any of those variables.

For example, a`lambda` expression satisfies this restriction because its body gets executed only when called, not when it's defined.

#### Arguments

|  |
| --- | ---
| `s_var` | Name of a local variable. The variables are bound to freshlocations holding undefined values. Each variable is assigned to the result of the corresponding `initExp`.
|  |
| --- | ---
| `s_initExp1` | Expressions evaluated for the initial value. The`initExps` are evaluated in the resulting environment (in some unspecified order).
|  |
| --- | ---
| `body` | A sequence of one or more expressions. The expressions inbody are evaluated sequentially in the extended environment.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of the last expression of`body`.
#### Example

```
letrec(     ( ;;; variable list        ( f             lambda( ( n )                 if( n > 0 then n*f(n-1) else 1                    ) ; if                ) ; lambda            ) ; f        ) ; variable list    f( 5 )    ) ; letrec => 120
```

This example declares a single recursive local function. The local function`f`computes the factorial of its argument. The `letrec` expression returns the factorial of 5.

### letseq

```
letseq(    (        ( s_var1 initExp1 )        ( s_var2 initExp2 )         ...    )body)=> g_result
```

#### Description

(SKILL++ mode) A`letseq` expression can be used *in SKILL++ mode only*. The bindings and evaluations are performed sequentially.

Use`letseq` to control the order of evaluation of the initialization expressions. `letseq` is similar to `let`, but the bindings are performed sequentially from left to right, and the scope of a binding indicated by (`var1 initExp1`) is that part of the `letseq` expression to the right of the binding. Thus the second binding is done in an environment in which the first binding is visible, and so on.

This form is equivalent to a corresponding sequence of nested let expressions. It is alsoequivalent to `let*` is the standard Scheme syntax. This function is equivalent of `let`\\*() but it is strongly recommended using this function over `let`\\*().

#### Arguments

|  |
| --- | ---
| `s_var` | Name of a local variable. Each variable is assigned to the resultof the corresponding `initExp`.
|  |
| --- | ---
| `initExp` | Expressions evaluated for the initial value. The`initExps` are evaluated sequentially in the environments that result from previous bindings.
|  |
| --- | ---
| `body` | A sequence of one or more expressions.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of the last expression of`body`.
#### Example

`letseq( ( ( x 1 ) ( y x+1 ) )     y     ) ; letseq=> 2`

The code above is a more convenient equivalent to the code below in which you control thesequence explicitly by the nesting.

`let( ( ( x 1 ) )    let( ( ( y x+1 ) )        y        )    )`

### mprocedure

`mprocedure( s_macroName( s_formalArgument ) g_expr1 ... )=> s_funcName`

#### Description

Defines a macro with the given name that takes a single formal argument. This is a`syntax` form.

The body of the macro is a list of expressions to be evaluated one after another. The value ofthe last expression evaluated is considered the result of `macro` expansion and is evaluated again to get the actual value of the macro call.

When a`macro` is called, `s_formalArgument` is bound to the entire macro call form, that is, a list with the name of the macro as its first element followed by the unevaluated arguments to the macro call.

Macros in SKILL are completely general in that a`macro` body can call any other function to build an expression that is to be evaluated again.

**Note:** A macro call within a function definition is expanded only once, when the function iscompiled. For this reason, be cautious when defining macros. sure they are purely functional, that is, side-effects free. You can use `expandMacro` to verify the correct behavior of a macro definition.

#### Arguments

|  |
| --- | ---
| `s_macroName` | Name of the macro function.
|  |
| --- | ---
| `s_formalArgument` | Formal arguments for the macro definition.
|  |
| --- | ---
| `g_expr1` | A SKILL expression.
#### Value Returned

|  |
| --- | ---
| `s_funcName` | Name of the macro defined.
#### Example

```
mprocedure( whenNot(callForm)            `(if !,(cadr callForm) then ,@(cddr callForm)))=> whenNot
```

`expandMacro( '(whenNot x>y z=f(y) x*z))=> if(!(x>y) then (z=f(y)) (x*z))`

`whenNot(1>2 "Good")=> "Good"`

#### Reference

[defmacro](#1039383 "Function and Program Structure")

### nlambda

`nlambda( ( s_formalArgument ) g_expr1 ... ) => u_result`

#### Description

(SKILL mode only) Allows`nlambda` functions to be defined without having names. In all other respects, `nlambda` is identical to `nprocedure`. This is a syntax form that is not supported in SKILL++ mode.

Allowing`nlambda` functions to be defined without having names is useful for writing temporary or local functions. In all other respects `nlambda` is identical to `nprocedure`.

An`nlambda` function should be declared to have a single formal argument. When evaluating an `nlambda` function, SKILL collects all the actual argument expressions unevaluated into a list and binds that list to the single formal argument. The body of the `nlambda` can selectively evaluate the elements of the argument list.

In general, it is preferable to use`lambda` instead of `nlambda` because `lambda` is more efficient. In most cases, `nlambdas` can be easily replaced by macros (and perhaps helper functions).

#### Arguments

|  |
| --- | ---
| `s_formalArgument` | Formal argument for the function definition.
|  |
| --- | ---
| `g_expr1` | SKILL expressions to be evaluated when the function is called.
#### Value Returned

|  |
| --- | ---
| `u_result` | A function object.
#### Example

`putd( 'foo nlambda( (x) println( x )))=> funobj:0x309128`

```
apply( nlambda((y) foreach(x y printf(x))) '("Hello" "World\n"))HelloWorld=> ("Hello" "World\n")
```

#### Reference

, , , ,

### nprocedure

`nprocedure( s_funcName( s_formalArgument ) g_expr1 ... )=> s_funcName`

#### Description

(SKILL mode only) Defines an`nlambda` function with a function name and a single formal argument. This is a syntax form that is not supported in SKILL++ mode.

The body of the procedure is a list of expressions to be evaluated one after another. The valueof the last expression evaluated is returned as the value of the function. There must be no white space separating the `s_funcName` and the open parenthesis of the list containing `s_formalArgument`.

An`nlambda` function defined by `nprocedure` differs from a `lambda` function defined by `procedure` in that an `nlambda` function does not evaluate its arguments; it binds the whole actual argument list to its single formal argument. `lambda` functions, on the other hand, evaluate each argument in the actual argument list and bind them one by one to each formal argument on the formal argument list. It is recommended that `procedure` be used over `nprocedure` whenever possible, in part because `procedure` is faster and also offers better type checking.

In general, it is preferable to use`lambda` instead of `nlambda` because `lambda` is more efficient.

#### Arguments

|  |
| --- | ---
| `s_funcName` | Name of newly defined function.
|  |
| --- | ---
| `s_formalArgument` | Formal argument for the function definition.
|  |
| --- | ---
| `g_expr1` | SKILL expressions to be evaluated when the function is called.
#### Value Returned

|  |
| --- | ---
| `s_funcName` | Returns the name of the function defined.
#### Example

`procedure( printarg(x) println(x))=> printarg`

Defines a`lambda` function.

`nprocedure( nprintarg(x) println(x))=> nprintarg`

Defines an`nlambda` function.

`y = 10=> 10printarg(y * 2)20=> nil`

Calls a`lambda` function. Prints the value 20. `println` returns nil.

`nprintarg(y * 2)((y * 2))=> nil`

Calls an`nlambda` function. Prints a list of the unevaluated arguments. `println` returns `nil`.

#### Reference

, ,

### procedure

`procedure( s_funcName( l_formalArglist ) g_expr1 ... )=> s_funcName`

#### Description

Defines a function using a formal argument list. The body of the procedure is a list ofexpressions to evaluate.

The body of the procedure is a list of expressions to be evaluated one after another when`s_funcName` is called. There must be no white space between `procedure` and the open parenthesis that follows, nor between `s_funcName` and the open parenthesis of `l_formalArglist`. However, for `defun` there must be white space between `s_funcName` and the open parenthesis. This is the only difference between the two functions. `defun` has been provided principally so that you can your code appear more like other LISP dialects.

The last argument in`l_formalArglist` can be a string denoting type-checking characters, specified using the argument type template. For more information about specifying the argument type template, see [Type Checking](../sklanguser/chap3.html#typechecking) in [Cadence SKILL Language User Guide](../sklanguser/sklanguserTOC.md).

Expressions within a function can reference any variable on the formal argument list or anyglobal variable defined outside the function. If necessary, local variables can be declared using the `let` or `prog` functions.

#### Arguments

|  |
| --- | ---
| `s_funcName` | Name of the function you are defining.
|  |
| --- | ---
| `l_formalArglist` | Formal argument list.
|  |
| --- | ---
| `g_expr1` | Expression or expressions to be evaluated when `s_funcName` is called.
#### Value Returned

|  |
| --- | ---
| `s_funcName` | Name of the function being defined.
#### ARGUMENT LIST PARAMETERS

Several parameters provide flexibility in procedure argument lists. These parameters arereferred to as @ ("at") options. The parameters are `@rest`, `@optional`, `@key`, and `@aux`.

#### @rest Option

The`@rest` option allows an arbitrary number of arguments to be passed into a function. Let's say you need a function that takes any number of arguments and returns a list of them in reverse order. Using the `@rest` option simplifies this task.

**Note:** The name of the parameter following`@rest` is changeable. The `r` has been used for convenience.

`procedure( myReverse( @rest r )    reverse( r ))=> myReverse`

`myReverse( 'a 'b 'c )=> (c b a)`

#### @optional Option

