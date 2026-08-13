### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

3
=

Data Operator Functions
=======================

### alphaNumCmp

`alphaNumCmp( S_arg1 S_arg2 [ g_arg3 ] ) => 1 | 0 | -1`

#### Description

Compares twostring or symbol names alphanumerically or numerically.

If the third optional argument is non-`nil` and the first two arguments are strings holding purely numeric values, then a numeric comparison is performed on the numeric representation of the strings.

#### Arguments

|  |
| --- | ---
| `S_arg1` | First string or symbol to compare.
|  |
| --- | ---
| `S_arg2` | String or symbol to compare against`S_arg1`.
|  |
| --- | ---
| `g_arg3` | If non-`nil`, can cause a numeric comparison of `S_arg1` and `S_arg2` depending whether those arguments are strings holding purely numeric values.
#### Value Returned

1. If`S_arg1` is alphanumerically greater than `S_arg2`

1. If`S_arg1` is alphanumerically identical to `S_arg2`.

|  |
| --- | ---
| `-1` | If`S_arg2` is alphanumerically greater than `S_arg1`.
#### Example

```
alphaNumCmp( "a" "b" )               => -1alphaNumCmp( "b" "a" )               => 1alphaNumCmp( "name12" "name12" )     => 0alphaNumCmp( "name23" "name12" )     => 1alphaNumCmp( "00.09" "9.0E-2" t)     => 0
```

#### Reference

