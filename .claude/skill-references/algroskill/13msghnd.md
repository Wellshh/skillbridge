### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

13
==

Message Handler Functions
=========================

Overview
--------

This chapter describes the AXL-SKILL message handler system and functions. The message handler system allows you to write AXL-SKILL code that does not have to deal explicitly with errors after each call to a lower level routine, but rather checks at only one or two points. This contrasts with application programs that do not have a buffering and exception-handling message facility, where you must test for and respond to errors and exceptions at each point of possible occurrence in your code. Using the functions described in this chapter, you can do the following:

* Establish a*context* for your application messages.

> A context is a logical section of your application during which you want to buffer and test for the potential errors and warnings you provided for in the lower levels of your application code.

* Write messages to the user with one of five levels of*severity*:

1. **Type Description and Response by AXL Message Handler**
2. Data created by the application, such as a log or report. Writes to journal and the user interface without being buffered.
3. Such as "10% done," "20% done"... Writes to user interface only,not to context message buffer nor to the journal.
4. Such as "Connect line is 5 mils wider than allowed." Writes to context message buffer and journal with a "W" warning tag.
5. Such as "Cannot find symbol DIP24\_200 in library." Beeps and writes to context message buffer and journal with an "E" error tag.
6. Such as "Disk read error. Cannot continue." Double beeps and writes to context message buffer and journal with an "F" fatal tag.

* Test and change the severity level of the messages created and buffered in a context.

* Check for specific messages in the message buffer, and respond appropriately to anticipated conditions detected by lower-level functions.

* Close a context.

The following illustration shows how`axlMsg`functions move messages to and from a context message buffer and the SKILL user interface.

#### Message Handler Example

> ```
> context = axlMsgContextStart("My own context.")axlMsgPut(list("My warning" 2)) axlMsgPut(list("My error" 3)) printf("Message severity %d",axlMsgContextTest(context))axlMsgPut(list("My fatal error %s" 4) "BAD ERROR")if( axlMsgContextInBuf(context "My error")    printf("%s\n" "my error is there"))printf("Message severity %d",axlMsgContextTest(context))axlMsgContextPrint(context)axlMsgContextFinish(context) ⇒ t
> ```

* Starts a context with`axlMsgContextStart`

* Puts a warning, an error, and a fatal error message using`axlMsgPut`

* Checks for the error message with`axlMsgContextInBuf`

* Tests for the context severity level with`axlMsgContextTest`

* Prints the context buffer with`axlMsgContextPrint`

* Ends with`axlMsgContextFinish`

When you load the SKILL program shown above, the SKILL command line outputs the following:

> ```
> W- My warningE- My errorF- My fatal error BAD ERRORMessage severity 3my error is thereMessage severity 4t
> ```

**General usage of the axlMsg System**

* Messages first go to the context buffer

* `axlMsgContextPrint` prints them to the SKILL command line

* The contents of the output buffer from any`print` and `printf` data write to the command line when control returns to the command line. That is why the messages "`Message severity 3`," "`my error is there`" and "`Message severity 4`" follow the buffered messages ("`W- My warning`" ...)

Message Handler Functions
-------------------------

This section lists message handler functions.

### axlMsgPut

`axlMsgPut(g_message_format[g_arg1 ...])⇒ t`

#### Description

Puts a message in the journal file. Use this function to "print" messages. It buffers any errors or warnings, but processes other message classes immediately.

#### Arguments

