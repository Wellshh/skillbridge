### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

3
=

Creating Functions in SKILL
===========================

["Getting Started"](chap1.html#1008199 "Getting Started") introduces you to developing a Cadence® SKILL language function. This chapter introduces you to constructs for defining a function and defining local and global variables.

This chapter covers the following topics:

* [Terms and Definitions](#1009052 "Creating Functions in SKILL")

* [Kinds of Functions](#1009074 "Creating Functions in SKILL")

* [Syntax Functions for Defining Functions](#1009085 "Creating Functions in SKILL")

* [Defining Parameters](#1009179 "Creating Functions in SKILL")

* [Type Checking](#typechecking "Creating Functions in SKILL")

* [Local Variables](#1009266 "Creating Functions in SKILL")

* [Global Variables](#1009291 "Creating Functions in SKILL")

* [Redefining Existing Functions](#1009325 "Creating Functions in SKILL")

* [Physical Limits for Functions](#1009333 "Creating Functions in SKILL")

See also["Advanced Topics"](chap9.html#1008199 "Advanced Topics") for more information.

Terms and Definitions
---------------------

|  |
| --- | ---
| function, procedure | In SKILL, the terms procedure and function are usedinterchangeably to refer to a parameterized body of code that can be executed with actual parameters bound to the formal parameters. SKILL can represent a function as both a hierarchical list and as a function object.
|  |
| --- | ---
| argument, parameter | The terms argument and parameter are used interchangeably.The actual arguments in a function call correspond to the formal arguments in the declaration of the function.
|  |
| --- | ---
| byte-code | A generic term for the machine code for a "virtual" machine.
|  |
| --- | ---
| virtual machine | A machine that is not physically built, but is emulated in softwareinstead.
|  |
| --- | ---
| function object | The set of byte-code instructions that implement a function'salgorithm. SKILL programs can treat function objects on a basic level like other data types: compare for equality, assigning to a variable, and pass to a function.
|  |
| --- | ---
| function body | The collection of SKILL expressions that define the function'salgorithm.
|  |
| --- | ---
| compilation | The generation of byte-code that implements the function'salgorithm.
|  |
| --- | ---
| compile time | SKILL compiles function definitions when you load source code.Top-level expressions are compiled and then executed.
|  |
| --- | ---
| run time | The time during which SKILL evaluates a function object.
Kinds of Functions
------------------

SKILL has several different kinds of functions, classified by the internal names of`lambda`,`nlambda`, and `macro`. SKILL follows different steps when evaluating these functions.

* Most of the functions you will define are`lambda` functions. SKILL executes a `lambda` function after evaluating the parameters and binding the results to the formal parameters.

* You will probably not need to define an`nlambda` function. However, several built-in SKILL functions are `nlambda` functions.

> An`nlambda` function should be declared to have a single formal argument. When evaluating an `nlambda` function, SKILL collects all the actual argument expressions unevaluated into a list and binds that list to the single formal argument. The body of the nlambda can selectively evaluate the elements of the argument list.

* It is not likely that you will write many macros. A`macro` function allows you to adapt the normal SKILL function call syntax to the needs of your application. Unlike `lambda` and `nlambda` functions, SKILL evaluates a macro at compile-time. When compiling source code, if SKILL encounters a `macro` function call, it evaluates the function call immediately and the last expression computed is compiled in the current function object.

Syntax Functions for Defining Functions
---------------------------------------

SKILL supports the following syntax functions for defining functions. You should use the`procedure` function or the `defun` function in most cases.

### procedure

The`procedure` function is the most general and is easiest to use and understand. Anything that can be done with the other function definition functions can be done with a `procedure` and possibly a `quote` in the call.

The`procedure` function provides the standard method of defining functions. Its return value is the symbol with the name of the function. For example:

```
procedure( trAdd( x y )       printf( "Adding %d and %d … %d \n" x y x+y )       x+y       ) => trAddtrAdd( 6 7 ) => 13
```

### lambda

The`lambda` function defines a function without a name. Its return value is a function object that can be stored in a variable. For example:

```
trAddWithMessageFun = lambda( ( x y )      printf( "Adding %d and %d … %d \n" x y x+y )       x+y       ) => funobj:0x1814b90
```

You can subsequently pass a function object to theapply function
together with an argument list. For example:

`apply( trAddWithMessageFun '( 4 5 ) ) => 9`

The use of`lambda` can render code difficult to understand. Often the function being defined is required at some other point in the program and so a procedural definition is better. However, the `lambda` structure can be useful when defining special purpose functions and for passing very small functions to functions such as `sort`. For example, to sort a list `signalList` of disembodied property list objects by a property named `strength`, do the following:

```
signalList = '(       ( nil strength 1.5 )      ( nil strength 0.4 )      ( nil strength 2.5 )      )
```

`sort( signalList      lambda( ( a b ) a->strength <= b->strength )      )`

Refer to["Declaring a Function Object (lambda)"](chap9.html#1008388 "Advanced Topics") for further details.

### nprocedure

Do not use the`nprocedure` function in new code that you write. It is only included in the system for compatibility with prior releases.

* To allow your function to accept an indeterminate number of arguments, use the`@rest` option with the `procedure` function.

* To allow your function to receive arguments unevaluated, use the`defmacro` function.

### defmacro

The`defmacro` function provides a means for you to define a `macro` function. You can use a macro to design your own customized SKILL syntax. Your macro is responsible for translating your custom syntax at compile time into a SKILL expression to be compiled and subsequently executed.

Refer to["Macros"](chap9.html#Macros "Advanced Topics") for further discussion and examples.

### mprocedures

The`mprocedure` function is a more primitive alternative to the `defmacro` function. The `mprocedure` function has a single argument. The entire custom syntax is passed to the `mprocedure` function unevaluated.

Do not use the`mprocedure` function in new code. It is only included in the system for compatibility with prior releases. Use the `defmacro` function instead. If you need to receive an indeterminate number of unevaluated arguments, use an `@rest`argument.

Refer to["Macros"](chap9.html#Macros "Advanced Topics") for further discussion and examples.

### defglofun

The defglofun function defines a function which is global within a lexical scope.

### Summary of Syntax Functions

The following table summarizes each syntax function for declaring a function.You should think twice about using anything other than `procedure`.

****Comparison of Syntax Functions****

| **SyntaxFunction** | **FunctionType** | **Argument Evaluation** | **Execution**
| procedure | lambda | The arguments areevaluated and bound to the corresponding formal arguments. | The expressions in the bodyare evaluated at run time. The last value computed is returned.
| defmacro | macro | The arguments are boundunevaluated to the corresponding formal arguments. | The expressions in the bodyare evaluated at compile time. The last value computed is compiled.
| mprocedure | macro | The entire function call isbound to the single formal argument. | The expressions in the bodyare evaluated at compile time. The last value computed is compiled.
| nprocedure | nlambda | All arguments are gatheredunevaluated into a list and bound to the single formal argument. | The expressions in the bodyare evaluated at run time. The last value computed is returned.
Defining Parameters
-------------------

You can declare how parameters are to be passed to your function by adding the at (@)options in the formal argument list. The available @ options are `@rest`, `@optional`, and `@key`. You can use these options in `procedure`, `lambda`, and `defmacro` argument lists.

### @rest Option

The`@rest` option allows an arbitrary number of parameters to be passed to a function in a list. The name of the parameter following `@rest` is arbitrary, although `args` is a good choice.

The following example illustrates the benefits of an`@rest` argument.

```
procedure( trTrace( fun @rest args )      let( ( result )            printf( "\nCalling %s passing %L" fun args )            result = apply( fun args )            printf( "\nReturning from %s with %L\n" fun result )            result            ) ; let      ) ; procedure
```

For example, invoking the`trTrace` function passing `plus` and `1, 2, 3` returns `6`.

`trTrace( 'plus 1 2 3 ) => 6`

and displays the following output in the CIW.

`Calling plus passing (1 2 3)Returning from plus with 6`

* The`trTrace` function calls the `fun` function and passes the arguments it received.

* The`apply` function calls a given function with the given argument list. `trTrace` passes the `@rest`argument list directly to the `apply` function.

The`trTrace` function must accept an arbitrary number of arguments. The number of arguments passed can vary from call to call.

Another benefit of`@rest` is that it puts the arguments into a single list. The `trTrace` function would be less convenient to use if the caller had to put `fun`'s arguments into a list.

If in a function that specifies keyword arguments and passes arguments using`@rest`option, you use the same keyword argument more than once, SKILL uses the first value of the keyword encountered in the function. Any value that does not match with either required or keyword arguments are passed to the `@rest` argument.

The following example illustrates the scenario where the same keyword argument (`x`) is specified twice.

`defun( test (a @key x y @rest z)`

`printf("a=%L x=%L y=%L z=%L\n" a x y z))`

`(test 0 ?x 1 ?x 2)`

`=> a=0 x=1 y=nil z=(?x 2)`

### @optional Option

The`@optional` option gives you another way to specify a flexible number of arguments. With `@optional`, each argument on the actual argument list is matched up with an argument on the formal argument list.

You can provide any optional parameter with a default value. Specify the default value usinga default form. The default form is a two-member list. The first member of this list is the optional parameter's name. The second member is the default value.

The default value is assigned only if no value is assigned when the function is called. If theprocedure does not specify a default value for an argument, `nil` is assigned.

If you place`@optional` in the argument list of a procedure definition, any parameter following it is considered optional.

The`trBuildBBox` function builds a bounding box.

```
procedure( trBuildBBox( height width @optional       ( xCoord 0 ) ( yCoord 0 ) )            list(             xCoord:yCoord ;;; lower left             xCoord+width:yCoord+height ) ;;; upper right      ) ; procedure
```

Both`length` and `width` must be specified when this function is called. However, the coordinates of the box are declared as optional parameters. If only two parameters are specified, the optional parameters are given their default values. For `xCoord` and `yCoord`, those values are 0.

Examine the following calls to`trBuildBBox` and their return values:

```
trBuildBBox( 1 2 )       => ((0 0) (2 1))trBuildBBox( 1 2 4 )     => ((4 0) (6 1)) trBuildBBox( 1 2 4 10)   => ((4 10) (6 11))
```

### @key Option

`@optional` relies on order to determine what actual arguments are assigned to each formal argument. The `@key` option lets you specify the expected arguments in any order.

For example, examine the following generalization of the`trBuildBBox` function. Notice that within the body of the function, the syntax for referring to the parameters is the same as for ordinary parameters:

```
procedure( trBuildBBox(       @key ( height 0 ) ( width 0 ) ( xCoord 0 ) ( yCoord 0 ) )      list(             xCoord:yCoord ;;; lower left             xCoord+width:yCoord+height ) ;;; upper right      ) ; procedure
```

```
trBuildBBox()                                                           => ((0 0) (0 0))trBuildBBox( ?height 10 )                              => ((0 0) (0 10))trBuildBBox( ?width 5 ?xCoord 10 )   => ((10 0) (15 0))
```

### Combining Arguments

`@key` and `@optional` are mutually exclusive; they cannot appear in the same argument list. Consequently, there are two standard forms that `procedure` argument lists follow:

```
procedure(functionname([var1 var2 …]      [@optional opt1 opt2 …]      [@rest r])      .      .)
```

```
procedure(functionname([var1 var2 …]      [@key key1 key2 …]      [@rest r])      .      .)
```

Type Checking
-------------

Unlike most conventional languages that perform type checking at compile time, SKILLperforms dynamic type checking when functions are executed (not when they are defined). Each SKILL lambda or macro function can have as part of its definition an argument template that defines the types of arguments that the function expects. Type checking is not supported in `mprocedure` functions.

Type characters are discussed in["Data Characteristics"](chap2.html#1008463 "Language Characteristics"). For type checking purposes, you can use several composite type characters (shown in the table below) representing a union of data types.

**Composite Characters for Type Checking**

| **Character** | **Meaning**
| `S` | Symbol or string
| `n` | Number:`fixnum`, `flonum`
| `u` | Function: Either the name of a function (symbol) or a lambda function body (list)
| `g` | Any data type
You specify the argument type template as a string of type characters at the end of a formalargument list. If the template is present, SKILL matches the data type of each actual argument against the template at the time the function is invoked. For example:

`procedure( f(x y "nn") x**2 + y**2 )`

`nn` specifies that `f` accepts two numerical arguments.

`procedure( comparelength(str len "tx") strlen(str) == len)`

`tx` specifies that the first argument must be a string and the second must be an integer.

Local Variables
---------------

When you write functions, you should make your variables local. You can define localvariables using the `let` and `prog` functions:

* [Defining Local Variables Using the let Function](#1012098 "Creating Functions in SKILL")

* [Defining Local Variables Using the prog Function](#1012049 "Creating Functions in SKILL")

See also["Initializing Local Variables to Non-nil Values"](#1009288 "Creating Functions in SKILL").

### Defining Local Variables Using the let Function

You can use the`let` function to establish temporary values for local variables.

* You can include a list of the local variables followed by one or more SKILL expressions.These variables are initialized to `nil`.

* The SKILL expressions make up the body of the`let` function, which returns the value of the last expression computed within its body.

* The local variables are known only within the`let` statement. The values of the variables are not available outside the `let` statement.

> ```
> procedure( trGetBBoxHeight( bBox )    let( ( ll ur lly ury )        ll                 = car( bBox )        lly      = cadr( ll )        ur       = cadr( bBox )        ury      = cadr( ur )        ury - lly    ) ; let) ; procedure
> ```

* The local variables are`ll, ur, lly`, and `ury`.

* They are initialized to`nil`.

* The return value is`ury - lly`.

### Defining Local Variables Using the prog Function

A list of local variables and your SKILL statements make up the arguments to the`prog` function.

`prog( ( localVariables ) yourSKILLstatements )`

The`prog` function allows an explicit loop to be written because the`go` function is supported within the `prog`. In addition, `prog` allows you to have multiple return points through use of the `return` function. If you are not using either of these two features, `let` is much simpler and faster (see ["Defining Local Variables Using the let Function"](#1012098 "Creating Functions in SKILL")).

### Initializing Local Variables to Non-nil Values

You can use`let` to initialize local variables to non-`nil` values by making a two element list with the local variable and its initial value. You cannot refer to any other local variable in the initialization expression. For example:

```
procedure( trGetBBoxHeight( bBox )    let( ( ( ll car( bBox ) ) ( ur cadr( bBox ) ) lly ury )        lly            = cadr( ll )        ury            = cadr( ur )        ury - lly    ) ; let) ; procedure
```

Global Variables
----------------

Besides predefined functions that you are not allowed to modify, there are several variablenames reserved by various system functions. They are listed in ["Naming Conventions"](chap2.html#1009937 "Language Characteristics").

The use of global variables in SKILL, as with any language, should be kept to a minimum.

Following standard naming conventions and running SKILL Lint can reduce your exposure toproblems associated with global variables.

### Testing Global Variables

Applications typically initialize one or more global variables. Before an application runs for thefirst time, it is likely that its global variables are `unbound`. In such circumstances, retrieving the value of such a global variable causes an error.

Use the`boundp` function to check whether a variable is `unbound` before accessing its value. For example:

`boundp( 'trItems ) && trItems`

returns`nil` if `trItems` is `unbound` and returns the value of `trItems` otherwise.

### Avoiding Name Clashes

Two applications might accidentally access and set the same global value. Use a standardnaming scheme to minimize the chance of this problem occurring. SKILL Lint can flag global variables that do not obey your naming scheme. For details, refer to the chapter on SKILL Lint in *Cadence SKILL IDE User Guide*.

Assume that`trApplication1` and `trApplication2` are two application functions that are supposed to be totally independent. In particular, the order in which they are executed should not matter. Assume both rely on a single global variable. To observe what can happen if the two applications were accidentally coded to use the same global variable, consider the following example.

```
procedure( trApplication1()      when( !boundp( 'sharedGlobal ) ;;; not set             sharedGlobal = 1            ) ; when      ) ; procedureprocedure( trApplication2()      when( !boundp( 'sharedGlobal ) ;;; not set            sharedGlobal = 2            ) ; when      ) ; procedure
```

The order in which you run`trApplication1` and `trApplication2` determines the final value of `sharedGlobal`.

```
sharedGlobal = 'unboundtrApplication1()                      => 1sharedGlobal                          => 1trApplication2()                      => nilsharedGlobal                          => 1
```

```
sharedGlobal = 'unboundtrApplication2()                      => 2sharedGlobal                          => 2trApplication1()                      => nilsharedGlobal                          => 2
```

Name "clashes" can also occur between functions because programmers can be using thesame function names. In this case, a subsequent function definition either overwrites a previous one, or, if `writeProtect` is set, the function definition fails with an error.

### Naming Scheme

The recommended naming scheme is to

* Use casing to separate code that is developed within Cadence from that developedoutside.

* Use a group prefix to separate code developed within Cadence.

All code developed by Cadence Design Systems should name global variables and functionswith an optional underscore; up to three lowercase characters that signify the code package; an optional further lowercase character (one of c, i, or v) and then the name itself starting with an uppercase character. For example, `dmiPurgeVersions()` or `hnlCellOutputs`. All code developed outside Cadence should name global variables by starting them with an uppercase character, such as `AcmeGlobalForm.`

### Reducing the Number of Global Variables

One other technique to reduce the number of global variables is to consolidate a collection ofrelated globals into a disembodied property list or a symbol's property list. That symbol becomes the only global.

This technique could even be extended to associate one symbol with an entire softwaremodule. The disadvantage of this approach is that long property lists involve an access time penalty.

Redefining Existing Functions
-----------------------------

You often need to redefine a function that you are debugging. The procedure definingconstructs allow you to redefine existing functions; however, functions that are write protected cannot be redefined.

* A function not being executed can be redefined if the write protection switch was turnedoff when the function was initially defined. To turn off the `writeProtect` switch, type

> `sstatus( writeProtect nil )`

* When building contexts,`writeProtect` is always set to`t`.

Aside from debugging, the ability to have multiple definitions for the same function is usefulsometimes. For example, within the Open Simulation System (OSS) "default" netlisting functions can be overridden by user-defined functions.

Finally, you should use a standard naming scheme for functions and variables.

Physical Limits for Functions
-----------------------------

The following physical limitations exist for functions:

* Total number of`keyword/optional` arguments is less than 255

* Max size of code vector is less than 1GB

By default, code vectors are limited to functions that can compile less than 32KB words. Thistranslates roughly into a limit of 20000 lines of SKILL code per function. The maximum number of arguments limit of 32KB is mostly applicable in the case when functions are defined to take an @rest argument or in the case of apply called on an argument list longer than 32KB elements.

```
To remove that limitation you should set the following value: setSaveContextVersion(getNativeContextVersion())
```

Then, the generated contexts (version:602) will not be compatible with old releases but allowcode vector in functions to be greater than 32KB.

SKILL Lint catches argument numbers greater than the limits with the following message:

```
NEXT RELEASE (DEF6): <filename - line number> (<funcname> :definition for <funcname> cannot have more than 255 optional arguments.
```




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
