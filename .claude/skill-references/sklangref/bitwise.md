### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

7
=

Bitwise Operator Functions
==========================

### band

`band( x_op1 x_op2 [ x_op3 ... ] ) => x_result`

#### Description

Returns the integer result of the Boolean AND operation on each parallel pair of bits in eachoperand. Prefix form of the `&` bitwise operator.

#### Arguments

|  |
| --- | ---
| `x_op1` | Operand to be evaluated.
|  |
| --- | ---
| `x_op2` | Operand to be evaluated.
|  |
| --- | ---
| `x_op3` | Optional additional operands to be evaluated.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the operation.
#### Example

`band(12 13)     => 12band(1 2 3 4 5) => 0`

#### Reference

, ,[bnor](#1038878 "Bitwise Operator Functions"), [bnot](#1038920 "Bitwise Operator Functions"), , , ,

### bitfield

`bitfield( x_val x_msb x_lsb ) => x_result`

#### Description

Returns the value of a specified set of bits of a specified integer. Prefix form of the`<:>` operator.

#### Arguments

|  |
| --- | ---
| `x_val` | Integer for which you want to extract the value of a specified setof bits.
|  |
| --- | ---
| `x_msb` | Leftmost bit of the set of bits to be extracted.
|  |
| --- | ---
| `x_lsb` | Rightmost bit of the set of bits to be extracted.
#### Value Returned

|  |
| --- | ---
| `x_result` | Value of the set of bits.
#### Example

`x = 0b1011bitfield(x 2 0) => 3bitfield(x 3 0) => 11`

#### Reference

,[setqbitfield1](#1039235 "Bitwise Operator Functions"),

### bitfield1

`bitfield1( x_val x_bitPosition ) => x_result`

#### Description

Returns the value of a specified bit of a specified integer. Prefix form of the`<>` operator.

#### Arguments

|  |
| --- | ---
| `x_val` | Integer for which you want to extract the value of a specified bit.
|  |
| --- | ---
| `x_bitPosition` | Position of the bit whose value you want to extract.
#### Value Returned

|  |
| --- | ---
| `x_result` | Value of a single bit.
#### Example

`x = 0b1001bitfield1(x 0) => 1bitfield1(x 3) => 1`

#### Reference

[bitfield](#1038735 "Bitwise Operator Functions"), [setqbitfield1](#1039235 "Bitwise Operator Functions"),

### bnand

`bnand( x_op1 x_op2 [ x_op3 ... ] ) => x_result`

#### Description

Returns the integer result of the Boolean NAND operation on each parallel pair of bits in eachoperand. Prefix form of the `~&` bitwise operator.

#### Arguments

|  |
| --- | ---
| `x_op1` | Operand to be evaluated.
|  |
| --- | ---
| `x_op2` | Operand to be evaluated.
|  |
| --- | ---
| `x_op3` | Optional additional operands to be evaluated.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the operation.
#### Example

`bnand(12 13)     => -13bnand(1 2 3 4 5) => -1`

#### Reference

`, band, bnor, bnot, , , ,`

### bnor

`bnor( x_op1 x_op2 [ x_op3 ... ] ) => x_result`

#### Description

Returns the integer result of the Boolean NOR operation on each parallel pair of bits in eachoperand. Prefix form of the `~|` bitwise operator.

#### Arguments

|  |
| --- | ---
| `x_op1` | Operand to be evaluated.
|  |
| --- | ---
| `x_op2` | Operand to be evaluated.
|  |
| --- | ---
| `x_op3` | Optional additional operands to be evaluated.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the operation.
#### Example

`bnor(12 13)     => -14bnor(1 2 3 4 5) => -8`

#### Reference

`, band, , bnot, , , ,`

### bnot

`bnot( x_op ) => x_result`

#### Description

Returns the integer result of the Boolean NOT operation on each parallel pair of bits in eachoperand. Prefix form of the `~` (one's complement) unary operator.

#### Arguments

|  |
| --- | ---
| `x_op` | Operand to be evaluated.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the operation.
#### Example

`bnot(12)  => -13bnot(-12) => 11`

#### Reference

,[band](#1038671 "Bitwise Operator Functions"), , [bnor](#1038878 "Bitwise Operator Functions"), , , ,

### bor

`bor( x_op1 x_op2 [ x_op3 ... ] ) => x_result`

#### Description

Returns the integer result of the Boolean OR operation on each parallel pair of bits in eachoperand. Prefix form of the `|` bitwise operator.

#### Arguments

|  |
| --- | ---
| `x_op1` | Operand to be evaluated.
|  |
| --- | ---
| `x_op2` | Operand to be evaluated.
|  |
| --- | ---
| `x_op3` | Optional additional operands to be evaluated.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the operation.
#### Example

`bor(12 13)     => 13bor(1 2 3 4 5) => 7`

#### Reference

,[band](#1038671 "Bitwise Operator Functions"), , [bnor](#1038878 "Bitwise Operator Functions"), [bnot](#1038920 "Bitwise Operator Functions"), , ,

### bxnor

`bxnor( x_op1 x_op2 [ x_op3 ... ] ) => x_result`

#### Description

Returns the integer result of the Boolean XNOR operation on each parallel pair of bits in eachoperand. Prefix form of the `~^` bitwise operator.

#### Arguments

|  |
| --- | ---
| `x_op1` | Operand to be evaluated.
|  |
| --- | ---
| `x_op2` | Operand to be evaluated.
|  |
| --- | ---
| `x_op3` | Optional additional operands to be evaluated.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the operation.
#### Example

`bxnor(12 13)     => -2bxnor(1 2 3 4 5) => -2`

#### Reference

,[band](#1038671 "Bitwise Operator Functions"), , [bnor](#1038878 "Bitwise Operator Functions"), [bnot](#1038920 "Bitwise Operator Functions"), , ,

### bxor

`bxor( x_op1 x_op2 [ x_op3 ... ] ) => x_result`

#### Description

Returns the integer result of the Boolean XOR operation on each parallel pair of bits in eachoperand. Prefix form of the `^` bitwise operator.

#### Arguments

|  |
| --- | ---
| `x_op1` | Operand to be evaluated.
|  |
| --- | ---
| `x_op2` | Operand to be evaluated.
|  |
| --- | ---
| `x_op3` | Optional additional operands to be evaluated.
#### Value Returned

|  |
| --- | ---
| `x_result` | Result of the operation.
#### Example

`bxor(12 13)     => 1bxor(1 2 3 4 5) => 1`

#### Reference

,[band](#1038671 "Bitwise Operator Functions"), , [bnor](#1038878 "Bitwise Operator Functions"), [bnot](#1038920 "Bitwise Operator Functions"), , ,

### setqbitfield

`setqbitfield( s_var x_val x_msb x_lsb ) => x_result`

#### Description

Sets a value into a set of bits in the bit field specified by the variable`s_var`, stores the new value back into the variable, and then returns the new value. Prefix form of the `<:>=` operator.

#### Arguments

|  |
| --- | ---
| `s_var` | Variable representing the bit field whose value is to be changed.
|  |
| --- | ---
| `x_val` | New value of the bit.
|  |
| --- | ---
| `x_msb` | Leftmost bit of the set of bits whose value is to be changed.
|  |
| --- | ---
| `x_lsb` | Rightmost bit of the set of bits whose value is to be changed.
#### Value Returned

|  |
| --- | ---
| `x_result` | New value of`s_var`.
#### Example

`x = 0`

`setqbitfield(x 0b1001 3 0) => 9x => 9`

`setqbitfield(x 1 2 1) => 11x => 11`

`setqbitfield(x 0 3 2) => 3x => 3`

#### Reference

`, bitfield, setqbitfield1`

### setqbitfield1

`setqbitfield1( s_var x_val x_bitPosition ) => x_result`

#### Description

Sets a value into a single bit in the bit field specified by the variable`s_var`, stores the new value back into the variable, and then returns the new value. Prefix form of the `<>=` operator.

#### Arguments

|  |
| --- | ---
| `s_var` | Variable representing the bit field whose value is to be changed.
|  |
| --- | ---
| `x_val` | New value of the bit.
|  |
| --- | ---
| `x_bitPosition` | Position of the bit whose value you are changing.
#### Value Returned

|  |
| --- | ---
| `x_result` | New value of`s_var`.
#### Example

`x = 0b1001setqbitfield1(x 1 1) => 11x => 11`

`setqbitfield1(x 1 2) => 15x => 15`

#### Reference

,[bitfield](#1038735 "Bitwise Operator Functions"),




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
