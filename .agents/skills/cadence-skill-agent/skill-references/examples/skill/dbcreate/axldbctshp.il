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
;; axldbctshp.il - Create Shape test driver
;;
;; REQUIREMENT: design must have 2 decimal places
;;		and have 2 nets called GND and VCC


(defun dbc_shp_t1 ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_t1")
        ;; unfilled shape
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 3:5.5 3:6.5 3.5:6.7 4:6.5 4:5.5 3:5.5))
                                        nil "BOARD GEOMETRY/DIMENSION"))
	(setq shape (car (axlDBCreateCloseShape shape)))

        ;; default layer
        (setq shape (axlDBCreateOpenShape
            		(axlPathStart (list 1.2:1.5 1.2:2.5 1.35:2.7 1.5:2.5
							1.5:1.5 1.2:1.5))
			t nil))
	(setq shape (car (axlDBCreateCloseShape shape)))))

(defun dbc_shp_t2 ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_t2")
        ;; filled shape (etch)
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 4:4.5 4:6 5:6.2 6:6 6:4.5 4:4.5))
                                        t "ETCH/TOP" "GND"))
	(axlDBCreateCloseShape shape)))

(defun dbc_shp_t3 ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_t3")
        ;; filled shape with void and voidCircle
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 4:1.5 4:4 6:4 6:1.5 4:1.5))
				(list
				    (make_axlFill ?origin 0:0
					?angle 45.0 ?width .01 ?spacing .05)
				    (make_axlFill ?origin 0:0
					?angle 135.0 ?width .01 ?spacing .05))
				"ETCH/TOP" "GND"))
	(axlDBCreateVoid shape
	    (axlPathStart (list 5:2 5.2:2.2 5.4:2 5.2:1.8 5:2) 0.01))

	(axlDBCreateVoidCircle shape (list 4.2:3.8 0.5) .01)

	(axlDBCreateCloseShape shape)))

(defun dbc_shp_t4 ()
        (axlMsgPut "**Starting dbc_shp_t4")
        ;; unfilled shape using axlDBCreateShape interface
        (axlDBCreateShape
            (axlPathStart (list 2.5:5.5 2.5:6.5 2.6:6.7 2.75:6.5
						2.75:5.5 2.5:5.5))
	    nil "BOARD GEOMETRY/DIMENSION"))

(defun dbc_shp_t5 ()
        (axlMsgPut "**Starting dbc_shp_t5")
        ;; solid filled shape using axlDBCreateShape interface
        (axlDBCreateShape
            (axlPathStart (list 1.5:4.5 1.5:6 1.6:6.2 1.75:6 1.75:4.5 1.5:4.5))
	    t "BOARD GEOMETRY/DIMENSION"))

(defun dbc_shp_t6 ()
        (axlMsgPut "**Starting dbc_shp_t6")
        ;; cross hatch filled shape using axlDBCreateShape interface
        (axlDBCreateShape
            (axlPathStart (list 1:1.5 1:4 1.4:4 1.4:1.5 1:1.5))
				(list
				    (make_axlFill ?origin 0.018:0.018
					?angle 0.0 ?width .010 ?spacing .2)
				    (make_axlFill ?origin 0:0
					?angle 90.0 ?width .010 ?spacing .10))
				"ETCH/TOP" "GND"))

(defun dbc_shp_t7 ()
        (axlMsgPut "**Starting dbc_shp_t7")
        ;; unfilled shape using axlDBCreateRectangle interface
        (axlDBCreateRectangle (list 0.2:0.2 10.5:8.0)
				nil "BOARD GEOMETRY/OUTLINE")

        ;; filled shape using axlDBCreateRectangle interface - DRC created
        (axlDBCreateRectangle (list 8:1.5 9:4)
				t "ETCH/TOP" "VCC"))

(defun dbc_shp_t8 ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_t8")
 
        ;; attached text to copy
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 7:5 7:5.5 7.5:5.5 7.5:5 7:5))
                                        nil "BOARD GEOMETRY/DIMENSION"))
        (axlDBAddProp shape (list "signal_model" "signal_model_value"))
        (axlDBCreateText "Attached Text\nAnd a second line" 7:4.5 "3"
                "BOARD GEOMETRY/DIMENSION" shape)
        (setq shape (car (axlDBCreateCloseShape shape)))
))

(defun dbc_shp_t9 ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_t9")
 
        ;; can't make a rectangle - props only defined for shapes
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 8:5 8:5.5 8.5:5.5 8.5:5 8:5))
                                        t "ETCH/TOP"))
        (axlDBAddProp shape (list "imbedded_plane_flag" t))
        (setq shape (car (axlDBCreateCloseShape shape)))
))

