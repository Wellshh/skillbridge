### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

15
==

Using SKILL and SKILL++ Together
================================

This chapter discusses the pragmatics of developing programs in the Cadence® SKILL++ language. You should be familiar with both SKILL and SKILL++, specifically the material in ["About SKILL++ and SKILL"](chap13.html#1008199 "About SKILL++ and SKILL") and ["Using SKILL++"](chap14.html#1008199 "Using SKILL++").

Developing a SKILL++ application involves the same basic tasks as for developing SKILLapplications. Because most viable applications will involve tightly integrated SKILL and SKILL++ components, there are several more factors to consider:

* Selecting an interactive language

> When entering a language expression into the command interpreter, you need to choosethe appropriate language mode.

* Partitioning an application into a SKILL portion and a SKILL++ portion

> You are free to implement your application as a heterogenous collection of source codefiles. You need to choose a file extension accordingly.

* Cross-calling between SKILL and SKILL++

> In general, SKILL++ functions and SKILL functions can transparently call one another.However, a few families of SKILL functions can operate differently when called from SKILL than when called from SKILL++. You need to be able to identify such SKILL functions, adjust your expectations, and exercise caution, when calling them from SKILL++.

* Debugging a SKILL++ program

> In a hybrid application, errors can occur in either SKILL functions or SKILL++ functions.Displaying the SKILL stack will reveal SKILL++ environments and SKILL++ function objects which you will want to examine.

* Communicating between SKILL and SKILL++

> Data allocated with one language is accessible from the other language. For example,you can allocate a list in a SKILL++ function and retrieve data from it in a SKILL function. Both languages use the same print representations for data.

The phrase `from within a SKILL program' means

* from a SKILL interactive loop

* from within SKILL source code, outside of a function definition

* from within a SKILL function

Similar definitions apply `from within a SKILL++ program'.

For more information, see the following sections:

* [Selecting an Interactive Language](#1008234 "Using SKILL and SKILL++ Together")

* [Partitioning Your Source Code](#1008259 "Using SKILL and SKILL++ Together")

* [Cross-Calling Guidelines](#1008269 "Using SKILL and SKILL++ Together")

* [Redefining Functions](#1008297 "Using SKILL and SKILL++ Together")

* [Sharing Global Variables](#1008301 "Using SKILL and SKILL++ Together")

* [Debugging SKILL++ Applications](#1008329 "Using SKILL and SKILL++ Together")

Selecting an Interactive Language
---------------------------------

You can use SKILL or SKILL++ for interactive work. Both languages support a read-eval-printloop in which you repeat the following steps:

* You type a language expression.

* The system parses, compiles, and evaluates the expression in accordance with eitherSKILL or SKILL++ languages syntax and semantics.

* The system displays the result using the print representation appropriate to the result'sdata type.

### Starting an Interactive Loop (toplevel)

You can call the`toplevel` function to start an interactive loop with either SKILL or SKILL++. SKILL is the default.

* To select the SKILL language, type

> `toplevel( 'il )`

* To select the SKILL++ language and the SKILL++ top-level environment, type

> `toplevel( 'ils )`

* To select the SKILL++ language and the environment to be made active during theinteractive loop, pass the environment object as the second argument:

> `toplevel( 'ils envobj( 0x1e00b4 ))`

In this example, the environment object is retrieved from the print representation.

### Exiting the Interactive Loop (resume)

Use the`resume` function to exit the interactive loop, returning a specific value. This value is the return value of the `toplevel` function. The following example is a transcript of a brief session, including prompts.

```
> R = toplevel( 'ils )ILS-<2> resume( 1 )1> R1                ;;;return value of the toplevel function.
```

Partitioning Your Source Code
-----------------------------

You are free to implement your application as a heterogenous collection of source code files.The `load` and `loadi` functions select the language to apply to the source code based on the file extension.

`FileA.ilFileB.ilFileC.ilsFileD.ilsFileE.ils`

Functions defined in each file can call functions defined in the other files without regard to thelanguage in which the functions are written. The syntax for function calls is the same regardless of whether the function called is a SKILL function or a SKILL++ function. Specifically,

* SKILL++ functions are visible to the SKILL portions of your application

* SKILL functions are automatically visible to the SKILL++ portions of your application

You may call SKILL application procedural interface functions from a SKILL++ program. Mostapplications continue to rely heavily on SKILL functions.

Cross-Calling Guidelines
------------------------

Several key semantic differences between SKILL and SKILL++ dictate certain guidelines youshould follow when calling SKILL functions from SKILL++, including the following:

* All SKILL++ environments, other than the top-level environment, are invisible to SKILL

* All SKILL++ local variables are invisible to SKILL

You should avoid calling SKILL functions that call

* The`eval`, `symeval`, or `evalstring` functions

* The`set` function

You should avoid calling`nlambda` SKILL functions.

### Avoid Calling SKILL Functions That Call eval, symeval, or evalstring

When you call the one-argument version of`eval`, `symeval`, or `evalstring` functions from a SKILL function, you are using dynamic scoping. Any symbol or expression which you pass to a SKILL function will probably evaluate to a different result than it would have in the SKILL++ caller.

In general, to determine whether a SKILL function calls any of these functions, you shouldconsult the reference documentation.

### Avoid Calling nlambda Functions

The nlambda category of SKILL functions are highly likely to call the`eval` or `symeval`functions.

A SKILL`nlambda` function receives all of its argument expressions unevaluated in a list. Such a function usually evaluates one or more of the arguments. The `addVars` SKILL function adds the values of its arguments.

```
nprocedure( addVars( args )    let( (( sum 0 ))        foreach( arg args            sum = sum+eval(arg)            ) ; foreach        sum        )     )     let( ((x 1) (y 2) (z 3 ))        addVars( x y z )        )=> 6
```

When called from SKILL++, the`eval` function uses dynamic scoping to resolve the variable references. In this case, the variable `x` was unbound.

```
ILS-<2> let( ((x 1) (y 2) (z 3 ))    addVars( x y z )    )*WARNING* (addVars): calling NLambda from Scheme code -     addVars(x y z)*Error* eval: unbound variable - xILS-<2>
```

If necessary, reimplement the SKILL`nlambda` function as a SKILL or SKILL++ macro, using `defmacro`. For example,

```
defmacro( addVars ( @rest args )    `let( (( sum 0 ))        foreach( arg list( ,@args )            sum = sum + arg            ) ; foreach        sum        )     )
```

### Use the set Function with Care

Avoid calling SKILL functions that in turn call the`set` function. Usually such SKILL functions store values in other SKILL variables. If you call such a function from SKILL++ and pass a quoted local variable, the SKILL function will not store the value in the SKILL++ local variable. Instead, the value goes into the SKILL variable of the same name.

The following`SetMyArg` SKILL function behaves differently when called from SKILL++ than when called from SKILL.

#### SetMyArg Called from SKILL

```
> procedure( SetMyArg( aSymbol aValue )    set( aSymbol aValue )    ) ; procedureSetMyArg> let( ( ( x 3 ))    SetMyArg( 'x 5 )    x    ) ; let5
```

#### SetMyArg Called from SKILL++

`> toplevel 'ils ILS-<2> let( (( x 3 ))  SetMyArg( 'x 5 )  x  ) ; let3`

Redefining Functions
--------------------

During a single session, you are warned when you redefine a SKILL function to be a SKILL++function, or visa versa.

You are only likely to encounter this when doing interactive work and are confused aboutwhich language "owns" the interaction.

Sharing Global Variables
------------------------

It is generally desirable to avoid relying on global variables. However, it is sometimesnecessary or expedient for the SKILL++ and SKILL portions of your application to communicate through global variables.

### Using importSkillVar

Before the SKILL and SKILL++ portions of your application can share a global variable, youmust first call the `importSkillVar` function. The SKILL++ global variable and the SKILL global variable will then be bound to the same location.

For example, consider the following interaction with a SKILL top level.

`> delta = 22> procedure( adder( y )    delta+y    ) ;adder>`

To set the value of the`delta` variable from within a SKILL++ program, you should first

`importSkillVar( delta )`

as the following sample interaction with a SKILL++ top level shows.

```
> toplevel 'ilsILS-<2>delta*Error* eval: unbound variable - deltaILS-<2> importSkillVar( delta )ILS-<2> delta2ILS-<2> adder( 4 )6
```

**Note:** You do not need to import`delta` just to call `adder` from within SKILL++ code.

### How importSkillVar Works

Although understanding this level of detail is not necessary to effectively use`importSkillVar`, this section is provided for expert users.

In SKILL++, a variable is bound to a memory location called the variable's binding. Thefamiliar operation of "storing a value in a variable" actually stores the value in the variable's binding. SKILL++ variable bindings are organized into environment frames. The SKILL++ top-level environment contains all the variable bindings initially available at system start up.

Normally, all global (top-level) SKILL++ variables are bound to the function slot of the SKILLsymbol with the same name as the variable. For example, the variable `foo` is bound to the function slot of the symbol `foo`. Consequently, in SKILL++, when you retrieve the value of a SKILL variable, you are getting the contents of the symbol's function slot.

The`importSkillVar` function directs the compiler to instead bind a SKILL++ global variable in the top-level environment to the value slot of the symbol with the same name. Informally, you can use `importSkillVar` to enable access to a SKILL symbol's current value binding from within SKILL++.

### Evaluating an Expression with SKILL Semantics

As an advanced programmer, you might find that separating closely related SKILL code andSKILL++ code into different files is distracting or otherwise not convenient. For example, suppose that in the middle of a SKILL++ source code file you want to declare a SKILL function that refers to a SKILL variable.

Using the previous example

`delta = 5procedure( adder( y )    delta+y )`

The`inSkill` macro below allows you to splice SKILL language source code into a SKILL++ source code file. You can use the `inSkill` macro as shown.

`inSkill(    delta = 5    procedure( adder( y )        delta+y ) ; procedure    )`

Debugging SKILL++ Applications
------------------------------

This section addresses common tasks that arise when debugging hybrid SKILL and SKILL++applications.

### Examining the Source Code for a Function Object

Use the`pp` SKILL function to display the source code for a global function. The `pp` function expects that its argument is a symbol. It retrieves the function object stored in the function slot of the symbol you pass. To use `pp` to display the source code for a function object, store the function object in an unused global.

In SKILL++

`G4 = funobj( 0x1e3628 )pp( G4 )`

In SKILL

`putd( 'G4 ) = funobj( 0x1e3628 )pp( G4 )`

The`pp` function pretty-prints the function object stored in the function slot of the symbol. The `pp` function uses the global symbol to name the function object. This is only seriously misleading if the function object is recursive.

### Pretty-Printing Package Functions

Use the`pp` function as explained above to pretty-print package functions.

```
MathPackage = let( ()    procedure( add( x y ) x+y )    procedure( mult( x y ) x*y )    list( nil 'add add 'mult mult )    )    => (nil add funobj:0x1c9c48 nult funobj:0x1c9c58)ILS-1> Q = MathPackage->addfunobj:0x1c9c48ILS-1> pp( Q )procedure( Q(x y)    (x + y)    )
```

### Inspecting Environments

A significant SKILL++ application is likely to include many function objects, each with its ownseparate environment. While debugging, you may need to interactively examine or set a local variable in an environment other than the active environment.

You can

* Retrieve the active environment

* Inspect an environment with the`->` operator

* Retrieve the environment of a function object

### Retrieving the Active Environment

The`theEnvironment` function returns the enclosing lexical environment when you call it from within SKILL++ code.

#### Example 1

`Z = let( (( x 3 ))     theEnvironment()     ) ; let    => envobj:0x1e0060`

This example returns the environment that the`let` expression establishes. The value of `Z` is an environment in which `x` is bound to `3`. Each time you execute the above expression, it returns a different environment object.

#### Example 2

```
W = let( (( r 3 ) ( y 4 ))    let( (( z 5 ) ( v 6 ))        theEnvironment()        )     )
```

This example returns the environment that the nested`let` expressions establish.

### Testing Variables in an Environment (boundp)

Use the`boundp` function to determine whether a variable is bound in an environment. The optional second argument should be a SKILL++ environment.

`boundp( 'b W ) => nilboundp( 'r W ) => t`

### Using the -> Operator with Environments

You can use the`->` operator against an environment to read and write variables bound in the environment.

`W->z => 5W->v = 100`

Alternatively, you can use the`symeval` function to retrieve the value of a variable relative to an environment.

`symeval( 'r W ) => 3`

Alternatively, you can use the`set` function to set the value of a variable in an environment.

`set( 'r 200 W ) => 200`

### Using the ->?? Operator with Environments

Use the`->??` operator to dump out the environment as a list of association lists with one association list for each environment frame.

`W->?? => ( ((z 5) (v 6)) ((r 3) (y 4)) )`

### Evaluating an Expression in an Environment (eval)

Use the`eval` function to evaluate an expression in a given lexical environment.

`eval( '( z+v ) W ) => 11eval( '( z = 100 ) W ) => 100eval( '( z+v ) W ) => 106`

### Examining Closures

As function objects, closures have both source code and data. For example, consider thefollowing closure generated when the `makeAdder` function is called.

```
procedure( makeAdder( delta )    lambda( ( x ) x + delta )    ) => makeAdderadd5 = makeAdder( 5 )=> funobj:0x1fe668
```

#### Examining the Source Code

Use the`pp` function as explained above to examine the source code for the closure.

`ILS-1> pp( add5 )procedure( add5(x)    (x + delta))nil`

#### Examining the Environment

Install the SKILL Debugger and use the`theEnvironment` function to retrieve the environment for the function object. Use the `->??` operator to examine the environment.

`theEnvironment( funobj( 0x1fe668 ) )->??=> (((delta 5)))`

See the`makeStack` example in ["Implementing the makeStack Function"](chap14.html#1008451 "Using SKILL++")

```
S = makeStack( '( 1 2 3 )) => funobj:0x1e3758E = theEnvironment( S ) => envobj:0x1e00b4E->push => funobj:0x1e3738E->initialContents => (1 2 3)
```

### General SKILL Debugger Commands

#### Tracing (tracef)

You can only use the`tracef` function to trace SKILL functions or SKILL++ functions defined in the top-level SKILL++ environment.

#### Setting Breakpoints

You can only set breakpoints at SKILL functions or SKILL++ functions defined in the top-levelSKILL++ environment.

#### Calling the break Function

You can insert a call to the`break` function but that requires redefining the function that calls the `break` functions. If called from SKILL++, the enclosing lexical environment is the active environment during the debugger session.

```
ILS-<2> MathPackage = let( ()    procedure( add( x y ) break() x+y )    procedure( mult( x y ) x*y )    list( nil 'add add 'mult mult )    )(nil add funobj:0x1c9ca8 mult funobj:0x1c9cb8)
```

```
ILS-<2> MathPackage->add( 3 4 )<<< Break >>> on explicit 'break' requestSKILL Debugger: type 'help debug' for a list of commands or debugQuit to leave.ILS-<3> theEnvironment()->??(((x 3)         (y 4)    )     ((add funobj:0x1c9ca8)         (mult funobj:0x1c9cb8)    ))ILS-<3>
```

#### Examining the Stack (stacktrace)

During the execution of both SKILL and SKILL++ function calls, use the`stacktrace` function to examine the SKILL stack. The stack will probably contain several function object and environment object references. You can use the techniques discussed above to display source code for a function object and to examine an environment.

For example, at the break point in the previous example notice that the`break` function passes the active environment to the break handler.

```
ILS-<3> stacktrace()<<< Stack Trace >>>breakHandler(envobj:0x1bb108)break()funcall((MathPackage->add) 3 4)toplevel('ils)4ILS-<3>
```




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
