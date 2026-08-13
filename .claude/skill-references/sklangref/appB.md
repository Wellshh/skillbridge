### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

B
=

Mapping Symbols to Values
=========================

There are many objects in SKILL which map symbols to values. The`get` function tries to work for all of them. Of course this over-intelligence causes confusion in cases such as hash tables.

#### Reader-Writer Correspondence

The functions come in reader/writer pairs as given below. The functions (`get`, `getq`, `getqq`) in the left-hand column, read from a given object. The functions (`putprop`, `putpropq`, `putpropqq`) in the right-hand column, write to (or modify) a given object.

`get <--> putprop`

`getq <--> putpropq`

`getqq <--> putpropqq`

#### Using the Infix Operator

The`get` and `putprop` functions have no corresponding infix operators. The infix operators for the other four functions are as given in the following table:

|  |  |  |  |
| --- | --- | --- | --- | ---
|  |  |  | Examples |
| Function | InfixOperator | LHS orRHS | Function Call | Infix Operator
| `getq` | `->` | LHS | `getq(obj prop)` | `obj->prop`
| putpropq | `-> =` | RHS | `putpropq(obj value``prop)` | `obj->prop =``value`
| getqq | `.` | LHS | `getqq(obj prop)` | `obj.prop`
| putpropqq | `.=` | RHS | `putpropqq(obj value``prop)` | `obj.prop = value`
#### Evaluating Arguments

The functions differ about which of their arguments are taken as literals or are evaluated. Thefollowing table describes the arguments that are evaluated for each of the four functions:

|  |  |
| --- | --- | ---
| Function CallUsing Infix Operator | Function Call Using theSyntax | Arguments Evaluated
| - | get(obj prop) | obj, prop
| - | putprop(obj value prop) | obj, value, prop
| obj->prop | getq(obj prop) | obj
| obj->prop=value | putpropq(obj valueprop) | obj, value
| obj.prop | getqq(obj prop) |
| obj.prop=value | putpropqq(obj valueprop) | value
The following are equivalent:

`getq(obj prop) <--> get(obj 'prop)`

`getqq(obj prop) <--> get('obj 'prop) <--> getq('obj prop)`

`putpropq(obj value prop) <--> putprop(obj value 'prop)`

`putpropqq(obj value prop) <--> putprop('obj value 'prop) <-->``putpropq('obj value prop)`

Except for the quoting semantics, all the functions behave the same. They retrieve the valueassociated with a symbol in a specified object. If a string is given rather than a symbol as the property name, the effect is as if the function were called with the symbol that has the print-name.

The following are equivalent:

`get(obj 'prop) <--> get(obj "prop")`

`getq(obj prop) <--> getq(obj "prop")`

`getqq(obj prop) <--> getqq(obj "prop")`

`putprop(obj value 'prop) <--> putprop(obj value "prop")`

`putpropq(obj value prop) <--> putpropq(obj value "prop")`

`putpropqq(obj value prop) <--> putpropqq(obj value "prop")`

#### Working with Lists

If the given object is a list,`get`, `getq`, `putprop`, and `putpropq` assume it is a DPL and consequently read or modify the named field of the DPL.

#### Working with Symbols

If the given object is a symbol,`get`, `getq`, `putprop`, and `putpropq` read or modify the symbol's property list.

#### Working with Hash Tables

For the cases of hash tables (returned by`Instance`) the functions arrayref and setarray can be used instead. There are also`[]` and `[]=` infix operators which obey the following equivalence:

`hash->prop`

`hash['prop]`

`getq(hash prop)`

`get(hash 'prop)`

`get(hash "prop")`

`getq(hash "prop")`

`arrayref(hash 'prop)`

And, the following are equivalent:

`hash->prop = value`

`hash['prop] = value`

`putpropq(hash value prop)`

`putpropq(hash value "prop")`

`putprop(hash value 'prop)`

`putprop(hash value "prop")`

`setarray(hash 'prop value)`

#### Working with SKILL++

For the cases of SKILL++ instances of`standardObject` (returned by `Table`), the functions `slotValue` and `setSlotValue` can be used in accordance to the equivalence sets specified below.

The following are equivalent:

`self->slot`

`getq(self slot)`

`get(self 'slot)`

`slotValue(self 'slot)`

And, the following are equivalent:

`self->slot = value`

`putprop(self value 'slot)`

`putprop(self value "slot")`

`putpropq(self value slot)`

`putpropq(self value "slot")`

`setSlotValue(self 'slot value)`

In addition to the uses described above, applications that embed SKILL (such as Virtuoso andAllegroPCB) extend the capabilities of the `get` and `putprop` family of functions to work intuitively on their data structures, these include hi forms, menus and widgets, dbobjects, CDF objects, waveform objects, and many other types of objects.




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
