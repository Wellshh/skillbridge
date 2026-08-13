### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

12
==

Core Functions
==============

### arglist

`arglist( g_function ) => l_argumentList`

#### Description

Returns the number and types of arguments expected for a function. Also checks if thespecified function is a binary object,

This function is useful for determining how many arguments a function takes and what theyare.

If the function is read-protected, the arguments are still returned. If the function is a primitive(binary), the argument list is based on the type template for the function specified. If the function is defined in SKILL, the argument list in the function definition is returned.

#### Arguments

|  |
| --- | ---
| `g_function` | Name of the function or the symbol whose argument list youwant to see.
#### Value Returned

|  |
| --- | ---
| `l_argumentList` | Number and types of arguments for `g_function`.
#### Example

`arglist('rexMatchp) => ( t_string S_stringSymbol "tS")`

The first argument of`rexMatchp` must be a string and the second must be a string or symbol.

### assert

`assert( g_expression ) => nil`

#### Description

Enables you to insert assertions into the SKILL code, either at the top-level or within afunction. It evaluates the expression (`g_expression`) and returns `nil` if the expression value is non-nil. Otherwise, throws an error and returns the unevaluated expression.

#### Arguments

|  |
| --- | ---
| `g_expression` | A generic expression.
#### Value Returned

|  |
| --- | ---
| `nil` | Assertion is successful.
| g\_expression | Assertion failed.
#### Example

`assert(1 == 1)`

`=>nil`

### atom

`atom( g_arg ) => t | nil`

#### Description

Checks if an object is an atom.

*Atoms* are all SKILL objects except non-empty lists. The special symbol `nil` is both an atom and a list.

#### Arguments

