<!--
source: sklangref/stringfunc.md
part: 1/2
estimated_tokens: 13487
-->

### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

5
=

String Functions
================

### blankstrp

`blankstrp( t_string ) => t | nil`

#### Description

Checks if the given string is empty or has blank space characters only and returns`true`. If there are non-space characters `blankstrp` returns `nil`.

#### Arguments

|  |
| --- | ---
| `t_string` | A string.
#### Value Returned

|  |
| --- | ---
| `t` | If`t_string` is blank or is an empty string.
|  |
| --- | ---
| `nil` | If there are non-space characters.
#### Example

`blankstrp( "")t`

`blankstrp( " ")t`

     blankstrp( "a string")
nil

### buildString

`buildString( l_strings [ S_glueCharacters ] ) => t_string`

#### Description

Concatenates a list of strings with specified separation characters.

#### Arguments

|  |
| --- | ---
| `l_strings` | List of strings. A null string is permitted.
|  |
| --- | ---
| `S_glueCharacters` | Separation characters you use within the strings. A null string ispermitted. If this argument is omitted, the default single space is used.
#### Value Returned

|  |
| --- | ---
| `t_string` | Strings concatenated with`t_glueCharacters`. Signals an error if `l_strings` is not a list of strings.
#### Example

```
buildString( '("test" "il") ".")      => "test.il"buildString( '("usr" "mnt") "/")      => "usr/mnt"buildString( '("a" "b" "c"))          => "a b c"buildString( '("a" "b" "c") "")       => "abc"buildString( '("A" "B") 'and)         => "AandB"
```

#### Reference

`parseString`

### getchar

`getchar( S_arg x_index ) => s_char | nil`

#### Description

Returns an indexed character of a string or the print name if the string is a symbol.Unlike the C library, the `getc` and `getchar` SKILL functions are totally unrelated.

#### Arguments

|  |
| --- | ---
| `S_arg` | Character string or symbol.
|  |
| --- | ---
| `x_index` | Number corresponding to an indexed point in`S_arg`.
#### Value Returned

|  |
| --- | ---
| `s_char` | Single character symbol corresponding to the character in`S_arg` indexed by `x_index`.
|  |
| --- | ---
| `nil` | If`x_index` is less than 1 or greater than the length of the string.
#### Example

`getchar("abc" 2)  => bgetchar("abc" 4)  => nil`

#### Reference

