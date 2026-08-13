### Cadence SKILL Language User Guide Product Version 6.1.6 November 2014

16
==

SKILL++ Object System
=====================

To gain benefits from object-oriented programming, the Cadence® SKILL language requires extensions beyond lexical scoping and persistent environments.

The CadenceSKILL++ Object System allows for object-oriented interfaces based on classes and generic functions composed of methods specialized on those classes. A class can inherit attributes and functionality from another class known as its superclass. SKILL++ class hierarchies result from this inheritance relationship.

To attain the maximum benefit from the SKILL++ Object System, you should only use it withlexical scoping, because lexical scoping magnifies the power of the interfaces you can develop with the SKILL++ Object System.

You do not need to be familiar with another object-oriented programming language or systemto understand or use the SKILL++ Object System. However, if you are familiar with the Common Lisp Object System (CLOS), you can apply your experience of CLOS in learning the SKILL++ Object System as the SKILL++ Object System is modelled after a subset of the Common Lisp Object System.

For more information, see the following sections:

* [Basic Concepts](#1008217 "SKILL++ Object System")

* [Class Hierarchy](#1016722 "SKILL++ Object System")

* [Browsing the Class Hierarchy](#1008418 "SKILL++ Object System")

* [Advanced Concepts](#1008466 "SKILL++ Object System")

Basic Concepts
--------------

The following items are central concepts of the SKILL++ Object System:

* [Classes and Instances](#1008219 "SKILL++ Object System")

* [Generic Functions and Methods](#generic functions "SKILL++ Object System")

* [Subclasses and Superclasses](#1008238 "SKILL++ Object System")

For more information, see the following sections:

* [Defining a Class (defclass)](#1016021 "SKILL++ Object System")

* [Instantiating a Class (makeInstance)](#1013605 "SKILL++ Object System")

* [Initializing an Instance (initializeInstance)](#1014872 "SKILL++ Object System")

* [Reading and Writing Instance Slots](#1017762 "SKILL++ Object System")

* [Defining a Generic Function (defgeneric)](#defgeneric "SKILL++ Object System")

* [Defining a Method (defmethod)](#1008323 "SKILL++ Object System")

### Classes and Instances

A class is a data structure template. A specific application of the template is termed aninstance. All instances of a class have the same slots. SKILL++ Object System provides the following functions:

* `defclass` function to create a class

* `makeInstance` function to create an instance of a class

* `initializeInstance` function to initialize a newly created instance

### Generic Functions and Methods

A`generic function` is a collection of function objects. Each element in the collection is called a `method`. Each method corresponds to a class. When you call a generic function, you pass an instance as the first argument. The SKILL++ Object System uses the class of the first argument to determine which methods to evaluate.

To distinguish them from SKILL++ Object System generic functions, SKILL functions arecalled `simple functions`. The SKILL++ Object System provides the following functions.

* `defgeneric` function to declare a generic function

* `defmethod` function to declare a method

### Subclasses and Superclasses

SKILL++ Object System supports both single and multiple inheritance. In single inheritance,one class B can inherit structure slots and methods from another class A. You can describe the relationship between the class A and class B as follows:

* B is a subclass of A

* A is a superclass of B

In multiple inheritance, class B can inherit structure slots and methods from multiple classes.For example, class A and class C. In this case, the relationship between class A, B, and C is as follows:

* B is a subclass of A and C

* A is a superclass of B

* C is a superclass of B

#### Class Precedence List

All inheritance decisions are governed by the class precedence list, which is an ordered listof a given class and its superclasses. The following rules determine the precedence order of classes:

* In single inheritance: A class is always more specific than its superclass. So the order ofprecedence flows from left to right. For example,

> `defclass (A ())`

> `defclass (B (A))`

> `; order of precedence is from B to A`

* In multiple inheritance: For a given class, superclasses listed on the left are more specificthan those listed on the right. So the order of precedence is from the superclass on the left to the superclass on the right. For example,

> `defclass (A () ())`

> `defclass (B () ())`

> `defclass (X (A B) ()) ; in class X, class A should come before class B`

> `defclass (Y (B A) ()) ; in class Y, class B should come before class A`

> `; as per the above rule, the following code results in an error:`

> `defclass (M (X Y) ())`

### Defining a Class (defclass)

The domain of geometric objects provides good examples for using object orientedprogramming. Use the `defclass` function to define a class. You specify the superclass, if any, and all the slots of the class.

```
defclass( GeometricObject    ()               ;;; superclass     ()               ;;; list of slot descriptions     ) ; defclass
```

This example defines the`GeometricObject`class. Defining the `GeometricObject` class allows the subsequent definition of default behavior of all geometric objects. It has no slots. Because no superclass is specified, the superclass is the `standardObject` class.

```
defclass( Triangle     ( GeometricObject ) ;;; superclass    (        ( x )       ;;; x slot description         ( y )       ;;; y slot description        ( z )       ;;; z slot description        )    ) ; defClass
```

This example defines the`Triangle` class. It declares that

* The`Triangle` class is a subclass of the `GeometricObject` class

* Each instance shall have three slots named`x`, `y`, and z

#### Slot Options

Slot options, also known as slot specifiers, govern how you initialize the slot as well as youraccess to the slot.

|  |  |
| --- | --- | ---
| **Slot Option** | **Value** | **Meaning**
| `@initarg` | symbol | Defines a keyword argument for the`makeInstance` function.  **Note:** You can supply more than one`@initarg` for a given slot.  For more information on the order of precedence usedwhen multiple @initargs are supplied, see [Rules of Initialization](#1013955 "SKILL++ Object System").
| `@initform` | expression | Defines an expression which initializes the slot.
| `@reader` | symbol | Defines a generic function with this name. The functionreturns the value of the slot.
| `@writer` | symbol | Defines a generic function with this name. The functionaccepts a single argument which becomes the new slot value.
#### Example 1

```
defclass( Triangle     ( GeometricObject )    (        ( x             @initarg x            )        ( y             @initarg y            )        ( z             @initarg z            )        )    ) ; defClass
```

#### Example 2

```
defclass( Circle    ( GeometricObject )    (        ( r @initarg r )        )    ) ; defClass
```

#### Inheritance of Slots

The following rules govern the inheritance of slots in subclasses:

* If a subclass is inherited from a superclass, it also inherits the slots of the superclass.

* If a subclass is inherited from multiple superclasses, which have slots with the samename, then only one slot of the given name is inherited. For example:

> ```
> defclass( Z1 () ((a @initform 1) (b @initform 1)))defclass( Z2 () ((b @initform 2) (a @initform 2) (zz)))defclass( Z3 () ((b @initform 3) (a @initform 3) (zz)))defclass( Z4 () ((b @initform 4))defclass( Z5 (Z1 Z2 Z3 Z4) ())defclass( Z6 (Z4 Z3 Z2 Z1) ())z5 = makeInstance('Z5 )z5->?=> (a b zz) ;; slots a, b, and zz are not duplicated
> ```

**Note:** If you define a class with two slots that have the same name, SKILL creates the classbut also issues a warning.

`defclass(A () ((slotA) (slotB) (slotA @initform 42)))`

`*WARNING* duplicate slot slotA`

Similarly, an error is raised if you define a class in which two`@reader` or `@writer` slot options have the same name. For example:

`defclass(A () ((aa @reader getA) (ff @reader getA)))`

`*Error* defclass: slots (aa ff) cannot use the same name for @reader - getA`

`defclass(B () ((aa @reader getB) (dd @writer getB)))`

```
*Error* defclass: slot aa cannot use the same name for @reader and @writer - getB
```

#### *Rules of Initialization*

* If a subclass is inherited from a superclass, it also inherits the slots and methods of thesuperclass. When you instantiate such a subclass, the initialization arguments (`@initargs`) of the subclass have precedence over the initialization arguments of the superclass. For example:

> ```
> defclass( A1 ()((slot @initform 1 @initarg a)))defclass( B1 (A1)((slot @initform 2 @initarg b)))(slotValue (makeInstance 'B1 ?b 3) 'slot) => 3(slotValue (makeInstance 'B1 ?a 3) 'slot) => 3(slotValue (makeInstance 'B1 ?b 3 ?a 4) 'slot) => 3(slotValue (makeInstance 'B1 ?a 3 ?b 4) 'slot) => 4
> ```

> For more information on instantiating classes, see[Instantiating a Class (makeInstance)](#1013605 "SKILL++ Object System").

* If two or more`@initargs` initialize the same slot, then the order of precedence of the initialization arguments is from left to right. For example:

> ```
> defclass( C1 () ((slot1)(slot3 @initarg s3 @reader rs3)(slot4 @initarg s4 @writer ws4 @initarg (s4a 'slot34))))(slotValue (makeInstance 'C1 ) 'slot4 ) => slot34(slotValue (makeInstance 'C1 ?s4a 5 ) 'slot4 ) => 5(slotValue (makeInstance 'C1 ?s4 5 ) 'slot4 ) => 5(slotValue (makeInstance 'C1 ?s4 5 ?s4a 6 ) 'slot4 ) => 5(slotValue (makeInstance 'C1 ?s4a 5 ?s4 6 ) 'slot4 ) => 6
> ```

### Instantiating a Class (makeInstance)

Use the`makeInstance` function to instantiate a class. The first argument designates the class you are instantiating. Subsequent keyword arguments initialize the instance's slots. The `makeInstance` function returns the newly allocated instance of the class.

```
procedure( makeTriangle( x y z )    if( x<y+z && y<z+x && z<x+y      then        makeInstance( 'Triangle           ?x 1.0*x           ?y 1.0*y           ?z 1.0*z          )      else        error(           "%n %n %n fail triangle inequality test\n"           x y z           )      ) ; if    ) ; procedureexampleTriangle = makeTriangle( 3 4 5 ) => stdobj:0x1e6030
```

The print representation for a SKILL++ Object System instance consists of`stdobj:` followed by a hexadecimal number.

**Note:** `makeInstance` function does not check for invalid `@initargs`. If your code contains invalid `@initargs`, `makeInstance` accepts the `@initargs` as additional `@rest` options.

### Initializing an Instance (initializeInstance)

The`initializeInstance` function is called by `makeInstance` to initialize a newly created instance. You can define methods for `initializeInstance` to specify the actions that need to be taken when the instance is intialized. You can also use `initializeInstance` to add initialization parameters in addition to those defined by `@initform`.

`defclass( A () ())=>t`

```
defmethod( initializeInstance ((obj A) @key (a 3) @rest args))    (printf "initializeInstance : A : was called with args - obj == '%L'     a == '%L' rest == '%L'\n" obj a args) to defmethod( initializeInstance ((obj     A) @key (a 3) @rest args)
```

`(printf "initializeInstance : A : was called with args - obj == '%L'`

`a == '%L' rest == '%L'\n" obj a args))`

`(callNextMethod)=>t`

```
makeInstance( 'A ?a 7)    initializeInstance : A : was called with args - obj == 'stdobj@0x83bf048' a    == '7' rest == 'nil'=>stdobj@0x83bf048
```

```
makeInstance( 'A)    initializeInstance : A : was called with args - obj == 'stdobj@0x83bf054' a    == '3' rest == 'nil'=>stdobj@0x83bf054
```

### Reading and Writing Instance Slots

You can use the arrow operator to read a slot's value.

`exampleTriangle->x => 3.0exampleTriangle->y => 4.0exampleTriangle->z => 5.0`

You can use the`->` operator on the left-side of an assignment statement.

`exampleTriangle->x = 3.5`

The`->??` expression returns a list of the slots and their values.

Another approach is to use the`@reader`and `@writer` slot options to define generic functions for reading and writing slots when you define the class.

```
defclass( Triangle     ( GeometricObject )    (        ( x             @initarg         x            @reader          get_x            @writer          set_x            )        ( y             @initarg         y            @reader          get_y            @writer          set_y            )        ( z             @initarg         z            @reader          get_z            @writer          set_z            )        )    ) ; defClassexampleTriangle = makeTriangle( 3 4 5 ) => stdobj:0x1e603cget_y( exampleTriangle ) => 4.0set_x( exampleTriangle 3.5 ) => 3.5
```

### Defining a Generic Function (defgeneric)

Use the`defgeneric` function to define a generic function. The body of the generic function defines the default method for the generic function.

```
defgeneric( Perimeter ( geometricObject )      error( "Subclass responsibility\n" )      ) ; defgeneric
```

This example indicates that relevant subclasses of the`geometricObject` class, such the `polygon` class, should have a `Perimeter` method. Although not strictly necessary to do so, defining a generic function before defining any methods for it has two advantages:

* You can specify a default method

> Using the`defgeneric` function gives you control over the default method. When you invoke a generic function that has no default method, the SKILL++ Object System raises an error. The following example illustrates calling a generic function which does not have a method defined for the specific argument.

> `Perimeter( 3 )*Error* (Default-method) generic:Perimeter class:fixnum`

* You can document the template argument list

> In the absence of a generic function, the first method you define automatically declaresthe generic function. The method's argument list becomes the template argument list.

You can also use the`defgeneric` function to associate a *proxy* class, called a *generic* *function class*, with the generic function. A *proxy* class is useful when defining customSpecializer methods for a particular class, or for defining dependency protocol where the methods are specialized on a particular generic function class. The basic need for an application specific *proxy* class is to be able to differentiate one group of generic functions from others in an application specific way.

By default, all generic functions are associated with`class:ilGenericFunction`. So, to be able to use a *proxy* class you need to inherit the class from `class:ilGenericFunction`as shown in the following example.

#### Example 1

`defclass(niGF (ilGenericFunction) ()) ; generic class 'niGF`

```
defgeneric(niTest (x y) ?genericFunctionClass niGF) ; generic function niTest is associated with class:niGF
```

In this example,`niGF` is the *proxy* class for the generic function, `niTest`. The instance of this class is created when either a generic function is defined (at `defgeneric` time) or when this class is accessed for the first time.

**Note:** This lazy creation of the*proxy* object is especially true for generic functions loaded from a context.

To retrieve a*proxy* instance from the generic function object, use the `getGFproxy` function as shown in the example below. The instance of the proxy object retrieved is stored in property list of generic function symbol.

#### Example 2

`getGFproxy('niTest)`

`=> stdobj@0x83c0018`

`classOf(getGFproxy('niTest))`

`=> class:niGF`

```
classOf(getGFproxy('printself))  ;; class of standard generic function (printself)
```

`=> class:ilGenericFunction ;; default`

`getGFproxy('abc)`

`=> nil ;; non-existing generic function`

In addition, you can inherit from a generic function*proxy* class by using the `defclass` function, which is in turn inherited from `class:ilGenericFunction` (or optionally from any other standardObject class).

### Defining a Method (defmethod)

Use the`defmethod` function to define a method. You do not need to define the generic function before you define a method for it. When you invoke a generic function, the SKILL++ Object System chooses the method to run based on the class of the first argument you pass to the function.

* If you use conventional syntax`defmethod( … )` in place of the LISP syntax
  `( defmethod … )`, use white space to separate the method name from the argument list.

* You must specify the class of the method's first argument to the`defmethod` function. The first argument to `defmethod` uses the following syntax:

> `( s_arg1 s_class )`

#### Example 1

```
defmethod( Perimeter (( triangle Triangle ))    let( (        (x triangle->x)        (y triangle->y)        (z triangle->z)        )        x+y+z        ) ; let    ) ; defmethodPerimeter( exampleTriangle ) => 12.0
```

This example defines a method named`Perimeter`. It is specialized on the `Triangle` class.

#### Example 2

`defmethod( Perimeter (( c Circle ))    2*c->r*3.1415    ) ; defmethod`

This example defines a`Circle` class and defines the `Perimeter` method for the `Circle` class.

You can specify additional optional arguments while defining a method of a generic functionby using the `@rest` option. For example:

```
defgeneric( myTest (x @rest _args)); The following derived methods use additional @key and @optional arguments:defmethod( myTest (x) 1)=> tdefmethod( myTest ((x string) @key (z 2)) 3)=> tdefmethod( myTest ((x number) @optional a b c) 4)=> t
```

#### The eqv Specializer

While defining a method using`defmethod`, you can use the `eqv` specializer to specialize the method on objects other than classes (for example, some value of its arguments).

When`eqv` is encountered in a method declaration, the value of the argument of the method is compared to the `eqv` value. If a match is found, the method is excecuted. For example,

`defgeneric( factorial (x))`

`defmethod( factorial ((x fixnum)) ;; #1`

`(times x (factorial (sub1 x))))`

`defmethod( factorial ((x (eqv 0)) ;; #2`

`1)`

`; method #2 is applicable if the argument is eqv to 0`

### Defining Method Combinations (@before, @after, and @around)

Once you have defined a generic function, you can combine it with methods that executebefore or after the normal implementation. There are three kinds of additional or auxiliary methods that you can use with `defmethod`: `@before,` `@after`,and `@around` methods.

A standard method combination will have`defmethod` as the primary method and a method qualifier (`@before,` `@after, @around`) between the name of the method and the parameter list.

`defmethod( mymethod @before ((x number)) )`

`defmethod( mymethod @after ((x fixnum)) )`

`defmethod( mymethod @around ((x number) y))`

All the applicable methods are evaluated and partitioned into separate lists according to theirqualifiers. A diagrammatic representation of the order in which the applicable methods are invoked is given below:

The detailed order in which the applicable methods are invoked is as follows:

* The`@around` methods, if defined, are executed first.

> If an`@around` method invokes `callNextMethod`, execute the next most specific `@around` method, with all its `callNextMethod` methods.

> **Note:** If no applicable primary method is defined but an`@around` method exists, an error occurs.

* If there are no`@around` methods or if an `@around` method invokes `callNextMethod` but there are no further `@around` methods to call then proceed as follows:

* The`@before` methods are executed thereafter, with the most-specific method invoked first. All `@before` methods are called before any of the primary methods.

> > If you use a`callNextMethod` in a `@before` method, an error returns.

* Then, the most-specific primary methods are called.

> > You can use a`callNextMethod` inside the body of a primary method to call the next most-specific primary method.

* The`@after` methods are called after the primary methods but in the reverse order, with the least-specific method called first.

> > If you use a`callNextMethod` in an `@after` method, an error returns.

> > **Note:** Calling a generic function that has no primary method, but only`@before` or `@after` method qualifiers, results in an error.

If there is an error in a method, the execution returns to the nearest toplevel.

#### Example 1

`defmethod( mymethod (( x fixnum)) ;; # 1 - primary method`

`...)`

`defmethod( mymethod @before (( x number )) ;; # 2`

`...)`

`defmethod( mymethod @before (( x fixnum )) ;; # 3`

`...)`

`defmethod( mymethod @after (( x fixnum )) ;; #4`

`...)`

`defmethod( mymethod @around (( x fixnum)) ;; # 5 - primary method`

`. . .`

`callNextMethod()`

`. . .)`

When`mymethod` is invoked (with a `fixnum` argument), the methods are called in the following order:

`#5 -> #3 -> #2 -> #1 -> #4`

#### Example 2

`defmethod(aTest @around ((x number) y)`

> `/* 1 : around method*/`

> `callNextMethod())`

`defmethod(aTest @before ((x number) y)`

> `/* 2 : before method */`

> `…)`

`defmethod(aTest ((x number) y)`

> `/* 3 : a primary method */`

> `callNextMethod())`

`defmethod(aTest @after ((x number) y)`

> `/* 4 : after method */`

> `…)`

`defmethod(aTest @around ((x systemObject) y)`

> `/* 5 : another @around method */`

> `callNextMethod())`

`aTest(1)`

`=> #1 -> #5 -> #2 -> #3 -> #4 (calling order)`

### Multi-Method Dispatch

SKILL++ supports multi-method dispatch. With multi-method dispatch, all arguments of amethod are treated equally and the method to be applied is decided at runtime, based on the dynamically-determined types of arguments.

It means that you can define more than one method with the same name in your code. Whenthe method call is made, instead of one parameter specializer determining the method to be applied, it is determined by multiple parameter specializers.

#### Example: Single-Dispatch

`;; body of method1`

`;; method1 specialized on its first argument only (obj)`

`defmethod ( method1 ((obj string) x y)`

`) ; end of method1(string)`

#### Example: Multiple-Dispatch

`;; body of method2`

`;; method2 specialized on 3 arguments:`

`;; obj of type string`

`;; x of type number`

`;; y of class "classY"`

`defmethod ( method2 ((obj string) (x number) (y classY))`

`) ; end of method2`

#### Method Specificity

In case, all applicable methods have the arguments of the same type, the methods are sortedon the order of specificity. So, the most-specific primary method is called first; other methods can then be called from the primary method by using the `callNextMethod`. For example,

```
defmethod( test ((x number) (y string))printf("test number/string\n")callNextMethod())
```

```
defmethod( test ((x fixnum) (y string))printf("test fixnum/string\n")callNextMethod())
```

```
defmethod( test ((x number) (y primitiveObject))printf("test number/primitiveObject\n")callNextMethod())
```

```
defmethod( test ((x fixnum) (y primitiveObject))printf("test fixnum/primitiveObject\n")callNextMethod())
```

`defmethod( test ((x t) (y t))printf("test t/t\n"))`

The class precedence list is used in determining the method specificity:

`t -> systemObject -> primitiveObject -> string`

`t -> systemObject -> primitiveObject -> number -> fixnum`

So, for`test(1 "test")` the order of method calls is:

```
; all the applicable methods are called according to the class precedence of arguments:
```

```
=> test fixnum/string=> test fixnum/primitiveObject=> test number/string=> test number/primitiveObject=> test t/t
```

For`test(1.0 "test")`, the order of method calls is:

```
;three applicable methods are called according to the class precedence of arguments:=> test number/string=> test number/primitiveObject=> test t/t
```

Class Hierarchy
---------------

The diagram below is a horizontal view of the SKILL++ Object System class hierarchy.

* `t` is the superclass of all classes. Class `t` has two immediate subclasses, `standardObject` and `systemObject`.

* `standardObject` is the superclass of all classes you define with `defclass` function. This is the primary portion of the class hierarchy that you can extend.

* `systemObject` is the superclass of `primitiveObject`and`specialObject`. No subclasses of `systemObject` can be used with `defclass`. However, you can add a subclass of `specialObject` by passing a `defstruct` to the `addDefstructClass` function.

* `primitiveObject` is the superclass of all SKILL built-in classes.

* `specialObject` is the superclass of all classes corresponding to the C-level registrable "user-types." It is also the superclass of all classes you define with the `addDefstructClass` function.

This example shows how you can list all of the subclasses. Run this program to see what theclass hierachy is at any given time.

```
procedure( getDirectSubclasses( classObject )    foreach( mapcar c subclassesOf( classObject )        className( c )        ) ; foreach    ) ; procedure
```

```
procedure( getAllSubclasses( classObject )    let( ( direct )        direct = getDirectSubclasses( classObject )        cons(            className( classObject )            direct && foreach( mapcar c direct                 getAllSubclasses( findClass( c ))                ) ; foreach            ) ; cons        ) ; let    ) ; procedure
```

```
getAllSubclasses( findClass( 't )) =>(t     (standardObject         (GeometricObject             (Triangle)                 (Point)                )            )     (systemObject        (primitiveObject            list()            (port)             (funobj)             (array)            (string)             (symbol)             (number                 (fixnum)                 (flonum)                )            )     ( specialObject        (other)         (assocTable)        )    ))
```

Browsing the Class Hierarchy
----------------------------

The SKILL++ Object System provides a number of functions for browsing the class hierarchy:

* [Getting the Class Object from the Class Name](#1008425 "SKILL++ Object System")

* [Getting the Class Name from the Class Object](#1008429 "SKILL++ Object System")

* [Getting the Class of an Instance](#1008434 "SKILL++ Object System")

* [Getting the Class of the Environment Object (envObj)](#1015699 "SKILL++ Object System")

* [Getting the Superclasses of an Instance](#1015633 "SKILL++ Object System")

* [Checking if an Object Is an Instance of a Class](#1008444 "SKILL++ Object System")

* [Checking if One Class Is a Subclass of Another](#1008453 "SKILL++ Object System")

Examples in these sections refer to the following code:

```
defclass( GeometricObject    ()      ;;; superclass     ()      ;;; list of slot descriptions     ) ; defclass
```

```
defclass( Triangle     ( GeometricObject ) ;;; superclass    (        ( x @initarg x )  ;; x slot description         ( y @initarg y )  ;; y slot description        ( z @initarg z )  ;; z slot description        )    ) ; defClass
```

`exampleTriangle = makeTriangle( 3 4 5 ) => stdobj:0x1e6030`

### Getting the Class Object from the Class Name

Use the`findClass` function to get the class object from its name. Use a SKILL symbol to represent the class name.

`findClass( 'Triangle ) => funobj:0x1cb2d8`

### Getting the Class Name from the Class Object

Use the`className` function to get the class symbol. The term `class symbol` refers to the symbol used to represent the class name. The SKILL++ Object System uses a SKILL symbol to represent the class name.

`className( findClass( 'Triangle )) => Triangle`

### Getting the Class of an Instance

Use the`classOf` function to get the class of an instance.

`className( classOf( exampleTriangle ) ) => Triangle`

### Getting the Class of the Environment Object (envObj)

Use the`classOf` function to get the class of the environment object `envObj`.

`z = let( (( x 3 ))`

`theEnvironment()`

`) ; let`

`=> envobj:0x1e0060`

`classOf(z)`

`=> class:envobj`

### Getting the Superclasses of an Instance

Use the`superclassesOf` function to get the superclasses of a class. The function returns a list of class objects.

```
L = superclassesOf( classOf( exampleTriangle ) ) foreach( mapcar classObject L     className( classObject )    ) ; foreach=> (Triangle GeometricObject standardObject t)
```

### Checking if an Object Is an Instance of a Class

Use the`classp` function to check if an object is an instance of a class. You can pass either the class symbol or the class object as the second argument.

#### Example 1

```
classp( exampleTriangle 'Triangle ) => tclassp( 5 'fixnum ) => tclassp( 5 'Triangle ) => nil
```

5 is a`fixnum`. 5 is not an instance of `Triangle`.

#### Example 2

```
classp( exampleTriangle 'GeometricObject ) => tclassp( exampleTriangle 'standardObject ) => tclassp( exampleTriangle t ) => t
```

This example illustrates that`classp` returns `t`for all superclasses of the class of an instance. `Triangle` is a subclass of `GeometricObject`. `GeometricObject` is a subclass of `standardObject`. `standardObject` is a subclass of `t`.

### Checking if One Class Is a Subclass of Another

Use the`subclassp` function to determine whether one class is a subclass of another.

#### Example 1

```
subclassp(     findClass( 'Triangle )     findClass( 'GeometricObject )     ) => t
```

`Triangle` is a subclass of `GeometricObject`.

#### Example 2

`subclassp(     findClass( 'Triangle )     findClass( t )    ) => t`

`Triangle` is a subclass of `t`.

#### Example 3

`subclassp(     findClass( 'Triangle )     findClass( 'fixnum )    ) => nil`

`Triangle` is not a subclass of `fixnum.`

Advanced Concepts
-----------------

This section covers the following advanced aspects of the SKILL++ Object System:

* [Method Argument Restrictions](#1008470 "SKILL++ Object System")

* [Applying a Generic Function](#1020260 "SKILL++ Object System")

* [Incremental Development](#1008502 "SKILL++ Object System")

* [Methods versus Slots](#1008515 "SKILL++ Object System")

* [Sharing Private Functions and Data Between Methods](#1008519 "SKILL++ Object System")

### Method Argument Restrictions

Method argument lists have the following restrictions:

* **Restriction**
* The methods of a generic function can have additonal`@optional` arguments.
* All methods of a generic function must take`@rest` arguments if any of the methods take `@rest` arguments.
* Allow a superset of the keyword arguments specified in the`defgeneric` declaration
* Take`@rest` arguments if any of the methods take @rest arguments

#### Example

```
(defmethod test ((x class1) (y class2) @key a @rest _rest) ... )(defmethod test ((x class3) (y class2) @key b @rest _rest) ... )(defmethod test ((x class1) y @rest _rest) ... )(defmethod test (x y @rest _rest) ... )
```

In the example above, the method`test()` can be called with or without `@key` arguments, provided at least two required arguments are passed to `test()`.

### Applying a Generic Function

When you apply a generic function to some arguments, the SKILL++ Object System performsthe following actions to complete the function call. This process is called *method* *dispatching*. The SKILL++ Object System

* Retrieves the methods of the generic function.

* Determines the class of the first argument to the generic function.

> Based on the class of the first argument passed to the generic function, the SKILL++Object System finds

* No applicable methods

> > SKILL++ Object System calls the default method for the generic function if oneexists. Otherwise it signals an error.

* Exactly one method

* More than one applicable method

> > This situation occurs when you have methods specialized on one or moresuperclasses of the first argument's class.

* Determines applicable methods by examining the method's class specializer.

> A method is applicable if it specialized on the class of the first argument or a superclassof the class of the first argument.

* Sorts the applicable methods according to the chain of superclasses of the firstargument's class.

* The first method in the ordering is the most specific method.

* The last method in the ordering is the least specific method.

* Calls the first method.

You can invoke the`callNextMethod` function from within a method to access the next applicable method in the ordering. For example:

```
defgeneric( describe (obj) ())defclass( GeometricObject () () ) ; no slots or superclassesdefclass( Point    ( GeometricObject )    (         ( name      @initarg name )        ( x         @initarg x );;; x-coordinate        ( y         @initarg y );;; y-coordinate        )    ) ; defclassdefmethod( describe (( object GeometricObject ))    className( classOf( object ))    ) ; defmethoddefmethod( describe (( p Point ))    sprintf( nil "%s %s @ %n:%n"         callNextMethod( p )        p->name        p->x        p->y        )    ) ; the most specific methodaPoint = makeInstance( 'Point ?name "A" ?x 1 ?y 0 )describe( aPoint )     => "Point A @ 1:0"
```

In the example, the`describe` generic function has two methods that are applicable to the argument `aPoint`:

* The method specialized on the`Point` class

* The method specialized on the`GeometricObject` class

The method specializing on the`Point` class is the more specific method, therefore the SKILL++ Object System applies the most specific method to the argument.

### Incremental Development

In the SKILL++ environment , you can redefine SKILL++ functions incrementally. You shouldobserve the following guidelines when redefining SKILL++ Object System elements of your application:

* Redefining methods

> During development, you can expect to redefine methods about as frequently as youredefine procedures. You can redefine a method as long as the redefined method's argument list continues to conform to the generic function.

* Redefining generic functions

> You need to redefine a generic function to change the generic function's default methodor argument list. Such need occurs infrequently. When you redefine a generic function, the SKILL++ Object System discards all existing methods for the generic function.

* Redefining classes

> You need to redefine a class when you want to

* Change the superclass

* Add or remove a slot

* Add or remove a slot option

> If you need to redefine a class, you should exit the SKILL++ environment and reload youapplication. A frequent need to redefine classes probably indicates that you should analyze your application before further programming.

### Methods versus Slots

Methods are generally more expensive to use compared to slots but they offer data hidingand safety. Consider whether the `Triangle`'s `Area` method should access a slot containing the (precomputed) area or whether the area should be computed on the fly. The nature of your application dictates your final decision.

Computing the area on the fly may be costly if, for example, the area of triangles is used often.In such a situation it would be more advantageous to add a slot for area to the triangle class. But then we would have to add @writer methods for the sides of a triangle to recalculate the area when the length of a side changes.

### Sharing Private Functions and Data Between Methods

Using lexical scoping with the SKILL++ Object System allows all methods specialized on aclass to share private functions and data.

The methods for a class might need access to data, such as an association table, that isshared between all instances of the class. Slots you specify in the `defclass` declaration are allocated within each instance of the class.

The methods for a class might all rely on certain helper functions which you need to makeprivate.

Using the following template as a guide achieves both goals.

```
defgeneric( Fun1 ( obj … ) … )defgeneric( Fun2 ( obj … ) … )defclass( Example ( … ) ( … ))let(     (        ( classVar1 … )              ;data shared between all        ( classVar2 … ) …. )       ;instances of the class        )    procedure( HelpFun1( …. ) ;private helper functions    procedure( HelpFun2( …. )    …    defmethod( Fun1 (( obj Example) …. )    defmethod( Fun2 (( obj Example ) … )    ….    ) ; let
```




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2014, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