(defun dbc_shp_te_args ()
        (axlMsgPut "**Starting dbc_shp_te_args")
        ;; illegal path
        (axlDBCreateOpenShape "notapath")

        ;; illegal layer
        (axlDBCreateOpenShape 
            (axlPathStart (list 3:5.5 3:6.5 3.5:6.7 4:6.5 4:5.5 3:5.5))
	    nil "BOARD GUMMY/DIMENSION")

        ;; illegal net
        (axlDBCreateOpenShape 
            (axlPathStart (list 3:5.5 3:6.5 3.5:6.7 4:6.5 4:5.5 3:5.5))
	    nil "ETCH/TOP" "sigmund")

        ;; illegal parent
        (axlDBCreateOpenShape 
            (axlPathStart (list 3:5.5 3:6.5 3.5:6.7 4:6.5 4:5.5 3:5.5))
	    nil "ETCH/TOP" nil "badparent")

	;; close - illegal shape
	(axlDBCreateCloseShape "notashape"))

(defun dbc_shp_te_close ()
    (let (shape shape2 shape0)
        (axlMsgPut "**Starting dbc_shp_te_close")
        (setq shape0 (axlDBCreateOpenShape
            (axlPathStart (list 1:1.5 1:2.5 1.5:2.5 1.5:1.5 1:1.5))
                                        t "ETCH/BOTTOM"))

	(setq shape (car (axlDBCreateCloseShape shape0)))

        (setq shape2 (axlDBCreateOpenShape
            (axlPathStart (list 1:1.5 1:2.5 1.5:2.5 1.5:1.5 1:1.5))
                                        t "ETCH/TOP"))
        ;; close the non-active shape
	(axlDBCreateCloseShape shape)

        ;; close an already closed shape
	(setq shape2 (car (axlDBCreateCloseShape shape2))) ; first close
	(axlDBCreateCloseShape shape2)			; no error on second

        ;; close providing illegal shape DBID
	(axlDBCreateCloseShape shape0)  ; shape0 not the shape
))


(defun dbc_shp_te_fill ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_te_fill")
        ;; unfilled shape on keepout subclass
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 3:5.5 3:6.5 4:6.5 4:5.5 3:5.5))
                                        nil "ROUTE KEEPOUT/ALL"))

        ;; filled shape on keepin subclass
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 3:5.5 3:6.5 4:6.5 4:5.5 3:5.5))
                                        t "ROUTE KEEPIN/ALL"))

        ;; bad fill record (string) 
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 3:5.5 3:6.5 4:6.5 4:5.5 3:5.5))
                                        "abc" "ROUTE KEEPOUT/ALL"))

        ;; bad fill record (list of non-defstructs) 
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 3:5.5 3:6.5 4:6.5 4:5.5 3:5.5))
                                        (list "defstruct") "ROUTE KEEPOUT/ALL"))

	;; too many fill structs
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 4:1.5 4:4 6:4 6:1.5 4:1.5))
				(list
				    (make_axlFill
					?angle 45.0 ?width .010 ?spacing .05)
				    (make_axlFill
					?angle 90.0 ?width .010 ?spacing .05)
				    (make_axlFill
					?angle 135.0 ?width .010 ?spacing .05))
				"ETCH/TOP" "GND"))

	;; bad angle type
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 4:1.5 4:4 6:4 6:1.5 4:1.5))
	    (list (make_axlFill ?angle "angle" ?width .010 ?spacing .05))
	    "ETCH/TOP" "GND"))

	;; bad width
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 4:1.5 4:4 6:4 6:1.5 4:1.5))
	    (list (make_axlFill ?angle 45.0 ?width "width" ?spacing .05))
	    "ETCH/TOP" "GND"))

	;; negative width
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 4:1.5 4:4 6:4 6:1.5 4:1.5))
	    (list (make_axlFill ?angle 45.0 ?width -1 ?spacing .05))
	    "ETCH/TOP" "GND"))

	;; bad spacing
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 4:1.5 4:4 6:4 6:1.5 4:1.5))
	    (list (make_axlFill ?angle 45.0 ?width .010 ?spacing "space"))
	    "ETCH/TOP" "GND"))

	;; negative increment
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 4:1.5 4:4 6:4 6:1.5 4:1.5))
	    (list (make_axlFill ?angle 45.0 ?width .010 ?spacing -.05))
	    "ETCH/TOP" "GND"))

))

