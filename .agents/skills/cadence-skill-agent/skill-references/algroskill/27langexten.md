### axldo

`axldo( g_initList g_terminateList [g_body] ) => g_result`

#### Description

A do function, modeled after the CL (Common Lisp) do.

`Public: (defmacro do ((var [init [step]]) ...) (end-test result result ...) @body) (defmacro doStar ((var [init [step]]) ...) (end-test result result ...)` The do macro provdes a generalized iteration facility, with an arbitrary number of index variables. These variables are bound within the iteration and stepped in specified ways. They may be used both to generate successive values of interest or to accumulate results. When an end condition is met (as specified by end-test), the iteration terminates, the result sexps are successive evaluated, and the value of the last result sexp is returned.

The first item in the form is a list of 0 or more index-variable specifiers. Each index-variable specifier is a list of the name of the variable, `var`; an initial value, `init`; and a stepping form, `step`.

If `init` is omitted, it defaults to nil. If `step` is omitted, the `var` is not changed by the do construct between repetitions (though code within the do is free to alter the value of the variable by using `setq`).

An index-variable specified can also be just the name of a variable. In this case, the variable has an initial value of nil and is not changed betgween repetitions. This would be used much as a locally scoped variable in a let statement would be.

Before the first iteration, all the init forms are evaluated, and each var is bound to the value of its respective init. Because this is a binding, and not an assignment, when the loop termintes the old values of the variables is restored. All of the init forms are evaluated before any var is bound; hence all the init forms may refer to the old bindins of all the variables (that is, to the values visible BEFORE beginning execution of the do).

Note: All init bindings are done in parallel for `axldo`, and serially for `axldoStar`.

The second element of the loop is a list of an end-testing predicate form end-test, and zero or more result forms. This resembles a conditional clause. At the beginning of each iteration, after processing the variables, the end-test is evaluated. If the result is nil, execution proceeds with the body of the form. If the result is non-nil, the result forms are evaluated in order as an implicit prog, and then the do returns the value of the last evaluated result.

At the beginning of each iteration, the index variables are updated as follows.

- All the step forms are evaluated, from left to right, and the resulting values are assigned to the respective index variables. Any variable that has no step value is not assigned.

#### Arguments

| Name | Description |
|---|---|
| `g_initList` | 0 or more index variable specifiers |
| `g_termiateList` | end test predicate |
| `g_body` | body of procedure |

#### Value Returns

Value resulting from evaluating last result sexp.

#### See Also

letStar

### copyDeep

`copyDeep( l_object ) => l_newObject`

#### Description

This function recursively copy a list.

The copy function makes a new list containing copies of all top level elements in the source list. But each new element contains references to the same sublist elements as the source list. Thus, if sublist items are modified in the source list they are also modified in the copy, and vice-versa. The copyDeep function makes a complete copy of the list, top to bottom. So changes in one list do not affect the other. This allocates more memory, of course.

#### Arguments

| Name | Description |
|---|---|
| `l_object` | The list to be copied |

#### Value Returns

A new list identical to the orginal but sharing no memory.

### isBoxp

`isBoxp( g_bBox ) => t/nil`

#### Description

Checks argument to see if it is a valid bounding box. A valid bounding box should be of the form of `((a b) (c d))` where `a`, `b`, `c`, and `d` are all numbers and `a!= c` and `b!= d`, to ensure that the bounding box encloses some area.

#### Arguments

| Name | Description |
|---|---|
| `g_bBox` | input argument to be tested. |

#### Value Returns

`t`: If g_bBox is a valid bounding box.

`nil`: If g_bBox is not a valid bounding box.

### lastelem

`lastelem( l_list ) => g_elem`

#### Description

The `last()` function returns the last LIST object in a list, but `lastelem()` takes the car of that to get the last ATOM.

#### Arguments

| Name | Description |
|---|---|
| `l_list` | a list |

#### Value Returns

The last atom element of a list.

### letStar

`letStar( l_bindings [@body] ) => g_lastValue`

#### Description

`l = list(1 2 3) last(l) -> (3) lastelem(l) -> 3` This is a let* implementation of CL (Common Lisp).This is a mprocedure function.

#### Arguments

| Name | Description |
|---|---|
| `l_bindings` | list of l_varbind<br><br>`l_varbind`; is (<name> <value>) `name:`interned as lexically-scoped symbol `value:`evaluated to arrive at value |
| `@body` | one or more expressions to be evaluated. |

#### Value Returns

last value of `@body`

#### See Also

axldo

