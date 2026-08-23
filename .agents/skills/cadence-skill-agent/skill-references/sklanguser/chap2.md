### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

2
=

Language Characteristics
========================

This chapter explains the basic structure and syntax of the Cadence® SKILL language. The best way to learn SKILL, of course, is by using it to accomplish a real task. Before you begin using SKILL, you should study this chapter.

Programming experience is helpful for those who want to program extensively in SKILL.References to the C programming language in this text make it easier for C programmers to learn SKILL. This text does not require you to be an experienced programmer.

Experienced C programmers must remember that SKILL is not C even though the syntaxappears familiar.

For more information, see the following topics:

* [Naming Conventions](#1009937 "Language Characteristics")

* [Function Calls](#1008239 "Language Characteristics")

* [SKILL Syntax](#1008253 "Language Characteristics")

* [Data Characteristics](#1008463 "Language Characteristics")

Naming Conventions
------------------

This section describes Cadence naming conventions for functions, variables, and theirarguments.

* ***To avoid conflict with Cadence-supplied functions and variables,customers should begin their function and variable names with uppercase letters.***

### Names of Functions

If you look in SKILL API reference manuals, you will notice that functions for tools are usuallygrouped with identifiable, unique prefixes. These prefixes vary across Cadence tools, but all use lowercase letters.

The recommended naming scheme is to

* Use casing to separate code that is developed within Cadence from that developedoutside.

* Use a group prefix to separate code developed within Cadence.

Cadence internal developers should name functions with

* An optional underscore (\_) prefix to indicate private functions. Cadence customersshould not use private functions. See [Cadence-Private Functions](#1010003 "Language Characteristics").

* A prefix that has two to five lowercase characters that signify the code package.

* The lowercase character in the prefix can be one of the following:

|  |  |
| --- | --- | ---
| **Name Type** | **Character** | **Meaning**
| Bit Field Constant | b | Bit-field constant
| Constants | c | Enumerated constant
| Errors | e | Name of a structure describing anerror
| Internal Functions | i | An internal function, these functionsshould not be called directly by application programs
| Functions | f | Occasionally used as a functionindicator.
| Macros | m | Rarely used macro indicator.
| Global Variables | v | Public global variable
* The root name itself starting with an uppercase character.

### Cadence-Private Functions

* ***Functions beginning with an underscore are considered Cadence-private, internal functions and are not supported.***

Cadence-private functions are undocumented, unsupported functions that are used internallyby Cadence engineering. These Cadence-private functions are subject to change at any time, without notice, because they are not intended for public use.

### Names of Variables

* ***Cadence customers can avoid naming conflicts with Cadence-suppliedvariables by beginning the first letter of their variable names with uppercase letters.***

You should not set the following Cadence internal variables without a full understanding ofpotential consequences.

|  |
| --- | ---
| **Variable** | **Meaning**
| `stdin` | Standard input port.
| `stdout` | Standard output port.
| `piport` | Standard input port from which user input is read.
| `poport` | Standard output port, which is the default for print statements.
| `ptport` | Standard output port for tracing results.
| `errport` | Standard output port for error messages.
| `printlength` | Controls the number of elements in a list that are printed.
| `printlevel` | Controls the depth of elements in a list which are printed.
| `tracelength` | Controls the number of elements in a list that are printed.
| `tracelevel` | Controls the depth of elements in a list that are printed duringtracing.
| `pprintresult` | Controls the pretty printing of the results of values returned bythe top level.
| `editor` | Controls the default text editor.
| `gcdisable` | Toggles enabling of garbage collection. Use cautiously. Internalvariable used in memory management for debugging purposes only.
| `_gcprint` | Toggles the printing of garbage collection messages. Internalvariable used in memory management for debugging purposes only.
| echoInput | Controls the echoing of expressions or all contents of files beingloaded (via `load`()/`loadi`()), for example `sstatus`(`echoInput` `t`)
| roport | Controls printing messages to CIW.
You might see internal variable names when you are using the debugging tools, especially ifyou are dumping the stack.

Function Calls
--------------

SKILL is a functional programming language, which means that computation is bothexpressed and performed as a series of function calls.

* Every operator in SKILL corresponds to a predefined function. The operator "`+`," for example, corresponds to the function `plus`.

* You can add two numbers together either by calling the function, for example,`plus(x``y)`, or by using the `infix` expression `x+y`.

In SKILL, even control statements are implemented by calls to special functions; the special functions then evaluate their arguments in a specific order.

Function calls can be written in either of the following notations.

* Algebraic notation used by most programming languages, that is,`func`(`arg1``arg2` … ).

* Prefix notation used by the Lisp programming language, that is; (`func``arg1``arg2`…).

Remember that there must be no white space between the function name and the leftparenthesis in the algebraic notation.

The functional programming concepts implemented in SKILL are reflected in the basic syntaxof the language. SKILL programs are written as sequences of nested function calls. To utilize SKILL fully, you must first have a good grasp of the underlying concepts of functional programming.

SKILL Syntax
------------

This section describes SKILL syntax, which includes the use of special characters,comments, spaces, parentheses, and other notation.

### Special Characters

Certain characters are special in SKILL. These include the`infix` operators such as less than (<), colon (:), and assignment (=). The table below lists these special characters and their meaning in SKILL.

**Note:** All non-alphanumeric characters (other than `\_' and `?') must be preceded ("escaped")by a backslash (`\') when you use them in the name of a symbol.

****Special Characters in SKILL****

| **Character** | **Name** | **Meaning**
| \ | backslash | Escape for special characters
| ( ) | parentheses | Grouping of list elements, function calls
| [ ] | brackets | Array index, super right bracket
| { } | braces | Grouping of expressions using`progn`
| ' | single quote | Quoting the expression to prevent its evaluation
| " | double quote | String delimiter
| , | comma | Optional delimiter between list elements; also used withinthe scope of a backquoted expression to force the evaluation of the expression
| ; | semicolon | Line-style comment character
| : | colon | Bit field delimiter, range operator
| . | period | getq operator
| +, -, \*, / | arithmetic | For arithmetic operators; the /\* and \*/ combinations are alsoused as comment delimiters
| !,^,&,| | logical | For logical operators
| <,>,= | relational | For relational and assignment operators; < and > are also used in the specification of bit fields
| # | pound sign | Signals special parsing if it appears in the first column
| @ | "at" sign | If first character, implies reserved word; also used withcomma to force evaluation and list splicing in the context of a backquoted expression
| ? | question mark | If first character, implies keyword parameter
| ` | backquote | Quoting the expression prevents its evaluation, with supportfor the comma (,) and comma-at (,@) operators to allow evaluation within backquoted forms
| % | percent sign | Used as a scaling character for numbers
| $ | - | Reserved for future use
### Comments

SKILL permits two different styles of comments. One style is block-oriented, where commentsare delimited by /\* and \*/. For example:

`/* This is a block of (C style) commentscomment line 2comment line 3 etc.*/`

The other style is line-oriented where the semicolon (;) indicates that the rest of the input lineis a comment. For example:

`a=3 ;Assign valueb=2 ;In the next line, add two numbersa+b`

`=>325`

There may be times, when you want to break a long comment line for aesthetic reasons. Inthat case, you can use a backslash (\). A backslash allows the comment to continue on to the next line without the need to repeat the comment character (;) at the start of that following line. For example:

`a=3 ;Assign valueb=2 ;In the next \line add two numbersa+b`

`=>325`

> **Note:** If the backslash in the comment line is followed by a command, the command willbe considered as part of the comment and will not be executed. For example:

> `a=3 ;Assign valueb=2 ;In the next line add two numbers\a+b=>32`

> In this example, the sum of the two numbers,`a` and `b`, is not displayed.

> In such a case, place ` ` immediately after the backslash to avoid disprupting the flow ofcode. This is shown in the example below.

> `a=3b=2 ;To add two numbers\' 'a+b`

> `=>325`

For simplicity, line-oriented comments are recommended. Block-oriented comments cannotbe nested because the first \*/ encountered terminates the whole comment.

### White Space

White space sometimes takes on semantic significance and a few syntactic restrictions musttherefore be observed. See [Solving Some Common Problems](chap1.html#1008398 "Getting Started").

Write function calls so the name of a function is immediately followed by a left parenthesis;no white space is allowed between the function name and the parenthesis. For example:

`f(a b c)` and `g()` are legal function calls, but
`f (a b c)` and `g ()`are illegal.

The unary minus operator must immediately precede the expression it applies to. No whitespace is allowed between the operator and its operand. For example:

`-1`, `-a`, and `-(a*b)` are legal constructs, but
`- 1`,`- a`, and `- (a*b)` are illegal.

The binary minus (subtract) operator should either be surrounded by white space on bothsides or there should be no white space on either side. To avoid ambiguity, one or the other method should be used consistently. For example:

`a - b` and `a-b` are legal constructs for binary minus, but `a -b` is illegal.

### White Space Characters

The white space characters in SKILL are generally the same as the C standard white spacecharacters: \t \f \r \n \v. Respectively, they are space, tab, form feed, carriage return, new line, and vertical tab.

The default break characters used by the SKILL language function parseString(), when theoptional second argument is not specified, are the white space characters: /t /f /r /n /v.

### Parentheses

There is a subtle point about SKILL syntax that C programmers, in particular, must be verycareful to note.

#### Parentheses in C

In C, the relational expression given to a conditional statement such as`if, while`, and `switch` must be enclosed by an outer set of parentheses for purely syntactical reasons, even if that expression consists of only a single Boolean variable. In C, an `if` statement might look like:

`if (done) i=0; else i=1;`

#### Parentheses in SKILL

In SKILL, however, parentheses are used for calling functions, delimiting multipleexpressions, and controlling the order of evaluation. You can write function calls in prefix notation

`(fn2 arg1 arg2) or (fn0)`

as well as in the more conventional algebraic form:

`fn2(arg1 arg2) or fn0()`

The use of syntactically redundant parentheses causes variables, constants, or expressionsto be interpreted as the names of functions that need to be further evaluated. Therefore,

* Never enclose a constant or a variable in parentheses by itself. For example, (1), (x).

* For arithmetic expressions involving`infix` operators, you can use as many parentheses as necessary to force a particular order of evaluation, but never put a pair of parentheses immediately outside another pair of parentheses, for example, `((a +``b))`; the expression delimited by the inner pair of parentheses would be interpreted as the name of a function.

For example, because`if` evaluates its first argument as a logical expression, a variable containing the logical condition to be tested should be written without any surrounding parentheses; the variable by itself is the logical expression. This is written in SKILL as:

`if( done then i = 0 else i = 1)`

### Super Right Bracket

When you are entering deeply nested expressions, it often becomes tedious to match upeach left parenthesis with a right parenthesis at the end of the expression. The right bracket ] can be used as a super right parenthesis to close off all open parentheses that are still pending. It is a convenient shorthand notation for interactive input, but it is not recommended for use in programs. For example:

`f1( f2( f3( f4( x ) ) ) )`

can also be written as

`f1( f2( f3( f4( x ]`

### Backquote, Comma, and Comma-At

SKILL supports a special notation for list construction from templates. This notation allowsselective evaluation within a quoted form. This selective evaluation eliminates long sequences of calls to `list` and `append`.

In absence of commas and the comma-at (,@) construction, backquote functions in exactlythe same way as single quote. However, if a comma appears inside a backquoted form, the expression that immediately follows the comma is evaluated, and the result of evaluation replaces the original form.

Commas are still acceptable as argument list separators in all contexts except within thescope of a backquote. This means that the backquote comma syntax does not have any implications for SKILL code created before the `backquote` `comma` facility was implemented. For example:

```
y = 1'(x y z)                      => (x y z)'(x ,y z)                      => (x 1 z)
```

The comma-at construction causes evaluation just as the comma does, but the results ofevaluation must be a list, and the elements of the list, rather than the list itself, replace the original form. For example:

```
x = 1y = '(a b c)'(,x ,y z)                 => (1 (a b c) z)'(,x ,@y z)                 => (1 a b c z)
```

Here's an example of a simple macro implemented with backquote:

`defmacro(myWhen (@rest body)******'if( ,car( body) progn( ,@cdr(body))))`

The expression

`a = 2b = 7myWhen( eq( a b ) printf( "The same\n" ) list( a b ))`

expands to

`if( eq( a b ) progn( printf( "The same\n" ) list( a b )))`

### Line Continuation

SKILL places no restrictions on how many characters can be placed on an input line, eventhough SKILL does impose an 8191 character limit on the strings being input. The parser reads as many lines as needed from the input until it has read in a complete form (that is, expression). If there are parentheses that have not yet been closed or binary `infix` operators whose right sides have not yet been given, the parser treats carriage returns (that is, newlines) just like spaces.

Because SKILL reads its input on a form-by-form basis, it is rarely necessary to "continue" aninput line. There might be times, however, when you want to break up a long line for aesthetic reasons. In that case, you can tell the parser to ignore a carriage return in the input line simply by preceding it immediately with a backslash (\) character.

`string = "This is \a test."=> "This is a test."`

SKILL always considers a backslash at the end of a line as a continuation regardless ofwhether the line is a command line, a command string, or a comment.

### Length of Input Lists

The SKILL parser imposes a limit of 6000 on the number of elements that can be in a listbeing read in. Internally and on output, there is no limit to how many elements a list can contain.

Data Characteristics
--------------------

This section describes the following basic data characteristics:

* Data Types

* Numbers

* Strings

* Atoms

* Escape Sequences

* Symbols

* Characters

These other SKILL data characteristics are discussed in the chapters indicated:

* Lists - see["Advanced List Operations"](chap8.html#1008199 "Advanced List Operations")

* Property Lists, Defstructs, and Arrays - see["Data Structures"](chap4.html#1008199 "Data Structures")

* Type Predicates - see["Arithmetic and Logical Expressions"](chap5.html#1016567 "Arithmetic and Logical Expressions")

### Data Types

SKILL supports several data types, including integer and floating-point numbers, characterstrings, arrays, and a highly flexible linked list structure for representing aggregates of data.

For symbolic computation, SKILL has data types for dealing with symbols and functions.

For input/output, SKILL has a data type for representing I/O ports. The table below lists all thedata types supported by SKILL with their internal names and single-character mnemonic abbreviations.

**Data Types Supported by SKILL**

| **Data Type** | **Internal Name** | **Single CharacterMnemonic**
| array | array | a
| Cadence database object | dbobject | d
| floating-point number | flonum | f
| any data type | general | g
| linked list | list | l
| integer or floating point number |  | n
| user-defined type |  | o
| I/O port | port | p
| defstruct |  | r
| relative object design (ROD) object | rodObj | R
| symbol | symbol | s
| symbol or character string |  | S
| character string (text) | string | t
| function object |  | u
| window type |  | w
| integer number | fixnum | x
| binary function | binary | y
**Note:** In a SKILL function, the last type template character is propagated to any remainingarguments. Therefore, for the case where few template characters are supplied, or if an @rest argument is given, the last type template character is used for the remainder of the arguments except for the @aux arguments.

### Numbers

SKILL supports the following numeric data types:

* Integers

* Floating-point

* Scaling factors

#### Integers

Unless they are preceded by one of the prefixes listed in the table below, integers areinterpreted as decimal numbers. Binary numbers are prefixed with "0b," octal numbers with a leading "0," and hexadecimal numbers with "0x." Integers (`fixnum`'s) in SKILL are stored internally as 32-bit wide numbers.

**Prefixes for Binary/Octal/Hexadecimal Integers**

| **Radix** | **Prefix** | **Examples [value in decimal]**
| binary | 0b or 0B | 0b0011 [ 3 ] 0b0010 [ 2 ]
| octal | 0 | 077 [ 63 ] 011 [ 9 ]
| hexadecimal | 0x or 0X | 0x3f[ 63 ]  0xff [ 255 ]
**Note:** If very large numeric values are used (that is, greater than 2147483647 or less than -2147483647), integer overflow might occur. The parser would then return the `INT_MAX` value and display a warning message.

#### Floating-Point Numbers

You use the same syntax for floating-point numbers in SKILL as you do in most programminglanguages. You can have an integer followed by a decimal point, a fraction, and an optionally signed exponent preceded by "e" or "E". Either the integer or the fraction must be present to avoid ambiguity. The following examples illustrate correct syntax:

`10.0, 10., 0.5, .5, 1e10, 1e-10, 1.1e10`

#### Scaling Factors

SKILL provides a set of scaling factors that can be added on at the end of a decimal number(integer or floating point) to achieve the desired scaling.

* Scaling factors must appear immediately after the numbers they affect; spaces are notallowed between a number and its scaling factor.

* Only the first nonnumeric character that appears after a number is significant; othercharacters following the scaling factor are ignored.

* If the number being scaled is an integer, SKILL tries to keep it an integer; the scalingfactor must be representable as an integer (that is, the scaling factor is an integral multiplier and the result does not exceed the maximum value that can be represented as an integer). Otherwise a floating-point number is returned. The scaling factors are listed in the following table.

**Scaling Factors**

| **Character** | **Name** | **Multiplier** | **Examples** |
| Y | Yotta | 1024 | 10Y [ 10e+25 ] |
| Z | Zetta | 1021 | 10Z [ 10e+22 ] |
| E | Exa | 1018 | 10E [ 10e+19 ] |
| P | Peta | 1015 | 10P [ 10e+16 ] |
| T | Tera | 1012 | 10T [ 10e+13 ] |
| G | Giga | 109 | 10G [ 10,000,000,000 ] |
| M | Mega | 106 | 10M [ 10,000,000 ] |
| k or K | kilo | 103 | 10k [ 10,000 ] |
| % | percent | 10-2 | 5% [ 0.05 ] |
| m | milli | 10-3 | 5m [ 5.0e-3 ] |
| u | micro | 10-6 | 1.2u [ 1.2e-6 ] |
| n | nano | 10-9 | 1.2n [ 1.2e-9 ] |
| p | pico | 10-12 | 1.2p [ 1.2e-12 ] |
| f | femto | 10-15 | 1.2f [ 1.2e-15 ] |
| a | atto | 10-18 | 1.2a [ 1.2e-18 ] |
| z | zepto | 10-21 | 1.2z [ 1.2e-21 ] |
| y | yocto | 10-24 | 1.2y [ 1.2e-24 ] |
### Strings

Strings are sequences of characters, for example, "abc" or "123." A string is marked off bydouble quotes, just as in the C language; the empty string is represented as " ''. The SKILL parser limits the length of input strings to a maximum of 8191 characters. There is, however, no limit to the length of strings created during program execution. Strings of >8191 characters can be created by applications and used in SKILL if they are not given as arguments to SKILL string manipulation functions.

You specify

* Printable characters (except a double quote) as part of a string without preceding themwith the backslash (\) escape character

* Unprintable characters and the double quote itself by preceding them with the backslash(\) escape character as in the C language

### Atoms

An`atom` is any data object that is not an aggregate of other data objects. In other words, atom is a generic term covering data objects of all scalar data types. Built into SKILL are several special atoms that are fundamental to the language.

|  |
| --- | ---
| nil | The`nil` atom represents both a false logical condition and an empty list.
|  |
| --- | ---
| t | The symbol`t` represents a true logical condition.
Both`nil` and `t` always evaluate to themselves and must never be used as the name of a variable.

|  |
| --- | ---
| unbound | To make sure you do not use the value of an uninitializedvariable, SKILL sets the value of all symbols and array elements initially to `unbound` so that such an error can be detected.
### Escape Sequences

The table below lists all the escape sequences supported by SKILL. Any unprintablecharacter can be represented by listing its ASCII code in two or three octal digits after the backslash. For example, BELL can be represented as \007 and Control-c can be represented as \003.

**Escape Sequences**

| **Character** | **Escape Sequence**
| new-line (line feed) | \n
| horizontal tab | \t
| vertical tab | \v
| backspace | \b
| carriage return | \r
| form feed | \f
| backslash | \\
| double quote | \"
| ASCII code ddd (octal) | \ddd
### Symbols

Symbols in SKILL correspond to variables in C. In SKILL, we often use the terms "symbol"and "variable" interchangeablyeven though symbols in SKILL are used for other things as well. Each symbol has the following components:

* Print name, which is limited to 255 characters

* Value, which is`unbound` if a value has not been assigned

* Function binding

* Property list ([The Property List of a Symbol](chap4.html#1008279 "Data Structures").)

Symbol names can contain alphanumeric characters (a-z, A-Z, 0-9), the underscore (\_)character, and the question mark (?). If the first character of a symbol is a digit, it must be preceded by the backslash character. Other printable characters can be used in symbol names by preceding each special character with a backslash (\). The following examples

`Var0Var_Name\*name\+`

are all legal names for symbols. The internal name for the last symbol is \*name+.

You can assign values to variables using the equals sign (=) assignment operator. You do notneed to declare a variable before assigning a value to it, but you cannot use an unassigned variable, that is, an `unbound` variable. Variables are untyped, which means that the same variable name can store any data type.

It is not advisable to give symbols both a value and a function binding, such as

```
myTest = 3                       ;assigns the value of 3 to myTest.procedure( myTest( x y ) x+y )   ;declares the function myTest.
```

### Characters

SKILL represents characters by symbols instead of using a separate data type. For example,the function `getc` returns the symbol representing a character. To verify this, read the characters one by one in the string "abc".

```
myPort = instring( "abc" )=> port:"*string*"char = getc( myPort ) => a ;;; the first character type( char ) => symbol       ;;; is represented by the symbol a.getc( myPort ) => b          ;;; the next charactergetc( myPort ) => c          ;;; the next charactergetc( myPort ) => nil        ;;; end of stringclose( myPort )
```

* Use the`%c` format with the `printf` function to print a single character. For example:

> `char = 'Aprintf("Character = %c\n" char ) => t`

> This function prints the following:

> `Character = A`

* Use extreme care when referring to symbols that represent certain characters. Certaincharacters must be escaped if they are the initial character in a symbol name. Specifically, you must escape any ASCII character other than an alphabetic character [a-z, A-Z], the underline character (\_) or the question mark character (?).

* You can use a character's ASCII octal value to represent any character other than NULL.Be aware that if the octal code you use as a symbol name defines a printable character then SKILL uses that character as a print name for the symbol. For example,

> `char = '\120 char => Pprintf( "Char = %c\n" '\120 ) => t`

> and prints

> `Char = P`

* As an alternative to ASCII octal values, you can refer to the unprintable characters listedin the [Escape Sequences](#1010958 "Language Characteristics"). For example, the formfeed character is represented by \f and the newline character is represented by \n.

The table below lists all the ASCII characters and their corresponding symbol. The only ASCIIcharacter that cannot be handled by SKILL is NULL (ASCII code 0) because the null character always terminates a string in UNIX.

**Symbols for ASCII Characters**

| **Character(s)** | **SKILL Symbol Name(s)**
| a, b, …, z | a, b, …, z
| A, B, …, Z | A, B, …, Z
| ?, \_ | ?, \_
| 0, 1, …, 9 | \0, \1, …, \9
| ^A, ^B, …, ^Z, … (octal codes 001-037) | \001, \002, …, \032, … (in octal)
| <space> | \<space> (backslash followed by a space)
| ! . ; : , | \! \. \; \: \,
| ( ) [ ] { } | \( \) \[ \] \{ …
| " # % & + - \* | \" \# \% …
| < = > @ / \ ^ ~ | \< \= \> …
| DEL | \177
For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
