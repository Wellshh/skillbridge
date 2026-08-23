;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 ; file.cc --
 ;
 ; Author --
 ;	Cadence Design Systems
 ;
 ; Function --
 ;	
 ; Copyright, 2011, Cadence Design Systems, Inc.
 ; No part of this file may be reproduced, stored in a retrieval system,
 ; or transmitted in any form or by any means --- electronic, mechanical,
 ; photocopying, recording, or otherwise --- without prior written permission
 ; of Cadence Design Systems, Inc.
 ;
 ; WARRANTY:
 ; NONE. NONE. NONE.
 ; Use all material in this code at your own risk.  Cadence Design Systems 
 ; makes no claims about any material in this archive.  These examples may
 ; not function or may only function in specific instances. We'd like to hear 
 ; what you think of our approach to this, and how we can improve it.
 ;
 ; RESTRICTIONS:
 ; All software contained within this archive is in the public domain or
 ; the author has given us permission for redistribution.  Some packages
 ; have explicit copyrights and notices concerning their redistribution.
 ; Please carefully read all documentation with any package on this tape.
 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


/*
 * Author: John Lane    Cadence Design Systems
 *
 * creates:	Places the BOM of file within the design
 *		NOTE: Truncates Package and Device names if too long
 *
 * Programming example if AXL SKill 
 *	- Creating a user layer
 *	- Uses Extract
 *	- Parsing of a extract result file
 *	- axlDMOpenFile instead of infile to avoid skillPath problems
 *	- adding lines and text to db
 *	- adding all items to a GENERIC group
 */

axlCmdRegister("bom_place" 'billOfMaterial ?cmdType "interactive")

procedure( billOfMaterial( )
prog( ( fp lyr rpt view coord 
	upperleftX upperleftY)

    lyr = "MANUFACTURING/BILL_OF_MATERIALS"
    view = "bom_rep"
    rpt = "bom_rpt"

    /* generate report file to use when adding BOM to design */
    axlExtractToFile(view rpt)
    deleteFile( "extract.log")
    fp = axlDMOpenFile( "ALLEGRO_TEXT" rpt "r")
    unless( fp
	return())

    coord = axlEnterPoint(?prompts "Select origin for Bill of Materials." ?gridSnap t)
    unless( coord
	return())

    upperleftX = car( coord)
    upperleftY = cadr( coord)

    /*
     * create a BILL_OF_MATERIALS subclass in the
     * MANUFACTURING class. Set this class/subclass active
     */  

    axlLayerCreateNonConductor(lyr)
    axlVisibleLayer(lyr t)

    _bomFormat( fp upperleftX upperleftY lyr)
    axlDMClose( fp)

    return(t)
))




procedure( _bomFormat( fp x y lyr )
let( ( textBlock param textOrn symName lastSym device header lstrs word_list
	refdes lrefdes lastRefdes
	dbid grp line newline total partTotal partTotalStr vertexes buf dist grpName
        originalX originalY 
	tst1  char_width char_height char_linespacing char_inc
	linePt1x linePt1y linePt2x linePt2y )

    grpName = "BOMRPT"
    grp = car(axlSelectByName("GROUP" grpName nil))
    axlClearSelSet()
    if( grp then
        when(grp 
	    axlDeleteObject(grp->groupMembers))
    else
        grp = axlDBCreateGroup(grpName "generic" nil)
    )

    textBlock = axlDBControl('activeTextBlock)
    param = axlGetParam(sprintf(nil "paramTextBlock:%d" textBlock))

    originalX = x
    originalY = y
    char_width = param->width + param->charSpace
    char_height = param->height
    char_linespacing = param->lineSpace
    char_inc = char_height + char_linespacing

    textOrn = make_axlTextOrientation(?textBlock textBlock)

    gets( line fp)
    gets( line fp)

    /* Initial title line added to design */
    header = "PACKAGE NAME     DEVICE NAME      REFDES                TOTAL"
    dbid = axlDBCreateText( header x:y textOrn lyr)
    when(dbid
	axlDBAddGroupObjects(grp car(dbid)))

    /*
     * Loop through the report file, grab data
     * and reformat it, then ADD TEXT it
     */

    ;line format:
    ;	A!SYM_NAME!COMP_DEVICE_TYPE!COMP_VALUE!COMP_TOL!COMP_CLASS!REFDES_SORT!REFDES

    y = y - char_inc
    y = y - char_inc
    
    tst1 = t
    total = 0
    while( tst1
	tst1 = gets( line fp)

	if( tst1 then
	    word_list = parseString( line "!")
	    symName = nthelem( 2 word_list)
	    refdes = nthelem( 6 word_list)
	else
	    symName = ""
	)

	unless(lastSym lastSym = symName)

	when( strcmp(symName, lastSym)!=0 
	   ; output data

	   ; number of parts
	   partTotal = length( lrefdes)

	   ; now create output strings for refdes (max 21 chars per line)
		buf = ""
		lstrs = nil
		lastRefdes = car( last(lrefdes))
		foreach(r lrefdes
		    when( (strlen(buf) + strlen(r)+1 > 21)
			lstrs = cons(buf, lstrs)
			buf = ""
		    )
		    buf = strcat(buf r)
		    when((lastRefdes != r)
		       buf = strcat(buf ",") )
		)
		lstrs = cons(buf, lstrs)

		; output text to db
		sprintf(partTotalStr "%d" partTotal)
		printf("HACK %L\n" lstrs)
		lstrs = reverse(lstrs)
		foreach(r lstrs
		    sprintf( newline "%-16.16s %-16.16s %-22.22s%4s" lastSym device r partTotalStr)
    		    dbid = axlDBCreateText( newline x:y textOrn lyr)
		    when(dbid
		        axlDBAddGroupObjects(grp car(dbid)))

	    	    y = y - char_inc	; describing next part type
		    lastSym = ""
		    device = ""
		    partTotalStr = ""
		)

	    lastSym = symName
	    lrefdes = nil

	    total = total + partTotal
	)

	; accumulate refdes of next symbol
	device = nthelem( 3 word_list)
	lrefdes = cons(refdes lrefdes)
    )

    dist = (strlen( header) +2) * char_width
    linePt1x = originalX - char_width
    linePt1y = originalY + char_inc
    linePt2x = originalX + dist		
    linePt2y = y + char_linespacing

    ; skip first 2 lines of extract output (A and J records)
    vertexes = list(
	     linePt1x:linePt1y
	     linePt2x:linePt1y
	     linePt2x:linePt2y
	     linePt1x:linePt2y
	     linePt1x:linePt1y)
    _bomLine(grp vertexes lyr)

    ; draw header delin line
    y = linePt1y - char_linespacing * 3
    vertexes = list( linePt1x:y linePt2x:y)

    _bomLine(grp vertexes lyr)
    ; draw 3 vertical lines
    x = linePt1x + (17.0 * char_width)
    vertexes = list( x:linePt1y x:linePt2y)
    _bomLine(grp vertexes lyr)

    x = x + (17.0 * char_width)
    vertexes = list( x:linePt1y x:linePt2y)
    _bomLine(grp vertexes lyr)

    x = x + (22.0 * char_width)
    vertexes = list( x:linePt1y x:linePt2y)
    _bomLine(grp vertexes lyr)
))

procedure( _bomLine(grp vertexes lyr )
    let( (dbid)
    dbid = axlDBCreateLine(vertexes 0.0 lyr)
    when(dbid axlDBAddGroupObjects(grp car(dbid)))
))
