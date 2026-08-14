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
;; axldbctsym2.il - second axlDBCreateSymbol test driver
;;

(defun dbc_sym2_t1 ()
        (axlMsgPut "**Starting dbc_sym2_t1")

        ;; Alternate symbol refdes
        (axlDBCreateSymbol (list "res500" nil "r9") 0.7:6.3)

        ;; Alternate symbol refdes - OK for symbol not in alt_symbols property
        (axlDBCreateSymbol (list "res1000" 'package "r20") 1.7:6.3)

        ;; Alternate symbol refdes - invalid symbol - pin mismatch
        (axlDBCreateSymbol (list "dip14_3" 'package "r19") 0.7:6.3)

        ;; Alternate symbol refdes - refdes not in database
        (axlDBCreateSymbol (list "dip14_3" 'package "rnope") 0.7:6.3)
)

(defun dbc_sym2_t2 ()
	(axlMsgPut "**Starting dbc_sym2_t2")

     (let ( (pin1
		(make_axlPinData ?number "1" ?padstack "via_rect"
		    ?origin 0:0 ?rotation 0))
	    (pin2
		(make_axlPinData ?number "2" ?padstack "via_rect"
		    ?origin 0.1:0 ?rotation 0)))

	;; Skeleton - unmirrored
	(axlDBCreateSymbolSkeleton "r18" 4.0:5.9 nil nil (list pin1 pin2))

	;; Skeleton - mirrored
	(setq pin1
		(make_axlPinData ?number "1" ?padstack "via_rect"
		    ?origin 0:0 ?rotation 0))
	(setq pin2
		(make_axlPinData ?number "2" ?padstack "via_rect"
		    ?origin 0.1:0 ?rotation 0))
	(axlDBCreateSymbolSkeleton "r15" 4.0:5.8 t 0 (list pin1 pin2))

	;; Skeleton - unmirrored, rotated pins
	(setq pin1
		(make_axlPinData ?number "1" ?padstack "via_rect"
		    ?origin 0:0 ?rotation 20))
	(setq pin2
		(make_axlPinData ?number "2" ?padstack "via_rect"
		    ?origin 0.1:0 ?rotation 90))
	(axlDBCreateSymbolSkeleton "r10" 4.0:5.7 nil 0 (list pin1 pin2))

	;; Skeleton - mirrored, rotated pins
	(setq pin1
		(make_axlPinData ?number "1" ?padstack "via_rect"
		    ?origin 0:0 ?rotation 20))
	(setq pin2
		(make_axlPinData ?number "2" ?padstack "via_rect"
		    ?origin 0.1:0 ?rotation 90))
	(axlDBCreateSymbolSkeleton "r8" 4.0:5.6 t 0 (list pin1 pin2))
))

(defun dbc_sym2_t3 ()
	(axlMsgPut "**Starting dbc_sym2_t3")

     (let ( (pin1
		(make_axlPinData ?number "1" ?padstack "via_rect"
		    ?origin 0:0 ?rotation 0))
	    (pin2
		(make_axlPinData ?number "2" ?padstack "via_rect"
		    ?origin 0.1:0 ?rotation 0)))

	;; Skeleton - unmirrored
	(axlDBCreateSymbolSkeleton "r19" 4.5:5.9 nil 40 (list pin1 pin2))

	;; Skeleton - mirrored
	(setq pin1
		(make_axlPinData ?number "1" ?padstack "via_rect"
		    ?origin 0:0 ?rotation 0))
	(setq pin2
		(make_axlPinData ?number "2" ?padstack "via_rect"
		    ?origin 0.1:0 ?rotation 0))
	(axlDBCreateSymbolSkeleton "r21" 4.5:5.8 t 40 (list pin1 pin2))

	;; Skeleton - unmirrored, rotated pins
	(setq pin1
		(make_axlPinData ?number "1" ?padstack "via_rect"
		    ?origin 0:0 ?rotation 20))
	(setq pin2
		(make_axlPinData ?number "2" ?padstack "via_rect"
		    ?origin 0.1:0 ?rotation 90))
	(axlDBCreateSymbolSkeleton "r6" 4.5:5.7 nil 40 (list pin1 pin2))

	;; Skeleton - mirrored, rotated pins
	(setq pin1
		(make_axlPinData ?number "1" ?padstack "via_rect"
		    ?origin 0:0 ?rotation 20))
	(setq pin2
		(make_axlPinData ?number "2" ?padstack "via_rect"
		    ?origin 0.1:0 ?rotation 90))
	(axlDBCreateSymbolSkeleton "r3" 4.5:5.6 t 40 (list pin1 pin2))
))

(defun dbc_sym2_t4 ()
	(axlMsgPut "**Starting dbc_sym2_t4")

	;; Skeleton - format symbol
	(axlDBCreateSymbolSkeleton (list "target" "format") 7:7.1
		nil nil nil)

	;; Skeleton - drafting symbol
	(axlDBCreateSymbolSkeleton (list "radial_dimension" "drafting") 7:7.3
		nil nil nil)

	;; Skeleton - drafting symbol feature_control symbol - a problem
	(axlDBCreateSymbolSkeleton (list "feature_control symbol" "drafting")
		7:7.3 nil nil nil)

	;; Skeleton - shape symbol is illegal
	(axlDBCreateSymbolSkeleton (list "do_it" "shape") 7:7.3
		nil nil nil)
)

(defun dbc_sym2_test ()
	(dbc_sym2_t1)
	(dbc_sym2_t2)
	(dbc_sym2_t3)
	(dbc_sym2_t4)
	nil
)
