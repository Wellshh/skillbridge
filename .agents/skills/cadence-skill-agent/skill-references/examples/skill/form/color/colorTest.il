
; demostration for useing color switches in a form popup

unless(boundp('ct) ct = nil)

defun( colorTest ()
    let( (form colorList colorString color)

    form = axlFormCreate('ct "colorTest" nil 'colorTestDispatch t)
    ct = form
    
    for(i 1 axlColorGet('count)
        color = axlColorGet(i);
        colorString = sprintf(nil "i=%L, r=%L, g=%L, b=%L" i car(color) cadr(color) caddr(color))
        colorList = cons(list(colorString i i) colorList)
    );
    colorList = reverse(colorList);
    axlFormBuildPopup(form "COLOR_LIST" colorList);
    axlFormDisplay(form);
))

defun( colorTestDispatch (fw)
    printf("field/value %L = %L (int %L\n)"
	fw->curField fw->curValue, fw->curValueInt )
    if((nequal fw->doneState 0) axlFormClose(fw))
    nil
)
