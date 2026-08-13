### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

11
==

Writing Style
=============

Good style in any language can lead to programs that are understandable, reusable,extensible, efficient, and easy to maintain. These attributes are particularly important to have in programs developed using an extension language like the Cadence® SKILL language because the programs tend to change a lot and the number of contributors can be many.

Useful SKILL programs, or pieces of them, get copied and passed around via e-mail orbulletin boards. Hence, it is important to consider the following when writing SKILL programs:

* Be specific, concise, and most importantly consistent.

* Anticipate a novice reader's questions and document the code accordingly.

* Be conventional. Using fancy techniques that are generally possible in a Lisp-basedlanguage, yet generally not well understood, might not be a good idea (unless you are doing it to gain in performance or reduce memory use).

* Avoid too many global states and direct access to them. Use abstractions.

* Make functional interfaces non-modal. That is, try and not predicate your interfaces on aglobal state or global mode such that a second user of the interface does not experience unpredictable behavior. For example, it is bad style to have a procedure that puts an editor in "insert" mode and uses subsequent calls to insert objects into the design. It is better to have one call that takes a list of objects to be inserted:

|  |
| --- | ---
| ****GOOD**** | **BAD**
| `EDinsert(database '(obj1 obj2 obj3))` | ``` EDstartInsert(database)EDinsert(obj1)EDinsert(obj2)EDinsert(obj3)EDendInsert(database) ```
|||
|
|
|
As in all programming languages, the layout of code within a file can greatly affect thereadability and maintainability of the code. The code examples in this manual use a layout that is both intuitive and easy to understand, but layout is really a matter of taste.

The rest of this chapter describes specific situations where coding style issues are important.

