### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

2
=

Data Structure
==============

### arrayp

`arrayp( g_value ) => t | nil`

#### Description

Checks if an object is an array.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | Any data object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is an array object.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`declare(x[10])arrayp(x)  => tarrayp('x) => nil`

#### Reference

`declare`

### arrayref

`arrayref( g_collection g_index ) => g_element`

#### Description

Returns the element in a collection that is in an array or a table of the given index.

This function is usually called implicitly using the`[ ]` syntax.

#### Arguments

|  |
| --- | ---
| `g_collection` | An array or a table.
|  |
| --- | ---
| `g_index` | An integer for indexing an array. An arbitrary object for indexinga table.
#### Value Returned

|  |
| --- | ---
| `g_element` | The element selected by the given index in the given collection.
#### Example

`a[3] => 100              ;if the fourth element of the array is 100`

`(arrayref a 3 )=> 100              ;same as a[3]`

#### Reference

The syntax`a[i] = b`, referred to as the [setarray](#1039356 "Data Structure") function.

### assoc, assq, assv

`assv( g_key l_alist ) => l_association | nil`

#### Description

The`assoc`,`assq`, and `assv` functions find the first list in `l_alist` whose car field is `g_key` and return that list. `assq` uses `eq` to compare `g_key` with the car fields of the lists in `alist`. `assoc` uses `equal`. `assv` uses `eqv`.

The association list,`l_alist`, must be a list of lists. An association list is a standard data structure that has the form `((key1``value1``) (key2``value2``) (key3``value3``) ...)`. These functions find the first list in `l_alist` whose car field is `g_key` and return that list. `assq` uses `eq` to compare `g_key` with the car fields of the lists in `l_alist`*.* `assv` uses `eqv`*.* `assoc` uses `equal`.

#### Arguments

|  |
| --- | ---
| `g_key` | An arbitrary object as the search key.
|  |
| --- | ---
| `l_alist` | Association list. Must be a list of lists.
#### Value Returned

|  |
| --- | ---
| `l_association` | The returned list is always an element of`l_alist`.
|  |
| --- | ---
| `nil` | If no list in`l_alist` has `g_key`, as its `car`.
#### Example

```
e = '((a 1) (b 2) (c 3))(assq 'a e) => (a 1)(assq 'b e) => (b 2)(assq 'd e) => nil(assq (list 'a) '(((a)) ((b)) ((c)))) => nil(assoc (list 'a) '(((a)) ((b)) ((c)))) => ((a))(assv 5 '((2 3) (5 7) (11 13))) => (5 7)
```

#### Reference

[eq](logicalrel.html#1038850 "Logical and Relational Functions"), [equal](logicalrel.html#1038894 "Logical and Relational Functions"), [eqv](logicalrel.html#1038922 "Logical and Relational Functions")

### declare

`declare( s_arrayName [ x_sizeOfArray ] ) => a_newArray`

#### Description

Creates an array with a specified number of elements. This is a syntax form. All elements of the array are initialized to `unbound`.

#### Arguments

|  |
| --- | ---
| `s_arrayName` | Name of the array. There must be no white space between thename of an array and the opening bracket containing the size.
|  |
| --- | ---
| `x_sizeOfArray` | Size of the array as an integer.
#### Value Returned

|  |
| --- | ---
| `a_newArray` | Returns the new array.
#### Example

When the name of an array appears on the right side of an assignment statement, only apointer to the array is used in the assignment; the values stored in the array are not copied. It is therefore possible for an array to be accessible by different names. Indices are used to specify elements of an array and always start with 0; that is, the first element of an array is element 0. SKILL checks for an out of bounds array index with each array access.

`declare(a[10])a[0] = 1a[1] = 2.0a[2] = a[0] + a[1]`

Creates an array of 10 elements. *a* is the name of the array, with indices ranging from 0 to 9. Assigns the integer 1 to element 0, the float 2.0 to element 1, and the float 3.0 to element 2.

`b = a`

`b` now also refers to the same array as `a`.

`declare(c[10])`

declares another array of 10 elements.

`declare(d[2])`

declares`d` as array of 2 elements.

`d[0] = b`

`d[0]` now refers to the array pointed to by `b` and `a`.

`d[1] = c`

`d[1]` is the array referred to by `c`.

`d[0][2]`

Accesses element 2 of the array referred to by`d[0]`.
This is the same element as `a[2]`.

Brackets (`[]`) are used in this instance to represent array references and are part of the statement syntax.

#### Reference

[Vector](#1039306 "Data Structure")

### defprop

`defprop( s_id g_value s_name ) => g_value`

#### Description

Adds properties to symbols but none of its arguments are evaluated. This is a syntax form.

The same as`putprop` except that none of its arguments are evaluated.

#### Arguments

|  |
| --- | ---
| `s_id` | Symbol to add property to.
|  |
| --- | ---
| `g_value` | Value of the named property.
|  |
| --- | ---
| `s_name` | Named property.
#### Value Returned

|  |
| --- | ---
| `g_value` | Value of the named property.
#### Example

`defprop(s 3 x)   => 3`

Sets property`x` on symbol `s` to 3.

`defprop(s 1+2 x) => (1+2)`

Sets property`x` on symbol `s` to the unevaluated expression 1+2.

#### Reference

[get](dataoperator.html#1038893 "Data Operator Functions"), [putprop](dataoperator.html#1040238 "Data Operator Functions")

### defstruct

`defstruct( s_name s_slot1 [ s_slot2.. ] ) => t`

#### Description

Creates a`defstruct`, a named structure that is a collection of one or more variables.

`Defstructs` can have slots of different types that are grouped together under a single name for handling purposes. They are the equivalent of structs in C. The `defstruct` form also creates an instantiation function, named `_<``name``>` where `<name>` is the structure name supplied to `defstruct`. This constructor function takes keyword arguments: one for each slot in the structure. Once created, structures behave just like disembodied property lists.

**Note:** Just like disembodied property lists, structures can have new slots added at any time.However these dynamic slots are less efficient than the statically declared slots, both in access time and space utilization.

Structures can contain instances of other structures; therefore one needs to be careful aboutstructure sharing. If sharing is not desired, a special copy function can be used to generate a copy of the structure being inserted. The `defstruct` form also creates a function for the given `defstruct` called `copy_<``name``>`. This function takes one argument, an instance of the `defstruct`. It creates and returns a copy of the given instance. An example appears after the description of the other defstruct functions.

#### Arguments

|  |
| --- | ---
| `s_name` | A structure name.
|  |
| --- | ---
| `s_slot1` | Name of the first slot in structure`s_name`.
|  |
| --- | ---
| `s_slot2` | Name of the second slot in structure`s_name`.
#### Value Returned

|  |
| --- | ---
| `t` | Always.
#### Example

```
defstruct(myStruct slot1 slot2 slot3) => tstruct = _myStruct(?slot1 "one" ?slot2 "two"                        ?slot3 "three")
```

`struct->slot1 => "one"`

Returns the value associated with a slot of an instance.

`struct->slot1 = "new" => "new"`

Modifies the value associated with a slot of an instance.

`struct->? => (slot3 slot2 slot1)`

Returns a list of the slot names associated with an instance.

`struct->?? => (slot3 "three" slot2 "two" slot1 "new")`

Returns a property list (not a disembodied property list) containing the slot names and valuesassociated with an instance.

#### Reference

[defstruct](#defstruct "Data Structure"), `prints``truct`

### defstructp

`defstructp( g_object [ S_name ] ) => t | nil`

#### Description

Checks if an object is an instance of a particular`defstruct`.

If the optional second argument is given, it is used as the`defstruct` name to check against. The suffix `p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_object` | A data object.
|  |
| --- | ---
| `S_name` | Name of the structure to be tested for.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_object` is an instance of `defstruct` `S_name`.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

```
defstruct(myStruct slot1 slot2 slot3) => tstruct = _myStruct(?slot1 "one" ?slot2 "two" ?slot3 "three")=> array[5]:3555552
```

`defstructp( "myDefstruct") => nildefstructp(struct 'myStruct) => t`

#### Reference

[defstruct](#defstruct "Data Structure"), `prints``truct`

### defvar

`defvar( s_varName [ g_value ] ) => g_value | nil`

#### Description

Defines a global variable and assigns it a value. You can also use the`defun` or `define` syntax form to define global variables in SKILL++ mode.

#### Arguments

|  |
| --- | ---
| `s_varName` | Name of the variable to be defined.
|  |
| --- | ---
| `g_value` | Value to assign to the variable. If`g_value` is not given, `nil` is assigned to the variable.
#### Value Returned

|  |
| --- | ---
| `g_value` | If given.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`defvar(x 3) => 3`

Assigns`x` a value of 3.

#### Reference

[defprop](#1038889 "Data Structure"), [set](dataoperator.html#1040473 "Data Operator Functions"), [setq](dataoperator.html#1040675 "Data Operator Functions")

### makeTable

`makeTable( S_name [ g_default_value ] ) => o_table`

#### Description

Creates an empty association table.

#### Arguments

|  |
| --- | ---
| `S_name` | Print name (either a string or symbol) of the new table.
|  |
| --- | ---
| `g_default_value` | Default value to be returned when references are made to keysthat are not in the table. If no default value is given, the system returns `unbound` if the key is not defined in the table.
#### Value Returned

|  |
| --- | ---
| `o_table` | The new association table.
#### Example

```
myTable = makeTable("atable1" 0)   => table:atable1myTable[1]                         => 0
```

If you specify a default value when you create the table, the default value is returned if anonexistent key is accessed.

```
myTable2 = makeTable("atable2")   => table:atable2myTable2[1]                       => unbound
```

If you do not specify a default value when you create the table, the symbol`unbound` is returned if an undefined key is accessed.

```
myTable[1] = "blue"               => bluemyTable["two"] = '(r e d)         => (r e d)myTable['three] = 'green          => green
```

You can refer to and set the contents of an association table with the standard syntax foraccessing array elements.

`myTable['three]                   => green`

#### Reference

[declare](#1038822 "Data Structure")

### Vector

`Vector( x_size [ g_init_val ] )=> a_vectorArray`

#### Description

Creates an array (vector) with the specified number of elements, and optionally initializeseach entry.

Allocates a vector of`x_size` number of entries. `Vector` initializes each entry in the vector with `g_init_val`. The default value of `g_init_val` is the symbol `unbound`.

#### Arguments

|  |
| --- | ---
| `x_size` | Size of the vector to be allocated.
|  |
| --- | ---
| `g_init_val` | Initial value of each entry of thevector to be allocated.
#### Value Returned

|  |
| --- | ---
| `a_vectorArray` | Array of the given size.
#### Example

```
V = Vector( 3 0 )   => array[3]:1955240V[0]                    => 0V[1]                    => 0V[2]                    => 0
```

### setarray

```
setarray( a_array x_index g_value ) => g_valuesetarray( o_table g_key g_value ) => g_value
```

#### Description

Assigns the given value to the specified element of an array or to the specified key of a table.Normally this function is invoked implicitly using the array-subscription syntax, such as, x[i] = v.

Assigns`g_value` to the `x_index` element of `a_array`, or adds the association of `g_value` with `g_key` to `o_table`, and returns `g_value`. Normally this function is invoked implicitly using the array-subscription syntax, such as, x[i] = v.

#### Arguments

|  |
| --- | ---
| `a_array` | An array object.
|  |
| --- | ---
| `x_index` | Index of the array element to assign a value to. Must be between0 and one less than the size of the array.
|  |
| --- | ---
| `g_key` | Any SKILL value.
|  |
| --- | ---
| `g_value` | Value to be assigned to the specified array element or tableentry.
#### Value Returned

|  |
| --- | ---
| `g_value` | Value assigned to the specified array element or table entry.
#### Example

```
declare(myar[8])    => array[8]:3895304myar[0]             => unboundsetarray(myar 0 5)  => 5myar[0]             => 5setarray(myar 8 'hi)
```

Signals an array bounds error.

```
setarray(myar     (plus 1 2)                ; assigns element 3 the value 8.    (plus 3 5))     => 8
```

```
mytab = makeTable('myTable) => table:myTablesetarray(mytab 8 4)  => 4mytab[8]             => 4mytab[9] = 3         => 3     ; same as setarray(mytab 9 3)mytab[9]             => 3
```

#### Reference

[arrayref](#1038715 "Data Structure"), [declare](#1038822 "Data Structure")

### tablep

`tablep( g_object ) => t | nil`

#### Description

Checks if anobject is an association table.

#### Arguments

|  |
| --- | ---
| `g_object` | A SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_object` is an association table.
|  |
| --- | ---
| `nil` | If`g_object` is not an association table.
#### Example

```
myTable = makeTable("atable1" 0)    => table:atable1tablep(myTable)                     => ttablep(9)                           => nil
```

#### Reference

[makeTable](#1043790 "Data Structure")

### type, typep

`type( g_value ) => s_type | niltypep( g_value ) => s_type | nil`

#### Description

Returns a symbol whose name denotes the type of a data object. The functions`type` and `typep` are identical.

#### Arguments

|  |
| --- | ---
| `g_value` | A data object.
#### Value Returned

|  |
| --- | ---
| `s_type` | Symbol whose name denotes the type of`g_value`.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`type( 'foo )    => symboltypep( "foo" )  => string`

#### Reference

[fixp](arithmetic.html#1039304 "Arithmetic Functions"), [floatp](arithmetic.html#1039359 "Arithmetic Functions"), [numberp](logicalrel.html#1039447 "Logical and Relational Functions"), [portp](inputoutput.html#1040208 "Input Output Functions"), [stringp](stringfunc.html#1040671 "String Functions"), [symbolp](dataoperator.html#1040737 "Data Operator Functions")

### vector

`vector( g_value ... )=> a_vectorArray`

#### Description

Returns a vector, or array, filled with the arguments in the given order. The`vector` function is analogous to the `list` function.

A vector is implemented as a SKILL array.

#### Arguments

|  |
| --- | ---
| `g_value` | Ordered list of values to be placed in an array.
#### Value Returned

|  |
| --- | ---
| `a_vectorArray` | Array filled with the arguments in the given order.
#### Example

`V = vector( 1 2 3 4 ) => array[4]:33394440V[0] => 1V[3] => 4`

#### Reference

[declare](#1038822 "Data Structure"), [list](list.html#1039311 "List Functions"), [Vector](#1039306 "Data Structure")

### vectorp

`vectorp( g_value ) => t | nil`

#### Description

Checks if an object is a vector. Behaves the same as`arrayp`.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | Any data object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is a vector object.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`declare(x[10])arrayp(x) => tarrayp('x) => nil`

#### Reference

[declare](#1038822 "Data Structure"), [arrayp](#1038672 "Data Structure")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