(defun dbc_shp_te_fill_origin ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_te_fill_origin")

	; origin out of drawing - this is currently allowed
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 5:1.5 5:4 7:4 7:1.5 5:1.5))
	    (list (make_axlFill ?angle 45.0 ?width .010 ?spacing .05
					?origin 2000:5000))
	    "ETCH/TOP" "GND"))
	(axlDBCreateCloseShape shape)	; since isn't currently an error

	;; bad origin
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 4:1.5 4:4 6:4 6:1.5 4:1.5))
	    (list (make_axlFill ?angle 45.0 ?width .010 ?spacing .05
					?origin "bad origin"))
	    "ETCH/TOP" "GND"))

))

(defun dbc_shp_te_layer ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_te_layer")
        ;; shape on illegal class
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 3:5.5 3:6.5 4:6.5 4:5.5 3:5.5))
                                        nil "PIN/TOP"))
	(axlDBCreateCloseShape shape)

        ;; shape on illegal subclass
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 3:5.5 3:6.5 4:6.5 4:5.5 3:5.5))
                                        nil "MANUFACTURING/NO_GLOSS_ALL"))
	(axlDBCreateCloseShape shape)
))

(defun dbc_shp_te_open ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_te_open")
        ;; already open shape
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 1:1.5 1:2.5 1.5:2.5 1.5:1.5 1:1.5))
                                        t "ETCH/BOTTOM"))
        (axlDBCreateOpenShape
            (axlPathStart (list 1:1.5 1:2.5 1.5:2.5 1.5:1.8 1:1.5))
                                        t "BOARD GEOMETRY/DIMENSION")
	(axlDBCreateCloseShape shape)	;the one opened
))

(defun dbc_shp_te_path ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_te_path")
        ;; no path specifiied - no error
        (axlDBCreateOpenShape nil nil "BOARD GEOMETRY/DIMENSION")

	;; outline not closed
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 1.3:1.5 1.3:2.5 1.5:2.5 1.5:1 1:1.25))
                                        t "ETCH/BOTTOM"))
	(axlDBCreateCloseShape shape)

	;; outline self intersecting
        (setq shape (axlDBCreateOpenShape
            (axlPathStart
		(list 2.3:1.5 2.5:2.5 2.3:2.5 2.5:1.5 2.3:1.6 2.3:1.5))
                                        t "ETCH/BOTTOM"))
	(axlDBCreateCloseShape shape)
))

(defun dbc_shp_te_rect ()
        ;; illegal rectangle
        (axlMsgPut "**Starting dbc_shp_te_rect")
        (axlDBCreateRectangle (list 8:1.5 8:4)
				t "ETCH/TOP" "VCC"))


(defun dbc_shp_te_void ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_te_void")
        ;; void to an unfilled shape 
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 1:1.5 1:2.5 1.5:2.5 1.5:1.5 1:1.5))
                                        nil "BOARD GEOMETRY/DIMENSION"))
	(axlDBCreateVoidCircle shape (list 1.2:1.8 .01))
	(axlDBCreateCloseShape shape)	;the one opened

        ;; void to filled shape that doesn't allow voids
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 1:1.5 1:2.5 1.5:2.5 1.5:1.5 1:1.5))
                                        t "ROUTE KEEPOUT/ALL"))
	(axlDBCreateVoidCircle shape (list 1.2:1.8 .01))
	(axlDBCreateCloseShape shape)	;the one opened

	;; void boundary not connected
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 1:1.5 1:2.5 1.5:2.5 1.5:1.5 1:1.5))
                                        t "ETCH/BOTTOM"))
        (axlDBCreateVoid shape
            (axlPathStart (list 1.3:1.7 1.3:2.3 1.4:2.3 1.4:1.7 1.35:1.7)))

	;; void boundary crossover
        (axlDBCreateVoid shape
            (axlPathStart
		(list 1.3:1.7 1.4:2.3 1.3:2.3 1.4:1.7 1.3:1.8 1.3:1.7)))
	(axlDBCreateCloseShape shape)	;the one opened

        ;; void to a closed shape 
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 1:1.5 1:2.5 1.5:2.5 1.5:1.5 1:1.5))
                                        t "BOARD GEOMETRY/DIMENSION"))
	(setq shape (car (axlDBCreateCloseShape shape)))
	(axlDBCreateVoidCircle shape (list 1.2:1.8 .01))
))

