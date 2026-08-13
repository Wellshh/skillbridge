### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

1
=

List Functions
==============

### append

```
append( l_list1 l_list2 ) => l_result append( o_table g_assoc ) => o_table     append( o_table1 o_table2 ) => o_newTable
```

#### Description

Creates a list containing the elements of `l_``list1` followed by the elements of `l_list2` or returns the original association table including new entries.

The top-level list cells of`l_list1` are duplicated and the `cdr` of the last duplicated list cell is set to point to `l_list2`; therefore, this is a time-consuming operation if `l_list1` is a long list.

**Note:** This is a slow operationand the functions `tconc`, `lconc`, and `nconc` can be used instead for adding an element or a list to the end of a list. The command `cons` is even better if the new list elements can be added to the beginning of the list.

The`append` function can also be used with association tables as shown in the second syntax statement. Key/value pairs are added to the original association table (not to a copy of the table). This function should be used mainly in converting existing association lists or disembodied property lists to an association table. See "[Association Table](../sklanguser/chap4.html#Association Tables)" in the *Cadence* *SKILL Language User Guide* for more details.

#### Arguments

|  |
| --- | ---
| `l_list1` | List of elements to be added to a list.
|  |
| --- | ---
| `l_list2` | List of elements to be added.
|  |
| --- | ---
| `o_table` | Association table to be updated.
|  |
| --- | ---
| `g_assoc` | Key/value pairs to be added to the association table.
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns a list containing elements of`l_list1` followed by elements of `l_list2`.
|  |
| --- | ---
| `o_table` | Returns the original association table including the new entries.
#### Example

`/* List Example */append( '(1 2) '(3 4) ) => (1 2 3 4)`

```
/* Association Table Example */myTable = makeTable("myAssocTable")=> table:myAssocTablemyTable['a] = 1=> 1append(myTable '((b 2) (c 3)))=> table:myAssocTable
```

```
/* Check the contents of the assoc table */tableToList(myTable)=> ((a 1) (b 2) (c 3))
```

#### Reference

`tconc, lconc, nconc, append1, cons`

### append1

`append1( l_list g_arg ) => l_result`

#### Description

Adds new arguments to the end of a list.

Returns a list just like`l_list` with `g_arg` added as the last element of the list.

**Note:** This is a slow operation and the functions`tconc`, `lconc`, and `nconc` can be used instead for adding an element or a list to the end of a list. The command `cons` is even better if the new list elements can be added to the beginning of the list.

#### Arguments

|  |
| --- | ---
| `l_list` | List to which`g_arg` is added.
|  |
| --- | ---
| `g_arg` | Argument to be added to the end of`l_list`.
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns a copy of`l_list` with `g_arg` attached to the end.
#### Example

`append1('(1 2 3) 4) => (1 2 3 4)`

Like`append`, `append1` duplicates the top-level list cells of `l_list`.

#### Reference

`append`

### caar, caaar, caadr, cadr, caddr, cdar, cddr, ...

`ca|d[ a|d ][ a|d ][ a|d ]r( l_list ) => g_result`

#### Description

Performs operations on a list using repeated applications of`car` and `cdr`. For example, `caaar` is equivalent to `car( car( car(``l_list``)))`. The possible combinations are caaaar, caaadr, caadar, caaddr, caar, caddar, cadddr, cadr, cdaaar, cdaadr, cdaar, cdadar, cdaddr, cdadr, cdar, cddaar, cddadr, cddar, cdddar, cddddr, cdddr, cddr, caaar, caadr, cadar, caddr, cdadr, cadaar, cadadr, caddar, cadddr, cdaaar, cdaadr, cdadar, cdaddr, cddaar, cddadr, cdddar, and cddddr.

The`cadr(``l_list``)` expression, for example, applies `cdr` to get the tail of the list and then applies `car` to get the first element of the tail, in effect extracting the second element from the list. SKILL implements all `c...r`functions with any combination of `a` and `d` up to four characters.

#### Arguments

|  |
| --- | ---
| `l_list` | List of elements.
#### Value Returned

|  |
| --- | ---
| `g_result` | Returns the value of the specified operation.
#### Example

