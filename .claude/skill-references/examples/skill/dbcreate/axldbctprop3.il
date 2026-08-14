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
;; axldbctprop3.il - axlDBGetProperties test driver
;;

(defun dbc_prop3_t1 ()
	(axlMsgPut "**Starting dbc_prop3_t1")

	(axlDBAddProp (axlDBGetDesign) (list "BOARD_THICKNESS" "4.2 hands"))
	(axlDBAddProp (list nil) (list "schematic_name" "your sch"))

	;; layout props - nil as the object
	(printf "nil as object\n")
	(pprint (axlDBGetProperties nil))

	;; layout props - design DBID as the object
	(printf "\ndesign as object\n")
	(pprint (axlDBGetProperties (axlDBGetDesign)))

	;; ask for user props - none defined, propType not a list
	(printf "\nno user props\n")
	(pprint (axlDBGetProperties nil 'user))
	(printf "\n")
	t
)

(defun dbc_prop3_t2 ()
	(axlMsgPut "**Starting dbc_prop3_t2")
    (letStar ( (r1 (caar (axlDBCreateLine (list 5:4 5.6:4.2) .02
						"ETCH/TOP" "SIG1")))
	    (r2 (get r1 'net)))

	(axlDBCreatePropDictEntry "nets_for_get" "string" "nets")

	(axlDBAddProp (list r2)
	    (list (list "stub_length" ".022")
	        (list "bus_name" "Uptown 22")
	        (list "ecl" t)
		(list "ts_allowed" "anywhere")
		(list 'max_parallel "10:12")
		(list 'max_undershoot .015)
		(list 'min_prop_delay "5 ns")
		(list 'nets_for_get "user defined")))

	;; various data types, user and allegro, prop type list provided
	(printf "allegro and user props:\n")
	(pprint (axlDBGetProperties r2 (list "allegro" 'user)))

	;; various data types, allegro only, prop type list with one entry
	(printf "\nallegro props:\n")
	(pprint (axlDBGetProperties r2 (list 'allegro)))

	;; various data types, user only
	(printf "\nuser props:\n")
	(pprint (axlDBGetProperties r2 (list 'user)))

	;; ask for allegro  props - none defined
	(printf "\nno allegro props\n")
	(pprint (axlDBGetProperties r1 'allegro))

	;; ask for default  props - none defined
	(printf "\nno user props\n")
	(pprint (axlDBGetProperties r1))

	(printf "\n")
	r2	; return in case want to have the DBID
))

(defun dbc_prop3_te_args ()
	(axlMsgPut "**Starting dbc_prop3_te_args")

	;; illegal object
	(axlDBGetProperties 73 (list 'notfound))

	;; invalid property group - not a string
	(axlDBGetProperties nil (list 7777))

	;; invalid property group - unknown category
	(axlDBGetProperties nil (list 'notfound))
)
(defun dbc_prop3_test ()
	(dbc_prop3_t1)
	(dbc_prop3_t2)
	(dbc_prop3_te_args)
)
