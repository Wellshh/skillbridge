### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

8
=

Trigonometric Functions
=======================

### asin

`asin( n_number ) => f_result`

#### Description

Returns the arc sine of a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `f_result` | Arc sine of the value passed in.
#### Example

`asin(0.3) => 0.3046927`

#### Reference

### atan

`atan( n_number ) => f_result`

#### Description

Returns the arc tangent of a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `f_result` | Arc tangent of`n_number`.
#### Example

`atan(0.3) => 0.2914568`

#### Reference

`, atan2`

### atan2

`atan2(n_yn_x) => f_result`

#### Description

Computes the principal value of the arc tangent of`n_y`/`n_x`, using the signs of both arguments to determine the quadrant of the return value.

#### Arguments

|  |
| --- | ---
| `n_y` | Vertical coordinate value.
|  |
| --- | ---
| `n_x` | Horizontal coordinate value.
|  |
| --- | ---
| `n_y`/`n_x` is the tangent of the required angle. |
#### Value Returned

|  |
| --- | ---
| `f_result` | Arc tangent of`y/x` in the range `[-pi,pi]` radians. If both arguments are 0.0, 0.0 is returned.
|  |
| --- | ---
|  | If`x` or `y` is `NaN`, `NaN` is returned.
|  |
| --- | ---
|  | In IEEE754 mode,`atan2()` handles the following exceptional arguments according to ANSI/IEEE Std 754-1985:
|  |
| --- | ---
|  | `atan2(+0,x)` returns `+0` for `x>0` or `x=+0``atan2(+0,x)` returns `+pi` for `x<0` or `x=-0``atan2(y,+0)` returns `pi/2` for `y>0``atan2(y,+0)` returns `-pi/2` for `y<0``atan2(+y,Inf)` returns `+0` for finite `y>0``atan2(+Inf,x)` returns `+pi/2` for finite `x``atan2(+y,-Inf)` returns `+pi` for finite `y>0``atan2(+Inf,Inf)` returns `+pi/4``atan2(+Inf,-Inf)` returns `+3pi/4`
#### Example

`atan2(1 1) => 0.7853982`

`atan2(0 0) => 0.0`

#### Reference

[atan](#1037693 "Trigonometric Functions"),

### cos

`cos( n_number ) => f_result`

#### Description

Returns the cosine of a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `f_result` | Cosine of`n_number`.
#### Example

`cos(0.3)         => 0.9553365cos(3.14/2)      => 0.0007963`

#### Reference

### sin

`sin( n_number ) => f_result`

#### Description

Returns the sine of a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `f_result` | Sine of`n_number`.
#### Example

`sin(3.14/2)        => 0.9999997sin(3.14159/2)     => 1.0`

Floating point results from evaluating the same expressions may be machine dependent.

#### Reference

,[asin](#1037652 "Trigonometric Functions"),

### tan

`tan( n_number ) => f_result`

#### Description

Returns the tangent of a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `f_result` | Tangent of`n_number`.
#### Example

`tan( 3.0 ) => -0.1425465`

#### Reference

[atan](#1037693 "Trigonometric Functions"), [atan2](#1037715 "Trigonometric Functions"), ,

### acos

`acos( n_number ) => f_result`

#### Description

Returns the arc cosine of a floating-point number or integer.

#### Arguments

|  |
| --- | ---
| `n_number` | Floating-point number or integer.
#### Value Returned

|  |
| --- | ---
| `f_result` | Arc cosine of`n_number`.
#### Example

`acos(0.3)=> 1.266104`

#### Reference




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
