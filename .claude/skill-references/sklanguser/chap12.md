### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

12
==

Optimizing SKILL
================

Before you embark on optimizing your SKILL code, your SKILL program should work. Youmight waste time if you try to optimize the performance of a program that has not yet met its functional requirements.

**Note:** In this chapter, you can find information about techniques for modifying your programsto run faster. You will not learn how to create better algorithms: You need to design algorithmic performance into your programs from the outset.

When optimizing your SKILL code, you should do the following:

* Focus your efforts

> Before optimizing, you should determine what you need to optimize. If 80% of the time isspent in 20% of the code, you should focus your efforts on optimizing that small portion of the program where there is a performance bottle-neck.

> Always measure the benefit gained after you modify your code. You should leavewell-written and well-structured code untouched if the changes do not yield significant performance improvements.

* Use[profiling tools](../skillide/skillideTOC.md) to measure code performance

* You should expect reduced execution speed when profiling and gatheringperformance data because these operations are necessarily intrusive in nature. The measurements you gather should take this into account. When profiling, you should think of code performance in terms of percentages rather than absolute values. See ["Printing Summary Statistics"](chap9.html#1017628 "Advanced Topics") for information on the how to obtain and interpret a summary of memory allocation.

> You can optimize your SKILL code for time spent and memory used.

* Time: You can use the SKILL Profiler to find out where most of the time is spent inyour program. You can gather global statistical information about time spent in functions called in a given session. The profiler takes a sample of the runtime stack at pre-specified intervals and presents timing information as call graphs identifying the critical paths. You can use this information to direct your effort.

> > You can use`measureTime` to evaluate specific expressions and get timing results. You can also add your own more deterministic instrumentation to the code to collect relevant information about your algorithms and structures.

* Memory: You can use the SKILL Profiler to track memory usage in your program.SKILL has an automatic memory manager and programs can be written to generate excessive amounts of memory. Before you optimize for time, make sure to profile memory usage to see if that is where you need to spend your effort. A good indicator that memory usage needs optimizing is if the function `gc` (garbage collection) appears high among functions profiled for time.

See the following sections for more information:

* [Optimizing Techniques](#1011309 "Optimizing SKILL")

* [General Optimizing Tips](#1012537 "Optimizing SKILL")

* [Miscellaneous Comparative Timings](#1008399 "Optimizing SKILL")

Optimizing Techniques
---------------------

You can try the following techniques to optimize your code. Not all techniques are effective inall circumstances. You should experiment and measure performance gain.

* [Macros](#1008228 "Optimizing SKILL")

* [Caching](#1008232 "Optimizing SKILL")

* [Mapping and Qualifying](#1008247 "Optimizing SKILL")

* [Write Protection](#1008256 "Optimizing SKILL")

* [Minimizing Memory](#1008264 "Optimizing SKILL")

### Macros

In many situations, you can improve the performance of your code by replacing function callswith macros. However, because macros are in-line expanded, they can grow the size of the code at runtime. So there is a balance as to what kind of functions can be written as macros.

For example, functions small in size that are likely to be used a lot are good candidates.Expressions that can be reduced at compile time leaving smaller subexpressions to be evaluated at run time are also good candidates.

### Caching

Caching is a technique used to save the results of costly computations in a fast access cachestructure. You have to balance the benefit of time saved versus amount of memory used for the cache structure.

A good data structure to use for caches is the association table. For example, if you called acompute-intensive function, say factorial or fibonacci, many times in a session, you might consider caching the results so a second call to the function with same argument will run faster. To do this, you first need to create an assoc table and store it as a property on the symbol for the function, for example:

The fibonacci function described in["Fibonacci Function"](chap17.html#1008381 "Programming Examples").

```
myFib.cache = makeTable("fibonacciTable" nil)procedure( myFib(num)(let ((res myFib.cache[num]))      cond( !res myFib.cache[num]= fibonacci(num))            ( t res)))
```

You could write the function`myFib` as a macro:

```
defmacro( myFib (num)      `or(myFib.cache[,num]             myFib.cache[,num] = fibonacci(,num)))
```

For example, compare the following timing numbers (in seconds).

`fibonacci(25)myFib(25)`

`1st call 23 232nd call 23 0.009`

### Mapping and Qualifying

Mapping functions (`map, mapcar,` `maplist`, and so forth) have been described in detail in ["Advanced List Operations"](chap8.html#1008199 "Advanced List Operations") When manipulating lists, you can achieve significant performance gains if you use map\* functions instead of loops that directly manipulate the lists. The same argument applies to qualifiers like `foreach`, `setof`and`exists`. The qualifiers are generic in nature in that they apply to lists as well as to association tables.

Consider the following two examples performing the same operation of adding consecutivenumbers in two equal length lists and returning a list of the results. The example using `mapcar` is at least twice as fast.

`L1 = '(1 2 3 4 5 … 100)L2 = '(100 99 98 .. 1)`

```
mapcar(lambda((x y) x+y) L1 L2)(let (res)       while(      car(L1)                   res=cons(car(L1)+car(L2) res)                  L1 = cdr(L1)                  L2 = cdr(L2)      ) res)
```

### Write Protection

Ensuring that all of your functions and data structures that are static in nature are writeprotected reduces the amount of work the garbage collector has to perform whenever it is triggered. Generally, all functions can be write protected because they are not likely to be over-written at run time. Some data structures, like lookup tables, whose contents are not likely to be modified at run time, can also be write protected.

It is highly recommended that SKILL code destined for production be packaged in contextsand that all contexts are built with the status flag `writeProtect` set to `t` (see ["Protecting Functions and Variables"](chap10.html#1008452 "Delivering Products")). To set write protection on global variables use `setVarWriteProtect`.

When SKILL memory is write protected, the garbage collector does not touch it, thusconsiderably reducing the amount paging and work done at run time.

### Minimizing Memory

The way memory is used in SKILL is by`cons`ing (the basic list building operation), creating strings, arrays, and so forth, or by generating instances of defstructs and user types. The goal of memory optimizing is to reduce the overall amount of memory used. This reduction

* Saves on run-time page swapping that an operation has to perform when physicalmemory resources are scarce

* Reduces the work load on the garbage collector

#### Run the SKILL Profiler in Memory Mode

To start optimizing memory usage, use the SKILL profiler in memory mode to discover thefunctions responsible for the largest amount of memory used. From there start tweaking the functions. You should be aware of the nature of the utilities and library calls you use.

For example, removing elements from lists using`remove` makes a copy of the original list minus the element removed. You should check to see if that is the desired behavior. If you can use a destructive remove instead, such as `remd`, you can cut down memory use considerably on this particular operation. Experiment.

#### Ways to Minimize

When generating large data structures in memory from information on disk, you should askyourself whether you need to generate the whole image in memory if all of it is not likely to be used. Use the technique known as lazy evaluation to expand your structures on demand rather than at start-up.

For example, you can embed`lambda` constructs in your data structures to retrieve information on demand (see ["Declaring a Function Object (lambda)"](chap9.html#1008388 "Advanced Topics") for a description of `lambda` constructs). Experiment.

If you know from the outset the amount of memory your application is likely to need at runtime, you can preallocate that memory to reduce the number of times the garbage collector is triggered. There is a delicate balance you have to make here between total memory allocated and garbage collection.

Remember, preallocating memory is**not** a substitute for fine tuning memory use in your program.

Only preallocate memory when you have tuned the program and determined the minimumamount of memory needed to run efficiently. Read ["Memory Management (Garbage Collection)"](chap9.html#1008565 "Advanced Topics") to better understand the nature of automatic memory management.

### Tail-Call Optimization

When a function is called, its return address is pushed to the call stack. Each recursive callto the function results in a new stack frame being pushed to the call stack. Since the call stack has limited memory, recursive calls to a function can result in stack overflow. SKILL uses tail-call optimization to keep runtime stack-overflow errors in check.

If the last thing a function does before it returns is call another function, rather than allocatinga new stack frame for the called function, tail-call optimization allows you to reuse the stack frame of the calling function. By using tail-call optimization, you can eliminate all intermediate return calls and implement recursion as a simple iteration.

To implement tail-call optimization in SKILL, set the`optimizeTailCall` variable to `t`, that is

`sstatus(optimizeTailCall t)`

**Note:** Tail-call optimization is applicable to SKILL code with lexical scoping (scheme/`.ils` files). The `.il` files (dynamic scoping) use the runtime stack to store the function call's arguments, and therefore, the tail-call optimization is not applicable for `.il` files. In addition, tail call optimization does not work in the debug mode. Ensure that `debugMode` switch is set to `nil` before compiling the function and setting `optimizeTailCall` switch.

You can run the following examples and verify how tail-recursion is eliminated when you usetail-call optimization:

#### Example 1:

`toplevel('ils) ;; in SCHEME mode`

`sstatus(debugMode nil) ;; turn off debugMode`

`tracef t ;; set trace = on`

`defun(test ()`

`let( ()`

`--x`

`if(x > 0 then`

`test()`

`)`

`)`

`) ;; recursive call to test()`

`ILS-<2>x = 4`

Calling`test()` without setting `optimizeTailCall`:

`test()`

`(3 > 0)`

`greaterp --> t`

`test()`

`(2 > 0)`

`greaterp --> t`

`test()`

`(1 > 0)`

`greaterp --> t`

`test()`

Calling`test()` after setting `optimizeTailCall`:

`ILS-<2> sstatus(optimizeTailCall t)`

`ILS-<2> x = 4 ;; set x`

`ILS-<2> test()`

`test()`

`(3 > 0)`

`greaterp --> t`

`test()`

`(2 > 0)`

`greaterp --> t`

`test()`

`(1 > 0)`

`greaterp --> t`

`test()`

`(0 > 0)`

`greaterp --> nil`

When you call`test()` by setting `optimizeTailCall`, the stack-overflow errors are eliminated as the existing stack frame is reused.

#### Example 2:

`toplevel('ils) ;; in SCHEME mode`

`ILS-<2> defun(a (x)`

`if(x > 0`

`b(x)`

`)`

`)`

`a`

`ILS-<2> defun(b (x)`

`a(--x)`

`)`

`b`

`;this implements a simple delay:`

`ILS-<2> a(1000000)`

`*Error* b: Runtime Stack Overflow!`

`ILS-<2> sstatus optimizeTailCall t`

`a(1000000)`

`=>nil ; no stack overflow`

Benefits of using tail-call optimization:

* Functions execute faster since recursive push and pop operations are reduced.

* Stack-overflow errors are eliminated.

Limitations of using tail-call optimization:

* Debugging and tracing of optimized code is difficult as the intermediate return calls areeliminated.

General Optimizing Tips
-----------------------

See the following sections for general optimizing tips:

* [Element Comparison](#1008287 "Optimizing SKILL")

* [List Accessing](#1008327 "Optimizing SKILL")

* [List Building](#1008330 "Optimizing SKILL")

* [List Searching](#1008381 "Optimizing SKILL")

* [List Sorting](#1008386 "Optimizing SKILL")

* [Element Removal and Replacing](#1008389 "Optimizing SKILL")

* [Alternatives to Lists](#1008394 "Optimizing SKILL")

### Element Comparison

In SKILL, there are two basic functions used to compare values. These functions are`eq` and `equal` (also known as the infix operator, `==`).

It is important to understand the difference between these two functions, because both areuseful in particular circumstances. There are several functions in SKILL which have alternative implementations depending on whether the user wants to compare using the `eq` or `equal` function. For example, the two functions `memq` and `member` are used to search a list for an object. `memq` uses the `eq` function for comparison and `member` uses the `equal` function.

The`eq` function is far stricter in its comparison than the `equal` function. There are objects which `equal` would consider to be the same, but which `eq` considers to be different.

You can compare the following objects using`eq`:

* SKILL symbols

* Small integers (`-2**29 <= i <= 2**28`)

* List objects (NOT their contents)

* Any pointers

* Characters (NOT strings)

* Ports

The important things that cannot be reliably compared by`eq` are strings and lists, unless they are identical objects referenced by the same pointer. In many situations SKILL tries to optimize memory use by caching certain objects and reusing them. For example, there is a string caching mechanism that saves SKILL from generating the same string multiple times. Code and data segments in static (write-protected) memory are also cached so they are reused within the static space.

The following are some examples of the more unexpected differences between thecomparison operations:

`x = '(1 2 3)y = '(1 2 3)eq(x y)              => nilequal(x y)           => t`

```
s1 = "string"s2 = "string"s3 = s2eq(s1 s2)            => t    ; unreliableequal(s1 s2)         => t    ; reliableeq(s3 s2)            => t    ; reliableequal(s3 s2)         => t    ; reliable
```

```
eq(12345 12345)      => nill = '(12345)eq(car(l) car(l))    => tl = '("string")eq(car(l) car(l))    => t
```

To understand more about`equal` and `eq`, keep in mind how they are implemented. The following are pseudo-code definitions of the two functions (they are actually implemented in C):

`eq(A B) if A is the same object as B then t else nilend eq`

```
equal(A B) if eq(A B) then t else       if the contents of A and B are `equal'       then t       else nilend equal
```

Suppose the two functions are used to compare two SKILL objects, A and B. If A and B arein fact the same object then `eq` will immediately return `t`. Because the first thing that `equal` does is call `eq`, it too will immediately return`t` in this case. Now suppose that A and B represent distinct objects. In this case, `eq` will immediately return `nil`. `equal`, however, goes on to try to establish if the `contents` of the two objects are the same, (for example, if the objects are lists, `equal` compares each element of the two lists for equality) and this process involves a large overhead. To summarize this behavior:

`eq('a 'a)            => t        (fast)`

```
equal('a 'a)         => t        (fast)eq('a 'b)            => nil      (fast)equal('a 'b)         => nil      (SLOW)
```

If in doubt about which of`eq` and `equal` to use, observe the following rules:

* If the objects are simple (symbols, small integers, pointers, characters), use`eq` because `eq` is faster than `equal`.

* If the objects are compound or complex (lists or strings, for example), consider whatfunctionality is needed. To test whether two strings contain the same characters, use `equal`; To test whether two strings are in fact the same `object`, use `eq`.

Some common tests can be more efficiently implemented by using the built-in SKILLfunctions, or simply by using the fact that in SKILL, any non-`nil` object is true, not just `t`. Examples of some simple transformations are:

|  |
| --- | ---
| ****Original Test**** | **Improved Test**
| a == 0 | zerop(a)
| a == 1 | onep(a)
| strcmp(a,"teststring") == 0 | a == "teststring"
| a != nil | a
| a == nil | !a
| !null(a) | a
For`a != nil`, providing a Boolean value is all that is required, for example,

`if( a != nil ) can be coded as if( a )`

For `!null(a),` providing a Boolean value is all that is required, for example,

`if( !null(a)) can be coded as if( a )`

### List Accessing

The basic list accessing operations of SKILL (`car`, `cdr` and so forth) are very fast, and their performance is very predictable. The `nth` and `nthcdr` functions are significantly faster than the equivalent number of basic operations (because they avoid procedure call overhead) and should be used if lists are long. The operation that should be used with the most care is the `last` operation. This function must traverse the entire list to find the last element, so a large overhead is incurred for long lists.

### List Building

There are two main methods of building lists: iteratively, either as part of a program'soperation or when all the elements are the same type and non-iteratively when the format and number of elements are known. List building is an area that is open to abuse, and it is important that the processes involved are clearly understood.

#### Iterative List Creation

The standard function for adding an element to the start of a list is the`cons` function, which is very efficient and has predictable performance. New users often find `cons` difficult to use because elements are added to the `front`of the list, giving a result that is "back to front". There are several methods of producing a list in the "right" order, which vary in efficiency:

Use`append1` to add each element to the end of the list rather than to the start.

This is the most inefficient method, and lists should never be iteratively created in this way.As each element is added, the `append1` function makes a copy of the original list, with the new element on the end. If a list of n elements is built using this method, then on the order of n2 list cells are created, and most of them are promptly discarded again.

Use`nconc` to add each element to the end of the list rather than to the start.

This method is also quite inefficient, and lists should never be iteratively created in this way.Because `nconc` is a "destructive" append, only `n` list cells need to be created to form the list. However, on the order of n2 list cells must be traversed to build the list.

Use`cons` to build the list backwards, and then use `reverse` to turn the list around.

This is a much more efficient, and easily understood method. To create a list of`n`elements,`2n` list cells are created, but half of them are immediately discarded.

Use the`tconc` structure and function to build the list in the right order.

This is the most efficient method in terms of storage requirements. To create a list of`n` elements, only`n+1` list cells are created. Because creation of list cells is relatively time consuming, this means that using `tconc` to build a long list is faster than using `cons` and `reverse`. A slight disadvantage is that the code is less intuitive.

In general, if the code is not time critical, it might be better to build the list backwards using`cons` and then apply `reverse`. If the code is in a time critical part of the program, then the `tconc` method should be used, along with some detailed commenting. From a memory usage point of view, if the list being built is long, then it is better to use the `tconc` method to prevent the garbage collector being called unnecessarily.

To build lists that are derived from existing lists, it is far better to use the mapping functions,possibly coupled with the `foreach` function. This is discussed in detail later.

#### Non-Iterative List Creation

To build lists of known format, use one of the`list`, `quote`, or `backquote` functions as follows:

* Use`list` when all elements of the result must be evaluated (in other words, none of the list members are known constants).

* Use`backquote` when the list contains a mixture of known constants and evaluated entries.

* Use`quote` when the list consists entirely of known constants.

For example, suppose we have the three variables, a, b, and c such that:

`a = 1 b = "a string" c = '(A B C D E)`

If we wanted to make a disembodied property list (dpl) of symbol-value pairs using thesevariables then we could use `list` or a mixture of `quote` and `backquote`, as follows:

```
/* These are identical in function. */dpList1 = list('a a 'b b 'c c) dpList2 = `(a ,a b ,b c ,c)
```

In the second case, some items are preceded with commas (with no space after the comma)and some are not. Those `not` preceded with commas are treated as literals, as if this was a normal quoted list. Those preceded by commas are evaluated, as if the list was declared using `list`.

If this was the only use of`backquote`, it would not be very useful. However, there are two useful extra features. The first is that you can splice in entire `lists` by using the `,@` (comma-at) specifier, as follows:

`` `(a ,a b ,b c ,@c) => (a 1 b "a string" c A B C D E) ``

Here, the five elements`A`, `B`, `C`, `D`, and `E` have been used in place of the placeholder `,@c`. This cannot be done easily using `list`. The second useful feature is that the expansion can descend hierarchically. Suppose that instead of a dpl we wanted to create an assoc list. To do this using just `list`, would require the following:

```
list( list('a a) list('b b) list('c c) )=> ((a 1) (b "a string") (c (A B C D E)))
```

Using`backquote` simplifies this to:

`` `((a ,a) (b ,b) (c ,c)) => ((a 1) (b "a string") (c (A B C D E))) ``

The last element can still be flattened using ,@ if required:

`` `((a ,a) (b ,b) (c ,@c)) => ((a 1) (b "a string") (c A B C D E)) ``

**Note:** Care should be taken with lists defined using`quote`. These lists form part of the program code, and if edited using the destructive list operations the actual program code will be changed. This is particularly important when building `tconc` lists. It is very tempting to initialize a `tconc` structure to `'(nil nil)`, but this is wrong. If this is done, then as each element is added the program itself is being modified.

Consider the following naive list copy:

```
procedure(copylist(inputList)      let( ((tc '(nil nil)))            foreach(element inputList                  tconc(tc element)            )            car(tc)      ) /* let */) /* copylist */
```

This works the first time it is called, but the list assigned to`tc` in the variable declaration part is being modified as part of the program, so the next time the function is called, the copied list will actually be appended to the list that was copied in the first call:

`copylist('(1 2 3)) => (1 2 3)copylist('(a b c)) => (1 2 3 a b c)`

The list should be initialized by using either`list(nil nil)` or `tconc(nil nil)`. The second method makes it more obvious that the variable is being initialized as a `tconc` structure, but in this case the return value would be `cdar(tc)` rather than `car(tc)`.

### List Searching

There are two methods for searching a list, depending on its structure. For a simple list, thefunctions `memq` and `member` can be used to search the list. The `memq` function is faster because it uses the `eq` function for comparison and is therefore preferred whenever the list contains elements for which the `eq` function is suitable.

If the list is an assoc list, that is, it is a list of key-value pairs, then the functions`assoc` and `assq` should be used to do the searching. Again, `assq` is faster because it uses the `eq` function for the comparison. It is therefore worthwhile, when building assoc lists, trying to ensure that the key elements are suitable for use with the `eq` function. In particular, when building an assoc list that would normally have keys that are strings, it may be worthwhile using the `concat` function to turn these strings into symbols, and then using those symbols as the keys in the list. This will then allow the `assq` rather than the `assoc` function to be used.

There are, however, two disadvantages with this method. The first disadvantage is thatsymbols in SKILL use memory and are not garbage collected (they are persistent), so creating many symbols uses up memory. Garbage collection is also slowed because the speed of this is directly related to the number of symbols. The second disadvantage is that the `concat` function is itself quite slow, so the overhead of this might outweigh any gains from using `assq` instead of `assoc`.

### List Sorting

The`sort` and `sortcar` functions for lists are based on a recursive merge sort and are thus reasonably efficient. The list is sorted in-place, with no new list elements created, thus the list returned replaces the one passed as argument, and the one passed as argument should no longer be used.

### Element Removal and Replacing

Two non-destructive functions are provided for removal of elements from a list,`remq` and `remove`. The equivalent but destructive functions are `remd` and `remdq` These functions remove all elements from the list which match a given value, using the `eq` and `equal` function respectively. The `remq` function is faster than the `remove` function.

The function`subst` is provided for replacement of all elements of a list matching a particular value with another value. This function uses`equal` and so should be used sparingly.

It should be noted that the non-destructive functions return a`copy` of the original list with the matching elements removed. This means that these functions should not be used within a loop in order to remove a large number of elements. If a number of different elements must be removed from a list, then it is more efficient to generate a new list by traversing the old one just once, selecting only the required elements for the new list.

### Alternatives to Lists

In many cases, there are faster and more compact alternatives to list structures. For example,if you need a property list that is likely to remain small in contents and most of the properties are known, consider using a `defstruct`.

If you need an assoc or property list whose contents are likely to be large (in the order of tensat least), then consider using assoc tables. Assoc tables offer much faster access time and for a large set of key-value pairs memory usage is more efficient. Assoc tables are not ordered (they are implemented as hash tables).

Miscellaneous Comparative Timings
---------------------------------

This section gives comparative timings for various pieces of SKILL code to furtherdemonstrate and reinforce the comments made in the previous sections. The examples are listed in an order that matches the structure of the preceding sections.

The timings were ascertained using the SKILL`profile` command and are expressed in ratios of the first example. In producing the timings, every effort has been made to compare like with like.

### Element Comparison

The difference in speed between the`eq` and `equal` functions can be demonstrated using the following functions:

```
procedure(equal_test()      equal('fred 'joe)      equal('fred 'fred)) /* end equal_test */
```

```
procedure(eq_test()       eq('fred 'joe)       eq('fred 'fred)) /* end eq_test */
```

Note that each procedure has two comparisons, one failing and one succeeding. Thecomparative times for these were:

`equal_test 1.00eq_test 0.92`

Further tests demonstrated that it is when the symbols are`not` equal that the `eq` function gains over the `equal` function. This means that if the test is expected to succeed on most occasions, there is little difference between the two functions.

### List Building

As noted, there are several methods for building a list. The following examples attempt to builda list of the first 50 integers. The last example builds the list in descending order; the others build the list in ascending order.

```
procedure(list1() let( (returnList)            for(i 1 50                  returnList = append1(returnList i)            )            /* return */            returnList ) /* end let */) /* end list1 */
```

```
procedure(list2() let( ((returnList list(nil nil))            )            for(i 1 50                  tconc(returnList i)            )            car(returnList) ) /* end let */) /* end list2 */
```

```
procedure(list3() let( (returnList)            for(i 1 50                  returnList = cons(i returnList)            )            reverse(returnList)       ) /* end let */) /* end list3 */
```

```
procedure(list4() let( (returnList)            for(i 1 50                  returnList = cons(i returnList)            )            returnList ) /* end let */) /* end list4 */
```

The outcome of this test depends on the length of the list being built. These examples use amedium length list, and the results of running these examples are:

`list1 1.00list2 0.14list3 0.11list4 0.10`

These results demonstrate that with this size of list there is little difference between using the`tconc` method and the `cons`and`reverse` method. In fact, there will be little difference between these methods for any length of list because they both have to carry out the same basic functions. The only difference is that the `reverse` method must find twice as many list elements as the `tconc` method. This gives a greater chance of the garbage collector being called, which might cause the program to slow down, especially for large lists.

### Mapping Functions

To demonstrate the relative speeds of the mapping functions, consider the followingimplementations of a function that picks every even integer out of a list of integers, returning the list of even integers in the same order as the originals.

```
procedure(map1(intList)      let( (res)            while(intList                  when(evenp(car(intList))                              res = cons(car(intList) res)                  )                  intList = cdr(intList)            ) /* end while */            reverse(res)      ) /* end let */) /* end map1 */
```

```
procedure(map2(intList)      let( (res)            foreach(i intList                  when(evenp(i)                        res = cons(i res)                  )            ) /* end foreach */            reverse(res)      ) /* end let */) /* end map2 */
```

```
procedure(map3(intList)      foreach(mapcan i intList            when(evenp(i)                  ncons(i)            )      ) /* end foreach */) /* end map3 */
```

```
procedure(map4(intList)      mapcan((lambda (i) when(evenp(i) ncons(i)))            intList      )) /* end map4 */
```

The relative timings for these are:

`map1    1.00map2    0.68map3    0.64map4    0.29`

This shows that the version using a`lambda` function along with the basic mapping function is the fastest. However, this is the least readable of these functions and should only be used with a great deal of caution, and a large number of comments.

### Data Structures

It is difficult to give meaningful comparisons between the data structure functions becausethey are all suitable for different tasks. The following two examples attempt to compare the time taken to access and change one element of a data structure stored as an array, simple list, assoc list, defstruct and property list.

`elem_number = 9elem_symbol = 'j`

`procedure(access1(array)      array[elem_number]) /* end access1 */`

`procedure(access2(list) nth(elem_number list)) /* end access2 */`

```
procedure(access3(assoc_list) cadr(assq(elem_symbol assoc_list))) /* end access3 */
```

`procedure(access4(dstruct) get(dstruct elem_symbol)) /* end access4 */`

`procedure(access5(plist) get(plist elem_symbol)) /* end access5 */`

`procedure(access6(assocTable) assocTable[elem_symbol]) /* end access */`

The comparative timings for these are:

```
access1    1.00access2    1.3access3    1.47access4    1.08access5    1.55access6    1.11
```

`procedure(set1(array val) array[elem_number] = val) /* end set1 */`

`procedure(set2(list val) rplaca(nthcdr(elem_number list) val)) /* end set2 */`

```
procedure(set3(assoc_list val) rplaca(cdr(assq(elem_symbol assoc_list)) val)) /* end set3 */
```

`procedure(set4(dstruct val) putprop(dstruct val elem_symbol)) /* end set4 */`

`procedure(set5(plist val) putprop(plist val elem_symbol)) /* end set5 */`

`procedure(set6(assocTable val) assocTable[elem_symbol] = val) /* end set6 */`

The comparative timings for these are:

`set1    1.00set2    1.14set3    1.09set4    0.93set5    1.71set6    1.2`

No comment will be made about the readability of these functions because accessprocedures should be made available for all data structure access anyway. It is clear from these results that there is little to be gained, in terms of speed from the choice of data structure, although arrays do seem to be fastest overall. When choosing data structures it is more important to consider the other factors mentioned in the data structures section of this document.

Because the structures used contained a small number of elements, the experiment isnaturally biased. You can repeat this experiment using `measureTime` to find out how effective your data structure accesses are for a given volume of data. For example, for sets of hundreds of elements, association tables will be significantly faster to access than property lists and assoc lists. For large sets it would be impractical to use arrays or defstructs.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
