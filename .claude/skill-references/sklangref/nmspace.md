### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

15
==

Namespace Functions
===================

### makeNamespace

`makeNamespace( t_name ) => o_namespace / nil`

#### Description

Creates a SKILL namespace with the given`t_name`. A namespace or its parts can be saved in a context and loaded with the context.

#### Arguments

|  |
| --- | ---
| `t_name` | Name for the namespace.
#### Value Returned

|  |
| --- | ---
| `o_namespace` | Returns the namespace object when successfully created.
| nil | Returns nil if the namespace is not created or a namespacewith the same name already exists.
#### Example

`makeNamespace("METHODS")`

`=> ns@METHODS`

### findNamespace

`findNamespace( t_name ) => o_namespace / nil`

#### Description

Returns the namespace object with the given name.

#### Arguments

|  |
| --- | ---
| `t_name` | Specify the name for which you want retrieve the namespaceobject.
#### Value Returned

|  |
| --- | ---
| `o_namespace` | Returns the namespace object.
| nil | Returns nil if no namespace object exists with the given name.
#### Example

`findNamespace("A")`

`=> ns@A`

### useNamespace

`useNamespace(t_namespace) => t / nil`

#### Description

Sets the given namespace for use and imports its symbols into the current namespace.

#### Arguments

|  |
| --- | ---
| `t_namespace` | Specify the name of the namespace that you want to use.
#### Value Returned

|  |
| --- | ---
| t | Returns t when the given namespace is successfully set foruse.
| nil | Returns nil if the given namespace is not set.
#### Example

`useNamespace("METHODS")`

`=> t`

### unuseNamespace

`unuseNamespace(t_namespace) => t / nil`

#### Description

Unsets the given namespace.

#### Arguments

|  |
| --- | ---
| `t_namespace` | Specify the name of the namespace that you want to unset.
#### Value Returned

|  |
| --- | ---
| t | Returns t when the given namespace is successfully unset foruse.
| nil | Returns nil if the given namespace cannot be unset.
#### Example

`unuseNamespace("METHODS")`

`=> t`

### importSymbol

`importSymbol(l_symbolList[t_namespace])=> t / nil`

#### Description

Imports symbols into the given namespace. By default, this function imports into the`IL`(or default)namespace.

#### Arguments

|  |
| --- | ---
| `l_symbolList` | Specify a list of symbols that you want to import into the defaultnamespace
| `t_namespace` | (Optional). Specifies the name of the namespace into whichyou want to import the given symbols.
#### Value Returned

|  |
| --- | ---
| t | Returns t if the symbols are successfully imported into thenamespace (given or default).
#### Example

