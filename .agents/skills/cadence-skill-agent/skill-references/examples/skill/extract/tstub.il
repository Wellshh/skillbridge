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
;; axltextract2.il - example os property use along with axlExtractMap
;;

; setStubLengthOnECL
;
;  net - the DBID of the net
;  netData - a disembodied property list with the following fields
;	value - the stub length if the property doesn't exist
;	for our example it will have a single field called 'nets that has
;	a value that is the list of net names we will build
;
(defun setStubLengthOnECL (net netData)
    (let ((props (axlDBGetProperties net)))	; get all props for the net

	; see if this is a net that we care about
	; note that 'props' is a standard Skill 'assoc' list
	(cond
	    ((and (assq 'ECL props) (null (assq 'STUB_LENGTH props)))
		; has ECL property and no Stub Length property
		;  so add a STUB_LENGTH and an AUTO_STUB_LENGTH to indicate
		;  that it was added by this process, not manually
		(axlDBAddProp
		    net				; don't need list for just 1
		    ; next argument is a list of name-value lists
	    	    (list
			(list "stub_length"	; add stub_length with value
			    (get netData 'value)) ; from netData prop list
			(list "auto_stub_length" t)))

		; now add the net name to the list of nets that we processed
		(putprop
		    netData			; the prop list
		    (cons			; new value by cons'ing
		        (get net 'name)		; the net name - could also
						;   use dbid->name format
		        (get netData 'nets))	; onto the front of the current
	            'nets)))			; field for the 'putprop'
	t))					; return non nil to continue

(defun mainFunction ()
	; byReference is the disembodied property list containing:
	;    value - the value to use for stub lengths that are added
	;    nets - a list of nets that had the property added
	;
	; note - the first nil makes it disembodied

    (let ((byReference (list nil 'value "0 mils" 'nets nil)))

	; ensure that the property is defined
	(if (null (axlDBGetPropDictEntry "auto_stub_length"))
	    (axlDBCreatePropDictEntry
	        "auto_stub_length"		; the name of the property
	        "boolean"			; the data type of the property
	        "nets"))			; the objects it can attach to

	; walk all "real" data using axlExtractMap
	(axlExtractMap
	    "net_baseview"			; net view - NET_NAME != ""
	    'setStubLengthOnECL			; name of the function that
						;  axlExtractMap will call
						;  for each net
	    byReference)			; the data to pass to the
						;  supplied user function
	(get byReference 'nets)))		; get the resulting list
						;  of net names as the function
						;  return

