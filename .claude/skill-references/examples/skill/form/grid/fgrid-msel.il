;;	7/8/97
; Grid programming with multi-select  option
;  -- see fgrid.il for other styles of grid programming

;----------------------------------------------------------------
; PUBLICALLY CALLABLE TEST FUNCTIONS

procedure( mgridtest()

    fg = m_grid("fgrid")
    m_initCols()
    m_initRows()

    ; set multi-row select (note can also set in form file via OPTIONS MULTISELROW
    axlFormGridEvents(fg "grid" '(mrowselect))

    axlFormSetFieldVisible(fg "rowselect" 0)
    axlFormSetFieldVisible(fg "cellselect" 0)
    axlFormSetFieldVisible(fg "change" 0)
    axlFormSetFieldVisible(fg "rightpopup" 0)
    axlFormSetFieldVisible(fg "add4" 0)
    axlFormSetFieldVisible(fg "del4" 0)

    axlFormGridUpdate(fg "grid")
    axlFormSetField(fg "rowselect" t)
    axlFormDisplay(fg)
)

; END PUBLIC FUNCTIONS
;----------------------------------------------------------------
; Open form
procedure( m_grid(t_name)
    let( (f)
        f = axlFormCreate('fg t_name '("msgLines" 0) 'm_gridCB t nil)
    )
)
 
;----------------------------------------------------------------
;; Form callback with grid control
procedure( m_gridCB(fw)
    prog((test cell a b)
     unless((fw->doneState == 0)
	 axlFormClose(fw)
	 return(t)
     )

     case(fw->curField
     ("grid"
	printf("%L:\t(%d,%d) %L\n", fw->event, fw->row, fw->col, fw->curValue)
     )
     )
))
 



;----------------------------------------------------------------
; Initialize columns
; 	Setup 6 columns, one of each column type
;	also play with setting other column options

procedure( m_initCols()
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
; Now create 12 rows
;	also load cells via Batch interface
m_rows = 12

procedure( m_initRows()
	lf = fg
	axlFormGridInsertRows(lf "grid" 0 m_rows)
	axlFormGridSetBatch(lf, "grid" `m_rowsCB, readOnly)
)

;----------------------------------------------------------------
; initialize the cells
;	Play with setting cell options in rows 5 through 8
;	Also set side header for these same rows to override numbers

;
; test data
;
 
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

procedure( m_rowsCB(textCol)
let( (cell)

	cell = axlFormGridNewCell()
        cell->col = 0		; side heading

        for( i 0 m_rows-1
 
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

	      cell->noEdit = t
	      cell->invisible = nil
 
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
;;  reload this file
procedure( m_reload()
        load("fgrid-msel.il")
)        

mgridtest()
