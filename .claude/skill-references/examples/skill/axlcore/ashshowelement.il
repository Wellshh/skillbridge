/* $Header: /vobs/psd_backend_skill/context/axlcore/ashshowelement.il /main/6 05-Aug-08.11:58:25 fxf $ */
/*INDENT OFF*/
/*------------------------------------------------------------------------*/
/*-
 *	Cadence Design Systems
 *
 * (C) COPYRIGHT, Cadence Design Systems, Inc. 2003
 * All Rights Reserved
 * Licensed Materials - Property of Cadence Design Systems
 *
 * No part of this file may be reproduced, stored in a retrieval system,
 * or transmitted in any form or by any means --- electronic, mechanical,
 * photocopying, recording, or otherwise --- without prior written permission
 * of Cadence Design Systems, Inc.
 *
 * WARRANTY:
 * Use all material in this file at your own risk.  Cadence Design Systems 
 * makes no claims about any material contained in this file.
 */
/*------------------------------------------------------------------------*/

/*-
 *
 * This module contains:
 *	This dumps dbid info to a file or stdout in more computer readable format. 
 *	To use 
 *		stdout: 	ashElement(nil dbid)
 *		file: 		ashElement(o_port dbid)
 *					while o_port is an file descriptor
 *	Format is for each element:
 *
 *		@----------------------------------------
 *		<type letter> <attribute><tab><value...>
 *
 *	type letters
 *		c - core element
 *		a - attribute of element
 *		p - property
 *		g - element's group(s) membership
 *		l - line's owned by object
 *		
 */
/*INDENT ON*/

; certain attrs are ignored either because we don't care (readOnly)
; or we want to print them force them out at a certain position (objType)
_ashIgnoredAttrs = '(name objType xy prop readOnly segments)

; if t print even filtered elements
ashElementAll = nil


procedure( ashElement(port item)

ashtest = item

	_ashElement_nest(port item 0)
)

