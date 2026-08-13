### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

9
=

Logical and Relational Functions
================================

### alphalessp

`alphalessp( S_arg1 S_arg2 ) => t | nil`

#### Description

Compares two string or symbol names alphabetically.

This function returns`t` if the first argument is alphabetically less than the second argument. If `S_arg` is a symbol, then its name is its print name. If `S_arg` is a string, then its name is the string itself.

#### Arguments

|  |
| --- | ---
| `S_arg1` | First name you want to compare.
|  |
| --- | ---
| `S_arg2` | Name to compare against.
#### Value Returned

|  |
| --- | ---
| `t` | If`S_arg1` is alphabetically less than the name of `S_arg2`.
|  |
| --- | ---
| `nil` | In all other cases.
#### Example

```
alphalessp( "name" "name1" )   => talphalessp( "third" "fourth" ) => nilalphalessp('a 'ab)             => t
```

#### Reference

[strcmp](stringfunc.html#1040645 "String Functions"), [strncmp](stringfunc.html#1040843 "String Functions")

### and

`and( g_arg1 g_arg2 [ g_arg3... ] ) => nil | g_val`

#### Description

Evaluates from left to right its arguments to see if the result is`nil`. As soon as an argument evaluates to `nil`, `and` returns `nil` without evaluating the rest of the arguments. Otherwise, `and` evaluates the next argument. If all arguments except for the last evaluate to non-`nil`, `and` returns the value of the last argument as the result of the function call. Prefix form of the `&&` binary operator.

#### Arguments

|  |
| --- | ---
| `g_arg1` | Any SKILL object.
|  |
| --- | ---
| `g_arg2` | Any SKILL object.
|  |
| --- | ---
| `g_arg3` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `nil` | If an argument evaluates to`nil`.
|  |
| --- | ---
| `g_val` | Value of the last argument if all the preceding argumentsevaluate to non-`nil`.
#### Example

`and(nil t)  => nil and(t nil)  => nil and(18 12)  => 12`

#### Reference

[band](bitwise.html#1038671 "Bitwise Operator Functions"), [bnand](bitwise.html#1038836 "Bitwise Operator Functions"), [bnor](bitwise.html#1038878 "Bitwise Operator Functions"), [bnot](bitwise.html#1038920 "Bitwise Operator Functions"), [bor](bitwise.html#1039005 "Bitwise Operator Functions"), [bxnor](bitwise.html#1039068 "Bitwise Operator Functions"), [bxor](bitwise.html#1039138 "Bitwise Operator Functions")

### compareTime

`compareTime( t_time1 t_time2 ) => x_difference`

#### Description

Compares two string arguments, representing a clock-calendar time.

#### Arguments

|  |
| --- | ---
| `t_time1` | First string in the`month day hour:minute:second``year` format.
|  |
| --- | ---
| `t_time2` | Second string in the`month day hour:minute:second``year` format.
#### Value Returned

|  |
| --- | ---
| `x_difference` | An integer representing a time that is later than (positive), equalto (zero), or earlier than (negative) the second argument. The units are seconds.
#### Example

`compareTime( "Apr 8 4:21:39 1991" "Apr 16 3:24:36 1991")=> -687777.`

687,777 seconds have occurred between the two dates given. For a positive number ofseconds, the most recent date needs to be given as the first argument.

`compareTime("Apr 16 3:24:36 1991" "Apr 16 3:14:36 1991")=> 600`

600 seconds (10 minutes) have occurred between the two dates.

#### Reference

[getCurrentTime](environment.html#1039237 "Environment Functions")

### eq

`eq( g_arg1 g_arg2 ) => t | nil`

#### Description

Checks addresses when testing for equality.

Returns`t` if `g_arg1` and `g_arg2` are exactly the same (that is, are at the same address in memory). The `eq` function runs considerably faster than `equal` but should only be used for testing equality of symbols or shared lists. Using `eq` on types other than symbols and lists will give unpredictable results and should be avoided.
For testing equality of numbers, strings, and lists in general, the `equal` function and not the `eq` function should be used. You can test for equality between symbols using `eq` more efficiently than using the `==` operator, which is the same as the `equal` function.

#### Arguments

|  |
| --- | ---
| `g_arg1` | Any SKILL object.`g_arg1` is compared with `g_arg2` to see if they point to the same object.
|  |
| --- | ---
| `g_arg2` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | Both arguments are the same object.
|  |
| --- | ---
| `nil` | The two objects are not identical.
#### Example

`x = 'dog eq( x 'dog )        => teq( x 'cat )        => nil`

`y = 'dog eq( x y )           => t`

#### Reference

[equal](#1038894 "Logical and Relational Functions")

### equal

`equal( g_arg1 g_arg2 ) => t | nil`

#### Description

Checks contents of strings and lists when testing for equality.

Checks if two arguments are equal or if they are logically equivalent, for example,`g_arg1` and `g_arg2` are equal if they are both lists/strings and their contents are the same. Note that this test is slower than using `eq` but works for comparing objects other than symbols.

* If the arguments are the same object in virtual memory (that is, they are`eq`*),* `equal` returns `t`.

* If the arguments are the same type and their contents are equal (for example, strings withidentical character sequence), `equal` returns `t`.

* If the arguments are a mixture of fixnums and flonums,`equal` returns `t` if the numbers are identical (for example, 1.0and 1).

#### Arguments

|  |
| --- | ---
| `g_arg1` | Any SKILL object.`g_arg1` and `g_arg2` are tested to see if they are logically equivalent.
|  |
| --- | ---
| `g_arg2` | Any SKILLobject.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_arg1` and `g_arg2` are equal.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`x = 'cat equal( x 'cat )    => t`

`x == 'dog          => nil     ; == is the same as equal.`

`x = "world" equal( x "world" ) => t`

`x = '(a b c) equal( x '(a b c)) => tequal(2 2.0)       => t`

#### Reference

`eq`

### eqv

`eqv( g_general1 g_general2 ) => t | nil`

#### Description

Tests for the equality between two strings or two numbers of the same type (for example, bothnumbers are integers). Except for numbers, `eqv` is like `eq`.

#### Arguments

|  |
| --- | ---
| `g_general1` | The first SKILL object.
|  |
| --- | ---
| `g_general2` | The second SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | `g_general1` and `g_general2` represent the same string or the same number.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

```
(eqv 1.5 1.5)                => t(equal 1.5 1.5)              => t(eq 1.5 1.5)                 => nil(eqv (list 1 2) (list 1 2))  => nil
```

`s1="world"`

`s2="world"`

`eqv(s1 s2)                   => t`

#### Reference

[eq](#1038850 "Logical and Relational Functions"), [equal](#1038894 "Logical and Relational Functions")

### geqp

`geqp( n_num1 n_num2 ) => t | nil`

#### Description

This predicate function checks if the first argument is greater than or equal to the secondargument. Prefix form of the `>=` operator.

#### Arguments

|  |
| --- | ---
| `n_num1` | Number to be checked.
|  |
| --- | ---
| `n_num2` | Number against which`n_num1` is checked.
#### Value Returned

|  |
| --- | ---
| `t` | `n_num1` is greater than or equal to `n_num2`.
|  |
| --- | ---
| `nil` | `n_num1` is less than `n_num2`.
#### Example

`geqp(2 2)   => tgeqp(-2 2)  => nilgeqp(3 2.2) => t`

#### Reference

[greaterp](#1039043 "Logical and Relational Functions"), [leqp](#1039179 "Logical and Relational Functions"), [lessp](#1039206 "Logical and Relational Functions")

### greaterp

`greaterp( n_num1 n_num2 ) => t | nil`

#### Description

This predicate function checks if the first argument is greater than the second argument.Prefix form of the `>` operator.

#### Arguments

|  |
| --- | ---
| `n_num1` | Number to be checked.
|  |
| --- | ---
| `n_num2` | Number against which`n_num1` is checked.
#### Value Returned

|  |
| --- | ---
| `t` | `n_num1` is greater than `n_num2`.
|  |
| --- | ---
| `nil` | `n_num1` is less than or equal to `n_num2`.
#### Example

`greaterp(2 2)   => nilgreaterp(-2 2)  => nilgreaterp(3 2.2) => t`

#### Reference

[geqp](#1038995 "Logical and Relational Functions"), [leqp](#1039179 "Logical and Relational Functions"), [lessp](#1039206 "Logical and Relational Functions")

### leqp

`leqp( n_num1 n_num2 ) => t | nil`

#### Description

This predicate function checks if the first argument is less than or equal to the secondargument. Prefix form of the `<=` operator.

#### Arguments

|  |
| --- | ---
| `n_num1` | Number to be checked.
|  |
| --- | ---
| `n_num2` | Number against which`n_num1` is checked.
#### Value Returned

|  |
| --- | ---
| `t` | `n_num1` is less than or equal to `n_num2`.
|  |
| --- | ---
| `nil` | `n_num1` is greater than `n_num2`.
#### Example

`leqp(2 2)   => tleqp(-2 2)  => tleqp(3 2.2) => nil`

#### Reference

`geqp, greaterp, lessp`

### lessp

`lessp( n_num1 n_num2 ) => t | nil`

#### Description

This predicate function checks if the first argument is less than the second argument. Prefixform of the `<` operator.

#### Arguments

|  |
| --- | ---
| `n_num1` | Number to be checked.
|  |
| --- | ---
| `n_num2` | Number against which`n_num1` is checked.
#### Value Returned

|  |
| --- | ---
| `t` | `n_num1` is less than `n_num2`.
|  |
| --- | ---
| `nil` | `n_num1` is greater than or equal to `n_num2`.
#### Example

`lessp(2 2)   => nillessp(-2 2)  => tlessp(3 2.2) => nil`

#### Reference

[geqp](#1038995 "Logical and Relational Functions"), [greaterp](#1039043 "Logical and Relational Functions"), [leqp](#1039179 "Logical and Relational Functions")

### member, memq, memv

`member( g_obj l_list ) => l_sublist | nil`

#### Description

Returns the largest sublist of`l_list` whose first element is `g_obj`. For comparison, `member` uses the `equal` function, `memq` uses the `eq` function, and `memv` uses `eqv`.

`memq` should only be used when comparing symbols and lists. See `eq` for restrictions on when `eq` based comparisons can be used.

**Note:** It is faster to convert a string to a symbol using`concat` in conjunction with `memq` than to simply use `member`, which performs a comparison using `equal` which is slower, especially for large lists. These functions return a non-`nil` value if the first argument matches a member of the list passed in as the second argument.

#### Arguments

|  |
| --- | ---
| `g_obj` | Element to be searched for in`l_list`.
|  |
| --- | ---
| `l_list` | List to search.
#### Value Returned

|  |
| --- | ---
| `l_sublist` | The part of `l_list` beginning with the first match of `g_obj`.
|  |
| --- | ---
| `nil` | If`g_obj` is not in the top level of `l_list`.
#### Example

```
x = "c"                          => "c"member( x '("a" "b" "c" "d"))    => ("c" "d")memq('c '(a b c d c d))          => (c d c d)memq( concat( x ) '(a b c d ))   => (c d)memv( 1.5 '(a 1.0 1.5 "1.5"))    => (1.5 "1.5")
```

#### Reference

[eq](#1038850 "Logical and Relational Functions"), [equal](#1038894 "Logical and Relational Functions"), [eqv](#1038922 "Logical and Relational Functions"), [concat](dataoperator.html#1038735 "Data Operator Functions")

### neq

`neq( g_arg1 g_arg2 ) => t | nil`

#### Description

Checks if two arguments arenot identical using the *eq* function and returns *t* if they are not. That is, `g_arg1` and `g_arg2` are tested to see if they are at the same address in memory.

#### Arguments

|  |
| --- | ---
| `g_arg1` | Any SKILL object.
|  |
| --- | ---
| `g_arg2` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_arg1` and `g_arg2` are not `eq`.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`a = 'dog            => dogneq( a 'dog )       => nilneq( a 'cat )       => t`

`z = '(1 2 3)        => (1 2 3)neq(z z)            => nilneq('(1 2 3) z)     => t`

#### Reference

[eq](#1038850 "Logical and Relational Functions"), [equal](#1038894 "Logical and Relational Functions"), [eqv](#1038922 "Logical and Relational Functions"), [nequal](#1039359 "Logical and Relational Functions")

### nequal

`nequal( g_arg1 g_arg2 ) => t | nil`

#### Description

Checks if two arguments are *not* logically equivalent using the `equal` function and returns `t` if they are not.

`g_arg1` and `g_arg2` are only equal if they are either `eqv` or they are both lists/strings and their contents are the same.

#### Arguments

|  |
| --- | ---
| `g_arg1` | Any SKILL object.
|  |
| --- | ---
| `g_arg2` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_arg1` and `g_arg2` are not `equal`.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

```
x = "cow"            => "cow"nequal( x "cow" )    => nilnequal( x "dog" )    => t
```

```
z = '(1 2 3)         => (1 2 3)nequal(z z)          => nilnequal('(1 2 3) z)   => nil
```

### null

`null( g_value ) => t | nil`

#### Description

Checks if an object is equal to`nil`.

`null` is a type predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A data object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is equal to `nil`.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`null( 3 )        => nilnull('())        => tnull( nil)       => t`

### numberp

`numberp( g_value ) => t | nil`

#### Description

Checks if a data object is a number, that is, either an integer or floating-point number.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A data object.
#### Value Returned

|  |
| --- | ---
| `t` | The data object is a number.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`numberp( 3 )         => tnumberp('isASymbol)  => nilnumberp( 3.5)        => t`

### or

`or( g_arg1 g_arg2 [ g_arg3... ] ) => nil | g_val`

#### Description

Evaluates from left to right its arguments to see if the result is non-`nil`. As soon as an argument evaluates to non-`nil`, `or` returns that value without evaluating the rest of the arguments. If all arguments except the last evaluate to `nil`, `or` returns the value of the last argument as the result of the function call. Prefix form of the `||` binary operator.

#### Arguments

|  |
| --- | ---
| `g_arg1` | First argument to be evaluated.
|  |
| --- | ---
| `g_arg2` | Second argument to be evaluated.
|  |
| --- | ---
| `g_arg3` | Optional additional arguments to be evaluated.
#### Value Returned

|  |
| --- | ---
| `nil` | All arguments evaluate to`nil`.
|  |
| --- | ---
| `g_val` | Value of the argument that evaluates to non-`nil`, or the value of the last argument if all the preceding arguments evaluate to `nil`.
#### Example

`or(t nil) => tor(nil t) => tor(18 12) => 18`

### sxtd

`sxtd( x_number x_bits ) => x_result`

#### Description

Sign-extends the number represented by the rightmost specified number of bits in the giveninteger.

Sign-extends the rightmost`x_bits` bits of `x_number`. That is, sign-extends the bit field `x_number<x_bits - 1:0>` with `x_number<x_bits - 1>` as the sign bit.

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
| `x_result` | `x_number` with the rightmost `x_bits` sign-extended.
#### Example

`sxtd( 7 4 )  => 7sxtd( 8 4 )  => -8sxtd( 5 2 )  => 5`

#### Reference

[zxtd](arithmetic.html#1041106 "Arithmetic Functions")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