importSymbol('(A::level A::value))

=> t

### findSymbol

`findSymbol(t_name[?namespace t_namespace])=> s_symbolName / nil`

#### Description

Searches for a symbol that is specified as a string in the given namespace and returns itscorresponding SKILL symbol.

#### Arguments

|  |
| --- | ---
| `t_name` | A string value to specify the name of the symbol you want tosearch for.
| `t_namespace` | (Optional) The namespace in which you want to search for thesymbol.
#### Value Returned

|  |
| --- | ---
| `s_symbolName` | Returns the name of the symbol.
| nil | Returns nil if no such symbol exists in the namespace.
#### Example

`> (Namespace "my")`

`ns@my`

`> 'my:::aaa`

`my:::aaa`

`> (findSymbol "aaa" ?namespace "my")`

`my:::aaa`

`> (findSymbol "bbb" ?namespace "my")`

`nil`

### addToExportList

`addToExportList(l_symbols) => t`

#### Description

Adds the specified symbols to the namespace export list. This function does not throw anyerrors if a symbol is already exported.

**Note:** You can export any symbol from your namespace.

#### Arguments

|  |
| --- | ---
| `l_symbols` | Specify the symbols that you want to add to the namespaceexport list.
#### Value Returned

|  |
| --- | ---
| t | Returns t when the specified symbols are successfully added tothe namespace export list.
#### Example

`> (addToExportList '(newNameSpace:::aaa newNameSpace:::bbb))`

`t`

`> (useNamespace "newNameSpace")`

`t`

`> (getSymbolNamespace 'aaa)`

`ns@newNameSpace`

### getSymbolNamespace

`getSymbolNamespace(s_name)=> o_namespace`

#### Description

Returns the namespace where the symbol was created.

#### Arguments

|  |
| --- | ---
| `s_name` | Specifies the name of the symbol for which you want to retrievethe namespace where the symbol was created
#### Values Returned

|  |
| --- | ---
| `o_namespace` | Returns the namespace where the specified symbol wascreated.
#### Example

`getSymbolNamespace('car)`

`=> ns@IL`

### removeFromExportList

`removeFromExportList(l_symbolList)=> t`

#### Description

Removes symbols referenced in`l_symbolList` from the export list of its namespace. This function will not throw an error, if some of the symbols are not exported. If a symbol from `l_symbolList` was imported by `useNamespace` it will not removed by `unuseNamespace`.

#### Arguments

|  |
| --- | ---
| `l_symbolList` | Specifies the symbols that you want to remove from the exportlist of your namespace.
#### Value Returned

|  |
| --- | ---
| t | Returns t when the referenced symbols are successfullyremoved.
#### Example

`> (removeFromExportList '(jane::aaa))`

`t`

`> (useNamespace "jane")`

`t`

`> (getSymbolNamespace 'aaa)`

`nil`

### addToNamespace

`addToNamespace(t_namespaceNamel_symbolList) => t`

#### Description

Adds and imports the given list of symbol names to the export list of the namespace`t_namespaceName`.

#### Arguments

|  |
| --- | ---
| t\_namespaceName | Specify the name of the namespace to which you want to addthe given list of symbols.
| `l_symbolList` | Specifies the symbols that you want to add to the export list ofthe specified namespace.
#### Value Returned

|  |
| --- | ---
| t | Returns t when the list of symbols are successfully added.
#### Example

`> (addToNamespace "A" '("a" "b" "c"))`

`t`

`> (getSymbolNamespace 'a)`

`ns@A`

### shadow

`shadow(l_symbols[t_namespace] )=> t`

#### Description

Adds symbols`s_symbol` to the shadow list of the default namespace. The symbols which are added to the shadow list are not overridden by import.

#### Arguments

|  |
| --- | ---
| `l_symbols` | Specify a list of symbols to be protected in the defaultnamespace.
| t\_namespace | (Optional) Specify the namespace in which these symbolsshould be protected. The default value is the "`IL`" namespace.
#### Value Returned

|  |
| --- | ---
| t | Returns`t` to indicate that the symbol was added to the shadow list of the current namespace.
#### Example

`aaddToExportList('(p1:::x p1:::y p1:::z))`

`=>t`

`addToExportList('(p2:::x p2:::y p2:::z))`

`=>t`

`useNamespace("p1")`

`=>t`

`useNamespace("p2")`

`*error* useNamespace symbol name conflict - p2::x p2::y p2::z`

`unuseNamespace("p1")`

`shadow(shadow('x y z))`

`=> t`

`useNamespace("p2")`

`=>t`

### shadowImport

`shadowImport(l_symbols [t_namespace])=> t`

#### Description

Adds symbols to the namespace shadow list.

#### Arguments

|  |
| --- | ---
| `l_symbols` | Specify the list of symbols that you want to add to the shadowlist.
| `t_namespace` | (Optional) Specify the namespace of the shadow list to whichyou want to add the symbols. If you do not provide a namespace, the symbols are added to the shadow list of the default namespace,`IL`.
#### Value Returned

|  |
| --- | ---
| t | Returns t when the symbols are successfully added to thenamespace shadow list.
#### Example

shadowImport('(methods::drawPolygon))

=> t

### removeShadowImport

`shadowImport(l_symbols [t_namespace])=> t`

#### Description

Removes the specified symbols from the namespace shadow list.

#### Arguments

|  |
| --- | ---
| `l_symbols` | Specify the list of symbols that you want to remove from theshadow list.
| `t_namespace` | (Optional) Specify the namespace of the shadow list from whichyou want to remove the symbols. If you do not provide a namespace, the symbols are removed from the shadow list of the default namespace,`IL`.
#### Value Returned

|  |
| --- | ---
| t | Returns t when the symbols are successfully removed from thenamespace shadow list.
#### Example

`removeShadowImport('drawPolygon)`

`=> t`

### unimportSymbol

`unimportSymbol(l_symbolList[t_namespace])=> t`

#### Description

Unimports symbols from the given namespace. By default, this function unimports from the`IL` (or default) namespace.

#### Arguments

|  |
| --- | ---
| `l_symbolList` | Specify a list of symbols that you want to unimport from thedefault namespace.
| `t_namespace` | (Optional). Specifies the name of the namespace from whichyou want to unimport the given symbols.
#### Values Returned

|  |
| --- | ---
| t | Returns t, if successful
#### Example

`unimportSymbol('(A::level A::value))`

`=> t`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