procedure( _ashElement_nest(port item nest)
    prog( (attrs prop props value cnt temp pcell)

    unless(axlIsDBIDType(item)
	return(nil))
    unless(port port = poport)

    attrs = item->?
    foreach( cell _ashIgnoredAttrs
	attrs = remq(cell attrs))

    attrs = sort(attrs 'alphalessp)

    caseq(nest
    (0 
        fprintf(port "@----------------------------------------------------\n")
    )
    (1
        fprintf(port "\n@====================(NESTED)\n")
    )
    (t
	return t)
    )
    
    ; items of importance -- also list above
    fprintf(port "c objType\t%s\n" item->objType )
    when(item->name
        fprintf(port "c name\t\t%s\n" item->name ))
    when(item->xy
        fprintf(port "c xy\t\t%L\n" item->xy ))
    fprintf(port "\n")

    foreach(cell attrs
	value = nil
	pcell = cell
	caseq(cell
	(xnet
	    value = item->xnet->name
	    when( value==item->name
		value = nil)
	    )
	(net
	    value = item->net->name)
	(definition
	    value = item->definition->name)
	(component
	    value = item->component->name)
	(fill
	    value = get(item cell)
	    when(value != t && value != nil 
		temp = car(value)
		fprintf(port "a xhatch spacing=%L width=%L origin=%L angle=%L\n"
			temp->spacing temp->width temp->origin temp->angle)
		temp = cadr(value)
		when( temp
		   fprintf(port "a xhatch spacing=%L width=%L origin=%L angle=%L\n"
			temp->spacing temp->width temp->origin temp->angle)
		)
		value = nil
	    )
	)
	(symbol
	    value = nil)
	(pads
	    value = nil)
	(priority		; don't report shape priority
	    value = nil)
	(ratsnestOn		; for now don't show this
	    value = nil)
	(pins
	    cnt=0
	    foreach( mapc cell item->pins cnt++)
	    value = cnt)
	(instances
	    cnt=0
	    foreach( mapc cell item->instances cnt++)
	    value = cnt)
	(functions
	    cnt=0
	    foreach( mapc cell item->functions cnt++)
	    value = cnt)
	(voids
	    cnt=0
	    foreach( mapc cell item->voids cnt++)
	    	value = cnt)
	(branches
	    value = _ashNetBranches(item->branches, item->ratT)
	    pcell = 'pins)
	(parent
	    if( item->parent && nest==0  then
                fprintf(port "a parent_objType\t%L\n" item->parent->objType)
	        value = item->parent->name
	    )
	)
	(violations
	    cnt = 1
    	    foreach( cell item->violations
               fprintf(port "a violations%d\t%L %L\n" cnt cell->objType cell->name)
	       cnt++)
	    value = nil)
	(t
	    value = get(item cell)
	    unless(ashElementAll
		; check if value is a dbid (or list) and nil it
	        if( axlIsDBIDType(value)  then
	   	    value = nil
		else if( (type(value) == 'list) then
		    temp = car(value)
		    if( temp == nil then
			value = nil
		    else if( axlIsDBIDType(temp) then
	   	        value = nil
		    else if( ((type(temp) == 'list) && axlIsDBIDType(car(temp))) then
	   	        value = nil
		    )))
	        ))
	    )
	))
	when(value  || (car(value)!= nil)
            fprintf(port "a %L\t%L\n" pcell value))
    )

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ; derived 'p' types

    when((item->objType == "net") 
	value = axlDBGetManhattan(item)
        fprintf(port "a etchLength\t%L\n" car(value))
        fprintf(port "a path\t%L\n" cadr(value))
        fprintf(port "a manhattan\t%L\n" caddr(value))
    )

    when( (item->objType == "via") || (item->objType == "pin")
		|| (item->objType == "path")
	value = axlDBGetConnect(item t)
	cnt = 0
	foreach( mapc cell value cnt++)
	when( cnt != 0
            fprintf(port "a numConnections\t%L\n" cnt))

	when( (item->objType == "path") 
	    foreach( cell value 
           	fprintf(port "a connections\t%L %L\n" cell->objType cell->xy)
	    )
	)
    )

    when(item->segments
	_ashSegments(port item->segments))


    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ; groups
    when(item->parentGroups
	_ashGroups(port item->parentGroups))

    when( item->parentGroups
    	fprintf(port "\n"))

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ; properties

    prop = item->prop
    props = prop->?
    props = sort(props 'alphalessp)
    foreach(cell props
        fprintf(port "p %L\t%L\n" cell get(prop cell))
    )
    when((item->objType == "net") && item->diffpair
    	prop = item->diffpair->prop
    	props = prop->?
    	props = sort(props 'alphalessp)
	when(props
            fprintf(port "gp %s Props\n" item->diffpair->type))
	   
    	foreach(cell props
            fprintf(port "p %L\t%L\n" cell get(prop cell))
	)
    )

    when( props
        fprintf(port "\n"))

    ; specials
    ++nest

    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ; nesting elements

    when(value==nil && item->symbol
	_ashElement_nest(port item->symbol nest))

    foreach( cell item->children 
	when(cell->objType == "text"
	    _ashElement_nest(port cell nest))
    )

    when((item->objType == "ratsnest") || (item->objType == "function")
	foreach( cell item->pins 
	    _ashElement_nest(port cell nest))
    )

    t
))

procedure( _ashSegments(port segments )

    foreach( cell segments
        fprintf(port "l %s\t%L w= %L" cell->objType cell->startEnd cell->width)
	when((cell->objType == "arc") 
            fprintf(port " c= %L r= %L" cell->xy cell->radius))
        fprintf(port "\n")
    )
)

procedure( _ashGroups(port groups )

    foreach( cell groups
        fprintf(port "g group %s name= %s\n" cell->type cell->name)
    )
)

procedure( _ashNetBranches(branches ratT )
    let( (name value)
    foreach( branch branches
    	foreach( cell branch->children
	    when(cell->objType=="pin"
		sprintf(name "%s.%s" cell->component->name cell->number)
	        value = cons(name value)
	    )
	)
    )
    foreach( cell ratT
	value = cons(cell->name value))
    value = sort(value 'alphalessp)
))
		