(defun dbc_shp_te_void_args ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_te_void_args")
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 1:1.5 1:2.5 1.5:2.5 1.5:1.5 1:1.5))
                                        nil "BOARD GEOMETRY/DIMENSION"))

        ;; illegal shape
        (axlDBCreateVoid "not_a_shape")

        ;; illegal path
        (axlDBCreateVoid shape (make_axlFill)) ; axlFill is not an r_path
	(axlDBCreateCloseShape shape)))

(defun dbc_shp_te_void_in_void ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_te_void_in_void")
        ;; void inside another void
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 3:1.5 3:2.5 3.5:2.5 3.5:1.5 3:1.5))
                                        t "BOARD GEOMETRY/DIMENSION"))
	(axlDBCreateVoid shape
	    (axlPathStart (list 3.1:1.9 3.1:2.1 3.3:2.1 3.3:1.9 3.1:1.9)))
	(axlDBCreateVoid shape
	    (axlPathStart (list 3.15:1.95 3.15:2.05
					3.25:2.05 3.25:1.95 3.15:1.95)))
	(axlDBCreateCloseShape shape)
))

(defun dbc_shp_te_void_over_void ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_te_void_over_void")
        ;; void encloses another void
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 4:1.5 4:2.5 4.5:2.5 4.5:1.5 4:1.5))
                                        t "BOARD GEOMETRY/DIMENSION"))
	(axlDBCreateVoid shape
	    (axlPathStart (list 4.15:1.95 4.15:2.05
					4.25:2.05 4.25:1.95 4.15:1.95)))
	(axlDBCreateVoid shape
	    (axlPathStart (list 4.1:1.9 4.1:2.1 4.3:2.1 4.3:1.9 4.1:1.9)))
	(axlDBCreateCloseShape shape)
))

(defun dbc_shp_te_void_outside ()
    (let (shape)
        (axlMsgPut "**Starting dbc_shp_te_void_outside")
        ;; void outside of the shape - simple
        (setq shape (axlDBCreateOpenShape
            (axlPathStart (list 2:1.5 2:2.5 2.5:2.5 2.5:1.5 2:1.5))
                                        t "BOARD GEOMETRY/DIMENSION"))
	(axlDBCreateVoid shape
	    (axlPathStart (list 8:2 8.2:2.2 8.4:2 8.2:1.8 8:2)))

	(axlDBCreateVoidCircle shape (list 1:1 .01))
	(axlDBCreateCloseShape shape)

))


(defun dbc_shp_t10 ()
    (let (shape aVoid)
        axlMsgPut("**Starting dbc_shp_t10 - reopen shape and add circle void")

        ;; filled shape with void and voidCircle
        shape = axlDBCreateOpenShape(
            axlPathStart( list(4000:1000 4000:4000 5000:4500 6000:4000 
				6000:1000 4000:1000))
				t "ETCH/TOP" "GND")
	; add a rectangle void when shape is created
	aVoid = axlDBCreateVoid(shape
	    axlPathStart( list(4050:1050 4050:1150 5000:1150 5000:1050 4050:1050 )))
	axlDBCreateCloseShape(shape)

	; re-open shape and add 2 voids
	;  1st void shows you don't need to pass the shape dbid
	axlDBOpenShape(shape)
	axlDBCreateVoidCircle(nil list( 5000:3000 100))
	axlDBCreateVoidCircle(shape list( 5000:3300 100))
	axlDBCreateCloseShape(shape)

	; add one void, don't bother opening and closing the shape
	axlDBCreateVoidCircle(shape list( 4900:3600 100))

	; pass a poly to create a void
	aPoly = car(axlPolyFromDB(aVoid))
	aPoly = axlPolyOffset(aPoly 100:200)
	printf("HACK %L\n" aPoly)
	axlDBCreateVoid(shape aPoly)
	shape
))

(defun dbc_shp_test ()
        (dbc_shp_t1)
        (dbc_shp_t2)
        (dbc_shp_t3)
        (dbc_shp_t4)
        (dbc_shp_t5)
        (dbc_shp_t6)
        (dbc_shp_t7)
        (dbc_shp_t8)
        (dbc_shp_t9)

	(dbc_shp_te_args)
	(dbc_shp_te_close)
	(dbc_shp_te_fill)
	(dbc_shp_te_fill_origin)
	(dbc_shp_te_layer)
	(dbc_shp_te_open)
	(dbc_shp_te_path)
	(dbc_shp_te_rect)
	(dbc_shp_te_void)
	(dbc_shp_te_void_args)
	(dbc_shp_te_void_in_void)
	(dbc_shp_te_void_over_void)
	(dbc_shp_te_void_outside)
)

