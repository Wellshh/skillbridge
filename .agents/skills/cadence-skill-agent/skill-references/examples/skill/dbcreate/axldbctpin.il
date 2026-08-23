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
;; axldbctpin.il - axlDBCreatePin test driver
;;

; uncomment for print information
(defun dbc_pin_print (return)
        ;(if return (pprint (get (car return) '??)))
        return)

(defun dbc_pin_t1 ()
	(axlMsgPut "**Starting dbc_pin_t1")
	;; all arguments specified in full
	(dbc_pin_print (axlDBCreatePin "pad60sq36d" 0:600
		(make_axlPinText ?number "1FFE" ?offset -100:0
			?text (make_axlTextOrientation ?textBlock "2"
				?rotation 90 ?mirrored t ?justify "right"))))
	;; just text block string instead of the text orientation structure
	(dbc_pin_print (axlDBCreatePin "pad60cir36d" 0:500
		(make_axlPinText ?number "2" ?offset -100:0 ?text "2")))
)
(defun dbc_pin_t2 ()
	(axlMsgPut "**Starting dbc_pin_t2")
	;; lower case pin number
	(dbc_pin_print (axlDBCreatePin "pad60cir36d" 0:300
		(make_axlPinText ?number "4low" ?offset -100:0 ?text "2")))
)
(defun dbc_pin_te_args ()
	(axlMsgPut "**Starting dbc_pin_te_args")
	;; bad location
	(axlDBCreatePin "pad60cir36d" (list "aloc")
		(make_axlPinText ?number "9" ?offset -100:0 ?text "2"))

	;; bad rotation
	(axlDBCreatePin "pad60cir36d" 0:500
		(make_axlPinText ?number "9" ?offset -100:0 ?text "2") "rotrot")

	;; missing padstack
	(axlDBCreatePin "padnofind" 0:500
		(make_axlPinText ?number "9" ?offset -100:0 ?text "2"))

	;; pin text not an axlPinText defstruct
	(axlDBCreatePin "pad60cir36d" 0:500 (make_axlTextOrientation))

	;; pin text - pin number not a string
	(axlDBCreatePin "pad60cir36d" 0:500
		(make_axlPinText ?number 123 ?offset -100:0 ?text "2"))

	;; pin text - pin offset illegal
	(axlDBCreatePin "pad60cir36d" 0:500
		(make_axlPinText ?number "2" ?offset -100 ?text "2"))

	;; pin text - no textOrientation
	(axlDBCreatePin "pad60cir36d" 0:500
		(make_axlPinText ?number "2" ?offset -100:0))
)
(defun dbc_pin_te_text ()
	(axlMsgPut "**Starting dbc_pin_te_text")
	;; pin text  - pin number text out of extents
	(axlDBCreatePin "pad60cir36d" 100:500
		(make_axlPinText ?number "2" ?offset -11100:0 ?text "2"))

	;; pin text  - illegal character in pin number text
	(axlDBCreatePin "pad60cir36d" 200:500
		(make_axlPinText ?number "2!" ?offset -100:0 ?text "2"))

	;; pin text  - nil pin number text
	(axlDBCreatePin "pad60cir36d" 200:500
		(make_axlPinText ?number nil ?offset -100:0 ?text "2"))
)
(defun dbc_pin_test ()
	(dbc_pin_t1)
	(dbc_pin_t2)
	(dbc_pin_te_args)
	(dbc_pin_te_text)
	nil
)
