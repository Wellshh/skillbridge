# Chapter 14: Capture Communication Server

14.1 Introduction
This application provides a TCL based communication server-client framework. This framework
enables Capture as a communication server. Solution providers and end-users can write their own
server and client side TCL methods and use this framework to establish a communication channel
between Capture (server) and their applications (client).
14.2 Use-model and Customization
The communication server can be invoked from the TCL/Tk Applications Dashboard.

---

This brings up the communication server start-stop dialog:
The user enters a port number and start the server. The user can invoke the same dialog to stop
the server.
The user can then invoke TCL commands on Capture from their application. User can source his
TCL script (with server side methods) in the Capture TCL command shell to create a set of
customized procedures.
For example, the user can define a server side TCL procedure to “Select the object at a particular
location on the page” as-
proc ::capCommServerMethod::SelectObject { pList } {
# requires schematic view to be active
if { [IsSchematicViewActive] != 1 } {
set lReturnValue [list "No schematic view active"]
return $lReturnValue
}
set lX [lindex $pList 0]
set lY [lindex $pList 1]
set lStatus [DboState]
::SelectObject $lX $lY FALSE
set lReturnValue [::GetSelectedObjects]
set lNullObj NULL
if { [llength $lReturnValue] == 0 } {
set lReturnValue [list "No Object for selection"]
}
$lStatus -delete
return $lReturnValue
}

---

Then, the user writes his client-side TCL procedure to call the corresponding server-side TCL
method.
For example, to select an object in Capture schematic (server) from a tclsh (client), the user would
write his TCL procedure and call it from the client end.
proc ::capCommClientMethod::InitClient {host port} {
set s [socket $host $port]
fconfigure $s -buffering line
return $s
}
proc ::capCommClientMethod::SelectObject { pX pY } {
set s [InitClient localhost 9020]
set lObj [list "::capCommServerMethod::SelectObject" [list $pX $pY]]
puts $s $lObj
# wait for the data
gets $s lReturnValue
return $lReturnValue
}

---

Using this framework, the users and solution providers can take advantage of all TCL commands
available in Capture within their application.
For sample procedures, you may refer to the following locations-
1) Server-side methods - <install_root> /tclscripts/capCustomSamples/capCommServerMethods.tcl
2) Client-side methods - <install_root> /tclscripts/capCustomSamples/capCommClientMethods.tcl