[nindex](#1038874 "String Functions"), [parseString](#1038922 "String Functions"), [strlen](#1040734 "String Functions"), [substring](#1041005 "String Functions")

### index

`index( t_string1 S_string2 ) => t_result | nil`

#### Description

Returns a string consisting of the remainder of`string1` beginning with the first occurrence of `string2`.

#### Arguments

|  |
| --- | ---
| `t_string1` | String to search for the first occurrence of`S_string2`.
|  |
| --- | ---
| `S_string2` | String to search for in`t_string1`.
#### Value Returned

|  |
| --- | ---
| `t_result` | If`S_string2` is found in `t_string1`, returns a string equal to the remainder of `t_string1` that begins with the first character of `S_string2`.
|  |
| --- | ---
| `nil` | If`S_string2` is not found.
#### Example

index( "abc" 'b )            => "bc"
index( "abcdabce" "dab" )    => "dabce"
index( "abc" "cba" )         => nil
index( "dandelion" "d")      => "dandelion"

### lowerCase

`lowerCase( S_string ) => t_result`

#### Description

Returns a string that is a copy of the given argument with uppercase alphabetic charactersreplaced by their lowercase equivalents.

If the parameter is a symbol, the name of the symbol is used.

#### Arguments

|  |
| --- | ---
| `S_string` | Input string or symbol.
#### Value Returned

|  |
| --- | ---
| `t_result` | Copy of`S_string` in lowercase letters.
#### Example

`lowerCase("Hello World!") => "hello world!"`

#### Reference

[upperCase](#1041067 "String Functions")

### lsprintf

`lsprintf( t_formatString[ g_arg1 ... ] ) => t_string`

#### Description

Returns a string according to the provided format.`lsprintf` is a lambda version of the `sprintf` function that can be used as an argument with `apply`or`funcall`.

Refer to the "[Common Output Format Specifications](../sklangref/inputoutput.html#outputformat)" table on the `fprintf` manual page. If `nil` is specified as the first argument, no assignment is made, but the formatted string is returned.

#### Arguments

|  |
| --- | ---
| `t_formatString` | Specifies the format string
|  |
| --- | ---
| `g_arg1` | Specifies the arguments following the format string that areprinted corresponding to their format specifications.
#### Value Returned

|  |
| --- | ---
| `t_string` | Returns the formatted string
#### Example

```
let( (format( "%d %d %s %L\n")    printf_style_args( (list 42 41 "hello" (list "world"))))    apply( 'lsprintf format printf_style_args))
```

=>"42 41 hello (\"world\")\n"

### nindex

`nindex( t_string1 S_string2 ) => x_result | nil`

#### Description

Finds the symbol or string,`S_string2`, in `t_string1` and returns the character index, starting from one, of the first point at which the `S_string2` matches part of `t_string1`.

#### Arguments

|  |
| --- | ---
| `t_string1` | String you want to search for`S_string2`.
|  |
| --- | ---
| `S_string2` | String you want to find occurrences of in`t_string1`.
#### Value Returned

|  |
| --- | ---
| `x_result` | Index corresponding to the point at which`S_string2` matches part of `t_string1`. The index starts from one.
|  |
| --- | ---
| `nil` | No character match.
#### Example

```
nindex( "abc" 'b )            => 2nindex( "abcdabce" "dab" )    => 4nindex( "abc" "cba" )         => nil
```

#### Reference

[getchar](#1038768 "String Functions"), [substring](#1041005 "String Functions")

### outstringp

`outstringp( g_port ) => t / nil`

#### Description

Checks whether the specified value is an outstring port.

#### Arguments

|  |
| --- | ---
| `g_port` | The value to be checked.
#### Value Returned

|  |
| --- | ---
| `t` | If the given value is an outstring port.
| nil | If the given value is not an outstring port.
#### Example

`p = outstring()`

`outstringp(p)`

`= >t`

### parseString

`parseString( S_string [ S_breakCharacters ] ) => l_strings`

#### Description

Breaks a string into a list of substrings with break characters.

Returns the contents of`S_string` broken up into a list of words. If the optional second argument, `S_breakCharacters`, is not specified, the white space characters, \t\f\r\n\v, are used as the default.

A sequence of break characters in`S_string` is treated as a single break character. By this rule, two spaces or even a tab followed by a space is the same as a single space. If this rule were not imposed, successive break characters would cause null strings to be inserted into the output list.

If`S_breakCharacters` is a null string, `S_string` is broken up into characters. You can think of this as inserting a null break character after each character in `S_string`.

No special significance is given to punctuation characters, so the "words" returned by`parseString` might not be grammatically correct.

#### Arguments

|  |
| --- | ---
| `S_string` | String to be parsed.
|  |
| --- | ---
| `S_breakCharacters` | List of individual break characters.
#### Value Returned

|  |
| --- | ---
| `l_strings` | List of strings parsed from`S_string`.
#### Example

`parseString( "Now is the time" )   => ("Now" "is" "the" "time")`

Space is the default break character

`parseString( "prepend" "e" )       => ("pr" "p" "nd" )`

`e` is the break character.

`parseString( "feed" "e")           => ("f" "d")`

A sequence of break characters in`S_string` is treated as a single break character.

`parseString( "~/exp/test.il" "./") => ("~" "exp" "test" "il")`

Both . and / are break characters.

`parseString( "abc de" "")          => ("a" "b" "c" " " "d" "e")`

The single space between`c` and `d` contributes " " in the return result.

#### Reference

[buildString](#1038709 "String Functions"), [linereadstring](inputoutput.html#1039880 "Input Output Functions"), [strcat](#1053714 "String Functions"), [strlen](#1040734 "String Functions"), [stringp](#1040671 "String Functions")

### pcreCompile

`pcreCompile( t_pattern [ x_options ] ) => o_comPatObj | nil`

#### Description

Compiles a regular expression string pattern (`t_pattern`) into an internal representation that you can use in a [`pcreExecute`](../sklangref/stringfunc.html#pcreExecute) function call. The compilation method is PCRE/Perl-compatible. You can use a second (optional) argument to specify independent option bits for controlling pattern compilation. You can set and unset the [`PCRE_CASELESS`](../sklangref/stringfunc.html#PCRE_CASELESS), [`PCRE_MULTILINE`](../sklangref/stringfunc.html#PCRE_MULTILINE), [`PCRE_DOTALL`](../sklangref/stringfunc.html#PCRE_DOTALL), and [`PCRE_EXTENDED`](../sklangref/stringfunc.html#PCRE_EXTENDED) independent option bits from within the pattern. The content of the options argument specifies the initial setting at the start of compilation. You can set the [`PCRE_ANCHORED`](../sklangref/stringfunc.html#PCRE_ANCHORED) option at matching time and at compile time.

**Note:** PCRE stands for*Perl Compatible Regular Expressions*. The PCRE library contains functions that implement Perl-compatible regular expression pattern matching. You can visit [`http://www.pcre.org`](http://www.pcre.org) for more information.

#### Arguments

|  |
| --- | ---
| `t_pattern` | String containing regular expression string to be compiled.
`x_options` (Optional) Independent option bits that affect the compilation. You can specify zero or more of these options symbolically using the [`pcreGenCompileOptBits`](#pcreGenCompileOptBits "String Functions") SKILL function.
Valid values:

|  |  |
| --- | --- | ---
|  | **PCRE\_CASELESS / 0x00000001** |
|  |  | Equivalent to setting?caseLess t using the pcreGenCompileOptBits SKILL function.
|  | PCRE\_MULTILINE / 0x00000002 |
|  |  | Equivalent to setting?multiLine t using the pcreGenCompileOptBits SKILL function.
|  | PCRE\_DOTALL / 0x00000004 |
|  |  | Equivalent to setting?dotAll t using the pcreGenCompileOptBits SKILL function.
|  | PCRE\_EXTENDED / 0x00000008 |
|  |  | Equivalent to setting?extended t using the pcreGenCompileOptBits SKILL function.
|  | PCRE\_ANCHORED / 0x00000010 |
|  |  | Equivalent to setting?anchored t using the pcreGenCompileOptBits SKILL function.
|  | PCRE\_DOLLAR\_ENDONLY / 0x00000020 |
|  |  | Equivalent to setting?dollar\_endonly t using the pcreGenCompileOptBits SKILL function.
|  | PCRE\_UNGREEDY / 0x00000200 |
|  |  | Equivalent to setting?ungreedy t using the pcreGenCompileOptBits SKILL function.
|  | PCRE\_NO\_AUTO\_CAPTURE / 0x00001000 |
|  |  | Equivalent to setting ?no\_auto\_capture t using the pcreGenCompileOptBits SKILL function.
|  | PCRE\_FIRSTLINE / 0x00040000 |
|  |  | Equivalent to setting?firstline t using the pcreGenCompileOptBits SKILL function.
#### Value Returned

|  |
| --- | ---
| `o_comPatObj` | Data object containing the compiled pattern.
|  |
| --- | ---
| `nil` | Pattern compilation failed. An error message indicating thecause of the failure appears.
#### Example

```
comPat1 = pcreCompile( "\\Qabc\\$xyz\\E" ) => pcreobj@0x27d0fcpcreExecute( comPat1 "abc\\$xyz" )         => t
```

```
comPat2 = pcreCompile( "sam|Bill|jack|alan|bob" ) => pcreobj@0x27d108pcreExecute( comPat2 "alan" )                => t
```

```
comPat3 = pcreCompile( "z{1,5}" ) => pcreobj@0x27d120pcreExecute( comPat3 "zzzzz" ) => t
```

```
comPat4 = pcreCompile( "/\\*.*?\\*/" ) => pcreobj@0x27d12cpcreExecute( comPat4 "/* first command */ not comment /* second comment */" ) => t
```

```
comPat5 = pcreCompile( "^[a-z][0-9a-z]*" pcreGenCompileOptBits(?caseLess t) ) => pcreobj@0x27d138pcreExecute( "AB12cd" ) => t
```

```
comPat6 = pcreCompile( "[a-z" ) => *Error* pcreCompile: compilation failed at offset 4: missing terminating ] for character classnil
```

#### Reference

[pcreExecute](#pcreExecute "String Functions"), [pcreGenCompileOptBits](#pcreGenCompileOptBits "String Functions")

### pcreExecute

`pcreExecute( o_comPatObj S_subject [ x_options ] ) => t | nil`

#### Description

Matches the subject string or symbol (`S_subject`) against a previously compiled pattern set up by the last [`pcreCompile`](../sklangref/stringfunc.html#pcreCompile) call (`o_comPatObj`). The matching algorithm is PCRE/Perl-compatible. You can use a third (optional) argument to specify independent option bits for controlling pattern matching. You can use this function in conjunction with [`pcreCompile`](../sklangref/stringfunc.html#pcreCompile) to match several subject strings or symbols against a single pattern.

#### Arguments

|  |
| --- | ---
| `o_comPatObj` | Data object containing the compiled pattern returned from aprevious [`pcreCompile`](../sklangref/stringfunc.html#pcreCompile) call.
|  |
| --- | ---
| `S_subject` | Subject string or symbol to be matched. If it is a symbol, its printname is used.
|  |
| --- | ---
| `x_options` | (Optional) Independent option bits that affect pattern matching.You can specify zero or more of these options symbolically using the [`pcreGenExecOptBits`](#pcreGenExecOptBits "String Functions") SKILL function. Valid values:
|  |  |
| --- | --- | ---
|  | `PCRE_ANCHORED` | Equivalent to setting[`?anchored t`](#g_setAnchoredp pcreGenExecOptBits "String Functions") using the [`pcreGenExecOptBits`](#pcreGenExecOptBits "String Functions") SKILL function.
|  | `PCRE_NOTBOL` | Equivalent to setting[`?notbol t`](#g_setNotbolp "String Functions") using the [`pcreGenExecOptBits`](#pcreGenExecOptBits "String Functions") SKILL function.
|  | `PCRE_NOTEOL` | Equivalent to setting[`?noteol t`](#g_setNoteolp "String Functions") using the [`pcreGenExecOptBits`](#pcreGenExecOptBits "String Functions") SKILL function.
|  | `PCRE_NOTEMPTY` | Equivalent to setting[`?notempty t`](#g_setNotemptyp "String Functions") using the [`pcreGenExecOptBits`](#pcreGenExecOptBits "String Functions") SKILL function.
|  | `PCRE_PARTIAL` | Equivalent to setting[`?partial t`](#g_setPartialp "String Functions") using the [`pcreGenExecOptBits`](#pcreGenExecOptBits "String Functions") SKILL function.
#### Value Returned

|  |
| --- | ---
| `t` | A match is found.
|  |
| --- | ---
| `nil` | No match. You can see the error message associated with this matching failure by calling [`pcrePrintLastMatchErr`](#pcrePrintLastMatchErr "String Functions").
#### Example

```
comPat1 = pcreCompile( "[12[:^digit:]]" ) => pcreobj@0x27d150pcreExecute( comPat1 "abc" )             => t
```

```
comPat2 = pcreCompile( "((?i)ab)c" ) => pcreobj@0x27d15cpcreExecute( comPat2 "aBc" )         => t
```

```
comPat3 = pcreCompile( "\\d{3}" ) => pcreobj@0x27d168pcreExecute( comPat3 "789" )      => t
```

```
comPat4 = pcreCompile( "(\\D+|<\\d+>)*[!?]" ) => pcreobj@0x27d174pcreExecute( comPat4 "Hello World!" )         => t
```

```
comPat5 = pcreCompile( "^\\d?\\d(jan|feb|mar|apr|may|jun)\\d\\d$/" ) => pcreobj@0x27d180pcreExecute( comPat5 "25jun3" ) => nilpcreExecute( comPat5 "25jun3" pcreGenExecOptBits(?anchored t) ) => nilpcreExecute( comPat5 "25jun3" pcreGenExecOptBits(?partial t) ) => t
```

#### Reference

`pcreCompile, pcreExecute, pcreGenExecOptBits`

### pcreGenCompileOptBits

```
pcreGenCompileOptBits( [ ?caseLess  g_setCaseLessp ][ ?multiLine g_setMultiLinep ][ ?dotAll    g_setDotAllp ][ ?extended  g_setExtendedp ][ ?anchored  g_setAnchoredp ][ ?dollar_endonly g_setDollarEndonlyp ][ ?ungreedy  g_setUngreedyp ][ ?no_auto_capture g_setNoAutoCapturep ][ ?firstline g_setFirstlinep ]) => x_resultOptBits
```

#### Description

Generates bitwise inclusive OR--`bor()`--of zero or more independent option bits that affect compilation so that you can specify them symbolically in the [`pcreCompile`](../sklangref/stringfunc.html#pcreCompile) function. If you call `pcreGenCompileOptBits` with no arguments, the function returns a zero (options have their default settings).

#### Arguments

|  |
| --- | ---
| `g_setCaseLessp` | When not`nil`, letters in the pattern match both upper and lower case letters. Setting this bit is equivalent to using Perl's `/i` option. You can change this setting within a pattern using `(?i)`.
|  |
| --- | ---
| `g_setMultiLinep` | When not`nil`, each newline in the subject string defines a line of characters for which the start-of-line metacharacter (`^`) matches at the start of the line and the end-of-line metacharacter (`$`) matches at the end of the line.  By default, PCRE treats the subject string as a single line of characters, even if it contains newlines, such that the start-of-line metacharacter (`^`) matches only at the start of the string and the end-of-line metacharacter (`$`) matches only at the end of the string, or before a terminating newline (unless [`PCRE_DOLLAR_ENDONLY`](../sklangref/stringfunc.html#PCRE_DOLLAR_ENDONLY) is set).
|  |
| --- | ---
| `g_setDotAllp` | When not`nil`, a dot metacharater in the pattern matches all characters, including newlines. Without it, newlines are excluded.  Setting this bit is equivalent to using Perl's `/s` option. You can change this setting within a pattern using `(?s)`. A negative class such as `[^a]` always matches a newline character, independent of whether this bit is set or not.
|  |
| --- | ---
| `g_setExtendedp` | When not`nil`, PCRE ignores whitespace data characters in the pattern except when they are escaped or inside a character class.  Whitespace does not include the VT character (code 11).  PCRE also ignores characters between an unescaped `#` outside a character class and the next newline character, inclusive.  Setting this bit is equivalent to using Perl's `/x` option. You can change this setting within a pattern using `(?x)`.  You can use this setting to include comments (data characters only) inside complicated patterns.  You may not use whitespace characters in special character sequences in a pattern, such as `(?(` which introduces a conditional subpattern.
|  |
| --- | ---
| `g_setAnchoredp` | When not`nil`, PCRE constrains the match to the first matching point in the subject string. You can achieve this same effect using appropriate constructs in the pattern itself.
|  |
| --- | ---
| `g_setDollarEndonlyp` | When not`nil`, a dollar metacharacter in the pattern matches at the end of the subject string only. Without this option, a dollar metacharacter also matches immediately before the final character if it is a newline (but not before any other newlines). PCRE ignores this setting if you specify [`PCRE_MULTILINE`](../sklangref/stringfunc.html#PCRE_MULTILINE).
|  |
| --- | ---
| `g_setUngreedyp` | When not`nil`, PCRE inverts the greed of quantifiers so that they are not greedy by default. You can force a quantifier to become greedy by putting `?` after it. You can change this setting within a pattern using `(?U)`.
|  |
| --- | ---
| `g_setNoAutoCapturep` | When not`nil`, If you set this bit, you are disabling the use of numbered capturing parentheses in a pattern. Any opening parenthesis that is not followed by `?` behaves as if it were followed by `?:` but you can still use named parentheses for capturing (and they acquire numbers in the usual way).
|  |
| --- | ---
| `g_setFirstlinep` | When not`nil`, PCRE requires an unanchored pattern to match before or at the first newline character in the subject string; the matched text may continue over the newline.
#### Value Returned

|  |
| --- | ---
| `x_resultOptBits` | Bitwise inclusive OR--`bor()`--of zero or more independent option bits that affect pattern compilation.
#### Example

```
comPat1 = pcreCompile( "^abc$"pcreGenCompileOptBits(?dollar_endonly t ?multiLine t) ) = > pcreobj@0x27d060pcreExecute( comPat1 "abc\ndef") => t
```

```
pcreMatchAssocList("^[a-z][0-9]*$"'((abc "ascii") ("123" "number") ("yy\na123"  "alphanum") (a12z "ana"))pcreGenCompileOptBits(?multiLine t) pcreGenExecOptBits( ?notbol t) )=> (("yy\na123" "alphanum"))
```

#### Reference

`pcreCompile, pcreExecute, pcreGenExecOptBits, pcreMatchAssocList`

### pcreGenExecOptBits

```
pcreGenExecOptBits( [ ?anchored g_setAnchoredp ][ ?notbol   g_setNotbolp ][ ?noteol   g_setNoteolp ][ ?notempty g_setNotemptyp ][ ?partial  g_setPartialp ])=> x_resultOptBits
```

#### Description

Generates bitwise inclusive OR--`bor()`--of zero or more independent option bits that affect pattern matching so that you can specify them symbolically in the [`pcreExecute`](#pcreExecute "String Functions") function. If you call `pcreGenExecOptBits` with no arguments, the function returns a zero (options have their default settings).

#### Arguments

|  |
| --- | ---
| `g_setAnchoredp` | When not`nil`, PCRE constrains the match to the first matching point in the [`pcreExecute`](#pcreExecute "String Functions") function.  If you compiled a pattern using the [`PCRE_ANCHORED`](../sklangref/stringfunc.html#PCRE_ANCHORED) option, or if the pattern was anchored by virtue of its contents, then it must also be anchored at matching time.
|  |
| --- | ---
| `g_setNotbolp` | When not`nil`, the first character of the subject string is not the beginning of a line such that the circumflex metacharacter `^` does not match before it. If you enable this option without setting the [`PCRE_MULTILINE`](../sklangref/stringfunc.html#PCRE_MULTILINE) option (at compile time), the circumflex metacharacter never results in a match.  This option affects the behavior of `^` only; it does not affect the behavior of `\A`.
|  |
| --- | ---
| `g_setNoteolp` | When not`nil`, the end of the subject string is not the end of a line such that the dollar sign metacharacter `$` does not match it nor does it match a newline character immediately before it (except if you have set the [`PCRE_MULTILINE`](../sklangref/stringfunc.html#PCRE_MULTILINE) option). If you enable this option without setting the [`PCRE_MULTILINE`](../sklangref/stringfunc.html#PCRE_MULTILINE) option (at compile time), the dollar sign metacharacter never results in a match.  This option affects the behavior of `$` only; it does not affect the behavior of `\Z` or `\z`.
|  |
| --- | ---
| `g_setNotemptyp` | When not`nil`, an empty string is not a valid match. PCRE attempts to match any alternatives in the pattern. If all the alternatives match the empty string, the entire match fails. For example, if you do not set this option, when PCRE applies the following sequence to a string that does not begin with `a` or `b`, it matches the empty string at the start of the subject:
|  |
| --- | ---
|  | `a?b?`
|  |
| --- | ---
|  | If you set this option, an empty string is not a valid match; PCREsearches further into the string for occurrences of `a` or `b`.
|  |
| --- | ---
| `g_setPartialp` | When not`nil`, the function returns `PCRE_ERROR_PARTIAL` instead of `PCRE_ERROR_NOMATCH` in the case of a partial match. A partial match occurs when PCRE encounters the end of a subject string before it can match the complete pattern. You may not use this option with all patterns. The following restrictions apply:
|  |
| --- | ---
|  | You may not specify quantified atom matches to search forrepeated single characters or repeated single metasequences where the maximum quantity is greater than one. However, you may specify quantifiers with any values after parentheses. For example:
|  |
| --- | ---
|  | Use`(a){2,4}` instead of `a{2,4}`. Use `(\d)+` instead of `\d+`.
#### Value Returned

|  |
| --- | ---
| `x_resultOptBits` | Bitwise inclusive OR--`bor()`--of zero or more independent option bits that affect pattern matching.
#### Example

```
comPat = pcreCompile( "^\\d?\\d(jan|feb|mar|apr|may|jun)\\d\\d$/" )=> pcreobj@0x27d0d8pcreExecute( comPat "25jun3" pcreGenExecOptBits(?partial t) )=> t
```

```
pcreMatchAssocList("^[a-z][0-9]*$"'((abc "ascii") ("123" "number") ("yy\na123"  "alphanum") (a12z "ana"))pcreGenCompileOptBits(?multiLine t) pcreGenExecOptBits( ?notbol t) )=> (("yy\na123" "alphanum"))
```

#### Reference

[pcreCompile](#pcreCompile "String Functions"), [pcreExecute](#pcreExecute "String Functions"), [pcreGenCompileOptBits](#pcreGenCompileOptBits "String Functions"), [pcreMatchAssocList](#pcreMatchAssocList "String Functions")

### pcreListCompileOptBits

`pcreListCompileOptBits()=> t`

#### Description

Displays information about the options used with`pcreGenCompileOptBits`. See the description of `pcreGenCompileOptBits` for more information.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | Returns`t`.
#### Reference

`pcreGenCompileOptBits`

### pcreListExecOptBits

`pcreListExecOptBits()=> t`

#### Description

Displays information about the options used with`pcreGenExecOptBits`. See the description of `pcreGenExecOptBits` for more information.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `t` | Returns`t`.
#### Reference

`pcreGenExecOptBits`

### pcreMatchAssocList

```
pcreMatchAssocList( g_pattern l_subjects [ x_compOptBits ] [ x_execOptBits ]) => l_results | nil | error message(s)
```

#### Description

Matches the keys of an association list of subjects (strings or symbols) against a regularexpression pattern (`g_pattern`) and returns an association list of those elements that match. The keys are the first elements of each key/value pair in the association list. You can use optional arguments to specify independent option bits for controlling pattern compiling and matching. The compiling and matching algorithms are PCRE/Perl-compatible.

The specified regular expression pattern overwrites the previously-compiled pattern and isused for subsequent matching until you provide a new pattern. The function reports any errors in the given pattern.

You can set and unset the[`PCRE_CASELESS`](../sklangref/stringfunc.html#PCRE_CASELESS), [`PCRE_MULTILINE`](../sklangref/stringfunc.html#PCRE_MULTILINE), [`PCRE_DOTALL`](../sklangref/stringfunc.html#PCRE_DOTALL), and [`PCRE_EXTENDED`](../sklangref/stringfunc.html#PCRE_EXTENDED) independent option bits from within the pattern. The content of the options argument specifies the initial setting at the start of compilation. You can set the `PCRE_ANCHORED` option at matching time and at compile time.

**Note:** If`pcreObject` is specified as the `g_pattern`, `pcreMatchAssocList` skips pattern compilation and ignores `x_compOptBits`.

#### Arguments

|  |
| --- | ---
| `g_pattern` | String containing regular expression string to be compiled or a`pcreObject`.
|  |
| --- | ---
| `l_subjects` | Association list whose keys are strings or symbols.
|  |
| --- | ---
| `x_compOptBits` | (Optional) Independent option bits that affect the compilation.Valid values for this argument are the same as those for the `x_options` argument to the [`pcreCompile`](../sklangref/stringfunc.html#pcreCompile) SKILL function.
|  |
| --- | ---
| `x_execOptBits` | (Optional) Independent option bits that affect pattern matching.Valid values for this argument are the same as those for the `x_options` argument to the [`pcreExecute`](../sklangref/stringfunc.html#pcreCompile) SKILL function.
#### Value Returned

|  |
| --- | ---
| `l_results` | Association list of elements from the subject association listwhose keys match the pattern.
|  |
| --- | ---
| `nil` | No keys in the subject association list match the pattern.
|  |
| --- | ---
| error message(s) | Zero or more error messages that appear if the function fails forany reason, if the subject association list is not valid, or if the pattern compilation fails (indicating the cause of the failure).
#### Example

```
pcreMatchAssocList( "^[a-z][0-9]*$" '((abc "ascii") ("123" "number") (a123 "alphanum")(a12z "ana")) )=> ((a123 "alphanum"))
```

```
pcreMatchAssocList("^[a-z][0-9]*$" '((abc "ascii") ("123" "number") ("yy\na123"  "alphanum") (a12z "ana")) pcreGenCompileOptBits(?multiLine t) pcreGenExecOptBits( ?notbol t) )=> (("yy\na123" "alphanum"))
```

```
pcreMatchAssocList( "box[0-9]*" '(square circle "cell9" "123") ) => *Error* pcreMatchAssocList: element in the list given as argument #2 is not a valid association because its car() (taken as a key) is not either a symbol or a string - square
```

#### Reference

`pcreCompile, pcreExecute, pcreGenCompileOptBits, pcreGenExecOptBits`

### pcreMatchList

```
pcreMatchList( g_pattern l_subjects [ x_compOptBits ] [ x_execOptBits ]) => l_results | nil | error message(s)
```

#### Description

Matches a list of subjects (strings or symbols) against a regular expression pattern(`g_pattern`) and returns a list of those elements that match. You can use optional arguments to specify independent option bits for controlling pattern compiling and matching. The compiling and matching algorithms are PCRE/Perl-compatible.

The specified regular expression pattern overwrites the previously-compiled pattern and isused for subsequent matching until you provide a new pattern. The function reports any errors in the given pattern.

You can set and unset the[`PCRE_CASELESS`](../sklangref/stringfunc.html#PCRE_CASELESS), [`PCRE_MULTILINE`](../sklangref/stringfunc.html#PCRE_MULTILINE), [`PCRE_DOTALL`](../sklangref/stringfunc.html#PCRE_DOTALL), and [`PCRE_EXTENDED`](../sklangref/stringfunc.html#PCRE_EXTENDED) independent option bits from within the pattern. The content of the options argument specifies the initial setting at the start of compilation. You can set the `PCRE_ANCHORED` option at matching time and at compile time.

**Note:** If`pcreObject` is specified as the `g_pattern`, `pcreMatchList` skips pattern compilation and ignores `x_compOptBits`.

#### Arguments

|  |
| --- | ---
| `g_pattern` | String containing regular expression string to be compiled or a`pcreObject`.
|  |
| --- | ---
| `l_subjects` | List of subject strings or symbols to be matched against theregular expression string. If it is a symbol, its print name is used.
|  |
| --- | ---
| `x_compOptBits` | (Optional) Independent option bits that affect the compilation.Valid values for this argument are the same as those for the `x_options` argument to the [`pcreCompile`](../sklangref/stringfunc.html#pcreCompile) SKILL function.
|  |
| --- | ---
| `x_execOptBits` | (Optional) Independent option bits that affect pattern matching.Valid values for this argument are the same as those for the `x_options` argument to the [`pcreExecute`](../sklangref/stringfunc.html#pcreCompile) SKILL function.
#### Value Returned

|  |
| --- | ---
| `l_results` | List of strings, symbols, or PCRE objects from the subject list thatmatch the pattern.
|  |
| --- | ---
| `nil` | No matches or match failure.
|  |
| --- | ---
| error message(s) | Zero or more error messages that appear if the function fails forany reason, if the subject list is not valid, or if the pattern compilation fails (indicating the cause of the failure).
#### Example

```
pcreMatchList( "^[a-z][0-9]*" '(a01 x02 "003" aa01 "abc") )=> (a01 x02 aa01 "abc")
```

`pcreMatchList( "^[a-z][0-9][0-9]*" '(a001 b002 "003" aa01 "abc") )=> (a001 b002)`

`pcreMatchList( "box[0-9]*" '(square circle "cell9" "123") )=> nil`

```
pcreMatchList("^[a-z][0-9][0-9]*" '("12\na001" b002) pcreGenCompileOptBits(?multiLine t) pcreGenExecOptBits( ?notbol t) )=> ("12\na001")
```

```
pcreMatchList("^[a-z][0-9]*" '(abc 123)) => *Error* pcreMatchList: element in the list given as argument #2 must be either a symbol or a string - 123
```

```
pcreMatchList( "^[a-z][0-9]*$" '((abc "ascii") (a123 "alphanum")) ) => *Error* pcreMatchList: element in the list given as argument #2 must be either a symbol or a string - (abc "ascii")
```

#### Reference

`pcreCompile, pcreExecute, pcreGenCompileOptBits, pcreGenExecOptBits`

### pcreMatchp

`pcreMatchp( g_pattern S_subject [ x_compOptBits ] [ x_execOptBits ] ) => t | nil`

#### Description

Checks to see whether the subject string or symbol (`S_subject`) matches the specified regular expression pattern (`g_pattern`). You can use optional arguments to specify independent option bits for controlling pattern compiling and matching. The compiling and matching algorithms are PCRE/Perl-compatible. For greater efficiency when matching a number of subjects against a single pattern, you should use [`pcreCompile`](../sklangref/stringfunc.html#pcreCompile) and [`pcreExecute`](#pcreExecute "String Functions").

The specified regular expression pattern overwrites the previously-compiled pattern and isused for subsequent matching until you provide a new pattern. The function reports any errors in the given pattern.

You can set and unset the[`PCRE_CASELESS`](../sklangref/stringfunc.html#PCRE_CASELESS), [`PCRE_MULTILINE`](../sklangref/stringfunc.html#PCRE_MULTILINE), [`PCRE_DOTALL`](../sklangref/stringfunc.html#PCRE_DOTALL), and [`PCRE_EXTENDED`](../sklangref/stringfunc.html#PCRE_EXTENDED) independent option bits from within the pattern. The content of the options argument specifies the initial setting at the start of compilation. You can set the `PCRE_ANCHORED` option at matching time and at compile time.

**Note:** If`pcreObject` is specified as the `g_pattern`, `pcreMatchp` skips pattern compilation and ignores `x_compOptBits`.

#### Arguments

|  |
| --- | ---
| `g_pattern` | String containing regular expression string to be compiled or a`pcreObject`.
|  |
| --- | ---
| `S_subject` | Subject string or symbol to be matched. If it is a symbol, its printname is used.
|  |
| --- | ---
| `x_compOptBits` | (Optional) Independent option bits that affect the compilation.Valid values for this argument are the same as those for the `x_options` argument to the [`pcreCompile`](../sklangref/stringfunc.html#pcreCompile) SKILL function.
|  |
| --- | ---
| `x_execOptBits` | (Optional) Independent option bits that affect pattern matching.Valid values for this argument are the same as those for the `x_options` argument to the [`pcreExecute`](../sklangref/stringfunc.html#pcreCompile) SKILL function.
#### Value Returned

|  |
| --- | ---
| `t` | A match is found. A message appears if you have any errors in the regular expression pattern.
|  |
| --- | ---
| `nil` | No match. An error message indicating the cause of the matching failure appears.
#### Example

`pcreMatchp( "[0-9]*[.][0-9][0-9]*" "100.001" ) => t`

`pcreMatchp( "[0-9]*[.][0-9]+" ".001" )      => t`

`pcreMatchp( "[0-9]*[.][0-9]+" "." )      => nil`

```
pcreMatchp( "[0-9" "100" ) => *Error* pcreCompile: compilation failed at offset 4: missing terminating ] for character class nil
```

`pcreMatchp( "((?i)rah)\\s+\\1" "rah rah" ) => t`

```
pcreMatchp( "^[0-9]+" "abc\n123\nefg" pcreGenCompileOptBits(?multiLine t) pcreGenExecOptBits( ?notbol t) )=> t
```

#### Reference

`pcreCompile, pcreExecute, pcreGenCompileOptBits, pcreGenExecOptBits`

### pcreObjectp

`pcreObjectp( g_arg ) => t | nil`

#### Description

Checks to see whether the given argument is a`pcreObject` or not.

#### Arguments

|  |
| --- | ---
| `g_arg` | A value to be checked.
#### Value Returned

|  |
| --- | ---
| `t` | `g_arg` is a pcreObject.
|  |
| --- | ---
| `nil` | `g_arg` is not a pcreObject.
#### Example

`a = pcreCompile("abc[0-9]+")`

`=>pcreobj@0x83b8018`

`(pcreObjectp a)`

`=>t`

`(pcreObjectp 9)`

`=>nil`

#### Reference

`pcreCompile`

### pcrePrintLastMatchErr

`pcrePrintLastMatchErr( o_patMatchObj ) => t | nil`

#### Description

Prints the error message associated with the last failed matching operation (that is, when[`pcreExecute`](#pcreExecute "String Functions") returns `nil`).

#### Argument

|  |
| --- | ---
| `o_patMatchObj` | Data object containing information from a previously failedpattern comilation/matching operation.
#### Value Returned

|  |
| --- | ---
| `t` | Prints the error message associated with the last failed matchingoperation and returns `t`.
|  |
| --- | ---
| `nil` | No previously failed matching operation.
#### Example

```
comPat = pcreCompile( "[0-9]*[.][0-9]+" ) => pcreobj@0x27d060pcreExecute( comPat "123" ) => nilpcrePrintLastMatchErr( comPat ) => The subject string did not match the compiled pattern.
```

```
pcreExecute( comPat "123" pcreGenCompileOptBits(?caseLess t) ) => nilpcrePrintLastMatchErr( comPat ) => An unrecognized bit was set in the options argument.
```

#### Reference

[pcreCompile](#pcreCompile "String Functions"), [pcreExecute](#pcreExecute "String Functions"), [pcreGenCompileOptBits](#pcreGenCompileOptBits "String Functions"), [pcreGenExecOptBits](#pcreGenExecOptBits "String Functions")

### pcreReplace

```
pcreReplace( o_comPatObj t_source t_replacement x_index [ x_options ] ) => t_result | t_source
```

#### Description

Replaces one or all occurrences of a previously-compiled regular expression in the givensource string with the specified replacement string. The integer index indicates which of the matching substrings to replace. If the index is less than or equal to zero, the function applies the replacement string to all matching substrings. You can use an optional argument to specify independent option bits for controlling pattern matching. The matching algorithm is PCRE/Perl-compatible.

#### Arguments

|  |
| --- | ---
| `o_comPatObj` | Data object containing the compiled pattern returned from aprevious [`pcreCompile`](../sklangref/stringfunc.html#pcreCompile) call.
|  |
| --- | ---
| `t_source` | Source string to be matched and replaced.
|  |
| --- | ---
| `t_replacement` | Replacement string. You can use pattern tags in this string (see [`pcreSubstitute`](#pcreSubstitute "String Functions")).
|  |
| --- | ---
| `x_index` | Integer index indicating which of the matching substrings toreplace. If the index is less than or equal to zero, the function applies the replacement string to all matching substrings.
|  |
| --- | ---
| `x_options` | (Optional) Independent option bits that affect pattern matching.Valid values for this argument are the same as those for the `x_options` argument to the [`pcreExecute`](../sklangref/stringfunc.html#pcreCompile) SKILL function.
#### Value Returned

|  |
| --- | ---
| `t_result` | Copy of the source string with the specified replacement(determined by the integer index).
|  |
| --- | ---
| `t_source` | Original source string if no match was found.
#### Example

```
comPat1 = pcreCompile( "[0-9]+" ) => pcreobj@0x27d258 pcreReplace( comPat1 "abc-123-xyz-890-wuv" "(*)" 0 )=> "abc-(*)-xyz-(*)-wuv"pcreReplace( comPat1 "abc-123-xyz-890-wuv" "(*)" 1 )=> "abc-(*)-xyz-890-wuv"pcreReplace( comPat1 "abc-123-xyz-890-wuv" "(*)" 2 )=> "abc-123-xyz-(*)-wuv"pcreReplace( comPat1 "abc-123-xyz-890-wuv" "(*)" 3 )=> "abc-123-xyz-890-wuv"
```

```
comPat2 = pcreCompile( "xyz" ) => pcreobj@0x27d264 pcreReplace( comPat2 "xyzzyxyzz" "xy" 0 ) => "xyzyxyz"
```

#### Reference

`pcreCompile`

### pcreSubstitute

`pcreSubstitute( [o_pcreObject]t_string ) => t_result | nil`

#### Description

If`o_pcreObject` is not provided, `pcreSubstitute` copies the input string and substitutes all pattern tags in it using the corresponding matched strings from the last `pcreExecute`/`pcreMatch*` operation.

If`o_pcreObject` is provided, `pcreSubstitute` copies the input string and substitutes all pattern tags in it using the corresponding matched strings from the last `pcreExecute` operation that used the given `o_pcreObject`.

Pattern tags are of the form`\n`, where `n` is `0`-`9`. `\0` (or `&`) refers to the string that matched the entire regular expression; `\k` refers to the string that matched the pattern wrapped by the `k`th backslash (`...\`) in the regular expression.

If`o_pcreObject` is provided, pattern tag can also have the next form `\{x_num}`, where `x_num` is a positive integer. This refers to the string that matches the pattern by the `x_num(``th``)` backslash (`...\`) in the regular expression which has been compiled to `o_pcreObject`. The matched string will be taken from the last string which was matched by `pcreExecute` using `o_pcreObject`.

#### Argument

|  |
| --- | ---
| `o_pcreObject` | An object that was used in`pcreExecute`.
|  |
| --- | ---
| `t_string` | Argument string to which the function applies the substitution.
#### Value Returned

|  |
| --- | ---
| `t_result` | Copy of the argument with the specified substitutions.
|  |
| --- | ---
| `nil` | The last string matching operation failed (none of the patterntags are meaningful).
#### Example

```
comPat = pcreCompile( "([a-z]+)\\.\\1" ) => pcreobj@0x27d048pcreExecute( comPat "abc.bc" ) => tpcreSubstitute( "*\\0*" ) => "*bc.bc*"pcreSubstitute( "The matched string is: \\1" )=> "The matched string is: bc"
```

`r = pcreCompile("x[0-9]")`

`=>pcreobj@0x81ca018`

`pcreExecute(r "x1")`

`=>t`

`str1 = "\\0fff\\1ffff\\2fffff"`

`"\\0fff\\1ffff\\2fffff"`

`pcreSubstitute(str1)`

`=>"x1ffffffffffff"`

`pcre = pcreCompile("(a)(b+)([as]+)(q)(w)(r*)(t)(u)(i)(h)(k)(b).*")`

`=>pcreobj@0x83bb018`

`pcre1 = pcreCompile("0x([0-9]+)")`

`=>pcreobj@0x83bb034`

`pcreExecute(pcre "abbbasasssqwtuihkbdddd")`

`=>t`

`pcreExecute(pcre1 "0x333")`

`=>t`

`(for i 0 12`

`str = (if i < 10 (sprintf nil "\\%d" i) (sprintf nil "\\{%d}" i))`

`(printf "pcreSubstitute(pcre '%s') == '%L'\n" str pcreSubstitute(pcre str))`

`)`

`pcreSubstitute(pcre '\0') == '"abbbasasssqwtuihkbdddd"'`

`pcreSubstitute(pcre '\1') == '"a"'`

`pcreSubstitute(pcre '\2') == '"bbb"'`

`pcreSubstitute(pcre '\3') == '"asasss"'`

`pcreSubstitute(pcre '\4') == '"q"'`

`pcreSubstitute(pcre '\5') == '"w"'`

`pcreSubstitute(pcre '\6') == '""'`

`pcreSubstitute(pcre '\7') == '"t"'`

`pcreSubstitute(pcre '\8') == '"u"'`

`pcreSubstitute(pcre '\9') == '"i"'`

`pcreSubstitute(pcre '\{10}') == '"h"'`

`pcreSubstitute(pcre '\{11}') == '"k"'`

`pcreSubstitute(pcre '\{12}') == '"b"'`

`t`

`pcreSubstitute("the last pcreExecute was called - &")`

`=>"the last pcreExecute was called - 0x333"`

#### Reference

[pcreCompile](#pcreCompile "String Functions"), [pcreExecute](#pcreExecute "String Functions")

### readstring

`readstring( t_string ) => g_result | nil`

#### Description

Returns the first expression in a string. Subsequent expressions in the string are ignored. Theexpression is not processed in any way.

#### Arguments

|  |
| --- | ---
| `t_string` | String to read.
#### Value Returned

|  |
| --- | ---
| `g_result` | The object read in.
|  |
| --- | ---
| `nil` | When the port is at the end of the string.
#### Example

`readstring("fun( 1 2 3 ) fun( 4 5 )") => ( fun 1 2 3 )`

The first example shows normal operation.

`readstring("fun(" )`

`fun(`

`^`

```
SYNTAX ERROR found at line 1 column 4 of file *string**Error* lineread/read: syntax error encountered in input*WARNING* (include/load): expression was improperly terminated.
```

The second example shows the error message if the string contains a syntax error.

```
EXPRESSION = 'list( 1 2 ) => list(1 2)EXPRESSION == readstring( sprintf( nil "%L" EXPRESSION ))=> t
```

The third example illustrates that`readstring` applied to the print representation of an expression, returns the expression.

#### Reference

[linereadstring](inputoutput.html#1039880 "Input Output Functions")

### rexCompile

`rexCompile( t_pattern ) => t | nil`

#### Description

Compiles a regular expression string pattern into an internal representation to be used by succeeding calls to `rexExecute`.

This allows you to compile the pattern expression once using `rexCompile` and then match a number of targets using `rexExecute`; this gives better performance than using `rexMatchp` each time.

**Note:** `rexCompile` does not support the extended regular expression syntax. To parse such regular expressions, you can use the `pcre` (Perl Compatible Regular Expressions) functions (such as `pcreCompile`) instead.

#### Arguments

|  |
| --- | ---
| `t_pattern` | Regular expression string pattern.
#### Value Returned

|  |
| --- | ---
| `t` | The given argument is a legal regular expression string.
|  |
| --- | ---
| `nil` | Signals an error if the given pattern is ill-formed or not a legalexpression.
#### Example

```
rexCompile("^[a-zA-Z]+")                => trexCompile("\\([a-z]+\\)\\.\\1")        => trexCompile("^\\([a-z]*\\)\\1$")         => trexCompile("[ab") => *Error* rexCompile: Missing ] - "[ab"
```

#### Reference

[rexExecute](#1040261 "String Functions"), [rexMatchp](#1040383 "String Functions"), [rexSubstitute](#1040442 "String Functions"), [pcreCompile](#pcreCompile "String Functions")

#### Pattern Matching of Regular Expressions

In many applications, you need to match strings or symbols against a pattern. SKILL providesa number of pattern matching functions that are built on a few primitive C library routines with a corresponding SKILL interface.

A*pattern* used in the pattern matching functions is a string indicating a regular expression. Here is a brief summary of the rules for constructing regular expressions in SKILL:

**Rules for Constructing Regular Expressions**

| **Synopsis** | **Meaning**
| c | Any ordinary character (not a specialcharacter listed below) matches itself.
| . | A dot matches any character.
| \ | A backslash when followed by a special character matches that characterliterally. When followed by one of <, >, (, ), and 1,...,9, it has a special meaning as described below.
| [c...] | A nonempty string of characters enclosed in square brackets (called a set)matches one of the characters in the set. If the first character in the set is ^, it matches a character not in the set. A shorthand S-E is used to specify a set of characters S up to E, inclusive. The special characters ] and - have no special meaning if they appear as the first character in a set.
| \* | A regular expression of any of the forms above, followed by the closurecharacter \* matches zero or more occurrences of that form.
| + | Similar to \*, except it matches*one* or more times.
| \(...\) | A regular expression wrapped as \( form \) matches whatever*form* matches, but saves the string matched in a numbered register (starting from one, can be up to nine) for later reference.
| \n | A backslash followed by a digit *n* matches the contents of the *n*th register from the current regular expression.
| \<...\> | A regular expression starting with a \< and/or ending with a \> restricts thepattern matching to the beginning and/or the end of a word. A word defined to be a character string can consist of letters, digits, and underscores.
| rs | A composite regular expressionrs matches the longest match of r followed by a match for s.
| ^, $ | A ^ at the beginning of a regular expression matches the beginning of astring. A $ at the end matches the end of a string. Used elsewhere in the pattern, ^ and $ are treated as ordinary characters.
#### How Pattern Matching Works

The mechanism for pattern matching

* Compiles a pattern into a form and saves the form internally.

* Uses that internal form in every subsequent matching against the targets until the nextpattern is supplied.

The`rexCompile` function does the first part of the task, that is, the compilation of a pattern. The `rexExecute` function takes care of the second part, that is, actually matching a target against the previously compiled pattern. Sometimes this two-step interface is too low-level and awkward to use, so functions for higher-level abstraction (such as `rexMatchp`) are also provided in SKILL.

#### Avoiding Null and Backslash Problems

* A null string ("") is interpreted as no pattern being supplied, which means the previouslycompiled pattern is still used. If there was no previous pattern, an error is signaled.

* To put a backslash character (\) into a pattern string, you need an extra backslash (\) toescape the backslash character itself.

For example, to match a file name with dotted extension .`il`, the pattern "^[a-zA-Z]+\\.il$" can be used, but "^[a-zA-Z]\.il$" gives a syntax error. However, if the pattern string is read in from an input function such as *gets* that does not interpret backslash characters specifically, you should *not* add an extra backslash to enter a backslash character.

### rexExecute

`rexExecute( S_target ) => t | nil`

#### Description

Matches a string or symbol against the previously compiled pattern set up by the last`rexCompile` call.

This function is used in conjunction with`rexCompile` for matching multiple targets against a single pattern.

**Note:** Calls to`rexMatchp` reset the pattern set up by `rexCompile`. If any calls to `rexMatchP` have been made, `rexExecute` will not match the pattern set by `rexCompile`.

#### Arguments

|  |
| --- | ---
| `S_target` | String or symbol to be matched. If a symbol is given, its printname is used.
#### Value Returned

|  |
| --- | ---
| `t` | A match is found.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

```
rexCompile("^[a-zA-Z][a-zA-Z0-9]*")    => trexExecute('Cell123)                   => trexExecute("123 cells")                => nil
```

Target does not begin with a-z/A-Z

```
rexCompile("\\([a-z]+\\)\\.\\1")        => trexExecute("abc.bc")                    => trexExecute("abc.ab")                    => nil
```

#### Reference

`rexCompile, rexMatchp, rexSubstitute, pcreCompile`

### rexMagic

`rexMagic( [ g_state ] ) => t | nil`

#### Description

Turns on or off the special interpretation associated with the meta-characters in regularexpressions.

By default the meta-characters (^, $, \*, +, \, [, ], etc.) in a regular expression are interpreted specially. However, this "magic" can be explicitly turned off and on programmatically by this function. If no argument is given, the current setting is returned. Users of `vi` will recognize this as equivalent to the `set magic/set nomagic` commands.

#### Arguments

|  |
| --- | ---
| `g_state` | `nil` turns off the magic of the meta-characters. Anything else turns on the magic interpretation.
#### Value Returned

|  |
| --- | ---
| `t` | The current setting.
|  |
| --- | ---
| `nil` | The given argument.
#### Example

```
rexCompile( "^[0-9]+" )           => trexExecute( "123abc" )            => trexSubstitute( "got: \\0")        => "got: 123"rexMagic( nil )                   => nilrexCompile( "^[0-9]+" )            => t      recompile w/o magicrexExecute( "123abc" )            => nilrexExecute( "**^[0-9]+!**")       => trexSubstitute( "got: \\0")        => "got: \\0"rexMagic( t )=> trexSubstitute( "got: \\0")        => "got: ^[0-9]+"
```

#### Reference

`rexCompile, rexSubstitute, rexReplace`

### rexMatchAssocList

`rexMatchAssocList( t_pattern l_targets ) => l_results | nil`

#### Description

Returns a new association list created out of those elements of the given association listwhose key matches a regular expression pattern. The supplied regular expression pattern overwrites the previously compiled pattern and is used for subsequent matching until the next new pattern is provided.

`l_targets` is an *association list*, that is, each element on `l_targets` is a list with its `car` taken as a *key* (either a string or a symbol). This function matches the keys against `t_pattern`, selects the elements on `l_targets` whose keys match the pattern, and returns a new association list out of those elements.

#### Arguments

|  |
| --- | ---
| `t_pattern` | Regular expression pattern.
|  |
| --- | ---
| `l_targets` | Association list whose keys are strings and/or symbols.
#### Value Returned

|  |
| --- | ---
| `l_results` | New association list of elements that are in`l_targets` and whose keys match `t_pattern`.
|  |
| --- | ---
| `nil` | If no match is found. Signals an error if the given pattern is ill-formed.
#### Example

```
rexMatchAssocList("^[a-z][0-9]*$"    '((abc "ascii") ("123" "number") (a123 "alphanum")    (a12z "ana")))=> ((a123 "alphanum"))
```

#### Reference

`rexCompile, rexExecute, rexMatchp, rexMatchList`

### rexMatchList

`rexMatchList( t_pattern l_targets ) => l_results | nil`

#### Description

Creates a new list of those strings or symbols in the given list that matcha regular expression pattern. The supplied regular expression pattern overwrites the previously compiled pattern and is used for subsequent matching until the next new pattern is provided.

#### Arguments

|  |
| --- | ---
| `t_pattern` | Regular expression pattern.
|  |
| --- | ---
| `l_targets` | List of strings and/or symbols to be matched against the pattern.
#### Value Returned

|  |
| --- | ---
| `l_results` | List of strings (or symbols) that are on`l_targets` and found to match `t_pattern`.
|  |
| --- | ---
| `nil` | If no match is found. Signals an error if the given pattern is ill-formed.
#### Example

`rexMatchList("^[a-z][0-9]*" '(a01 x02 "003" aa01 "abc"))=> (a01 x02 aa01 "abc")`

```
rexMatchList("^[a-z][0-9][0-9]*"     '(a001 b002 "003" aa01 "abc"))=> (a001 b002)
```

`rexMatchList("box[0-9]*" '(square circle "cell9" "123"))=> nil`

#### Reference

`rexCompile, rexExecute, rexMatchAssocList, rexMatchp`

### rexMatchp

`rexMatchp( t_pattern S_target ) => t | nil`

#### Description

Checks to see if a string or symbol matches a given regular expression pattern. The supplied regular expression pattern overwrites the previously compiled pattern and is used for subsequent matching until the next new pattern is provided.

This function matches`S_target` against the regular expression `t_pattern` and returns `t` if a match is found, `nil` otherwise. An error is signaled if the given pattern is ill-formed. For greater efficiency when matching a number of targets against a single pattern, use the `rexCompile` and `rexExecute` functions.

#### Arguments

|  |
| --- | ---
| `t_pattern` | Regular expression pattern.
|  |
| --- | ---
| `S_target` | String or symbol to be matched against the pattern.
#### Value Returned

|  |
| --- | ---
| `t` | A match is found. Signals an error if the given pattern is ill-formed.
#### Example

```
rexMatchp("[0-9]*[.][0-9][0-9]*" "100.001")    => trexMatchp("[0-9]*[.][0-9]+" ".001")            => trexMatchp("[0-9]*[.][0-9]+" ".")               => nilrexMatchp("[0-9]*[.][0-9][0-9]*" "10."          => nil
```

`rexMatchp("[0-9" "100")*Error* rexMatchp: Missing ] - "[0-9"`

#### Reference

`rexCompile, rexExecute`

### rexReplace

