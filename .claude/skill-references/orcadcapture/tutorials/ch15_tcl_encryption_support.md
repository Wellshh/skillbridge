# Chapter 15: Tcl Encryption Support

Tcl/Tk support in OrCAD Capture allows users to extend the functionality of the application by writing
scripts. Normal Tcl/Tk programs are unencrypted and can easily be viewed by others. Often it is required
to block such viewing and perhaps editing of these scripts. The reasons for doing so would include the
ability to protect the intellectual property associated with such scripts (algorithms, etc), or to prevent
users from modifying the code, or both.
To address this requirement, Capture offers script developers the option to encrypt their Tcl/Tk scripts
into binary compiled modules. These binary modules are encrypted, making them difficult to view and
comprehend as compared to their original Tcl source-code counterparts.
15.1 Steps to Encrypt Tcl Scripts
To encrypt a Tcl script, the following needs to be done:
1. Write and debug your Tcl script.
2. Once you are satisfied that you have completed your Tcl script, compile your script to binary form
using the following command from the Capture Command Window:
Capture> orcad::encrypt <input_file> [output_file]
The output_file argument is optional, if not specified the output file will have the same name,
but its extension would be .enc.
As an example,
Capture> orcad::encrypt test.tcl
This invokes the built-in Tcl encrypter and generates an output file with the .enc extension. As an
illustration, if the script test.tcl is in C:\temp, then the command would be:
Capture> orcad::encrypt c:/temp/test.tcl
This would generate the file C:\temp\test.enc which would contain encrypted code. If the content of
test.tcl was:
proc show_app_version {} {
puts "You are running [info nameofexecutable]"
}
Then, test.enc would contain something like this:

---

orcad::load
{t1udpzesPvNuZVo8JvcQeQxyzmgf0xfO7PAoFznIS2B9d2V+Pc/cDPcCKL6dArq/wDuvh+X7IO9gJOh6
aXapFxa/2H5IInMDLYe6zWl4DOC3cACk2QlFgjgOBxy0FleeTcfkx+OWQbZaOsEaTB9xNEpGN1pRtNkSG
us1+yDL/DGQL2Wj8KWtmpxDPjz7K/xj7q4h/Q2va7KxTtqpwOgpc/X4Uy1TYFM8MzegKQNWVlcth7rNaX
gM4EIVtxbdF24gxGp3UtrWdV992QW3NUXZrRFE7xzl3fcw97/RKvVeLzNp9aPeqfMWBz/sWdYiaaPVK0K
svvoQls+LJRwCktLzaa/7RGZrQe5s1AhIpANUh9XeGm4ewk4U+VSEKxoHRgY0U7fxhoBAaGMlykspy+6E
ZB4zbV0+Fvr9lui4VLWDY0i7yWn6l+vuXJMT9LqQ4bS3BqsDALQk2TEEz/QJ3q63ppEC+zQcMPmw5O+3u
8quvXN1F7pvtql520xrcusm5udApeVO0Lt6M0ljFGsQ0lSvQy/X1uCl+BgAuvtYFF6HDqfCX/I8b0tjDu
r4epIYMY4iRbd6Xpvu7aJGMymISRlXSFgBFW4ngxbB2LxMT4HBr9u7ZU8vwuTZSuXLGhUntDmOl+B0VPX
aA6y4QyFzlohNk1brYC9G1hQkkvheLIuwV3SV8o09hOq/ViY/OT6GrwpwHLR5R7/TVH9MBwhzkeMRqkUO
kd/O8nom5fUdcGTq2G6hqOLGlbMS4zo71hiA9zEqHQ+vjC+NuuySIwOWLUiAYfUked7DcF1Tmg3hg2YpS
nR3Ytn7s4Bp+n65uUr0/ySoij5pOZWiYrEBalWbzlxZ/j1flbncsRxDCPK4WzGavNZrOXdRR6ukyY5FQQ
SV/Zg9YUGXMPDPSooI/oXoxAojdNwWQNOrjtC9My3gTcqdozkPU7WXuJq68Sqtce79DL8DHIN3OUeYbXS
Ug+PKobpZoFbc7wpz81xMR54JutdW7v/B97Po0iE2hMH3s+jSITaE}
This encrypted file can now be loaded into Capture and run like a normal Tcl script using the source
command:
source c:/temp/test.enc
If the user tries to inspect the code associated with the show_app_version procedure (using the Tcl
info body command), the following message is displayed:
Capture> info body show_app_version
# Compiled -- no source code available
error "called a copy of a compiled script"
This encrypted binary can now be distributed to users.
3. Save the original Tcl script in a secure location for later use. Note that if you discard the original Tcl
script, there is no way that you can get back the original Tcl script from the encrypted binary.
15.2 Important Information about Encrypting Tcl Scripts
The following points should be noted while using the Tcl encrypter:
 You should always save the original Tcl scripts from which you have created the encrypted Tcl files.
Note that there is no way you can get back your original Tcl script from the encrypted code.
 The built-in encrypter does not protect procedures whose bodies that are defined within a Tcl
namespace. As an example, if you have the following script:
# version 1
namespace eval test {
proc show_app_version {} {

---

puts "You are running [info nameofexecutable] "
}
}
The Tcl encrypter will not obfuscate, the body of the show_app_version procedure, and it will be
viewable by users with the info body test::show_app_version command. To work around
this problem you should restructure you Tcl code by defining the body of the procedure outside the
namespace scope as follows:
# version 2
namespace eval test {
}
proc test::show_app_version {} {
puts "You are running [info nameofexecutable] "
}
 If your Tcl code uses the info body command and executes the returned source code, then this will
not work when using encrypted Tcl. For example:
# embedded.tcl
proc get_print_code { a } {
puts "value is $a"
}
proc do_print { a } [info body get_print_code]
do_print "This is a test"
 Lastly, the built-in encrypter supports plain Tcl scripts. It does not support incr Tcl or other variants.