|  |
| --- | ---
| `g_message_format` | Context message (`printf` like) format string. See ["Overview"](#673530 "13") for a description of messages and valid arguments.
| `g_arg1` ... | Values for substitution arguments for the format string.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

See the["Message Handler Example"](#674168 "13").

> `axlMsgPut(list("Cannot find via %s" 3) "VIA10") ⇒ t`

### axlMsgContextPrint

`axlMsgContextPrint(r_context)⇒ t`

#### Description

Prints the buffered messages and removes them from the message buffer.

#### Arguments

|  |
| --- | ---
| `r_context` | Context handle from`axlMsgContextStart`. Prints messages only for this context (or any children). An argument of `nil` causes `axlMsgContextPrint` to look through all contexts.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

See the["Message Handler Example"](#674168 "13") in the beginning of this chapter.

> `axlMsgContextPrint(context) ⇒ t`

Prints the buffered messages in that context to SKILL command line:

> `W- My warning`

> `E- My error`

> `F- My fatal error BAD ERROR`

### axlMsgContextGetString

`axlMsgContextGetString(r_context)⇒ lt_messages/nil`

#### Description

Gets the messages in the message buffer and removes them from the buffer. Call`axlMsgContextGetString` subsequently to communicate those messages to the user (for example, in a log file).

#### Arguments

|  |
| --- | ---
| `r_context` | Context handle from`axlMsgContextStart`. Gets messages only for this context (or any children). An argument of `nil` causes `axlMsgContextGetString` to look through all contexts.
#### Value Returned

|  |
| --- | ---
| `lt_messages` | List of the text strings of the buffered messages.
| `nil` | No buffered messages found.
#### Example

See the["Message Handler Example"](#674168 "13").

```
axlMsgContextGetString(context)⇒ ("My warning" "My error" "My fatal error BAD ERROR")
```

### axlMsgContextGet

`axlMsgContextGet(r_context)⇒ lt_format_strings/nil`

#### Description

Gets the format strings of the buffered messages. (Not the messages themselves. Compare the example here and the one shown for `axlMsgContextGetString`.) Does not remove the messages from the message buffer, rather it simply provides the caller an alternative to making a number of `axlMsgContextInBuf` calls.

#### Arguments

|  |
| --- | ---
| `r_context` | Context handle from`axlMsgContextStart`. Gets messages only for this context (or any children). An argument of `nil` causes `axlMsgContextGet` to look through all contexts.
#### Value Returned

|  |
| --- | ---
| `lt_format_strings` | List of format strings of the buffered messages.
| `nil` | No buffered messages found.
#### Example

See the["Message Handler Example"](#674168 "13").

> ```
> mylist = axlMsgContextGet(context)⇒ ("My warning" "My error" "My fatal error %s")
> ```

### axlMsgContextTest

`axlMsgContextTest(r_context)⇒ x_class`

#### Description

Returns the most severe message class of the messages in the context message buffer. See[axlMsgContextInBuf](#673606 "13") to check for a particular message class.

#### Arguments

|  |
| --- | ---
| `r_context` | Context handle from`axlMsgContextStart`. Looks only for messages for this context. If `r_context` is `nil`, `axlMsgContextTest` looks through all contexts.
#### Value Returned

|  |
| --- | ---
| `x_class` | The most severe message class of the messages in the message buffer of the given context.
#### Example

See the[Message Handler Example](#674168 "13").

> > `printf("Message severity %d\n" axlMsgContextTest(context))⇒ Message severity 4`

### axlMsgContextInBuf

`axlMsgContextInBuf(r_contextt_format_string)⇒ t`

#### Description

Checks whether message`t_format_string` is in the message buffer of context `r_context`. Gives the application the ability to control code flow based on a particular message reported by a called function. The check is based on the original format string, not the fully substituted message.

#### Arguments

|  |
| --- | ---
| `r_context` | Context handle from`axlMsgContextStart`. Looks only for messages in this context (or any children). If `r_context` is `nil`, `axlMsgContextInBuf` looks through all contexts.
| `t_format_string` | Format string of the message.
#### Value Returned

|  |
| --- | ---
| `t` | Specified message is in the buffer.
| `nil` | Specified message is not in the buffer.
#### Example

See the["Message Handler Example"](#674168 "13").

> `if( axlMsgContextInBuf(context "My error")    printf(%s\n" "My error is there"))`

### axlMsgContextRemove

`axlMsgContextRemove(r_contextt_format_string)⇒ t`

#### Description

Removes a message (or messages) from the buffered messages. Lets you remove messages (usually warnings) from the buffer that you decide, later in a procedure, that you do not want the user to see.

#### Arguments

|  |
| --- | ---
| `r_context` | Context handle from`axlMsgContextStart`. Removes messages for only this context (or any children). If `r_context` is `nil`, `axlMsgContextRemove` looks through all contexts.
| `t_format_string` | Format string of the message. The match for the message in the buffer ignores the substitution parameters used to generate the full text of the message.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

See the["Message Handler Example"](#674168 "13").

> `axlMsgContextRemove(context, "My fatal error %s")⇒ t`

### axlMsgContextStart

`axlMsgContextStart(g_format_string[g_arg1 ...])⇒ r_context`

#### Description

Indicates the start of a message context. Prints any buffered messages for the context.

#### Arguments

|  |
| --- | ---
| `g_format_string` | Context message (`printf` like) message format string.
| `g_arg1` ... | Values for the substitution arguments for the format string. Use`axlMsgClear` (and`Test`*/*`Set`*)* functions to control code flow if the function returns insufficient values.
#### Value Returned

|  |
| --- | ---
| `r_context` | Context handle to use in subsequent`axlMsgContext` calls.
#### Example

See the["Message Handler Example"](#674168 "13").

> > `context = axlMsgContextStart("Messages for %s" "add line")Messages for add line5`

### axlMsgContextFinish

`axlMsgContextFinish(r_context)⇒ t`

#### Description

Indicates the finish of a message context. Prints any buffered messages in the context and clears the context buffer.

#### Arguments

|  |
| --- | ---
| `r_context` | Context handle from`axlMsgContextStart`*.*
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

See the["Message Handler Example"](#674168 "13").

> `context = axlMsgContextStart()... do some things ...axlMsgContextFinish(context)`

### axlMsgContextClear

`axlMsgContextClear(r_context)⇒ t`

#### Description

Clears the buffered messages for a context.

**Note:** You should not normally use this function. Use functions that print (`axlMsgContextPrint`) or retrieve (`axlMsgContextGetString`) messages and then clear them, or use a context finish (`axlMsgContextFinish`) that forces the messages to be printed.

#### Arguments

|  |
| --- | ---
| `r_context` | Context handle from`axlMsgContextStart`. If `r_context` is `nil`, clears all messages in all contexts.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

See the["Message Handler Example"](#674168 "13").

> `context = axlMsgContextStart()... do some things ...axlMsgContextClear(context)`

### axlMsgCancelPrint

`axlMsgCancelPrint()⇒ t`

#### Description

Prints a message informing the user that he requested*cancel*. Since the severity of this message is *Error* (3), AXL writes it to the context buffer as it does other warning, error, and fatal messages. Call this function only from a routine that requests user input.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

See the["Message Handler Example"](#674168 "13").

> `axlMsgCancelPrint()`

Sets severity level to 2 (warning) and puts the following into the message buffer (if`axlMsgSys` messages are in English):

> `User CANCEL received`

### axlMsgCancelSeen

`axlMsgCancelSeen()⇒ t/nil`

#### Description

Checks to see if the`axlMsgCancelPrint` message was printed. Does not poll the input stream for a *CANCEL* key. Checks the buffer of current messages for the occurrence of the `axlSsgSys.cancelRequest` message.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t` | Requested*cancel* has been seen.
| `nil` | No requested*cancel* has been seen.
#### Example

See the["Message Handler Example"](#674168 "13").

> `if( axlMsgCancelSeen()    ; clear input and return    ...`

### axlMsgClear

`axlMsgClear()⇒ t`

#### Description

Clears the current error severity level. You can reset the severity by first saving it using`axlMsgTest`, then setting it using `axlMsgSet`.

#### Arguments

None

#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

See the["Message Handler Example"](#674168 "13").

> `axlMsgClear()`

### axlMsgSet

`axlMsgSet(x_class)⇒ t`

#### Description

Sets the current error severity level. Use only to reset the severity cleared using`axlMsgClear`.

#### Arguments

|  |
| --- | ---
| `x_class` | Severity level.
#### Value Returned

|  |
| --- | ---
| `t` | Always returns`t`.
#### Example

See the["Message Handler Example"](#674168 "13").

> `level = axlMsgTest(); Do something...axlMsgSet(level)`

### axlMsgTest

`axlMsgTest()⇒ x_class`

#### Description

Determines the current error severity level. Returns a single number giving the severity level of the most severe message that has been printed since the last`axlMsgClear` or `axlMsgContextClear`/`Print`/`GetMsg` call.

#### Arguments

None.

#### Value Returned

|  |
| --- | ---
| `x_class` | Highest severity level of all the messages currently in the message buffer.
#### Example

See the["Message Handler Example"](#674168 "13").

> `level = axlMsgTest()⇒ 4`




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
