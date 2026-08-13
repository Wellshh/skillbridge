<!--
source: sklangref/stringfunc.md
part: 2/2
estimated_tokens: 3382
-->

`rexReplace( t_source t_replacement x_index ) => t_result`

#### Description

Returns a copy of the source string in which the specified substring instances that match thelast compiled regular expression are replaced with the given string.

Scans the source string`t_source` to find all substring(s) that match the last regular expression compiled and replaces one or all of them by the replacement string `t_replacement`. The argument `x_index` tells which occurrence of the matched substring is to be replaced. If it's 0 or negative, all the matched substrings will be replaced. Otherwise only the `x_index` occurrence is replaced. Returns the source string if the specified match is not found.

#### Arguments

|  |
| --- | ---
| `t_source` | Source string to be matched and replaced.
|  |
| --- | ---
| `t_replacement` | Replacement string to be used. Pattern *tags* can be used in this string (see [rexSubstitute](#rexSubstitute "String Functions")).
|  |
| --- | ---
| `x_index` | Specifies which of the matching substrings to replace. Do aglobal replace if it's <= 0.
#### Value Returned

|  |
| --- | ---
| `t_result` | Copy of the source string with specified replacement or theoriginal source string if no match was found.
#### Example

```
rexCompile( "[0-9]+" )               => trexReplace( "abc-123-xyz-890-wuv" "(*)" 1)                                    => "abc-(*)-xyz-890-wuv"rexReplace( "abc-123-xyz-890-wuv" "(*)" 2)                                    => "abc-123-xyz-(*)-wuv"
```

```
rexReplace( "abc-123-xyz-890-wuv" "(*)" 3)                                    => "abc-123-xyz-890-wuv"rexReplace( "abc-123-xyz-890-wuv" "(*)" 0)                                    => "abc-(*)-xyz-(*)-wuv"rexCompile( "xyz" )                 => trexReplace( "xyzzyxyzz" "xy" 0)                                   => "xyzyxyz" ; no rescanning!
```

#### Reference

`rexCompile, rexExecute, rexMatchp, rexSubstitute`

### rexSubstitute

`rexSubstitute( t_string ) => t_result | nil`

#### Description

Substitutes the pattern tags in the argument string with previously matched (sub)strings.

Copies the argument string and substitutes all pattern*tags* in it by their corresponding matched strings in the last string matching operation. The tags are in the form of '\n', where *n* is 0-9. '\0' (or '&') refers to the string that matched the entire regular expression and \k refers to the string that matched the pattern wrapped by the *k*'th \(...\) in the regular expression.

#### Arguments

|  |
| --- | ---
| `t_string` | Argument string to be substituted.
#### Value Returned

|  |
| --- | ---
| `t_result` | Copy of the argument with all the tags in it being substituted bythe corresponding strings.
|  |
| --- | ---
| `nil` | The last string matching operation failed (and none of the patterntags are meaningful).
#### Example

```
rexCompile( "[a-z]+\\([0-9]+\\)" ) => trexExecute( "abc123" )             => trexSubstitute( "*\\0*" )            => "*abc123*"rexSubstitute( "The matched number is: \\1" )                                    => "The matched number is: 123"rexExecute( "123456" )              => nil ; match failedrexSubstitute( "-\\0-")             => nil
```

#### Reference

[rexCompile](#1040094 "String Functions"), [rexExecute](#1040261 "String Functions"), [rexReplace](#1040409 "String Functions")

### rindex

`rindex( t_string1 S_string2 ) => t_result | nil`

#### Description

Returns a string consisting of the remainder of`string1` beginning with the last occurrence of `string2`.

Compares two strings. Similar to`index` except that it looks for the last (that is, rightmost) occurrence of the symbol or string `S_string2` in string `t_string` instead of the first occurrence.

#### Arguments

|  |
| --- | ---
| `t_string1` | String to search for the last occurrence of`S_string2`.
|  |
| --- | ---
| `S_string2` | String or symbol to search for.
#### Value Returned

|  |
| --- | ---
| `t_result` | Remainder of`t_string1` starting with last match of `S_string2`.
|  |
| --- | ---
| `nil` | There is no match.
#### Example

`rindex( "dandelion" "d") => "delion"`

#### Reference

[nindex](#1038874 "String Functions")

### sprintf

`sprintf( {s_Var | nil } t_formatString [ g_arg1 ... ] ) => t_string`

#### Description

Formats the output and assigns the resultant string to the variable given as the first argument.

**Note:** `sprintf` is a syntax form and should not be used as an argument to `apply` or `eval`.

Refer to the "[Common Output Format Specifications](../sklangref/inputoutput.html#outputformat)" table on the `fprintf` manual page. If `nil` is specified as the first argument, no assignment is made, but the formatted string is returned.

#### Arguments

|  |
| --- | ---
| `s_Var` | Variable name.
|  |
| --- | ---
| `nil` | `nil` if no variable name.
|  |
| --- | ---
| `t_formatString` | Format string.
|  |
| --- | ---
| `g_arg1` | Arguments following the format string are printed according totheir corresponding format specifications.
#### Value Returned

|  |
| --- | ---
| `t_string` | Formatted output string.
#### Example

```
sprintf(s "Memorize %s number %d!" "transaction" 5)=> "Memorize transaction number 5!"
```

`s => "Memorize transaction number 5!"`

`p = outfile(sprintf(nil "test%d.out" 10))=> port:"test10.out"`

### strcat

`strcat( S_string1 [ S_string2 ... ] ) => t_result`

#### Description

Takes input strings or symbols and concatenates them.

#### Arguments

|  |
| --- | ---
| `S_string1 S_string2 ...` | One or more input strings or symbols.
#### Value Returned

|  |
| --- | ---
| `t_result` | New string containing the contents of all input strings or symbols`S_string1, S_string2, ...,` concatenated together. The input arguments are left unchanged.
#### Example

`strcat( 'ab "xyz" )        => "abxyz"strcat( "l" "ab" "ef" )    => "labef"`

#### Reference

`buildString, concat, strncat, strcmp, strncmp, substring`

### strcmp

`strcmp( t_string1 t_string2 ) => 1 | 0 | -1`

#### Description

Compares two argument strings alphabetically.

Compares the two argument strings`t_string1` and `t_string2` and returns an integer greater than, equal to, or less than zero depending on whether `t_string1` is alphabetically greater, equal to, or less than `t_string2`. To simply test if the contents of two strings are the same, use the `equal` function.

#### Arguments

|  |
| --- | ---
| `t_string1` | First string to be compared.
|  |
| --- | ---
| `t_string2` | Second string to be compared.
#### Value Returned

1. `t_string1` is alphabetically greater than `t_string2`.

1. `t_string1` is alphabetically equal to `t_string2`.

|  |
| --- | ---
| `-1` | `t_string1` is alphabetically less than `t_string2`.
#### Example

```
strcmp( "abc" "abb" )    => 1strcmp( "abc" "abc")     => 0strcmp( "abc" "abd")     => -1
```

#### Reference

`strncmp`

### stringp

`stringp( g_value ) => t | nil`

#### Description

Checks if an object is a string.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A data object.
#### Value Returned

|  |
| --- | ---
| `t` | `g_value` is a string.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`stringp( 93)=> nil`

`stringp( "93")=> t`

#### Reference

[listp](list.html#1039344 "List Functions"), [symbolp](dataoperator.html#1040737 "Data Operator Functions")

### strlen

`strlen( t_string ) => x_length`

#### Description

Returns the number of characters in a string.

#### Arguments

|  |
| --- | ---
| `t_string` | String length you want to obtain.
#### Value Returned

|  |
| --- | ---
| `x_length` | Length of`t_string`.
#### Example

`strlen( "abc" )    => 3strlen( "\007" )   => 1  ; Backslash notation used.`

#### Reference

[parseString](#1038922 "String Functions"), [substring](#1041005 "String Functions"), [strcat](#1053714 "String Functions"), [strcmp](#1040645 "String Functions"), [strncmp](#1040843 "String Functions"), [stringp](#1040671 "String Functions")

### strncat

`strncat( t_string1 t_string2 x_max ) => t_result`

#### Description

Creates a new string by appending a maximum number of characters from`t_string2` to `t_string1`.

Concatenates input strings.Similar to `strcat` except that at most `x_max` characters from `t_string2` are appended to the contents of `t_string1` to create the new string. `t_string1` and `t_string2` are left unchanged.

#### Arguments

|  |
| --- | ---
| `t_string1` | First string included in the new string.
|  |
| --- | ---
| `t_string2` | Second string whose characters are appended to`t_string1`.
|  |
| --- | ---
| `x_max` | Maximum number of characters from`t_string2` that you want to append to the end of `t_string1`.
#### Value Returned

|  |
| --- | ---
| `t_result` | The new string;`t_string1` and `t_string2` are left unchanged.
#### Example

```
strncat( "abcd" "efghi" 2)        => "abcdef"strncat( "abcd" "efghijk" 5)      => "abcdefghi"
```

#### Reference

`parseString, strcat, strcmp, strncmp, substring, stringp`

### strncmp

`strncmp( t_string1 t_string2 x_max ) => 1 | 0 | -1`

#### Description

Compares two argument strings alphabetically only up to a maximum number of characters.

Similar to`strcmp` except that only up to `x_max` characters are compared. To simply test if the contents of two strings are the same, use the `equal` function.

#### Arguments

|  |
| --- | ---
| `t_string1` | First string to be compared.
|  |
| --- | ---
| `t_string2` | Second string to be compared.
|  |
| --- | ---
| `x_max` | Maximum number of characters in both strings to be compared.
#### Value Returned

For the first specified number of characters:

1. `t_string1` is alphabetically greater than `t_string2`

1. `t_string1` is alphabetically equal to `t_string2`.

|  |
| --- | ---
| `-1` | `t_string1` is alphabetically less than `t_string2`.
#### Example

```
strncmp( "abc" "ab" 3)  => 1strncmp( "abc" "de" 4)  => -1strncmp( "abc" "ab" 2)  => 0
```

#### Reference

[strcmp](#1040645 "String Functions")

### strpbrk

`strpbrk( t_str1t_str2) => t_subStr/nil`

#### Description

Returns a substring of the first occurence in`t_str1` of any character from the string pointed to by `t_str2`

#### Arguments

|  |
| --- | ---
| `t_str1` | Specifies the string that you need to scan
|  |
| --- | ---
| `t_str2` | Specifies the pattern that you need to match
#### Value Returned

|  |
| --- | ---
| `t_substr` | Returns a substring of the first occurence of any characterspecified in `t_str2`
|  |
| --- | ---
| `nil` | Returns`nil` if no occurence of any character from `t_str2` is found in `t_str1`
#### Example

`s="world"`

`strpbrk(s "o")`

`=>"orld"`

`strpbrk(s "sssssl")`

`=>"ld"`

`strpbrk(s "ss")`

`=>nil`

`strpbrk("WORLD" "world")`

`=>nil`

`strpbrk("WORLD" " ")`

=>nil

### subst

`subst( g_x g_y l_arg ) => l_result`

#### Description

Substitutes one object for another object in a list.

#### Arguments

|  |
| --- | ---
| `g_x` | Object substituted.
|  |
| --- | ---
| `g_y` | Object substituted for.
|  |
| --- | ---
| `l_arg` | A list.
#### Value Returned

|  |
| --- | ---
| `l_result` | Result of substituting`g_x` for all `equal`occurrences of `g_y` at all levels in `l_arg`.
#### Example

```
subst( 'a 'b '(a b c) )              => (a a c)subst('x 'y '(a b y (d y (e y))))    => (a b x (d x (e x )))
```

#### Reference

[remd](list.html#1039715 "List Functions")

### substring

`substring( S_string x_index [ x_length ] ) => t_result | nil`

#### Description

Creates a new substring from an input string, starting at an index point and continuing for a given length.

Creates a new substring from`S_string` with a starting point determined by `x_index` and length determined by an optional third argument `x_length`.

* If`S_string` is a symbol, the substring is taken from its print name.

* If`x_length` is not given, then all of the characters from `x_index` to the end of the string are returned.

* If`x_index` is negative the substring begins at the indexed character from the end of the string.

* If`x_index` is out of bounds (that is, its absolute value is greater than the length of `S_string`), `nil` is returned.

#### Arguments

|  |
| --- | ---
| `S_string` | A string.
|  |
| --- | ---
| `x_index` | Starting point for returning a new string. Cannot be zero.
|  |
| --- | ---
| `x_length` | Length of string to be returned.
#### Value Returned

|  |
| --- | ---
| `t_result` | Substring of`S_string` starting at the character indexed by `x_index`, with a maximum of `x_length` characters.
|  |
| --- | ---
| `nil` | If`x_index` is out of bounds.
#### Example

```
substring("abcdef" 2 4)    => "bcde"substring("abcdef" 4 2)    => "de"substring("abcdef" -4 2)   => "cd"
```

#### Reference

[parseString](#1038922 "String Functions")

### upperCase

`upperCase( S_string ) => t_result`

#### Description

Returns a string that is a copy of the given argument with the lowercase alphabetic charactersreplaced by their uppercase equivalents.

If the parameter is a symbol, the name of the symbol is used.

#### Arguments

|  |
| --- | ---
| `S_string` | Input string or symbol.
#### Value Returned

|  |
| --- | ---
| `t_result` | Copy of`S_string` in uppercase letters.
#### Example

`upperCase("Hello world!") => "HELLO WORLD!"`

#### Reference

[lowerCase](#1041866 "String Functions")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