[strcmp](stringfunc.html#1040645 "String Functions"), [strncmp](stringfunc.html#1040843 "String Functions")

### concat

`concat( Sx_arg1 [ Sx_arg2 ... ] ) => s_result`

#### Description

Concatenates strings, symbols, or integers into a single symbol.

This function is useful for converting strings to symbols. To concatenate several strings andhave a single string returned, use the `strcat` function. Symbol names are limited to 255 characters.

Symbol functions such as`eq`, `memq`, and `caseq` are much faster than their siblings `equal`, `member`, and `case` because they compare pointers rather than data. You can use `concat` to convert a string to a symbol before performing `memq` on large lists for increased speed.

#### Arguments

|  |
| --- | ---
| `Sx_arg1` | String, symbol, or integer to be concatenated.
|  |
| --- | ---
| `Sx_arg2` | Zero or more strings, symbols, or integers to be concatenated.
#### Value Returned

|  |
| --- | ---
| `s_result` | Returns a symbol whose print name is the result ofconcatenating the printed representation of the argument or arguments.
#### Example

```
concat("string")                      => stringconcat("ab" 123 'xy)                  => ab123xymemq( concat( "c" ) '(a b c d e))     => (c d e)
```

This demonstrates using`concat` to take advantage of the faster functions such as `memq`.

#### Reference

[strcat](stringfunc.html#1053714 "String Functions"), [member, memq, memv](logicalrel.html#1039268 "Logical and Relational Functions")

### copy\_<name>

`copy_<name>( r_defstruct ) => r_defstruct`

#### Description

Creates and returns a copy of a structure. This function is created by the`defstruct` function where `<name>` is the name of the defstruct.

Structures can contain instances of other structures; therefore you need to be careful aboutstructure sharing. If sharing is not desired, use the `copyDefstructDeep` function to generate a copy of the structure and its sub-elements.

#### Arguments

|  |
| --- | ---
| `r_defstruct` | An instance of a defstruct.
#### Value Returned

|  |
| --- | ---
| `r_defstruct` | Copy of the given instance
#### Example

```
defstruct(myStruct a b c) => tm1 = _myStruct(?a 3 ?b 2 ?c 1) => array[x]:xxxxm2 = copy_myStruct(m1) => array[x]:xxxx
```

#### Reference

`copyDefstructDeep, _<name>, printstruct`

### copyDefstructDeep

`copyDefstructDeep( r_object ) => r_defstruct`

#### Description

Performs a deep or recursive copy on defstructs with other defstructs as sub-elements,making copies of all the defstructs encountered.

The various`copy_<``name``>` functions are called to create copies for the various defstructs encountered in the deep copy.

**Note:** Only defstruct sub-elements are recursively copied. Other data types, like lists, are stillshared.

#### Arguments

|  |
| --- | ---
| `r_object` | An instance of a`defstruct`.
#### Value Returned

|  |
| --- | ---
| `r_defstruct` | A deep copy of the given instance.
#### Example

`defstruct(myStruct a b c) => t ;creates a function _myStruct`

`m1 = _myStruct(?a 3 ?b 2 ?c 1) => array[5]:3873024`

```
m2 = _myStruct(?a m1 ?b '(a b c) ?c 5) => array[5]:3873208         ; m1 is m2's sub-element
```

`m3 = copyDefstructDeep(m2) => array[5]:3873056         ; uses deep copy`

`m3->a => array[5]:3873344         ; a new object`

`eq(m3->a m2->a) => nil      ; eq checks object identity`

`m2->b => (a b c)`

```
eq(m3->b m2->b) => t                       ; still sharing the same object because                           ; the sub-element b is not a defstruct
```

`m4 = copy_myStruct(m2) => array[5]:3873376        ; uses shallow copy`

```
m4->a => array[5]:3873024eq(m4->a m2->a) => t       ; share identical substructureeq(m4->b m2->b) => t       ; the same object
```

#### Reference

[copy\_<name>](#1038791 "Data Operator Functions"), `prints``truct`,

### get

`get( sl_id S_name ) => g_result | nil`

#### Description

Returns the value of a property in a property list (including disembodied property list),association table, structure, database object, and a standard object (instance of a user defined subclass of standardObject). `get` has no infix operator syntax.

Used in conjunction with`putprop`, where `putprop` stores the property and `get` retrieves it.

#### Arguments

|  |
| --- | ---
| `sl_id` | Symbol or disembodied property list.
|  |
| --- | ---
| `S_name` | Name of the property you want the value of.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of`S_name` in the `sl_id` property list.
|  |
| --- | ---
| `nil` | The named property does not exist.
#### Example

`putprop( 'chip 8 'pins ) => 8`

Assigns the property pins to a value of 8 to the symbol chip.

`get( 'chip 'pins ) => 8chip.pins => 8`

`x = '(nil a 3 b 4)          ;a disembodied property listx->a => 3get(x 'a) => 3`

#### Reference

[plist](#1039739 "Data Operator Functions"), [putprop](#1040238 "Data Operator Functions")

### getSG

`getSG(g_objS_prop)=>g_propValue`

#### Description

Evaluates and then retrieves the value of the specified attribute or property. It is a lambdaimplementation of `getSGq()`.

#### Arguments

|  |
| --- | ---
| `g_obj` | Specifies the name of an object
| `S_prop` | Specifies the name of the attribute or property for which youwant to retireve the value
#### Value Returned

|  |
| --- | ---
| `g_propValue` | The value of the property
#### Example

In the following example,`getSG()` evaluates the `tbl_list` argument and then retrieves its value.

`tbl_list = list( (Table 'a nil)`

> > `Table( 'b nil)`

> > `Table( 'c nil))`

`setSG( tbl_list 41 'x)`

`=> '(41 41 41)`

`getSG( tbl_list 'x)`

=> '(41 41 41)

### getq

`getq( sl_id S_name ) => g_result | nilsl_id->S_name => g_result | nil`

#### Description

Returns the value of a property in a property list. Same as`get` except that the second argument is not evaluated. This is a syntax form.

`getq` corresponds to `->` as an LHS infix operator. So, `obj->prop` is equivalent to `getq(obj``prop).`For more information, see [Appendix B, "Mapping Symbols to Values"](appB.html#1008199 "Mapping Symbols to Values")

Used in conjunction with`putprop`, where `putprop` stores the property and `getq` retrieves it.

#### Arguments

|  |
| --- | ---
| `sl_id` | Symbol or disembodied property list.
|  |
| --- | ---
| `S_name` | Name of the property you want the value of.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of`S_name` in the `sl_id` property list.
|  |
| --- | ---
| `nil` | The named property does not exist.
#### Example

`putprop( 'chip 8 'pins ) => 8`

Assigns the property pins to a value of 8 to the symbol chip.

```
getq( 'chip pins )           => 8chip.pins                    => 8chip1 = list(nil 'pins 10)   => (nil pins 10)chip1->pins                  => 10
```

#### Reference

`get, getqq, plist, putprop`

### getqq

`getqq( s_id S_name ) => g_result | nilsl_id.S_name => g_result | nil`

#### Description

Returns the value of a property in a symbol's property list. Same as `get` except that neither argument is evaluated. This is a syntax form.

`getqq` corresponds to `.` as an LHS infix operator. So, `obj.prop` is equivalent to `getqq(obj``prop)`. For more information, see [Appendix B, "Mapping Symbols to Values"](appB.html#1008199 "Mapping Symbols to Values").

Used in conjunction with`putprop`, where `putprop` stores the property and `getqq` retrieves it.

#### Arguments

|  |
| --- | ---
| `s_id` | Symbol to get a property from.
|  |
| --- | ---
| `S_name` | Name of the property you want the value of.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value ofthe property `S_name` in the property list of `s_id`.
|  |
| --- | ---
| `nil` | The named property does not exist.
#### Example

`putprop( 'chip 8 'pins ) => 8`

Assigns the property pins to a value of 8 to the symbol chip.

`getqq( chip pins ) => 8chip.pins => 8`

#### Reference

`get, getq, plist, putprop`

### importSkillVar

`importSkillVar( s_variable ... ) => nil`

#### Description

(SKILL++ mode) Tells the compiler that the given variable names should be treated as SKILLglobal variables in SKILL++ code.

All global SKILL functions are automatically accessible from SKILL++ code, but not the SKILLvariables. This form tells the compiler that the given variable names should be treated as SKILL global variables in SKILL++ code.

This function has no effect if there is already a SKILL++ global variable of the same namedefined. Also remember that local variables can use the same name and always take precedence.

**Note:** This only means that the variables will be accessed as SKILL globals,*NOT* that they will follow SKILL's dynamic scope rule in SKILL++ code.

#### Arguments

|  |
| --- | ---
| `s_variable` | Variable to be treated as SKILL global variables in SKILL++code.
#### Value Returned

|  |
| --- | ---
| `nil` | Always returns`nil`. This function is for side-effect only.
#### Example

```
> q = 1=> 1> toplevel 'ilsILS-<2> q*Error* eval: unbound variable - qILS-<2> importSkillVar( q )=> 1ILS-<2> q=> 1
```

This example shows assigning a value to the global variable`q` in SKILL mode and then importing the variable into SKILL++.

### integerp

`integerp( g_obj ) => t | nil`

#### Description

Checks if an object is an integer. This function is the same as`fixp`.

#### Arguments

|  |
| --- | ---
| `g_obj` | Any SKILL object.
#### Value Returned

|  |
| --- | ---
| `t` | The given object is an integer.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`(integerp 123) => t(integerp "123") => nil`

#### Reference

[fixp](arithmetic.html#1039304 "Arithmetic Functions")

### \_<name>

`_<name>( ... ) => r_defstruct`

#### Description

Creates an instance of a`defstruct` specified by <`name`>.

#### Arguments

|  |
| --- | ---
| `...` | Initial values for structure elements (slots).
#### Value Returned

|  |
| --- | ---
| `r_defstruct` | Copy of the given instance
#### Example

```
defstruct(myStruct a b c) => tm1 = _myStruct(?a 3 ?b 2 ?c 1) => array[5]:3436504m2 = copy_myStruct(m1) => array[5]:3436168
```

#### Reference

`copy_<name>, copyDefstructDeep, printstruct`

### otherp

`otherp( g_value ) => t | nil`

#### Description

Checks if an object is a user type object, such as an association table or a window.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A data object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is a user type object.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

otherp(3.0)                        => nil
otherp( makeTable("table1" nil))   => t

### plist

`plist( s_symbolName ) => l_propertyList | nil`

#### Description

Returns the property list associated with a symbol.

From time to time, it is useful to print out the entire property list attached to a given symboland see what properties have been assigned to the symbol.

#### Arguments

|  |
| --- | ---
| `s_symbolName` | Name of the symbol.
#### Value Returned

|  |
| --- | ---
| `l_propertyList` | Property list for the named symbol.
|  |
| --- | ---
| `nil` | If there is no property list for the named symbol.
#### Example

`a.x = 10a.y = 20println(plist('a)) (y 20 x 10)=> nil`

Prints the property list attached to the symbol`a`. Returns `nil`, the result of `println`. Notice that a single quote is used in this example. You can think of this as passing in the name of the symbol rather than its value.

#### Reference

`putprop, setplist`

### popf

`popf( g_place) => g_result`

#### Description

A pop that uses the`setf` function. It returns the value for `g_place` that is removed.

#### Arguments

|  |
| --- | ---
| `g_place` | Place to be modified.
#### Value Returned

|  |
| --- | ---
| `g_result` | The value for`g_place` that is removed.
#### Example

`a = '((4 1) 2 3)`

`popf(car(a) )`

`=> 4`

`a == '((1) 2 3)`

#### References

[setf](#setf "Data Operator Functions"), [pushf](#pushf "Data Operator Functions")

### postArrayDec

`postArrayDec( g_array g_index ) => n_oldValue`

#### Description

Takes an array or an associated table element with an index`g_index`, decrements its value by one, stores the new value back into the array, and returns the original value. Prefix form of `s--.`

If the associated table element is not a number or`g_index` is not valid, it returns an error.

#### Arguments

|  |
| --- | ---
| `g_array` | An array or an associated table.
|  |
| --- | ---
| `g_index` | An index in the array or an associated table.
#### Value Returned

|  |
| --- | ---
| `n_oldValue` | Original value of the element.
#### Example

```
a = vector(1 2 34)array@0x8382028postArrayDec(a 2)=> 34 postArrayDec(a -4) *Error* setarray: array index out of bounds - postArrayDec(a -4)
```

#### Reference

`postArrayInc, postArraySet, postArrayDec, preArrayInc, preArraySet`

### postArrayInc

`postArrayInc( g_array g_index ) => n_oldValue`

#### Description

Takes an array or an associated table element with an index`g_index`, increments its value by one, stores the new value back into the array, and returns the original value. Prefix form of `s++.`

If the associated table element is not a number or`g_index` is not valid, it returns an error.

#### Arguments

|  |
| --- | ---
| `g_array` | An array or an associated table.
|  |
| --- | ---
| `g_index` | An index in the array or an associated table.
#### Value Returned

|  |
| --- | ---
| `n_oldValue` | Original value of the element.
#### Example

```
a = vector(1 2 34)array@0x8382028postArrayInc(a 2)=> 34 a[2]=> 35 postArrayInc(a -4) *Error* setarray: array index out of bounds - postArrayInc(a -4)
```

#### Reference

`postArrayDec, postArraySet, preArrayDec, preArrayInc, preArraySet`

### postArraySet

`postArraySet( g_array g_index n_modifier ) => n_oldValue`

#### Description

Takes an array or an associated table element with an index`g_index`, adds an n\_modifier value to its original value, stores the new value back into the array, and returns the original value.

If the associated table element is not a number or`g_index` is not valid, it returns an error.

#### Arguments

|  |
| --- | ---
| `g_array` | An array or an associated table.
|  |
| --- | ---
| `g_index` | An index in the array or an associated table.
|  |
| --- | ---
| `n_modifier` | Value that should be added to the element.
#### Value Returned

|  |
| --- | ---
| `n_oldValue` | Original value of the element.
#### Example

```
a = vector(1 2 34) array@0x8382028 postArraySet(a 2 3) => 34 postArraySet(a -4 9) *Error* setarray: array index out of bounds - postArraySet(a -4 9)
```

#### Reference

`postArrayDec, postArrayInc, preArrayDec, preArrayInc, preArraySet`

### postdecrement

`postdecrement( s_var ) => n_result`

#### Description

Takes a variable, decrements its value by one, stores the new value back into the variable,and returns the original value. Prefix form of `s--`. The name of the variable must be a symbol and the value must be a number.

#### Arguments

|  |
| --- | ---
| `s_var` | Variable representing a number.
#### Value Returned

|  |
| --- | ---
| `n_result` | Original value of the variable.
#### Example

`s = 2postdecrement( s ) => 2s => 1`

`s = 2.2postdecrement( s ) => 2.2s => 1.2`

#### Reference

`postincrement, predecrement, preincrement`

### postincrement

`postincrement( s_var ) => n_result`

#### Description

Takes a variable, increments its value by one, stores the new value back into the variable, andreturns the original value. Prefix form of `s++`. The name of the variable must be a symbol and the value must be a number.

#### Arguments

|  |
| --- | ---
| `s_var` | Variable representing a number.
#### Value Returned

|  |
| --- | ---
| `n_result` | Original value of the variable.
#### Example

`s = 2postincrement( s ) => 2s => 3`

`s = 2.2postincrement( s ) => 2.2s => 3.2`

#### Reference

`postdecrement, predecrement, preincrement`

### preArrayDec

`preArrayDec( g_array g_index ) => n_newValue`

#### Description

Takes an array or an associated table element with an index`g_index`, decrements its value by one, stores the new value back into the array, and returns the updated value. Prefix form of `--s`.

If the associated table element is not a number or`g_index` is not valid, it returns an error.

#### Arguments

|  |
| --- | ---
| `g_array` | An array or an associated table.
|  |
| --- | ---
| `g_index` | An index in the array or an associated table.
#### Value Returned

|  |
| --- | ---
| `n_newValue` | New value of the element.
#### Example

```
a = vector(1 2 34)array@0x8382028preArrayDec(a 2)=> 33 preArrayDec(a -4) *Error* setarray: array index out of bounds - preArrayDec(a -4)
```

#### Reference

`postdecrement, predecrement, preincrement`

### preArrayInc

`preArrayInc( g_array g_index ) => n_newValue`

#### Description

Takes an array or an associated table element with an index`g_index`, increments its value by one, stores the new value back into the array, and returns the updated value. Prefix form of `++s`.

If the associated table element is not a number or`g_index` is not valid, it returns an error.

#### Arguments

|  |
| --- | ---
| `g_array` | An array or an associated table.
|  |
| --- | ---
| `g_index` | An index in the array or an associated table.
#### Value Returned

|  |
| --- | ---
| `n_newValue` | New value of the element.
#### Example

```
a = vector(1 2 34)array@0x8382028preArrayInc(a 2)=> 35 preArrayInc(a -4) *Error* setarray: array index out of bounds - preArrayInc(a -4)
```

#### Reference

`postdecrement, predecrement, preincrement`

### preArraySet

`preArraySet( g_array g_index n_modifier ) => n_newValue`

#### Description

Takes array or an associated table element with an index`g_index`, adds an n\_modifier value to its original value, stores the new value back into the array, and returns the updated value.

If the associated table element is not a number or`g_index` is not valid, it returns an error.

#### Arguments

|  |
| --- | ---
| `g_array` | An array or an associated table.
|  |
| --- | ---
| `g_index` | An index in the array or an associated table.
|  |
| --- | ---
| `n_modifier` | The value that should be added to the element.
#### Value Returned

|  |
| --- | ---
| `n_newValue` | New value of the element i.e, (g\_array [`g_index`] + `n_modifier`)
#### Example

```
a = vector(1 2 34)array@0x8382028preArraySet(a 2 3)=> 37 preArraySet(a -4 9) *Error* setarray: array index out of bounds - preArraySet(a -4 9)
```

#### Reference

`postdecrement, predecrement, preincrement`

### predecrement

`predecrement( s_var ) => n_result`

#### Description

Takes a variable, decrements its value by one, stores the new value back into the variable,and returns the new value. Prefix form of `--s`. The name of the variable must be a symbol and the value must be a number.

#### Arguments

|  |
| --- | ---
| `s_var` | Variable representing a number.
#### Value Returned

|  |
| --- | ---
| `n_result` | Decremented value of the variable.
#### Example

`s = 2predecrement( s ) => 1s => 1`

`s = 2.2predecrement( s ) => 1.2s => 1.2`

#### Reference

`postdecrement, predecrement, preincrement`

### preincrement

`preincrement( s_var ) => n_result`

#### Description

Takes a variable, increments its value by one, stores the new value back into the variable, andreturns the new value. Prefix form of `++s`. The name of the variable must be a symbol and the value must be a number.

#### Arguments

|  |
| --- | ---
| `s_var` | Variable representing a number.
#### Value Returned

|  |
| --- | ---
| `n_result` | Incremented value of the variable.
#### Example

`s = 2preincrement( s ) => 3s => 3`

`s = 2.2preincrement( s ) => 3.2s => 3.2`

#### Reference

[postdecrement](#1039920 "Data Operator Functions"), [predecrement](#1040121 "Data Operator Functions")

### pushf

`pushf( g_objg_place) => g_newPlaceValue`

#### Description

A push that uses the`setf` function. It modifies the contents of the original storage location.

#### Arguments

|  |
| --- | ---
| `g_obj` | New value to be pushed.
|  |
| --- | ---
| `g_place` | Place to be modified with the new value.
#### Value Returned

|  |
| --- | ---
| `g_newPlaceValue` | New value.
#### Example

`a = list((list 1) 2 3)`

`pushf(4 (car a))`

`=> a == '((4 1) 2 3)`

#### References

[setf](#setf "Data Operator Functions"), [popf](#popf "Data Operator Functions")

### putprop

`putprop( sl_id g_value S_name ) => g_value`

#### Description

Adds properties to symbols or disembodied property lists.

If the property already exists, the old value is replaced with a new one. The`putprop` function is a `lambda` function, which means all of its arguments are evaluated. However, `putprop` has no infix operator syntax.

#### Arguments

|  |
| --- | ---
| `sl_id` | Symbol or disembodied property list.
|  |
| --- | ---
| `g_value` | Value of the named property.
|  |
| --- | ---
| `S_name` | Name of the property.
#### Value Returned

|  |
| --- | ---
| `g_value` | The value of the named property.
#### Example

`putprop('s 1+2 'x) => 3`

Sets the property`x` on symbol `s` to 3.

#### Reference

`get, putpropq, putpropqq`

### putpropq

`putpropq( sl_id g_value S_name ) => g_valuesl_id->S_name = g_value => g_value`

#### Description

Adds properties to symbols or disembodied property lists.Identical to `putprop` except that `S_name` is not evaluated. If the property already exists, the old value is replaced with a new one.

`putpropq` corresponds to `-> =` as an assignment operator. So, `obj->prop = value` is equivalent to `putpropq(obj value prop)`. For more information, see [Appendix B, "Mapping Symbols to Values"](appB.html#1008199 "Mapping Symbols to Values").

#### Arguments

|  |
| --- | ---
| `sl_id` | Symbol or disembodied property list.
|  |
| --- | ---
| `g_value` | Value of the named property.
|  |
| --- | ---
| `S_name` | Name of the property.
#### Value Returned

|  |
| --- | ---
| `g_value` | Value of the named property.
#### Example

`putpropq('s 1+2 x)    => 3y = 'x                => xy->x = 1+2            => 3`

Both examples are equivalent expressions that set the property`x` on symbol `s` to 3.

#### Reference

`get, putprop, putpropqq`

### putpropqq

`putpropqq( s_id g_value S_name ) => g_values_id.S_name = g_value => g_value`

#### Description

Adds properties to symbols.Identical to `putprop` except that `sl_id` and `S_name` are not evaluated. If the property already exists, the old value is replaced with a new one.

`putpropqq` corresponds to `. =`as an assignment operator. So, `obj.prop = value` is equivalent to `putpropqq(obj value prop)`. For more information, see [Appendix B, "Mapping Symbols to Values"](appB.html#1008199 "Mapping Symbols to Values").

#### Arguments

|  |
| --- | ---
| `s_id` | Can only be a symbol.
|  |
| --- | ---
| `g_value` | Value of the named property.
|  |
| --- | ---
| `S_name` | Name of the property.
#### Value Returned

|  |
| --- | ---
| `g_value` | Value of the named property.
#### Example

`putpropqq(s 1+2 x)    => 3s.x = 1+2             => 3`

Both examples are equivalent expressions that set the property`x` on symbol `s` to 3.

#### Reference

[get](#1038893 "Data Operator Functions"), [putprop](#1040238 "Data Operator Functions"), [putpropq](#1040267 "Data Operator Functions")

### quote

`quote( g_expr ) => g_result`

#### Description

Returns the name of the variable or the expression. Prefix form of the`'` operator. Quoting is used to prevent expressions from being evaluated.

#### Arguments

|  |
| --- | ---
| `g_expr` | Variable or expression.
#### Value Returned

|  |
| --- | ---
| `g_result` | Name of the variable or expression.
#### Example

(quote a)       => a
(quote (f a b)) => (f a b)

### remprop

`remprop( sl_id S_name ) => l_result | nil`

#### Description

Removes a property from a property list and returns the property's former value.

#### Arguments

|  |
| --- | ---
| `sl_id` | Symbol or disembodied property list.
|  |
| --- | ---
| `S_name` | Property name.
#### Value Returned

|  |
| --- | ---
| `l_result` | Former value of the property as a single element list.
|  |
| --- | ---
| `nil` | The property does not exist.
#### Example

`putprop( 'chip 8 'pins ) => 8`

Assigns the property pins to`chip`.

`get( 'chip 'pins ) => 8remprop( 'chip 'pins ) => (8)`

Removes the property pins from`chip`.

`get( 'chip 'pins) => nil`

#### Reference

[get](#1038893 "Data Operator Functions"), [putprop](#1040238 "Data Operator Functions")

### rotatef

`rotatef( [ gplace1 ][ gplace2 ].....[ gplacen ]) => g_newPlaceValues`

#### Description

Modifies the value of each place by rotating the values from one place to another in a cyclicorder.

#### Arguments

|  |
| --- | ---
| `gplace1...gplacen` | Values to be rotated.
#### Value Returned

|  |
| --- | ---
| `g_newPlaceValues` | New values.
#### Example

`a=1 b=2 c=3`

`rotatef(a b c)`

`=> a=b b=c c=a,`

Now,

`a=2 b=3 c=1`

### set

`set( s_variableName g_newValue [ e_environment ]) => g_result`

#### Description

Sets a variable to a new value. Similar to`setq` but the first argument for `set` is evaluated.

The`set` function is similar to the `setq` function, but unlike `setq`, the first argument for `set` is evaluated. This argument must evaluate to a symbol, whose value is then set to `g_newValue`.

#### Arguments

|  |
| --- | ---
| `s_variableName` | Symbol that is evaluated.
|  |
| --- | ---
| `g_newValue` | Value to set symbol to.
|  |
| --- | ---
| `e_environment` | If this argument is given, SKILL++ semantics is assumed. Theforms entered will be evaluated within the given (lexical) environment.
#### Value Returned

|  |
| --- | ---
| `g_result` | Returns`g_newValue`.
#### Example

```
y = 'a  => a    ; Sets y to the constant a.set (y 5) => 5    ; Sets the value of y to 5.y       => a a       => 5
```

#### Reference

`setq`

### setf

`setf( g_place g_value ) => g_result`

#### Description

Assigns a new value to an existing storage location, destroying the value that was previouslyin that location. The `setf`function uses special expander functions:defined as `setf_<helper>`. For a list of the helper functions, see [setf Helper Functions](appC.html#1008199 "setf Helper Functions").

#### Arguments

|  |
| --- | ---
| `g_place` | Specifies the storage location
|  |
| --- | ---
| `g_value` | Specifies the new value
#### Value Returned

|  |
| --- | ---
| `g_result` | Returns the updated result
#### Example

`x = '(a b c d e)setf( (car x) 42);; here x changes to (42 b c d e)`

`=>(42 b c d e)`

#### References

[pushf](#pushf "Data Operator Functions"), [popf](#popf "Data Operator Functions")

### setf\_`<helper>`

`setf_<helper>( g_new[ g_cell ]) => g_result`

#### Description

An expander function for`setf`, which returns the result of the corresponding `setf` operation. In the function, replace `helper` with the expander name. For a list of the helper functions, see [setf Helper Functions](appC.html#1008199 "setf Helper Functions").

#### Arguments

|  |
| --- | ---
| `g_new` | New value to be set for`g_cell`.
|  |
| --- | ---
| `g_cell` | Cell to be modified.
#### Value Returned

|  |
| --- | ---
| `g_result` | Result of the corresponding`setf` operation.
#### Example

The following is an example of the helper function for`getSkillPath`:

`defun(setf_getSkillPath (new)`

`if(listp(new)`

`setSkillPath(new)`

`setSkillPath(list(new)))) ; alters the skill path with setf`

```
setf(getSkillPath()   "/home/user/temp")  ; now skill path changed to "/home/user/temp"
```

### setguard

`setguard( ( s_symbol ) g_guard ) => u_guard`

#### Description

Mainly enforces disciplined use of a symbol as a global variable by associating it with aguarding function that is either a symbol that identifies the name of the guarding function or a lambda form (just like the first argument to the `apply` function). If the guarding function is `nil`, the symbol is unguarded. The guarding function is called with two arguments whenever a new value is assigned to the symbol: the symbol and the value to be assigned to it. The result of the guarding function determines the `setguard` return value that gets assigned to the symbol.

**Note:** The guarding function associated with a guarded symbol is triggered whenever a newvalue is assigned to that symbol by way of the `setq` (or `set`) function. Neither a lambda binding nor a let binding will cause the guarding function to be called (see examples below).

#### Arguments

|  |
| --- | ---
| `s_symbol` | Symbol to be associated with the guarding function.
|  |
| --- | ---
| `g_guard` | Guarding function to be associated with the symbol.
#### Value Returned

|  |
| --- | ---
| `u_guard` | Either a symbol that identifies the name of the guarding functionor a function object.
#### Example

```
> procedure( myPortGuard(varName newValue)        if( portp(newValue)        then            newValue        else            printf("Only port values can be assigned to `%s'\n" varName)            symeval(varName)        )  )myPortGuard
```

`> setguard('poport 'myPortGuard)myPortGuard`

`` > poport = nilOnly port values can be assigned to `poport'port:"*stdout*" ``

`` > poport = 123Only port values can be assigned to `poport'port:"*stdout*" ``

```
> setguard( 'myStringVar        lambda((varName newValue)            if(stringp(newValue)            then                newValue            else                printf("Only strings can be assigned to `%s'\n" varName)                symeval(varName)            )        ) ; lambda  ) ; setguard
```

`> myStringVar = "default""default"`

`` > myStringVar = 123Only strings can be assigned to `myStringVar'"default" ``

`` > myStringVar = nilOnly strings can be assigned to `myStringVar'"default" ``

```
;; A lambda binding will not trigger the guard> ((lambda (myStringVar) (println 'hello)) nil)hellonil
```

```
;; A let binding will also not trigger the guard> let( ((myStringVar 123))        println(myStringVar)  )123nil
```

`` ;; This s the symbol `myStringVar' unguarded> setguard('myStringVar nil)nil ``

`> myStringVar = 123123`

#### Reference

`apply, lambda, let, set, setq`

### setplist

`setplist( s_atom l_plist ) => l_plist`

#### Description

Sets the property list of an object to a new property list; the old property list attached to theobject is lost.

* ***Users are strongly discouraged from using setplist because it mightremove vital properties being used by the system or other applications.***

#### Arguments

|  |
| --- | ---
| `s_atom` | A symbol.
|  |
| --- | ---
| `l_plist` | New property list to attach to`s_atom`.
#### Value Returned

|  |
| --- | ---
| `l_plist` | New property list for`s_atom`; the old property list is lost.
#### Example

```
setplist( 'chip '(pins 8 power 5) )    => (pins 8 power 5)plist( 'chip )                         => (pins 8 power 5)chip.power                             => 5
```

#### Reference

[getq](#1038956 "Data Operator Functions"), [getqq](#1038989 "Data Operator Functions"), [plist](#1039739 "Data Operator Functions"), [putpropq](#1040267 "Data Operator Functions"), [putpropqq](#1040295 "Data Operator Functions"), [remprop](#1040408 "Data Operator Functions")

### setq

```
setq( s_variableName g_newValueExp ) => g_resultsetq( s_variableName = g_newValue ) => g_result
```

#### Description

Sets a variable to a new value.`setq` is the same as the assignment (=) operator. This is a syntax form.

The symbol`s_variableName` is bound to the value of `g_newValueExp`. Note that the first argument to `setq` is not evaluated but the second one is.

#### Arguments

|  |
| --- | ---
| `s_variableName` | Variable to be bound.
|  |
| --- | ---
| `g_newValueExp` | Expression to be evaluated and bound to`s_variableName`.
#### Value Returned

|  |
| --- | ---
| `g_result` | Evaluated result of`g_newValueExp` is returned.
#### Example

`x = 5         => 5`

Assigns the value`5` to the variable `x`.

`setq( x 5 )   => 5`

Assigns the value`5` to the variable `x`.

`y = 'a        => a`

Assigns the symbol`a` to the variable `y`.

#### Reference

[set](#1040473 "Data Operator Functions")

### setSG

`setSG(g_objS_propg_value)=>g_propValue`

#### Description

Evaluates and then sets the value for the specified attribute or property. It is a lambdaimplementation of `setSGq()`.

#### Arguments

|  |
| --- | ---
| `g_obj` | Specifies the name of an object
| `S_prop` | Specifies the name of the attribute or property for which youwant to set the value
| g\_value | Specifies the value you want to set
#### Value Returned

|  |
| --- | ---
| `g_propValue` | The set value of the property
#### Example

In the following example,`setSG()` evaluates the `tbl_list` argument and then sets its value.

`tbl_list = list( (Table 'a nil)`

> > `Table( 'b nil)`

> > `Table( 'c nil))`

`setSG( tbl_list 41 'x)`

=> '(41 41 41)

### symbolp

`symbolp( g_value ) => t | nil`

#### Description

Checks if an object is a symbol.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A data object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is a symbol.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

```
symbolp( 'foo)            => tsymbolp( "foo")           => nilsymbolp( concat("foo"))   => t
```

#### Reference

[concat](#1038735 "Data Operator Functions"), [stringp](stringfunc.html#1040671 "String Functions")

### symeval

`symeval( s_symbol [ e_environment ] ) => g_result`

#### Description

Returns the value of the named variable.

`symeval` is slightly more efficient than `eval` and can be used in place of `eval` when you are sure that the argument being evaluated is indeed a variable name.

#### Arguments

|  |
| --- | ---
| `s_symbol` | Name of the variable.
|  |
| --- | ---
| `e_environment` | If this argument is given, SKILL++ semantics is assumed. Thevariable name will be looked up within the given (lexical) environment.
#### Value Returned

|  |
| --- | ---
| `g_result` | Value of thenamed variable.
#### Example

`x = 5symeval( 'x ) => 5`

`symeval( 'y ) => unbound    ;Assumes y is unbound.`

#### Reference

[eval](funcprog.html#1039816 "Function and Program Structure")

### symstrp

`symstrp( g_value ) => t | nil`

#### Description

Checks if an object is either a symbol or a string.

The suffix`p` is usually added to the name of a function to indicate that it is a predicate function.

#### Arguments

|  |
| --- | ---
| `g_value` | A data object.
#### Value Returned

|  |
| --- | ---
| `t` | If`g_value` is either a symbol or a string.
|  |
| --- | ---
| `nil` | Otherwise.
#### Example

`symstrp( "foo" )    => tsymstrp( 'foo )     => tsymstrp( 3 )        => nil`

#### Reference

[stringp](stringfunc.html#1040671 "String Functions"), [symbolp](#1040737 "Data Operator Functions")




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
