;;	7/8/97
; Example of Form grid control programming

alias agc axlFormGridInsertCol
alias agu axlFormGridUpdate
alias agg axlFormGridGetCell
alias ago axlFormGridOptions

;----------------------------------------------------------------
; PUBLICALLY CALLABLE TEST FUNCTIONS

procedure( grestore()
    axlFormRestoreField(fg "grid")
)

procedure( geditable(mode)
    axlFormSetFieldEditable(fg "grid" mode)
)

procedure( gvisible(mode)
    axlFormSetFieldVisible(fg "grid" mode)
)

;; Primary entry point to display file
;;	Requires grid.form in current directory

procedure( gridtest()

    fg = grid("fgrid")
    initCols()
    initRows()
    axlFormGridUpdate(fg "grid")
    axlFormSetField(fg "rowselect" t)
    axlFormGridOptions(fg "grid" 'goto -1)
    axlFormDisplay(fg)
)

;
; Demo popup pre-Event filter for both right and left popups
;	left popups only for drop-down cells
;
procedure( ShowPreEvent()
    axlFormGridEvents(fg, "grid" 
	'(rightpopup rightpopupPre rowselect change leftpopupPre))
)

; END PUBLIC FUNCTIONS
;----------------------------------------------------------------
; Open form
procedure( grid(t_name)
    let( (f)
        f = axlFormCreate('fg t_name '("msgLines" 0) 'gridCB t nil)
    )
)
 
;----------------------------------------------------------------
; Available event masks
_eventMask = '(nil rowselect cellselect change rightpopup)

; Test proc for setting event masks
procedure( setMask(fw)
    let( (lenv env mask)
        
	lenv = _eventMask
        while(lenv = cdr(lenv)
	    env = car(lenv)
	    when( axlFormGetField(fw get_pname(env))
		mask = cons(env mask)
	    )
	)
    	axlFormGridEvents(fw "grid" mask)
))        

;----------------------------------------------------------------
;; Form callback with grid control
procedure( gridCB(fw)
    prog((test cell a b)
     unless((fw->doneState == 0)
	 axlFormClose(fw)
	 return(t)
     )

     case(fw->curField
     ("grid"
	printf("%L:\t(%d,%d) %L\n", fw->event, fw->row, fw->col, fw->curValue)
	;;pprint(fw->??)
	axlFormSetField(fw "row" fw->row)
	axlFormSetField(fw "col" fw->col)
	axlFormSetField(fw "event" get_pname(fw->event))
	case(fw->event 
	('rightpopup 
	    case(fw->curValue
	    ("enableCell" 
		cell = axlFormGridNewCell()
		cell->row = fw->row
		cell->col = fw->col
		axlFormSetField(fw "grid" cell)
    		axlFormGridUpdate(fg "grid")
	    )
	    ("disableCell"
		cell = axlFormGridNewCell()
		cell->row = fw->row
		cell->col = fw->col
		cell->noEdit = t
		axlFormSetField(fw "grid" cell)
    		axlFormGridUpdate(fg "grid")
	    )
	    ; override cell with this popup
	    ("setEnum"
		cell = axlFormGridNewCell()
		cell->row = fw->row
		cell->col = fw->col
		cell->popup = "penum2"
		axlFormSetField(fw "grid" cell)
    		axlFormGridUpdate(fg "grid")
	    )
	    ; restore cell to column popup if enum or fillin cell if fill col
	    ("unsetEnum"
		cell = axlFormGridNewCell()
		cell->row = fw->row
		cell->col = fw->col
		cell->popup = ""
		axlFormSetField(fw "grid" cell)
    		axlFormGridUpdate(fg "grid")
	    ))
        )

	; Either of these two events are used when you desire to change
	; the popup before it is displayed (e.g. to control it on
	; a per cell, per column or per row basis
	('leftpopupPre 
	    when(fw->row == 3 axlFormGridCancelPopup(fw, "grid"))
	)
	('rightpopupPre 
	    when(fw->row == 2 axlFormGridCancelPopup(fw, "grid"))
	)
        )
		
     )
     ("rowselect"
	when(fw->curValue
	    setMask(fw)
	)
     )
     ("cellselect"
	when(fw->curValue
	    setMask(fw)
	)
     )
     ("change"
	setMask(fw)
     )
     ("rightpopup"
	setMask(fw)
     )
     ("add4"
	addrows()
     )
     ("del4"
	delrows()
     )
     ("data"
	cell = axlFormGridNewCell()
	sscanf(fw->curValue "%d %d" a b)
	cell->row = a
	cell->col = b
	axlFormGridGetCell(fw, "grid", cell)
	a = cell->??
	pp(a)
     ))
))
 



;----------------------------------------------------------------
; Initialize columns
; 	Setup 6 columns, one of each column type
;	also play with setting other column options

procedure( initCols()
let( (lf p)

	lf = fg

	p = make_formGridCol()

	p->fieldType = 'CHECKITEM
	p->colWidth = 6
	p->align = 'center
	p->headText = "Check"
; Set scripting label for column
	p->scriptLabel = "check"
	axlFormGridInsertCol(lf "grid" p)

	p->fieldType = 'TEXT
	p->colWidth = 8
	p->headText = "Text"
; restore rest of columns back to scripting column number
	p->scriptLabel = nil
	axlFormGridInsertCol(lf "grid" p)

	p->fieldType = 'ENUMSET
	p->colWidth = 8
	p->align = 'left
	p->popup = "penum"
	p->headText = "DropDown"
	axlFormGridInsertCol(lf "grid" p)
	p->popup = nil

	p->fieldType = 'STRING
	p->colWidth = 0
	p->align = 'left
	p->fieldLength = 32
	p->headText = "Fillin Data"
	axlFormGridInsertCol(lf "grid" p)

	p->fieldType = 'LONG
	p->colWidth = 8
	p->align = 'right
	p->fieldLength = 4
	p->min = 1
	p->max = 50
	p->headText = "Integer"
	axlFormGridInsertCol(lf "grid" p)

	p->fieldType = 'REAL
	p->colWidth = 8
	p->fieldLength = 8
	p->min = 0.0
	p->max = 32.0
	p->decimals = 1
	p->headText = "Real"
	axlFormGridInsertCol(lf "grid" p)

	p->fieldType = 'STRING
	p->colWidth = 12
	p->align = 'left
	p->fieldLength = 10
	p->min = nil
	p->max = nil
	p->headText = "String With DropDown"
	p->popup = "pstring"
	axlFormGridInsertCol(lf "grid" p)
	p->popup = nil
))


;----------------------------------------------------------------
; Now create 16 rows
;	also load cells via Batch interface

procedure( initRows()
	lf = fg
	axlFormGridInsertRows(lf "grid" 0 16)
	axlFormGridSetBatch(lf, "grid" `rowsCB, readOnly)
)

;----------------------------------------------------------------
; initialize the cells
;	Play with setting cell options in rows 5 through 8
;	Also set side header for these same rows to override numbers

;
; test data
;
rows = 16
 
checks = listToVector(`(t,nil,t,nil,t,nil,t,nil,t,nil,t,nil,t,nil,t,nil))

readOnly  = listToVector(`("Read","only","text","example",
        "Read","only","text","example",
                "Read","only","text","example",
                        "Read","only","text","example",
                                "Read","only","text","example"
                                ))

drop = listToVector(`("Drop","Down","Enum","Drop",
        "Drop","Enum", "AAAAA", "bbbbb",
                "Drop","Down", "AAAAA", "bbbbb",
                        "Drop","Down", "AAAAA", "bbbbb",
                                "Drop","Down", "AAAAA", "bbbbb"
                                ))

fillin = listToVector(`("type", "in", "any", "text",
                        "type", "in", "any", "text",
                        "type", "in", "any", "text",
                        "type", "in", "any", "text"
                                ))

intVal = listToVector(`(1,-2,3,-4,5,-6,-7,8,9,10,11,12,13,14,15,16,17))

doubleVal = listToVector(`(1.0,-2.0,3.0,-4.0,5.0,-6.0,-7.0,8.0,9.0,10.0,
                11.0,12.0,13.0,14.0,15.0,16.0))

enumEditVal = listToVector( `(
	"An","edit","control","with", "dropdown","support", 
	"An","edit","control","with", "dropdown","support", 
	"An","edit","control","with", "dropdown","support", 
	"An","edit","control","with", "dropdown","support" ))

procedure( rowsCB(textCol)
let( (cell)

	cell = axlFormGridNewCell()
        cell->col = 0		; side heading

	cell->row = 1
        cell->value = "Scr"
; set scripting label for column
	cell->scriptLabel = "rowscr"
        axlFormGridBatch(cell)

	cell->row = 2
        cell->value = "Enum"
; back to using column number for scripting
	cell->scriptLabel = nil
        axlFormGridBatch(cell)
 
        cell->row = 4
        cell->value = "NoEd"
        axlFormGridBatch(cell)

        cell->row = 5
        cell->value = "Inv"
        axlFormGridBatch(cell)
 
        cell->row = 6
        cell->value = "TClr"
        axlFormGridBatch(cell)
 
        cell->row = 7
        cell->value = "BClr"
        axlFormGridBatch(cell)

        cell->row = 8
        cell->value = "Both"
        axlFormGridBatch(cell)
 
        for( i 0 rows-1
 
              cell->row = i +1
	      cell->popup = nil

; set first row to use cell popup overrides. This turns typein cells
; into enum cells and for enum column overrides column popup
; illegal column types will be ignored by form code
	      cond(
	      (i == 1 
		   cell->popup = "penum2"
	           )
	      )

	      cell->textColor = nil
	      cell->backColor = nil

              cond(
              (i == 3
		   cell->noEdit = t
                   )
              (t
	           cell->noEdit = nil
		   )
              )

              cond(
              (i == 4
		   cell->invisible = t
                   )
              (t
	           cell->invisible = nil
		   )
              )
 
              ; -----------------------------------------
              ; CHECK */
              cell->col = 1
              cell->check = checks[i]
              cell->value = nil
 
              cond(
              (i == 5
                  cell->textColor = 'yellow
                  )
              (i == 6
                  cell->backColor = 'yellow
                  )
              (i == 7
                  cell->value = "No"
                   ) 
              (i == 8
                  cell->value = "Yes"
                    )
              )
              axlFormGridBatch(cell)
 
              ;-----------------------------------------
              ; TEXT */
              cell->col = cell->col +1

; VERIFY THAT PRIVATE DATA TO axlFormGridSetBatch works
              cell->value = textCol[i]
 
	      cond(
              (i == 5
                cell->textColor = 'red
		)
              (i == 6
                cell->backColor = 'red
		)
              (i == 7
                cell->backColor = 'red
                cell->textColor = 'green
		)
              )
              axlFormGridBatch(cell)

              ;-----------------------------------------
              ; ENUM */
              cell->col = cell->col +1
              cell->value = drop[i]
 
	      cond(
              ((i == 5)
                cell->textColor = 'yellow
		)
              ((i == 6)
                cell->backColor = 'yellow
		)
	      )
              axlFormGridBatch(cell)
 
              ;-----------------------------------------
              ; FILLIN */
              cell->col = cell->col +1
              cell->value = fillin[i]
 
	      cond(
              ((i == 0)
; Set cell scriptlabel
		cell->scriptLabel = "Fillin1"
		)
              ((i == 5)
                cell->textColor = 'red
		)
              ((i == 6)
                cell->backColor = 'red
		)
              ((i == 7) 
                cell->backColor = 'red
                cell->textColor = 'green
		)
              )
              axlFormGridBatch(cell)
; restore back for rest of cells
	      cell->scriptLabel = nil

              ;-----------------------------------------
              ; INT */
              cell->col = cell->col +1
              cell->value = intVal[i]
 
	      cond(
              ((i == 5)
                cell->textColor = 'green
		)
              ((i == 6)
                cell->backColor = 'green
		)
	      )
              axlFormGridBatch(cell)
 
              ;-----------------------------------------
              ; DOUBLE */
              cell->col = cell->col +1
              cell->value = doubleVal[i]
 
	      cond(
              ((i == 5)
                cell->textColor = 'button
		)
              ((i == 6)
                cell->backColor = 'button
                cell->textColor = 'white
		)
	      )
              axlFormGridBatch(cell)

              ;-----------------------------------------
              ; String W/Enum */
              cell->col = cell->col +1
              cell->value = enumEditVal[i];
              axlFormGridBatch(cell)
 
        )
	t	; return success
))


;----------------------------------------------------------------
; Delete 4 rows at row 5

rowCnt = 4

procedure( delrows()
    axlFormGridDeleteRows(fg "grid" 5 eval(rowCnt))
    axlFormGridUpdate(fg "grid")
)

;----------------------------------------------------------------
; Insert 4 rows at row 5

procedure( addrows()
    axlFormGridInsertRows(fg "grid" 5 eval(rowCnt))
    axlFormGridUpdate(fg "grid")
)

;----------------------------------------------------------------
; Change enum popup -- see if scrolling works
procedure( genum()
    (axlFormBuildPopup fg "penum" 
	'(
	"item1" "item2" "item3"
	"item4" "item5" "item6"
	"item7" "item8" "item9"
	"item10" "item11" "item12"
	"item13" "item14" "item15"
	) 
    )
)

;----------------------------------------------------------------
;;  reload this file
procedure( reload()
        load("fgrid.il")
)        

procedure( form(t_name)
        f = axlFormCreate('f1s t_name '("msgLines" 0) nil nil nil)
        axlFormDisplay(f)
        f
)

gridtest()
