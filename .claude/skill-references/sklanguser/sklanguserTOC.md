### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

Contents
========

[Preface](preface.html#1008685 "Preface")
-----------------------------------------

[Licensing in Cadence SKILL Language](preface.html#1013800 "Preface")

[About the SKILL Language](preface.html#1012850 "Preface")

[SKILL Development Helpful Hints](preface.html#1010348 "Preface")

[Related Documents](preface.html#1014491 "Preface")

:   [Installation, Environment, and Infrastructure](preface.html#1012869 "Preface")

[Section Names and Meanings](preface.html#1012886 "Preface")

[Typographic and Syntax Conventions](preface.html#1012896 "Preface")

:   [SKILL Syntax Examples](preface.html#1012922 "Preface")

[Identifiers Used to Denote Data Types](preface.html#1012942 "Preface")

[Additional Learning Resources](preface.html#1014620 "Preface")

[How to Contact Technical Support](preface.html#KeyBindings "Preface")

[1](chap1.html#1005655 "Getting Started")
-----------------------------------------

[Getting Started](chap1.html#1008199 "Getting Started")
-------------------------------------------------------

[SKILL's Relationship to Lisp](chap1.html#Lisp "Getting Started")

:   [Programming Notation](chap1.html#1008210 "Getting Started")
:   [Data Manipulation](chap1.html#1008218 "Getting Started")
:   [Characters](chap1.html#1008226 "Getting Started")

[Cadence SKILL Language at a Glance](chap1.html#1008229 "Getting Started")

:   [Terms and Definitions](chap1.html#1008238 "Getting Started")
:   [Invoking a SKILL Function](chap1.html#1008255 "Getting Started")
:   [Return Value of a Function](chap1.html#1013963 "Getting Started")
:   [Simplest SKILL Data](chap1.html#1008295 "Getting Started")
:   [Calling a Function](chap1.html#1008319 "Getting Started")
:   [Operators Are SKILL Functions](chap1.html#1008327 "Getting Started")
:   [Using Variables](chap1.html#1008381 "Getting Started")
:   [Alternative Ways to Invoke a Function](chap1.html#1008389 "Getting Started")
:   [Solving Some Common Problems](chap1.html#1008398 "Getting Started")

[SKILL Lists](chap1.html#1008456 "Getting Started")

:   [Building Lists](chap1.html#1008489 "Getting Started")
:   [Accessing Lists](chap1.html#1008542 "Getting Started")
:   [Modifying Lists](chap1.html#1008565 "Getting Started")

[File Input/Output](chap1.html#1008650 "Getting Started")

:   [Displaying Data](chap1.html#1008655 "Getting Started")
:   [Writing Data to a File](chap1.html#1008710 "Getting Started")
:   [Reading Data from a File](chap1.html#1008730 "Getting Started")

[Flow of Control](chap1.html#1008779 "Getting Started")

:   [Relational Operators](chap1.html#1008787 "Getting Started")
:   [Logical Operators](chap1.html#1008876 "Getting Started")
:   [The if Function](chap1.html#1008931 "Getting Started")
:   [The when and unless Functions](chap1.html#1008943 "Getting Started")
:   [The case Function](chap1.html#1008950 "Getting Started")
:   [The for Function](chap1.html#1008959 "Getting Started")
:   [The foreach Function](chap1.html#1008969 "Getting Started")

[Developing a SKILL Function](chap1.html#1008981 "Getting Started")

:   [Grouping SKILL Statements](chap1.html#1008990 "Getting Started")
:   [Declaring a SKILL Function](chap1.html#1009001 "Getting Started")
:   [Defining Function Parameters](chap1.html#1009009 "Getting Started")
:   [Selecting Prefixes for Your Functions](chap1.html#1009016 "Getting Started")
:   [Maintaining SKILL Source Code](chap1.html#1009021 "Getting Started")
:   [Loading Your SKILL Source Code](chap1.html#1009028 "Getting Started")
:   [Redefining a SKILL Function](chap1.html#1014254 "Getting Started")

[2](chap2.html#1005655 "Language Characteristics")
--------------------------------------------------

[Language Characteristics](chap2.html#1008199 "Language Characteristics")
-------------------------------------------------------------------------

[Naming Conventions](chap2.html#1009937 "Language Characteristics")

:   [Names of Functions](chap2.html#Names of Functions "Language Characteristics")
:   [Cadence-Private Functions](chap2.html#1010003 "Language Characteristics")
:   [Names of Variables](chap2.html#1010007 "Language Characteristics")

[Function Calls](chap2.html#1008239 "Language Characteristics")

[SKILL Syntax](chap2.html#1008253 "Language Characteristics")

:   [Special Characters](chap2.html#1008256 "Language Characteristics")
:   [Comments](chap2.html#1008389 "Language Characteristics")
:   [White Space](chap2.html#1008396 "Language Characteristics")
:   [White Space Characters](chap2.html#1011531 "Language Characteristics")
:   [Parentheses](chap2.html#1008410 "Language Characteristics")
:   [Super Right Bracket](chap2.html#1008429 "Language Characteristics")
:   [Backquote, Comma, and Comma-At](chap2.html#1009080 "Language Characteristics")
:   [Line Continuation](chap2.html#1008453 "Language Characteristics")
:   [Length of Input Lists](chap2.html#1014326 "Language Characteristics")

[Data Characteristics](chap2.html#1008463 "Language Characteristics")

:   [Data Types](chap2.html#1013610 "Language Characteristics")
:   [Numbers](chap2.html#1015707 "Language Characteristics")
:   [Strings](chap2.html#1008770 "Language Characteristics")
:   [Atoms](chap2.html#1008778 "Language Characteristics")
:   [Escape Sequences](chap2.html#1008785 "Language Characteristics")
:   [Symbols](chap2.html#1008834 "Language Characteristics")
:   [Characters](chap2.html#1008854 "Language Characteristics")

[3](chap3.html#1005655 "Creating Functions in SKILL")
-----------------------------------------------------

[Creating Functions in SKILL](chap3.html#1008199 "Creating Functions in SKILL")
-------------------------------------------------------------------------------

[Terms and Definitions](chap3.html#1009052 "Creating Functions in SKILL")

[Kinds of Functions](chap3.html#1009074 "Creating Functions in SKILL")

[Syntax Functions for Defining Functions](chap3.html#1009085 "Creating Functions in SKILL")

:   [procedure](chap3.html#1009088 "Creating Functions in SKILL")
:   [lambda](chap3.html#1009093 "Creating Functions in SKILL")
:   [nprocedure](chap3.html#1009107 "Creating Functions in SKILL")
:   [defmacro](chap3.html#1009113 "Creating Functions in SKILL")
:   [mprocedures](chap3.html#1009120 "Creating Functions in SKILL")
:   [defglofun](chap3.html#1012786 "Creating Functions in SKILL")
:   [Summary of Syntax Functions](chap3.html#1009128 "Creating Functions in SKILL")

[Defining Parameters](chap3.html#1009179 "Creating Functions in SKILL")

:   [@rest Option](chap3.html#1009182 "Creating Functions in SKILL")
:   [@optional Option](chap3.html#1009196 "Creating Functions in SKILL")
:   [@key Option](chap3.html#1009207 "Creating Functions in SKILL")
:   [Combining Arguments](chap3.html#1009213 "Creating Functions in SKILL")

[Type Checking](chap3.html#typechecking "Creating Functions in SKILL")

[Local Variables](chap3.html#1009266 "Creating Functions in SKILL")

:   [Defining Local Variables Using the let Function](chap3.html#1012098 "Creating Functions in SKILL")
:   [Defining Local Variables Using the prog Function](chap3.html#1012049 "Creating Functions in SKILL")
:   [Initializing Local Variables to Non-nil Values](chap3.html#1009288 "Creating Functions in SKILL")

[Global Variables](chap3.html#1009291 "Creating Functions in SKILL")

:   [Testing Global Variables](chap3.html#1009300 "Creating Functions in SKILL")
:   [Avoiding Name Clashes](chap3.html#1009306 "Creating Functions in SKILL")
:   [Naming Scheme](chap3.html#1009316 "Creating Functions in SKILL")
:   [Reducing the Number of Global Variables](chap3.html#1009321 "Creating Functions in SKILL")

[Redefining Existing Functions](chap3.html#1009325 "Creating Functions in SKILL")

[Physical Limits for Functions](chap3.html#1009333 "Creating Functions in SKILL")

[4](chap4.html#1005655 "Data Structures")
-----------------------------------------

[Data Structures](chap4.html#1008199 "Data Structures")
-------------------------------------------------------

[Access Operators](chap4.html#1008203 "Data Structures")

[Symbols](chap4.html#1008218 "Data Structures")

:   [Creating Symbols](chap4.html#1008228 "Data Structures")
:   [The Print Name of a Symbol](chap4.html#1008239 "Data Structures")
:   [The Value of a Symbol](chap4.html#1008247 "Data Structures")
:   [The Function Binding of a Symbol](chap4.html#1008274 "Data Structures")
:   [The Property List of a Symbol](chap4.html#1008279 "Data Structures")
:   [Important Symbol Property List Considerations](chap4.html#1008317 "Data Structures")

[Disembodied Property Lists](chap4.html#1008324 "Data Structures")

:   [Important Considerations](chap4.html#1008341 "Data Structures")
:   [Additional Property List Functions](chap4.html#1008353 "Data Structures")

[Strings](chap4.html#1008386 "Data Structures")

:   [Concatenating Strings](chap4.html#1008391 "Data Structures")
:   [Comparing Strings](chap4.html#1008407 "Data Structures")
:   [Getting Character Information in Strings](chap4.html#1008431 "Data Structures")
:   [Indexing with Character Pointers](chap4.html#1008440 "Data Structures")
:   [Creating Substrings](chap4.html#1008462 "Data Structures")
:   [Converting Case](chap4.html#1008481 "Data Structures")
:   [Pattern Matching of Regular Expressions](chap4.html#patternMatching "Data Structures")
:   [Pattern Matching Functions](chap4.html#1008560 "Data Structures")

[Defstructs](chap4.html#1008596 "Data Structures")

:   [Behavior Is Similar to Disembodied Property Lists](chap4.html#1008603 "Data Structures")
:   [Additional Defstruct Functions](chap4.html#1008614 "Data Structures")
:   [Accessing Named Slots in SKILL Structures](chap4.html#1008630 "Data Structures")
:   [Extended defstruct Example](chap4.html#1008656 "Data Structures")

[Arrays](chap4.html#1008683 "Data Structures")

:   [Allocating an Array of a Given Size](chap4.html#1008690 "Data Structures")
:   [Accessing Arrays](chap4.html#1008698 "Data Structures")

[Association Tables](chap4.html#1008719 "Data Structures")

:   [Initializing Tables](chap4.html#1008727 "Data Structures")
:   [Manipulating Table Data](chap4.html#1008735 "Data Structures")
:   [Traversing Association Tables](chap4.html#1014851 "Data Structures")
:   [Implementing Sparse Arrays](chap4.html#1015140 "Data Structures")
:   [List-Oriented Functions for Association Tables](chap4.html#1014773 "Data Structures")

[Association Lists](chap4.html#1008817 "Data Structures")

[User-Defined Types](chap4.html#1008828 "Data Structures")

[5](chap5.html#1016565 "Arithmetic and Logical Expressions")
------------------------------------------------------------

[Arithmetic and Logical Expressions](chap5.html#1016567 "Arithmetic and Logical Expressions")
---------------------------------------------------------------------------------------------

[Creating Arithmetic and Logical Expressions](chap5.html#1008226 "Arithmetic and Logical Expressions")

:   [Role of Parentheses](chap5.html#1008231 "Arithmetic and Logical Expressions")
:   [Quoting to Prevent Evaluation](chap5.html#1008237 "Arithmetic and Logical Expressions")
:   [Arithmetic and Logical Operators](chap5.html#operator_table "Arithmetic and Logical Expressions")
:   [Predefined Arithmetic Functions](chap5.html#1008555 "Arithmetic and Logical Expressions")
:   [Bitwise Logical Operators](chap5.html#1008660 "Arithmetic and Logical Expressions")
:   [Bit Field Operators](chap5.html#1008696 "Arithmetic and Logical Expressions")
:   [Mixed-Mode Arithmetic](chap5.html#1018988 "Arithmetic and Logical Expressions")
:   [Function Overloading](chap5.html#1008854 "Arithmetic and Logical Expressions")
:   [Integer-Only Arithmetic](chap5.html#1008861 "Arithmetic and Logical Expressions")
:   [True (non-nil) and False (nil) Conditions](chap5.html#1012306 "Arithmetic and Logical Expressions")
:   [Controlling the Order of Evaluation](chap5.html#1008894 "Arithmetic and Logical Expressions")
:   [Testing Arithmetic Conditions](chap5.html#1008904 "Arithmetic and Logical Expressions")

[Differences Between SKILL and C Syntax](chap5.html#1008946 "Arithmetic and Logical Expressions")

[SKILL Predicates](chap5.html#SKILL Predicates "Arithmetic and Logical Expressions")

:   [The atom Function](chap5.html#1008965 "Arithmetic and Logical Expressions")
:   [The boundp Function](chap5.html#1008970 "Arithmetic and Logical Expressions")
:   [Using Predicates Efficiently](chap5.html#1008977 "Arithmetic and Logical Expressions")
:   [The eq Function](chap5.html#1008983 "Arithmetic and Logical Expressions")
:   [The equal Function](chap5.html#1008987 "Arithmetic and Logical Expressions")
:   [The neq Function](chap5.html#1008998 "Arithmetic and Logical Expressions")
:   [The nequal Function](chap5.html#1009003 "Arithmetic and Logical Expressions")
:   [The member and memq Functions](chap5.html#1009007 "Arithmetic and Logical Expressions")
:   [The tailp Function](chap5.html#1009014 "Arithmetic and Logical Expressions")
:   [Type Predicates](chap5.html#Type Predicates "Arithmetic and Logical Expressions")

[6](chap6.html#1005655 "Control Structures")
--------------------------------------------

[Control Structures](chap6.html#1008199 "Control Structures")
-------------------------------------------------------------

[Control Functions](chap6.html#1008203 "Control Structures")

:   [Conditional Functions](chap6.html#1008208 "Control Structures")
:   [Iteration Functions](chap6.html#1008237 "Control Structures")

[Selection Functions](chap6.html#1008252 "Control Structures")

[Declaring Local Variables with prog](chap6.html#1008269 "Control Structures")

:   [The prog Function](chap6.html#1008277 "Control Structures")
:   [The return Function](chap6.html#1008283 "Control Structures")

[Grouping Functions](chap6.html#1008290 "Control Structures")

:   [Using prog, return, and let](chap6.html#1008297 "Control Structures")
:   [Using the progn Function](chap6.html#1008317 "Control Structures")
:   [Using the prog1 and prog2 Functions](chap6.html#1008321 "Control Structures")

[7](chap7.html#1005655 "I/O and File Handling")
-----------------------------------------------

[I/O and File Handling](chap7.html#1008199 "I/O and File Handling")
-------------------------------------------------------------------

[File System Interface](chap7.html#1008204 "I/O and File Handling")

:   [Files](chap7.html#1008207 "I/O and File Handling")
:   [Directories](chap7.html#1008210 "I/O and File Handling")
:   [Directory Paths](chap7.html#1008214 "I/O and File Handling")
:   [The SKILL Path](chap7.html#1008228 "I/O and File Handling")
:   [Working with the SKILL Path](chap7.html#1008240 "I/O and File Handling")
:   [Working with the Installation Path](chap7.html#1008256 "I/O and File Handling")
:   [Checking File Status](chap7.html#1008276 "I/O and File Handling")
:   [Working with Directories](chap7.html#1008337 "I/O and File Handling")

[Ports](chap7.html#1008398 "I/O and File Handling")

:   [Predefined Ports](chap7.html#1008402 "I/O and File Handling")
:   [Opening and Closing Ports](chap7.html#1008433 "I/O and File Handling")

[Output](chap7.html#1008463 "I/O and File Handling")

:   [Unformatted Output](chap7.html#1008466 "I/O and File Handling")
:   [Formatted Output](chap7.html#1008492 "I/O and File Handling")
:   [Pretty Printing](chap7.html#1008599 "I/O and File Handling")

[Input](chap7.html#1008613 "I/O and File Handling")

:   [Reading and Evaluating SKILL Formats](chap7.html#1008653 "I/O and File Handling")
:   [Reading but Not Evaluating SKILL Formats](chap7.html#1008693 "I/O and File Handling")
:   [Reading Application-Specific Formats](chap7.html#1008705 "I/O and File Handling")
:   [Reading Application-Specific Formats from Strings](chap7.html#1009485 "I/O and File Handling")

[System-Related Functions](chap7.html#1013686 "I/O and File Handling")

:   [Executing UNIX Commands](chap7.html#1008770 "I/O and File Handling")
:   [System Environment](chap7.html#1008783 "I/O and File Handling")

[8](chap8.html#1005655 "Advanced List Operations")
--------------------------------------------------

[Advanced List Operations](chap8.html#1008199 "Advanced List Operations")
-------------------------------------------------------------------------

[Conceptual Background](chap8.html#1008211 "Advanced List Operations")

:   [How Lists Are Stored in Virtual Memory](chap8.html#1008214 "Advanced List Operations")
:   [Destructive versus Non-Destructive Operations](chap8.html#1008378 "Advanced List Operations")

[Summary of List Operations](chap8.html#1008388 "Advanced List Operations")

[Altering List Cells](chap8.html#1008504 "Advanced List Operations")

:   [The rplaca Function](chap8.html#1008507 "Advanced List Operations")
:   [The rplacd Function](chap8.html#1008545 "Advanced List Operations")
:   [The setf function](chap8.html#1017501 "Advanced List Operations")

[Accessing Lists](chap8.html#1018204 "Advanced List Operations")

:   [Selecting an Indexed Element from a List (nthelem)](chap8.html#1008596 "Advanced List Operations")
:   [Applying cdr to a List a Given Number of Times (nthcdr)](chap8.html#1008600 "Advanced List Operations")
:   [Getting the Last List Cell in a List (last)](chap8.html#1008604 "Advanced List Operations")

[Building Lists Efficiently](chap8.html#1008608 "Advanced List Operations")

:   [Adding Elements to the Front of a List (cons, xcons)](chap8.html#1008611 "Advanced List Operations")
:   [Building a List with a Given Element (ncons)](chap8.html#1008658 "Advanced List Operations")
:   [Adding Elements to the End of a List (tconc)](chap8.html#1008662 "Advanced List Operations")
:   [Appending Lists](chap8.html#1008697 "Advanced List Operations")

[Reorganizing a List](chap8.html#1008772 "Advanced List Operations")

:   [Reversing a List](chap8.html#1008775 "Advanced List Operations")
:   [Sorting Lists](chap8.html#1008783 "Advanced List Operations")

[Searching Lists](chap8.html#1008798 "Advanced List Operations")

:   [The member Function](chap8.html#1008800 "Advanced List Operations")
:   [The memq Function](chap8.html#1008816 "Advanced List Operations")
:   [The exists Function](chap8.html#1008819 "Advanced List Operations")

[Copying Lists](chap8.html#1008824 "Advanced List Operations")

:   [The copy Function](chap8.html#1008826 "Advanced List Operations")
:   [Copying a List Hierarchically](chap8.html#1008835 "Advanced List Operations")

[Filtering Lists](chap8.html#1008839 "Advanced List Operations")

[Removing Elements from a List](chap8.html#1008850 "Advanced List Operations")

:   [Non-Destructive Operations](chap8.html#1008877 "Advanced List Operations")
:   [Destructive Operations](chap8.html#1008891 "Advanced List Operations")

[Substituting Elements](chap8.html#1008902 "Advanced List Operations")

[Transforming Elements of a Filtered List](chap8.html#1008910 "Advanced List Operations")

[Validating Lists](chap8.html#1008924 "Advanced List Operations")

:   [The forall Function](chap8.html#1008939 "Advanced List Operations")
:   [The exists Function](chap8.html#1008946 "Advanced List Operations")

[Using Mapping Functions to Traverse Lists](chap8.html#1008951 "Advanced List Operations")

:   [Using lambda with the map\* Functions](chap8.html#1008957 "Advanced List Operations")
:   [Using the map\* Functions with the foreach Function](chap8.html#1008966 "Advanced List Operations")
:   [The mapc Function](chap8.html#1008974 "Advanced List Operations")
:   [The map Function](chap8.html#1008986 "Advanced List Operations")
:   [The mapcar Function](chap8.html#1009000 "Advanced List Operations")
:   [The maplist Function](chap8.html#1009012 "Advanced List Operations")
:   [The mapcon Function](chap8.html#1017863 "Advanced List Operations")
:   [The mapcan Function](chap8.html#1017931 "Advanced List Operations")
:   [The mapinto Function](chap8.html#1009036 "Advanced List Operations")
:   [Summarizing the List Traversal Operations](chap8.html#1017472 "Advanced List Operations")

[List Traversal Case Studies](chap8.html#1009072 "Advanced List Operations")

:   [Handling a List of Strings](chap8.html#1009074 "Advanced List Operations")
:   [Making Every List Element into a Sublist](chap8.html#1009084 "Advanced List Operations")
:   [Using mapcan for List Flattening](chap8.html#1009090 "Advanced List Operations")
:   [Flattening a List with Many Levels](chap8.html#1009100 "Advanced List Operations")
:   [Manipulating an Association List](chap8.html#1009109 "Advanced List Operations")
:   [Using the exists Function to Avoid Explicit List Traversal](chap8.html#1009125 "Advanced List Operations")
:   [Commenting List Traversal Code](chap8.html#1009147 "Advanced List Operations")

[9](chap9.html#1005655 "Advanced Topics")
-----------------------------------------

[Advanced Topics](chap9.html#1008199 "Advanced Topics")
-------------------------------------------------------

[Cadence SKILL Language Architecture and Implementation](chap9.html#1009947 "Advanced Topics")

[SKILL Namespace](chap9.html#namespace "Advanced Topics")

:   [Need for a SKILL Namespace](chap9.html#1013727 "Advanced Topics")
:   [Default Namespace](chap9.html#1015470 "Advanced Topics")
:   [Working with a Namespace](chap9.html#1014706 "Advanced Topics")
:   [Nesting Namespaces](chap9.html#1013933 "Advanced Topics")

[Evaluation](chap9.html#1013741 "Advanced Topics")

:   [Evaluating an Expression (eval)](chap9.html#1008295 "Advanced Topics")
:   [Getting the Value of a Symbol (symeval)](chap9.html#1008304 "Advanced Topics")
:   [Applying a Function to an Argument List (apply)](chap9.html#1008312 "Advanced Topics")

[Function Objects](chap9.html#1008328 "Advanced Topics")

:   [Retrieving the Function Object for a Symbol (getd)](chap9.html#1008334 "Advanced Topics")
:   [Assigning a New Function Binding (putd)](chap9.html#1008379 "Advanced Topics")
:   [Declaring a Function Object (lambda)](chap9.html#1008388 "Advanced Topics")
:   [Evaluating a Function Object](chap9.html#1008397 "Advanced Topics")
:   [Efficiently Storing Programs as Data](chap9.html#1008405 "Advanced Topics")

[Macros](chap9.html#Macros "Advanced Topics")

:   [Benefits of Macros](chap9.html#1008422 "Advanced Topics")
:   [Macro Expansion](chap9.html#1008429 "Advanced Topics")
:   [Redefining Macros](chap9.html#1008432 "Advanced Topics")
:   [defmacro](chap9.html#1008436 "Advanced Topics")
:   [mprocedure](chap9.html#1008442 "Advanced Topics")
:   [Using the Backquote (](chap9.html#1008446 "Advanced Topics")`` ` ``) Operator with defmacro
:   [Using an @rest Argument with defmacro](chap9.html#1008456 "Advanced Topics")
:   [Using @key Arguments with defmacro](chap9.html#1008467 "Advanced Topics")

[Variables](chap9.html#1008477 "Advanced Topics")

:   [Lexical Scoping](chap9.html#1008482 "Advanced Topics")
:   [Dynamic Scoping](chap9.html#1008489 "Advanced Topics")
:   [Dynamic Globals](chap9.html#1008499 "Advanced Topics")

[Error Handling](chap9.html#1008505 "Advanced Topics")

:   [The errset Function](chap9.html#errset "Advanced Topics")
:   [Using err and errset Together](chap9.html#1008522 "Advanced Topics")
:   [The error Function](chap9.html#1008529 "Advanced Topics")
:   [The warn Function](chap9.html#1008538 "Advanced Topics")
:   [The getWarn Function](chap9.html#1008543 "Advanced Topics")
:   [The](chap9.html#1012613 "Advanced Topics") `throw` and `catch`functions

[Top Levels](chap9.html#1008553 "Advanced Topics")

[Memory Management (Garbage Collection)](chap9.html#1008565 "Advanced Topics")

:   [How to Work with Garbage Collection](chap9.html#1008572 "Advanced Topics")
:   [Printing Summary Statistics](chap9.html#1017628 "Advanced Topics")
:   [Allocating Space Manually](chap9.html#1008654 "Advanced Topics")

[Exiting SKILL](chap9.html#1008660 "Advanced Topics")

[10](chap10.html#1005655 "Delivering Products")
-----------------------------------------------

[Delivering Products](chap10.html#1008199 "Delivering Products")
----------------------------------------------------------------

[Contexts](chap10.html#1008203 "Delivering Products")

:   [Deciding When to Use Contexts](chap10.html#1010943 "Delivering Products")
:   [Creating Contexts](chap10.html#1008254 "Delivering Products")
:   [Creating Utility Functions](chap10.html#1008310 "Delivering Products")
:   [Building the Contexts](chap10.html#1008322 "Delivering Products")
:   [Initializing Contexts](chap10.html#1008334 "Delivering Products")
:   [Loading Contexts](chap10.html#1008346 "Delivering Products")
:   [Customizing External Contexts](chap10.html#1008369 "Delivering Products")
:   [Potential Problems](chap10.html#1008377 "Delivering Products")
:   [Context Building Functions](chap10.html#1008397 "Delivering Products")
:   [Context Version Functions](chap10.html#1014158 "Delivering Products")

[Autoloading Your Functions](chap10.html#1015635 "Delivering Products")

[Autoloading Your Classes](chap10.html#autoloadclass "Delivering Products")

[Encrypting and Compressing Files](chap10.html#1015492 "Delivering Products")

[Protecting Functions and Variables](chap10.html#1008452 "Delivering Products")

:   [Explicitly Protecting Functions](chap10.html#1008457 "Delivering Products")
:   [Protecting Variables](chap10.html#1008474 "Delivering Products")
:   [Global Function Protection](chap10.html#1008489 "Delivering Products")

[11](chap11.html#1005655 "Writing Style")
-----------------------------------------

[Writing Style](chap11.html#1010111 "Writing Style")
----------------------------------------------------

[Code Layout](chap11.html#1008218 "Writing Style")

:   [Comments and Documentation](chap11.html#1008220 "Writing Style")
:   [Function Calls and Brackets](chap11.html#1008242 "Writing Style")
:   [Commas](chap11.html#1008271 "Writing Style")

[Using Globals](chap11.html#1008275 "Writing Style")

[Coding Style Mistakes](chap11.html#1008293 "Writing Style")

:   [Inefficient Use of Conditionals](chap11.html#1008296 "Writing Style")
:   [Misusing prog and Conditionals](chap11.html#1008310 "Writing Style")

[Red Flags](chap11.html#1008333 "Writing Style")

:   [Any Use of eval or evalstring](chap11.html#1008336 "Writing Style")
:   [Excessive Use of reverse and append](chap11.html#1008338 "Writing Style")
:   [Excessive Use of gensym and concat](chap11.html#1008340 "Writing Style")
:   [Overuse of the Functions Combining car and cdr](chap11.html#1008342 "Writing Style")
:   [Use of eval Inside Macros](chap11.html#1008344 "Writing Style")
:   [Misuse of prog and return in SKILL++ mode](chap11.html#1010226 "Writing Style")

[12](chap12.html#1005655 "Optimizing SKILL")
--------------------------------------------

[Optimizing SKILL](chap12.html#1008199 "Optimizing SKILL")
----------------------------------------------------------

[Optimizing Techniques](chap12.html#1011309 "Optimizing SKILL")

:   [Macros](chap12.html#1008228 "Optimizing SKILL")
:   [Caching](chap12.html#1008232 "Optimizing SKILL")
:   [Mapping and Qualifying](chap12.html#1008247 "Optimizing SKILL")
:   [Write Protection](chap12.html#1008256 "Optimizing SKILL")
:   [Minimizing Memory](chap12.html#1008264 "Optimizing SKILL")
:   [Tail-Call Optimization](chap12.html#tail_call "Optimizing SKILL")

[General Optimizing Tips](chap12.html#1012537 "Optimizing SKILL")

:   [Element Comparison](chap12.html#1008287 "Optimizing SKILL")
:   [List Accessing](chap12.html#1008327 "Optimizing SKILL")
:   [List Building](chap12.html#1008330 "Optimizing SKILL")
:   [List Searching](chap12.html#1008381 "Optimizing SKILL")
:   [List Sorting](chap12.html#1008386 "Optimizing SKILL")
:   [Element Removal and Replacing](chap12.html#1008389 "Optimizing SKILL")
:   [Alternatives to Lists](chap12.html#1008394 "Optimizing SKILL")

[Miscellaneous Comparative Timings](chap12.html#1008399 "Optimizing SKILL")

:   [Element Comparison](chap12.html#1008403 "Optimizing SKILL")
:   [List Building](chap12.html#1008412 "Optimizing SKILL")
:   [Mapping Functions](chap12.html#1008425 "Optimizing SKILL")
:   [Data Structures](chap12.html#1008436 "Optimizing SKILL")

[13](chap13.html#1005655 "About SKILL++ and SKILL")
---------------------------------------------------

[About SKILL++ and SKILL](chap13.html#1008199 "About SKILL++ and SKILL")
------------------------------------------------------------------------

[Background Information about SKILL and Scheme](chap13.html#1012100 "About SKILL++ and SKILL")

[Relating SKILL++ to IEEE and CFI Standard Scheme](chap13.html#1008239 "About SKILL++ and SKILL")

:   [Syntax Differences](chap13.html#1008246 "About SKILL++ and SKILL")
:   [Semantic Differences](chap13.html#1008260 "About SKILL++ and SKILL")
:   [Syntax Options](chap13.html#1008281 "About SKILL++ and SKILL")
:   [Compliance Disclaimer](chap13.html#1008293 "About SKILL++ and SKILL")
:   [References](chap13.html#1008300 "About SKILL++ and SKILL")

[Extension Language Environment](chap13.html#1008308 "About SKILL++ and SKILL")

[Contrasting Variable Scoping](chap13.html#1008383 "About SKILL++ and SKILL")

:   [SKILL++ Uses Lexical Scoping](chap13.html#1008390 "About SKILL++ and SKILL")
:   [SKILL Uses Dynamic Scoping](chap13.html#1008394 "About SKILL++ and SKILL")
:   [Lexical versus Dynamic Scoping](chap13.html#1012754 "About SKILL++ and SKILL")
:   [Example 1: Sometimes the Scoping Rules Agree](chap13.html#1012756 "About SKILL++ and SKILL")
:   [Example 2: When Dynamic and Lexical Scoping Disagree](chap13.html#1008404 "About SKILL++ and SKILL")
:   [Example 3: Calling Sequence Effects on Memory Location](chap13.html#1008410 "About SKILL++ and SKILL")

[Contrasting Symbol Usage](chap13.html#1008428 "About SKILL++ and SKILL")

:   [How SKILL Uses Symbols](chap13.html#1008430 "About SKILL++ and SKILL")
:   [How SKILL++ Uses Symbols](chap13.html#1008529 "About SKILL++ and SKILL")

[Contrasting the Use of Functions as Data](chap13.html#1008533 "About SKILL++ and SKILL")

:   [Assigning a Function Object to a Variable](chap13.html#1008536 "About SKILL++ and SKILL")
:   [Passing a Function as an Argument](chap13.html#1008544 "About SKILL++ and SKILL")

[SKILL++ Closures](chap13.html#1008568 "About SKILL++ and SKILL")

:   [Relationship to Free Variables](chap13.html#1008571 "About SKILL++ and SKILL")
:   [How SKILL++ Closures Behave](chap13.html#1008579 "About SKILL++ and SKILL")

[SKILL++ Environments](chap13.html#1008606 "About SKILL++ and SKILL")

:   [The Active Environment](chap13.html#1008615 "About SKILL++ and SKILL")
:   [The Top-Level Environment](chap13.html#1008621 "About SKILL++ and SKILL")
:   [Creating Environments](chap13.html#1008629 "About SKILL++ and SKILL")
:   [Functions and Environments](chap13.html#1008697 "About SKILL++ and SKILL")
:   [Persistent Environments](chap13.html#1008725 "About SKILL++ and SKILL")

[14](chap14.html#1005655 "Using SKILL++")
-----------------------------------------

[Using SKILL++](chap14.html#1008199 "Using SKILL++")
----------------------------------------------------

[Declaring Local Variables in SKILL++](chap14.html#1008217 "Using SKILL++")

:   [Using let](chap14.html#1008222 "Using SKILL++")
:   [Using letseq](chap14.html#1008242 "Using SKILL++")
:   [Using letrec](chap14.html#1008263 "Using SKILL++")
:   [Using procedure to Declare Local Functions](chap14.html#1008274 "Using SKILL++")

[Sequencing and Iteration](chap14.html#1008294 "Using SKILL++")

:   [Using begin](chap14.html#1008301 "Using SKILL++")
:   [Using do](chap14.html#1008312 "Using SKILL++")
:   [Using a Named let](chap14.html#1008348 "Using SKILL++")

[Software Engineering with SKILL++](chap14.html#1008365 "Using SKILL++")

[SKILL++ Packages](chap14.html#1008377 "Using SKILL++")

:   [The Stack Package](chap14.html#1008384 "Using SKILL++")
:   [Retrofitting a SKILL API as a SKILL++ Package](chap14.html#1008392 "Using SKILL++")
:   [SKILL++ Modules](chap14.html#1008400 "Using SKILL++")
:   [Stack Module Example](chap14.html#1008412 "Using SKILL++")
:   [The Container Module](chap14.html#1008460 "Using SKILL++")

[15](chap15.html#1005655 "Using SKILL and SKILL++ Together")
------------------------------------------------------------

[Using SKILL and SKILL++ Together](chap15.html#1008199 "Using SKILL and SKILL++ Together")
------------------------------------------------------------------------------------------

[Selecting an Interactive Language](chap15.html#1008234 "Using SKILL and SKILL++ Together")

:   [Starting an Interactive Loop (toplevel)](chap15.html#1008241 "Using SKILL and SKILL++ Together")
:   [Exiting the Interactive Loop (resume)](chap15.html#1008253 "Using SKILL and SKILL++ Together")

[Partitioning Your Source Code](chap15.html#1008259 "Using SKILL and SKILL++ Together")

[Cross-Calling Guidelines](chap15.html#1008269 "Using SKILL and SKILL++ Together")

:   [Avoid Calling SKILL Functions That Call eval, symeval, or evalstring](chap15.html#1008278 "Using SKILL and SKILL++ Together")
:   [Avoid Calling nlambda Functions](chap15.html#1008281 "Using SKILL and SKILL++ Together")
:   [Use the set Function with Care](chap15.html#1008289 "Using SKILL and SKILL++ Together")

[Redefining Functions](chap15.html#1008297 "Using SKILL and SKILL++ Together")

[Sharing Global Variables](chap15.html#1008301 "Using SKILL and SKILL++ Together")

:   [Using importSkillVar](chap15.html#1008304 "Using SKILL and SKILL++ Together")
:   [How importSkillVar Works](chap15.html#1008315 "Using SKILL and SKILL++ Together")
:   [Evaluating an Expression with SKILL Semantics](chap15.html#1008322 "Using SKILL and SKILL++ Together")

[Debugging SKILL++ Applications](chap15.html#1008329 "Using SKILL and SKILL++ Together")

:   [Examining the Source Code for a Function Object](chap15.html#1008336 "Using SKILL and SKILL++ Together")
:   [Pretty-Printing Package Functions](chap15.html#1008344 "Using SKILL and SKILL++ Together")
:   [Inspecting Environments](chap15.html#1008347 "Using SKILL and SKILL++ Together")
:   [Retrieving the Active Environment](chap15.html#1008355 "Using SKILL and SKILL++ Together")
:   [Testing Variables in an Environment (boundp)](chap15.html#1008365 "Using SKILL and SKILL++ Together")
:   [Using the -> Operator with Environments](chap15.html#1008371 "Using SKILL and SKILL++ Together")
:   [Using the ->?? Operator with Environments](chap15.html#1008379 "Using SKILL and SKILL++ Together")
:   [Evaluating an Expression in an Environment (eval)](chap15.html#1008384 "Using SKILL and SKILL++ Together")
:   [Examining Closures](chap15.html#1008394 "Using SKILL and SKILL++ Together")
:   [General SKILL Debugger Commands](chap15.html#1008410 "Using SKILL and SKILL++ Together")

[16](chap16.html#1005655 "SKILL++ Object System")
-------------------------------------------------

[SKILL++ Object System](chap16.html#1008199 "SKILL++ Object System")
--------------------------------------------------------------------

[Basic Concepts](chap16.html#1008217 "SKILL++ Object System")

:   [Classes and Instances](chap16.html#1008219 "SKILL++ Object System")
:   [Generic Functions and Methods](chap16.html#generic functions "SKILL++ Object System")
:   [Subclasses and Superclasses](chap16.html#1008238 "SKILL++ Object System")
:   [Defining a Class (defclass)](chap16.html#1016021 "SKILL++ Object System")
:   [Instantiating a Class (makeInstance)](chap16.html#1013605 "SKILL++ Object System")
:   [Initializing an Instance (initializeInstance)](chap16.html#1014872 "SKILL++ Object System")
:   [Reading and Writing Instance Slots](chap16.html#1017762 "SKILL++ Object System")
:   [Defining a Generic Function (defgeneric)](chap16.html#defgeneric "SKILL++ Object System")
:   [Defining a Method (defmethod)](chap16.html#1008323 "SKILL++ Object System")
:   [Defining Method Combinations (@before, @after, and @around)](chap16.html#method_combination "SKILL++ Object System")
:   [Multi-Method Dispatch](chap16.html#1015033 "SKILL++ Object System")

[Class Hierarchy](chap16.html#1016722 "SKILL++ Object System")

[Browsing the Class Hierarchy](chap16.html#1008418 "SKILL++ Object System")

:   [Getting the Class Object from the Class Name](chap16.html#1008425 "SKILL++ Object System")
:   [Getting the Class Name from the Class Object](chap16.html#1008429 "SKILL++ Object System")
:   [Getting the Class of an Instance](chap16.html#1008434 "SKILL++ Object System")
:   [Getting the Class of the Environment Object (envObj)](chap16.html#1015699 "SKILL++ Object System")
:   [Getting the Superclasses of an Instance](chap16.html#1015633 "SKILL++ Object System")
:   [Checking if an Object Is an Instance of a Class](chap16.html#1008444 "SKILL++ Object System")
:   [Checking if One Class Is a Subclass of Another](chap16.html#1008453 "SKILL++ Object System")

[Advanced Concepts](chap16.html#1008466 "SKILL++ Object System")

:   [Method Argument Restrictions](chap16.html#1008470 "SKILL++ Object System")
:   [Applying a Generic Function](chap16.html#1020260 "SKILL++ Object System")
:   [Incremental Development](chap16.html#1008502 "SKILL++ Object System")
:   [Methods versus Slots](chap16.html#1008515 "SKILL++ Object System")
:   [Sharing Private Functions and Data Between Methods](chap16.html#1008519 "SKILL++ Object System")

[17](chap17.html#1005655 "Programming Examples")
------------------------------------------------

[Programming Examples](chap17.html#1008199 "Programming Examples")
------------------------------------------------------------------

[List Manipulation](chap17.html#1008203 "Programming Examples")

[Symbol Manipulation](chap17.html#1008215 "Programming Examples")

[Sorting a List of Points](chap17.html#1008233 "Programming Examples")

[Computing the Center of a Bounding Box](chap17.html#1008248 "Programming Examples")

[Computing the Area of a Bounding Box](chap17.html#1008263 "Programming Examples")

[Computing a Bounding Box Centered at a Point](chap17.html#1008271 "Programming Examples")

[Computing the Union of Several Bounding Boxes](chap17.html#1008282 "Programming Examples")

[Computing the Intersection of Bounding Boxes](chap17.html#1008293 "Programming Examples")

[Prime Factorizations](chap17.html#1008301 "Programming Examples")

:   [Evaluating a Prime Factorization](chap17.html#1008307 "Programming Examples")
:   [Computing the Prime Factorization](chap17.html#1008330 "Programming Examples")
:   [Multiplying Two Prime Factorizations](chap17.html#1008355 "Programming Examples")
:   [Using Prime Factorizations to Compute the GCD](chap17.html#1008369 "Programming Examples")

[Fibonacci Function](chap17.html#1008381 "Programming Examples")

[Factorial Function](chap17.html#1008390 "Programming Examples")

[Exponential Function](chap17.html#1008395 "Programming Examples")

[Counting Values in a List](chap17.html#1008400 "Programming Examples")

[Counting Characters in a String](chap17.html#1008422 "Programming Examples")

[Regular Expression Pattern Matching](chap17.html#1008430 "Programming Examples")

[Geometric Constructions](chap17.html#1009907 "Programming Examples")

:   [Application Domain](chap17.html#1008450 "Programming Examples")
:   [Implementation](chap17.html#1008480 "Programming Examples")
:   [Classes](chap17.html#1008492 "Programming Examples")
:   [Generic Functions](chap17.html#1008522 "Programming Examples")
:   [Describing the Methods by Class](chap17.html#1008529 "Programming Examples")
:   [Source Code](chap17.html#1008668 "Programming Examples")
:   [Extending the Implementation](chap17.html#1008703 "Programming Examples")

[Index](sklanguserIX.html#1036761 "Index")
------------------------------------------




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
