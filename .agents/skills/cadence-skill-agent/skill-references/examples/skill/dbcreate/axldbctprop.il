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
;; axldbctprop.il - axlDB (Add) property test driver
;;

(defun dbc_prop_t1 ()
	(axlMsgPut "**Starting dbc_prop_t1")
	;; simple prop, name-value list not a list
	(axlDBAddProp (axlDBGetDesign) (list "BOARD_THICKNESS" "4.2 hands"))

	;; simple prop - override existing
	(axlDBAddProp (list nil) (list "schematic_name" "your sch"))
        (printf "your sch\n")
        (pprint (axlDBGetProperties nil))
	(axlDBAddProp (list nil) (list (list "schematic_name" "my sch")))
        (printf "\nmy sch\n")
        (pprint (axlDBGetProperties nil))

	;; simple delete prop
	(axlDBDeleteProp (list nil) "BOARD_THICKNESS")
        (printf "\nno thickness\n")
        (pprint (axlDBGetProperties nil))

        (printf "\n")
)

(defun dbc_prop_t2 ()
	(axlMsgPut "**Starting dbc_prop_t2")
    (letStar ( (r1 (caar (axlDBCreateLine (list 5:4 5.6:4.2) .02
						"ETCH/TOP" "SIG1")))
    	    (r2 (caar (axlDBCreateLine (list 4.5:3 4.5:3.2) .02
						"ETCH/TOP" "SIG2")))
            (r3 (get r1 'net))
	    (r4 (get r2 'net)))

	;; attach provided as a DBID, not a list
	(axlDBAddProp r4 (list "max_parallel" "10:12"))

	;; booleans ignore the value - thus nil same as t or 777
	(axlDBAddProp r4 (list "ecl" nil))

	;; list of dbids and list of props - values string, number, boolean
	(axlDBAddProp (list r1 r2 r3)
	    (list (list "stub_length" ".022")
	        (list "no_lin2shape_fat" t)
	        (list "symbol_etch" 7)		; 7 is ignored
		(list 'min_bond_length .005)
		(list 'max_bond_length "10 mil")))

        (printf "r3 - no parallel\n")
        (pprint (axlDBGetProperties r3))
        (printf "\nr4 - with parallel\n")
        (pprint (axlDBGetProperties r4))

        (printf "\n")

	(axlDBDeleteProp r1 "symbol_etch")
	r4	; just so can get the DBID
))

(defun dbc_prop_te_args ()
	(axlMsgPut "**Starting dbc_prop_te_args")
    (letStar ( (r1 (caar (axlDBCreateLine (list 4.4:2.6 4.4:2.59) .02
						"ETCH/TOP" "SIG1")))
            (r2 (get r1 'net)))

	;; nil attach list
	(if (null (axlDBAddProp nil (list "stub_length" .002)))
	    (axlMsgPut "correct nil returned"))

	;; no properties added
	(axlDBAddProp (list nil) (list "stub_length" .002))

	;; syntax error
	(axlDBAddProp r2 (list "max_parallel" "abc"))

	;; range error
	(axlDBCreatePropDictEntry "range_check"
                "integer" "nets" (list -1 4))
	(axlDBAddProp r2 (list "range_check" 112))

	;; bad prop name
	(axlDBAddProp (list nil) (list 789 t))

	;; prop name not found
	(axlDBAddProp (list nil) (list "nopropfound" t))

	;; bad value - fails converting to a double
	(axlDBAddProp (list nil) (list "schematic_name" r2))

	;; bad parent
	(axlDBAddProp "not a parent" (list "schematic_name" "foo"))
))

(defun dbc_prop_te_args_delete ()
	(axlMsgPut "**Starting dbc_prop_te_args_delete")
    (letStar ( (r1 (caar (axlDBCreateLine (list 7:4 8:4) .02
						"ETCH/TOP" "SIG1")))
            (r2 (get r1 'net)))

	;; delete - nil attach list
	(if (null (axlDBDeleteProp nil (list "stub_length")))
	    (axlMsgPut "correct nil returned"))

	;; delete - no properties deleted
	(axlDBDeleteProp (list nil) (list "stub_length"))

	;; delete - bad prop name
	(axlDBAddProp (list nil) (list 789 t))

	;; delete - prop name not found
	(axlDBDeleteProp (list nil) (list "nopropfound"))

	;; delete - bad parent
	(axlDBDeleteProp "not a parent" (list "schematic_name"))
))

(defun dbc_prop_test ()
	(dbc_prop_t1)
	(dbc_prop_t2)
	(dbc_prop_te_args)
	(dbc_prop_te_args_delete)
)
