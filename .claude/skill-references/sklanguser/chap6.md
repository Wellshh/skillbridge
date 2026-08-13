### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

6
=

Control Structures
==================

You can read about control structures in the following sections:

* [Control Functions](#1008203 "Control Structures")

* [Selection Functions](#1008252 "Control Structures")

* [Declaring Local Variables with prog](#1008269 "Control Structures")

* [Grouping Functions](#1008290 "Control Structures")

Control Functions
-----------------

The Cadence® SKILL language control functions provide a great deal of functionality familiar to users of a language such as C. These high-level control functions give SKILL additional power over most Lisp languages.

The control functions are also the biggest cause of inefficient code in the SKILL language.One of the inevitabilities of providing so many control structures is that some are more efficient than others and that there is a great deal of overlap between the functions. This means that it is easy for a programmer to choose a structure that works perfectly well for the task in hand, but is not in fact the best structure to use as far as efficiency and (even occasionally) readability are concerned.

A control function is any function that controls the evaluation of expressions given to it asarguments. The order of evaluation can depend on the result of evaluating test conditions, if any, given to the function. In addition to supporting standard control constructs such as `if/``while/for`, SKILL makes it easy for you to define control functions of your own. Because control functions in SKILL correspond to "statements" in conventional languages, this manual sometimes uses the terms interchangeably.

### Conditional Functions

Conditional functions test for a condition and perform operations when that condition is found.

There are four conditional functions available to the SKILL programmer:`if`, `when`, `unless`, and `cond`. These each have their own distinct characteristics and uses. Because the four functions carry out very similar tasks, it is very easy for the programmer to choose an inappropriate function. Choose a conditional function according to the following criteria:

|  |
| --- | ---
| if | There are exactly two values to consider, true and false.
|  |
| --- | ---
| when | There are statements to carry out when the test proves true.
|  |
| --- | ---
| unless | There are statements to carry out unless the test proves true.
|  |
| --- | ---
| cond | There is more than one test condition, but only the statements ofone test are to be carried out.
The`cond` function is discussed here. For a discussion of the `if, when,` and `unless` functions, refer to ["Getting Started"](chap1.html#1008199 "Getting Started").

#### The cond Function

The`cond` function offers multiway branching.

```
cond(       ( condition1 exp11 exp12 … )      ( condition2 exp21 exp22 … )      ( condition3 exp31 exp32 … )      ( t expN1 expN2 … )      ) ; cond
```

The`cond` function

* Sequentially evaluates the conditions in each branch until it finds one that is non-`nil`. It then executes all the expressions in the branch and exits.

* Returns the last value computed in the branch it executes.

The`cond` function is equivalent to

```
if           condition1       exp11   exp12 …else if      condition2       exp21   exp22 …else if      condition3       exp31   exp32 ……else     expN1expN2 ….
```

For example, this version of the`trClassify` function is equivalent to the one using the `prog` and `return` functions in ["The return Function"](#1008283 "Control Structures").

```
procedure( trClassify( signal )       cond(             ( !signal nil )             ( !numberp( signal ) nil )             ( signal >= 0 && signal < 3 'weak )             ( signal >= 3 && signal < 10 'moderate )             ( signal >= 10 'extreme )             ( t          'unexpected )             ) ; cond       ) ; procedure
```

### Iteration Functions

There are two basic iteration functions available in the SKILL language:`while` and `for`. These are both very general functions that have many uses.

#### The while Function

The`while` function is the more general function because everything that can be done with a `for` can be done with a `while`.

When using the`while` function remember that all parts of the test condition are evaluated on each pass of the loop. This means that if there are parts of the test that do not depend on the contents of the loop, they should be moved outside of the loop. Consider the following code:

`while( i < length(myList)      …      i++)`

If the value of the symbol`myList` does not change within this loop, the value of `length(myList)` is being re-evaluated on each loop for no reason. It would be better to assign the value of`length(myList)` to a variable before starting the `while` loop.

When using a`while` loop, consider whether it would be better to use one of the list iteration and quantifier functions such as `foreach`, `setof`, or `exists`.

#### The for Function

The main advantage of the`for` function is that it automatically declares the loop variable. This means that the variable does not need to be declared in a local variable section of a structure such as `prog` or `let`. It also means that the variable cannot be used outside the loop, which differs from the case in C. Consider the following code:

```
for( i 1 length(myList)      evaluateList(i))if( i == 0      printf("The list was empty!\n"))
```

The`if` test is incorrect because the variable `i` will be unbound by the time it is executed.

Selection Functions
-------------------

There are two selection functions in SKILL:`caseq` and `case`. The difference between these functions is the range of values that are allowed within the test conditions.

`caseq` is a considerably faster version of `case`. `caseq` uses the function `eq` rather than `equal` for comparison. The comparators for `caseq` are therefore restricted to being either symbols or small integer constants (-256 <= i <= 255), or lists containing symbols and small integer constants.

The`caseq` and `case` functions allow lists of elements within the test parts and match if the test value is `eq` or `equal` to one of those elements, as appropriate.

One common fault with the use of the`caseq` function is the misconception that the values in the conditional part of the function are evaluated. Consider the following call to `caseq`:

`caseq( x ('a "a") ('b "b"))`

The conditional parts of this,`'a` and `'b`, are `not` evaluated, so this code equates to

`caseq( x ((quote a) "a") ((quote b) "b"))`

That is, if the value of`x` is the symbol `a` or is the symbol `quote`, `caseq` returns the value `a`. This is clearly not what was actually required.

Be careful when using symbols in these selection functions because the symbol`t` indicates the default case and should not therefore be used. For example, consider the case where a function returns one of the values `t`, `nil`, or `indeterminate`.

It might be tempting to write a function such as

```
caseq( value (t                  printf("Suceeded.\n")) (nil                printf("Failed.\n")) (indeterminate      printf("Indeterminate.\n")))
```

But this function will not work because the`t` case is the default and always matches. The correct way to write this test is

```
caseq( value (nil                printf("Failed.\n")) (indeterminate      printf("Indeterminate.\n")) (t                  when( eq(value,t)                          printf("Succeeded.\n")                     )      )) /* caseq */
```

The problem can also be avoided by putting the`t` within parentheses because the default case only matches against a single `t`. This is not recommended because it is an implementation dependency. The SKILL Lint program always warns of dubious uses of the `t` case in a selection function.

Declaring Local Variables with prog
-----------------------------------

All variables that appear in a SKILL program are global to the whole program unless they areexplicitly declared as local variables. You declare local variables using the `prog` control construct, which initializes all its local variables to `nil` upon entry and restores their original values (that is, the values of the variables before the `prog` was executed) upon exit from the `prog`.

A symbol's current value is accessible at any time from anywhere. The SKILL interpretertransparently manages a symbol's value slot as if it were a stack.

* The current value of a symbol is simply the top of the stack.

* Assigning a value to a symbol changes only the top of the stack.

Whenever your program invokes the`prog` function, the system pushes a temporary value onto the value stack of each symbol in the local variable list. When the flow of control exits, the system pops the temporary value off the value stack, restoring the previous value.

### The prog Function

The`prog` function allows an explicit loop to be written since `go` is supported within the `prog`. In addition, `prog` allows you to have multiple return points through use of the function `return`. If you are not using either of these two features, `let` is much simpler and faster.

If you need to conditionally exit a collection of SKILL statements, use the`prog` function. A list of local variables and your SKILL statements make up the arguments to the `prog` function.

`prog( ( local variables ) your SKILL statements )`

### The return Function

Use the`return` function to force the `prog` to immediately return a value skipping over subsequent statements. If you do not call the `return` function, the `prog` expression returns `nil`.

Example: The`trClassify` function returns either `nil, weak, moderate,``extreme,` or `unexpected` depending on `signal`. It does not use any local variables.

```
procedure( trClassify( signal )       prog( ()             unless( signal return( nil ))             unless( numberp( signal )return( nil ))             when( signal >= 0 && signal < 3return( 'weak ))             when( signal >= 3 && signal < 10return( 'moderate ))            when( signal >= 10return( 'extreme ))            return( 'unexpected )             ) ; prog       ) ; procedure
```

Use the`prog` function and the `return` function to exit early from a `for` loop. This example finds the first odd integer less than or equal to 10.

```
prog( ( )      for( i 0 10             when( oddp( i )                  return( i )                  ) ; when            ) ; for      ) ; prog
```

Grouping Functions
------------------

Three main functions allow the grouping of statements where only a single statement wouldotherwise be allowed. These functions are `prog`, `let`, and `progn`. In addition, the `let` and `prog` functions allow for the declaration of local variables. The `prog` function also allows for the use of`return` statements to jump out from within a piece of code and the `go` function, along with labels, to jump around within the code.

When considering whether to use`prog`, `let`, or `progn`, the function with the least extra functionality should be used at all times because the functions are progressively more expensive in terms of run time. Use the functions as follows:

* If local variables and jumps are not needed, use a`progn`.

* If local variables are needed but not jumps, use a`let`.

* Only if jumps are really needed, use a`prog`.

### Using prog, return, and let

The`prog` statement should be used only when it is absolutely necessary. Its overuse is one of the biggest causes of inefficiency in all SKILL code. Returning from the middle of a piece of code is not only highly expensive, but can also lead to code that is difficult to read and understand. As with all high level programming languages, the use of `go` (the SKILL `goto' statement) is highly discouraged. There are cases when it is necessary, but these are few.

A programmer usually uses the`prog` form when a certain amount of error checking must be done at the start of a function, with the rest of the function only being carried out if the error checking succeeds. Consider the following piece of code:

```
procedure(check(arg1 arg2) prog( ()          when(illegal_val(arg1)                  printf("Arg1 in error.\n")                  return()            ) /* end when */            when(illegal_val(arg2)                  printf("Arg2 in error.\n")                  return()            ) /* end when */
```

`Rest of code … ) /* end prog */) /* end check */`

This code is reasonably clear, except that it is easy for someone to miss the`return` statements, and it uses the `prog` form. Consider the following alternative. This code seems to be a longer procedure, but it is clearer, faster, and more maintainable:

```
procedure(check(arg1 arg2)      cond(            ( illegal_val(arg1)                  printf("Arg1 in error.\n")                  nil            ) /* check arg1 */
```

```
(illegal_val(arg2)                  printf("Arg2 in error.\n")                  nil            ) /* check arg2 */
```

`(t                  Rest of code …      ) ) /* end cond */) /* end check */`

A separate function could be called from within the`t` condition, which could expect its arguments to be correct. This would, at the small cost of an extra function call, separate the error checking code completely from the main body of the function, thereby making it even easier for programmer maintaining the code to see exactly what is involved in the function, without having to worry about the peripheral interfaces.

Another common mistake with the use of the`prog` and `let` functions is the initialization of the local variables to `nil`. All local variables in a `prog` or `let` are automatically initialized to `nil`. Remember that the`let` function allows local variables to be initialized within the declaration. This saves both time and space, and, as long as care is taken over the layout of the code, can be no less readable:

```
procedure(test()      let( ((localvar1 initvalue1)            (localvar2 initvalue2)            localvar3                   /* initial value nil */            )      Rest of code …       ) /* end let */) /* end procedure */
```

When setting initial values within the declaration, reference cannot be made to other localvariables. For example, the following is wrong:

```
procedure(incorrect(list) let( ((listHead         car(list))            (headval       car(listHead)) /* WRONG!!! */            )            Rest of code …
```

Note that the`prog` and `let` functions have different return values.

* The`prog` function returns the value given in a `return` statement or, if it exits without a `return`, returns `nil`.

* The`let` function always returns the value of the last statement.

This means that in converting a`prog` to a `let`, it might be necessary to add an extra `nil` to the end of the function.

### Using the progn Function

The`progn` function is a simple means of grouping statements where multiple statements are required, but only one is expected.

An example is the`setof` function, which only allows a single statement in the conditional part.

Remember that there is an overhead in using`progn`. It should only be used where there is more than one statement, and only one statement is allowed.

### Using the prog1 and prog2 Functions

Two minor grouping functions that have roughly the same overhead as the`progn` function are `prog1` and `prog2`.

#### The prog1 Function

`prog1` evaluates expressions from left to right and returns the value of the first expression.

`prog1(      x = 5      y = 7 )=> 5`

#### The prog2 Function

`prog2` evaluates expressions from left to right and returns the value of the second expression.

`prog2(       x = 4       p = 12      x = 6 )=> 12`

`prog1` and `prog2` are often useful when a local variable would otherwise be needed to hold a temporary variable before that variable is returned. These two functions should be used with caution, because they can detract from the readability of the program, and they are generally only useful where otherwise a `let` would be necessary. For example:

```
procedure(main()      let( (status)            initialize()            /* Main body of program */            status = analyzeData()             wrapUp()/* Return the status */            status      ) /* end let */) /* end main */
```

This code can be more efficiently (but less clearly) implemented using a`prog2`:

```
procedure(main()    prog2(            initialize()            /* Main body of program.            * The value of this will be returned by prog2.            */            nalyzeData()            wrapUp()      ) /* end prog2 */) /* end main */
```




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
