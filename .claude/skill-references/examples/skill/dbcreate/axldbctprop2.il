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
;; axldbctprop2.il - axlDB property (DictEntry) test driver
;;

(defun dbc_prop2_print (pname)
	(pprint (get (axlDBGetPropDictEntry pname) '??))
	(printf "\n"))

(defun dbc_prop2_t1 ()
	(axlMsgPut "**Starting dbc_prop2_t1")

	;; string, elements-value list not a list, layout
	(axlDBCreatePropDictEntry "layout_string"
		"string" "layout")
	(dbc_prop2_print "layout_string")

	;; string, multiple elements in elements list, misc geometry
	(axlDBCreatePropDictEntry "geometry_string"
		"string" (list "clines" "lines" "vias" "shapes"))
	(dbc_prop2_print "geometry_string")
)

(defun dbc_prop2_t2 ()
	(axlMsgPut "**Starting dbc_prop2_t2")

	;; integer, with range and units, nets
	(axlDBCreatePropDictEntry "nets_int_range_units"
		"integer" "nets" (list -1 4) "furlongs") 
	(dbc_prop2_print "nets_int_range_units")

	;; integer, with range reversed, and units, nets
	(axlDBCreatePropDictEntry "nets_int_range_rev"
		"integer" "nets" (list 1 -4) "furlongs") 
	(dbc_prop2_print "nets_int_range_rev")

	;; integer, with low range only, nets
	(axlDBCreatePropDictEntry "nets_integer_low_range"
		"integer" "nets" (list 1 nil))
	(dbc_prop2_print "nets_integer_low_range")

	;; integer, with high range only, nets
	(axlDBCreatePropDictEntry "nets_integer_high_range"
		"integer" "nets" (list nil -1))
	(dbc_prop2_print "nets_integer_high_range")
)
(defun dbc_prop2_t3 ()
	(axlMsgPut "**Starting dbc_prop2_t3")

	;; real, with range, nets
	(axlDBCreatePropDictEntry "nets_real_with_ranges"
		"real" "nets" (list -12.5 22.7)) 
	(dbc_prop2_print "nets_real_with_ranges")

	;; real, with low range only, nets
	(axlDBCreatePropDictEntry "nets_real_low_range"
		"real" "nets" (list 1 nil))
	(dbc_prop2_print "nets_real_low_range")

	;; real, with high range only, nets
	(axlDBCreatePropDictEntry "nets_real_high_range"
		"real" "nets" (list nil -1))
	(dbc_prop2_print "nets_real_high_range")
)

(defun dbc_prop2_t4 ()
	(axlMsgPut "**Starting dbc_prop2_t4")
	;; integer, with very big name and high range, nets
	(axlDBCreatePropDictEntry "nets_longname_range_units678901"
		"integer" "nets" (list -1 0)) 
	(dbc_prop2_print "nets_longname_range_units678901")

	;; real, with very big high range and units, nets
	(axlDBCreatePropDictEntry "big_real_range"
		"real" "layout" (list -1 12345678901234.000001234)) 
	(axlDBAddProp (list nil) (list "big_real_range" 12345678901234.0))
	(dbc_prop2_print "big_real_range")
)
(defun dbc_prop2_t5 ()
	(axlMsgPut "**Starting dbc_prop2_t5")
    (let (r)
	;; get individual fileds with the -> operator
	(axlDBCreatePropDictEntry "for_field_test"
		"real" "layout" (list -1 25) "my units")
	(setq r (axlDBGetPropDictEntry "for_field_test"))
	(foreach fld (get r '?) (printf "%L %L\n" fld (get r fld)))
	nil
))

(defun dbc_prop2_te_args ()
	(axlMsgPut "**Starting dbc_prop2_te_args")

	;; invalid attribute name
	(axlDBCreatePropDictEntry "$%#name" "string" 723)

	;; bad data type
	(axlDBCreatePropDictEntry "fooname" "littlebadstring" 723)

	;; non-string elements list
	(axlDBCreatePropDictEntry "layout_string" "string" 723)

	;; invalid attach element
	(axlDBCreatePropDictEntry "layout_string" "string" "badelement")

	;; bad range - not a list
	(axlDBCreatePropDictEntry "ranger" "real" "layout" "notarange")

	;; bad range - low value not a number
	(axlDBCreatePropDictEntry "ranger" "real" "layout"
			(list "notalow" 22))

	;; bad range - high value not a number
	(axlDBCreatePropDictEntry "ranger" "real" "layout"
			(list 1 "notahigh"))

	;; bad units name - not a string
	(axlDBCreatePropDictEntry "layout_string" "string" "layout"
		nil 7272)

	;; bad units name - too long
	(axlDBCreatePropDictEntry "layout_string" "string" "layout"
		nil "1234567890123456789012345678901234567890")
)

(defun dbc_prop2_te_get ()
	(axlMsgPut "**Starting dbc_prop2_te_args")

	;; invalid attribute name
	(axlDBGetPropDictEntry "$%#name")

	;; no such prop
	(axlDBGetPropDictEntry "your_not_there_name")
)

(defun dbc_prop2_te_inuse ()
	(axlMsgPut "**Starting dbc_prop2_te_inuse")

	(axlDBCreatePropDictEntry "inuse" "boolean" "layout")
	(axlDBAddProp (list nil) (list "inuse" t))
	(axlDBCreatePropDictEntry "inuse" "boolean" "layout")

)
(defun dbc_prop2_test ()
	(dbc_prop2_t1)
	(dbc_prop2_t2)
	(dbc_prop2_t3)
	(dbc_prop2_t4)
	(dbc_prop2_t5)
	(dbc_prop2_te_args)
	(dbc_prop2_te_get)
	(dbc_prop2_te_inuse)
)
