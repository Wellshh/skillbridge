# Chapter 2: Learn Basic TCL

If you are already not aware of TCL programming language, this chapter will provide you a good start
point on the way of learning TCL.
2.1 Command
The most important aspect of TCL language is “command”. A TCL program is nothing but commands in
sequence.
An example is, suppose you want to set a variable’s value as 20 and then print its value, it will be done
with two commands:
set x 20
puts $x
The characteristics of a command are as follows:
 A command is space separated words
 A command terminates with a newline or with a ; character
 A command returns a value
o In the above example, “set” command returns the value assigned to the variable. If you
call the set command with just one argument (the variable name), it returns the current
value of the variable
2.2 Command as a parameter (argument) to another command
A command can include a parameter (argument) that appears between [ and ] braces and the content
between [ and ] braces is another command. The example in the previous section can be written as:
puts [set x 20]
In this example, the first argument of puts is another command that sets the variable value to 20 and
returns this value to the puts command, which prints it.

---

2.3 Variable
The value on the variable is set using set command. The value of the variable is retrieved using the
variable name prefixed with $ character.
set x 20  set the variable value
puts $x  get the variable value
2.4 “Space”
Because “space” acts as a delimiter, special care needs to be taken for handling space in names. There
are two ways of dealing with it.
2.4.1 Enclose in double quotes, i.e. " and "
puts "Cadence Design Systems"
This will print “Cadence Design Systems”
Commands and variables substitution work inside the grouping done with double-quotes.
set c Cadence
set d Design
puts "$c $d Systems"
This will print "Cadence Design Systems". Also, escapes like \t, \n will work inside this grouping.
2.4.2 Enclose in curly braces, i.e. { and }
puts { Cadence Design Systems }
This will print “Cadence Design Systems”
Commands and variables substitution “does not” work inside the grouping done with curly braces.
set c Cadence
set d Design
puts {$c $d Systems}
This will print "$c $d Systems".

---

2.5 Control constructs and Eval
Control constructs, e.g. if, for, while, switch etc., are all also commands.
set x 20
if $x {
puts "x is $x"
}
if is a command with two arguments. The first argument is the condition, i.e. the value of the variable
“x”, and the second argument is evaluation block, i.e. {puts “x is $x”} that gets evaluated if the first
argument’s condition is true.
But, in the last section, we said that “Commands and variables substitution “does not” work inside the
grouping done with curly braces”, then how does this second argument of ‘if’ inside curly-braces gets
evaluated as command with all variable substitutions. This happens because the control construct
commands evaluate such arguments using a special command called “Eval” that forces this evaluation.
2.6 String
In TCL, everything is actually a string. Every command is also a string. Because of this, you can create
commands at runtime.
set x p
set y uts
$x$y "Its amazing!"
All these bindings are dynamic and they happen at runtime. The command-name, numbers etc., are all
strings. Every command decides how it interprets its argument strings. These strings can represent a list,
a complete structure, an object or anything. Commands have to do a strict type checking before
converting string to their expected type.
2.7 List
A TCL list is another string, but at the same time TCL provides additional commands to operate directly
on lists for more convenience. Lists are also like commands as they are again space separated words. For
example the string "Cadence Design Systems" is a list with three elements. There are specific commands
to operate on the data as list, e.g. llength of the list will return number of elements, lindex will return
the element at specific index of the list etc. Lists cab also have elements containing spaces. list
command is used to create such desired lists. For example:

---

set ls [list "Cadence Design" Systems]
puts [llength $ls]
llength returns the length of the list as 2. ”lindex $ls 0” will return “Cadence Design” and "lindex $ls 1"
will return "Systems".
A string in TCL can always be interpreted as list and a list can always be interpreted as string, because
everything is eventually a string.
2.8 Math
expr is a command that does the mathematical operations on its arguments.
set i 1
set j 2
puts [expr $j-$i]
This will print 1. If we use “puts [$j-$i]” instead of “puts [expr $j-$i]”, the output would be 2-1
Control constructs commands, e.g. if and while, use expr internally in order to evaluate their condition
argument.
while {$i < $j} {
puts "less"
}
2.9 User defined command, aka Procedure
TCL programmers can write their own set of commands as procedures. Every procedure is a command
with some arguments, a body and a return value. proc command defines a procedure.
proc square {i} {
expr {$i*$i}
}
proc command’s first argument is the procedure name, the second argument is the list of
parameters/arguments and the third argument is the body of the procedure. By default, the return

---

value of the last command inside the body of a procedure is the return value of the procedure.
The return command can also be explicitly used.
You can redefine the TCL built-in commands with your custom procedure.