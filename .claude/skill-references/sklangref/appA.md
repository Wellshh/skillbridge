### Cadence SKILL Language Reference Product Version 6.1.6 November 2014

A
=

Scheme/SKILL++ Equivalents Tables
=================================

The purpose of this appendix is to help users familiar with Scheme to get a jump start withSKILL++. All of Scheme's special (syntax) forms and functions are listed along with their SKILL++ equivalents.

The tables, which are divided into expressions, lexical structure, and functions, use theseterms:

|  |
| --- | ---
| Same | Means that this Scheme functionality is provided with the samename (syntax) and same behavior in SKILL++.
| Supported | Means that this Scheme functionality is provided, but it isimplemented under a different name and/or is used somewhat differently. For example,
|  | (1) In SKILL++, the Scheme function`-vector` becomes `Vector`.
|  | (2) The global variable`piport` is used in place of the Scheme function `current-input-port`.
| Infix only | Means that the specific Scheme functionality is provided, but thegiven name can only be used as an infix operator in SKILL++. There is usually an equivalent function with a different name to which this infix operator can be mapped.
| Unsupported | Means that this Scheme functionality is not yet provided incurrent SKILL++.
See the following sections for more information:

* [Lexical Structure](#1008212 "Scheme/SKILL++ Equivalents Tables")

* [Expressions](#1010253 "Scheme/SKILL++ Equivalents Tables")

* [Functions](#1008405 "Scheme/SKILL++ Equivalents Tables")

Lexical Structure
-----------------

****Scheme/SKILL++ Equivalents Table - Lexical Structure****

| **Scheme** | **SKILL++** | **Comment**
| Boolean literals #`t`, #`f` | Supported. | Use`t` for #`t`, `nil` for #`f`.
| Character literals#`\...` | Unsupported. | Character type not supported.
| Simple numeric literalssuch as integers & floats | Supported. | Use 0..., 0x..., and 0b... for #o..., #x...,and #b... (octal/hex/binary integers).
| String literals "..." | Same. |
| Vector literals #(...) | Same. |
| case-insensitivesymbols | Unsupported. | Symbols in SKILL++ are always case-sensitive.
| `nil` as a symbol | Unsupported. | In SKILL++, just as in SKILL,`nil` is not a symbol.
| Special symbolconstituent characters such as !, $, %, &, \*, /, <, =, and so forth. | Unsupported. | Some of these are used for (infix)operators in SKILL++, others are illegal characters. `?` is used for keyword prefix.
| ' (single quote) | Same. | Shorthand for`quote`.
| ` (back quote) | Same. | Shorthand for`quasiquote` in Scheme and for `_backquote` in SKILL++.
| , (comma) | Same. | Shorthand for`unquote` in Scheme and for  `_comma` in SKILL++.
| ,@ | Same. | Shorthand for`unquote-splicing` in Scheme and for `_commaAt`in SKILL++.
Expressions
-----------

**Scheme/SKILL++ Equivalents Table - Expressions**

| **Scheme** | **SKILL++** | **Comment**
| (improper lists), such as (d ... . d) | Unsupported. | SKILL++ lists must end with`nil`.
| (procedure calls), such as (f e ...) | Same. | Can be written as`f(e ...)` in SKILL++ if `f` is a symbol (variable).
| (and e ...) | Same. |
| (begin e ...) | Same. | Equivalent to`progn` in SKILL++.
| (case ((d ...) e ...) ...[(else e ...)]) | Same. |
| (cond (e ...) ... [(else e...)]) | Same. |
| (define x e)  (define (x v ...) body) | Same. | One can also use SKILL's`procedure` syntax to define functions in SKILL++.
| (do ((v e [e]) ...) (e ...) e...) | Same. |
| (if e1 e2 e3) | Same. | SKILL++ allows extended`if` syntax (with `then` and `else` keywords) as in SKILL.
| (lambda (x ...) body) | Same. | Improper variable list such as`(x ...``. y)` can't be used as formals in SKILL++. Use SKILL style `@rest`, `@optional`instead.
| (let [x] ((v e) ...) body) | Same. |
| (let\* ((v e) ...) body) | Supported. | Use`letseq` instead of `let*` in SKILL++.
| (letrec ((v e) ...) body) | Same. |
| (or e ...) | Same. |
| (set! x e) | Supported. | Use`setq` or the infix `=` operator.
Functions
---------

**Scheme/SKILL++ Equivalents Table - Functions**

| **Scheme** | **SKILL++** | **Comment**
| +, -, \*, / | Infix only. | Equivalent to functions`plus`*,* `difference`*,* `times`*,* and `quotient` in SKILL++.
| <, <=, >, >= | Infix only. | Equivalent to functions`lessp`*,* `leqp`*,* `greaterp`, and `geqp` in SKILL++.
| = | Supported. | Note that`=` is used as the infix assignment operator in SKILL++. For equality, use the infix operator `==` or function `equal`.
| abs | Same. |
| acos | Same. |
| angle | Unsupported. |
| append | Same. | Takes two arguments only.
| apply | Same. |
| asin | Same. |
| assoc | Same. |
| assq | Same. |
| assv | Same. |
| atan | Same. | In SKILL++,`atan` takes one argument only; `atan2` takes two arguments.
| boolean? | Supported. | Use`booleanp`.
| car, cdr, caar, ...,cddddr | Same. |
| call-with-current-continuation | Unsupported. |
| call-with-input-file | Unsupported. |
| call-with-output-file | Unsupported. |
| ceiling | Same. |
| char->integer | Unsupported. | True character type is not supported inSKILL++. However, single-character symbols can be used to simulate it. The function `charToInt` has the same effect on symbols.
| char-alphabetic? | Unsupported. | Character type not supported.
| char-ci<=? | Unsupported. | Character type not supported.
| char-ci<? | Unsupported. | Character type not supported.
| char-ci=? | Unsupported. | Character type not supported.
| char-ci>=? | Unsupported. | Character type not supported.
| char-ci>? | Unsupported. | Character type not supported.
| char-downcase | Unsupported. | Character type not supported.
| char-lower-case? | Unsupported. | Character type not supported.
| char-numeric? | Unsupported. | Character type not supported.
| char-upcase | Unsupported. | Character type not supported.
| char-upper-case? | Unsupported. | Character type not supported.
| char-whitespace? | Unsupported. | Character type not supported.
| char<=? | Unsupported. | Character type not supported.
| char<? | Unsupported. | Character type not supported.
| char=? | Unsupported. | Character type not supported.
| char>=? | Unsupported. | Character type not supported.
| char>? | Unsupported. | Character type not supported.
| char? | Unsupported. | Character type not supported.
| close-input-port | Supported. | Use`close`.
| close-output-port | Supported. | Use`close`.
| complex? | Unsupported. |
| cons | Same. | The second argument must be a list.
| cos | Same. |
| current-input-port | Supported. | Use the`piport` global variable.
| current-output-port | Supported. | Use the`poport` global variable.
| denominator | Unsupported. |
| display | Same. |
| eof-object? | Unsupported. | SKILL++ reader returns`nil` on EOF.
| eq? | Supported. | Use`eq`.
| equal? | Supported. | Use`equal`.
| eqv? | Supported. | Use`eqv`.
| even? | Supported. | Use`evenp`.
| exact->inexact | Unsupported. |
| exact? | Unsupported. |
| exp | Same. |
| expt | Same. |
| floor | Same. | Use`fix` or `floor`.
| for-each | Supported. | Use`mapc`.
| gcd | Unsupported. |
| imag-part | Unsupported. |
| inexact->exact | Unsupported. |
| inexact? | Unsupported. |
| input-port? | Supported. | Use`inportp`.
| integer->char | Unsupported. | Character type not supported. Use`intToChar` for the same effect on symbols.
| integer? | Supported. | Use`fixp` or `integerp`.
| lcm | Unsupported. |
| length | Same. | Works for both lists and vectors.
| list | Same. |
| list->vector | Supported. | Use`listToVector`.
| list-ref | Supported. | Use`nth`.
| list? | Supported. | Use`listp`.
| log | Same. |
| magnitude | Unsupported. |
| -polar | Unsupported. |
| -rectangular | Unsupported. |
| -string | Unsupported. |
| -vector | Supported. | Use`Vector`.
| map | Supported. | Use`mapcar` instead. Note that `map` in SKILL++ behaves differently from `map` in standard Scheme.
| max | Same. |
| member | Same. |
| memq | Same. |
| memv | Same. |
| min | Same. |
| modulo | Same. | `modulo` differs from `mod` in SKILL++, which is the same as `remainder`.
| negative? | Supported. | Use`minusp` or `negativep`.
| newline | Same. |
| not | Same. | New for SKILL++. Same as ! operator.
| null? | Supported. | Use`null`.
| number->string | Supported. | Use`sprintf`.
| number? | Supported. | Use`numberp`.
| numerator | Unsupported. |
| odd? | Supported. | Use`oddp`.
| open-input-file | Supported. | Use`infile`.
| open-output-file | Supported. | Use`outfile`.
| output-port? | Supported. | Use`outportp`.
| pair? | Supported. | Use`dtpr` or `pairp`.
| peek-char | Unsupported. |
| positive? | Supported. | Use`plusp`.
| procedure? | Supported. | Use`procedurep`.
| quotient | Same. |
| rational? | Unsupported. |
| rationalize | Unsupported. |
| read | Supported. | Or use`lineread`. Returns `nil` on EOF.
| read-char | Unsupported. | Character type not supported. Use`getc` for similar effect.
| real-part | Unsupported. |
| real? | Supported. | Use`floatp` or `realp`.
| remainder | Same. | Use`mod` or `remainder`.
| reverse | Same. |
| round | Same. |
| set-car! | Supported. | Use`rplaca` or `setcar`.
| set-cdr! | Supported. | Use`rplacd` or `setcdr`.
| sin | Same. |
| sqrt | Same. |
| string | Unsupported. |
| string->number | Supported. | Use`readstring`.
| string->symbol | Supported. | Use`concat` or `stringToSymbol`.
| string-append | Supported. | Use`strcat`*.*
| string-ci<=? | Unsupported. |
| string-ci<? | Unsupported. |
| string-ci>? | Unsupported. |
| string-length | Supported. | Use`strlen`.
| string-ref | Unsupported. | Use`getchar` for similar effect.
| string-set! | Unsupported. | Strings in SKILL++ are immutable.
| string<? | Supported. | Use`alphalessp` or `strcmp`.
| string=? | Supported. | Use`alphalessp` or `strcmp`.
| string>=? | Supported. | Use`alphalessp` or `strcmp`.
| string>? | Supported. | Use`alphalessp` or `strcmp`.
| string? | Supported. | Use`stringp`.
| substring | Supported. | Argument values differ. SKILL++ uses`index` and `length`. Scheme standard uses `start` and `end` (`index`).
| symbol->string | Supported. | Use`get_pname` or `symbolToString`.
| symbol? | Supported. | Use`symbolp`.
| tan | Same. |
| truncate | Same. |
| vector | Same. |
| vector-length | Supported. | Use`length`.
| vector->list | Supported. | Use`vectorToList`.
| vector-ref | Supported. | Use`arrayref` or the `a[i]`syntax.
| vector-set! | Supported. | Use`setarray` or the `a[i] = v` syntax.
| vector? | Supported. | Use`arrayp` or `vectorp`.
| write | Same. |
| write-char | Unsupported. |
| zero? | Supported. | Use`zerop`.
For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
