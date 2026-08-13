# Chapter 17: Common TCL/Tk Issues

 The TCL interpreter is case-sensitive. It is important to type commands in the correct case. In TCL the
“\” is the escape character and can be used for various purposes, for example line continuation
within scripts, etc. It is therefore important that Windows path names be converted to the
appropriate TCL understandable path names for your scripts to work properly. For example, the
following command will produce incorrect results:
source c:\caprev.tcl
The correct command would be:
source {c:\caprev.tcl}
 Press “F5” to refresh the Tk dialog/form, if you observe cluttering due to its overlap with other
dialogs/forms.