* [Code Layout](#1008218 "Writing Style")

* [Using Globals](#1008275 "Writing Style")

* [Coding Style Mistakes](#1008293 "Writing Style")

* [Red Flags](#1008333 "Writing Style")

Code Layout
-----------

The readability of the code is the most important aspect of the code layout. The followingguidelines can help you to write more readable code.

### Comments and Documentation

You can use either of the following methods for commenting in SKILL:

* `;` at the beginning of a line

* `/*…*/` surrounding your comments

> **Note:** Because`/*…*/` comments cannot be nested, some programmers find them easier to see.

While it is typically easier to understand and maintain code that is well-commented, you mustalso keep your comments consistent with your code. Comments that are misleading because they have not been maintained along with the code can be worse than not having any comments at all.

You should document your data structures by describing the motivation behind them and theeffect of each structure on the algorithm. Well-designed and -documented data structures can tell a lot about the nature of the program.

If you are reading someone else's code and find it inadequately documented, write down yourquestions as comments. They may get answered or will encourage other readers to persevere.

As you develop a program, you should maintain a "to-do" list. For example, you can put a"to-do" comment around a dubious looking piece of code to explain your misgivings so that another developer can track a bug in that code.

Generally, if you find that you need to write convoluted comments about a convolutedalgorithm, you should rewrite the algorithm. Strong code can be self-documenting.

#### Things to Comment and Document

Cadence suggests that you comment the following items:

|  |
| --- | ---
| **Item to comment** | **What to comment**
| Code modules | Each code module should have a header containing at least theauthor, creation date, and change history of the module, plus a general description of the contents.
| Procedure definitions | Precede procedure definitions with a block comment detailingthe functionality of and interfaces to the procedure. Add a help string inside the procedure (see ["procedure"](chap3.html#1009088 "Creating Functions in SKILL")). Help systems extract this information for display. As much as possible, add type templates for procedure arguments to help erroneous use; type information can be extracted by help systems.
| Data structures | Describe contents of data structures and impact on algorithms.
| Complex conditionals | Comment any test within a conditional function that is nontrivialto indicate the pass/fail conditions.
| Mapping functions | Comment complex mapping functions to state what the returnvalues are.
| Terminating parentheses | Where a function call extends over several lines, label theclosing parenthesis with the function name.
#### Things Not to Comment and Document

While including any number of comments in your code does not affect performance once ithas been read into the SKILL interpreter, Cadence suggests that you do not comment the following in production code:

|  |
| --- | ---
| **Item not to comment** | **Explanation**
| Long change details | You should use your source code control system (such as RCSor SCCS) to maintain full details of any changes you make and include only a brief outline of your changes in the module header (rather than in the body of the code). Including details in the body of the code can make maintenance more difficult.
| PCR details | You should maintain product change request information in thePCR itself.
### Function Calls and Brackets

Function calls in SKILL can be written in two distinct ways, with the opening parenthesis eitherbefore the function name, as in Lisp, or after it, as in C. Once again, the method chosen is not as important as ensuring that it is chosen consistently. However, putting the parenthesis after the function name does make it easier for a non-Lisp programmer to read the code. It is also easier to distinguish between function names and arguments, and between function calls and other lists.

When a function call extends over more than one line in a file, it is recommended that theclosing parenthesis is aligned, on a separate line, with the beginning of the function name. This makes it is easier to see where a particular function call finishes and has the added advantage that missing parentheses are easier to see.

**Note:** Having extra newlines to allow alignment of function arguments or parentheses doesnot affect the performance of the code once it has been read into the SKILL interpreter.

#### Avoid Using a Super Right Bracket

Using the super right bracket (`]`) is strongly discouraged except when using the interactive interpreter because

* Missing parentheses can become difficult to locate.

* Inserting another function call around the code containing the super right bracket can bedifficult.

* Bracket-matching procedures in editors neither manage nor account for super rightbracket.

* One method you can use to make sure that all your parentheses are matching whenwriting SKILL code is to insert the closing parenthesis immediately after the opening parenthesis of a function call, and then to go back and fill in the arguments.

#### Brackets in SKILL Are Always Significant

* In C, it is possible to insert brackets where they are not really needed and not affect thefunctionality of the program.

* In SKILL, the insertion of extra brackets can be, and usually is, incorrect.

The problem usually occurs with infix operators. In SKILL (as in Lisp) every function evaluatesto a list whose head is the function name. Thus, code such as

`a + b`

is held internally as the list

`(plus a b)`

You must understand the relative precedence of the built-in SKILL functions. For example,consider the following code:

`a = b && c`

The line of code above is held as the following list:

`(setq a (and b c))`

rather than

`(and (setq a b) c)`

While this precedence is exactly what you would expect from any language, it might notnecessarily be what you want. Consider the following:

`if(res = func1(arg) && res != no_val then …)`

* **What actually happens:**
* The interpreter evaluates the expression`func1(arg) && (res != no_val)` and assigns the result to `res`.
* Call`func1` and store the result in `res`.
* Check that`res` is not equal to `no_val`.

The programmer needs to write the code as follows to perform the desired function:

`if((res = func1(arg)) && res != no_val then …)`

* ***Using too many parentheses can cause the code to fail. For example, thefollowing statement has too many levels of parentheses:***

> `a = ((func1(arg1)) && (func2(arg2)))`

**Note:** Parentheses in function calls are only optional for the built-in unary and infix operators,such as `!` and `+`. The following functions are equivalent:

`!a`

`!(a)`

`(!a)`

### Commas

Commas between function arguments, and list elements, are optional in SKILL.Programmers from a C programming background will probably want to insert commas, those from a Lisp background probably will not. The general recommendation is that commas should not be used.

Using Globals
-------------

The use of global variables in SKILL, as with any language, should be kept to a minimum. Theproblems are greater in SKILL however because of its dynamic scoping of variables.

The problem with global variables is that different programmers can be using a variable withthe same name. This type of "name clash" can cause problems that are even more difficult to isolate than the "Error Global" problem, because programs can fail because of the order in which they have been run. However, because this problem can usually be easily avoided by adopting a standard naming scheme, SKILL Lint will report this type of variable as a "Warning Global". To illustrate the problem, consider the example code below:

```
/*********************************************************** * myShowForm()***********************************************************/
```

```
procedure( myShowForm()      /* If we don't already have the form, then create it. */      unless(boundp('theForm) && theForm            myBuildForm()      )
```

`/* Display the form. */      hiDisplayForm(theForm)) /* end myShowForm */`

```
/********************************************************** * yourShowForm()***********************************************************/
```

```
procedure( yourShowForm()      /* If we don't already have the form, then create it. */      unless(boundp('theForm) && theForm            yourBuildForm()      )      /* Display the form. */      hiDisplayForm(theForm)) /* end yourShowForm */
```

```
/*********************************************************** * myBuildForm()***********************************************************/
```

```
procedure( myBuildForm()      hiCreateForm('theForm,             "My Form"             "myFormCallback()"             list( hiCreateStringField(?name 'string1,                              ?prompt "my field")             ) /* end list */ )       /* end hiCreateForm */) /* end myBuildForm */
```

```
/*********************************************************** * yourBuildForm() * * Build the form.***********************************************************/
```

```
procedure( yourBuildForm()      hiCreateForm('theForm,             "Your Form"             "yourFormCallback()"             list( hiCreateStringField(?name 'string1,                              ?prompt "your field")             ) /* end list */      ) /* end hiCreateForm */) /* end myBuildForm */
```

If`myShowForm` is called before `yourShowForm`, the global variable `theForm` will be set to a different value than if yourShowForm is called before myShowForm.

Coding Style Mistakes
---------------------

C programmers sometimes make the following mistakes when programming in SKILL. Eventhough these mistakes have mostly to do with coding style, some of them can have an impact on performance.

* [Inefficient Use of Conditionals](#1008296 "Writing Style")

* [Misusing prog and Conditionals](#1008310 "Writing Style")

### Inefficient Use of Conditionals

A common mistake with conditional checks is to use multiple inversions and boolean checkswhen using De Morgan's Law would result in a simpler and clearer test. For example, the code below shows a common form of check.

`if( !template || !templateDir       warn("Invalid templates\n")) /* end if */`

This check can be optimized using De Morgan's Law to be:

`if( !(template && templateDir)      warn("Invalid templates\n")) /* end if */`

Another common mistake is made by many programmers used to having only the standard`if` and `case` conditionals. SKILL provides a rich variety of conditional functions, and appropriate use of these functions can lead to much clearer and faster code. For example, an `unless` could be used in the above check to yield the clearer and more efficient:

```
unless( template && templateDir       warn("Invalid templates\n")) /* end unless */
```

Another example is where multiple if-then-else checks are used, such as:

```
if(stringp(layer) then      layerName = layerelse       if(fixp(layer) then            layerNum = layer      else            if(listp(layer) then                  layerPurpose = cadr(layer)            ) /* end if */      ) /* end if */) /* end if */
```

This can be more clearly and efficiently implemented using a`cond`:

```
cond(      (stringp(layer)  layerName = layer)      (fixp(layer)     layerNum = layer)      (listp(layer)    layerPurpose = cadr(layer) )) /* end cond */
```

When applying multiple tests, either in a nested`if` function or a `cond` function, it is important to consider the order in which the tests will be carried out.

* If one test is more likely to be true than the others then it should go first.

* If all tests are equally likely to be true, then the test that involves the most work shouldgo last.

### Misusing prog and Conditionals

Quite often,`prog` statements are used to return from a procedure when an error condition occurs. In the example below,`template` and `templateDir` are both verified, and only if both are correct is the rest of the procedure executed:

```
procedure( EditCallback()       prog( ( templateFile templateDir fullName )             templateFile  = ReportForm->Template->value             templateDir   = ReportForm->TemplateDir->value
```

`/* Check the template directory. */`

```
if( ((templateDir == "") || (!templateDir)) then                  return(warn("Invalid template directory.\n"))             )
```

`/* Check the template file. */`

```
if( ((templateFile == "") || (!templateFile)) then                  return(warn("Invalid template file name.\n"))             )
```

`/* If both are correct then act.*/`

```
sprintf(fullName "%s/%s" templateDir templateFile)            if(isFile(fullName) then                   LoadCallback()             else                   SetUpEnviron()             ) /* end if */
```

```
return(hiDisplayForm(EditTemplateForm ))       ) /* end prog */ ) /* end EditCallback */
```

Using the fact that a`cond` returns the value of the last statement executed allows us to more efficiently implement this example using a `let`:

```
procedure( EditCallback()       let(((templateFile ReportForm->Template->value)              (templateDir  ReportForm->TemplateDir->value)               fullName)
```

`cond(                  /* Check the template directory. */`

```
( (templateDir == "") || (!templateDir)                         warn("Invalid template directory.\n")                  )
```

`/* Check the template file. */`

```
( (templateFile == "") || (!templateFile)                         warn("Invalid template file name.\n")                  )
```

`/* If both are correct then act. */`

```
(t                         sprintf(fullName "%s/%s" templateDir                                           templateFile)                         if(isFile(fullName) then                               LoadCallback()                         else                               SetUpEnviron()
```

`) /* if */`

```
hiDisplayForm(EditTemplateForm )                       )           ) /* end cond */       ) /* end let */) /* end of EditCallback */
```

Red Flags
---------

The following are situations or functions that require special attention. Their use is oftensymptomatic of problems with the way interfaces or algorithms are designed. In some cases, their use is legitimate and these comments do not apply.

* [Any Use of eval or evalstring](#1008336 "Writing Style")

* [Excessive Use of reverse and append](#1008338 "Writing Style")

* [Excessive Use of gensym and concat](#1008340 "Writing Style")

* [Overuse of the Functions Combining car and cdr](#1008342 "Writing Style")

* [Use of eval Inside Macros](#1008344 "Writing Style")

* [Misuse of prog and return in SKILL++ mode](#1010226 "Writing Style")

### Any Use of eval or evalstring

Strictly speaking these calls are inefficient and any code using them is either sufferingthrough using a bad interface from another application or the code itself is badly designed.

### Excessive Use of reverse and append

Excessive use of`reverse` and `append` is an indication that algorithms using list structures are badly designed. They are acceptable when prototyping but production code should not suffer their consequences. Both these functions are capable of generating a lot of memory. There are alternatives to these functions and the recommendation is that code using these functions should be rewritten using `tconc`.

### Excessive Use of gensym and concat

Symbols are large structures and applications that have to generate symbols at run time maynot be designed to use the right data structure. Many times applications use symbols in place of small strings to save on memory because symbols are unique in the system. However, SKILL caches strings so this optimization might not always yield the desired effect.

### Overuse of the Functions Combining car and cdr

One function that combines`car` and `cdr` is `cdaddr`. Using such functions, which are not as intuitive as calls to `nthelem` and `nthcdr`, can lead to programmer and reader errors.

### Use of eval Inside Macros

Calling`eval` inside a macro means you are determining the value of an entity at compile time as opposed to evaluating it at run time, which may result in undesirable behavior. In general, macros should massage expressions and return expressions (see ["Macros"](chap9.html#Macros "Advanced Topics")).

### Misuse of prog and return in SKILL++ mode

Misuse of`prog` and `return` in SKILL++ might corrupt SKILL++ environment frames and can lead to a fatal programming error. The following example demonstrates misuse that you should avoid (using `prog` and `return` in a SKILL++ `.ils` file). Immediately following this example is an example of what you should do instead.

```
procedure( myFunc(namelist keys "ll")  let( (selectedlist)    foreach( name namelist      prog(()        foreach( key keys          when( rexMatchp(key name)            return(t)          )        )        return(nil)      )      selectedlist = cons(name selectedlist)    )  ))
```

Instead, do this:

```
procedure( myFunc(namelist keys "ll")  let( ()    setof( name namelist      setof(key keys rexMatchp(key name))    )  ))
```




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