`caaar('(((1 2 3)(4 5 6))(7 8 9))) => 1`

`caaar` is equivalent to `car( car( car(``l_list``)))`.

`caadr('(((1 2 3)(4 5 6))(7 8 9))) => 7`

Equivalent to`car( car( cdr(``l_list``)))`.

`caar('(((1 2 3)(4 5 6))(7 8 9))) => (1 2 3)`

Equivalent to`car( car(``l_list``))`.

`z = '(1 2 3)     => (1 2 3)cadr(z)          => 2`

Equivalent to`car( cdr(``l_list``))`.

#### Reference

[car](#car "List Functions"), [cdr](#1038898 "List Functions")

### car

`car( l_list ) => g_result`

#### Description

Returns the first element of a list. `car` is nondestructive, meaning that it returns the first element of a list but does not actually modify the list that was its argument.

The functions`car` and `cdr` are typically used to take a list of objects apart, whereas the `cons` function is usually used to build up a list of objects. `car` was a machine language instruction on the first machine to run Lisp. `car` stands for *contents of the address register*.

#### Arguments

|  |
| --- | ---
| `l_list` | A list of elements.
#### Value Returned

|  |
| --- | ---
| `g_result` | Returns the first element in a list. Note that`car(nil)` returns `nil`.
#### Example

`car( '(a b c) )      => a`

```
z = '(1 2 3)         => (1 2 3)y = car(z)           => 1y                    => 1z                    => (1 2 3)car(nil)             => nil
```

#### Reference

[cdr](#1038898 "List Functions"), [cons](#1038941 "List Functions")

### cdr

`cdr( l_list ) => l_result`

#### Description

Returns the tail of the list, that is, the list without its first element.

The expression`cdr(nil)` returns `nil`. `cdr` was a machine language instruction on the first machine to run Lisp. `cdr` stands for *contents of the decrement register*.

#### Arguments

|  |
| --- | ---
| `l_list` | List of elements.
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns the end of a list, or the list minus the first element.
#### Example

`cdr( '(a b c) )  => (b c)`

`z = '(1 2 3)cdr(z)          => (2 3)`

**Note:** `cdr` always returns a list, so `cdr('(2 3))`returns the `list (3)` rather than the `integer 3`.

#### Reference

`caar, caaar, caadr, cadr, caddr, cdar, cddr, ...`

### cons

`cons( g_element l_list ) => l_result`

#### Description

Adds an element to the beginning of a list.

Thus the`car` of `l_result` is `g_element` and the `cdr` of `l_result` is `l_list`. `l_list` can be `nil`, in which case a new list containing the single element is created.

#### Arguments

|  |
| --- | ---
| `g_element` | Element to be added to the beginning of`l_list`.
|  |
| --- | ---
| `l_list` | List that can be`nil`.
#### Value Returned

|  |
| --- | ---
| `l_result` | List whose first element is`g_element` and whose `cdr` is `l_list`.
#### Example

`cons(1 nil)                  => (1)cons( 'a '(b c))             => (a b c)`

The following example shows how to efficiently build a list from 1 to 100. You can reverse thelist if necessary.

```
x = nilfor( i 1 100 x = cons( i x )) => tx                             => (100 99 98 .. 2 1)x = reverse( x )              => (1 2 3 .. 100)
```

#### Reference

[car](#car "List Functions"), [cdr](#1038898 "List Functions"), [append](#append "List Functions"), [append1](#1038713 "List Functions")

### constar

`constar( [ g_arg1 ... ] l_list ) => l_result`

#### Description

Adds elements to the beginning of a list.

This function is equivalent to`cons`\\*(), and should be used instead.

The last argument,`l_list`, must be a list. `l_list` can be `nil`, in which case a new list containing the elements is created.The car of `l_result` is the first argument passed to `constar`() and the `cdr` of `l_result` is rest of the elements of the newly created list (including `l_list`).

#### Arguments

|  |
| --- | ---
| [ `g_arg1` ... ] | Elements to be added to the beginning of`l_list`.
|  |
| --- | ---
| `l_list` | The last argument that must be a list (which can be`nil`).
#### Value Returned

|  |
| --- | ---
| `l_result` | List whose first element is the first argument and whose cdr isrest of the elements of the newly created list (including `l_list`).
#### Example

The first element of the newly created list is the first argument while cdr is rest of the elements(including `l_list`):

`newList = constar( '(a b) '("hello") 1 2.3 '(x y) )`

`=> ((a b) ("hello") 1 2.3 x y z)`

`car( newList ) => (a b)`

`cdr( newList ) => (("hello") 1 2.3 x y z)`

The last argument can be nil:

`constar( 1 2 3 nil ) => (1 2 3)`

The last argument must be a list:

`constar( 'x 1 2 )`

`*Error* constar: the last arg must be a list - 2`

`constar`() is cleaner and more efficient in adding multiple elements to the beginning of a list than cons():

`cons(1 cons(2 cons(3 '(a b c)))) => (1 2 3 a b c)`

`constar( 1 2 3 '(a b c)) => (1 2 3 a b c)`

### copy

`copy( l_arg ) => l_result`

#### Description

Returns a copy of a list, that is, a list with all the top-level cells duplicated.

Because list structures in SKILL are typically shared, it is usually only necessary to passaround pointers to lists. If, however, any function that modifies a list destructively is used, `copy` is often used to create new copies of a list so that the original is not inadvertently modified by those functions. This call is costly so its use should be limited. This function only duplicates the top-level list cells, all lower level objects are still shared.

#### Arguments

|  |
| --- | ---
| `l_arg` | List of elements.
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns a copy of`l_arg`.
#### Example

```
z = '(1 (2 3) 4) => (1 (2 3) 4)x = copy(z)      => (1 (2 3) 4)equal(z x)       => t
```

`z` and `x` have the same value.

`eq(z x)         => nil`

`z` and `x` are not the same list.

### dtpr

`dtpr( g_value ) => t | nil`

#### Description

Checks if an object is a non-empty list.

`dtpr` is a predicate function that is equivalent to `pairp`.

#### Arguments

|  |
| --- | ---
| `g_value` | An object.
#### Value Returned

|  |
| --- | ---
| `t` | Object is a non-empty list.
|  |
| --- | ---
| `nil` | Otherwise. Note that`dtpr(nil)` returns `nil`.
#### Example

`dtpr( 1 ) => nildtpr( list(1)) => t`

#### Reference

`listp, pairp`

### last

`last( l_arg ) => l_result`

#### Description

Returns the last list cell in a list.

#### Arguments

|  |
| --- | ---
| `l_arg` | List of elements.
#### Value Returned

|  |
| --- | ---
| `l_result` | Last list cell (not the last element) in`l_arg`.
#### Example

```
last( '(a b c) )         => (c)z = '(1 2 3)last(z)                  => (3)last( '(a b c (d e f)))  => ((d e f))
```

#### Reference

[car](#car "List Functions"), [cdr](#1038898 "List Functions"), [list](#1039311 "List Functions"), [listp](#1039344 "List Functions")

### lconc

`lconc( l_tconc l_list ) => l_result`

#### Description

Uses a`tconc` structure to efficiently splice a list to the end of another list.

See the example below.

#### Arguments

|  |
| --- | ---
| `l_tconc` | A`tconc` structure that must initially be created using the `tconc` function.
|  |
| --- | ---
| `l_list` | List to be spliced onto the end of the`tconc` structure.
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns`l_tconc`, which must be a `tconc` structure, with the list `l_list` spliced in at the end.
#### Example

```
x = tconc(nil 1)      ; x is initialized ((1) 1)lconc(x '(2 3 4))     ; x is now ((1 2 3 4) 4)lconc(x nil)          ; Nothing is added to x.lconc(x '(5))         ; x is now ((1 2 3 4 5) 5)x = car( x )          ; x is now (1 2 3 4 5)
```

#### Reference

[append](#append "List Functions"), [tconc](#1040425 "List Functions")

### length

`length( lao_arg ) => x_result | 0`

#### Description

Determines the length of a list, array, or association table.

#### Arguments

|  |
| --- | ---
| `lao_arg` | SKILL list, array, or association table.
#### Value Returned

|  |
| --- | ---
| `x_result` | Length of the`lao_arg` object. (The length is either the number of elements in the list or array or the number of key/value pairs in the association table).
1. `lao_arg` is `nil` or an empty array or table.

#### Example

```
length( '(a b c d) )             => 4z = '(1 2 3)                     => (1 2 3)length( z )                      => 3
```

```
declare(a[11])length( a )                      => 11myTable = makeTable( "atable" 0) => table:atablemyTable[ 'one] = "blue"          => "blue"myTable[ "two"] = '(red)         => (r e d)length(myTable)                  => 2
```

#### Reference

`list`

### lindex

`lindex( l_list g_element ) => x_result / nil`

#### Description

Returns the index number of the given element in`l_list`.

#### Arguments

|  |
| --- | ---
| `l_list` | A list of elements.
|  |
| --- | ---
| `g_element` | The element to be searched in`l_list`.
#### Value Returned

|  |
| --- | ---
| `x_result` | The index number of`g_element` in `l_list`.
|  |
| --- | ---
| `nil` | Returns`nil`, if the given element is not found in `l_list`.
#### Example

`lindex('(1 2 3 4) 2)`

`=> 2`

### list

`list( [ g_arg1 g_arg2 ... ] ) => l_result | nil`

#### Description

Creates a list with the given elements.

#### Arguments

|  |
| --- | ---
| `g_arg1` | Element to be added to a list.
|  |
| --- | ---
| `g_arg2` | Additional elements to be added to a list
#### Value Returned

|  |
| --- | ---
| `l_result` | List whose elements are`g_arg1`, `g_arg2`, and so on.
|  |
| --- | ---
| `nil` | No arguments are given.
#### Example

`list(1 2 3)     => (1 2 3)list('a 'b 'c)  => (a b c)`

#### Reference

`car, cdr, cons, listp, tconc`

### listp

`listp( g_value ) => t | nil`

#### Description

Checks if an object is a list.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A data object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is a list, a data type whose internal name is also `list`. Note that `listp(nil)` returns `t`.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`listp('(1 2 3))  => tlistp( nil )     => tlistp( 1 )       => nil`

#### Reference

`list`

### nconc

`nconc( l_arg1 l_arg2 [ l_arg3 ... ] ) => l_result`

#### Description

Equivalent to a destructive`append` where the first argument is actually modified.

This results in`nconc` being much faster than `append` but not quite as fast as `tconc` and `lconc`. Thus `nconc` returns a list consisting of the elements of `l_arg1`, followed by the elements of `l_arg2`, followed by the elements of `l_arg3`, and so on. The `cdr` of the last list cell of `l_arg`i is modified to point to`l_arg`i+1. Thus caution must be taken because if `nconc` is called with the `l_arg`i two consecutive times it can form an infinite structure where the *cdr* of the last list cell of `l_arg`i points to the *car* of `l_arg`i.

Use the`nconc` function principally to reduce the amount of memory consumed. A call to `append` would normally duplicate the first argument whereas `nconc` does not duplicate any of its arguments, thereby reducing memory consumption.

#### Arguments

|  |
| --- | ---
| `l_arg1` | List of elements.
|  |
| --- | ---
| `l_arg2` | List elements concatenated to`l_arg1`.
|  |
| --- | ---
| `l_arg3` | Additional lists.
#### Value Returned

|  |
| --- | ---
| `l_result` | The modified value of`l_arg1`.
#### Example

```
x = '(a b c) nconc( x '(d))        ; x is now (a b c d)nconc( x '(e f g) )   ; x is now the list (a b c d e f g)nconc( x x )          ; Forms an infinite structure.
```

> This forms an infinite list structure (a b c d e f g a b c d e f g ...).

#### Reference

`lconc, tconc`

### ncons

`ncons( g_element ) => l_result`

#### Description

Builds a list containing an element. Equivalent to`cons(` `g_element``nil )`.

#### Arguments

|  |
| --- | ---
| `g_element` | Element to be added to the beginning of an empty list.
#### Value Returned

|  |
| --- | ---
| `l_result` | A list with`g_element` as its single element.
#### Example

`ncons( 'a )    => (a)z = '(1 2 3)   => (1 2 3)ncons( z )     => ((1 2 3))`

#### Reference

`list`

### nth

`nth( x_index0 l_list ) => g_result | nil`

#### Description

Returns an index-selected element of a list, assuming a zero-based index.

Thus`nth(0``l_list``)` is the same as `car(``l_list``)`. The value `nil` is returned if `x_index0` is negative or is greater than or equal to the length of the list.

#### Arguments

|  |
| --- | ---
| `x_index0` | Index of the list element you want returned.
|  |
| --- | ---
| `l_list` | List of elements.
#### Value Returned

|  |
| --- | ---
| `g_result` | Indexed element of`l_list`, assuming a zero-based index
|  |
| --- | ---
| `nil` | If`x_index0` is negative or is greater than or equal to the length of the list.
#### Example

```
nth( 1 '(a b c) )    => bz = '(1 2 3)         => (1 2 3)nth(2 z)             => 3nth(3 z)             => nil
```

#### Reference

`list, nthcdr, nthelem`

### nthcdr

`nthcdr( x_count l_list ) => l_result`

#### Description

Applies`cdr` to a list a given number of times.

#### Arguments

|  |
| --- | ---
| `x_count` | Number of times to apply`cdr` to `l_list`.
|  |
| --- | ---
| `l_list` | List of elements.
#### Value Returned

|  |
| --- | ---
| `l_result` | Result of applying`cdr` to `l_list`, `x_count` number of times.
#### Example

```
nthcdr( 3 '(a b c d))  => (d)z = '(1 2 3)nthcdr(2 z)            => (3)nthcdr(-1 z)           => (nil 1 2 3)
```

If`x_count` is less than 0, then `cons(nil``l_list``)` is returned.

#### Reference

`nth`

### nthelem

`nthelem( x_index1 l_list ) => g_result | nil`

#### Description

Returns the indexed element of the list, assuming a one-based index.

Thus`nthelem(1``l_list``)` is the same as `car(``l_list``)`.

#### Arguments

|  |
| --- | ---
| `x_index1` | Index of the element of`l_list` you want returned.
|  |
| --- | ---
| `l_list` | List of elements.
#### Value Returned

|  |
| --- | ---
| `g_result` | The`x_index1` element of `l_list`.
|  |
| --- | ---
| `nil` | If`x_index1` is less than or equal to 0 or is greater than the length of the list.
#### Example

`nthelem( 1 '(a b c) )  => az = '(1 2 3)nthelem(2 z)           => 2`

#### Reference

`nth`

### pairp

`pairp( g_obj ) => t | nil`

#### Description

Checks if an object is a`cons` object, that is, a non-empty list.

This function is equivalent to`dtpr`.

#### Arguments

|  |
| --- | ---
| `g_obj` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | `g_obj` is a `cons` object.
|  |
| --- | ---
| `nil` | `g_obj` is not a `cons` object.
#### Example

`(pairp nil)        => nil(pairp 123)        => nil(pairp '(1 2))     => t`

#### Reference

`listp`

### range

`range( n_num1 n_num2 ) => l_result`

#### Description

Returns a list whose first element is`n_num1` and whose tail is `n_num2`. Prefix form of the `:` operator.

#### Arguments

|  |
| --- | ---
| `n_num1` | First element of the list.
|  |
| --- | ---
| `n_num2` | Tail of the list.
#### Value Returned

|  |
| --- | ---
| `l_result` | Result of the operation.
#### Example

`L = range(1 2) => (1 2)car(L) => 1cdr(L) => (2)`

L = range(1.1 3.3) => (1.1 3.3)
car(L) => 1.1
cdr(L) => (3.3)

### remd

`remd( g_x l_arg ) => l_result`

#### Description

Removes all top-level elements`equal` to a SKILL object from a list. This is a destructive removal, which means that the original list itself is modified. Therefore, any other reference to that list will also see the changes.

`remd` uses `equal` for comparison.

* ***This is a destructive removal. The original list itself will be modifiedexcept for the first element from the original list. Therefore, any other reference to that list will also see the changes. See example 3 where the same variable is used to hold the updated list.***

#### Arguments

|  |
| --- | ---
| `g_x` | Any SKILL object to be removed from the list.
|  |
| --- | ---
| `l_arg` | List from which to remove`g_x`.
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns`l_arg` modified so that all top-level elements equal to `g_x` are removed.
#### Example 1

`y = '("a" "b" "x" "d" "f")  => ("a" "b" "x" "d" "f")`

`remd( "x" y)                => ("a" "b" "d" "f")`

`y                           => ("a" "b" "d" "f")`

#### Example 2

The first element from the original list will not be modified in-place.

`y = '("a" "b" "d" "f")  => ("a" "b" "d" "f")`

`remd( "a" y)                => ("b" "d" "f")`

`y                           => ("a" "b" "d" "f")`

Note the original list, y, is not modified.

#### Example 3

In order to remove the first element from the original list, use the same variable (that holdsthe original list) to hold the updated list.

`y = '("a" "b" "d" "f")      => ("a" "b" "d" "f")`

`y=remd("a" y)               => ("b" "d" "f")`

`y                           => ("b" "d" "f")`

#### Reference

`remdq, remove, remq`

### remdq

`remdq( g_x l_arg ) => l_result`

#### Description

Removes all top-level elements that are identical to a SKILL object using`eq` from a list. This is a destructive removal, which means that the original list itself is modified. Therefore, any other reference to that list will also see the changes.

`remdq` uses `eq` instead of `equal` for comparison.

* ***This is a destructive removal, which means that the original list itself ismodified. Therefore, any other reference to that list will also see the changes.***

#### Arguments

|  |
| --- | ---
| `g_x` | Any SKILL object to be removed from the list.
|  |
| --- | ---
| `l_arg` | List from which to remove`g_x`.
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns`l_arg` modified so that all top-level elements `eq` to `g_x` are removed.
#### Example

```
y = '(a b x d f x g)    => (a b x d f x g)remdq('x y)             => (a b d f g)y                       => (a b d f g)
```

#### Reference

`remd, remove, remq`

### remove

`remove( g_x l_arg ) => l_resultremove( g_key o_table ) => g_value`

#### Description

Returns a copy of a list with all top-level elements`equal` to a SKILL object removed. Can also be used to remove an entry from an association table, in which case the removal is destructive, that is, any other reference to the table will also see the changes. `remove` uses `equal` for comparison. `remove` can also be used with an association table to identify and remove an entry corresponding to the key specified in the function.

#### Arguments

|  |
| --- | ---
| `g_x` | Any SKILL object to be removed from the list.
|  |
| --- | ---
| `l_arg` | List from which to remove`g_x`.
|  |
| --- | ---
| `g_key` | Key or first element of the key/value pair.
|  |
| --- | ---
| `o_table` | Association table containing the key/value pairs to be processed.
#### Value Returned

|  |
| --- | ---
| `l_result` | Copy of`l_arg` with all top-level elements equal to `g_x` removed.
|  |
| --- | ---
| `g_value` | Value associated with the key that is removed.
#### Example

`remove( "x" '("a" "b" "x" "d" "f")) => ("a" "b" "d" "f")`

`myTable = makeTable("myTable" -1) => table:myTable                ;default is -1`

`myTable["two"]=2=> 2`

```
remove("two" myTable)=> 2                            ; permanently removed from table
```

`myTable["two"]=> -1                          ; the default value`

#### Reference

`remd, remove, remq`

### remq

`remq( g_x l_arg ) => l_result`

#### Description

Returns a copy of a list with all top-level elements that are identical to a SKILL objectremoved. Uses `eq`.

#### Arguments

|  |
| --- | ---
| `g_x` | Any SKILL object to be removed from the list.
|  |
| --- | ---
| `l_arg` | List from which to remove`g_x`.
#### Value Returned

|  |
| --- | ---
| `l_result` | A copy of`l_arg` with all top-level elements `eq` to `g_x` removed.
#### Example

`remq('x '(a b x d f x g)) => (a b d f g)`

#### Reference

`remd, remove`

### reverse

`reverse( l_arg ) => l_result`

#### Description

Returns a copy of the given list with the elements in reverse order.

Because this function copies the list, it uses a lot of memory for large lists.

#### Arguments

|  |
| --- | ---
| `l_arg` | A list.
#### Value Returned

|  |
| --- | ---
| `l_result` | A new list with the elements at the top level in reverse order.
#### Example

```
reverse( '(1 2 3) )        => (3 2 1)reverse( '(a b (c d) e) )  => '(e (c d) b a)
```

### rplaca

`rplaca( l_arg1 g_arg2 ) => l_result`

#### Description

Replaces the first element of a list with an object. This function does not create a new list; italters the input list. Same as `setcar`.

* ***This is a destructive operation, meaning that any other reference to thelist will also see the change.***

#### Arguments

|  |
| --- | ---
| `l_arg1` | A list.
|  |
| --- | ---
| `g_arg2` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `l_result` | Modified`l_arg1` with the `car` of `l_arg1` replaced by `g_arg2`.
#### Example

`x = '(a b c)rplaca( x 'd )    => (d b c)x                 => (d b c)`

The`car` of `x` is replaced by the second argument.

#### Reference

`rplacd, setcar, setcdr`

### rplacd

`rplacd( l_arg1 l_arg2 ) => l_result`

#### Description

Replaces the tail of a list with the elements of a second list. This function does not create anew list; it alters the input list. Same as `setcdr`.

* ***This is a destructive operation, meaning that any other reference to thelist will also see the changes.***

#### Arguments

|  |
| --- | ---
| `l_arg1` | List that is modified.
|  |
| --- | ---
| `l_arg2` | List that replaces the`cdr` of `l_arg1`.
#### Value Returned

|  |
| --- | ---
| `l_result` | Modified`l_arg1` with the `cdr` of the list `l_arg1` replaced with `l_arg2`.
#### Example

`x = '(a b c)rplacd( x '(d e f))  => (a d e f)x                    => (a d e f)`

The`cdr` of `x` is replaced by the second argument.

#### Reference

[rplaca](#1040002 "List Functions"), [setcar](#1040134 "List Functions"), [setcdr](#1040165 "List Functions")

### setcar

`setcar( l_arg1 g_arg2 ) => l_result`

#### Description

Replaces the first element of a list with an object. Same as`rplaca`.

* ***This is a destructive operation, meaning that any other reference to thelist will also see the change.***

#### Arguments

|  |
| --- | ---
| `l_arg1` | A list.
|  |
| --- | ---
| `g_arg2` | A SKILL object.
#### Value Returned

|  |
| --- | ---
| `l_result` | Modified`l_arg1` with the `car` of `l_arg1` replaced by `g_arg2`.
#### Example

```
x = '(a b c)        => (a b c)setcar( x 'd )      => (d b c)x                   => (d b c)
```

The`car` of `x` is replaced by the second argument.

#### Reference

`rplacd, rplaca, setcdr`

### setcdr

`setcdr( l_arg1 l_arg2 ) => l_result`

#### Description

Replaces the tail of a list with the elements of a second list. Same as`rplacd`.

* ***This is a destructive operation, meaning that any other reference to thelist will also see the change.***

#### Arguments

|  |
| --- | ---
| `l_arg1` | List that is modified.
|  |
| --- | ---
| `l_arg2` | List that replaces the`cdr` of `l_arg1`.
#### Value Returned

|  |
| --- | ---
| `l_result` | Modified`l_arg1` with the `cdr` of the list `l_arg1` replaced with `l_arg2`.
#### Example

```
x = '(a b c)setcdr( x '(d e f))    => (a d e f)x                      => (a d e f)
```

The`cdr` of `x` is replaced by the second argument.

#### Reference

[rplacd](#1040068 "List Functions"), [setcar](#1040134 "List Functions"), [rplaca](#1040002 "List Functions")

### tailp

`tailp( l_arg1 l_arg2 ) => l_arg1 | nil`

#### Description

Returns`arg1` if a list cell `eq` to `arg1` is found by `cdr` down `arg2` zero or more times, `nil` otherwise.

Because`eq` is being used for comparison `l_arg1` must actually point to a tail list in `l_arg2` for this predicate to return a non-`nil` value.

#### Arguments

|  |
| --- | ---
| `l_arg1` | A list.
|  |
| --- | ---
| `l_arg2` | Another list, which can contain`l_arg1` as its tail.
#### Value Returned

|  |
| --- | ---
| `l_arg` | If a list cell`eq` to `l_arg1` is found by `cdr`'ing down `l_arg2` zero or more times.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

```
y = '(b c)z = cons( 'a y )    => (a b c)tailp( y z )        => (b c)tailp( '(b c) z )   => nil
```

`nil` was returned because '`(b c)` is not `eq` the `cdr( z )`.

### tconc

`tconc( l_ptr g_x ) => l_result`

#### Description

Creates a list cell whose`car` points to a list of the elements being constructed and whose `cdr` points to the last list cell of the list being constructed.

A`tconc` structure is a special type of list that allows efficient addition of objects to the end of a list. It consists of a list cell whose `car` points to a list of the elements being constructed with `tconc` and whose `cdr` points to the last list cell of the list being constructed. If `l_ptr` is `nil`, a new `tconc` structure is automatically created. To obtain the list under construction, take the `car` of the `tconc` structure.

`tconc` and `lconc` are much faster than `append` when adding new elements to the end of a list. The `append` function is much slower, because it traverses and copies the list to reach the end, whereas `tconc` and `lconc` only manipulate pointers.

|  |
| --- | ---
| `l_ptr` | A`tconc` structure. Must be initialized to `nil` to create a new `tconc` structure.
|  |
| --- | ---
| `g_x` | Element to add to the end of the list.
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns`l_ptr`, which must be a `tconc` structure or `nil`, with `g_x` added to the end.
#### Example

```
x = tconc(nil 1)        ; x is now ((1) 1)tconc(x 2)              ; x is now ((1 2) 2)tconc(x 3)              ; x is now ((1 2 3) 3)x = car(x)              ; x is now (1 2 3)
```

`x` now equals `(1 2 3)`, the desired result.

#### Reference

`lconc`

### xcons

`xcons( l_list g_element ) => l_result`

#### Description

Adds an element to the beginning of a list. Equivalent to `cons` but the order of the arguments is reversed.

#### Arguments

|  |
| --- | ---
| `l_list` | A list, which can be`nil`.
|  |
| --- | ---
| `g_element` | Element to be added to the beginning of`l_list`.
#### Value Returned

|  |
| --- | ---
| `l_result` | Returns a list.
#### Example

`xcons( '(b c) 'a ) => ( a b c )`

#### Reference

`append1, lconc, list, ncons, tconc`

### xCoord

`xCoord( l_list ) => g_result`

#### Description

Returns the first element of a list. `D`oes not modify the argument list.

**Note:** The`xCoord` and `yCoord` functions are aliases for the [*car*](../sklangref/list.html#car) and [*cadr*](../sklangref/list.html#cadr) functions.

#### Arguments

|  |
| --- | ---
| `l_list` | A list of elements.
#### Value Returned

|  |
| --- | ---
| `g_result` | Returns the first element in a list.
#### Example

`xValue = 300 yValue = 400 aCoordinate = xValue:yValue => ( 300 400 )`

xCoord( aCoordinate ) => 300
yCoord( aCoordinate ) => 400

### yCoord

`yCoord( l_list ) => g_result`

#### Description

Returns the tail of the list, that is, the list without its first element.

**Note:** The`xCoord` and `yCoord` functions are aliases for the [*car*](../sklangref/list.html#car) and [*cadr*](../sklangref/list.html#cadr) functions.

#### Arguments

|  |
| --- | ---
| `l_list` | A list of elements.
#### Value Returned

|  |
| --- | ---
| `g_result` | Returns the end of a list, or the list minus the first element.
#### Example

`xValue = 300 yValue = 400 aCoordinate = xValue:yValue => ( 300 400 )`

xCoord( aCoordinate ) => 300
yCoord( aCoordinate ) => 400




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
