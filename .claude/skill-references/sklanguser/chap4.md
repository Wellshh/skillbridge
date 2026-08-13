### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

4
=

Data Structures
===============

For information on data structures and related topics, see the following sections:

* [Access Operators](#1008203 "Data Structures")

* [Symbols](#1008218 "Data Structures")

* [Disembodied Property Lists](#1008324 "Data Structures")

* [Strings](#1008386 "Data Structures")

* [Defstructs](#1008596 "Data Structures")

* [Arrays](#1008683 "Data Structures")

* [Association Tables](#1008719 "Data Structures")

* [Association Lists](#1008817 "Data Structures")

* [User-Defined Types](#1008828 "Data Structures")

Access Operators
----------------

Several of the data access operators have a generic nature. That is, the syntax of accessingdata for different data types can be the same. You can view the arrow operator as being a property accessor and the array reference operator [ ] as an indexer. The operators described below are used in examples throughout this chapter.

#### Arrow (->) Operator

The arrow (->) operator can be applied to disembodied property lists, defstructs, associationtables, and user types (special application-supplied types) to access property values. The property must always be a symbol and the value of the property can be any valid Cadence® SKILL language type.

#### Squiggle Arrow (~>) Operator

The squiggle arrow (~>) operator is a generalization of the arrow operator. It works the sameway as an arrow operator when applied directly to an object, but it can also accept a list of such objects. It walks the list applying the arrow operator whenever it finds an atomic object.

The underlying functions for ~> operator are the`setSGq` and `getSGq` functions, which set and retrieve the value of an attribute or a property. For example,

`setSGq(obj value prop)             ; is equivalent to:`

`obj~>prop=value`

`a=getSGq(obj prop)                 ; is equivalent to:`

`a=obj~>prop`

`info=getSGq(cvId objType)          ; is equivalent to:`

`info=cvId~>objType`

`setSGq(rect list(10:10 100:120) bBox) ; is equivalent to:`

`rect~>bBox=list(10:10 100:120)`

#### Array Access Syntax [ ]

The array access syntax [ ] can be used to access

* Elements of an array

* Key-value pairs in an association list

Symbols
-------

Symbols in SKILL correspond to variables in C. In SKILL, the terms "symbol" and "variable"are often used interchangeablyeven though symbols in SKILL are used for other things as well. Each symbol has the following components:

* Print name

* Value

* Function binding

* Property list

Except for the name slot, all slots can be optionally empty. It is not advisable to give symbolsboth a value and a function binding.

### Creating Symbols

The system creates a symbol whenever it encounters a text reference to the symbol for thefirst time. When the system creates a new symbol, the value of the symbol is set to *unbound*.

Normally, you do not need to explicitly create symbols. However, the following functions letyou create symbols.

#### Creating a Symbol with a Given Base Name (gensym)

Use the*gensym* function to create a symbol with a given base name. The system determines the index appended to the base name to ensure that the symbol is new. The *gensym* function returns the newly created symbol, which has the value *unbound.* For example:

`gensym( 'net ) => net2`

#### Creating a Symbol from Several Strings (concat)

Use the*concat* function to create a symbol when you need to build the name from several strings.

### The Print Name of a Symbol

Symbol names can contain alphanumeric characters (a-z, A-Z, 0-9), the underscore (\_)character, and the question mark (?). If the first character of a symbol is a digit, it must be preceded by the backslash character (\). Other printable characters can be used in symbol names by preceding each special character with a backslash.

#### Retrieving the Print Name of a Symbol (get\_pname)

Use the*get\_pname* function to retrieve the print name of a symbol. This function is most useful in a program that deals with a variable whose value is a symbol. For example:

`location = 'U235get_pname( location ) => "U235"`

### The Value of a Symbol

The value of a symbol can be any type, including the type*symbol*.

#### Assigning a Symbol's Value

Use the = operator to assign a value to a symbol. The*setq* function corresponds to the = operator. The following are equivalent.

`U235 = 100setq( U235 100 )`

#### Retrieving a Symbol's Value

Refer to the symbol's name to retrieve its value.

`U235 => 100`

#### Using the Quote Operator with a Symbol

If you need to refer to a symbol itself instead of its value, use the quote operator.

`location = 'U235 => U235`

#### Storing a Symbol's Value Indirectly (set)

You can assign a value indirectly to a symbol with the*set* function. There is no operator that corresponds to the *set* function. The following assigns 200 to the symbol *U235*.

`set( location 200 )`

#### Retrieving a Symbol's Value Indirectly (symeval)

You can retrieve a symbol's value indirectly with the*symeval* function. There is no operator that corresponds to the *symeval* function.

`symeval( location ) => 200`

#### Global and Local Values for a Symbol

Global and local variables and function parameters are handled differently in SKILL than theyare in C and Pascal.

SKILL uses symbols for both global and local variables. A symbol's current value is accessibleat any time from anywhere. SKILL manages a symbol's value slot transparently as if it were a stack. The current value of a symbol is simply the top of the stack. Assigning a value to a symbol changes only the top of the stack. Whenever the flow of control enters a *let* or *prog* expression, the system pushes a temporary value onto the value stack of each symbol in the local variable list.

### The Function Binding of a Symbol

When you declare a SKILL function, the system uses the function's name to determine asymbol to hold the function definition. The function definition is stored in the function slot.

If you are redefining the function, the same symbol is reused and the previous functiondefinition is discarded.

Unlike the symbol's value slot, the symbol's function slot is not affected when the flow ofcontrol enters or exits *let* or *prog* expressions.

### The Property List of a Symbol

A*property list* is a list containing property name/value pairs. Each name/value pair is stored as two consecutive elements on a property list. The *property* *name*, which must be a symbol, comes first. The *property value*, which can be of any data type, comes next.

When a symbol is created, SKILL automatically attaches to it a property list initialized to*nil*. A symbol property list can be accessed in the same way structures or records are accessed in C or Pascal, by using the dot operator and arrow operators.

#### Setting a Symbol's Property List (setplist)

The*setplist* function sets a symbol's property list. For example:

`setplist( 'U235 '( x 200 y 300 ) ) => ( x 200 y 300 )`

#### Retrieving a Symbol's Property Lst (plist)

The*plist* function returns the property list associated with a symbol.

`plist( 'U235 ) => ( x 200 y 300 )`

#### Using the Dot Operator to Retrieve Symbol Properties

The dot (.) operator gives you a simple way of accessing properties stored on a symbol'sproperty list. The dot operator cannot be nested, and both the left and right sides of the dot operator must be symbols. For example:

`U235.x => 200`

The*getqq* function implements the dot operator. For example, the following behave identically.

`U235.x getqq( U235 x )`

The*qq* suffix informally indicates that both arguments are implicitly quoted.

If you ask for the value of a particular property on a symbol and the property does not existon the symbol's property list, *nil* is returned.

#### Using the Dot and Assignment Operators to Store Symbol Properties

If you assign a value to a property that does not exist, that property is created and put on theproperty list.

#### Using the arrow operator toRetrieve Symbol Properties

The arrow ( -> ) operator gives you a simple way of indirectly accessing properties stored ona symbol's property list. The *getq* function implements the arrow operator. Both the left and right sides of the -> operator must be symbols. For example:

```
designator = 'U235U235.x = 200 U235.y = 300designator->x => 200designator->y => 300
```

#### Using the Arrow Operator and the Assignment Operator to Store Symbol Properties

The arrow ( -> ) operator and the assignment ( = ) operator work together to provide a simpleway of indirectly storing properties on a symbol's property list. For example:

`designator->x = 250U235.x => 250`

The*putpropq* function implements both the arrow operator and the assignment operator. For example, the following behave identically.

`designator->x = 250putpropq( designator 250 x )`

### Important Symbol Property List Considerations

Property lists attached to symbols are*globally visible to all applications*. Whenever you pass a symbol to a function, that function can add or alter properties on that symbol's property list.

In the following example, even though the sample property is established within a*let* expression, it is still available outside the *let* expression. In other words, when the flow of control enters and subsequently exits a *let* or *prog* expression, the property lists of local symbols are not affected.

```
x = 0let( ( x )       x = 2       x.example = 5       ) ; letx => 0plist( 'x ) => (example 5)
```

* ***If you want to use symbol property lists to pass data from one function toanother, you must make sure you choose unique names to avoid possible name collisions with other applications. Use setplist with caution because you might inadvertently destroy properties of importance to other applications.***

Disembodied Property Lists
--------------------------

A disembodied property list is logically equivalent to a record. Unlike C structures or Pascalrecords, new fields can be dynamically added or removed. The arrow operator (->) can be used to store and retrieve properties in a disembodied property list.

A disembodied property list starts with a SKILL data object, usually*nil*, followed by alternating name/value pairs. The property names must satisfy the SKILL symbol syntax to be visible to the arrow operator. The first element of the disembodied list does not have to be *nil*. It can be any SKILL data object.

In the following example, a disembodied property list is used to represent a complex number.

```
procedure( trMakeComplex( @key ( real 0 ) ( imaginary 0 ) )      let( ( result )            result = ncons(nil)            result->real = real             result->imaginary = imaginary            result       ) ; let) ; procedure
```

```
complex1 = trMakeComplex( ?real 2 ?imaginary 3 )      => (nil imaginary 3 real 2)complex2 = trMakeComplex( ?real 4 ?imaginary 5 )      => (nil imaginary 5 real 4)
```

`i = trMakeComplex( ?imaginary 1 )      => (nil imaginary 1 real 0)`

```
procedure( trComplexAddition( cmplx1 cmplx2 )      trMakeComplex(             ?real        cmplx1->real + cmplx2->real             ?imaginary   cmplx1->imaginary + cmplx2->imaginary      )) ; procedureprocedure( trComplexMultiplication( cmplx1 cmplx2 )      trMakeComplex(             ?real                  cmplx1->real * cmplx2->real -                  cmplx1->imaginary * cmplx2->imaginary            ?imaginary                  cmplx1->imaginary * cmplx2->real +                  cmplx1->real * cmplx2->imaginary      ) ) ; procedure
```

`trComplexMultiplication( i i ) => (nil imaginary 0 real -1)`

In several circumstances using a disembodied property list to represent a record hasadvantages over using a symbol's property list.

* An appropriate symbol to which you can attach a property list might not be available. Forexample, no symbol exists for complex numbers in the example above.

* If you create a symbol for each record your application tracks and your applicationrequires many records, SKILL will have a lot of extra symbols to manage.

* It is easier to pass a disembodied property list as a parameter than it is to pass a symbolas a parameter.

You can store a disembodied property list as the value of a symbol without affecting thesymbol's property list.

```
setplist( 'x '( example 0.5 ))x = complex1     => (nil imaginary 3 real 2)plist( 'x )      => ( example 0.5 )
```

### Important Considerations

Be careful when you are assigning disembodied property lists to variables.

* ***Property list functions that modify property lists modify the original liststructures directly. If the property list is not to be shared, use the copy function to make a copy of the original property list.***

This caution applies in general to assigning lists as values. Internally, SKILL uses pointers tothe lists in virtual memory. For example, as a result of the following assignment

`complex1 = complex2`

both symbols*complex1* and *complex2* refer to the same list in virtual memory. Using the arrow operator to modify the *real* or *imaginary* properties of *complex2* is reflected in *complex1*.

Notice that

`complex1 == complex2     => teq( complex1 complex2 )  => t`

To avoid this problem, perform the assignment as follows.

`complex1 = copy( complex2 )`

Notice that

`complex1 == complex2     => teq( complex1 complex2 )  => nil`

### Additional Property List Functions

#### Adding Properties to Symbols or Disembodied Property Lists (putprop)

*putprop* adds properties to symbols or disembodied property lists. If the property already exists, the old value is replaced with a new one. The *putprop* function is a *lambda* function, which means all of its arguments are evaluated.

`putprop('s 1+2 'x)   => 3s.x = 1+2            => 3`

Both examples are equivalent expressions that set the property*x* on symbol *s* to 3.

#### Getting the Value of a Named Property in a Property List (get)

*get* returns the value of a named property in a property list. *get* is used with *putprop*, where *putprop* stores the property and *get* retrieves it.

`putprop( 'U235 8 'pins )`

> > Assigns the property*pins* on the symbol *U235* to a value of 8.

`get( 'U235 'pins )   => 8U235.pins                               => 8`

#### Adding Properties to Symbols or Disembodied Property Lists (defprop)

*defprop* adds properties to symbols or disembodied property lists, but none of its arguments are evaluated. *defprop* is the same as *putprop* except that none of its arguments are evaluated.

`defprop(s 3 x)       => 3`

> > Sets property*x* on symbol *s* to 3.

`defprop(s 1+2 x)     => 1+2`

> > Sets property*x* on symbol *s* to the unevaluated expression 1+2.

#### Removing a Property and Restoring a Previous Value (remprop)

*remprop* removes a property from a property list. The return value is not useful.

`setplist( 'U235 '( x 100 y 200 )) => (x 100 y 200)`

> Sets the property list to*(x 100 y 200 )*.

`putprop( 'U235 8 'pins )       => 8`

> Sets the value of the pins property to 8.

`plist( 'U235 )       => (pins 8 x 100 y 200)`

> Verifies the operation.

`get( 'U235 'pins )       => 8`

> Retrieves the pins property.

`remprop( 'U235 'x )`

> Removes the*x* property.

`plist( 'U235 )       => (pins 8 y 200)`

Strings
-------

A*string* is a specialized one-dimensional array whose elements are characters.

The string functions in this section are patterned after functions of the same name in the Crun-time library. Strings can be compared, taken apart, or concatenated.

### Concatenating Strings

#### Concatenating a List of Strings with Separation Characters (buildString)

*buildString* makes a single string from the list of strings. You specify the separation character in the third argument. A null string is permitted. If this argument is omitted, *buildString* provides a separating space as the default.

```
buildString( '("test" "il") ".")  => "test.il"buildString( '("usr" "mnt") "/")  => "usr/mnt"buildString( '("a" "b" "c"))      => "a b c"buildString( '("a" "b" "c") "")   => "abc"
```

#### Concatenating Two or More Input Strings (strcat)

*strcat* creates a new string by concatenating two or more input strings. The input strings are left unchanged.

`strcat( "l" "ab" "ef" ) => "labef"`

You are responsible for any separating space.

```
strcat( "a" "b" "c" "d" )     => "abcd" strcat( "a " "b " "c " "d " ) => "a b c d "
```

#### Appending a Maximum Number of Characters from Two Input Strings (strncat)

*strncat* is similar to *strcat* except that the third argument indicates the maximum number of characters from *string2* to append to *string1* to create a new string. *string1* and *string2* are left unchanged.

```
strncat( "abcd" "efghi" 2)   => "abcdef"strncat( "abcd" "efghijk" 5) => "abcdefghi"
```

### Comparing Strings

#### Comparing Two String or Symbol Names Alphabetically (alphalessp)

*alphalessp* compares two objects, which must be either a string or a symbol, and returns *t* if *arg1* is alphabetically less than the name of *arg2*. *alphalessp* can be used with the *sort* function to sort a list of strings alphabetically. For example:

```
stringList = '( "xyz" "abc" "ghi" )sort( stringList 'alphalessp ) => ("abc" "ghi" "xyz")
```

The next example returns a sorted list of all the files in the login directory.

`sort( getDirFiles( "~" ) 'alphalessp )`

#### Comparing Two Strings Alphabetically (strcmp)

*strcmp* compares two strings. To simply test if two strings are equal or not, you can use the *equal* command. The return values for *strcmp* indicate

1. **Meaning**
2. string1 is alphabetically greater than string2.
3. string1 is alphabetically equal to string2.
4. string1 is alphabetically less than string2.

`strcmp( "abc" "abb" )=> 1strcmp( "abc" "abc")=> 0strcmp( "abc" "abd")=> -1`

#### Comparing Two String or Symbol Names Alphanumerically or Numerically (alphaNumCmp)

*alphaNumCmp* compares two string or symbol names. If the third optional argument is non-nil and the first two arguments are strings holding purely numeric values, a numeric comparison is performed on the numeric representation of the strings. The return values indicate

1. **Meaning**
2. arg1 is alphanumerically greater than arg2.
3. arg1 is alphanumerically identical to arg2.
4. arg2 is alphanumerically greater than arg1.

```
alphaNumCmp( "a" "b" )           =>-1alphaNumCmp( "b" "a" )           => 1alphaNumCmp( "name12" "name12" ) => 0alphaNumCmp( "name23" "name12" ) => 1alphaNumCmp( "00.09" "9.0E-2" t) => 0
```

#### Comparing a Limited Number of Characters (strncmp)

*strncmp* compares two strings alphabetically, but only up to the maximum number of characters indicated in the third argument. The return values indicate the same as for *strcmp* above.

`strncmp( "abc" "ab" 3) => 1strncmp( "abc" "de" 4) => -1`

### Getting Character Information in Strings

#### Getting the Length of a String in Characters (strlen)

Refer to["Pattern Matching of Regular Expressions"](#patternMatching "Data Structures") for information on the backslash notation used below.

`strlen( "abc" ) => 3strlen( "\007" )=> 1`

### Indexing with Character Pointers

#### Getting the Index Character of a String (getchar)

*getchar* returns an indexed character of a string or the print name if the string is a symbol.

`getchar("abc" 2) => bgetchar("abc" 4) => nil`

*getchar* returns a symbol whose print name is the character, not a string.

SKILL represents an individual character by the symbol whose print name is the stringconsisting solely of the character. For example:

```
getchar( "1.2" 2 )               => \.type( getchar( "1.2" 2 ) )       => symbolget_pname( getchar( "1.2" 2 ) )  => "."
```

If you are familiar with C, you should note that the*getchar* SKILL function is totally unrelated to the C function of the same name.

#### Getting the Tail of a String (index, rindex)

*index* returns the remainder of *string1* beginning with the first occurrence of *string2*.

```
index( "abc" 'b )                                       => "bc"index( "abcdabce" "dab" )                    => "dabce"index( "abc" "cba" )                                => nilindex( "dandelion" "d")          => "dandelion"
```

*rindex* returns the remainder of *string1* beginning with the last occurrence of *string2*.

`rindex( "dandelion" "d")         => "delion"`

#### Getting the Character Index of a String (nindex)

*nindex* finds the symbol or string, *string2*, in *string1* and returns the character index, starting from one, of the first point at which *string2* matches part of *string1*.

```
nindex( "abc" 'b )         => 2nindex( "abcdabce" "dab" ) => 4nindex( "abc" "cba" )      => nil
```

### Creating Substrings

#### Copying Substrings (substring)

*substring* creates a new substring from an input string, starting at an index point (*arg2*) and continuing for a given length (*arg3*).

`substring("abcdef" 2 4)=> "bcde"substring("abcdef" 4 2)=> "de"`

#### Breaking Lists Into Substrings (parseString)

*parseString* breaks a string into a list of substrings with specified break characters, which are indicated by an optional second argument.

`parseString( "Now is the time" ) => ("Now" "is" "the" "time")`

> Space is the default break character

`parseString( "prepend" "e" )      => ("pr" "p" "nd" )`

> *e* is the break character.

`parseString( "feed" "e")          => ("f" "d")`

> A sequence of break characters in*t\_string* is treated as a single break character.

`parseString( "~/exp/test.il" "./") => ("~" "exp" "test" "il")`

> Both . and / are break characters.

`parseString( "abc de" "")         => ("a" "b" "c" " " "d" "e")`

> The single space between c and d contributes " " in the return result.

### Converting Case

#### Converting to Upper Case (*upperCase*)

*upperCase* replaces lowercase alphabetic characters with their uppercase equivalents. If the parameter is a symbol, the name of the symbol is used.

`upperCase("Hello world!")    => "HELLO WORLD!"`

```
symName = "nameofasymbol"    => "nameofasymbol"upperCase(symName)           => "NAMEOFASYMBOL"
```

#### Converting to Lower Case (*lowerCase*)

*lowerCase* replaces uppercase alphabetic characters with their lowercase equivalents. If the parameter is a symbol, the name of the symbol is used.

`lowerCase("Hello World!")          => "hello world!"`

### Pattern Matching of Regular Expressions

In many applications, you need to match strings or symbols against a pattern. SKILL providesa number of pattern matching functions that are built on a few primitive C library routines with a corresponding SKILL interface.

A*pattern* used in the pattern matching functions is a string indicating a regular expression. Here is a brief summary of the rules for constructing regular expressions in SKILL:

****Rules for Constructing Regular Expressions****

| **Synopsis** | **Meaning**
| c | Any ordinary character (not a specialcharacter listed below) matches itself.
| . | A dot matches any character.
| \ | A backslash when followed by a special character matches thatcharacter literally. When followed by one of <, >, (, ), and 1,…,9, it has a special meaning as described below.
| [c…] | A nonempty string of characters enclosed in square brackets (called aset) matches one of the characters in the set. If the first character in the set is ^, it matches a character not in the set. A shorthand S-E is used to specify a set of characters S up to E, inclusive. The special characters ] and - have no special meaning if they appear as the first character in a set.
| \* | A regular expression in the above form, followed by the closurecharacter \* matches zero or more occurrences of that form.
| + | Similar to \*, except it matches*one* or more times.
| \(…\) | A regular expression wrapped as \( form \) matches whatever*form* matches, but saves the string matched in a numbered register (starting from one, can be up to nine).
| \n | A backslash followed by a digit *n* matches the contents of the *n*th register from the current regular expression.
| \<…\> | A regular expression starting with a \< and/or ending with a \> restrictsthe pattern matching to the beginning and/or the end of a word. A word defined to be a character string can consist of letters, digits, and underscores.
| rs | A composite regular expression*rs* matches the longest match of *r* followed by a match for *s*.
| ^, $ | A ^ at the beginning of a regular expression matches the beginning ofa string. A $ at the end matches the end of a string. Used elsewhere in the pattern, ^ and $ are treated as ordinary characters.
#### How Pattern Matching Works

The mechanism for pattern matching

* Compiles a pattern into a form and saves the form internally

* Uses that internal form in every subsequent matching against the targets until the nextpattern is supplied

The*rexCompile* function does the first part of the task, that is, the compilation of a pattern. The *rexExecute* function takes care of the second part, that is, actually matching a target against the previously compiled pattern. Sometimes this two-step interface is too low-level and awkward to use, so functions for higher-level abstraction (such as *rexMatchp*) are also provided in SKILL.

#### Avoiding Null and Backslash Problems

* A null string ("") is interpreted as no pattern being supplied, which means the previouslycompiled pattern is still used. If there was no previous pattern, an error is signaled.

* To put a backslash character (\) into a pattern string, you need an extra backslash (\) toescape the backslash character itself.

For example, to match a file name with dotted extension ".il", the pattern "^[a-zA-Z]+\\.il$" canbe used, but "^[a-zA-Z]\.il$" gives a syntax error. However, if the pattern string is read in from an input function such as *gets* that does not interpret backslash characters specifically, you should *not* add an extra backslash to enter a backslash character.

### Pattern MatchingFunctions

#### Finding a Pattern Within a String or Symbol (rexMatchp)

```
rexMatchp("[0-9]*[.][0-9][0-9]*" "100.001")   => trexMatchp("[0-9]*[.][0-9]+" ".001")           => trexMatchp("[0-9]*[.][0-9]+" ".")              => nilrexMatchp("[0-9]*[.][0-9][0-9]*" "10.")     => nil
```

`rexMatchp("[0-9" "100")=> *Error* rexMatchp: Missing ] - "[0-9"`

#### Finding a Pattern within a String, Symbol, or PCRE object (pcreMatchp)

`pcreMatchp( g_pattern S_subject [ x_compOptBits ] [ x_execOptBits ] ) => t | nil`

Checks to see if a string or symbol matches a given regular expression.

#### Examples

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

#### Compiling a Regular Expression String Pattern (rexCompile)

*rexCompile* compiles a regular expression string pattern into an internal representation to be used by succeeding calls to *rexExecute*.

```
rexCompile("^[a-zA-Z]+")                  => trexCompile("\\([a-z]+\\)\\.\\1")          => trexCompile("^\\([a-z]*\\)\\1$")           => trexCompile("[ab") => *Error* rexCompile: Missing ] - "[ab"
```

#### Compiling a Regular Expression String Pattern (pcreCompile)

Compiles a regular expression string pattern (`t_pattern`) into an internal representation that you can use in a `pcreExecute` function call.

`pcreCompile( t_pattern [ x_options ] ) => o_comPatObj | nil`

#### Examples

comPat1 = pcreCompile( "[12[:^digit:]]" ) => pcreobj@0x27d150

comPat2 = pcreCompile( "((?i)ab)c" ) => pcreobj@0x27d15c

comPat3 = pcreCompile( "\\d{3}" ) => pcreobj@0x27d168

#### Matching Against a Previously Compiled Pattern (rexExecute)

*rexExecute* matches a string or symbol against the previously compiled pattern created by the last *rexCompile* call.

```
rexCompile("^[a-zA-Z][a-zA-Z0-9]*")       => trexExecute('Cell123)                      => trexExecute("123 cells")                  => nil
```

The target "123 cells" does not begin with a-z/A-Z.

```
rexCompile("\\([a-z]+\\)\\.\\1")          => trexExecute("abc.bc")                      => trexExecute("abc.ab")                     => nil
```

```
rexCompile("\\(^[a-z]+\\)\\.\\1")         =>trexExecute("abc.bc")                     => nil
```

The caret (^) in the*rexCompile* pattern requires that the pattern must match from the beginning of the input string.

#### Matching Against a Previously Compiled Pattern (pcreExecute)

Matches against a string or symbol (`S_subject`) against a previously compiled pattern set up by the last pcreCompile call.

pcreExecute(
`o_comPatObj`
`S_subject`
[ `x_options` ]
)
=> t | nil

#### Examples

```
comPat1 = pcreCompile( "[12[:^digit:]]" ) => pcreobj@0x27d150pcreExecute( comPat1 "abc" )             => t
```

```
comPat2 = pcreCompile( "((?i)ab)c" ) => pcreobj@0x27d15cpcreExecute( comPat2 "aBc" )         => t
```

```
comPat3 = pcreCompile( "\\d{3}" ) => pcreobj@0x27d168pcreExecute( comPat3 "789" )      => t
```

#### Matching a List of Strings or Symbols (rexMatchList)

*rexMatchList* matches a list of strings or symbols against a regular expression string pattern and returns a list of the strings or symbols that match.

`rexMatchList("^[a-z][0-9]*" '(a01 x02 "003" aa01 "abc"))=> (a01 x02 aa01 "abc")`

```
rexMatchList("^[a-z][0-9][0-9]*"       '(a001 b002 "003" aa01 "abc"))=> (a001 b002)
```

`rexMatchList("box[0-9]*" '(square circle "cell9" "123"))=> nil`

#### Creating an Association List Made of Matching Strings (rexMatchAssocList)

*rexMatchAssocList* returns a new association list created out of those elements of an association list whose key matches a regular expression string pattern.

```
rexMatchAssocList("^[a-z][0-9]*$"      '((abc "ascii") ("123" "number") (a123 "alphanum")      (a12z "ana")))=> ((a123 "alphanum"))
```

```
rexMatchAssocList("^[a-z]*[0-9]*$"      '((abc "ascii") ("123" "number") (a123 "alphanum")      (a12z "ana")))=> ((abc "ascii") ("123" "number") (a123 "alphanum"))
```

#### Turning Meta-Characters On and Off (rexMagic)

*rexMagic* turns on or off the special interpretation associated with the meta-characters (^, $, \*, +, \, [, ], and so forth) in regular expressions. Users of *vi* will recognize this as equivalent to the *set magic/set nomagic* commands.

```
rexCompile( "^[0-9]+" )      => trexExecute( "123abc" )       => trexSubstitute( "got: \\0")   => "got: 123"rexMagic( nil )                                  => nilrexCompile( "^[0-9]+" )      => t;Recompile w/o magic.rexExecute( "123abc" )       => nilrexExecute( "**^[0-9]+!**")  => trexSubstitute( "got: \\0")   => "got: \\0"rexMagic( t )                                       => trexSubstitute( "got: \\0")   => "got: ^[0-9]+"
```

#### Replacing a Substring (rexReplace)

*rexReplace* replaces the substring(s) in the source string that matched the last regular expression compiled by the replacement string. The third argument tells which occurrence of the matched substring is to be replaced. If it's 0 or negative, all the matched substrings will be replaced. Otherwise only the specified occurrence is replaced. *rexReplace* returns the source string if the specified match is not found

```
rexCompile( "[0-9]+" )=> trexReplace( "abc-123-xyz-890-wuv" "(*)" 1)=> "abc-(*)-xyz-890-wuv"rexReplace( "abc-123-xyz-890-wuv" "(*)" 2)=> "abc-123-xyz-(*)-wuv"rexReplace( "abc-123-xyz-890-wuv" "(*)" 3)=> "abc-123-xyz-890-wuv"rexReplace( "abc-123-xyz-890-wuv" "(*)" 0)=> "abc-(*)-xyz-(*)-wuv"rexCompile( "xyz" )              => trexReplace( "xyzzyxyzz" "xy" 0)  => "xyzyxyz" ; No rescanning!
```

Defstructs
----------

Defstructs are collections of one or more variables. They can be of different types andgrouped together under a single name for easy handling. They are the equivalent of structs in C.

The following template for*defstruct* defines a data structure with the named slots:

`defstruct( s_name s_slot1 [s_slot2..] ) => t`

The*defstruct* also creates a constructor function, *make\_name*, where *name* is the structure name supplied to *defstruct*. The constructor function takes keyword arguments: one for each slot in the structure. All arguments are symbols and none need to be quoted.

**Note:** The increment (pre-increment, post-increment) and decrement (pre-decrement, post-decrement) operations can't be used to directly modify the variable values when used within structures. However, you can use these operations with arrays and associated table elements. For example,

`array[index]++`

`array[index]--`

`--array[index]`

`++array[index]`

### Behavior Is Similar to Disembodied Property Lists

Once created, structures behave just like disembodied property lists, but are more efficient inspace utilization and access times. Structures can have new slots added at any time. However, these dynamic slots are less efficient than the statically declared slots, both in access time and space utilization.

Defstructs respond to the following operations, assuming*struct* is an instance built from a constructor function:

`struct->slot`

Returns the value associated with a slot of an instance.

`struct->slot = newval`

Modifies the value associated with a slot of an instance.

`struct->?`

Returns a list of the slot names associated with an instance.

`struct->??`

Returns a property list (not a disembodied property list) containing the slot names and valuesassociated with an instance.

### Additional Defstruct Functions

#### Testing a SKILL Object (defstructp)

`defstructp( g_object [st_name] ) => t / nil`

*defstructp* tests a SKILL object, returning *t* if it's a structure instance, otherwise *nil*. The second argument is optional and denotes the name of the structure to test for. The test in this case is stronger and only returns *t* if *g\_object* is an instance of defstruct *st\_name*. The name can be passed either as a symbol or a string.

#### Printing the Contents of a Structure (printstruct)

`printstruct( r_structureInstance ) => t`

For debugging, the*printstruct* function prints the contents of a structure in an easily readable form. It recursively dumps out any slot value that is also a structure instance. The *printstruct* function dumps out a structure instance.

#### Beware of Structure Sharing (copy\_<name>)

Structures can contain instances of other structures; therefore, you need to be careful aboutstructure sharing. If sharing is not desired, a special copy function can be used to generate a copy of the structure being inserted. The *defstruct* function also creates a function for the given *defstruct* called *copy\_<name>*. This function takes one argument, an instance of the *defstruct*. It creates and returns a copy of the instance.

#### Making a Deep or Recursive Copy (copyDefstructDeep)

`copyDefstructDeep( r_object ) => r_object`

Performs a deep or recursive copy on defstructs with other defstructs as sub-elements,making copies of all the defstructs encountered. The various *copy\_name* functions are called to create copies for the defstructs encountered in the deep copy.

### Accessing Named Slots in SKILL Structures

#### Slot Access Example

This example defines a*card* structure and allocates an instance of *card*.

`defstruct( card rank suit faceUp ) => t`

This structure has three slots:*rank suit faceUp*. Next, allocate an instance of *card* and store a reference to it in *aCard*.

`aCard = make_card( ?rank 'ace ?suit 'spades )=> array[5]:21556040`

Structure instances are implemented as arrays. Refer to["Arrays"](#1008683 "Data Structures").

`aCard => array[5]:21556040`

The*type* function returns the structure name.

`type( aCard ) => card`

#### Use the Arrow Operator -> and ~> to Access Slots

`aCard->rank => aceaCard->faceUp = t => t`

#### Use ->? to Get a List of the Slot Names

`aCard->? => ( faceUp suit rank )`

#### Use ->?? to Get a List of Slot Names and Values

`aCard->?? => ( faceUp t suit spades rank ace )`

Slots can be created dynamically for an instance by simply referencing them with the ->operator.

If you have a list of instances of defstructs and you wish access the same slot in all theinstances in that list use the ~> operator.

```
cardList = list( make_card( ?rank 'ace ?suit 'spades )                   make_card( ?rank 'king ?suit 'diamonds))cardList~>rank       => (ace king)cardList~>faceUp     => (nil nil)cardList~>faceUp = t => (t t)cardList~>faceUp     => (t t)
```

### Extended defstruct Example

* Define a structure.

> `defstruct(point x y)             => t`

* Define another structure.

> `defstruct(bbox ll ur)            => t`

* Make an instance.

> `p1 = make_point(?x 100 ?y 200)   => array[4]:xxx`

* Make another instance.

> `p2 = make_point(?x 0 ?y 0)       => array[4]:xxxx`

* Make a*bbox* instance.

> `b1 = make_bbox()                 => array[4]:xxxx`

* Set a field in*b1*.

> `b1->ll = p2                      => array[4]:xxxx`

* Set the other field.

> `b1->ur = p1                      => array[4]:xxxx`

* Look inside and note the recursive printing.

> ```
> printstruct( b1 )                ; Look inside Structure of type bbox :        ; Note the recursive printing       ll :         Structure of type point:                  x:0            y:0
> ```

> `ur:      Structure of type point:            x: 100      y: 200`

> `b1->ll->x = 12 => 12`

> `printstruct( p2 )Structure of type point :      x: l2      y: 0`

> `p1->??=> (y 200 x 100)`

> `b1->??=> (ur array[4]:xxx ll array[4]:xxx)`

* Add a previously undefined slot.

> ```
> b1->color = 'blueprintstruct( b1 )      Structure of type bbox :            ll :                  Structure of type point :            x: 12            y: 0      ur:      Structure of type point  :            x: 100            y: 200      color: blue
> ```

> `b1->?=> (color ll ur)`

> > Returns the list of currently defined fields.

Arrays
------

An*array* represents aggregate data objects in SKILL. Unlike simple data types, you must explicitly create arrays before using them so the necessary storage can be allocated. SKILL arrays allow efficient random indexing into a data structure using familiar syntax.

* Arrays are not typed. Elements of the same array can be different data types.

* SKILL provides run-time array bounds checking.

* Arrays are one dimensional. You can implement higher dimensional arrays using singledimensional arrays. You can create an array of arrays.

* The array bounds are checked with each array access during run-time. An error occursif the index is outside the array bounds.

### Allocating an Array of a Given Size

Use the*declare* function to allocate an array of a given size.

```
declare( week[7] )       => array[7]:9780700 week                     => array[7]:9780700type( week )             => array arrayp( week )           => t days = '(monday tuesday wednesday                   thursday friday saturday sunday) for( day 0 length(week)-1       week[day] = nth(day days))
```

* The*declare* function returns the reference to the array storage and stores it as the value of *week*.

* The*type* function returns the symbol *array*.

* The*arrayp* function returns *t*.

### Accessing Arrays

When the name of an array appears without an index on the right side of an assignmentstatement, only the array object is used in the assignment; the values stored in the array are not copied. It is therefore possible for an array to be accessible by different names. Indices are used to specify elements of an array and always start with 0; that is, the first element of an array is element 0. SKILL normally checks for an out-of-bounds array index with each array access.

`declare(a[10])a[0] = 1a[1] = 2.0a[2] = a[0] + a[1]`

Creates an array of 10 elements. *a* is the name of the array, with indices ranging from 0 to 9. Assigns the integer 1 to element 0, the float 2.0 to element 1, and the float 3.0 to element 2.

`b = a`

*b* now refers to the same array as *a*.

`declare(c[10])`

Declares another array of 10 elements.

`declare(d[2])`

Declares*d* as an array of 2 elements.

`d[0] = b`

*d[0]* now refers to the array pointed to by *b* and *a*.

`d[1] = c`

*d[1]* is the array referred to by *c*.

`d[0][2]`

Accesses element 2 of the array referred to by*d[0]*.
This is the same element as *a[2]*.

Brackets ([ ]) are used to represent array references and are part of the statement syntax.The *declare* function is also an example of an *nlambda* function. The arguments of *nlambda* functions are passed literally (that is, not evaluated). It is up to the called function to evaluate selected arguments when necessary.

Association Tables
------------------

An association table is a generalized array, a collection of key/value pairs. The SKILL datatypes that can be used as keys in a table are integer, float, string, list, symbol, and instances of certain user-defined types. An association table is implemented internally as a hash table.

An association table lets you look up any entry with valid instances of SKILL data types. Datais stored in key/value pairs that can be quickly accessed with syntax for standard array access and various iterative functions. This access is based on a system that uses the SKILL *equal* function to compare keys.

Association tables offer convenience and performance not available in disembodied propertylists, arrays, or association lists. Disembodied property lists and association lists are not efficient in situations where their contents can expand greatly. In addition, using symbols for properties or keys in a disembodied property list can be wasteful. A simple conversion process converts disembodied property lists and association lists to association tables. An association table can also be converted to a list of association pairs.

### Initializing Tables

The*makeTable* function defines and initializes the association table. This function takes a single string argument as the table name for printing purposes. An optional second argument provides the default value that is returned when a query to the table yields no match. The *tablep* predicate verifies the data type of a table, and the *length* function determines the number of keys in the table. To refer to and add elements, use the syntax for standard array access.

The following example creates a table and loads it with keys and related values that pairnumbers and colors for a color map. The keys can be any of the data type mentioned earlier; they are not restricted to numeric data types.

```
myTable = makeTable("atable1" 0) => table:atable1tablep(myTable)                  => tmyTable[1] = "blue"              => "blue"myTable["two"] = '(r e d)        => (r e d)myTable["three"] = 'green        => greenlength(myTable)                  => 3
```

If a new pair is added to the table but its key already exists, the new value replaces the existingvalue in the table.

If a key to be accessed does not exist, the process returns either the default value specifiedat table creation or the symbol *unbound*, if no default value was specified.

### Manipulating Table Data

The*foreach, forall,* and *setof* functions scan the contents of an association table and perform iterative programming functions on each key and its associated value. Standard input and output functions are available through the *readTable, writeTable*, and *printstruct* functions.

The*append* function appends data from existing disembodied property lists, association lists, or an association table to another existing association table. You specify the association table (created with the *makeTable* function) as the first argument for this function. For the second argument, you specify the disembodied property list, association list, or other association table whose data is to be appended. You can use the *remove* function to remove an entry from an association table.

#### Testing Whether a Data Value is a Table (tablep)

Use the*tablep* function to test whether a data value is a table.

```
myTable = makeTable("atable1" 0)  => table:atable1tablep(myTable)                   => ttablep(9)                         => nil
```

#### Converting the Contents of an Association Table to an Association List (tableToList)

This function eliminates the efficiency that you gain from referencing data in an associationtable. Do not use this function for processing data in an association table. Instead, use this function interactively to look at the contents of a table.

`tableToList(myTable)=> (("two" (r e d)) ("three" green) (1 "blue"))`

#### Writing the Contents of an Association List to a File (writeTable)

The*writeTable* function is for writing basic SKILL data types that are stored in an association table. The function cannot write database objects or other user-defined types that might be stored in association tables.

`writeTable("inventory.log" myTable) => t`

#### Appending the Contents of a File to an Existing Association Table (readTable)

The file must have been created with the*writeTable* function so that the contents are in a usable format.

`readTable("inventory.log" myTable)=> t`

#### Printing the Contents of an Object in a Tabular Format (printstruct)

For debugging, the*printstruct* function prints the contents of a structure in an easily readable form. It recursively prints nested structures.

`printstruct(myTable)=>      1: "blue"      "three": green      "two": (r e d)`

#### Removing Contents from a Table (remove)

The*remove* function can be used to remove an entry from an association table.

`remove(g_key o_table)`

`=> l_result`

Consider an example with the structure of the type association table`myTable` as follows:

`"1": "blue"`

`"3": "yellow"`

`"0": "red"`

`"2": "green"`

Use the remove function as follows:

`remove("1" myTable)`

When you print the contents of the table again, the entry "1" is removed from the table.

`Structure of type association table (table:myTable):`

`"3": "yellow"`

`"0": "red"`

`"2": "green"`

**Note:** When you use the*remove* function, the removal is destructive, that is, any other reference to the table will also see the changes (see "[Removing Elements from a List](chap8.html#1008850 "Advanced List Operations")" ).

### Traversing Association Tables

Use the*foreach* function to visit every key in an association table. For example, use the following function call to print each key/value pair in a table.

```
foreach( key myTable            println(                   list( key myTable[ key ] )                   )      )
```

**Note:** You can also use`myTable['?]` or `myTable->?` to get a list of all the available keys in an association table.

You can also use the functions*forall, exists* and *setof* to traverse association tables. (These functions are described in detail in ["Advanced List Operations"](chap8.html#1008199 "Advanced List Operations"))

For example, use the following function call to test if every key/value pair in a table are suchthat the key is a string and value is an integer.

`forall( key myTable            stringp(key) && fixp(myTable[key])            )`

To check if there is a single pair that satisfies the above expression, call the following function.

`exists( key myTable            stringp(key) && fixp(myTable[key])            )`

* To write the entire contents of a table to a file, use*writeTable*.

* To read a file (created using*writeTable*), use *readTable*.

* To view the contents of a table, use*printstruct*.

The*append* function appends data from existing disembodied property lists or association lists to an existing association table. In addition, the *append* function can add data from one association table to another association table as shown in the following example.

### Implementing Sparse Arrays

A sparse array is an indexed collection, most of whose entries are unused. For large sparsearrays, it is wasteful to allocate the entire array. Instead, you can use an association table for a one-dimensional array. Use integers as the keys. To implement a two-dimensional sparse array, use lists of index pairs as keys.

```
procedure( tr2DSparseArray()            makeTable( gensym( 'trSparseArray ) )      ) ; proceduretrSparseTimesTable = tr2DSparseArray( )for( i 0 3       for( j 0 6             trSparseTimesTable[ list( i j ) ] = i*j            ) ; for      ) ; for
```

### List-Oriented Functions for Association Tables

Several list-oriented functions also work on tables, including iteration.

**List-Oriented Functions for Tables**

| **Use this** | **To do this**
| Syntax for array access | To store and retrieve entries in a table
| *makeTable* function | To create and initialize the association table. The argumentsare the table name (required) and (optional) the default value to return for keys not present in the table. The default is *unbound*.
| *foreach*function | To execute a collection of SKILL expressions for each key/value pair in a table
| *setof* function | To return a list of keys in a table that satisfy a criterion.
| *length* function | To return the number of key/value pairs in a table
| *remove* function | To remove a key from a table
Association Lists
-----------------

A list of key/value pairs is a natural means to record associations. An association list is a listof lists. The first element of each list is the key. The key can be an instance of any of SKILL's basic types.

`assocList = '( ( "A" 1 ) ( "B" 2 ) ( "C" 3 ) )`

The*assoc* function retrieves the list given the index.

`assoc( "B" assocList ) => ( "B" 2 )assoc( "D" assocList ) => nil`

Use the*rplaca* function to destructively update an entry. The following replaces the *car* of the *cdr* of the association list entry.

```
rplaca( cdr( assoc( "B" assocList ) ) "two" ) => ( "two" )assocList => (( "A" 1 ) ( "B" "two" ) ( "C" 3 ))
```

Association lists behave the same way as association tables. For lists with less than ten pairs,it is more efficient to use association lists than association tables. For lists likely to grow beyond ten pairs, it is more efficient to use association tables.

User-Defined Types
------------------

User-defined types are special foreign or external data types exported into SKILL by variousapplications. Their behavior is predetermined by the applications that own them. For example, database and window objects are generally implemented as C-structs and exported into SKILL as user-defined types.

The application that defines the SKILL behavior for the user-defined types provides methodsfor SKILL to apply in various situations. For example, when you apply the accessor operators -> or ~> to a user-defined type, the SKILL engine resolves the operation by calling the accessor method implemented for that type by an application.

There are other methods to support a user-defined type's behavior in SKILL. For example, totest two user-defined types for equality (*equal*), the application exporting the type provides a method to overload the SKILL *equal* function just for that type. The equal method takes two arguments and returns *t* or *nil*.

The application exporting the type determines what methods are needed to support the typein SKILL. If the application does not supply a method, SKILL applies a default behavior. In general, to a user, instances of a user-defined type look and feel very similar to instances of *defstructs*.

Specific information on user-defined types is supplied by the applications exporting the types.For example, creating instances of user-defined types happens when certain application functions are called, such as *dbOpen*.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
