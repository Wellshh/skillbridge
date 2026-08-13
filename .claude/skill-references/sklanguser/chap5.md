### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

5
=

Arithmetic and Logical Expressions
==================================

*Expressions* are Cadence® SKILL language objects that also evaluate to SKILL objects. SKILL performs a computation as a sequence of function evaluations. A SKILL *program* is a sequence of expressions that perform a specified action when evaluated by the SKILL interpreter. The three types of primitive expressions in SKILL are constants, variables, and function calls. You can combine constants, variables, and function calls with *operators* to form arithmetic and logical expressions (see ["Creating Arithmetic and Logical Expressions"](#1008226 "Arithmetic and Logical Expressions")).

A*constant* is an expression that evaluates to itself. That is, evaluating a constant returns the constant itself. For example:

`123`

`10.5`

`"abc"`

A*variable* stores values used during the computation and returns its value when evaluated. For example:

`a`

`x`

`init_var`

When SKILL creates a variable, it gives the variable an initial value of`unbound` (*that-value-**which-represents-no-value*). If the interpreter encounters an unbound variable, you get an error message. You must initialize all variables. For example:

`myVariable = 5`

**Note:** You will encounter the unbound variable error message if you misspell a variablebecause the misspelling creates a new variable.

A*function call* applies the named function to the list of arguments and returns the result when called. For example:

`f(a b c d)`

`abs(-123)`

`exit()`

See the following sections for more information:

* [Creating Arithmetic and Logical Expressions](#1008226 "Arithmetic and Logical Expressions")

* [Differences Between SKILL and C Syntax](#1008946 "Arithmetic and Logical Expressions")

* [SKILL Predicates](#SKILL Predicates "Arithmetic and Logical Expressions")

* [Type Predicates](#1012520 "Arithmetic and Logical Expressions")

Creating Arithmetic and Logical Expressions
-------------------------------------------

You can combine constants, variables, and function calls with*infix* operators such as less than (<), colon (:), and greater than (>) to form arithmetic and logical expressions. For example:

`1+2`

`a*b+c`

`x>y`

You can form arbitrarily complicated expressions by combining any number of primitiveexpressions (constants, variables, and function calls) and operators.

For more information about creating arithmetic and logical expressions, see the following:

* [Role of Parentheses](#1008231 "Arithmetic and Logical Expressions")

* [Quoting to Prevent Evaluation](#1008237 "Arithmetic and Logical Expressions")

* [Arithmetic and Logical Operators](#operator_table "Arithmetic and Logical Expressions")

* [Predefined Arithmetic Functions](#1008555 "Arithmetic and Logical Expressions")

* [Bitwise Logical Operators](#1008660 "Arithmetic and Logical Expressions")

* [Bit Field Operators](#1008696 "Arithmetic and Logical Expressions")

* [Mixed-Mode Arithmetic](#1018988 "Arithmetic and Logical Expressions")

* [Function Overloading](#1008854 "Arithmetic and Logical Expressions")

* [Integer-Only Arithmetic](#1008861 "Arithmetic and Logical Expressions")

* [True (non-nil) and False (nil) Conditions](#1012306 "Arithmetic and Logical Expressions")

* [Controlling the Order of Evaluation](#1008894 "Arithmetic and Logical Expressions")

* [Testing Arithmetic Conditions](#1008904 "Arithmetic and Logical Expressions")

### Role of Parentheses

Parentheses delimit the names of functions from their argument lists and delimit nestedexpressions. In general, the innermost expression of a nested expression is evaluated first, returning a value used in turn to evaluate the expression enclosing it, and so on until the expression at the top level is evaluated.

Parentheses resemble natural mathematical notation and are used in both arithmetic andcontrol expressions.

### Quoting to Prevent Evaluation

Occasionally you might want to prevent expressions from being evaluated. This is done by"quoting" the expression, that is, putting a single quote just before the expression.

#### Quoting Variables

Quoting is often used with the names of variables and their values. For example, putting asingle quote before the variable `a` (that is, `'a`) prevents `a` from being evaluated. Instead of returning the value of `a`, the name of the variable `a` is returned when `'a` is evaluated.

#### Quoting Lists

You generally specify lists of data within a program by quoting. Quoting is necessary becauseof the common list representation used for both program and data. For example, evaluating the list `(f a b c)` leads to the interpretation that `f` is the name of a function and `(a b c)` is a list of arguments for `f`. By quoting the same list, `'(f a b c)`, the list is instead treated as a data list containing the four elements `f, a, b,` and `c`.

#### Try It Out

The best way to understand evaluation and quoting is by trying them out in SKILL. Aninteractive session with the SKILL interpreter will help to clarify and reinforce many of the concepts just described.

### Arithmetic and Logical Operators

All arithmetic operators are translated into calls to predefined SKILL functions. Theseoperators are listed in the table below in descending order of operator precedence. The table also lists the names of the functions, which can be called like any other SKILL function.

Error messages report problems using the name of the function. The letters in the Synopsiscolumn refer to data types. Refer to the [Data Types](chap2.html#1013610 "Language Characteristics") for a discussion of data type characters.

**Arithmetic and Logical Operators**

| **Name of Function(s)** | **Synopsis** | **Operator**
| Data Access |  |
| arrayref | a[index] | [ ]
| setarray | a[index] = expr |
| bitfield1 | x<bit> | <>
| setqbitfield1 | x<bit>=expr |
| setqbitfield | x<msb:lsb>=expr |
| quote | 'expr | '
| getqq | g.s | .
| getq | g->s | ->
| putpropqq | g.s = expr, g->s = expr | ~>
| putpropq | d~>s, d~>s = expr |
| Unary |  |
| preincrement | ++s | ++
| postincrement | s++ | ++
| predecrement | --s | --
| postdecrement | s-- | --
| minus | -n | -
| null | !expr | !
| bnot | ~x | ~
| Binary |  |
| expt | n1 \*\* n2 | \*\*
| times | n1 \* n2 | \*
| quotient | n1 / n2 | /
| plus | n1 + n2 | +
| difference | n1 - n2 | -
| leftshift | x1 << x2 | <<
| rightshift | x1 >> x2 | >>
| lessp | n1<n2 | <
| greaterp | n1>n2 | >
| leqp | n1<=n2 | <=
| geqp | n1>=n2 | >=
| equal | g1 == g2 | ==
| nequal | g1 != g2 | !=
| band | x1 & x2 | &
| bnand | x1 ~& x2 | ~&
| bxor | x1 ^ x2 | ^
| bxnor | x1 ~^ x2 | ~^
| bor | x1 | x2 |
| bnor | x1 ~| x2 | |, ~|
| and | rel. expr && rel. expr | &&
| or | rel. expr || rel. expr | ||
| range | g1 : g2 | :
| setq | s = expr | =
| **Inplace Operators** | |
| plus | a = a + b | +=
| minus | a = a - b | -=
| divide | a = a / b | /=
| multiply | a = a \* b | \*=
| expt | a = a \*\* b | \*\*=
| bor | a = a | b | |=
| band | a = a & b | &=
| bxor | a = a ^ b | ^=
| leftshift | a = a<< b | <<=
| riightshift | a = a >> b | >>=
The following table gives more details on some of the arithmetic operators.

**More on Arithmetic Operators**

| **Arithmetic Operator** | **Comments**
| `+, -, *,` and `/` | Perform addition, subtraction, multiplication, and divisionoperations.
| Exponentiation operator`**` | Has the highest precedence among the binary operators.
| Shift operators (`<<, >>`) | Shift their first arguments left or right by the number of bitsspecified by their second arguments. Both the left and right shifts are logical (that is, vacated bits are 0-filled).
| Preincrement operator (++ appearing before the name of a variable) | Takes the name of a variable as its argument, increments itsvalue (which must be a number) by one, stores it back into the variable, and then returns the incremented value.
| Postincrement operator (++ appearing after the name of a variable) | Takes the name of a variable as its argument, increments itsvalue (which must be a number) by one, and stores it back into the variable.  However, it returns the original value stored in the variable as the result of the function call.
| Predecrement andpostdecrement operators | Similar to pre- and postincrement, but they decrementinstead of increment the values of their arguments by one.
| Range operator (:) | Evaluates both of its arguments and returns the results as atwo-element list. It provides a very convenient way of grouping a pair of data values for subsequent processing. For example, 1:3 returns the list `(1``3).`
### Predefined Arithmetic Functions

In addition to the basic infix arithmetic operators, several functions are predefined in SKILL.

**Predefined Arithmetic Functions**

| **Synopsis** | **Result**
| **General Functions** |
| add1(n) | n + 1
| sub1(n) | n - 1
| abs(n) | Absolute value of n
| exp(n) | e raised to the power n
| log(n) | Natural logarithm of n
| max(n1 n2 …) | Maximum of the given arguments
| min(n1 n2 …) | Minimum of the given arguments
| mod(x1 x2) | x1 modulo x2, that is, the integer remainder of dividing x1 by x2
| round(n) | Integer whose value is closest to n
| sqrt(n) | Square root of n
| sxtd(x w) | Sign-extends the rightmost w bits of x, that is, the bit field x<w-1:0> with x<w-1> as the sign bit
| zxtd(x w) | Zero-extends the rightmost w bits of x, executes faster thandoing x<w-1:0>
| **Trigonometric Functions** |
| sin(n) | sine, argument n is in radians
| cos(n) | cosine
| tan(n) | tangent
| asin(n) | arc sine, result is in radians
| acos(n) | arc cosine
| atan(n) | arc tangent
| **Random Number Generator** |
| random(x) | Returns a random integer between 0 and x-1. If random iscalled with no arguments, it returns an integer that has all of its bits randomly set.
| srandom(x) | Sets the initial state of the random number generator to x
### Bitwise Logical Operators

Theb`not, band, bnand, bxor, bxnor, bor,` and `bnor` operators all perform bitwise logical operations on their integer arguments.

**Bitwise Logical Operators**

| **Meaning** | **Operator**
| bitwise AND | &
| bitwise inclusive OR | |
| bitwise exclusive OR | ^
| left shift | >>
| right shift | <<
| one's complement (unary) | ~
### Bit Field Operators

Bit field operators operate on bit fields stored inside 32-bit words. To avoid confusion innaming bits, SKILL uses the uniform convention that the least significant bit in an integer is bit 0, with the bit number increasing as you move left in the direction of the most significant bit.

* You can select bit fields by naming the leftmost and the rightmost bits in the bit field orby just naming the bit if the bit field is only one bit wide.

* You can use either integer constants or integer variables to specify bit positions, butexpressions are not allowed.

* All bit fields are treated as unsigned integers.

* Use the`sxtd` function for sign-extending a bit field.

#### Bit Field Examples

`x = 0b01101     => 13`

Assigns`x` to 13 in binary.

`x<0>         => 1`

The contents of the rightmost bit of`x` is 1.

`x<1>         => 0`

The contents of bit one of`x` is 0.

`x<2:0>         => 5`

Extracts the contents of the rightmost three bits of`x`. These are `101` or 5 in decimal.

`x<7:4> = 0b1010 => 173`

Stores the bit pattern into the bits 4 through 7.

`(x + 4)<4:3>    => 2`

Adds 4 to`x`, then extracts the 3rd and 4th bits. 173 plus 4 is 177. SKILL returns the result of the last expression, which is binary `10` or 2 decimal.

#### Calling Conventions for Bit Field Functions

Because of limitations in the grammar, only integer constants or names of variables arepermitted inside the angle brackets. To use the value of an expression to specify a bit position, you must either first assign the value of the expression to a variable or directly call the bit field functions without using the less than (<), colon (:), and greater than (>) infix operators. The calling conventions for the bit field functions are as follows:

`bitfield1(       x_value       x_bitPosition )`

`setqbitfield1(       s_name       x_newvalue       x_bitPosition )`

`bitfield(       x_value       x_leftmostBit       x_rightmostBit )`

```
setqbitfield(       s_name       x_newvalue       x_leftmostBit       x_rightmostBit )
```

### Mixed-Mode Arithmetic

SKILL makes a distinction between integers and floating-point numbers.

* Integer arithmetic is used if all the arguments given to an arithmetic operator areintegers.

* Floating-point arithmetic is used if all arguments are floating-point numbers.

* When integers and floating-point numbers are mixed, SKILL uses integer arithmetic untilit encounters a floating-point number. SKILL then switches to floating-point arithmetic and returns a floating-point number as the result.

See the following topics for more information:

* [Floating-Point Issues](#fpIssues "Arithmetic and Logical Expressions")

* [Integer vs. Floating-Point Division](#intvsfloat "Arithmetic and Logical Expressions")

* [Type Conversion Functions (fix and float)](#fixTip "Arithmetic and Logical Expressions")

* [Comparing Floating-Point Numbers](#comparefloatnum "Arithmetic and Logical Expressions")

#### Floating-Point Issues

Because IEEE floating-point numbers use what are essentially binary (base 2) fractions torepresent real numbers, some functions that operate on floating-point numbers yield unexpected (and incorrect) results.

There are some floating-point numbers that the computer cannot represent exactly as binaryfractions. In these cases, the computer uses a binary (base 2) floating-point number to approximate your decimal (base 10) floating-point number. These approximations can lead to incorrect results for some functions that operate on floating-point numbers. Consider the following:

|  |  |  |
| --- | --- | --- | ---
| **Decimal fraction** | **Equivalent** | **Binary fraction** | **Result**
| 0.125 | 1/10 + 2/100 + 5/1000 | 0.001 | Exact representation
| 0.3333… | 3/10 + 3/100 + 3/1000… | 0.010101010101… | Approximation
| .1 | 1/10 | 0.0001100110011… | Approximation
Binary representation can result in a loss of precision. Also, when a program does not saveor retrieve the least significant bits of a number, that number loses precision. See also ["Comparing Floating-Point Numbers"](#comparefloatnum "Arithmetic and Logical Expressions") and ["Type Conversion Functions (fix and float)"](#fixTip "Arithmetic and Logical Expressions").

**Note:** Some applications use single precision to represent floating-point numbers. SKILLuses double precision.

#### Integer vs. Floating-Point Division

The division operator requires special attention because

* Integer division truncates its results

* Floating-point division computes an exact number

#### Type Conversion Functions (fix and float)

Before you can compare an integer to a floating-point number, you must convert bothnumbers to the same type (that is, `integer` or `float`).

**Note:** See also["Comparing Floating-Point Numbers"](#comparefloatnum "Arithmetic and Logical Expressions") for more information.

The`fix` and `fix2` functions converts a floating-point number and floating-point calculations, respectively, to an integer. The `float` function converts an integer to a floating-point number. If the argument given to `fix` or `float` is already of the desired type, the argument is returned. See [*Cadence SKILL Language Reference*](../sklangref/sklangrefTOC.md) for more information about these functions.

* Because of the["Floating-Point Issues"](#fpIssues "Arithmetic and Logical Expressions"), you can pass a floating-point argument to the `fix` function that yields an incorrect result. For example:

> `Skill > fix(4.1 * 100)409`

> `Skill > fix((30 - 18.1) * 10)118`

* You can load the following SKILL file (`real_fix.il`) into your SKILL development environment to force correct results in cases like those shown above.

> ```
> procedure(real_fix(number)let( (num_string fix_num)sprintf( num_string, "%f" number)fix_num = atoi(car(parseString(num_string)))fix_num));
> ```

#### Comparing Floating-Point Numbers

**Note:** Two numbers can only be equal if they are of the same type (either`integer` or `float`) and have identical values. Two floating-point numbers can appear the same when printed while differing internally in their least significant bits.

Simple comparison rarely works for floating-point numbers. For example:

`if( (a == b) println("same"))`

You can compare against an acceptable tolerance range with more success as follows(assuming `a` is not zero):

`if( (abs(a - b)/a < 1e-6) println("same"))`

You can also use the`fix2` for rounding the result in floating-point calculations. This function returns the largest integer not larger than the given argument.

* ***Unless two floating-point numbers are assigned identical constants orare generated by exactly the same sequence of computations, it is unlikely SKILL will treat them as equal when compared.***

You can think of a loop (such as`for`) as a special case of comparing floating-point numbers. Each time a program increments a floating-point loop variable, the number can lose precision resulting in a cummulative error. Under these circumstances, your loop might not execute the expected number of times.

### Function Overloading

Some applications that are based on SKILL overload the arithmetic and/or bit-level functionswith new or modified semantics. While `sqrt(-1)` normally signals an error in SKILL, it returns a valid result as a complex number when some applications are running.

Because the arithmetic and bit-level operators are just simpler syntax for calling theircorresponding functions, by overloading these functions with extended semantics for new data types, you can use the same familiar notation in writing expressions involving objects of these new data types.

By overloading the`plus`, `difference`, `times`, and `quotient` functions for a complex-number data type, you can use +, -, \*, and / in forming arithmetic expressions involving complex numbers as you normally do in writing mathematical formulas.

* ***This kind of function overloading is done by the individual application.There is no support for user-definable function overloading in SKILL. Refer to the reference manuals of the individual applications for more details about which functions/operators have been overloaded and what semantics to use.***

### Integer-Only Arithmetic

In addition to standard arithmetic functions that can handle integers and floating-pointnumbers, SKILL provides several integer-only arithmetic functions that are slightly faster than the standard functions. These functions are named by prepending x to the names of the corresponding standard functions: xdifference, xplus, xquotient, and xtimes.

When integer mode is turned on using thesstatus function, the SKILL parser translates all arithmetic operators into calls on integer-only arithmetic functions. This results in small execution time savings and makes sense only for compute-intensive tasks whose inner loops are dominated by integer arithmetic calculations.

`sstatus( integermode t)=> t`

Turns on integer mode.

`status( integermode )=> t`

Checks the status of`integermode` and returns `t` if `integermode` is on. The default is off.

The internal variables are typically Boolean switches that accept only the Boolean values of`t` and nil. For efficiency and security, system variables are stored as internal variables that can only be set by status, rather than as SKILL variables you can set directly. Refer to ["Names of Variables"](chap2.html#1010007 "Language Characteristics") for a discussion of internal variables.

### True (non-nil) and False (nil) Conditions

Unlike C or other programming languages that use integers to represent true and falseconditions, SKILL uses the nonnumeric special atom `nil` to represent the false condition. The true condition is represented by the special atom `t`or anything other than `nil.`

#### Relational Operators

The relational operators`lessp` (<), `leqp` (<=), `greaterp` (>), `geqp` (>=), `equal` (==), and `nequal`(!=) operate on numeric arguments and return either `t` or `nil` depending on the results.

#### Logical Operators

The logical operators`and`(&&), `or` (||), and `null` (!), on the other hand, operate on nonnumeric arguments that represent either the false (`nil`) or true (non-`nil`) conditions.

#### False/True Conditions Do Not Equal Constants 0 and 1

If you program in C, be especially careful not to interpret the false/true conditions asequivalent to the integer constants 0 and 1.

#### Testing for Equality and Inequality

You can also use the`equal` (==) and the `nequal` (!=) operators to test for the equality and inequality of nonnumeric atoms.

* Two atoms are equal if they are the same type and have the same value.

* Two lists are equal if they contain exactly the same elements.

### Controlling the Order of Evaluation

The binary operators && and || are often used to control the order of evaluation.

#### The && Operator

The && operator evaluates its first argument and, if the result is`nil`, returns `nil` without evaluating the second argument. If the first argument evaluates to non-`nil`, && proceeds to evaluate the second argument and returns that value as the value of the function.

#### The || Operator

The || operator also evaluates its first argument to see if the result is non-`nil`. If so, || returns that result as its value and the second argument is not evaluated. If the first argument evaluates to `nil`, || proceeds to evaluate the second argument and returns that value as the value of the function.

### Testing Arithmetic Conditions

In addition to the six infix relational operators, several arithmetic predicate functions areavailable for efficient testing of arithmetic conditions. These predicates are listed in the table below.

**Arithmetic Predicate Functions**

| **Synopsis** | **Result**
| minusp(n) | `t` if n is a negative number, `nil` otherwise
| plusp(n) | `t` if n is a positive number, `nil` otherwise
| onep(n) | `t` if n is equal to 1, `nil` otherwise
| zerop(n) | `t` if n is equal to 0, `nil` otherwise
| evenp(x) | `t` if x is an even integer, `nil` otherwise
| oddp(x) | `t` if x is an odd integer, `nil` otherwise
Differences Between SKILL and C Syntax
--------------------------------------

Arithmetic and logical expressions in SKILL are the same as in the C programming languagewith the following minor differences:

* SKILL supports the following exponentiation operator:`**` (two asterisks).

* The function`mod` replaces the modulo operator "`%`" so that you do not have to use "`%`" for this infrequently-used function: Use `mod(i j)` instead of `i % j`.

* The more general`if/then/else` control construct in SKILL makes the conditional expression operators `?` and `:` obsolete.

* The indirection operator`*` and the address operator `&` do not have any meaning in SKILL and are not supported.

* The set of bitwise operators is augmented by`~&` (nand), `~|` (nor), and `~^` (xnor).

* Logical expressions that evaulate to false return the special atom`nil` and those that evaluate to true return any non-`nil` value (usually, the special atom `t`).

SKILL Predicates
----------------

The following predicate functions test for a condition:

* [The atom Function](#1008965 "Arithmetic and Logical Expressions")

* [The boundp Function](#1008970 "Arithmetic and Logical Expressions")

For a list of predicate functions for testing the type of a data object, see["Type Predicates"](#Type Predicates "Arithmetic and Logical Expressions").

### The atom Function

`atom` checks if an object is an atom. Atoms are all SKILL objects (except nonempty lists). The special symbol `nil` is both an atom and a list.

`atom( 'hello ) => t`

`x = '(a b c)atom( x ) => nilatom( nil ) => t`

### The boundp Function

`boundp` checks if a symbol is bound (has an assigned value).

`x = 5                ; Binds x to the value 5.y = 'unbound         ; Unbinds y`

`boundp( 'x ) => t`

`boundp( 'y ) => nil`

```
y = 'x               ; Binds y to the constant x.boundp( y ) => t     ; Returns t because y evaluates to x, which is bound.
```

### Using Predicates Efficiently

Some predicates are faster than others. For example, the`eq`, `neq`, `memq`, and `caseq` functions are faster than their close relatives the `equal`, `nequal`, `member`, and `case` functions.

The`equal, nequal, member`, and `case` functions compare values while the `eq`, `neq`, `memq`, and `caseq` functions test if the objects are the same. That is, they test whether the objects reside in the same location in virtual memory.

These functions result in quicker tests but might require that you alter your application to takeadvantage of them.

### The eq Function

`eq` checks addresses when testing for equality. The `eq` function returns `t` if both arguments are the same object in virtual memory. You can test for equality between symbols using `eq` more efficiently than using the == operator. The following example illustrates the differences between `equal` (==) and `eq` for lists.

```
list1 = '( 1 2 3 )           => ( 1 2 3 )list2 = '( 1 2 3 )           => ( 1 2 3 )list1 == list2               => teq( list1 list2 )            => nillist3 = cons( 0 list1 )      => ( 0 1 2 3 )list4 = cons( 0 list1 )      => ( 0 1 2 3 )list3 == list4               => teq( cdr( list3 ) list1 )     => taList = '( a b c )           => a b ceq( 'a car( aList ) )        => t
```

### The equal Function

`equal` tests for equality.

* If the arguments are the same object in virtual memory (that is, they are`eq`), `equal` returns `t`.

* If the arguments are the same type and their contents are equal (for example, strings withidentical character sequence), `equal` returns `t`.

* If the arguments are a mixture of fixnums and flonums,`equal` returns `t` if the numbers are identical (for example, `1.0` and `1`).

This test is slower than using`eq` but works for comparing objects other than symbols.

`x = 'cat equal( x 'cat )      => t`

`x == 'dog            => nil; == is the same as equal.`

`x = "world" equal( x "world" )  => t`

`x = '(a b c) equal( x '(a b c))  => t`

### The neq Function

`neq` checks if two arguments are not equal, and returns `t` if they are not. Any two SKILL expressions are tested to see if they point to the same object.

`a = 'dogneq( a 'dog )        => nilneq( a 'cat )        => t`

`z = '(1 2 3)neq(z z)             => nilneq('(1 2 3) z)      => t`

### The nequal Function

`nequal` checks if two arguments are not logically equivalent and returns `t` if they are not.

`x = "cow"nequal( x "cow" )    => nilnequal( x "dog" )    => t`

`z = '(1 2 3)nequal(z z)          => nilnequal('(1 2 3) z)   => nil`

### The member and memq Functions

These functions test for list membership.`member` tests using `equal` while `memq` uses `eq` and is therefore faster. These functions return a non-`nil`value if the first argument matches a member of the list passed in as the second argument.

```
x = 'c memq( x '(a b c d))                                  => (c d)memq( x '(a b d))                                          => nil
```

```
x = "c" member( x '("a" "b" "c" "d"))          => ("c" "d")memq('c '(a b c d c d))                        => (c d c d)memq( concat( x ) '(a b c d ))       => (c d)
```

### The tailp Function

`tailp` returns the first argument if a list cell `eq` to the first argument is found by `cdr`'ing down the second argument zero or more times, `nil` otherwise. Because `eq` is being used for comparison, the first argument must actually point to a tail list in the second argument for this predicate to return a non-`nil` value.

```
y = '(b c)z = cons( 'a y )            => (a b c)tailp( y z )                      => (b c)tailp( '(b c) z )    => nil
```

`nil` was returned because '`(b c)` is not eq the `cdr( z )`.

### Type Predicates

Many predicate functions are available for testing the data type of a data object. The suffix`p` on the name of a function usually indicates that it is a predicate function. Type predicates appear in the table below.

**Note:** `g` (general) can be any data type.

**Type Predicates**

| **Function** | **Value Returned**
| `arrayp(g)` | `t` if g is an array, `nil` otherwise
| `bcdp(g)` | `t` if g is a binary function, `nil` otherwise
| `dtpr(g)` | `t` if g is a non-empty list, `nil` otherwise (note that dtpr (`nil`) returns `nil`)
| `fixp(g)` | `t` if g is a fixnum, `nil` otherwise
| `floatp(g)` | `t` if g is a flonum, `nil` otherwise
| `listp(g)` | `t` if g is a list, `nil` otherwise (note that listp(`nil`) returns `t`)
| `null(g)` | `t` if g is `nil`, `nil` otherwise
| `numberp(g)` | `t` if g is a number (that is, fixnum or flonum), `nil` otherwise
| `otherp(g)` | `t` if g is a foreign data pointer, `nil` otherwise
| `portp(g)` | `t` if g is an I/O port, `nil` otherwise
| `stringp(g)` | `t` if g is a string, `nil` otherwise
| `symbolp(g)` | `t` if g is a symbol, `nil` otherwise
| `symstrp(g)` | `t` if g is either a symbol or a string, `nil` otherwise
| `type(g)` | a symbol whose name describes the type of g
| `typep(g)` | same as type(g)
For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
