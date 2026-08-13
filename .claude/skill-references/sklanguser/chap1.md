### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

1
=

Getting Started
===============

Cadence® SKILL is a high-level, interactive programming language based on the popular artificial intelligence language, [Lisp](#Lisp "Getting Started"). Because SKILL supports a more conventional C-like syntax, novice users can learn to use it quickly, and expert programmers can access the full power of the Lisp language. SKILL is as easy to use as a calculator as well as being a powerful programming language whose applications are virtually unlimited.

SKILL brings you a functional interface to the underlying subsystems. SKILL lets you quicklyand easily customize existing CAD applications and helps you develop new applications. SKILL has functions to access each Cadence tool using an application programming interface.

This document describes functions that are common to all of the Cadence tools used in eithera graphic or nongraphic environment. Once you master these basic functions, you need to learn only a few new functions to access any tool in the Cadence environment.

* [SKILL's Relationship to Lisp](#Lisp "Getting Started")

* [Cadence SKILL Language at a Glance](#1008229 "Getting Started")

* [SKILL Lists](#1008456 "Getting Started")

* [File Input/Output](#1008650 "Getting Started")

* [Flow of Control](#1008779 "Getting Started")

* [Developing a SKILL Function](#1008981 "Getting Started")

SKILL's Relationship to Lisp
----------------------------

**Note:** If you are new either to SKILL or to programming in general, start with["Cadence SKILL Language at a Glance"](#1008229 "Getting Started").

### Programming Notation

In SKILL, function calls can be written in either of the following notations:

* Algebraic notation used by most programming languages:`func`(`arg1``arg2``…`)

* Prefix notation used by the Lisp programming language: (`func``arg1``arg2`…)

For comparison, here is a SKILL program written first in algebraic notation, then the sameprogram, also implemented in SKILL, using a Lisp style of programming.

```
procedure( fibonacci(n)       if( (n == 1 || n == 2) then             1       else fibonacci(n-1) + fibonacci(n-2)       ))
```

Here is the same program implemented in SKILL using a Lisp style of programming.

```
(defun fibonacci (n)      (cond            ((or (equal n 1) (equal n 2)) 1)            (t (plus (fibonacci (difference n 1))                          (fibonacci (difference n 2))))      ))
```

### Data Manipulation

Because programs in SKILL are represented as lists, just as they are in Lisp, they can bemanipulated like data. You can dynamically create, modify, or selectively evaluate function definitions and expressions. This ability to manipulate data is one of the primary reasons why Lisp is the language of choice for artificial intelligence applications. Because it takes full advantage of the "program is data" concept of Lisp, SKILL can be used to write flexible and powerful applications.

Many SKILL list manipulation functions are available. These functions operate, in most cases,similar to functions of the same name in Lisp, and the Franz Lisp dialect in particular.

SKILL supports a special notation for list construction from templates. This notation isborrowed from Common Lisp and allows selective evaluation within a quoted form. Selective evaluation eliminates the long sequences of calls to `list` and `append`. See [Getting Started](#1008199 "Getting Started").

### Characters

Unlike many other programming languages, including Common Lisp, SKILL does not have aseparate character data type. Characters are instead represented by single character symbols. The character "A," for example, is the symbol "A." Unprintable characters can be referred to using the escape sequences.

Cadence SKILL Language at a Glance
----------------------------------

This section presents a quick look at various aspects of the SKILL programming language.These same subjects are discussed in greater detail in succeeding chapters.

This section introduces new terms and takes a general look at the Cadence Frameworkenvironment. It explores SKILL data, function calls, variables and operators, then tells you how to solve some common problems. Although each application defines the details of its SKILL interface to that application, this document most often refers to the Cadence Design Framework II environment when giving examples.

SKILL is the command language of the Cadence environment. Whenever you use forms,menus, and bindkeys, the Cadence software triggers SKILL functions to complete your task. For example, in most cases SKILL functions can

* Open a design window

* Zoom in by a factor of 2

* Place an instance or a rectangle in a design

Other SKILL functions compute or retrieve data from the Cadence Framework environmentor from designs. For example, SKILL functions can retrieve the bounding box of the current window or retrieve a list of all the shapes on a layer.

You can enter SKILL functions directly on a command line to bypass the graphic userinterface.

### Terms and Definitions

|  |
| --- | ---
| output | The destination of SKILL output can be an xterm screen, adesign window, a file, or in many cases, the Command Interpreter Window (CIW).
|  |
| --- | ---
| CIW | Command Interpreter Window: The start-up working window formany Cadence applications, which contains an input line, an output area, a menu banner with commands to launch various tools, and prompts for general information. The output area of the CIW is the destination of many of the examples used in this manual.
|  |
| --- | ---
| SKILL interpreter | The SKILL interpreter executes SKILL programs within theCadence environment. The interpreter translates a SKILL program's text source code into internal data structures, which it actively consults during the execution of the program.
|  |
| --- | ---
| compiler | A compiler translates source code into a target representation,which might be machine instructions or an intermediate instruction set.
|  |
| --- | ---
| evaluation | The process whereby the SKILL interpreter determines the valueof a SKILL expression.
|  |
| --- | ---
| SKILL expression | An invocation of a SKILL function, often by means of an operatorsupplying required parameters.
|  |
| --- | ---
| SKILL function | A named, parameterizable body of one or more SKILLexpressions. You can invoke any SKILL function from the command input line available in the application by using its name and providing appropriate parameters.
|  |
| --- | ---
| SKILL procedure | This term is used interchangeably with SKILL function.
### Invoking a SKILL Function

There are many ways to submit a SKILL function to the SKILL interpreter for evaluation. Inmany applications, whenever you use forms, menus, and bindkeys, the Cadence software triggers corresponding SKILL functions to complete your task. Normally, you do not need to be aware of SKILL functions or any syntax issues.

|  |
| --- | ---
| Bindkeys | A bindkey associates a SKILL function with a keyboard event.When you cause the keyboard event, the Cadence software sends the SKILL function to the SKILL interpreter for evaluation.
|  |
| --- | ---
| Forms | Some functions require you to provide data by filling out fields ina pop-up form.
|  |
| --- | ---
| Menus | When you choose an item in a menu, the system sends anassociated SKILL function to the SKILL interpreter for evaluation.
|  |
| --- | ---
| CIW | You can directly enter a SKILL function into the CIW forimmediate evaluation.
|  |
| --- | ---
| SKILL Process | You can launch a separate UNIX process that can submit SKILLfunctions directly to the SKILL interpreter.
You can submit a collection of SKILL functions for evaluation by loading a SKILL source codefile.

### Return Value of a Function

All SKILL functions compute a data value known as the return value of the function. You can

* Assign the return value to a SKILL variable

* Pass the return value to another SKILL function

Any type of data can be a return value. SKILL supports many data types, including integers,text strings, and lists.

### Simplest SKILL Data

The simplest SKILL expression is a data item. SKILL data is case sensitive. You can enterdata in many familiar ways, including the following.

**Sample SKILL Data Items**

| **Data Type** | **Syntax Example**
| integer | 5
| floating point | 5.3
| text string | "Mary had a little lamb"
### Calling a Function

Function names are case sensitive. To call a function, state its name and arguments in a pairof parentheses.

`strcat( "Mary" " had" " a" " little" " lamb" ) => "Mary had a little lamb"`

* No spaces are allowed between the function name and the left parenthesis.

* Several function calls can be on a single line. Use spaces to separate them.

* You can span multiple lines in the command line or a source code file.

> ```
> strcat(       "Mary" " had" " a"       " little" " lamb" ) => "Mary had a little lamb"
> ```

* When you enter several function calls on a single line, the system only displays the returnresult from the final function call.

### Operators Are SKILL Functions

SKILL provides many operators. Each operator corresponds to a SKILL function. Here aresome examples of useful operators:

**Sample SKILL Operators**

| **Operators in Descending Precedence** | **Underlying Function** | **Operation**
| \*\* | `expt` | arithmetic
| \* / | `times``quotient` | arithmetic
| + - | `plus``difference` | arithmetic
| ++s, s++ | `preincrement,``postincrement` | arithmetic
| == != | `equal``nequal` | tests for equality tests for inequality
| = | `setq` | assignment
The following example shows several function calls using operators on a single line. The callsare separated by spaces. The system displays the return result from the final function call.

`x = 5 y = 6 x+y => 11`

### Using Variables

You do not need to declare variables in SKILL. SKILL creates a variable the first time itencounters the variable in a session. Variable names can contain

* Alphanumeric characters

* Underscores ( \_ )

* Question marks

The first character of a variable cannot be a digit. Use the assignment operator to store avalue in a variable. You enter the variable name to retrieve its value. The `type` SKILL function returns the data type of the variable's current value.

```
lineCount = 4            => 4lineCount                => 4type( lineCount )        => fixnumlineCount = "abc"        => "abc"lineCount                => "abc"type( lineCount )        => string
```

### Alternative Ways to Invoke a Function

In addition to calling a function by stating its name and arguments in a pair of parentheses,as shown below, you can use two other syntax forms to invoke SKILL functions.

`strcat( "Mary" " had" " a" " little" " lamb" )`

* You can place the left parenthesis to the left of the function name (Lisp syntax).

> `( strcat "Mary" " had" " a" " little" " lamb" ) => "Mary had a little lamb"`

* You can omit the outermost levels of parenthesis if the SKILL function is the first elementat your SKILL prompt, that is, at the top level.

> `strcat "Mary" " had" " a" " little" " lamb" => "Mary had a little lamb"`

You can use all three syntax forms together. In programming, it is best to be consistent.Cadence recommends the first style noted above.

### Solving Some Common Problems

Here are three of the most common SKILL problems.

#### System Doesn't Respond

If you type in a SKILL function and press Return but nothing happens, you most likely haveone of these problems.

* Unbalanced parentheses

* Unbalanced string quotes

* The wrong log file filter set

You might have entered more left parentheses than right parentheses. The following stepstrigger a system response in most cases.

* Type a closing right bracket ( ] ) character. This character closes all outstanding rightparentheses.

* If you still don't get a response, type a double quote (") character followed by a rightbracket ( ] ) character.

In most cases, the system then responds.

If, however, the system responds but subsequently gives erroneous syntax errors for validinput, type an asterisk ( \* ) character followed by a right bracket ( ] ) character.

#### Inappropriate Space Characters

Do not put any space between the function name and the left parenthesis. Notice that thefollowing error messages do not identify the extra space as the cause of the problem.

* Trying to use the`strcat` function to concatenate several strings.

> ```
> strcat ( "Mary" " had" " a" " little" " lamb") Message: *Error* eval: not a function - "Mary"
> ```

* Trying to make an assignment to a variable.

> ```
> greeting = strcat ( "happy" " birthday" )Message: *Error* eval: unbound variable - strcat
> ```

#### Data Type Mismatches

An error occurs when you pass inappropriate data to a SKILL function. The error messageincludes a type template that indicates the expected type of the offending argument.

```
strcat( "Mary had a" 5 )Message: *Error* strcat: argument #2 should be either a string or a symbol (type template = "S") - 5
```

Here are the characters used in type templates for some common data types.

**Some Common Data Types**

| **Data Type** | **Character in Type Template**
| integer number | `x`
| floating point number | `f`
| symbol or character string | `S`
| character string (text) | `t`
| any data type (general) | `g`
For a complete list of data types supported by SKILL, see[Getting Started](#1008199 "Getting Started").

SKILL Lists
-----------

A SKILL list is an ordered collection of SKILL data objects.The list data structure is central to SKILL and is used in many ways.

The elements of a list can be of any data type, including variables and other lists. A list cancontain any number of objects (or be empty). The empty list can be represented either by empty parentheses "( )" or the special atom `nil`. The list must be enclosed in parentheses. Lists can contain other lists to form arbitrarily complex data structures. Here are some examples:

**Sample Lists**

| **List** | **Explanation**
| (1 2 3) | A list containing the integer constants 1, 2, and 3
| (1) | A list containing the single element 1
| ( ) | An empty list (same as the special atomnil)
| (1 (2 3) 4) | A list containing another list as its second element
SKILL displays a list with parentheses surrounding the members of the list. The followingexample stores a list in the variable `shapeTypeList`, then retrieves the variable's value.

```
shapeTypeList = '( "rect" "polygon" "rect" "line" )shapeTypeList => ( "rect" "polygon" "rect" "line" )
```

SKILL provides an extensive set of functions for creating and manipulating lists. Many SKILLfunctions return lists. SKILL can use multiple lines to display lists. SKILL stores the appropriate integer value in the `_itemsperline` global variable.

### Building Lists

There are several main ways to build a list.

* Specify all the elements of the list literally with the single quote (`'`) operator.

* Specify all the elements as evaluated arguments to the`list` function.

* Add an element to an existing list with the`cons` function.

* Merge two lists with the`append` function.

Both the`cons` and `append` functions allocate a new list and return it to you. You should store the return result in a variable. Otherwise, you cannot refer to the list later.

The following functions allow you to construct new lists and work with existing lists in differentways.

#### Making a list from given elements

Thesingle quote (`'`) operator builds a list using the arguments exactly as they are presented. The values of `a` and `b` are irrelevant. The `list` function fetches the values of variables for inclusion in a list.

```
'( 1 2 3 )                   => ( 1 2 3 )a = 1                        => 1b = 2                        => 2list( a b 3 )                => ( 1 2 3 )
```

#### Adding an element to the front of a list (cons)

You should store the return result from`cons` in a variable. Otherwise, you cannot refer to the list later. Commonly, you store the result back into the variable containing the target list.

```
result = '( 2 3 )             => ( 2 3 )result = cons( 1 result )     => ( 1 2 3 )
```

#### Merging two lists (append)

You should store the return result from`append` in a variable. Otherwise, you cannot refer to the list later.

```
oneList = '( 4 5 6 )             => ( 4 5 6 )aList = '( 1 2 3 )               => ( 1 2 3 )bList = append( oneList aList)   => ( 4 5 6 1 2 3 )
```

#### Common Questions and Answers

People often feel that`nil`, and the `cons` and `append` functions are difficult to understand. Let's look at some typical questions.

**Typical Questions**

| **Question** | **Answer**
| What's the difference between`nil` and '`( nil )`? | `nil` is a list containing nothing. Its length is 0.  '`( nil )` builds a list containing a single element. The length is 1.
| How can I add an element to theend of a list? | Use the`list` function to build a list containing the individual elements.  Use the `append` function to merge it to the first list.  More efficient ways to add an element to the end of a list are discussed in a later chapter.
| Can I reverse the order of thearguments to the `cons` function? Will the results be the same? | You might think that simply reversing the elements tothe `cons` function will put the element on the end of the list. However, this is not the case.
| What's the difference between`cons` and `append`? | The`cons` function requires only that its second argument be a list. The length of the resulting list is one more than the length of the original list.  The `append` function requires that both its arguments be lists. The length of the resulting list is the sum of the lengths of the two argument lists.  `append` is slower than `cons` for large lists.
### Accessing Lists

Lists are stored internally as a series of branching decision points. Think of the left branch aspointing to the first element and the right branch as pointing to the rest of the list (further branch decision points). The `car` function follows the left branch and the `cdr` function follows the right branch.

#### Retrieving the first element of a list (car)

`car` returns the first element of a list. `car` was a machine language instruction on the first machine to run Lisp. `car` stands for `contents of the address register`.

`numbers = '( 1 2 3 )         => ( 1 2 3 )car( numbers )               => 1`

#### Retrieving the tail of the list (cdr)

`cdr returns` a list minus the first element. `cdr` was a machine language instruction on the first machine to run Lisp. `cdr` stands for `contents of the decrement register`.

`numbers = '( 1 2 3 )         => ( 1 2 3 )cdr( numbers )               => ( 2 3 )`

#### Retrieving an element given an index (nth)

`nth` assumes a zero-based index. `nth(0 numbers)` is the same as
`car( numbers)`.

`numbers = '( 1 2 3 )         => ( 1 2 3 )nth( 1 numbers )             => 2`

#### Determining if a data object is in a list (member)

The`member` function cannot search all levels in a hierarchical list. It only looks at the top-level elements. Internally the `member` function follows right branches until it locates a branch point whose left branch dead ends in the element.

```
numbers = '( 1 2 3 )         => ( 1 2 3 )member( 4 numbers )          => nilmember( 2 numbers )          => ( 2 3 )
```

#### Counting the elements in a list (length)

`length` determines the length of a list, array, or association table.

`numbers = '( 1 2 3 )         => ( 1 2 3 )length( numbers )            => 3`

### Modifying Lists

The following functions operate on variables without changing their value or creating newvariables.

#### Coordinates

An xy coordinate is represented by a two-element list. The colon (:) binary operator builds acoordinate from an x value and a y value.

`xValue = 300 yValue = 400 aCoordinate = xValue:yValue => ( 300 400 )`

The functions`xCoord` and `yCoord` access the x coordinate and the y coordinate.

`xCoord( aCoordinate ) => 300 yCoord( aCoordinate ) => 400`

* You can use the single quote (`'`) operator or `list` function to build a coordinate list.

* You can use the`car` function to access the x coordinate and `car`(`cdr`( … ) ) to access the y coordinate.

#### Bounding Boxes

A bounding box is represented by a list of the lower-left and upper-right coordinates. Use the`list` function to build a bounding box that contains

* Coordinates specified with the binary operator (:).

> `bBox = list( 300:400 500:450 )`

* Coordinates specified by variables.

> ```
> lowerLeft        = 300:400 upperRight       = 500:450 bBox             = list( lowerLeft upperRight )
> ```

You can use thesingle quote (`'`) operator to build the bounding box if the coordinates are specified by literal lists.

`bBox = '(( 300 400 ) ( 500 450 ))`

Bounding boxes provide a good example of working with the`car` and `cdr` functions. Use any combination of four `a`'s (each `a` executes another `car`) or `d`'s (each `d` executes another `cdr`).

**Using`car` and `cdr` with Bounding Boxes**

| **Functions** | **Meaning** | **Example** | **Expression**
| car | car( … ) | lower left corner | ll = car( bBox)
| cadr | car( cdr( … ) ) | upper right corner | ur = cadr( bBox)
| caar | car( car( … ) ) | x-coord of lower left corner | llx = caar( bBox)
| cadar | car( cdr( car( … ) ) ) | y-coord of lower left corner | lly = cadar( bBox)
| caadr | car( car( cdr( … ) ) ) | x-coord of upper right corner | urx = caadr( bBox)
| cadadr | car( cdr( car( cdr( …] | y-coord of upper right corner | ury = cadadr( bBox)
File Input/Output
-----------------

This section introduces how to

* Display values using default formats and application-specific formats

* Write UNIX text files

* Read UNIX text files

### Displaying Data

Display data using

* The`print` and `println` functions

* The`printf` function

#### The`print` and `println` Functions

The SKILL interpreter has a default display format for each kind of data. The`print` and `println` functions use this format to display data.

**Sample Display Formats**

| **Data Type** | **Example of the Default Format**
| integer | 5
| floating point | 1.3
| text string | "Mary learned SKILL"
| variable | bBox
| list | ( 1 2 3 )
The`print` and `println` functions display a single data value. `println` is the same as `print` followed by a newline character.

`for( i 1 3 print( "hello" ))     ;Prints hello three times."hello""hello""hello"`

`for( i 1 3 println( "hello" ))   ;Prints hello three times."hello""hello""hello"`

#### The`printf` Function

The`printf` function writes formatted output. This example displays a line in a report.

```
printf(       "\n%-15s %-15s %-10d %-10d %-10d %-10d"       layerName purpose       rectCount labelCount lineCount miscCount       )
```

The first argument is a conversion control string containing directives.

```
%[-][width][.precision]conversion_code       [-]                  = left justify       [width]              = minimum number of character positions       [.precision]         = number of characters to be printed       conversion_code             d - decimal(integer)             f - floating point             s - string or symbol             c - character             n - numeric             L - list (Ignores width and precision fields.)            P - point list (Ignores width and precision fields.)            B - Bounding box list (Ignores width and precision.)
```

The %L directive specifies the default format. This directive is a convenient way to intersperseapplication-specific formats with default formats. The `printf` function returns `t`. For more information on directives, see [Formatted Output](chap7.html#1008492 "I/O and File Handling").

```
aList = '(1 2 3) printf( "\nThis is a list: %L" aList ) => t This is a list: (1 2 3) aList = nil printf( "\nThis is a list: %L" aList ) => t This is a list: nil
```

If the conversion control directive is inappropriate for the data item,`printf` displays an error.

```
printf( "%d %d" 5 nil ) Message: *Error* fprintf/sprintf:       format spec. incompatible with data - nil
```

### Writing Data to a File

To write text data to a file

* Use the`outfile` function to obtain an output port on a file.

* Use an optional output port parameter to the`print` and `println` functions
  and/or use a required port parameter to the `fprintf` function.

* Close the output port with the`close` function.

Both`print` and `println` accept an optional second argument, which should be an output port associated with the target file. Use the `outfile` function to obtain an output port for a file. Once you are finished writing data to the file, use the `close` function to release the port. The following code

```
myPort = outfile( "/tmp/myFile" ) for( i 1 3       println( list( "Number:" i) myPort )       ) close( myPort )
```

writes this data to the file`/tmp/myFile`.

`("Number:" 1) ("Number:" 2) ("Number:" 3)`

Notice how SKILL displays a port:

`myPort = outfile( "/tmp/myFile" )port:"/tmp/myFile"`

Use a full path with the`outfile` function. Keep in mind that `outfile` returns `nil` if you don't have write access to the file or if it can't be created in the directory specified in the path. The `print` and `println` functions display an error if the port argument is `nil`. Notice that the type template uses a `p` character to indicate a port is expected.

```
println( "Hello" nil ) Message: *Error* println: argument #2 should be an I/O port       (type template = "gp") - nil
```

Unlike the`print` and `println` functions, the `printf` function does `not` accept an optional port argument. Use the `fprintf` function to write formatted data to a file. Its first argument should be an output port associated with the file. The following code

```
myPort = outfile( "/tmp/myFile" ) for( i 1 3       fprintf( myPort "Number: %d\n" i )       ) close( myPort )
```

writes this data to the file`/tmp/myFile`.

`Number: 1 Number: 2 Number: 3`

### Reading Data from a File

To read a text file

* Use the`infile` function to obtain an input port.

* Use the`gets` function to read the file a line at a time and/or
  use the `fscanf` function to convert text fields upon input.

* Close the input port with the`close` function.

Use the`infile` function to obtain an input port on a file. The `gets` function reads the next line from the file. This example prints every line in the
`~/.cshrc` file.

```
inPort = infile( "~/.cshrc" ) when( inPort       while( gets( nextLine inPort )             println( nextLine )       )       close( inPort ) )
```

The`fscanf` function reads data from a file according to format directives. This example prints every word in `~/.cshrc`.

```
inPort = infile( "~/.cshrc" ) when( inPort       while( fscanf( inPort "%s" word )             println( word )       )       close( inPort ) )
```

The`gets` function reads the next line from the file. The arguments of `gets` are the variable that will receive the next line and the input port. `gets` returns the text string or `nil` when the end of file is reached.

The`fscanf` function reads data from a file according to conversion control directives. The arguments of `fscanf` are

* Input port

* Conversion control string

* Variable(s) that will receive the matching data values

`fscanf` returns the number of data items matched.Format directives commonly found include the following.

**Some Common Format Directives**

| **Format Specification** | **Data Type** | **Scans Input Port**
| %d | integer | for next integer
| %f | floating point | for next floating point
| %s | text string | for next text string
| %e | floating point | for next floating point
| %g | floating point | for next floating point
For common output format specifications, see[Formatted Output](chap7.html#1008492 "I/O and File Handling").

Flow of Control
---------------

This section introduces you to

* Relational Operators: <, <=, >, >=, ==, !=

* Logical Operators: !, &&, |
* Branching: if, when, unless

* Multi-way Branching: case

* Iteration: for, foreach

Iteration refers to repeatedly executing a collection of SKILL expressions by changing -usually incrementing or decrementing - the value of one or more loop variables.

### Relational Operators

Use the following operators to compare data values. SKILL generates an error if the datatypes are inappropriate. These operators all return `t` or `nil`.

**Sample Relational Operators**

| **Operator** | **Arguments** | **Function** | **Example** | **Return Value**
| < | numeric | lessp | 3 < 5 3 < 2 | t nil
| <= | numeric | leqp | 3 <= 4 | t
| > | numeric | greaterp | 5 > 3 | t
| >= | numeric | geqp | 4 >=3 | t
| == | numeric string list | equal | 3.0 == 3 "abc" == "ABc" | t  nil
| != | numeric string list | nequal | "abc" != "ABc" | t
It is helpful to know the function name because error messages mention the function(`greaterp` below) instead of the operator ( > ).

`1 > "abc" Message: *Error* greaterp: can't handle (1 > "abc")`

### Logical Operators

SKILL considers`nil` as FALSE and any other value as TRUE. The and (&&) and or (||) operators only evaluate their second argument if they need to determine the return result.

**Sample Logical Operators**

| **Operator** | **Arguments** | **Function** | **Example** | **Return Value**
| && | general | and | 3 && 5 5 && 3 t && nil nil && t | 5 3 nil nil
| || | general | or | 3 || 5 5 || 3 t || nil nil || t | 3 5 t t
The && and || operators return the value last computed. Consequently, both && and ||operators can be used to avoid cumbersome `if` or `when` expressions.

#### Using &&

When SKILL creates a variable, it gives the variable a value of`unbound` to indicate that the variable has not been initialized yet. Use the `boundp` function to determine whether a variable is `bound`. The `boundp` function

* Returns`t` if the variable is bound to a value.

* Returns`nil` if it is not bound to a value.

Suppose you want to return the value of a variable`trMessages`. If `trMessages` is `unbound`, retrieving the value causes an error. Instead, use the expression

`boundp( 'trMessages ) && trMessages`

#### Using |
Suppose you have a default name, such as`noName`. Suppose you have a variable, such as `userName`. To use the default name if `userName` is `nil`, use the following expression

`userName || "noName"`

### The if Function

Use the`if` function to selectively evaluate two groups of one or more expressions. The condition in an `if` expression evaluates to `nil` or non-`nil`. The return value of the `if` expression is the value last computed.

```
if( shapeType == "rect"       then             println( "Shape is a rectangle" )             ++rectCount       else            println( "Shape is not a rectangle" )             ++miscCount       )
```

SKILL does most of its error checking during execution. Error messages involving`if` expressions can be obscure. Be sure to

* Be aware of the placement of the parentheses:`if( … then … else … )`.

* Avoid white space immediately after the`if` keyword.

* Use`then` and `else` when appropriate to your logic.

Consider the error message when you accidentally put white space after the`if` keyword.

```
shapeType = "rect" if ( shapeType == "rect"       then             println( "Shape is a rectangle" )             ++rectCount       else             println( "Shape is not a rectangle" )             ++miscCount       )Message: *Error* if: too few arguments (at least 2 expected, 1 given)…
```

Consider the error message when you accidentally drop the`then` keyword, but include an `else` keyword, and the condition returns `nil`.

```
shapeType = "label" if( shapeType == "rect"             println( "Shape is a rectangle" )             ++rectCount       else             println( "Shape is not a rectangle" )             ++miscCount       ) Message: *Error* if: too many arguments …
```

### The when and unless Functions

Use the`when` function whenever you have only `then` expressions.

```
when( shapeType == "rect"            println( "Shape is a rectangle" )            ++rectCount       ) ; whenwhen( shapeType == "ellipse"      println( "Shape is an ellipse" )      ++ellipseCount       ) ; when
```

Use the`unless` function to avoid negating a condition. Some users find this less confusing.

```
unless( shapeType == "rect" || shapeType == "line"      println( "Shape is miscellaneous" )      ++miscCount       ) ; unless
```

The`when`and `unless` functions both return the last value evaluated within their body or `nil`.

### The case Function

The`case` function offers branching based on a numeric or string value.

```
case( shapeType       ( "rect"             ++rectCount             println( "Shape is a rectangle" )             )       ( "line"            ++lineCount             println( "Shape is a line" )             )       ( "label"             ++labelCount             println( "Shape is a label" )             )       ( t             ++miscCount             println( "Shape is miscellaneous" )             )       ) ; case
```

The optional value`t` acts as a -all and should be handled last. The `case` function returns the value of the last expression evaluated. In this example:

* The value of the variable`shapeType` is compared against the values `rect`, `line`, and `label.`If SKILL finds a match, the several expressions in that arm are evaluated.

* If no match is found, the final arm is evaluated.

* When an arm's target value is actually a list, SKILL searches the list for the candidatevalue. If SKILL finds the candidate value, all the expressions in the arm are evaluated.

> ```
> case( shapeType       ( "rect"             ++rectCount             println( "Shape is a rectangle" )             )       ( ( "label" "line" )             ++labelOrLineCount             println( "Shape is a line or a label" )             )       ( t             ++miscCount             println( "Shape is miscellaneous" )             )       ) ; case
> ```

### The for Function

The index in a`for` expression is saved before the `for` loop and is restored to its saved value after the `for` loop is exited. SKILL does most of its error checking during execution. Error messages involving `for` expressions can be obscure. Be sure to

* Be aware of the placement of the parentheses:`for( … )`.

* Avoid white space immediately after the`for` keyword.

The example below adds the integers from one to five to an intermediate`sum`. `i` is a variable used as a counter for the loop and as the value to add to `sum`. Counting begins with one and ends with the completion of the fifth loop. `i` increases by one for each iteration through the loop.

`sum = 0 for( i 1 5       sum = sum + i       println( sum )      )=> t`

SKILL prints the value of`sum` with a carriage return for each pass through the loop:

`1361015`

The`for` function always returns `t`.

### The foreach Function

The`foreach` function is very useful for performing operations on each element in a list. Use the `foreach` function to evaluate one or more expressions for each element of a list of values.

```
rectCount = lineCount = polygonCount = 0 shapeTypeList = '( "rect" "polygon" "rect" "line" ) foreach( shapeType shapeTypeList       case( shapeType             ( "rect"             ++rectCount )             ( "line"             ++lineCount )             ( "polygon"          ++polygonCount )             ( t                  ++miscCount )             ) ;case       ) ; foreach => ( "rect" "polygon" "rect" "line" )
```

When evaluating a`foreach` expression, SKILL determines the list of values and repeatedly assigns successive elements to the index variable, evaluating each expression in the `foreach` body. The `foreach` expression returns the list of values over which it iterates.

In the example:

* The variable`shapeType` is the index variable. Before entering the `foreach` loop, SKILL saves the current value of `shapeType`. SKILL restores the saved value after completing the `foreach` loop.

* The variable`shapeTypeList` contains the list of values. SKILL successively assigns the values in `shapeTypeList` to `shapeType`, evaluating the body of the `foreach` loop once for each separate value.

* The body of the`foreach` loop is a single case expression.

* The return value of the`foreach` loop is the list contained in variable `shapeTypeList`.

If you have executed the example above, you can examine the effect of the iterations by typingthe name of the counter:

`rectCount        => 2lineCount        => 1polygonCount     => 1`

Developing a SKILL Function
---------------------------

Developing a SKILL function includes the following tasks.

* Grouping several SKILL statements into a single SKILL statement

* Declaring a SKILL function with the`procedure` function

* Defining function parameters

* Maintaining your source code

* Loading your SKILL source code

* Redefining a SKILL function

### Grouping SKILL Statements

Sometimes it is convenient to group several SKILL statements into a single SKILL statement.Use braces { and } to group a collection of SKILL statements into a single SKILL statement. The return value of the single statement is the return value of the last SKILL statement in the group. You can assign this return value to a variable.

This example computes the pixel height of`bBox` and assigns it to the `bBoxHeight` variable:

```
bBoxHeight = {       bBox = list( 100:150 250:400)      ll = car( bBox )      ur = cadr( bBox )      lly = yCoord( ll )      ury = yCoord( ur )      ury - lly }
```

* The`ll` and `ur` variables hold the lower-left and upper-right coordinates of the bounding box.

* The`xCoord` and `yCoord` functions return the `x` and `y` coordinate of a point.

* The`ury - lly`expression computes the height. This last statement in the group determines the return value of the group.

* The return value is assigned to the`bBoxHeight` variable.

You can declare the variables`ll, ur, ury`, and `lly` to be local variables. Use the `prog` or `let` functions to define a collection of local variables for a group of several statements. However, defining local variables is not recommended for novices.

### Declaring a SKILL Function

To refer to the group of statements by name, use the`procedure` declaration to associate a name with the group. The group of statements and the name make up a SKILL function.

* The name is known as the function name.

* The group of statements is the function body.

* To execute the group of statements, mention the function name followed immediately by( ).

The`ComputeBBoxHeight` function example below computes the pixel height of `bBox`.

```
procedure( ComputeBBoxHeight( )       bBox = list( 100:150 250:400)      ll       = car( bBox )      ur       = cadr( bBox )      lly      = yCoord( ll )      ury      = yCoord( ur )      ury - lly       ) ; procedurebBoxHeight = ComputeBBoxHeight()
```

### Defining Function Parameters

To make your function more versatile, you can identify certain variables in the function bodyas formal parameters.

When you invoke your function, you supply a parameter value for each formal parameter.

In the following example, the`bBox` is the parameter.

```
procedure( ComputeBBoxHeight( bBox )       ll       = car( bBox )      ur       = cadr( bBox )      lly      = yCoord( ll )      ury      = yCoord( ur )      ury - lly       ) ; procedure
```

To execute your function, you must provide a value for the parameter.

`bBox = list( 100:150 250:400)bBoxHeight = ComputeBBoxHeight( bBox )`

### Selecting Prefixes for Your Functions

With only a few exceptions, the SKILL functions in this manual do not use a prefix identifier.Many examples in this manual use a "tr" prefix to indicate they are created for training purposes. If you look in other SKILL manuals, you will notice that functions for tools are usually grouped with identifiable, unique prefixes.

For example, functions used for technology file administration are all prefixed with "tc". Theseprefixes vary across Cadence tools, but all use lowercase letters. It is recommended that you establish a unique prefix using uppercase letters for your own functions.

### Maintaining SKILL Source Code

The Cadence environment makes it easy to invoke an editor of your choice. Set the SKILLvariable `editor` to a UNIX command line able to launch your editor.

`editor = "xterm -e vi"`

The`ed` function invokes an editor of your choice. If you optionally use the `edl` function, the system loads your file when you quit the editor.

`ed( "myFile.il")`

Alternatively, you can use an editor independent of the Cadence environment.

### Loading Your SKILL Source Code

The`load` function

* Evaluates each expression in a source code file]

* Is typically used to define a collection of functions

* Returns`t` if all expressions evaluate without errors

* Aborts if there are any errors, any expression following the offending expression is notevaluated

**Note:** If an error occurs while loading the source code, an error message displays listing theline number on which the error occured.

#### Giving a Relative Path

When you pass a relative path to the`load` function, the system resolves it in terms of a list of directories called the SKILL path. You usually establish the SKILL path in your initialization file by using the `setSkillPath` or `getSkillPath` functions.

* The`setSkillPath` function sets the path to a list of directories.

* The`getSkillPath` function returns a list of directories in search order.

#### Entering a Function

Sometimes you need to define a function without saving the source code file. Using themouse in your editor, select and paste the function into the command input line.

#### Setting the SKILL Path

Use the`setSkillPath` function in conjunction with the `prependInstallPath` and `getSkillPath` functions to set the SKILL path.

```
trSamplesPath = list(            prependInstallPath( "etc/context" )            prependInstallPath( "local" )            prependInstallPath( "samples/local" )            )
```

Use the`prependInstallPath` function to make a path relative to the installation directory. The function prepends `your_install_dir``/tools/dfII` to the path. Assuming your installation path is `/cds/9401 trSamplesPath` is now:

```
("/cds/9401/tools.sun4/dfII/etc/context"  "/cds/9401/tools.sun4/dfII/local"  "/cds/9401/tools.sun4/dfII/samples/local")
```

Assuming your SKILL path is ("." "~"), you can set a new SKILL path using`setSkillPath`.

`setSkillPath( append( trSamplesPath getSkillPath() ) )`

The return value of`setSkillPath` indicates a path that could not be located, not the actual SKILL path.

`("/cds/9401/tools.sun4/dfII/samples/local")`

The actual SKILL path is

```
("/cds/9401/tools.sun4/dfII/etc/context"  "/cds/9401/tools.sun4/dfII/local"  "/cds/9401/tools.sun4/dfII/samples/local" "." "~")
```

For more information on the SKILL path, see[Directory Paths](chap7.html#1008214 "I/O and File Handling").

### Redefining a SKILL Function

Users should be safeguarded against inadvertently redefining functions. Yet, whiledeveloping SKILL code, you often need to redefine functions.

The SKILL interpreter has an internal switch called`writeProtect` to prevent the virtual memory definition of a function from being altered during a session.

By default`writeProtect` is set to `nil`. SKILL functions defined while `writeProtect` is `t` cannot be redefined during the same session. Typically, you set the `writeProtect` switch in your initialization file.

```
sstatus( writeProtect t )        ;sets it to tsstatus( writeProtect nil )      ;sets it to nil
```

This example tries to redefine`trReciprocal` to prevent division by 0.

```
sstatus( writeProtect t ) => tprocedure( trReciprocal( x ) 1.0 / x ) => trReciprocalprocedure( trReciprocal( x ) when( x != 0.0 1.0 / x ))*Error* def: function name is write protected      and cannot be redefined - trReciprocal
```




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
