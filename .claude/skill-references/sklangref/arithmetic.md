### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

6
=

Arithmetic Functions
====================

### abs

`abs( n_number ) => n_result`

#### Description

Returns the absolute value of a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `n_result` | Absolute value of`n_number`.
#### Example

`abs( -209.625)=> 209.625`

`abs( -23)=> 23`

#### Reference

[min](#1039807 "Arithmetic Functions")

### add1

`add1( n_number ) => n_result`

#### Description

Adds one to a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer to increase by one.
#### Value Returned

|  |
| --- | ---
| `n_result` | `n_number` plus one.
#### Example

`add1( 59 )=> 60`

#### Reference

[sub1](#1040803 "Arithmetic Functions")

### atof

`atof( t_string ) => f_result | nil`

#### Description

Converts a string into a floating-point number. Returns`nil` if the given string does not denote a number.

The`atof` function calls the C library function `strtod` to convert a string into a floating-point number. It returns `nil` if `t_string` does not represent a number.

#### Arguments

|  |
| --- | ---
| `t_string` | A string.
#### Value Returned

|  |
| --- | ---
| `f_result` | The floating-point value represented by`t_string`.
|  |
| --- | ---
| `nil` | If`t_string` does not denote a floating-point number.
#### Example

```
atof("123")              => 123.0atof("abc")              => nilatof("123.456")          => 123.456atof("123abc")           => 123.0
```

#### Reference

`atoi`

### atoi

`atoi( t_string ) => x_result | nil`

#### Description

Converts a string into an integer. Returns`nil` if the given string does not denote an integer.

The`atoi` function calls the C library function `strtol` to convert a string into an integer. It returns `nil` if `t_string` does not represent an integer.

#### Arguments

|  |
| --- | ---
| `t_string` | A string.
#### Value Returned

|  |
| --- | ---
| `x_result` | The integer value represented by`t_string`.
|  |
| --- | ---
| `nil` | If`t_string` does not denote an integer.
#### Example

```
atoi("123")      => 123atoi("abc")      => nilatoi("123.456")  => 123atoi("123abc")   => 123
```

#### Reference

[atof](#1038767 "Arithmetic Functions")

### ceiling

`ceiling( n_number ) => x_integer`

#### Description

Returns the smallest integer not smaller than the given argument.

#### Arguments

|  |
| --- | ---
| `n_number` | Any number.
#### Value Returned

|  |
| --- | ---
| `x_integer` | Smallest integer not smaller than`n_number`.
#### Example

`(ceiling -4.3)  => -4(ceiling 3.5)   => 4`

#### Reference

[floor](#1039438 "Arithmetic Functions"), [round](#1040534 "Arithmetic Functions"), [truncate](#1040899 "Arithmetic Functions")

### defMathConstants

`defMathConstants( s_id ) => s_id`

#### Description

Associates a set of predefined math constants as properties of the given symbol.

#### Arguments

|  |
| --- | ---
| `s_id` | Must be a symbol. The properties to be associated with thesymbol are listed as name/value pairs. The names are explained in the following table.
|  |
| --- | ---
| **Name** | **Meaning**
| E | The base of natural logarithms. (*e*)
| LOG2E | The base-2 logarithm of*e*
| LOG10E | The base-10 logarithm of*e*
| LN2 | The natural logarithm of 2.
| LN10 | The natural logarithm of 10.
| PI | The ratio of the circumference of a circle to itsdiameter. ( π )
| PI\_OVER\_2 | π/2
| PI\_OVER\_4 | π/4
| ONE\_OVER\_PI | 1/π
| TWO\_OVER\_PI | 2/π
| TWO\_OVER\_SQRTPI |
| SQRT\_TWO | (The positive square root of 2.)
| SQRT\_POINT\_FIVE | (The positive square root of 1/2.)
| INT\_MAX | The maximum value of a SKILL integer.
| INT\_MIN | The minimum value of a SKILL integer.  **Note:** The minimum value of a SKILL integer is -2147483648. The minimum literal value which may appear in a program is -2147483647.
| DBL\_MAX | The maximum value of a SKILL double.
| DBL\_MIN | The minimum value of a SKILL double.
| SHRT\_MAX | The maximum value of a SKILL "short" integer.
| SHRT\_MIN | The minimum value of a SKILL "short" integer.
#### Value Returned

|  |
| --- | ---
| `s_id` | Returns the symbol ID.
#### Example

`` defMathConstants(`m) => m ``

```
m.?? => ( SQRT_POINT_FIVE 0.7071068 SQRT_TWO 1.414214 TWO_OVER_SQRTPI 1.128379 TWO_OVER_PI 0.6366198 ONE_OVER_PI 0.3183099 PI_OVER_4 0.7853982 PI_OVER_2 1.570796 PI 3.141593 LN10 2.302585 LN2 0.6931472 LOG10E 0.4342945 LOG2E 1.442695 E 2.718282 DBL_MIN 2.225074e-308 DBL_MAX 1.797693e+308 INT_MIN -2147483648 INT_MAX 2147483647 SHRT_MIN -32768 SHRT_MAX 32767)
```

`m.SQRT_POINT_FIVE => 0.7071068`

`m.INT_MIN => -2147483648`

`m.PI => 3.141593`

`printf("%0.17f\n" m.PI) => 3.14159265358979312`

#### Reference

`printf, getqq, plist, setplist`

### difference

`difference( n_op1 n_op2 [ n_op3 ... ] ) => n_result`

#### Description

Returns the result of subtracting one or more operands from the first operand. Prefix form ofthe `-` arithmetic operator.

#### Arguments

|  |
| --- | ---
| `n_op1` | Number from which the others are to be subtracted.
|  |
| --- | ---
| `n_op2` | Number to subtract.
|  |
| --- | ---
| `n_op3` | Optional additional numbers to subtract.
#### Value Returned

|  |
| --- | ---
| `n_result` | Result of the operation.
#### Example

```
difference(5 4 3 2 1) => -5difference(-12 13)    => -25difference(12.2 -13)  => 25.2
```

#### Reference

[xdifference](#1040947 "Arithmetic Functions")

### evenp

`evenp( g_general ) => t | nil`

#### Description

Checks if a number is an even integer.

#### Arguments

|  |
| --- | ---
| `g_general` | Number to check.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_general` is an even integer.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`evenp( 59 )=> nil`

`evenp( 60 )=> t`

`evenp( 2.0 )=> nil             ; Number is even, but not an integer.`

#### Reference

[minusp](#1039868 "Arithmetic Functions"), [oddp](#1040079 "Arithmetic Functions"), [onep](#1040119 "Arithmetic Functions"), [plusp](#1040213 "Arithmetic Functions"), [zerop](#1041072 "Arithmetic Functions")

### exp

`exp( n_number ) => f_result`

#### Description

Raises`e` to a given power.

#### Arguments

|  |
| --- | ---
| `n_number` | Power to raise`e` to.
#### Value Returned

|  |
| --- | ---
| `f_result` | Value of`e` raised to the `n_numberth` power.
#### Example

`exp( 1 )  => 2.718282exp( 3.0) => 20.08554`

#### Reference

[asin](trigono.html#1037652 "Trigonometric Functions"), [atan](trigono.html#1037693 "Trigonometric Functions"), [cos](trigono.html#1037791 "Trigonometric Functions"), [log](#1039664 "Arithmetic Functions"), [sin](trigono.html#1037827 "Trigonometric Functions")

### expt

`expt( n_base n_power ) => n_result`

#### Description

Returns the result of raising a base number to a power. Prefix form of the`**` exponentiation operator.

#### Arguments

|  |
| --- | ---
| `n_base` | Number to be raised to a power.
|  |
| --- | ---
| `n_power` | Power to which the number is raised.
#### Value Returned

|  |
| --- | ---
| `n_result` | Result of the operation.
#### Example

expt(2 3)   => 8
expt(-2 3)  => -8
expt(3.3 2) => 10.89

### fix

`fix( n_arg ) => x_result`

#### Description

Returns the largest integer not larger than the given argument.

This function is equivalent to`floor`. See also ["Type Conversion Functions (fix and float)"](../sklanguser/chap5.html#fixTip) in the *Cadence SKILL Language User Guide*.

#### Arguments

|  |
| --- | ---
| `n_arg` | Any number.
#### Value Returned

|  |
| --- | ---
| `x_result` | The largest integer not greater than`n_arg`. If an integer is given as an argument, it returns the argument.
#### Example

```
fix(1.9)      => 1fix(-5.6)     => -6fix(100)      => 100fix(4.1 * 100)      => 409
```

#### Reference

`ceiling, fixp, floor, round`

### fixp

`fixp( g_value ) => t | nil`

#### Description

Checks if an object is an integer, that is, a fixed number.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function. This function is equivalent to `integerp`.

#### Arguments

|  |
| --- | ---
| `g_value` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is an integer, a data type whose internal name is `fixnum`.
|  |
| --- | ---
| `nil` | If`g_value` is not an integer.
#### Example

`fixp(3)     => tfixp(3.0)   => nil`

#### Reference

`fix, float, floatp, integerp`

### fix2

`fix2( n_value ) => x_result / nil`

#### Description

This function is a version of the`fix` function that works for rounding issue in floating-point calculations. The function returns the largest integer not larger than the given argument.

For more information, see "[Comparing Floating-Point Numbers](../sklanguser/chap5.html#comparefloatnum)" in the "Arithmetic and Logical Expressions" chapter of the *SKILL Language User Guide*.

#### Arguments

|  |
| --- | ---
| `n_value` | Any number.
#### Value Returned

|  |
| --- | ---
| `x_result` | Returns the largest integer not larger than the given argument.
|  |
| --- | ---
| `nil` | If`n_value` is not an integer.
#### Example

`fix2(4.1 * 100)`

`=> 410`

#### Reference

`fix, float, floatp, integerp`

### float

`float( n_arg ) => f_result`

#### Description

Converts a number into its equivalent floating-point number.

#### Arguments

|  |
| --- | ---
| `n_arg` | Integer to be converted to floating-point. If you give a floating-point number as an argument, it returns the argument unchanged.
#### Value Returned

|  |
| --- | ---
| `f_result` | A floating-point number.
#### Example

`float(3)    => 3.0float(1.2)  => 1.2`

#### Reference

`fix, fixp, floatp`

### floatp

`floatp( g_value ) => t | nil`

#### Description

Checks if an object is a floating-point number. Same as`realp`.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is a floating-point number, a data type whose internal name is `flonum`.
|  |
| --- | ---
| `nil` | If`g_value` is not a floating-point number.
#### Example

`floatp(3)    => nilfloatp(3.0)  => t`

#### Reference

[fix](#1039274 "Arithmetic Functions"), [fixp](#1039304 "Arithmetic Functions"), [float](#1039334 "Arithmetic Functions"), [realp](#1040382 "Arithmetic Functions")

### floor

`floor( n_number ) => x_integer`

#### Description

Returns the largest integer not larger than the given argument.

#### Arguments

|  |
| --- | ---
| `n_number` | Any number.
#### Value Returned

|  |
| --- | ---
| `x_integer` | Largest integer not larger than`n_number`.
#### Example

`(floor -4.3) => -5(floor 3.5)  => 3`

#### Reference

[ceiling](#1038844 "Arithmetic Functions"), [fix](#1039274 "Arithmetic Functions"), [round](#1040534 "Arithmetic Functions"), [truncate](#1040899 "Arithmetic Functions")

### int

`int( g_value) => x_result`

#### Description

Rounds off the number value to the nearest integer. The`int` function works as an overloadable arithmetic operator adopted from DFII to the SKILL Core language. The argument (`g_value`) is specified on the number class (numberp arguments).

#### Arguments

|  |
| --- | ---
| `g_value` | Specifies the number value you want to round off
#### Value Returned

|  |
| --- | ---
| `x_result` | Returns the nearest integer
#### Example

`int(2.7)`

`=>2`

`int(.7)`

=>0

### isInfinity

`isInfinity( f_flownum ) => t | nil`

#### Description

Checks if the given flownum argument represents infinity (positive or negative).

#### Arguments

|  |
| --- | ---
| `f_flownum` | A floating-point number.
#### Value Returned

|  |
| --- | ---
| `t` | If`f_flownum` is infinity (positive or negative).
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

plus\_inf = 2.0 \* 1e999
isInfinity (plus\_inf) => t
isInfinity (987.65) => nil

### isNaN

`isNaN( f_flownum ) => t | nil`

#### Description

Checks if the given flownum argument represents NaN (not-a-number),`nil` otherwise.

#### Arguments

|  |
| --- | ---
| `f_flownum` | A floating-point number.
#### Value Returned

|  |
| --- | ---
| `t` | If`f_flownum` is NaN.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

nan = 0.0 \* 2.0 \* 1e999
isNan (nan) => t
isNan (123.456) => nil

### leftshift

`leftshift( x_val x_num ) => x_result`

#### Description

Returns the integer result of shifting a value a specified number of bits to the left. Prefix formof the `<<` arithmetic operator. Note that `leftshift` is logical (that is, vacated bits are 0-filled).

#### Arguments

|  |
| --- | ---
| `x_val` | Value to be shifted.
|  |
| --- | ---
| `x_num` | Number of bits`x_val` is shifted.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the operation.
#### Example

`leftshift(7 2)  => 28leftshift(10 1) => 20`

#### Reference

[rightshift](#1040492 "Arithmetic Functions")

### log

`log( n_number ) => f_result`

#### Description

Returns the natural logarithm of a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `f_result` | Natural logarithm of the value passed in.
|  |
| --- | ---
|  | If the value of`n_number` is not a positive number, an error is signaled.
#### Example

`log( 3.0 ) => 1.098612`

#### Reference

`exp, sqrt`

### log10

`log10( n_number ) => f_result`

#### Description

Returns the base 10 logarithm of a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `f_result` | Base 10 logarithm of the value passed in.
|  |
| --- | ---
|  | If the value of`n_number` is not a positive number, an error is signaled.
#### Example

`log10( 10.0 ) => 1.0`

`log10(-20.0)`

`*Error* log10: argument must be positive - -20`

#### Reference

[log](#1039664 "Arithmetic Functions"), [sqrt](#1040712 "Arithmetic Functions")

### max

`max( n_num1 [ n_num2 ... ]) => n_result`

#### Description

Returns the maximum of the values passed in. Requires a minimum of one argument.

#### Arguments

|  |
| --- | ---
| `n_num1` | First value to check.
|  |
| --- | ---
| `n_num2` | Additional values to check.
#### Value Returned

|  |
| --- | ---
| `n_result` | Maximum of the values passed in.
#### Example

`max(6)       => 6max(3 2 1)       => 3max(-3 -2 -1)    => -1`

#### Reference

[abs](#1038670 "Arithmetic Functions"), [min](#1039807 "Arithmetic Functions"), [numberp](logicalrel.html#1039447 "Logical and Relational Functions")

### min

`min( n_num1 [ n_num2 ... ] )=> n_result`

#### Description

Returns the minimum of the values passed in. Requires a minimum of one argument.

#### Arguments

|  |
| --- | ---
| `n_num1` | First value to check.
|  |
| --- | ---
| `n_num2` | Additional values to check.
#### Value Returned

|  |
| --- | ---
| `n_result` | Minimum of the values passed in.
#### Example

`min(3)        => 3min(1 2 3)        => 1min(-1 -2.0 -3)   => -3.0`

#### Reference

[abs](#1038670 "Arithmetic Functions"), [max](#1039746 "Arithmetic Functions"), [numberp](logicalrel.html#1039447 "Logical and Relational Functions")

### minus

`minus( n_op ) => n_result`

#### Description

Returns the negative of a number. Prefix form of the`-` unary operator.

#### Arguments

|  |
| --- | ---
| `n_op` | A number.
#### Value Returned

|  |
| --- | ---
| `n_result` | Negative of the number.
#### Example

`minus( 10 )   => -10minus( -1.0 ) => 1.0minus( -0 )   => 0`

### minusp

`minusp( g_general ) => t | nil`

#### Description

Checks if a value is a negative number. Same as`negativep`.

#### Arguments

|  |
| --- | ---
| `g_general` | Number to check.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_general` is a negative number.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`minusp( 3 )    => nilminusp( -3 )   => t`

#### Reference

[evenp](#1039099 "Arithmetic Functions"), [negativep](#1040006 "Arithmetic Functions"), [numberp](logicalrel.html#1039447 "Logical and Relational Functions"), [oddp](#1040079 "Arithmetic Functions"), [onep](#1040119 "Arithmetic Functions"), [plusp](#1040213 "Arithmetic Functions"), [zerop](#1041072 "Arithmetic Functions")

### modulo

`modulo( x_integer1 x_integer2 )=> x_integer`

#### Description

Returns the remainder of dividing two integers. The remainder always has the sign of thedivisor.

The`remainder (mod)` and `modulo` functions differ on negative arguments. The remainder is either zero or has the sign of the dividend if you use the `remainder` function. With `modulo` the return value always has the sign of the divisor.

#### Arguments

|  |
| --- | ---
| `x_integer1` | Dividend.
|  |
| --- | ---
| `x_integer2` | Divisor.
#### Value Returned

|  |
| --- | ---
| `x_integer` | The remainder of the division. The sign is determined by thedivisor.
#### Example

`modulo( 13 4)         => 1remainder( 13 4)      => 1`

`modulo( -13 4)        => 3remainder( -13 4)     => -1`

`modulo( 13 -4)        => -3remainder( 13 -4)     => 1`

`modulo( -13 -4)       => -1remainder( -13 -4)    => -1`

#### Reference

[remainder](#1040429 "Arithmetic Functions")

### negativep

`negativep( n_num ) => t | nil`

#### Description

Checks if a value is a negative number. Same as`minusp`.

#### Arguments

|  |
| --- | ---
| `n_num` | Number to check.
#### Value Returned

|  |
| --- | ---
| `t` | `n_num` is a negative number.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`negativep( 3 )    => nilnegativep( -3 )   => t`

#### Reference

[evenp](#1039099 "Arithmetic Functions"), [minusp](#1039868 "Arithmetic Functions"), [numberp](logicalrel.html#1039447 "Logical and Relational Functions"), [oddp](#1040079 "Arithmetic Functions"), [onep](#1040119 "Arithmetic Functions"), [plusp](#1040213 "Arithmetic Functions"), [zerop](#1041072 "Arithmetic Functions")

### oddp

`oddp( g_value ) => t | nil`

#### Description

Checks if an object is an odd integer.

`oddp` is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A SKILL object that is an integer.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is an odd integer.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`oddp( 7 )=> t`

`oddp( 8 ) => nil`

#### Reference

`evenp, fixp, integerp, minusp, onep, plusp, zerop`

### onep

`onep( g_value ) => t | nil`

#### Description

Checks if the given object is equal to one.

`onep` is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A SKILL object that is either a floating-point number or aninteger.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is equal to one.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`onep( 1 ) => t`

`onep( 7 ) => nil`

`onep( 1.0 ) => t`

#### Reference

[evenp](#1039099 "Arithmetic Functions"), [minusp](#1039868 "Arithmetic Functions"), [numberp](logicalrel.html#1039447 "Logical and Relational Functions"), [plusp](#1040213 "Arithmetic Functions"), [zerop](#1041072 "Arithmetic Functions")

### plus

`plus( n_op1 n_op2 [ n_op3 ... ] ) => n_result`

#### Description

Returns the result of adding one or more operands to the first operand. Prefix form of the`+` arithmetic operator.

#### Arguments

|  |
| --- | ---
| `n_op1` | First number to be added.
|  |
| --- | ---
| `n_op2` | Second number to be added.
|  |
| --- | ---
| `n_op3` | Optional additional numbers to be added.
#### Value Returned

|  |
| --- | ---
| `n_result` | Sum of the numbers.
#### Example

`plus(5 4 3 2 1) => 15plus(-12 -13)   => -25plus(12.2 13.3) => 25.5`

#### Reference

`xplus`

### plusp

`plusp( g_value ) => t | nil`

#### Description

Checks if the given object is a positive number.

`plusp` is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A SKILL object that is either a floating-point number or aninteger.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is a positive number.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`plusp( -209.623472)=> nil`

`plusp( 209.623472)=> t`

#### Reference

[evenp](#1039099 "Arithmetic Functions"), [minusp](#1039868 "Arithmetic Functions"), [oddp](#1040079 "Arithmetic Functions"), [onep](#1040119 "Arithmetic Functions"), [zerop](#1041072 "Arithmetic Functions")

### quotient

`quotient( n_op1 n_op2 [ n_op3 ... ] ) => n_result`

#### Description

Returns the result of dividing the first operand by one or more operands. Prefix form of the`/` arithmetic operator.

#### Arguments

|  |
| --- | ---
| `n_op1` | Dividend.
|  |
| --- | ---
| `n_op2` | Divisor.
|  |
| --- | ---
| `n_op3` | Optional additional divisors for multiple divisions.
#### Value Returned

|  |
| --- | ---
| `n_result` | Result of the operation.
#### Example

`quotient(5 4 3 2 1) => 0quotient(-10 -2)    => 5quotient(10.8 -2.2) => -4.909091`

#### Reference

[xquotient](#1041024 "Arithmetic Functions")

### random

`random( [ x_number ] ) => x_result`

#### Description

Returns a random integer between zero and a given number minus one.

If you call`random` with no arguments, it returns an integer that has all of its bits randomly set.

#### Arguments

|  |
| --- | ---
| `x_number` | An integer.
#### Value Returned

|  |
| --- | ---
| `x_result` | Random integer between zero and`x_number` minus one.
#### Example

`random( 93 )=> 26`

#### Reference

[srandom](#1040749 "Arithmetic Functions")

### realp

`realp( g_obj ) => t | nil`

#### Description

Checks if a value is a real number. Same as`floatp`.

#### Arguments

|  |
| --- | ---
| `g_obj` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | Argument is a real number.
|  |
| --- | ---
| `nil` | Argument is not a real number.
#### Example

`realp( 2789987)=> nilrealp( 2789.987)=> t`

#### Reference

[floatp](#1039359 "Arithmetic Functions"), [integerp](dataoperator.html#1039155 "Data Operator Functions"), [fixp](#1039304 "Arithmetic Functions")

### remainder

`remainder( x_integer1 x_integer2 ) => x_integer`

#### Description

Returns the remainder of dividing two integers. The remainder is either zero or has the signof the dividend. Same as `mod`.

The`remainder` and `modulo` functions differ on negative arguments. The remainder is either zero or has the sign of the dividend if you use the `remainder` function. With `modulo` the return value always has the sign of the divisor.

#### Arguments

|  |
| --- | ---
| `x_integer1` | Dividend.
|  |
| --- | ---
| `x_integer2` | Divisor.
#### Value Returned

|  |
| --- | ---
| `x_integer` | Remainder of dividing`x_integer1` by `x_integer2`. The sign is determined by the sign of `x_integer1`.
#### Example

`modulo( 13 4)            => 1remainder( 13 4)         => 1`

`modulo( -13 4)           => 3remainder( -13 4)        => -1`

`modulo( 13 -4)           => -3remainder( 13 -4)        => 1`

`modulo( -13 -4)          => -1remainder( -13 -4)       => -1`

#### Reference

[modulo](#1039941 "Arithmetic Functions")

### rightshift

`rightshift( x_val x_num ) => x_result`

#### Description

Returns the integer result of shifting a value a specified number of bits to the right. Prefix formof the `>>` arithmetic operator. Note that `rightshift` is logical (that is, vacated bits are 0-filled).

#### Arguments

|  |
| --- | ---
| `x_val` | Value to be shifted.
|  |
| --- | ---
| `x_num` | Number of bits`x_val` is shifted.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the operation.
#### Example

`rightshift(7 2)  => 1rightshift(10 1) => 5`

#### Reference

[leftshift](#1039623 "Arithmetic Functions")

### round

`round( n_arg ) => x_result`

#### Description

Rounds a floating-point number to its closest integer value.

#### Arguments

|  |
| --- | ---
| `n_arg` | Floating-point number.
#### Value Returned

|  |
| --- | ---
| `x_result` | Integer whose value is closest to`n_arg`.
#### Example

`round(1.5)        => 2round(-1.49)      => -1round(1.49)       => 1`

#### Reference

[fix](#1039274 "Arithmetic Functions"), [float](#1039334 "Arithmetic Functions")

### round2

`round2( n_arg ) => x_result`

#### Description

This function is a version of the`round` function that rounds the result in floating-point calculations to its closest integer value.

For more information, see "[Type Conversion Functions (fix and float)](../sklanguser/chap5.html#fixTip)" in the Arithmetic and Logical Expressions chapter of the *SKILL Language User Guide*.

#### Arguments

|  |
| --- | ---
| `n_arg` | A floating-point number.
#### Value Returned

|  |
| --- | ---
| `x_result` | Integer whose value is closest to`n_arg`.
#### Example

`val=-0.2865`

`round(val/0.001)*0.001`

`=> -0.286`

`round2(val/0.001)*0.001`

`=> -0.287`

### sort

`sort( l_data u_comparefn ) => l_result`

#### Description

Sorts a list according to a comparison function; defaults to an alphabetical sort when`u_comparefn` is `nil`. This function does not create a new list. It returns the altered input list. This is a destructive operation. The`l_data` list is modified in place and no new storage is allocated. Pointers previously pointing to `l_data` may not be pointing at the head of the sorted list.

Sorts the list`l_data` according to the `sort` function `u_comparefn`. `u_comparefn(``g_x``g_y``)` returns non-`nil` if `g_x` can precede `g_y` in sorted order, `nil` if `g_y` must precede `g_x`. If `u_comparefn` is `nil`, alphabetical order is used. The algorithm currently implemented in `sort` is based on recursive merge sort.

* ***The l\_data list is modified in place and no new storage is allocated.Pointers previously pointing to l\_data may not be pointing at the head of the sorted list.***

#### Arguments

|  |
| --- | ---
| `l_data` | List of objects to be sorted.
|  |
| --- | ---
| `u_comparefn` | Comparison function to determine which of any two elementsshould come first.
#### Value Returned

|  |
| --- | ---
| `l_result` | `l_data` sorted by the comparison function `u_comparefn`.
#### Example

```
y = '(c a d b)(sort y nil)        => (a b c d)y                   => (c d)  ;no longer points to head of listy = '(c a d b)y = (sort y nil)    => (a b c d)y => (a b c d)                ;reassignment points y to sorted list.
```

#### Reference

[lessp](logicalrel.html#1039206 "Logical and Relational Functions"), [sortcar](#1040654 "Arithmetic Functions")

### sortcar

`sortcar( l_data u_comparefn ) => l_result`

#### Description

Similar to`sort` except that only the `car` of each element in a list is used for comparison by the sort function. This function does not create a new list. It returns the altered input list.

This function also sorts`l_data` based on the function `u_comparefn`.

* ***The l\_data list is modified in place and no new storage is allocated.Pointers previously pointing to l\_data might not be pointing at the head of the sorted list.***

#### Arguments

|  |
| --- | ---
| `l_data` | List of objects to be sorted.
|  |
| --- | ---
| `u_comparefn` | Comparison function to determine which of any two elementsshould come first.
#### Value Returned

|  |
| --- | ---
| `l_result` | `l_data` sorted by the comparison function `u_comparefn`.
#### Example

`sortcar( '((4 four) (3 three) (2 two)) 'lessp )=> ((2 two) (3 three) (4 four)`

`sortcar( '((d 4) (b 2) (c 3) (a 1)) nil )=> ((a 1) (b 2) (c 3) (d 4))`

#### Reference

[sort](#1040591 "Arithmetic Functions")

### sqrt

`sqrt( n_number ) => f_result`

#### Description

Returns the square root of a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `f_result` | Square root of the value passed in.
|  |
| --- | ---
|  | If the value of`n_number` is not a positive number, an error is signaled.
#### Example

`sqrt( 49 )=> 7.0`

sqrt( 43942 )
=> 209.6235

### srandom

`srandom( x_number ) => t`

#### Description

Sets the seed of the random number generator to a given number.

#### Arguments

|  |
| --- | ---
| `x_number` | An integer.
#### Value Returned

|  |
| --- | ---
| `t` | Always.
#### Example

`srandom( 89 )=> t`

#### Reference

[random](#1040327 "Arithmetic Functions")

### sub1

`sub1( n_number ) => n_result`

#### Description

Subtracts one from a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `n_result` | `n_number` minus one.
#### Example

`sub1( 59 )=> 58`

#### Reference

[add1](#1038712 "Arithmetic Functions")

### times

`times( n_op1 n_op2 [ n_op3 ... ] ) => n_result`

#### Description

Returns the result of multiplying the first operand by one or more operands. Prefix form of the`*` arithmetic operator.

#### Arguments

|  |
| --- | ---
| `n_op1` | First operand to be multiplied.
|  |
| --- | ---
| `n_op2` | Second operand to be multiplied.
|  |
| --- | ---
| `n_op3` | Optional additional operands to be multiplied.
#### Value Returned

|  |
| --- | ---
| `n_result` | Result of the multiplication.
#### Example

`times(5 4 3 2 1)  => 120times(-12 -13)    => 156times(12.2 -13.3) => -162.26`

#### Reference

[xtimes](#1041045 "Arithmetic Functions")

### truncate

`truncate( n_number ) => x_integer`

#### Description

Truncates a given number to an integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Any SKILL number.
#### Value Returned

|  |
| --- | ---
| `x_integer` | `n_number` truncated to an integer.
#### Example

`truncate( 1234.567)=> 1234`

`round( 1234.567)=> 1235`

`truncate( -1.7)=> -1`

#### Reference

[ceiling](#1038844 "Arithmetic Functions"), [floor](#1039438 "Arithmetic Functions"), [round](#1040534 "Arithmetic Functions")

### xdifference

`xdifference( x_op1 x_op2 [ x_opt3 ] ) => x_result`

#### Description

Returns the integer result of subtracting one or more operands from the first operand.`xdifference` is an integer-only arithmetic function while `difference` can handle integers and floating-point numbers. `xdifference` runs slightly faster than `difference` in integer arithmetic calculation.

#### Arguments

|  |
| --- | ---
| `x_op1` | Operand from which one or more operands are subtracted.
|  |
| --- | ---
| `x_op2` | Operand to be subtracted.
|  |
| --- | ---
| `x_opt3` | Optional additional operands to be subtracted.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the subtraction.
#### Example

`xdifference(12 13)  => -1xdifference(-12 13) => -25`

#### Reference

[difference](#1042101 "Arithmetic Functions")

### xplus

`xplus( x_op1 x_op2 [ x_opt3 ] ) => x_result`

#### Description

Returns the integer result of adding one or more operands to the first operand.`xplus` is an integer-only arithmetic function while `plus` can handle integers and floating-point numbers. `xplus` runs slightly faster than `plus` in integer arithmetic calculation.

#### Arguments

|  |
| --- | ---
| `x_op1` | First operand to be added.
|  |
| --- | ---
| `x_op2` | Second operand to be added.
|  |
| --- | ---
| `x_opt3` | Optional additional operands to be added.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the addition.
#### Example

`xplus(12 13)   => 25xplus(-12 -13) => -25`

#### Reference

`plus`

### xquotient

`xquotient( x_op1 x_op2 [ x_opt3 ] ) => x_result`

#### Description

Returns the integer result of dividing the first operand by one or more operands.`xquotient` is an integer-only arithmetic function while `quotient` can handle integers and floating-point numbers. `xquotient` runs slightly faster than `quotient` in integer arithmetic calculation.

#### Arguments

|  |
| --- | ---
| `x_op1` | Dividend.
|  |
| --- | ---
| `x_op2` | Divisor.
|  |
| --- | ---
| `x_opt3` | Optional additional divisors.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the division.
#### Example

`xquotient(10 2)   => 5xquotient(-10 -2) => 5`

#### Reference

`quotient`

### xtimes

`xtimes( x_op1 x_op2 [ x_opt3 ] ) => x_result`

#### Description

Returns the integer result of multiplying the first operand by one or more operands.`xtimes` is an integer-only arithmetic function while `times` can handle integers and floating-point numbers. `xtimes` runs slightly faster than `times` in integer arithmetic calculation.

#### Arguments

|  |
| --- | ---
| `x_op1` | First operand to be multiplied.
|  |
| --- | ---
| `x_op2` | Second operand to be multiplied.
|  |
| --- | ---
| `x_opt3` | Optional additional operands to be multiplied.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the multiplication.
#### Example

`xtimes(12 13)   => 156xtimes(-12 -13) => 156`

### zerop

`zerop( g_value ) => t | nil`

#### Description

Checks if an object is equal to zero.

`zerop` is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A SKILL object that is either a floating-point number or aninteger.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is equal to zero.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`zerop( 0 )=> t`

`zerop( 7 )=> nil`

#### Reference

`evenp, minusp, oddp, onep, plusp`

### zxtd

`zxtd( x_number x_bits ) => x_result`

#### Description

Zero-extends the number represented by the rightmost specified number of bits in the giveninteger.

Zero-extends the rightmost`x_bits` bits of `x_number`. Executes faster than doing `x_number<x_bits - 1:0>`.

#### Arguments

|  |
| --- | ---
| `x_number` | An integer.
|  |
| --- | ---
| `x_bits` | Number of bits.
#### Value Returned

|  |
| --- | ---
| `x_result` | `x_number` with the rightmost `x_bits` zero-extended.
#### Example

zxtd( 8 3 )  => 0
zxtd( 10 2 ) => 2




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