### listnindex

`listnindex( l_theList g_item ) => x_found/nil`

#### Description

Finds the position of an item in a list. Works just like `nindex`, but finds the position of an element in a list instead of a character in a string. An integer denoting the sequence number of the first matching element is determined.

#### Arguments

| Name | Description |
|---|---|
| `l_theList` | A list containing the element to be found |
| `g_item` | The element to be found |

#### Value Returns

The position in the list where the element was first found, or `nil` if it is not found.

Note: x_found is 0 based so you use other Skill functions like nth

### movedown

`movedown( g_elem l_list ) => l_newlist`

#### Description

movedown - move an element one item farther from the head of a list

`listnindex( '("three" "dog" 'night) "dog") -> 1` Find all occurences of element within list `l` and move them one item closer to the list tail. No action for other items and the last element of the list.

This destructively modifies the list.

#### Arguments

| Name | Description |
|---|---|
| `g_elem` | The element to be moved, matched using (equal) |
| `l_list` | The list containing the element to be moved. |

#### Value Returns

The modified list.

### moveup

`moveup( g_elem l_list ) => l_newlist`

#### Description

Moves an element one item closer to the head of a list. Finds all occurences of the element within list `l` and moves them one item closer to the list head. No action for other items and the car.

This destructively modifies the list.

#### Arguments

| Name | Description |
|---|---|
| `g_elem` | The element to be moved, matched using (equal) |
| `l_list` | The list containing the element to be moved. |

#### Value Returns

The modified list.

### parseFile

`parseFile ( t_fileName s_handler [t_breakChars] ) => g_result`

#### Description

Parse all lines of a file. Opens input file and reads it line by line. Each line is parsed using `parseQuotedString`. The result of parseQuotedString is passed to the application defined handler `s_handler`. The handler defines the return value.

#### Arguments

| Name | Description |
|---|---|
| `t_fileName` | Name of file to be read. |
| `s_handler` | Application callback function to process parsed arguments `s_handler ( l_curLineInfo l_lineArgs g_result ) ==> g_result`<br><br>`l_curLineInfo`; List of info which describes the current line being processed.
 Defined as: `(t_fileName g_lineNo t_curString) t_fileName:`Name of file being read `g_lineNo:`Current line number `t_curString:`Unparsed file line<br><br>`l_lineArgs`; List of strings that result from parsing the line.<br><br>`g_result`; The application callback result. This is continually passed to s_handler so that a reult can be built up from the processing of all file lines. This will be nil the first time and will be whatever s_handler last returned for subsequent calls. |
| `t_breakChars` | Optional string containing characters that are used as break characters. The default is `"'\" "` (quote chars and space char). |

#### Value Returns

`g_result` The application callback result from the last call to `s_handler`.

### parseQuotedString

`parseQuotedString( t_string [t_breakCharacters] ) => l_strings`

#### Description

Breaks a string into a list of words. Multiple words enclosed within quotation marks are treated as single words.

#### Arguments

| Name | Description |
|---|---|
| `t_string` | String to be parsed. |
| `t_breakCharacters` | Optional string containing characters to be used as break characters. The default is `"'\" "` (quote chars and space char). |

#### Value Returns

| Name | Description |
|---|---|
| `l_strings` | A list of strings parsed from the `t_string` argument. |

Note: A word break is not created at the start of a quote unless the quote character is a break character.

#### Examples

- `parseQuotedString( "111 222'333 444'" " ")` => ("111" "222333 444")

- `parseQuotedString( "111 222'333 444'" "' ")` => ("111" "222" "333 444")

### pprintln

`pprintln( g_item [p_port] ) => t/nil`

#### Description

Prints a newline charanter at the end of the line.

#### Arguments

| Name | Description |
|---|---|
| `g_item` | The item to be printed. |
| `p_port` | The optional parameter that specifies the port to write to. Default value is stdout. |

#### Value Returns

Returns item pretty printed plus a newline character.

### propNames

`propNames( g_propList ) => lS_names/nil`

#### Description

Use this command to get the names of properties in a disembodied property list. Walk each property in disembodied property list, building a list of the names of each property.

Note: Order of returned property names is unspecified.

#### Arguments

| Name | Description |
|---|---|
| `g_propList` | A disembodied property list. |

#### Value Returns

| Name | Description |
|---|---|
| `lS_names` | A list of symbols corresponding to the names of each property found in the list. |

#### Examples

`n = ncons(nil) n->one = 1 n->two = 2 propNames(n) -> (one two)`

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

