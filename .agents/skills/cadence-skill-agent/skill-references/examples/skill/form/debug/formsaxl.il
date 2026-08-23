;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 ; file.cc --
 ;
 ; Author --
 ;	Cadence Design Systems
 ;
 ; Function --
 ;	
 ; Copyright, 1993, Cadence Design Systems, Inc.
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

;;
;; THIS IS A GOOD TEMPLATE FOR ASYNCRONOUS FORM PROGRAMMING
;;


/* $Header: $*/
/*******************************************************************
 *	Copyright 1993 Cadence Design Systems
 *******************************************************************/

/*******************************************************************************
 * ilIsAllegroRunning()
 *
 * Returns t if opus is running.
 ******************************************************************************/
procedure( ilIsAllegroRunning()
    getd('axlFormCreate)
)


/*******************************************************************************/
/*                                 TRACE FORM 
 */

(defstruct ilTraceData
	traceOn
	type
	symbols
	trace
	)
;(setFnWriteProtect 'make_ilTraceData)
;(setFnWriteProtect 'copy_ilTraceData)


ilTraceSettings = nil



/*******************************************************************************
 * ilTraceSetDefaults()
 *
 * Trace functions based on the fields in the form.  
 ******************************************************************************/

(defun ilTraceSetDefaults (reset)
	if(!ilTraceSettings then 
	    ilTraceSettings = (make_ilTraceData)
	    reset = t
	)

	if(reset then
	    ilTraceSettings->traceOn = t
	    ilTraceSettings->type = `functions
	    ilTraceSettings->symbols = ""
	    ilTraceSettings->trace = `by_name
	)
)

/*******************************************************************************
 * ilTraceSetForm()
 *
 * Trace functions based on the fields in the form.  
 ******************************************************************************/

(defun ilTraceSetForm (form)
	axlFormSetField(form 
		if(ilTraceSettings->traceOn "set" "clear") t)
	axlFormSetField(form get_string(ilTraceSettings->type) t)
	axlFormSetField(form "symbols" ilTraceSettings->symbols)
	axlFormSetField(form get_string(ilTraceSettings->trace) t)
)

/*******************************************************************************
 * ilTraceApply()
 *
 * Trace functions based on the fields in the form.  
 ******************************************************************************/

(defun ilTraceApply (form)
   (let (traceOn type trace symbols functions fnNames traceFn fnp varp propp skipp
	functionString)

	traceOn = ilTraceSettings->traceOn
	type = ilTraceSettings->type
	trace = ilTraceSettings->trace
	symbols = ilTraceSettings->symbols
	fnp = (type `functions)
	varp = (type `variables)
	propp = (type `properties)

	traceFn =
	    cond((fnp && traceOn
		    'tracef)
		 (fnp && !traceOn
		    'untrace)
		 (varp && traceOn
		    'tracev)
		 (varp && !traceOn
		    'untracev)
		 (propp && traceOn
		    'tracep)
		 (propp && !traceOn
		    'untracep)
	    )

	case(trace
	    (`by_name 
		fnNames = parseString(symbols " ()")
		functions = mapcar('concat fnNames))
	    (`in_context
		if(varp || propp
		    then axlUIWPrint(form
		     "Warning: Cannot trace variables or properties in a context." 
		     )
		       
		       skipp = t
	 	    else	
			functions = _iliGetContextFns(concat( symbols))
		)
	   )
	   (`regular_exp
		cond((fnp
		       functionString = car(parseString( symbols " ()"))
		       when(functionString
			   functions = listFunctions(functionString)
		       )
		     )
		     (varp
		       functionString = car(parseString( symbols " "))
		       when(functionString
			   functions = listVariables(functionString)
		       )
		     )
		     (t
			axlUIWPrint(form
			   "Warning: Cannot trace regular expressions for properties." 
			   )
		        skipp = t
		     )
		)
	   )
	   (`user_functions 
		if(varp || propp
		    then axlUIWPrint(form
		       "Warning Cannot trace user functions for variables or properties." 
		       )
		       skipp = t
		    else functions = setof(var listFunctions(".*") getd(var) && 
			!getFnWriteProtect(var))
		)
	   )
	   (`all 
		ncons(t))
	)
	unless(skipp
	    apply(traceFn functions)
	)
	skipp
))

/*******************************************************************************
 * ilAXLTraceCB()
 *
 * Track fields in the form
 ******************************************************************************/

(defun ilAXLTraceCB (theForm)
   (let (skipp)

      if(theForm->doneState == 3
      then skipp = t
      else
	case(theForm->curField
	    ("set"
		ilTraceSettings->traceOn = t)
	    ("clear"
		ilTraceSettings->traceOn = nil)

	    ("functions"
		ilTraceSettings->type = 'functions)
	    ("variables"
		ilTraceSettings->type = 'variables)
	    ("properties"
		ilTraceSettings->type = 'properties)

	    ("symbols"
		ilTraceSettings->symbols = theForm->curValue)

	    ("by_name" 
		ilTraceSettings->trace = `by_name)
	    ("in_context" 
		ilTraceSettings->trace = `in_context)
	    ("regular_exp" 
		ilTraceSettings->trace = `regular_exp)
	    ("user_functions" 
		ilTraceSettings->trace = `user_functions)
	    ("all" 
		ilTraceSettings->trace = `all)

	    ("done" 
		if(ilTraceApply(theForm) == nil
		    then axlFormClose(theForm)
		    ))
	    ("cancel" 
		axlFormClose(theForm))
	    ("defaults" 
		ilTraceSetDefaults(t)
		ilTraceSetForm(theForm))
	    ("apply" 
		ilTraceApply(theForm) )
	)
    )
))

/*******************************************************************************
 * ilAXLBuildTraceForm()
 *
 * Build the form that goes inside a window to invoke the SKILL Development
 * Environment functionality.
 ******************************************************************************/
procedure( ilAXLBuildTraceForm()
    let( (dummy) 
	/* And create the form. */
	axlFormCreate('ilTraceWindow "ilTracing"  '("E" "outer")
			'ilAXLTraceCB t nil)
	ilTraceSetDefaults(nil)
	ilTraceSetForm(ilTraceWindow)
	axlFormDisplay(ilTraceWindow)
)) /* skBuildForm */

/*******************************************************************************
 * ilTraceForm()
 * 
 * Display the inside a window that invokes the SKILL Development Environment
 * Functionality.
 ******************************************************************************/
procedure( ilTraceForm()
    (unless (_isSkillDev) error("Sorry - no licence to run SKILL Development."))
        unless( boundp('ilTraceForm) && ilTraceForm
                ilTraceForm = ilAXLBuildTraceForm()
        /* Carry out a sklint initialization here, if not already done.
           One thing this does is to ensure that all messages are registered.
        */
        
        )
)


/* Build trace form */
when( ilIsAllegroRunning() && (!boundp('ilTraceForm) || !ilTraceForm)
	ilTraceForm = ilAXLBuildTraceForm()
)

