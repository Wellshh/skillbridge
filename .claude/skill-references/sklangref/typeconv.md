### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

4
=

Type Conversion Functions
=========================

### charToInt

`charToInt( s_char ) => x_ascii`

#### Description

Returns the ASCII code of the first character of the given symbol. In SKILL, a single charactersymbol can be used as a *character* value.

#### Arguments

|  |
| --- | ---
| `s_char` | A symbol.
#### Value Returned

|  |
| --- | ---
| `x_ascii` | The ASCII code of the (first) character of the given symbol.
#### Example

`charToInt('B)=> 66`

`charToInt('Before)=> 66`

#### Reference

[intToChar](#1038520 "Type Conversion Functions")

### intToChar

`intToChar( x_ascii ) => s_char`

#### Description

Returns the single-character symbol whose ASCII code is the given integer value.

#### Arguments

|  |
| --- | ---
| `x_ascii` | ASCII code.
#### Value Returned

|  |
| --- | ---
| `s_char` | Symbol of single-character whose ASCII code is`x_ascii`.
#### Example

`intToChar( 66)=> B`

#### Reference

[charToInt](#1037774 "Type Conversion Functions")

### listToVector

`listToVector( l_list ) => a_vectorArray`

#### Description

Returns a vector (array) filled with the elements from the given list.

A vector is represented by an array.

#### Arguments

|  |
| --- | ---
| `l_list` | A list whose elements will be stored in consecutive entries in thevector.
#### Value Returned

|  |
| --- | ---
| `a_vectorArray` | Vector filled with the elements from the given list.
#### Example

```
V = listToVector( '( 1 2 3 ) ) => array[3]:1954920V[0] => 1V[1] => 2V[2] => 3V[3]*Error* arrayref: array index out of bounds - V[3]
```

### mod

`mod( x_integer1 x_integer2 ) => x_result`

#### Description

Returns the integer remainder of dividing two integers. The remainder is either zero or hasthe sign of the dividend.

This function is equivalent to`remainder`.

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
| `x_result` | Integer remainder of the division. The sign is determined by thedividend.
#### Example

`mod(4 3) => 1`

#### Reference

, ,

### modf

`modf( f_flonum1f_flonum2 ) => f_result`

#### Description

Returns the floating-point remainder of the division of`f_flonum1` by `f_flonum2`.

#### Arguments

|  |
| --- | ---
| `f_flonum1` | A floating-point number (Dividend).
| `f_flonum2` | A floating-point number (Divisor).
#### Value Returned

|  |
| --- | ---
| `f_result` | Floating-point remainder of the division. The sign is determined by the dividend.
#### Example

`;; Sign is determined by the dividendmodf(-10.1 10.0) => -0.1`

modf(10.1 -10.0) => 0.1

### stringToFunction

`stringToFunction( t_string [ s_langMode ] ) => u_function`

#### Description

Wraps and converts a string of SKILL code into a parameterless SKILL function.

Parses the given string argument and wraps the result with a parameterless`lambda`, then compiles the entire form into a function object. The returned function can later be *applied* with better performance than direct evaluation using `evalstring`.

#### Arguments

|  |
| --- | ---
| `t_string` | String representing some SKILL code.
|  |
| --- | ---
| `s_langMode` | Must be a symbol. Valid values:
|  |
| --- | ---
| `'ils` | Treats the string as SKILL++ code.
| `'il` | Treats the string as SKILL code.
#### Value Returned

|  |
| --- | ---
| `u_function` | Parameterless function equivalent to evaluating the string`(lambda( )``t_string``)`.
#### Example

`f = stringToFunction("1+2") => funobj:0x220038apply(f nil) => 3`

#### Reference

,

### stringToSymbol

`stringToSymbol( t_string ) => s_symbolName`

#### Description

Converts a string to a symbol of the same name.

#### Arguments

|  |
| --- | ---
| `t_string` | String to convert to a symbol.
#### Value Returned

|  |
| --- | ---
| `s_symbolName` | Symbol for the given string.
#### Example

`y = stringToSymbol( "test")=> testsprintf(nil "%L" y)=> "test"`

#### Reference

,

### stringToTime

`stringToTime( t_time ) => x_time`

#### Description

Given a date and time string, returns an integer time value representation. The time argumentmust be in the format as returned by the `timeToString` function, such as: `Dec 28``16:57:06 1996`.

All time conversion functions assume local time, not GMT time.

#### Arguments

|  |
| --- | ---
| `t_time` | String indicating a time and date in this format: "`Dec 28``16:57:06 1996`". Same as format returned by `timeToString` or `getCurrentTime`.
#### Value Returned

|  |
| --- | ---
| `x_time` | Integer time value.
#### Example

`fileTimeModified( "~/.cshrc" )=> 793561559`

`timeToString(793561559)=> "Feb 23 09:45:59 1995"`

`stringToTime("Feb 23 09:45:59 1995")=> 793561559`

#### Reference

, , ,

### symbolToString

`symbolToString( s_symbolName ) => t_string`

#### Description

Converts a symbol to a string of the same name. Same as`get_pname`.

#### Arguments

|  |
| --- | ---
| `s_symbolName` | Symbol to convert.
#### Value Returned

|  |
| --- | ---
| `t_string` | String with the same name as the input symbol.
#### Example

`y = symbolToString( 'test2)=> "test2"sprintf(nil "%L" y)=> "\"test2\""`

### tableToList

`tableToList( o_table ) => l_assoc_list`

#### Description

Converts the contents of an association table to an association list. Use this functioninteractively to look at the contents of a table.

**Note:** This function eliminates the efficiency that you gain from referencing data in anassociation table. Do not use this function for processing data in an association table. Instead, use this function interactively to look at the contents of a table.

#### Arguments

|  |
| --- | ---
| `o_table` | Association table to be converted.
#### Value Returned

|  |
| --- | ---
| `l_assoc_list` | Association list containing key/value pairs from the associationtable.
#### Example

myTable = makeTable( "table" 0)    => table:table
myTable[ "first"] = 1              => 1
myTable[ 'two] = 2                 => 2
tableToList(myTable)               => ((two 2)("first" 1))

### timeToString

`timeToString( x_time ) => t_time/nil`

#### Description

Takes an integer UNIX time value, returns a formatted string that the value denotes. Thestring is always in a form like: `Dec 28 16:57:06 1994`.

#### Arguments

|  |
| --- | ---
| `x_time` | Integer time value.
#### Value Returned

|  |
| --- | ---
| `t_time` | Formatted string the value denotes.
|  |
| --- | ---
| `nil` | Returns`nil` if a negative argument is passed.
#### Example

```
valTime=fileTimeModified( "~/.cshrc" )timeToString(valTime)timeToString(-valTime)
```

`=> "Feb 23 09:45:59 1995"`

`nil`

#### Reference

, ,

### timeToTm

`timeToTm( x_time ) => r_tm`

#### Description

Given an integer time value, returns a`tm` structure.

`r_tm` is a defstruct similar to POSIX's `tm` struct:

```
struct  tm {int     tm_sec;      /* seconds after the minute: [0, 61] */int     tm_min;      /* minutes after the hour: [0, 59] */int     tm_hour;     /* hours after midnight: [0, 23] */int     tm_mday;     /* day of the month: [1, 31] */int     tm_mon;      /* month of the year: [0, 11] */int     tm_year;     /* year since 1900 */int     tm_wday;     /* days since Sunday: [0, 6] */int     tm_yday;     /* days since January: [0, 365] */int     tm_isdst;    /* daylight saving time flag: <0,0,>0*/};
```

* Use`x->??` to get all its fields.

* Use`x->tm_sec` and so forth to access individual fields.

All time conversion functions assume local time, not GMT time.

#### Arguments

|  |
| --- | ---
| `x_time` | Integer time value.
#### Value Returned

|  |
| --- | ---
| `r_tm` | A defstruct similar to POSIX's`tm` struct.
#### Example

`fileTimeModified( "~/.cshrc" )=> 793561559`

`timeToString(793561559)=> "Feb 23 09:45:59 1995"`

`x = timeToTm(793561559)=>array[11]:1702872`

`x->??`

```
(tm_sec 59 tm_min 45 tm_hour    9 tm_mday 23 tm_mon 1    tm_year 95 tm_wday 4 tm_yday    53 tm_isdst 0)
```

`x->tm_mon=>1`

#### Reference

, , ,

### tmToTime

`tmToTime( r_tm ) => x_time`

#### Description

Given a`tm` structure, returns the integer value of the time it represents.

`r_tm` is a defstruct similar to POSIX's `tm` struct:

```
struct  tm {int     tm_sec;      /* seconds after the minute: [0, 61] */int     tm_min;      /* minutes after the hour: [0, 59] */int     tm_hour;     /* hours after midnight: [0, 23] */int     tm_mday;     /* day of the month: [1, 31] */int     tm_mon;      /* month of the year: [0, 11] */int     tm_year;     /* year since 1900 */int     tm_wday;     /* days since Sunday: [0, 6] */int     tm_yday;     /* days since January: [0, 365] */int     tm_isdst;    /* daylight saving time flag: <0,0,>0*/};
```

* Use`x->??` to get all its fields.

* Use`x->tm_sec` and so forth to access individual fields.

All time conversion functions assume local time, not GMT time.

#### Arguments

|  |
| --- | ---
| `r_tm` | A defstruct similar to POSIX's tm struct.
#### Value Returned

|  |
| --- | ---
| `x_time` | Integer time value.
#### Example

`fileTimeModified( "~/.cshrc" )=> 793561559`

`timeToString(793561559)=> "Feb 23 09:45:59 1995"`

`x = timeToTm(793561559)=>array[11]:1702872`

`x->??`

```
(tm_sec 59 tm_min 45 tm_hour    9 tm_mday 23 tm_mon 1    tm_year 95 tm_wday 4 tm_yday    53 tm_isdst 0)
```

`tmToTime(x)=> 793561559`

#### Reference

, , ,

### vectorToList

`vectorToList( a_vectorArray )=> l_list`

#### Description

Returns a list containing the elements of an array.

#### Arguments

|  |
| --- | ---
| `a_vectorArray` | Vector to be converted.
#### Value Returned

|  |
| --- | ---
| `l_list` | List constructed from the given vector.
#### Example

```
vectorToList( vector( 1 2 3 ) ) => ( 1 2 3 )vectorToList( Vector( 3 "Hi"))=> ("Hi" "Hi""Hi")
```

#### Reference

, , ,




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
