### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

14
==

Using SKILL++
=============

This chapter deals with the pragmatics of writing programs in the Cadence® SKILL++ language.

["About SKILL++ and SKILL"](chap13.html#1008199 "About SKILL++ and SKILL") provides an overview of the differences between the Cadence SKILL language and SKILL++.

["Using SKILL and SKILL++ Together"](chap15.html#1008199 "Using SKILL and SKILL++ Together") focuses on the key areas in which SKILL++ semantics differ from SKILL semantics.

["SKILL++ Object System"](chap16.html#1008199 "SKILL++ Object System") describes a system that allows for object-oriented interfaces based on classes and generic functions composed of methods specialized on those classes.

For more information, see the following sections:

* [Declaring Local Variables in SKILL++](#1008217 "Using SKILL++")

* [Sequencing and Iteration](#1008294 "Using SKILL++")

* [Software Engineering with SKILL++](#1008365 "Using SKILL++")

* [SKILL++ Packages](#1008377 "Using SKILL++")

Declaring Local Variables in SKILL++
------------------------------------

SKILL++ provides three binding constructs to declare local variables together withinitialization expressions. The syntax for `let, letseq` and `letrec`is identical but they differ in the order of evaluation of the initialization expressions and in the scope of the local variables.

#### Syntax Template for let, letseq and letrec

```
let(     ( ( s_var1 g_initExp1 ) ( s_var2 g_initExp2 )… )    g_bodyExp1     g_bodyExp2     …    )
```

### Using let

Each local variable has the body of the`let` expression as its lexical scope. The order of evaluation of the initialization expressions and the binding sequence is unspecified. You should avoid cross-references between variables in a `let` expression.

* ***The initialization expression bound to one local variable should not referto any of the other local variables.***

#### Example 1

`let( ( ( x 2 ) ( y 3 ) )    x*y     ) => 6`

#### Example 2

```
let( ( ( x 2 ) ( y 3 ) )    let( (( z 4 ))        x + y + z         ) ; let    ) ; let=> 9
```

#### Example 3

```
let( ( ( x 2 ) ( y 3 ) )    let( (( x 7 ) ( z x+y ) )        z*x        )    ) => 35
```

Because the initialization expressions are outside of the scope of the`let`, `z` is bound to `2+3`, instead of `7+3`.

#### Example 4

```
let( ( ( x 2 ) ( y 3 ) )    let( (( x 7 ) ( foo lambda( ( z ) x + y + z ) ) )        foo( 5 )        )     ) => 10
```

This example shows that the initialization expressions are also outside the scope of the`let`. Specifically, the occurrence of `x` in the body of `foo` is in the scope of the outer `let`.

### Using letseq

Use`letseq` to control the order of evaluation of the initialization expressions and the binding sequence of the local variables. Evaluation proceeds from left to right. The scope of each variable includes the remaining initialization expressions and the body of `letseq`. It is equivalent to a corresponding sequence of nested `let` expressions.

#### Example 1

`letseq( ( ( x 1 ) ( y x+1 ) )     y     ) => 2`

The code above is a more convenient equivalent to the code below in
which you control the sequence explicitly by the nesting.

`let( ( ( x 1 ) )    let( ( ( y x+1 ) )        y        )    )`

#### Example 2

```
let( ( ( x 2 ) ( y 3 ) )    letseq( (( x 7 ) ( z x+y ) )        z*x        )    ) => 70
```

This example is identical to["Example 3"](#1008234 "Using SKILL++") except that the inner `let` is replaced with `letsec`.

#### Example 3

```
let( ( ( x 2 ) ( y 3 ) )    letseq( (( x 7 ) ( foo lambda( ( z ) x + y + z ) ) )        foo( 5 )        )     ) => 15
```

This example is identical to["Example 4"](#Example 4 Using let "Using SKILL++") except that the inner `let` is replaced with `letseq`.

### Using letrec

Unlike`let` and `letseq`, each variable's scope is the entire `letrec` expression. In particular, each variable's scope includes all of the initialization expressions. Each initialization expression can refer to the other local variables with the following restriction: each initialization expression must be executable without accessing the other variables. This restriction is met when each initialization expression is a `lambda` expression. Therefore, use `letrec` to declare mutually recursive local functions.

#### Example 1

```
letrec(     ( ;;; variable list        ( f             lambda( ( n )                 if( n > 0 then n*f(n-1) else 1                      ) ; if                ) ; lambda            ) ; f        ) ; variable list    f( 5 )    ) ; letrec => 120
```

This example declares a single recursive local function. The`f` function computes the factorial of its argument. The `letrec` expression returns the factorial of 5.

#### Example 2

```
procedure( trParity( x )    letrec(      (           ( isEven               lambda( (x)                   x == 0 || isOdd( x-1 )                  ) ; lambda              ) ; isEven           ( isOdd               lambda( (x)                   x > 0 && isEven(x-1)) ; lambda               ) ; isOdd           ) ;       if( isEven( x ) then 'even else 'odd )      ) ; letrec    ) ; procedure
```

The`trParity` function returns the symbol `even,` if its argument is `even`, and returns the symbol `odd` otherwise. `trParity` relies on two mutually recursive local functions `isEven` and `isOdd`.

### Using procedure to Declare Local Functions

As an alternative to using`letrec` to define local functions, you can use the `procedure` syntax.

#### Example 1

This example uses the`procedure` construct to declare a local function instead of using `letrec`.

```
procedure( trParity( x )    procedure( isEven(x)         x == 0 || isOdd( x-1 )        )     procedure( isOdd(x)         x > 0 && isEven(x-1)         )     if( isEven( x ) then 'even else 'odd )    ) ; procedure
```

#### Example 2

```
procedure( makeGauge( tolerance )    let( ( ( iteration 0 ) ( previous 0.0 ) test )        procedure( performTest( value )            ++iteration            test = ( abs( value - previous ) <= tolerance )            previous = value            when( test list( iteration value ))            ) ; procedure        performTest        ) ; let    ) ; procedureG = makeGauge( .1 )=> funobj:0x322b28G(2) => nil                  ;; first iterationG(3)=> nil                   ;; secondG(3.01) = >                  ;; third iteration      ( 3 3.01 )
```

The`makeGauge` function declares the local `performTest` function and returns it. This function object is the gauge. Passing a value to the gauge compares it to the previous value passed then updates the previous value. The gauge returns a list of the iteration count and the value, or `nil`. The function object has access to the local variables `iteration`, `previous`, and `test,` as well as access to the argument `tolerance`. Notice that using a gauge object can simplify your code by isolating variables used only for the tracking of successive values.

For another`makeGauge` example, see ["Example 4: Using a Gauge When Computing the Area Under a Curve"](#Example 4 Using do "Using SKILL++").

#### Example 3

```
procedure( trPartition( nList )    procedure( loop( numbers nonneg neg )        cond(            ( !numbers list( nonneg neg ))            ( car( numbers ) > 0                 loop(                     cdr( numbers )                     cons( car( numbers ) nonneg ) ; ppush on nonneg                    neg                    ) ; loop                )            ( car( numbers ) < 0                loop(                     cdr( numbers )                     nonneg                    cons( car( numbers ) neg ) ; ppush on neg                    ) ; loop                 )            ) ; cond        ) ; procedure    loop( nList nil nil )    ) ; proceduretrPartition( '( 3 -2 1 6 5 )) => ((5 6 1 3) (-2))
```

In this example, the`trPartition` function separates a list of integers into a list of non-negative elements and negative elements. The local `loop` function is recursive.

Sequencing and Iteration
------------------------

The following sequencing and iteration functions are provided in SKILL++:

* Use`begin` to construct a single expression from one or more expressions.

* Use`do` to iteratively execute one or more expressions.

* Use a`named let` construct to extend the `let` construct with a recursive iteration capability.

### Using begin

Use`begin` to construct a single expression from one or more expressions. The expressions are evaluated from left to right. The return value of the `begin` expression is the return value of the last expression in the sequence.

The`begin` function is equivalent to the `progn` function. The `progn` function is used to implement the { } syntax. Use the `begin` function to write SKILL++-compliant code.

#### Example 1

```
ILS-1> begin(    x = 0    printf( "Value of x: %d\n" ++x )     printf( "Value of x: %d\n" ++x )    x    ) ; beginValue of x: 1Value of x: 22
```

This example shows a transcript using the`begin` function.

#### Example 2

```
ILS-1> { x = 0    printf( "Value of x: %d\n" ++x )     printf( "Value of x: %d\n" ++x )    x }Value of x: 1Value of x: 22
```

This example uses the { } braces to group the same expressions.

### Using do

Use`do` to iteratively execute one or more expressions. The `do` expression allows multiple loop variables with arbitrary variable initializations and step expressions. You can specify

* One or more loop variables, including an initialization expression and a step expressionfor each variable.

* A termination condition that is evaluated before the body expressions are executed.

* One or more termination expressions that are evaluated upon termination to determinea return value.

#### Syntax Template for do Expressions

```
do( ( ( s_var1 g_initExp1 [g_stepExp1] )( s_var2 g_initExp2 [g_stepExp2] )…)    ( g_terminationExp g_terminationExp1 …)    g_loopExp1 g_loopExp2 …)=> g_value
```

A`do` expression evaluates in two phases: the initialization phase and the iteration phase.

The initialization expressions`g_initExp1`, `g_initExp2`, … are evaluated in an unspecified order and the results bound to the local variables `var1`, `var2`, …

The iteration phase is a sequence of steps going around the loop zero or more times with theexit determined by the termination condition.

* Each iteration begins by evaluating the termination condition.

* If the termination condition evaluates to a non-nil value, the`do` expression exits with a return value computed as follows:

* The termination expressions`terminationExp1`, `terminationEx`p2, … are evaluated in order. The value of the last termination condition is returned as the value of the `do` expression.

* Otherwise, the`do` expression continues with the next iteration as follows.

* The loop body expressions`g_loopExp1, g_loopExp2, …`are evaluated in order.

* The step expressions`g_stepExp1, g_stepExp2, …`, if given, are evaluated in an unspecified order.

* The local variables`var1, var2, …` are bound to the above results. Reiterate from step one.

#### Example 1

```
procedure( sumList( L )    do(        (            ( tail L cdr( tail ))            ( sum 0 sum + car( tail ))        )        ( !tail sum )        )    ) ; proceduresumList( nil ) => 0sumList( '( 1 2 3 4 5 6 7 )) => 28
```

#### Example 2

By definition, the sum of the integers 1, …, N is the Nth triangular number. The followingexample finds the first triangular number greater than a given limit.

```
procedure( trTriangularNumber( limit )    do(        (                     ;;; start loop variables            ( i 0 i+1 )            ( sum 0 )        ;;; no update expression                             ;;; same as ( sum 0 sum )        )                    ;;; end loop variables        ( sum > limit        ;;; test            sum              ;;; return result            )         sum = sum+i ;;; body        ) ; do    ) ; proceduretrTriangularNumber( 4 ) => 6trTriangularNumber( 5 ) => 6trTriangularNumber( 6 ) => 10
```

#### Example 3

```
procedure( approximateArea( dx fun lower upper )          do(       ( ; loop variables          ( sum               0.0       ;;; initial value              sum+fun(x)   ;; update              )                 ( x               lower  ;;; initial value              x+dx ;;; update expression              )          ) ; end loop vars      ( x >= upper ;;; exit test          dx*sum ;;; return value          )      ;;; no loop expressions      ;;; all work is in the update expression for sum      ) ; do    ) ; procedureapproximateArea( .001 lambda( ( x ) 1 ) 0.0 1.0 ) => 1 approximateArea( .001 lambda( ( x ) x ) 0.0 1.0 ) => .4995
```

The function`approximateArea` computes an approximation to the area under the graph of the `fun` function over the interval from `lower` to `upper`. It sums the values `fun(x),``fun(x+dx), fun(x+dx+dx) …`

#### Example 4: Using a Gauge When Computing the Area Under a Curve

```
procedure( makeGauge( tolerance )    let( ( ( iteration 0 ) ( previous 0.0 ) test )        lambda( ( value )            ++iteration            test = ( abs( value - previous ) <= tolerance )            previous = value            when( test list( iteration value ))            ) ; lambda        ) ; let    ) ; procedureprocedure( computeArea( fun lower upper tolerance )    let( ((gauge makeGauge( tolerance )) result )         do(            ( ; loop variables                 (                    dx                     1.0*(upper-lower)/2 ;;; initial value                    dx/2               ;;; update expression                    )                 ) ; end loop variables                  ( result =                 gauge( approximateArea( dx fun lower upper ))                result                )            nil ;;; empty body            ) ; do        ) ; let    ) ; procedurecomputeArea( lambda( ( x ) 1 ) 0 1 .00001 ) => ( 2 1.0 )computeArea( lambda( ( x ) x ) 0 1 .00001 ) => ( 16 0.4999924)pi = 3.1415computeArea( sin 0 pi/2 .00001 ) =>(18 0.9999507)
```

The`computeArea` function invokes `approximateArea` iteratively until two successive results fall within the given tolerance. The `dx` loop variable is initialized to `1.0*(upper-``lower)/2` and updated to `dx/2`. This example uses a gauge to hide the details of comparing successive results. The source for the `makeGauge` function is replicated for your convenience. See [Example 2](#1008281 "Using SKILL++") in the "Using procedure to Declare Local Functions" section for a discussion of `makeGauge` and gauges in general.

### Using a Named let

The`named` `let` construct extends the `let` construct with a recursive iteration capability. Besides the name you provide in front of the list of the local variables, the `named let` has the same syntax and semantics as the ordinary `let` except you can recursively invoke the named `let` expression from within its own body, passing new values for the local variables.

#### Syntax Template for Named let

```
let(     s_name     ( ( s_var1 g_initExp1 ) ( s_var2 g_initExp2 )… )    g_bodyExp1     g_bodyExp2     …    )
```

#### Example 1

```
let(     factorial     (( n 5 ))    if( n > 1         then             factorial( n-1)*n         else             1         )    ) ; let => 120
```

This example computes the factorial of 5 with a named`let` expression. Compare the example above with the following

```
let( (( n 5 ))    procedure( factorial( n )        if( n> 1             then                 n*factorial( n-1)            else                 1             ) ; if        ) ; procedure    factorial( n )    ) ; let => 120
```

and with the following

```
letrec(     ( ;;; variable list        ( n 5 )        ( factorial            lambda( ( n )                 if( n > 0 then n*factorial(n-1) else 1 ) ; if                ) ; lambda            ) ; f        ) ; variable list    factorial( n )    ) ; letrec => 120
```

#### Example 2

```
let( loop         ;;; name for the let    (             ;;; start let variables        ( numbers '( 3 -2 1 6 -5 ))        ( nonneg nil )        ( neg nil )        )       ;;; end of let variables    cond(        ( !numbers ;;; loop termination test and return result              list( nonneg neg )              )        ( car( numbers ) > 0 ;;; found a non-negative number             loop( ;; recurse                cdr( numbers )                cons( car( numbers ) nonneg )                neg                ) ; loop             )        ( car( numbers ) < 0 ;;; found a negative number            loop( ;; recurse                cdr( numbers )                nonneg                cons( car( numbers ) neg )                ) ; loop             )        ) ; cond    ) ;;; loop let=> ((613) (-5 -2))
```

This example separates an initial list of integers into a list of the negative integers and a listof the non-negative integers. Compare this example with the `trPartition` function in ["Example 3"](#1008290 "Using SKILL++") which explicitly relies on a local recursive function.

Software Engineering with SKILL++
---------------------------------

SKILL++ supports several modern software engineering methodologies, such as

* Procedural packages

* Modules

* Object-oriented programming with classes (see[Chapter 16, "SKILL++ Object System"](chap16.html#1008199 "SKILL++ Object System"))

SKILL++ also facilitates information hiding.`Information hiding` refers to using private functions and private data which are not accessible to other parts of your application. Information hiding promotes reusability and robustness because your implementation is easier to change with no adverse effect on the clients of the module.

SKILL++ Packages
----------------

A`package` is a collection of functions and data. Functions within a package can share private data and private functions that are not accessible outside the package. Packages are a hallmark of modern software engineering.

SKILL++ facilitates two approaches to packages.

* You can explicitly represent the package as an collection of function objects and data.Clients of the package use the arrow (`->`) operator to retrieve the package functions. Different packages can have functions with the same name.

* You might want to reimplement a collection of SKILL functions as a SKILL++ package.Informal SKILL packages have no opportunity to hide private functions or data. Reimplementing a SKILL package in SKILL++ provides the opportunity. Usually, you want to do this in a way that clients do not need to change their calling syntax. In this case, you do not need to represent the collection as a data structure. Instead, the package exports some of its function objects and hides the remainder.

### The Stack Package

```
Stack = let( ()    procedure( getContents( aStack )        aStack->contents        ) ; procedure    procedure( setContents( aStack aList )        aStack->contents = aList        ) ; procedure    procedure( ppush( aStack aValue )        setContents(             aStack             cons(                aValue                getContents( aStack )                ) ; cons            )        ) ; procedure    procedure( ppop( aStack )        letseq( (              ( contents getContents( aStack ))              ( v car( contents ))              )            setContents( aStack cdr( contents ))            v            ) ; letseq        ) ; procedure    procedure( new( initialContents )        list( nil 'contents initialContents )        ) ; procedure    list( nil 'ppop ppop 'ppush ppush 'new new )    ) ; let=> ( nil         ppop funobj:0x1c9b38         ppush funobj:0x1c9b28        new funobj:0x1c9b48 )
```

#### Using the Stack Package

```
S = Stack->new( '( 1 2 3 4 )) => (nil contents ( 1 2 3 4 ))Stack->ppop( S ) => 1Stack->ppush( S 1 ) => (1 2 3 4)
```

#### Comments

The Stack package is represented by a disembodied property list. Alternate representationssuch as a defstruct are possible. The only requirement is that the package data structure obey the `->` protocol.

Only the`ppush`, `ppop`, and `new` function are visible to the clients of the package.

The`ppush` and `ppop` functions use the `getContents` and `setContents` functions. If you choose a different representation for a stack, you only need to change the `new`, `getContents`, and `setContents` functions. The `getContents` and `setContents` functions are hidden to protect the abstract behavior of a stack.

### Retrofitting a SKILL API as a SKILL++ Package

```
define( stackPush nil )define( stackPop nil )define( stackNew nil )let( ()    procedure( getContents( aStack )        aStack->contents        ) ; procedure    procedure( setContents( aStack aList )        aStack->contents = aList        ) ; procedure    procedure( ppush( aStack aValue )        setContents(           aStack           cons(            aValue            getContents( aStack )            ) ; cons          )        ) ; procedure    procedure( ppop( aStack )        letseq( (            ( contents getContents( aStack ))            ( v car( contents ))            )          setContents( aStack cdr( contents ))          v          ) ; letseq        ) ; procedure    procedure( new( initialContents )        list( nil 'contents initialContents )        ) ; procedure    stackPush = ppush    stackPop = ppop    stackNew = newnil) ; let
```

#### Using the stackNew, stackPop, and stackPush Functions

```
S = stackNew( '( 1 2 3 4 )) => (nil contents (1 2 3 4)) stackPop( S ) => 1stackPush( S 5 ) => (5 2 3 4)
```

#### Comments

This example assumes`stackNew`, `stackPop`, and `stackPush` are the names of the functions to be exported from the stack package. As is customary, the package prefix `stack` informally indicates the functions that compose a package.

* The`getContents` and `setContents` functions are local functions invisible to clients.

* Using the`define` forms for `stackNew`, `stackPop`, and `stackPush` is not strictly necessary. Using the `define` form alerts the reader to those functions which the ensuing `let` expression assigns a value to an exported API.

### SKILL++ Modules

You can structure a SKILL++ module around a creation function, which the client invokes toallocate one or more instances of the module. The client passes an instance to a procedural interface.

The`makeStack` and `makeContainer` functions in the following examples are creation functions in the following sense: when you call `makeStack` it "creates" a stack instance. The stack instance is a function object whose internals can only be manipulated (outside of the debugger) by the `ppushStack` and `popStack` functions.

The creation function has

* Arguments

* Local variables

* Several local functions that can access the arguments to the creation function and cancommunicate between themselves through the local variables

The creation function returns one of the following, depending on the implementation:

* A single local function object

* A data structure containing several of the local function objects

* A single function object which dispatches control to the appropriate local functions

### Stack Module Example

A`stack` is a well-known data structure that allows the client to push a data value onto it and to pop a data value from it.

#### The Procedural Interface

The following table summarizes the procedural interface functions to the sample stackmodule.

|  |  |
| --- | --- | ---
| ****Action**** | **Function Call** | **Return Value**
| Allocate a stack. | makeStack( aList ) | Function object
| Push a value onto the stack. | pushStack( aStack aValue ) | A list of the stack contents
| Pop a value from the stack. | popStack( aStack ) | A popped value
The variable`aStack` is assumed to contain a stack object allocated by calling the `makeStack` function.

#### Allocating a Stack

`S = makeStack( '( 1 2 3 4 )) => funobj:0x1e36d8`

#### Popping a Value

`popStack( S ) => 1popStack( S ) => 2`

#### Pushing a Value on the Stack

`pushStack( S 5 ) => (5 3 4)`

Returns a list of stack contents at this point.

#### Implementing the makeStack Function

The`makeStack` function returns a function object. This function object is an instance of the stack module. In turn, this function object returns one of several functions local to the `makeStack` function.

```
procedure( makeStack( initialContents )    let( (( theStack initialContents ))                    procedure( ppush( value )            theStack = cons( value theStack )            )               procedure( ppop( )            let( (( v car( theStack ) ))                theStack = cdr( theStack )                v                )             )         lambda( ( msg)           ;;;; return a function object            case( msg                 ( ( ppush ) ppush )                ( ( ppop ) ppop )                ( t nil )                )             )         ) ; let    ) ; procedure
```

#### Implementing the pushStack and popStack Functions

The variable`aStack` contains a function object.

* When`aStack` is called, it returns the appropriate local function `ppush` and `ppop`.

* The`ppush` and `ppop` functions are within the lexical scope of the local variable `theStack`.

Notice the syntactic convenience of calling the stack object indirectly through the`fun` variable.

```
procedure( pushStack( aStack aValue )    let( ( ( fun aStack( 'ppush ) ) )                              ;;; retrieve local ppush function        fun( aValue )        ;;; call it        )     ) procedure( popStack( aStack )    let( ( ( fun aStack( 'ppop ) ) )                             ;;; retrieve local ppop function        fun()                ;;; call it        )     )
```

### The Container Module

`Containers` are like variables with an important difference. You can reset a container to the original value that you provided when you created the container.

#### The Procedural Interface

The following table summarizes the procedural interface to the sample container module. Thisinterface relies on the availability of several function objects in the container instance's data structure. The arrow (`->`) operator is used to retrieve the interface functions.

|  |  |
| --- | --- | ---
| **Action** | **Function Call** | **Return Value**
| Allocate a container withan initial value. | `aContainer =``makeContainer(aValue)` | A disembodied property listrepresenting the container instance.
| Return the container'scurrent value. | `aContainer->get()` | Current value in aContainer
| Store a new value in thecontainer. | `aContainer->set(``bValue)` | The container's new value.
| Reset the container to theinitial value | `aContainer->reset()` | The container's originalvalue.
#### Implementing the makeContainer Function

* The`makeContainer` function returns a disembodied property list containing the local functions as property values.

* The three functions`resetValue`, `setValue`, and `getValue` are local but are accessible through `makeContainer'`s return value.

* Unlike the stack module example, there are no global functions in the proceduralinterface.

> ```
> procedure( makeContainer( initialValue )    let( ( (value initialValue))        ;;; initialize the container        procedure( resetValue()         ;;; reset value              value = initialValue               )        procedure( setValue( newValue ) ;;; store new value              value = newValue               )        procedure( getValue( )          ;;; return current value               value               )        resetValue()                                list( nil                       ;;; the return value              'set setValue               'get getValue               'reset resetValue               )        ) ; let  ) ; procedure
> ```

#### Allocating Container Instances

```
x = makeContainer( 0 )     => (nil           set funobj:0x1e38f8           get funobj:0x1e3908           reset funobj:0x1e38e8 )
```

This example allocates a container instance with initial value 0.

```
y = makeContainer( 2 )    => (nil           set funobj:0x1e3928           get funobj:0x1e3938          reset funobj:0x1e3918 )
```

This example allocates a container instance with an initial value of 2. Notice that the returnedvalue contains different function objects.

#### Retrieving Container Values

`x->get() + y->get() => 2`

This example retrieves the values of the two containers and adds them. Notice theconventional function call syntax accepts an arrow (`->`) operator expression in place of a function name to access member functions.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
