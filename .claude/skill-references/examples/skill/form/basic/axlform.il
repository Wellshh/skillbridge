;; AXL FORM DEMO 
;;	requires axlform.form file to in current directory.
;;	optional bitmap files (*.bmp)
;;
;; This demostrates form controls, options and programming. Exception
;; is the grid control which is demostrated in fgrid.il
;;
;;  To access demo, in Skill
;;	load "axlform.il"
;;	formtest
;;  Embedded test
;; 	EmbededForm 

;----------------------------------------------------------------
; PUBLIC CALLABLE TEST FUNCTIONS

;; init global form handle to nil
unless(boundp('f1s) f1s = nil)
unless(boundp('f1s_lastTab) f1s_lastTab = "Fillins")

; Open form in preferred programming model
procedure( formtest() 
	f1s = IFormTest(f1s)
)


;----------------------------------------------------------------
;; expose feature
(defun ExposeTest ()
    axlUIWExpose(f1s)
)



;----------------------------------------------------------------
; These make playing wirh form capabilities easier
alias fset axlFormSetField
alias fdelete axlFormListDeleteAll
alias fget axlFormGetField
alias finfo axlFormSetInfo
alias fsel  axlFormListSelect
alias wecho axlUIWPrint

;----------------------------------------------------------------
;----------------------------------------------------------------
;----------------------------------------------------------------

;(setq f2s nil)

; generate a list with 1000 strings
(defun listMany ()
     (let (manyStrings)
	manyStrings = tconc(nil "0")
	for(cnt 1 1000
	    tconc(manyStrings, sprintf(nil, "%d", cnt))
	)
     manyStrings = car(manyStrings)
))

(defun _afCallback (fw)
     (prog (t1 item field cnt)
	
	; support for active help (like in enved cmd) - must enable capability by
	; calling axlFormSetMouseActive after form is opened
	when(fw->mouseActive 
    	    axlFormSetField(fw "active_help" sprintf(nil "Help for %s" fw->curField))
	    return(t)
	)
	(printf "field/value %L = %L (int %L\n)" 
		fw->curField fw->curValue, fw->curValueInt )
	(printf "doneState %L\n" fw->doneState )

	case(fw->curField
	("tab"
		f1s_lastTab = fw->curValue)

        ("redraw"
                axlGRPDrwUpdate(fw->Bitmap_handle)
                axlGRPDrwUpdate(fw->Graphic_handle)
		)
	("progstep"
		axlFormSetField(fw "progress" nil)
	)
	("bmpcheck"
		if( fw->curValue == t then
    		    t1 = "axlformbmp3" 
		else
    		    t1 = "axlformbmp2" 
		)
    		axlFormSetField(fw "bmp2" t1 )
	)

; the TREE control handling RMB popups
;	note fw->curValueInt has the current item in the tree control
	("tree"
	    when( (fw->event == 'rightpopup)
		case(fw->curValue
		("expand_all"
		    axlFormTreeViewSet(fw "tree" 'TV_EXPAND nil))
		("collapse_top"
		    axlFormTreeViewSet(fw "tree" 'TV_COLLAPSE_TOP nil))
		)
	    )
	)

; FILLIN FIELD
	("string"
		axlUIYesNo("fillin")
	)

; FILLEN WITH DROPDOWN
	("strwenum"
		;;axlFormBuildPopup(fw "strwenum" 
		;;  '(("fee" "0") ("fi" "1") ("foo" "2") ("oops" "3") ("disabled" "4") ))
    		axlFormSetField(fw "strwenum" "10" )
	)

; LIST FIELD EVENTS
	("listfield"
		fw->_listIndex = fw->curValueInt
		axlFormSetField(fw "listtext" fw->curValue)
		when( fw->doubleClick printf("Double Click listfield!\n\n"))
	)
	("listfield_delete"
	    ; delete selected item and select next
	    field = "listfield"
	    unless(fw->_listIndex fw->_listIndex = 0)
	    axlFormListDeleteItem(fw field fw->_listIndex)

    	    item = axlFormListGetItem(fw field fw->_listIndex)
    	    unless( item
         	item = axlFormListGetItem(fw field -1)
		 fw->_listIndex =  fw->_listIndex - 1
		)
    	    when( item
        	axlFormListSelect(fw, field item)
		axlFormSetField(fw "listtext" item))
	)
	("mlistfield"
		fw->_listIndex = fw->curValueInt
		printf("multi-list isSelect %L\n" fw->event)
		axlFormSetField(fw "listtext" fw->curValue)
		when( fw->doubleClick printf("Double Click mlistfield!\n\n"))
	)
	("mlistfield_sel"
	     ; HACK
	     cnt = axlFormListGetSelCount(fw "mlistfield")
	     sprintf(item "Cnt = %L" cnt)
	     axlFormSetField(fw "listtext" item)

	     ; select or deselect all
	     if(fw->_mlistSel then
		fw->_mlistSel = nil
	     else
		fw->_mlistSel = t
	     )
	     axlFormListSelAll(fw "mlistfield" fw->_mlistSel)
	)
	)
		
	if((nequal fw->doneState 0)  then
	    axlFormClose(fw)
	)
	return()
))



;----------------------------------------------------------------
;----------------------------------------------------------------
;----------------------------------------------------------------
;; GENERAL FORM PROGRAMMING METHOD
;; 		async form mode
;;
;; This is a good example on how to program a form.
;; 
procedure( IFormTest(fw)
    prog( (position bitmap_handle graphic_handle)	; need to do this since have a return

    ;; Good pratice
    ;; If form is open expose it and return
    (cond (fw 
        (axlUIWExpose fw)
        (return fw)
        )
    )

    position = '("NE")

    ;; no msg lines in form
    position = '("NE" "msglines" 1)

    ;; create a form handle, position form and set-up mode
    fw = axlFormCreate('f1s "axlform" position '_afCallback t nil )

    ; enable active help field
    ; in _afCallback must see mouseActive code in start of funcition
    axlFormSetMouseActive(fw)

    bitmap_handle = axlGRPDrwInit(fw "bitmap" 'FlipIt)
    bitmap_handle->Flip = 0
    graphic_handle = axlGRPDrwInit(fw "graphic" 'FlipIt)
    graphic_handle->Flip = 1
    fw->Bitmap_handle = bitmap_handle
    fw->Graphic_handle = graphic_handle

    ;; Set a better title then the form file
    axlFormTitle(fw "--F1-- Skill Test Form" )
    
    ;; Build a dynamic popup for enum field
    ;axlFormBuildPopup(fw "enum" '(("item1" "1") ("item2" "2") ("item3" "3")) )
    axlFormBuildPopup(fw "enum" '(("item1") ("item2") ("item3")) )

    ; demostrate color and font type in popups
    axlFormBuildPopup(fw "enumcolor" 
	      '(("green" 1 green) 
		("yellow" 2 yellow bold) 
		("red" 3 red underline)
		("blue" 4 blue )
		("button" 5 button )
		("black" 6 black )
		("white" 7 white )
		("Bold" 8 bold )
		("Underline" 9 underline )
		) )

    ;; Set form fields to starting values
    IFormRefresh(fw)

    ;; Last thing to do is display the form
    axlFormDisplay(fw)

    return(fw)	; return form handle to caller
    )
)
    
procedure( IFormRefresh(fw)
    (let (tree tree1)	; need to do this since have a return

    ;; Give all fields default values
    (axlFormSetField fw "enum" "1" )
    (axlFormSetField fw "enumdrop" 3 )
    (axlFormSetField fw "enumcolor" 2 )
    (axlFormSetField fw "string" "hello" )
    (axlFormSetField fw "strwenum" "test" )
    (axlFormSetField fw "float" 20.1006 )
    (axlFormSetField fw "int" 50 )
    (axlFormSetField fw "slidebar" 4 )

    ; use newline ("\n") to create line breaks
    (axlFormSetField fw "mline" "Show multi-line\nLine 2\nLine 3\nLine 4")
    ; mark as read-only but user will still be able to scroll
    (axlFormSetFieldEditable fw "mline" nil )


    ; show associated text field is also greyed
    (axlFormSetField fw "grey_enum" "4" )
    (axlFormSetField fw "grey_string" "Disabled control" )
    TestGrey( nil ) 


    ;(axlFormSetFieldVisible fw "checkbox" 0 )
    (axlFormSetField fw "radio1" t )
    (axlFormSetField fw "checkbox" t )
    
    ;; normal list
    IFormLists(fw)

    ; Set group text
    (axlFormSetField fw "group" "Group Text Set By Program" )

    ; Show static text can be disabled
    (axlFormSetFieldEditable fw "disabled_text" nil)

    ;; We could also use axlFormSetInfo here
    (axlFormSetField fw "info" "Info set by program" )
    ; set multiline text
    (axlFormSetField fw "multiline" "This text can run to multiple lines. Got to type enough for it. See if three lines work for me. " )

    ;; Progress meter initial settin
    (axlFormSetField fw "progress" '(5 100 15) )

    ;; Color setting
    (axlFormSetField fw "color" 'red )
    (axlFormSetField fw "icolor" 'green )

    ;; Set Bitmap setting
    (axlFormSetField fw "bmp2" "axlformbmp2" )

    (axlFormSetField fw f1s_lastTab 1 )


    ;; tree view
    tree = axlFormTreeViewAddItem(fw "tree" "one" nil nil 'TVSELECT_3STATE)
        f1sTreeRoot = tree
        axlFormTreeViewAddItem(fw "tree" "one" tree nil 'TVSELECT_SINGLE)
        tree1 = axlFormTreeViewAddItem(fw "tree" "two" tree nil 'TVSELECT_2STATE)
            axlFormTreeViewAddItem(fw "tree" "one" tree1 nil t)
            axlFormTreeViewAddItem(fw "tree" "two" tree1 nil t)
            axlFormTreeViewAddItem(fw "tree" "three" tree1 nil t)
        axlFormTreeViewAddItem(fw "tree" "three" tree nil)
        axlFormTreeViewAddItem(fw "tree" "four" tree nil)
    tree = axlFormTreeViewAddItem(fw "tree" "two" nil nil )
        axlFormTreeViewAddItem(fw "tree" "two-one" tree nil nil)
        axlFormTreeViewAddItem(fw "tree" "two-two" tree nil nil)
    axlFormTreeViewAddItem(fw "tree" "three" nil nil)
    axlFormTreeViewAddItem(fw "tree" "four" nil nil)
    axlFormTreeViewAddItem(fw "tree" "five" nil nil)
    axlFormTreeViewAddItem(fw "tree" "six" nil nil)
    axlFormTreeViewAddItem(fw "tree" "seven" nil nil)
    axlFormTreeViewAddItem(fw "tree" "eight" nil nil t)
    axlFormTreeViewAddItem(fw "tree" "nine" nil nil t)
    axlFormTreeViewSetSelectState(fw "tree" tree 'TVSTATE_DISABLED)
))

;----------------------------------------------------------------
;----------------------------------------------------------------
;----------------------------------------------------------------
;; LESS DESIRABLE FORM PROGRAMMING METHODS

;; sync form mode -- no callback
;; no message lines
;; string only option to axlFormCreate
(defun f2 ()
( setq f2s (axlFormCreate 'f2s "axlform" '( "E" "outer" "msglines" ) nil nil t ))
(  axlFormTitle f2s "--F2-- Skill Test Form" )
(  axlFormDisplay f2s )
(printf "i am here\n")
(axlFormClose f2s)
)


;; sync form mode -- with callback
;; multiple message lines
(defun f3 ()
( setq myf3 
    (axlFormCreate 'myf3 "axlform" '( "msglines" 3 "E" "inner" ) 'f3func nil t ))
(  axlFormTitle myf3 "--F3-- Skill Test Form" )
(  axlFormDisplay myf3 )
(printf "i am here\n")
(axlFormClose myf3)
)

(defun sl ()
	(axlFormSetField f1s "info" (getCurrentTime) )
	(axlUIWUpdate f1s)
	(gets iport )
)

(defun blockTest ()
fblock = (axlFormCreate 'f1s "axlform" '( 's 'block ) '_afCallback t nil )
axlFormDisplay(fblock)
(printf "i am blocked\n")
axlUIWBlock(fblock)
)


;--------------------------------------------------------------
;--------------------------------------------------------------
;--------------------------------------------------------------
; MISC

(defun f3func (theform)
	
	if(theform->curField == "string" then
	   axlFormRestoreField(theform, "string")
	   )

	(printf "field/value %L = %L\n" theform->curField theform->curValue )

	; test prevention of display again blocking
	;axlFormDisplay(theform)

	(printf "doneState %L\n" theform->doneState )
	nil
)


;----------------------------------------------------------------
;----------------------------------------------------------------
;----------------------------------------------------------------
; Field Coding examples


;----------------------------------------------------------------
;----------------------------------------------------------------
; Modifications applicable to most control types
;
;
; Checks that double click option works in list field
;
procedure( TestGrey( on ) 
    (axlFormSetFieldEditable f1s "grey_enum" on)
    (axlFormSetFieldEditable f1s "grey_string" on)
)

;----------------------------------------------------------------
; checks that basic field types can have color added
;	color can also be database color but not shown 
;	(see axlFormColorize doc)


;----------------------------------------------------------------
; COLOR -- appling color to form fields both background and 
;    text (foreground)
;

f1s_field = "strwenum"

procedure( TestColor( mode color ) 
    prog((option )

    caseq(mode
    (background
	option = 'background)
    (text
	option = 'text)
    (nil
	TestColor('background nil)
	TestColor('text nil)
	return()
    ))
    axlFormColorize(f1s f1s_field option color)
))

procedure( ChangeColor( mode color ) 

    prog((option items )

    caseq(mode
    (background
	option = 'background)
    (text
	option = 'text)
    (nil
	ChangeColor('background nil)
	ChangeColor('text nil)
	return()
    ))

    ; set color on each control that supports color
    items = '("enum" "string" "strwenum" "float" "int" "slidebar" 
			"radio1" "checkbox" "info" "ButtoN")
    foreach( mapc item items
        axlFormColorize(f1s item option color)
    )
))

;----------------------------------------------------------------
; Various methods to dynamically build popups
(defun f1enum2 ()
  (  axlFormBuildPopup f1s "enum" '(("item4" 4) ("item5" 5) ("item6" 6)) )
)

(defun f1enum3 ()
  (  axlFormBuildPopup f1s "enum" '("item7" "item8" "item9") )
)


;; prereq -- run formtest func
(defun badPopTest ()
 axlFormBuildPopup( f1s "enum" '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16))
)

;----------------------------------------------------------------
;----------------------------------------------------------------
;
; LIST BOX

; Initialize list controls
procedure( IFormLists(fw)
    (let (items)	

    ; Multi-Selection List - Reflects optimal manner of initializing a 
    ;	list box control using lists of strings

    items = '("NET1" "NET2" "NET3" "NET4" "NET10" "GND" "VCC" "DP1" "DP2" "BUS1")
    axlFormSetField(fw "mlistfield" items )

    ; load Single Selection List - brute force programming
    axlFormSetField(fw "listfield" "a long string for horizontal scroll" )
    axlFormSetField(fw "listfield" " fxf  c  " )
    axlFormSetField(fw "listfield" "a" )
    axlFormSetField(fw "listfield" "b   c  " )
    axlFormSetField(fw "listfield" "g " )
    axlFormSetField(fw "listfield" "b" )
    axlFormSetField(fw "listfield" "d" )
    axlFormSetField(fw "listfield" "e" )
    axlFormSetField(fw "listfield" "f" )
    axlFormSetField(fw "listfield" "g" )
    axlFormSetField(fw "listfield" "h" )
    axlFormSetField(fw "listfield" "i" )
    axlFormSetField(fw "listfield" "j" )
    axlFormSetField(fw "listfield" "k" )
    axlFormSetField(fw "listfield" nil )

    ;axlFormListSelect(fw "listfield" "d" )

))


;
; Checks that double click option works in list field
;
procedure( TestDoubleClick( on ) 
    let((option)

    when( on  option = 'doubleClick)

    axlFormListOptions(f1s, "listfield" option)
))

;
; Checks that double click option works in list field
;
procedure( TestMultiSelect( ) 
    let((items cnt)

    cnt = axlFormListGetSelCount(f1s "mlistfield")
    items = axlFormListGetSelItems(f1s "mlistfield")
    printf("Selected items (cnt=%d) %L\n" cnt items)

))

;----------------------------------------------------------------
; test performance of lists
(defun plisttest ()
     (let (many)
	many = listMany()

	println("Test 1 -- new list -- individual SetFields")
	axlFormListDeleteAll(f1s, "listfield")
	axlShell("stopwatch reset")
	foreach( mapc x many
	    axlFormSetField(f1s, "listfield" x)
	)
	axlFormSetField(f1s, "listfield" nil)
	axlShell("stopwatch stop")

	; This is the optimal method for large lists
	println("Test 2 -- new list -- One call")
	axlFormListDeleteAll(f1s, "listfield")
	axlShell("stopwatch reset")
	axlFormSetField(f1s, "listfield" many)
	axlShell("stopwatch stop")

	println("Test 3 -- add to old list -- many calls")
	axlFormListDeleteAll(f1s, "listfield")
	axlFormSetField(f1s, "listfield" '("a" "b" "c" "d"))
	axlShell("stopwatch reset")
	foreach( mapc x many
	    axlFormListAddItem(f1s, "listfield" x 2)
	)
	axlFormSetField(f1s, "listfield" nil)
	axlShell("stopwatch stop")

	println("Test 4 -- add to old list -- One call")
	axlFormListDeleteAll(f1s, "listfield")
	axlFormSetField(f1s, "listfield" '("a" "b" "c" "d"))
	axlShell("stopwatch reset")
	axlFormListAddItem(f1s, "listfield" many 2)
	axlShell("stopwatch stop")
))

;----------------------------------------------------------------
;----------------------------------------------------------------
; TREE VIEW EXAMPLES
;      IFormRefresh (above) has basic tree view example
;

(defstruct TestTreeItem string id)
(defun TestTreeItems ()
(list
(make_TestTreeItem ?string "For Sale" ?id nil)
(list (make_TestTreeItem ?string "Redmond" ?id nil)
	(list (make_TestTreeItem ?string "100 B. Lnb" ?id nil))
	(list (make_TestTreeItem ?string "523 Apple Rd" ?id nil))
	(list (make_TestTreeItem ?string "12 Peach St" ?id nil)))
(list (make_TestTreeItem ?string "Bellevue" ?id nil)
	(list (make_TestTreeItem ?string "22 Daffodil Ln" ?id nil))
	(list (make_TestTreeItem ?string "354 Orchid Rd" ?id nil))
	(list (make_TestTreeItem ?string "64 Lily St" ?id nil)))
(list (make_TestTreeItem ?string "Seattle" ?id nil)
	(list (make_TestTreeItem ?string "33 Nicholas Ln" ?id nil))
	(list (make_TestTreeItem ?string "5 Tracy Rd" ?id nil))
	(list (make_TestTreeItem ?string "46 Jean St" ?id nil)))))

(defun TestAddTreeItem (form field parent item)
  (let (hParent hItem hAfter str)
	(cond
	(item->string
	  str = item->string
	  hParent = parent->id
	  hItem = axlFormTreeViewAddItem(form field str hParent hAfter)
	  item->id = hItem)
	(t
	  nil)
 	)
))

(defun TestAddTreeItems (form field l_list)
  (let ((parent (car l_list)))

    ;; root node
    TestAddTreeItem(form field nil parent)

    ;; Add the reset of the nodes
    TestAddTreeItemsRecursive(form field l_list)
))


(defun TestAddTreeItemsRecursive (form field l_list)
  (let ((parent (car l_list)))
    (when parent
	  (mapc
	    (lambda (item)
	       (TestAddTreeItem form field parent (car item))
	       (TestAddTreeItemsRecursive form field item))
	    (cdr l_list))))
)

(defun TreeAddSort ()
	axlFormTreeViewSet(f1s "tree" 'TV_SORTCHILDREN f1sTreeRoot)
)

;; tree control expand "ALL" methods
(defun TreeExpandAll ()
	axlFormTreeViewSet(f1s "tree" 'TV_EXPAND nil)
)

(defun TreeExpandTop ()
	axlFormTreeViewSet(f1s "tree" 'TV_EXPAND_TOP nil)
)

(defun TreeCollapseAll ()
	axlFormTreeViewSet(f1s "tree" 'TV_COLLAPSE nil)
)

(defun TreeCollapseTop ()
	axlFormTreeViewSet(f1s "tree" 'TV_COLLAPSE_TOP nil)
)


;----------------------------------------------------------------
;----------------------------------------------------------------
; TRACKBAR Example

(defun f1track50 ()
	; set midway -- define 0 to 100 in form file
	axlFormSetField(f1s, "trackbar" 50)
)

(defun f1trackInc ()
        ; Increment trackbar
        axlFormSetField(f1s "trackbar" t)
)

(defun f1tracklen500 ()
        ; set length of trackbar to 500 with default incrment (1)
        axlFormSetFieldLimits(f1s "trackbar" 1 500)
)


;----------------------------------------------------------------
;----------------------------------------------------------------
;
; DRAWING Example
;
(defun bitmap_callback (handle)
; Must map the window
    (axlGRPDrwMapWindow handle 232 60)
; Properties for outline rectangle
    (putprop handle "unfilled" 'fill)
    (putprop handle "black" 'color)
    (putprop handle 2 'width)

    (axlGRPDrwRectangle handle '(1 1) '(249 54))

; Example of using a bitmap
    (axlGRPDrwBitmap handle "test.bmp")

)

(defun graphic_callback (handle)
; Must map the window
    (axlGRPDrwMapWindow handle 1200 1800)

; Example of setting option properties for fill, color and width
    (putprop handle "unfilled" 'fill)
    (putprop handle "red" 'color)
    (putprop handle 3 'width)

; Example of  an unfilled, red,  rectangle
    (axlGRPDrwRectangle handle '(1 1) '(1200 1800))

; Example of a filled black rectangle
    (putprop handle "black" 'color)
    (putprop handle "filled" 'fill)
    (axlGRPDrwRectangle handle '(50 50) '(200 200))

; Example of an unfilled yellow rectangle with a really thick line
    (putprop handle "unfilled" 'fill)
    (putprop handle "yellow" 'color)
    (putprop handle 50 'width)
    (axlGRPDrwRectangle handle '(950 50) '(1100 500))
    (putprop handle 3 'width)

; Example of a blue, unfilled circle
    (putprop handle "blue" 'color)
    (axlGRPDrwCircle handle '(600 900) 300)

; Example of a filled, green circle
    (putprop handle "green" 'color)
    (putprop handle "filled" 'fill)
    (axlGRPDrwCircle handle '(600 900) 50)

; Example of a solid filled, green circle
    (putprop handle "blue" 'color)
    (putprop handle "filled_solid" 'fill)
    (axlGRPDrwCircle handle '(200 1300) 90)

; Example of a red, simple line
    (putprop handle "red" 'color)
    (putprop handle 50 'width)
    (axlGRPDrwLine handle (list '(500 500) '(750 750)))

; Example of a red, poly line
    (putprop handle "red" 'color)
    (putprop handle 50 'width)
    (axlGRPDrwLine handle (list '(100 1500) '(150 1600) '(200 1400)))

; Example of a white, filled, polygon
    (putprop handle "white" 'color)
    (axlGRPDrwPoly handle (list '(500 1500) '(650 1600) '(700 1400)))

; Example of a black, text, opaque background, left justified
    (putprop handle "black" 'color)
    (putprop handle "opaque" 'text_bkmode)
    (axlGRPDrwText handle '(300 100) "Left text")

; Example of a red, text, transparent background. center justified
    (putprop handle "red" 'color)
    (putprop handle "transparent" 'text_bkmode)
    (putprop handle "center" 'text_align)
    (axlGRPDrwText handle '(300 200) "center text")
)

(defun FlipIt (handle)
	if(zerop(handle->Flip) then
	   bitmap_callback(handle)
	   handle->Flip = 1
	else
	   graphic_callback(handle)
	   handle->Flip = 0
	)
)
