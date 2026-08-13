### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

8
=

Advanced List Operations
========================

["Getting Started"](chap1.html#1008199 "Getting Started") introduces you to building Cadence® SKILL language lists. Information in this chapter helps you perform more advanced list operations.

It is helpful to understand how lists are stored in virtual memory so that you can understandhow SKILL functions such as `car` and `cdr` manipulate lists and the issues behind building long lists efficiently (see ["Conceptual Background"](#1008211 "Advanced List Operations")).

You can read more about the following topics:

* [Summary of List Operations](#1008388 "Advanced List Operations")

* [Altering List Cells](#1008504 "Advanced List Operations")

* [Accessing Lists](#1018204 "Advanced List Operations")

* [Building Lists Efficiently](#1008608 "Advanced List Operations")

* [Reorganizing a List](#1008772 "Advanced List Operations")

* [Searching Lists](#1008798 "Advanced List Operations")

* [Copying Lists](#1008824 "Advanced List Operations")

* [Filtering Lists](#1008839 "Advanced List Operations")

* [Removing Elements from a List](#1008850 "Advanced List Operations")

* [Substituting Elements](#1008902 "Advanced List Operations")

* [Transforming Elements of a Filtered List](#1008910 "Advanced List Operations")

* [Validating Lists](#1008924 "Advanced List Operations")

* [Using Mapping Functions to Traverse Lists](#1008951 "Advanced List Operations")

* [List Traversal Case Studies](#1009072 "Advanced List Operations")

Conceptual Background
---------------------

### How Lists Are Stored in Virtual Memory

SKILL functions that manipulate lists and symbols are actually dealing with memory pointers.When you assign a list to a variable, the variable is internally assigned a pointer to the head of the list. When a list is taken apart by functions such as `car` and `cdr`, only pointers to various parts of the list are returned and no new list cells are created.

SKILL suppresses your awareness of pointers by how it displays lists and symbols. Ingeneral, when SKILL displays a supported data type, it uses a characteristic syntax to suppress irrelevant detail and focus on the essentials of the data. This syntax has implications for list and symbol data types. Instead of displaying memory addresses, SKILL displays

* The elements of a list surrounded by parentheses

* The name of a symbol

#### A SKILL List as a List Cell

SKILL represents a list by means of a list cell. A list cell occupies two locations in virtual memory.

* The first location holds a reference to the first element in the list.

* The second location holds a reference to the tail of the list, that is, another list cell or`nil`.

The expression`aList = '( 2 3 4 )` allocates the following three list cells.

The`car` function returns the contents of the first location of a list cell.

`car( aList) => 2`

The`cdr` function returns the contents of the second location of a list cell.

`cdr( aList) => (3 4)`

#### Lists Containing Sublists

The expression`bList = '( 1 ( 2 3 4 ) 5 )` allocates the following list cells.

`cadr(bList) => (2 3 4)`

#### Lists Containing Symbols

The expression`bList = '( 1 ( 2 a a ) b )` allocates the following list cells.

Internally the expression`'a` returns the pointer to the symbol `a` in the symbol table.

### Destructive versus Non-Destructive Operations

#### Non-Destructive Operations

The term`non-destructive modification` refers to any operation that allocates a copy of a list that reflects the desired alteration. The original list is not altered. It is your responsibility to update any variables that need to reflect the operation.

Such operations are generally easier for you to implement than destructive operations that doalter the original list. The disadvantage is that making an altered copy of the original list might be significantly time-consuming.

#### Destructive Operations

The term`destructive list modification` refers to any operation that alters either the car or cdr of a list cell. Destructive modification functions do not need to create new list structures. They are therefore considerably faster than equivalent nondestructive modification functions.

Depending on the operation, any variable referring to the original list can be affected. Manysubtle problems can arise when these functions are used without a thorough understanding of the implications.

* ***You should only use the destructive modification functions described inthis chapter with a very good understanding of how the SKILL language represents lists in virtual memory.***

Summary of List Operations
--------------------------

The following table summarizes the list operations that are discussed in this chapter. Use the destructive modification functions with great care.

**List Operations**

| **Operation** | **Function** | **Non-destructive** | **Destructive**
| Altering List Cells | rplaca, rplacd |  | x
| Accessing a List | nthelem, nthcdr, last | x |
| Building a List | cons, ncons, xcons,append1 | x |
| tconc, nconc, lconc |  | x
| Reorganizing a List | reverse | x |
| sort, sortcar |  | x
| Removing Elements | remove, remq | x |
| remd, remdq |  | x
| Searching Lists | member, memq, exists | x |
| Filtering Lists | setof | x |
| Substituting | subst | x |
| Traversal | mapc, map, mapcar,maplist, mapcan | x |
| Traversal | mapcan |  | x
Altering List Cells
-------------------

The most fundamental destructive operations concern altering a list cell. You can changeeither the `car` cell or the `cdr` cell. `rplac`a and `rplacd` are destructive operations. Starting from IC6.1.6, a new function, `setf`, has been introduced for altering a list cell.

### The rplaca Function

Use the`rplaca` function to replace the first element of a list.

```
aList = '( 1 2 3) => ( 1 2 3 )bList = rplaca( aList 4 ) => ( 4 2 3 )aList => ( 4 2 3 )eq( aList bList ) => t
```

### The rplacd Function

Use the`rplacd` function to replace the tail of a list.

```
aList = '( 1 2 3 ) => ( 1 2 3 )bList = rplacd( aList '( 4 5 ) ) => ( 1 4 5 )aList => ( 1 4 5 )eq( aList bList ) => t
```

Notice that the`rplacd` function returns a list with the desired modifications. An important point to remember about destructive operations is that the modified list is literally the same list in virtual memory as the original list. To verify this fact, use the `eq` function, which returns `t` if both arguments are the same object in virtual memory.

### The setf function

The`setf` function assigns a new value to an existing storage location, destroying the value that was previously in that location. Basically, the function expands into an update form that takes the first argument as a *reference location*,evaluates the second argument, and stores the result of evaluating the second argument (new value) in the *reference location*. For example,

`x = '(a b c d e)`

`setf((car x) 42)`

displays the following return value:

`(42 b c d e)`

A main objective of the`setf` function is to allow you to write your own `setf` expanders/functions defines as `setf_<expanders>`) so that you can use it with your macros and functions. This means that if you want to write a`setf` function to work with a method, you need to write a defmethod form. Also, in SKILL, a generic function must be named by a symbol, so setf\_ is concatenated to the getter function name, such as `setf_GetRandomVal` in the example given below.

`defgeneric(GetRandomVal (obj))`

`defclass( Random () ())`

`defclass( SemiRandom (Random)`

`(nextval( @initform nil)))`

`defmethod( GetRandomVal ((self Random))`

`(random))`

`defmethod( GetRandomVal ((self SemiRandom))`

`if( self->nextval`

`(prog1`

`self->nextval`

`self->nextval = nil)`

`(callNextMethod))`

`)`

`defmethod( setf_GetRandomVal (value (self Random))`

`error( "Random objects may not have their random value set"))`

`defmethod( setf_GetRandomVal ((value fixnum) (self SemiRandom))`

`self->nextval = value`

`)`

The list of`setf_ expanders` available in SKILL Language are as follows: setf helpers: (public functions)

|
| ---
| `setf_car`
| `setf_cdr`
| `setf_cadr`
| `setf_caar`
| `setf_cdar`
| `setf_cddr`
| `setf_caaar`
| `setf_caadr`
| `setf_cadar`
| `setf_cdaar`
| `setf_caddr`
| `setf_cddar`
| `setf_cdadr`
| `setf_cdddr`
| `setf_last`
| `setf_arrayref`
| `setf_nth`
| `setf_nthelem`
| `setf_nthcdr`
| `setf_xCoord`
| `setf_yCoord`
| `setf_leftEdge`
| `setf_rightEdge`
| `setf_bottomEdge`
| `setf_topEdge`
| `setf_upperRight`
| `setf_lowerLeft`
| `setf_getd`
| `setf_get`
| `setf_getq`
| `setf_getSGq`
| `setf_slotValue`
| `setf_getShellEnvVar`
Consider an example of using the`setf_cadr` helper function:

`data = list(1 2 3 4 5)`

`setf((cadr data) 42)`

The return value is:

`(1 42 3 4 5)`

Accessing Lists
---------------

The following functions are convenient variations and extensions of the`cdr`and`nth` functions introduced in ["Getting Started"](chap1.html#1008199 "Getting Started").

### Selecting an Indexed Element from a List (nthelem)

`nthelem` returns an indexed element of a list, assuming a one-based index. Thus `nthelem(1``l_list)` is the same as `car(l_list)`.

```
nthelem( 1 '( a b c ) )     => az = '( 1 2 3 )nthelem( 2 z )                             => 2
```

### Applying cdr to a List a Given Number of Times (nthcdr)

You supply the iterationcount and the list of elements.

```
nthcdr( 3 '( a b c d ))     => (d)z = '( 1 2 3 )nthcdr( 2 z )                               => ( 3 )
```

### Getting the Last List Cell in a List (last)

`last` returns the last list cell in a list. The `car` of the last list cell is the last element in the list. The `cdr` of the last list cell is `nil`.

`last( '(a b c) ) => (c)z = '( 1 2 3 )last( z )        => (3)`

Building Lists Efficiently
--------------------------

To build lists efficiently, you must understand how lists are constructed. Using a function like`append` involves searching for the end of a list, which can be unacceptably slow for large lists.

### Adding Elements to the Front of a List (cons, xcons)

If order is unimportant, the easiest way to build a list is to repeatedly call`cons` to add new elements at the head of the list.

The`cons` function allocates a new list cell consisting of two memory locations. It stores its first argument in the first location and its second argument in the second location.

The`cons` function returns a list whose first element is the one you supplied (1 below) and whose `cdr` is the list you supplied (aList below). The expressions

`aList = '( 2 3 4 )aList = cons( 1 aList ) => (1 2 3 4 )`

allocate the following.

`xcons` accepts the same arguments as the `cons` function, but in reverse order. `xcons` adds an element to the beginning of a list, which can be `nil`.

`xcons( '( b c ) 'a ) => ( a b c )`

### Building a List with a Given Element (ncons)

ncons builds a list by adding the `element` you supply to the beginning of an empty list. It is equivalent to `cons( g_element nil )`.

```
ncons( 'a )      => ( a )         ;;; equivalent to cons( 'a nil )z = '( 1 2 3 )ncons( z )      => ( ( 1 2 3 ) ) ;;; equivalent to cons( z nil )
```

### Adding Elements to the End of a List (tconc)

Because lists are singly linked in only one direction, searching for the end of a list typicallyrequires the traversal of every list cell in the list, which can be quite slow with a long list containing many list cells. This long traversal poses a problem when you want to build a list by adding elements at the end of a list. If a list must be built by adding new elements at the end of the list, the most efficient way is to use `tconc`.

The`tconc` function creates a list cell (known as a `tconc` structure) whose `car` points to the head of the list being built and whose `cdr` points to the last element of the list.

The`tconc` structure allows subsequent calls to `tconc` to find the end of a list instantly without having to traverse the entire list. For this reason, call `tconc` once to initialize a special list cell and pass this special list cell to subsequent calls on `tconc`. Finally, to obtain the actual value of the list you have been building, take the `car` of this special list cell. The typical steps required to use `tconc` are as follows:

* Create the`tconc` structure by calling `tconc` with `nil` as its first argument and the first element of the list being built as the second argument.

> `x = tconc(nil 1 )`

* Repeatedly call`tconc` with other elements to be added to the end of the list, each time giving the `tconc` structure as the first argument to `tconc`. There is no need to assign the value returned by `tconc` to a variable because `tconc` modifies the `tconc` structure. For example:

> `tconc(x 2 ), tconc(x 3 ) …`

* After the list has been built, take the`car` of the `tconc` structure to get the actual value of the list being built. For example:

> `x = car(x)`

### Appending Lists

#### The nconc Function

Use the`nconc` function to quickly append lists destructively. The `nconc` function takes two or more lists as arguments. Only the last argument list is unaltered.

```
cList = '( 1 2 )dList = '( 3 4 5 )eList = '( 6 7 )nconc( cList dList eList ) => ( 1 2 3 4 5 6 7 )cList => ( 1 2 3 4 5 6 7 )dList => ( 3 4 5 6 7 )eList => ( 6 7 )
```

Use the`apply` function and the `nconc` function to append a list of lists.

`apply( 'nconc '( ( 1 2 ) ( 3 4 5 ) ( 6 7 )) )=> (1 2 3 4 5 6 7 )`

#### The lconc Function

`lconc` uses a `tconc` structure to efficiently splice lists to the end of lists. The `tconc` structure must initially be created using the `tconc` function. See the example below.

```
x = tconc(nil 1)             ; x is initialized ((1) 1)lconc(x '(2 3 4))            ; x is now ((1 2 3 4) 4)lconc(x nil)                 ; Nothing is added to x.lconc(x '(5))                ; x is now ((1 2 3 4 5) 5)x = car( x )                 ; x is now (1 2 3 4 5)
```

Reorganizing a List
-------------------

SKILL provides several functions that reorganize a list. Sometimes the most efficient way tobuild a list is to reverse it or sort it after you have built it incrementally with the `cons` function. These functions change the sequence of the top-level elements of your list.

### Reversing a List

The following is a non-destructive operation.

#### Reversing the Order of Elements in a List (reverse)

`reverse` returns the top-level elements of a list in reverse order.

```
aList = '( 1 2 3 )aList = reverse( aList ) => ( 3 2 1 )anotherList = '( 1 2 ( 3 4 5 ) 6 )reverse( anotherList ) => ( 6 ( 3 4 5 ) 2 1 )
```

Although`reverse( anotherList )` returns the list in reverse order, the value of `anotherList`, the original list, is not modified. It is your responsibility to update any variables that you want to reflect this reversal.

`anotherList => ( 1 2 ( 3 4 5 ) 6 )`

### Sorting Lists

The following functions are helpful when you must sort lists according to various criteria andlocate elements within lists. They are destructive operations.

#### The sort Function

The syntax statement for the`sort` function is

`sort( l_data u_comparefn ) => l_result`

`sort` sorts a list of objects (`l_data`) according to the `sort` function (`u_comparefn`) you supply. `u_comparefn( g_x g_y )` returns non-`nil` if `g_x` can precede `g_y` in sorted order and `nil` if `g_y` must precede `g_x`. If `u_comparefn` is `nil`, alphabetical order is used. The algorithm in `sort` is based on recursive merge sort.

```
sort( '(4 3 2 1) 'lessp )         => (1 2 3 4)sort( '(d b c a) 'alphalessp) => (a b c d)
```

#### The sortcar Function

`sortcar` is similar to `sort` except that only the `car` of each element in a list is used for comparison by the sort function.

`sortcar( '((4 four) (3 three) (2 two)) 'lessp )=> ((2 two) (3 three) (4 four)`

`sortcar( '((d 4) (b 2) (c 3) (a 1)) nil )=> ((a 1) (b 2) (c 3) (d 4))`

The list is modified in place and no new storage is allocated. Pointers previously pointing tothe list might not be pointing at the head of the sorted list.

Searching Lists
---------------

SKILL provides several functions for locating elements within a list that satisfy a criterion. Themost basic criterion is equality, which in SKILL can mean either `value equality` or `memory address equality`.

### The member Function

The`member` function is briefly discussed in ["Getting Started"](chap1.html#1008199 "Getting Started"). It uses the `equal` function as the basis for finding a top-level element in a list. The `member` function

* Returns`nil` if the element is not equal to any top-level element in the list.

* Returns the first tail of the list that starts with the element.

Some examples include

`member( 3 '( 2 3 4 3 5 )) => (3 4 3 5)member( 6 '( 2 3 4 3 5 )) => nil`

The`member` function resembles the `cdr` function in that it internally returns a pointer to a list cell. The `car` of the list cell is equal to the element. You can use the `member` function with the `rplaca` function to destructively substitute one element for the first top-level occurrence of another in a list. For example, find the first occurrence of 3 and replace it with 6:

`rplaca(       member( 3 '( 2 3 4 3 5 ))       6 )`

SKILL provides a non-destructive`subst` function for substituting an element at all levels of a list. See ["Substituting Elements"](#1008902 "Advanced List Operations").

### The memq Function

The`memq` function is the same as the `member` function except that it uses the `eq` function for finding the element. Because the `eq` function is more efficient than the `equal` function, use `memq` whenever possible based on the nature of the data. For example, if the list to search contains only symbols, then using the `memq` function is more efficient than using the `member` function.

### The exists Function

The`exists` function can use an application-specific testing function to locate the first occurrence of an element in a list. The `exists` function generalizes the `member` and `memq` functions, which locate the first occurrence of an element in a list based on equality.

```
exists( x '( 2 4 7 8 ) oddp( x ) ) => ( 7 8 )exists( x '( 2 4 6 8 ) evenp( x ) ) => ( 2 4 6 8 )
```

```
exists( x '(1 2 3 4) (x > 1) )    => (2 3 4)exists( x '(1 2 3 4) (x > 4) )    => nil
```

Copying Lists
-------------

Sometimes it is more efficient to apply a destructive operation to a copy of a list than it is toapply a non-destructive operation. First determine whether a shallow copy of only the top-level elements is sufficient.

### The copy Function

`copy` returns a copy of a list. copy only duplicates the top-level list cells. All lower-level objects are still shared. You should consider making a copy of any list before using a destructive modification on the list.

```
z = '(1 (2 3) 4)  => (1 (2 3) 4)x = copy(z)       => (1 (2 3) 4)equal(z x)        => t
```

z and x have the same value.

`eq(z x)          => nil`

z and x are not the same list.

### Copying a List Hierarchically

The following function recursively copies a list.

```
procedure( trDeepCopy( arg )      cond(             ( !arg nil )            ( listp( arg );;; argument is a list                   cons(                         trDeepCopy( car( arg ) )                        trDeepCopy( cdr( arg ) )                        )                  )            ( t arg ) ;;; return the argument itself            ) ; cond      ) ; procedure
```

Filtering Lists
---------------

Many list operations can be abstractly considered as making a filtered copy of a list. The filtercan be any function that accepts a single argument. If the filter function returns non-`nil,` the element is included in the new list. If the filter function returns `nil`, the element is excluded from the new list.

`setof` makes a filtered copy of the top-level elements of a list, including all elements that satisfy a given criteria. For example, contrast the following two approaches to computing the intersection of two lists.

* One way to proceed is to use the`cons` function as follows:

> ```
> procedure( trIntersect( list1 list2 )      let( ( result )            foreach( element1 list1                  when( member( element1 list2 )                        result = cons( element1 result )                        ) ; when                  ) ; foreach            result            ) ; let      ) ; procedure
> ```

* The more efficient way is as follows:

> ```
> procedure( trIntersect( list1 list2 )      setof(             element list1             member( element list2 ) )      ) ; procedure
> ```

The criteria is used to decide whether to include each element of the list. The copied elementis not transformed.

Removing Elements from a List
-----------------------------

SKILL has several functions that remove all top-level occurrences of an element from a list.

**The Removal Function**

|  | **Non-destructive** | **Destructive**
| Uses equal | remove | remd
| Uses eq | remq | remdq
### Non-Destructive Operations

#### The remove Function

`remove` returns a copy of an argument with all top-level elements equal to a given SKILL object removed. The `equal` function, which implements the = operator, is used to test for equality.

`aList = '( 1 2 3 4 5 )remove( 3 aList ) => ( 1 2 4 5 )aList => ( 1 2 3 4 5 )`

It is your responsibility to make the appropriate assignment so that`aList` reflects the removal.

`aList = remove( 3 aList )`

The element to remove can itself be a list.

`remove( '( 1 2 ) '( 1 ( 1 2 ) 3 )) => ( 1 3 )`

#### The remq Function

`remq` returns a copy of an argument list with all top-level elements equal to a given SKILL object removed. The `eq` function is used to test for equality. This function is faster than the `remove` function because the `eq` equality test is faster than the `equal` equality test. However, the `eq` test is only meaningful for certain data types, such as symbols and lists. The `remq` function is appropriate, for example, when dealing with a list of symbols.

`remq( 'x '( a b x d f x g ) ) => ( a b d f g )`

The`remq` function does not work on association tables.

### Destructive Operations

#### The remd Function

remd removes all top-level elements equal to a given SKILL object from a list. remd uses equal for comparison. This is a destructive removal.

`remd( "x" '("a" "b" "x" "d" "f")) => ("a" "b" "d" "f")`

#### The remdq Function

`remdq` removes all top-level elements equal to the first argument from a list. `remdq` uses eq instead of equal for comparison. This is a destructive removal.

remdq('x '(a b x d f x g)) => (a b d f g)

Substituting Elements
---------------------

The`subst` function is a non-destructive operation. It is your responsibility to update any variables that you want to reflect this substitution.

#### Substituting One Object for Another Object in a List (subst)

`subst` returns the result of substituting the `new object` (first argument) for all equal occurrences of the `previous object`(second argument) at all levels in a list.

```
aList = '( a b c )            => ( a b c )subst( 'a 'b aList )          => ( a a c )anotherList = '( a b y ( d y ( e y )))subst('x 'y anotherList )     => ( a b x ( d x ( e x )))
```

Although`subst('x 'y anotherList )` returns a list reflecting the desired substitutions, the value of `anotherList`, the original list, is not modified.

`anotherList => ( a b y ( d y ( e y )))`

Transforming Elements of a Filtered List
----------------------------------------

Many list operations can be modeled as a filtering pass followed by a transformational pass.For example, suppose you are given a list of integers and you want to build a list of the squares of the odd integers.

#### Phase I: Filter the odd integers into a list.

You can use the`setof` function here.

`setof( x '( 1 2 3 4 5 6 ) oddp(x)) => ( 1 3 5 )`

#### Phase II: Square each element of the list.

You can use the`mapcar` function together with a function that squares its argument:

```
mapcar(       lambda( (x) x*x ) ;; square my argument      '( 1 3 5 )       ) => ( 1 9 25 )
```

or use the`foreach` function:

`foreach( mapcar x '( 1 3 5 ) x*x ) => ( 1 9 25 )`

The`trListOfSquares` function summarizes this approach.

```
procedure( trListOfSquares( aList )      let( ( filteredList )            filteredList =                   setof( element aList oddp( element ))            foreach( mapcar element filteredList                  element * element                  ) ; foreach            ) ; foreach      ) ; proceduretrListOfSquares( '( 1 2 3 4 5 6 )) => ( 1 9 25 )
```

Validating Lists
----------------

A predicate is a function that validates that a single SKILL object satisfies a criterion. SKILLprovides many basic predicates. (Refer to ["SKILL Predicates"](chap5.html#SKILL Predicates "Arithmetic and Logical Expressions") and ["Type Predicates"](chap5.html#Type Predicates "Arithmetic and Logical Expressions").) Predicates return `t`or`nil`.

SKILL provides the`forall` function and the `exists` function so you can check whether all elements or some elements in a list satisfy a criterion. These two functions correspond to quantifiers in mathematical logic.

* `forall` is represented mathematically as ∀.

* `exists` is represented mathematically as ∃.

The criterion is represented by a SKILL expression with a single argument that you identifyas the first argument to the `forall` or `exists` function.

### The forall Function

`forall` verifies that an expression remains true for every element in a list. The `forall` function can also be used to verify that an expression remains true for every key/value pair in an association table. (Refer to ["Association Tables"](chap4.html#1008719 "Data Structures") for further details.)

```
forall( x '( 2 4 6 8 ) evenp( x ) ) => tforall( x '( 2 4 7 8 ) evenp( x ) ) => nil
```

### The exists Function

`exists` can use an application-specific testing function to locate the first occurrence of an element in a list based on equality. The `exists` function generalizes the `member` and `memq` functions, which locate the first occurrence of an element in a list based on equality.

```
exists( x '( 2 4 7 8 ) oddp( x ) ) => ( 7 8 )exists( x '( 2 4 6 8 ) evenp( x ) ) => ( 2 4 6 8 )
```

```
exists( x '(1 2 3 4) (x > 1) )    => (2 3 4)exists( x '(1 2 3 4) (x > 4) )    => nil
```

Using Mapping Functions to Traverse Lists
-----------------------------------------

SKILL provides a family of very powerful functions for iterating over lists. For historicalreasons, these are called mapping functions. The mapping functions are `map`, `mapc`, `mapcar`, `mapcan`, `maplist`, and `mapcon`.

All`map`\* functions have the same arguments.

* A function, which must take a single argument

* A list

### Using lambda with the map\* Functions

It is often convenient to use the`lambda` construct to define a nameless function to be used as the first argument.

For example:

```
mapcar(       lambda( ( x ) list( x x**2 )) ;;; return pair of x x**x      '(0 1 2 3 ))      => ( (0 0) (1 1) (2 4) (3 9) )
```

Refer to["Syntax Functions for Defining Functions"](chap3.html#1009085 "Creating Functions in SKILL") for further details on the `lambda` construct.

### Using the map\* Functions with the foreach Function

Alternatively, you can use each mapping function as an option to the`foreach` function. Often, using the `foreach` function results in more understandable code.

For example, the following are equivalent.

```
foreach( mapcar x '( 0 1 2 3 )      list( x x**2 ) ;;; build 2 element list of a x and x*x      )       => ( (0 0) (1 1) (2 4) (3 9) )mapcar(       lambda( ( x ) list( x x**2 )) ;;; return pair of x x**x      '(0 1 2 3 ))
```

The relationship between the two usages of the mapping functions is very tight. When youuse the `foreach` function, SKILL actually incorporates the expressions within the `foreach` body in a `lambda` function as illustrated below. This `lambda` function is passed to the mapping function. For example, the following are equivalent:

```
foreach( mapcar x aList       exp1()      exp2()      exp3()      )mapcar(       lambda( ( x )             exp1()             exp2()             exp3()             )      aList      )
```

The following descriptions illustrate both approaches to using each mapping function.

### The mapc Function

The`mapc` function is the default mapping function used by the `foreach` macro. When used with the `foreach` function

* The`foreach` function iterates over each element of the argument list.

* At each iteration, the current element is available in the loop variable of the`foreach`.

* The`foreach` function returns the original argument list as a result.

For example:

`foreach( mapc x '(1 2 3 4 5)       println(x))`

`mapc(       lambda( ( x ) println( x ) )       '( 1 2 3 4 5 )      )`

displays the following:

`1 2 3 4 5`

The return value is`(1 2 3 4 5)`.

### The map Function

The`map` function is useful for processing each list cell because it uses `cdr` to step down the argument list. When used with the `foreach` function

* The`foreach` function iterates over each list cell of its argument.

* At each iteration, the current list cell is available in the loop variable of the`foreach`.

* The`foreach` function returns the original argument list as a result.

For example, suppose you want to make substitutions at the top-level of a list using a look-uptable such as the following:

`trLookUpList = '(      ( 1 "one" )      ( 2 "two" )      ( 3 "three" ))`

By using the`map` function, you gain access to each successive list cell, allowing you to use the `rplaca` function to make the desired substitution. Notice that the lookup list is an association list so that you can use the `assoc` function to retrieve the appropriate substitution.

`assoc( 2 trLookUpList ) => ( 2 "two" ) assoc( 5 trLookUpList ) => nil`

```
procedure( trTopLevelSubst( aList aLookUpList )      let( ( currentElement substValue )            foreach( map listCell aList                  currentElement = car( listCell )                  substValue = cadr(                         assoc( currentElement aLookUpList ) )                  when( substValue                        rplaca( listCell substValue )                        ) ; when                  ) ; foreach            aList            ) ; let      ) ; procedure
```

```
trList = '( 1 4 5 3 3 )trTopLevelSubst( trList trLookUpList ) =>            ("one" 4 5 "three" "three")
```

### The mapcar Function

The`mapcar` function is useful for building a list whose elements can be derived one-for-one from the elements of an original list. When used with the `foreach` function

* The`foreach` function iterates over each element of the argument list.

* At each iteration, the current element is available in the loop variable of the`foreach`.

* Each iteration produces a result value.

* These values are returned in a list as the result of the function.

For example:

`foreach(mapcar x '(1 2 3 4 5)       println(x)       x*3)`

displays the following:

`1 2 3 4 5`

The return value is`(3 6 9 12 15).`

### The maplist Function

The`maplist` function is useful for processing each list cell because it uses`cdr` to step down the argument list. Like the `mapcar` function, it returns the list of results that it collects for each iteration. When used with the `foreach` function

* The`foreach` function iterates over each list cell of the argument list.

* At each iteration, the current list cell is available in the loop variable of the`foreach`.

* Each iteration produces a result value, and these values are returned in a list as theresult of the `foreach` function.

For example, consider the substitution example illustrating the`map` function. In addition to making the substitutions, suppose that the function must display a message giving the number of substitutions made.

By using`maplist` instead of `map` you can build a list of 1s and Os reflecting the substitutions made. Use the `apply` function with `plus` to add up the numbers to produce the desired count.

```
procedure( trTopLevelSubst( aList aLookUpList )            let( ( currentElement substValue substCountList )            substCountList = foreach( maplist listCell aList                  currentElement = car( listCell )                  substValue = cadr(                         assoc( currentElement aLookUpList ) )                  if( substValue                        then                              rplaca( listCell substValue )                              1                        else                              0                        ) ; if                  ) ; foreach            printf( "There were %d substitutions\n"
```

```
apply( 'plus substCountList )                   )            aList            ) ; let      ) ; procedure trList = '( 1 4 5 3 3 )trTopLevelSubst( trList trLookUpList ) =>      ("one" 4 5 "three" "three")There were 3 substitutions
```

### The mapcon Function

Like the`maplist` function, the `mapcon` function is useful for processing each list cell because it uses`cdr` to step down the argument list. It returns a concatenated list of results that it collects after each iteration. When used with the `foreach` function:

* The`foreach` function iterates over each list cell of the argument list.

* At each iteration, the current list cell is available in the loop variable of the`foreach`.

* Each iteration produces a result value, and these values are returned as a concatenatedlist as the result of the `foreach` function.

An example of the`mapcon` function used with foreach is as follows:

`foreach(mapcon x '(1 2 3 4) list(x))`

The return value is:

`((1 2 3 4)`

`(2 3 4)`

`(3 4)`

`(4)`

`)`

You can use the`mapcon` function with more than one list argument. In this case, the supplied function argument is applied to successive sublists of the lists. This means that the supplied function is first applied to the lists themselves, and then to the `cdr` of each list, and then to the `cdr` of the `cdr` of each list, and so on.

A`mapcon` function example with a lambda function with one list argument:

```
mapcon((lambda (x)(printf "x = %L\n" x)(list (car x) (add1 (car x)))) '(1 2 3 4))
```

displays the following

`x = (1 2 3 4)`

`x = (2 3 4)`

`x = (3 4)`

`x = (4)`

The return value is:`(1 2 2 3 3 4 4 5)`

A`mapcon` function example with a lambda function with two list arguments:

`mapcon((lambda (x y) (printf "x = %L y = %L\n" x y)`

`(list (car x) (add1 (car y))))`

`'(1 2 3 4)`

`'(4 3 2 1)`

`)`

displays the following

`x = (1 2 3 4) y = (4 3 2 1)`

`x = (2 3 4) y = (3 2 1)`

`x = (3 4) y = (2 1)`

`x = (4) y = (1)`

The return value is:`(1 5 2 4 3 3 4 2)`

### The mapcan Function

Like the`mapcar` function, the `mapcan` function is useful for building a list by transforming the elements of the original list. However, instead of collecting the intermediate results into a list as `mapcar` does, `mapcan` appends them. The intermediate results must be lists. Notice that the resulting list need not be in 1-1 correspondence with the original list.

The`mapcan` function iterates over each element of the argument list. When used with the `foreach` function

* At each iteration, the current element is available in the loop variable of the`foreach`.

* Each iteration produces a result value, which must be a list. These lists are thenconcatenated by the destructive modification function `nconc`, and the new list is returned as the result of the function as a whole.

For example, flattening a list of lists can be easily done with

```
foreach( mapcan x '( ( 1 2 ) ( 3 4 5 ) ( 6 7 ) )      x       ) => ( 1 2 3 4 5 6 7 )
```

```
mapcan(      lambda( ( x ) x )      '( ( 1 2 ) ( 3 4 5 ) ( 6 7 ) )      ) => ( 1 2 3 4 5 6 7 )
```

For another example, the following builds a list of squares of the odd integers in the list`( 1``2 3 4 5 6 )`.

```
foreach( mapcan x '( 1 2 3 4 5 6 )      when( oddp( x )            list( x )            )      ) => ( 1 3 5 )      mapcan(       lambda( ( x ) when( oddp( x ) list( x )) )      '( 1 2 3 4 5 6 )      ) => ( 1 3 5 )
```

### The mapinto Function

Like the`mapcar` function, the `mapinto` function is useful for building a list by transforming the elements of the original list. However, instead of allocating a new list, `mapinto` reuses the preallocated list. The first argument of `mapinto` is a sequence that receives the results of the mapping.

* The`foreach` function iterates over each element of the argument list.

* At each iteration, the current element is available in the loop variable of the`foreach`.

* Each iteration produces a result value.

* These values are returned in a list as the result of the function.

For example:

```
foreach( mapinto x '(1 2 3 4) println(x))1 ; Prints the numbers 1 through 4234=> (1 2 3 4) ; Returns the second argument to foreach.
```

`> mapinto( '(1 2 3 4) 'plus )`

`(1 2 3 4)`

### Summarizing the List Traversal Operations

The table below summarizes how the mapping functions work. The term`Function` refers to the function you pass to the mapping function. Each table entry is a mapping function that behaves according to the row and column headings. In one case, there is no such mapping function.

**Summary of the Mapping Functions**

| **Mapping Function Return Value** | **Function is Passed Successive Elements** | **Function is Passed Successive  List Cells**
| Ignores the result of each iteration. Returnsthe original list. | mapc (default option) | map
| Collects the result of each iteration. Returnsthe list of results. | mapcar | maplist
| Collects the result of each iteration. Usesnconc to append the result of each iteration. | mapcan | No such function
List Traversal Case Studies
---------------------------

The most useful mapping functions are`mapc`, `mapcar`, and `mapcan`. A good understanding of these functions simplifies most list handling operations in SKILL.

### Handling a List of Strings

Suppose you need to calculate the length of each string in a list of strings so that the lengthsare returned in a new list. That is, the function should perform the following transformation:

`( "sam" "francis" "nick" ) => ( 3 7 4 )`

Someone not familiar with the`mapcar` option to `foreach` might code this as follows:

```
procedure( string_lengths( stringList )      let( (result)            foreach( element stringList                  result = cons( strlen(element) result)                  ) ; foreach            reverse( result )            ) ; let      ) ; procedure
```

Using the`mapcar` function allows this code to be written as

```
procedure(string_lengths(stringList)      foreach(mapcar element stringList            strlen(element)            ) ; foreach      ) ; procedure
```

In fact, the`foreach` function is implemented as a macro that expands to one of the mapping functions, so the same example can be written using the mapping function directly as follows:

```
procedure(string_lengths(stringList)      mapcar( 'strlen stringList)      ) ; procedure
```

### Making Every List Element into a Sublist

You can perform this operation with either version of the`trMakeSublists` function.

```
procedure( trMakeSublists( aList )      foreach( mapcar element aList            list( element )            ) ; foreach       ) ; procedure
```

```
procedure( trMakeSublists( aList )      mapcar(             'ncons               ;;; return argument in a list             aList      ) ) ; procedure
```

`trMakeSublists( '(1 2 3)) => ( ( 1 ) ( 2 ) ( 3 ) )`

### Using mapcan for List Flattening

The`mapcan` function is useful when a new list is derived from an old one, and each member of the old list produces a `number`of members in the new list. (Note that using `mapcar` allows `only a one-to-one mapping`). One application of `mapcan` is in list flattening. Suppose we have a list that contains lists of numbers:

`x = '( (1 2 3) (4) (5 6 7 8) () (9) )`

This list can be flattened using the following procedure:

```
procedure(flatten(numberList)      foreach( mapcan element numberList            element            ) ; foreach      ) ; procedureflatten(x) => ( 1 2 3 4 5 6 7 8 9 )
```

This function simply concatenates all sublists of the argument. Remember that`nconc` is a `destructive` modification function, so variable `x` no longer holds useful information after the call.

To preserve the value of`x`, each sublist should be `copied` within the `foreach` function to produce a new sublist that can be harmlessly modified:

```
procedure( flatten( numberList )      foreach( mapcan element numberList            copy(element)            ) ; foreach      ) ; procedure
```

```
x = '( (1 2 3) (4) (5 6 7 8) () (9) )flatten(x) => ( 1 2 3 4 5 6 7 8 9 )x => ((1 2 3) (4) (5 6 7 8) nil (9))
```

### Flattening a List with Many Levels

By using a type predicate and a recursive step, this procedure can be modified to flatten a listwith many levels:

```
procedure(flatten(numberList)      foreach(mapcan element numberList            if( listp( element )                  flatten(copy(element)) ;; then                  ncons(element)                  ) ; if            ) ; foreach      ) ; procedure
```

```
x = '((1) ((2 (3) 4 ((5)) () 6) ((7 8 ()))) 9)flatten(x)       => (1 2 3 4 5 6 7 8 9)x                => ((1) ((2 (3) 4 ((5)) nil 6) ((7 8 nil))) 9)
```

The body of the`foreach` first checks the type of the current list member.

* If the member is a list, the result is a list obtained by flattening a copy of it.

* If the member is not a list, it cannot be flattened further, and the result is a`one-``element list` containing the member.

Remember that when using`mapcan`, the result of each iteration must be a list so that the results can be concatenated using `nconc`.

### Manipulating an Association List

Mapping functions can be very powerful when used together. For example, suppose there isa database of names and extension numbers:

```
thePhoneDB = '(            ("eric" 2345 6472 8857)            ("sam" 4563 8857)            ("julie" 7765 9097 5654 6653)            ("francis")            ("pat" 5527)            )
```

The database is stored as a list with one entry for each person. An entry consists of a list ofthe person's name followed by a list of extensions at which the person can be reached. This type of list is known as an association list. Some people can be reached at several extensions, and some people at none at all. An automated dialing system has been introduced that accepts only name-number pairs: in other words, it requires data in the following format:

`(("eric" 2345) ("eric" 6472) ("eric" 8857) ("sam" 4563) . . . . . .`

How can the information be transformed from one format to another? Each`person` entry in the original database can produce several entries in the new database, so `mapcan` must be used to traverse person entries. Each `number` in the old database produces a single entry in the new database, so `mapcar` can be used to traverse the numbers.

From this information, a function can be written to translate the database:

```
procedure( translate( phoneDB )      let((name)            foreach(mapcan personEntry phoneDB                  name = car( personEntry )                  foreach( mapcar number cdr( personEntry )                        list( name number )                        ) ; foreach                  ) ; foreach             ) ; let      ) ; procedure
```

To show that this works, consider the innermost`foreach` loop first. This loop is called for each person entry in the database. Suppose that the entry `("sam" 4563 8857)` is being processed. In this case, `name` is set to `"sam"` and the `foreach` iterates over the list of numbers `(4563 8857)`.

Because this iteration is a`mapcar`, the result of the `foreach` is a new list with one entry for each number in the old list. Each entry in this new list is a name-number pair constructed by the expression `list(name number)`. Hence, the result of this `foreach`is the list

`(("sam" 4563) ("sam" 8857))`

The outermost`foreach` concatenates these lists of name-number pairs: it works exactly like the first example of `flatten` given previously. Notice that there is no need to copy the elements before concatenating them (as was the case in `flatten`) because they have just been created.

### Using the exists Function to Avoid Explicit List Traversal

SKILL provides a large number of list iteration functions. The most basic of these is the`foreach` function, which traverses all elements of a list. This traversal is useful, but often what is required is to traverse just part of a list, to check for a certain condition. In this situation, correct use of the `exists`,`forall`, and `setof` functions can greatly improve your code. Generally the alternatives are less efficient.

Consider writing a simple function that iterates over all integers in a list and checks whetherthere is any even integer. There are several approaches.

One approach is to use a`while` loop that explicitly tests a Boolean variable found.

```
procedure( contains_even( list ) let( (found)          while( list && !found                  when( evenp( car(list) )                   found = t             )             list = cdr(list)             ) /* end while */          /* Return whether found. */          found ) /* end let */) /* end contains_pass */
```

```
contains_even( '(1 2 3 4 )) => tcontains_even( '(1 7 3 9 )) => nilcontains_even( nil ) => nil
```

Another approach is to jump out of the`while` loop:

```
procedure(contains_even( list )      prog( ()            while(list                  if( evenp( car(list) )            return(t)                  )                  list = cdr(list)            ) /* end while */            return(nil) ) /* end prog */) /* end contains_pass */
```

This approach might appear to be better because there is no need for the local variable.

A third approach involves jumping out of a`foreach` loop:

```
procedure(contains_even(list)      prog( ()      foreach(element list                  if( evenp(element)                        return(t)                  )            ) /* end foreach */            return(nil) ) /* end prog */) /* end contains_pass */
```

But this approach still requires the`prog` to allow the jump out of the `foreach` loop once the element has been found.

A much simpler way of writing this procedure is as follows:

```
procedure(contains_even(list)      when( exists( element list evenp( element ))            t      ) /* when */) /* end contains_pass */
```

This approach has neither the`prog` nor any local variables, and is just as intuitive. The `exists` function terminates as soon as a matching list member has been found, so this example is just as efficient in this respect as the previous ones (which had to use `return` to achieve this result). The result of an `exists` is `nil` if no matching entry is found. Otherwise the result is the sublist of the argument that contains the matching member as its head. For example:

`exists( x '( 1 2 3 4 ) evenp( x ) ) => ( 2 3 4 )`

Because SKILL considers`nil` to be equivalent to false and non-`nil` to be equivalent to true, the result of an `exists` can be treated as a boolean if desired. Note that if the `contains_even` function was defined to return either `nil` or non-`nil` (rather than `t`), it could be further simplified to

```
procedure( contains_even( list )      exists( element list evenp( element ))) /* end contains_pass */
```

As with all the other iterative functions, there is no need to declare the loop variable for`exists` because the loop variable is local to the function and automatically declared.

### Commenting List Traversal Code

The examples above demonstrate the power of these mapping functions. Generally, wherevera `foreach` loop is used to build a list, a mapping function can usually be used instead. Because the mapping functions collect all the results and apply a single list building operation, they are faster than the equivalent iterative function and often look more succinct.

However, the mapping functions all look very similar, and it is often difficult to see exactly whata piece of code using a mapping function is trying to do. For this reason whenever a mapping function is used, you should write a comment detailing exactly what the function is expected to return.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