|  |
| --- | ---
| `g_arg` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_arg` is an atom.
|  |
| --- | ---
| `nil` | If`g_arg` is not an atom.
#### Example

`atom( 'hello )  => t`

`x = '(a b c)atom( x )       => nil`

`atom( nil )     => t`

### bcdp

`bcdp( g_value ) => t | nil`

#### Description

Checks if an object is a binary primitive function.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | Object to check.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is a binary function.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`bcdp(getd('plus)) => tbcdp('plus) => nil`

### booleanp

`booleanp( g_obj ) => t | nil`

#### Description

Checks if an object is a boolean. Returns`t` if the object is `t` or `nil`. Returns `nil` otherwise.

#### Arguments

|  |
| --- | ---
| `g_obj` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_obj` is either `t` or `nil`.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

(booleanp 0 ) => nil
(booleanp nil) => t
(booleanp t) => t

### boundp

`boundp( s_arg [ e_environment ] ) => t | nil`

#### Description

Checks if the variable named by a symbol is bound, that is, has been assigned a value. Thesingle argument form of `boundp` only works in SKILL mode.

Remember that a variable can be set to the special symbol`unbound`.

**Note:** `boundp()` does not check the current language mode. If single argument is specified, SKILL semantics are used, whereas if two arguments are specified, SKILL++ semantics are used.

#### Arguments

|  |
| --- | ---
| `s_arg` | Symbol to be tested to see if it is bound.
|  |
| --- | ---
| `e_environment` | If this argument is given, SKILL++ semantics are used. Thesymbol will be searched for within the given (lexical) environment.
#### Value Returned

|  |
| --- | ---
| `t` | If the symbol`s_arg` has been assigned a value.
|  |
| --- | ---
| `nil` | If the symbol`s_arg` has not been assigned a value.
#### Example

`x = 5                ; Binds x to the value 5.y = 'unbound         ; Unbind y`

`boundp( 'x )=> t`

`boundp( 'y )=> nil`

y = 'x               ; Bind y to the constant x.
boundp( y )
=> t                 ; Returns t because y evaluates to x,
                     ; which is bound.

### gc

`gc( [ t_string ] ) => nil`

#### Description

Forces a garbage collection. This function is also called by the system.

Garbage collection (`gc`) refers to the process in which SKILL locates storage cells that are no longer needed (thus the term garbage) and recycles them by putting them back on the free storage list. Garbage collection is also called by the system. Garbage collection is transparent to SKILL users and to users of applications built on top of SKILL.

You can turn on the printing of garbage collection messages by setting the`_gcprint` variable to `t` (that is, `_gcprint=t`). Garbage collection can be turned off at any time by setting the `gcdisable` variable to `t`. To enable garbage collection again, you can restore `gcdisable` to its previous value. You can force a garbage collection at any time by calling the `gc` function.

* ***Because some applications turn off garbage collection during theirexecution, you should be careful about enabling it. Corrupted data can result.***

#### Arguments

|  |
| --- | ---
| `t_string` | File into which additional information is dumped.
#### Value Returned

|  |
| --- | ---
| `nil` | Always returns`nil`.
#### Example

`gc( ) => nil`

#### Reference

`gc``summary`,

### gensym

`gensym( [ S_arg ] ) => s_result`

#### Description

Returns a new symbol based on the input argument.

The new symbol's print name is the result of concatenating the printed representation of theargument, or "G" if no argument is given, and the printed (decimal) representation of a number. The returned new symbol is unique in the sense that it does not exist at the time this function is called.

#### Arguments

|  |
| --- | ---
| `S_arg` | String or symbol to be concatenated into a new symbol. If notsupplied, the default value is `G`.
#### Value Returned

|  |
| --- | ---
| `s_result` | New unique symbol.
#### Example

```
gensym()                 => G5gensym("test")           => test6test7 = 10               => 10      ;test7 exists now.gensym('test)            => test8   ;test7 is skipped.gensym() == gensym()     => nil     ;Always returns nil.
```

### getSkillVersion

`getSkillVersion( [g_printSubVersion]) => t_version`

#### Description

Returns the major version if the argument is left`blank`; otherwise, returns the current subversion (or tarkit version) of SKILL that is running in the build

#### Arguments

|  |
| --- | ---
| `g_printSubVersion` | (Optional) Specify a flag to print the current subversion (or tarkitversion) of SKILL running in the build
#### Value Returned

|  |
| --- | ---
| `t_version` | If the argument flag is left`blank`, returns the major version of SKILL running in the build. If the argument flag is specified, returns the current subversion (tarkit version) of SKILL running in the build
#### Example

`getSkillVersion()=> "SKILL04.20"`

getSkillVersion(t)
"@(#)$CDS: il skillSrc33.12-d009 08/31/11 14:50 fwinteg sjfdl803 $"

### get\_pname

`get_pname( s_arg ) => t_result`

#### Description

Returns the print name of a symbol as a string.

This function is useful for converting symbols to strings. If you just want to print the name ofa symbol, you do *not* need to use this function. This function is equivalent to `symbolToString`.

#### Arguments

|  |
| --- | ---
| `s_arg` | A symbol.
#### Value Returned

|  |
| --- | ---
| `t_result` | Print name of the symbol.
#### Example

```
get_pname( 'a )                  => "a"get_pname(concat("Cell_" 123))   => "Cell_123"
```

#### Reference

`get_string`

### get\_string

`get_string( S_arg ) => t_result`

#### Description

Converts the argument to a string if it is a symbol. Otherwise it returns the string itself.

#### Arguments

|  |
| --- | ---
| `S_arg` | String or symbol.
#### Value Returned

|  |
| --- | ---
| `t_result` | Of the argument is a string, returns the argument itself. If theargument is a symbol, returns the print name as a string.
#### Example

`get_string('xyz)    => "xyz"get_string("xyz")   => "xyz"`

#### Reference

[get\_pname](#1038993 "Core Functions")

### getVersion

`getVersion( [ g_opt ] ) => t_[sub]version`

#### Description

Returns the version number of the Cadence software you are currently using. If you specifythe optional argument `g_opt,` as `t` (or a non-nil value), the subversion number of the Cadence software currently used is returned. By default, the full version number, including the hotfix version, of the Cadence software currently used is returned.

Use the SKILL system structure to determine the bitType (32bit / 64bit) of the current Virtuososession:

`system.LP64`

`=> nil ;; 32bit`

`=> t ;; 64bit`

or

`system.system.ILP32`

`=> nil ;; 64bit`

`=> t ;; 32bit`

These`system.??` properties are initialized at startup.

#### Arguments

|  |
| --- | ---
| `g_opt` | Optional argument.
|  |
| --- | ---
|  | If the optional argument,`g_opt`, is specified as `t` (or a non-nil value), the subversion number of the Cadence software currently used is returned. By default, the full version number, including the hotfix version, of the Cadence software currently used is returned.
#### Value Returned

|  |
| --- | ---
| `t_[sub]version` | String identifying the version/subversion of the program you arerunning.
#### Example

```
getVersion() => "@(#)$CDS: virtuoso version 6.1.6 07/24/2012 11:02 (cic612sun) $"
```

```
getVersion(nil) => "@(#)$CDS: virtuoso version 6.1.6 07/24/2012 11:02 (cic612sun) $"
```

`getVersion( 'subVer ) => "sub-version IC6.1.6.DEL.410"`

`getVersion(t) => "sub-version IC6.1.6.DEL.410 "`

`getVersion("subversion") => "sub-version IC6.1.6.DEL.410 "`

#### Reference

[dbGetVersion](../skdfref/chap2.html#dbGetVersion)

### getWarn

`getWarn( ) => t_warning`

#### Description

Returns the buffered warning if it has not already been printed.

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `t_warning` | The warning message that would have been printed if it had notbeen intercepted by the call to `getWarn`.
#### Example

```
procedure( testWarn( @key ( getLastWarn nil ) )    warn("This is warning %d\n" 1 ) ;;; print previous warning    warn("This is warning %d\n" 2 ) ;;; and buffer new one.    warn("This is warning %d\n" 3 )    when( getLastWarn         thrownAwayWarn = getWarn( ) ;;; throw away last warning        nil                         ;;; return nil        )                           ; when    )                               ; procedure
```

The`testWarn` function intercepts the last warning message and stores it in a global variable if `t` is passed in, and lets the system print all the warnings if `nil` is given as an argument. Use of the getWarn( ) function makes it possible to throw away a warning message, if desired.

```
testWarn( ?getLastWarn t)=> nil*WARNING* This is warning 1*WARNING* This is warning 2
```

Returns`nil.`The system prints the first two warnings and the third is intercepted and stored in global variable `thrownAwayWarn`.

```
testWarn( ?getLastWarn nil) => nil*WARNING* This is warning 1*WARNING* This is warning 2*WARNING* This is warning 3
```

Returns`nil`. The system prints all the queued warnings.

Note that the return value may be interleaved with the warning message output. The followingexample shows how the actual output can appear in the CIW.

```
testWarn( ?getLastWarn t)*WARNING* This is warning 1*WARNING* This is warning 2=> nil
```

```
testWarn( ?getLastWarn nil)*WARNING* This is warning 1*WARNING* This is warning 2=> nil*WARNING* This is warning 3
```

### help

`help( [ S_name ] ) => t | nil`

#### Description

Retrieves and prints the cdsFinder documentation strings for the given function name (asymbol). If the given name is a string, it is interpreted as a regular expression, and the entire cdsFinder database is searched for functions whose name or documentation string contains or matches the given string. Help is an `nlambda` function.

#### Arguments

|  |
| --- | ---
| `S_name` | Name to search for.
#### Value Returned

|  |
| --- | ---
| `t` | The given function name is found in the cdsFinder.
|  |
| --- | ---
| `nil` | No match is found for`S_name`.
#### Example

`help nonexist`

`=> nil`

`help scanf`

Prints the following and returns`t`.

`fscanf( p_inputPort t_formatString [s_var1 ...] )`

`scanf( t_formatString [s_var1 ...] )`

`sscanf( t_sourceString t_formatString [s_var1 ...] )`

The only difference between these functions is the source of input.`fscanf` reads input from a port according to format specifications and returns the number of items read in. `scanf` takes its input from piport implicitly. `scanf` only works in standalone SKILL when the piport is not the CIW. `sscanf` reads its input from a string instead of a port.

`=> t`

`help println`

Prints the following and returns`t`.

`println( g_value [p_outputPort] ) => nil`

Prints a SKILL object using the default format for the data type of the value, then prints anewline character.

`=> t`

`help "read"`

Prints the following and returns`t`.

```
fscanf, scanf, sscanf, getWarn, infile, instring, ipcReadProcess, ipcWaitForProcess, isReadable, lineread, linereadstring, load, loadstring, outfile, pp, putpropq, putpropqq, read, readTable, readstring
```

`=> t`

`help "match nowhere"`

=> nil

### inScheme

`inScheme( g_form ) => g_result`

#### Description

Evaluates a form as top-level SKILL++ code, disregarding the surrounding evaluation context.

#### Arguments

|  |
| --- | ---
| `g_form` | Form to be evaluated as top-level SKILL++ code.
#### Value Returned

|  |
| --- | ---
| `g_result` | Result of the evaluation.
#### Example

`(inScheme        (define myVar 100)) => myVar`

Defines a SKILL++ global variable, even if this code appears inside a SKILL file.

#### Reference

`inSkill`

### inSkill

`inSkill( g_form ) => g_result`

#### Description

Evaluates a form as top-level SKILL code, disregarding the surrounding evaluation context.

#### Arguments

|  |
| --- | ---
| `g_form` | Form to be evaluated as top-level SKILL code.
#### Value Returned

|  |
| --- | ---
| `g_result` | Result of the evaluation.
#### Example

`(inSkill        skillVar = 100) => 100`

Sets a SKILL global variable, even if this code appears inside a SKILL++ file.

### isVarImported

`isVarImported( s_var ) => t/nil`

#### Description

Checks if the specified variable was imported into SKILL++ or not.

#### Arguments

|  |
| --- | ---
| `s_var` | The variable to be checked.
#### Value Returned

|  |
| --- | ---
| `t` | The specified variable`s_var` was imported into SKILL++.
|  |
| --- | ---
| `nil` | Returns`nil`, if the given variable is not imported.
#### Example

`isVarImported('myvar)`

=> nil

### makeSymbol

`makeSymbol( S_createSymbol [ t_namespaceArg ]) => s_result`

#### Description

Creates a symbol corresponding to the specified symbol or character string. In IC6.1.6 andlater releases, optionally specify the namespace name (`t_namespace`) in which you want to create the symbol.

**Note:** The function`gensym()` also creates symbols. However, the symbol names are determined internally (and are therefore unique) whereas in the case of `makeSymbol()` the symbol name depends upon the string passed as a parameter to the function.

#### Arguments

|  |
| --- | ---
| `S_createSymbol` | Specifies the value for which a corresponding symbol needs tobe created.
|  |
| --- | ---
| `t_namespaceArg` | (Optional) Specifies the name of the namespace in which youwant to create the symbol.
#### Value Returned

|  |
| --- | ---
| `s_result` | Returns a symbol corresponding to the specifed string value.
#### Example 1

The following example creates a symbol corresponding to the specified string value,`myString`.

`makeSymbol("myString")=> myString`

#### Example 2

The following example usesd an increment counter (`count`) to create unique symbols (`myString1, myString2, and so on`)

`count=0`

`makeSymbol(strcat("myString" sprintf(nil "%L" ++count)))`

#### Example 3

The following example creates a symbol,`myString,` in the namespace, `newNamespace`.

`makeNamespace("newNamespace")`

`makeSymbol("myString" "newNamespace")`

`=> newNamespace:::myString`

### measureTime

`measureTime( g_expression ... ) => l_result`

#### Description

Measures the time needed to evaluate an expression and returns a list of four numbers. Thisis a syntax form.

* The first number is the amount of user CPU time in seconds devoted to the process.

* The second number is the amount of CPU time used by the kernel for the process.

* The third and most significant number is the total elapsed time it took to evaluate theexpression in seconds.

* The fourth number is the number of page faults that occurred during the evaluation of theexpression.

#### Arguments

|  |
| --- | ---
| `g_expression` | Expression(s) to be evaluated and timed.
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns the elapsed time and number of page faults to evaluate`g_expression`.
#### Example

```
myList = nil            ; Initializes the variable myList.measureTime( for( i 1 10000 myList = cons(i myList) ) )=> (0.4 0.05 0.4465 0)
```

Result indicates that it took .4 seconds and 0 page faults to build a list from 1 to 10,000 using`cons`.

```
myList = nil            ; Initializes the variable myList.measureTime( for( i 1 1000 myList = append1(myList i) ) )=> (5.04 0.03 5.06 0)
```

Result indicates that it took 5 seconds and 0 page faults to build a list from 1 to 1000 using`append1`.

### needNCells

`needNCells( {s_cellType | S_userType} x_cellCount )=> t | nil`

#### Description

Ensures that there is enough memory available for the specified number of SKILL objects(cells).

If necessary, more memory is allocated. The name of the user type can be passed in as astring or a symbol, however internal types like `list` or `fixnum` must be passed in as symbols.

#### Arguments

|  |
| --- | ---
| `s_cellType` | Objects of type`cellType`.
|  |
| --- | ---
| `S_userType` | Objects of type`userType`.
|  |
| --- | ---
| `x_cellCount` | Number of objects.
#### Value Returned

|  |
| --- | ---
| `t` | Enough memory is available.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`needNCells( 'list 1000 ) => t`

Guarantees there will always be 1000 list cells available in the system.

### restoreFloat

`restoreFloat( t_string ) => f_number`

#### Description

Restores a floating point number (`f_number`) from its serialized string (`t_string`) representation.

**Note:** `t_string` should be created by `saveFloat()`.

#### Arguments

|  |
| --- | ---
| `t_string` | A serialized float created by`ilSaveFloat()`.
#### Value Returned

|  |
| --- | ---
| `f_number` | The restored floating point number.
#### Example

`str = saveFloat(1.4106)`

`=> "float:3ff6a09e667f3bcd@3ff691d14e3bcd36"`

restoreFloat(str) == 1.4106

### saveFloat

`saveFloat( f_number ) => t_string`

#### Description

Serializes the given floating point number (`f_number`) to string (`t_string`).

#### Arguments

|  |
| --- | ---
| `f_number` | The floating point number that needs to be serialized.
#### Value Returned

|  |
| --- | ---
| `t_string` | The string representation of`f_number`.
#### Example

`str = saveFloat(1.4106)`

=> "float:3ff6a09e667f3bcd@3ff691d14e3bcd36"

### schemeTopLevelEnv

`schemeTopLevelEnv( ) => e_envobj`

#### Description

Returns the top level SKILL++ environment as an environment object.

#### Arguments

|  |
| --- | ---
| None. |
#### Value Returned

|  |
| --- | ---
| `e_envobj` | The top level SKILL++ environment object.
#### Example

`schemeTopLevelEnv() => envobj:0x1ad018`

### setPrompts

`setPrompts(s_prompt1s_prompt2)=> t | nil`

#### Description

Sets the prompt text string for the CIW. The first prompt is used to indicate the topmost top-level. The second prompt is used whenever a nested top-level is entered.

The text string for`s_prompt2` should always be the `%d` format string, which behaves the same as the `print`f() format string, such that the nesting level of a nested top-level will be shown as it deepens.

**Note:** Changing prompts in some applications can seriously interfere with their functioning;be very careful using this function.

#### Arguments

|  |
| --- | ---
| `s_prompt1` | Prompt text string.
| `s_prompt2` | Prompt text string.
#### Value Returned

|  |
| --- | ---
| `t` | The prompt has been set.
| `nil` | Returns`nil` and issues an error message if the prompt is not changed.
#### Example

```
> setPrompts("~> " "<%d>> ")t~> toplevel( 'ils )ILS-<2>> toplevel( 'ils )ILS-<3>>
```

Sets the topmost top-level to`~>` and the nested top-level to `<%d>>` :

```
> setPrompts("~> " "<%s>> ")*Error* setPrompts: setPrompts expected %d not %s in prompt --<%s>>
```

`%s` is an illegal format string.

### sstatus

`sstatus( s_name g_switchValue ) => g_switchValue`

#### Description

Sets the internal system variable named to a given value. This is a syntax form.

The internal variables are typically Boolean switches that accept only the Boolean values of`t` and `nil`. Efficiency and security are the reasons why these system variables are stored as internal variables that can only be set by `sstatus`, rather than as SKILL variables you can set directly.

#### Internal System Variables

|  |  |
| --- | --- | ---
| ****Name**** | Meaning | Default
| autoReload | Ift, the debugger will try to auto-reload a file that is not loaded under debugMode when the user tries to single step into the code defined by that file. Note: this may not work correctly for SKILL++ functions defined using assignment. | nil
| classContextAutoLoad | If t, sets the status function to allow class search in .aux files. | nil
| debugMode | Debug mode provides more information fordebugging SKILL programs. Allows you to redefine write-protected SKILL functions. | nil
| errsetTrace | Prints errors and stacktrace information that isnormally suppressed by errset. | nil
| fullPrecision | Ift, unformatted print functions (print, println, printlev) print floating point numbers in full precision (usually 16 digits); otherwise, the default is about 7 digits of precision. | nil
| integermode | When on (default is off), the parser translates allarithmetic operators into calls to functions that operate only on fixnums. This results in small execution time savings and makes sense only for compute-intensive tasks whose inner loops are dominated by integer arithmetic calculations. | nil
| mergemode | When on (default), arithmetic expressions aremerged by the parser whenever possible into a minimum number of function calls and therefore run somewhat faster because most of the arithmetic functions such as plus, difference, times, and quotient can accept a variable number of arguments. | `t`
| printinfix | Printing of arithmetic expressions and function callsin infix notation is turned off (on) if the second argument is nil (t). | `t`
| writeProtect | When on, all functions being defined have their writeprotection set to t so they cannot be redefined.  When off, all functions being defined for the first timeare not write-protected and thus can be redefined. When developing SKILL code, be sure this switch is set to off. | nil
| stacktraceDump | Prints the local variables when an error occurs ifsstatus( stacktrace t) is set. Toggle on/off with t / nil. | nil
| stacktrace | Prints stack frames every time an error occurs.Toggle on/off with t / nil, or set the number of frames to display. | 0
| sourceTracing | If t, the debugger will try to print out thecorresponding source location at stop/breakpoints (as well as in stack tracing).  A file must be loaded in when debugMode is set to tin order to get its source line numbers. The source forms printed are truncated to fit on one line. | nil
| traceArgs | If set to non-nil, the system will save the evaluated arguments of function calls, which can then be displayed in the stacktrace.  Setting debugMode or tracing functions (using tracef) will no longer turn on traceArgs automatically. The default behavior is to turn off this switch because it is very expensive to keep the evaluated arguments around all the time.  **Note:** Turning on this switch could slow down theexecution speed significantly. | nil
| profCount | If t, the SKILL Profiler provides the number of times a SKILL function is called (as an additional column in the table view of the profiler's result). | nil
| verboseLoad | If set to t, prints the complete path of the loaded filein CIW in debug mode. | nil
| showStepResult | If set to t, prints the expression evaluation resultsperformed by the step command in CIW. If SKILL IDE is also running, a new assistant window is displayed, which also displays the expression evaluation results. | nil
| optimizeNestedLet | If set to t, instructs the SKILL compiler to parse thecode for let() constructions (defining local variables and local functions) and expand/remove them by moving their local variables to the top-level function's local variables section.  **Note:** This variable works only for Scheme functions(for example, `.ils`/`.scm` files). | nil
| traceIndent | If set to`t`, prints the trace with many '|||||', that is the old trace style. To print the trace in the new '|[%level]' construction, use the default value (`nil`).  See Example 2 below. | nil
| debugMacro | If set to`t`, the IL compiler sets the lineNumber on the expanded macro code to the lineNumber of the original form. | nil
| stackTraceFormat | Controls the stacktrace output format. It can havethree values: `fullStack`, `onlyCall`, and `onlyTop`.  `fullStack` prints the complete set of SKILL stack frames.  `onlyCall` supresses the printing of non-function frames in the output.  `onlyTop` supresses the printing of non-function frames except for the top most function frame. | `fullStack`
#### Arguments

|  |
| --- | ---
| `s_name` | Name of internal system variable.
|  |
| --- | ---
| `g_switchValue` | New value for internal system variable, usually`t` or `nil`.
#### Value Returned

|  |
| --- | ---
| `g_switchValue` | The second argument to`sstatus`.
#### Example 1

`sstatus( debugMode t )          => t`

Turns on debug mode.

`sstatus( integermode t )        => t`

Turns on integer mode.

`sstatus( stacktraceDump t)      => t`

Prints the local variables when an error occurs if
`sstatus( stacktrace t)` is set.

`sstatus( stacktrace 6 )         => 6`

Prints the first six stack frames every time an error occurs.

#### Example 2

`defun factorial (n) (if (n== 0) 1 (n*factorial(n-1]`

`=>factorial`

```
(trace factorial);value of the traceIndent variable is nil, which is the default value
```

`=>(factorial)`

`(factorial 10)`

`|[1]factorial(10)`

`|[2]factorial(9)`

`|[3]factorial(8)`

`|[4]factorial(7)`

`|[5]factorial(6)`

`|[6]factorial(5)`

`|[7]factorial(4)`

`|[8]factorial(3)`

`|[9]factorial(2)`

`|[10]factorial(1)`

`|[11]factorial(0)`

`|[11]factorial --> 1`

`|[10]factorial --> 1`

`|[9]factorial --> 2`

`|[8]factorial --> 6`

`|[7]factorial --> 24`

`|[6]factorial --> 120`

`|[5]factorial --> 720`

`|[4]factorial --> 5040`

`|[3]factorial --> 40320`

`|[2]factorial --> 362880`

`|[1]factorial --> 3628800`

`3628800`

`(sstatus traceIndent t)`

`t`

`(factorial 10)`

`|factorial(10)`

`||factorial(9)`

`|||factorial(8)`

`||||factorial(7)`

`|||||factorial(6)`

`||||||factorial(5)`

`|||||||factorial(4)`

`||||||||factorial(3)`

`|||||||||factorial(2)`

`||||||||||factorial(1)`

`|||||||||||factorial(0)`

`|||||||||||factorial --> 1`

`||||||||||factorial --> 1`

`|||||||||factorial --> 2`

`||||||||factorial --> 6`

`|||||||factorial --> 24`

`||||||factorial --> 120`

`|||||factorial --> 720`

`||||factorial --> 5040`

`|||factorial --> 40320`

`||factorial --> 362880`

`|factorial --> 3628800`

`3628800`

### status

`status( s_name ) => g_switchValue`

#### Description

Returns the value of the internal system variable named. This`nlambda` function also works in SKILL++ mode.

See the`sstatus` function for a list of the [Internal System Variables](#1039940 "Core Functions").

#### Arguments

|  |
| --- | ---
| `s_name` | Name of internal system variable.
#### Value Returned

|  |
| --- | ---
| `g_switchValue` | Status of the internal system variable, usually either`t` or `nil`.
#### Example

`status( debugMode ) => t`

Checks the status of`debugMode` and returns `t` if `debugMode` is on.

The`status` function gets a switch. The `sstatus` function sets a switch.

```
status debugMode    ; read the current value of the switch=> nilsstatus debugMode t ; set the value of the switch to new value=> tstatus debugMode=> t
```

### theEnvironment

`theEnvironment( [ u_funobj ] ) => e_environment | nil`

#### Description

(SKILL++ mode only) Returns the top level environment if called from a SKILL++ top-level.Returns the enclosing lexical environment if called within a SKILL++ function. Returns the associated environment if passed a SKILL++ function object. Otherwise returns `nil`.

* In SKILL++, there is a unique top-level environment that implicitly encloses all other localenvironments. If you do not pass the optional argument, when you call `theEnvironment` from a SKILL++ top-level, `theEnvironment` returns this environment. The `schemeTopLevelEnv` function also returns this environment.

* If you call`theEnvironment` from within a SKILL++ function and if you do not pass the optional argument, `theEnvironment` returns the enclosing lexical environment.

* If you are in debug mode, you can pass a closure to`theEnvironment`. A *closure* is another term for a function object returned by evaluating a SKILL++ `lambda` expression which abstractly, consists of two parts:

* The code for the`lambda` expression.

* The environment in which the free variables in the body are bound when the`lambda` expression is evaluated.

* If you call`theEnvironment` from a SKILL function and do not pass a *closure*, then `theEnvironment` function returns `nil`.

#### Arguments

|  |
| --- | ---
| `u_funobj` | Optional argument. Should be a SKILL++ closure.
#### Value Returned

|  |
| --- | ---
| `nil` | Returned when called from a SKILL function and you do not passa SKILL++ closure as the optional argument.
|  |
| --- | ---
| `e_environment` | Either the top-level environment, or the enclosing environment,or the closure's environment.
#### Example

`Z = let( ( x )     x = 3     theEnvironment()     ) ; let=> envobj:0x1e0060`

Returns the environment that the`let` expression establishes. The value of `Z` is an environment in which `x` is bound to 3. Each time you execute the above expression, it returns a different environment object, as you can tell by observing the print representation.

```
Z = let( (( x theEnvironment()))    x    )=> envobj:0x2fc018eq( schemeTopLevelEnv() Z ) => t
```

Uses`theEnvironment` to illustrate that the variable initialization expressions in a `let` expression refer to the enclosing environment.

```
V = letrec( (( x theEnvironment()))    x    )=> envobj:0x33506ceq( schemeTopLevelEnv() V ) => nileq( V~>x V ) => t
```

Uses`theEnvironment` to illustrate that the variable initialization expressions in a `letrec` expression refers to the `letrec`'s environment.

```
W = let( (( r 3 ) ( y 4 ))        let( (( z 5 ) ( v 6 ))            theEnvironment()            ) ; let        ) ; let=> envobj:0x456030cW~>r => 3W~>z => 5W~>?? => ((z(5) (v 6)) ((r 3) y(4)))
```

Returns the environment that the nested`let` expressions establish. Notice that assigning it to the top-level variable W makes it persistent.

```
Q = letrec(     ( ;; begin locals        ( X 6 )        ( self             lambda( ( )                 theEnvironment()                 ) ; lambda            ) ; self        ) ;;; end of locals    self     ) ; letrec => funobj:0x1e38b8Q() => envobj:0x1e00e4theEnvironment( Q ) => envobj:0x1e00e4 ;in debug mode only
```

Returns a function object which, in turn, returns its local environment.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
