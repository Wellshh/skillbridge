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




;; test_textblockgroup  - test attribute access of Textblockgroup Attrs
;find all Textblockgroup Attrs
  ;    print out all attributes of Textblockgroup Parameter type

  (defun test_textblockgroup (p)
    (pprint (setq dsn (axlGetParam "paramTextGroup")) p)
    (fprintf p "\n")
 ;   (pprint dsn->? p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "Setting NChildren to: ")
     (pprint (putprop dsn "15" 'nChildren) p)
    (fprintf p "\n")
    (fprintf p "Expecting no change, found nChildren to be: ")	
    (pprint dsn->nChildren p)
    (fprintf p "\n")
    (fprintf p "Setting objtype to: ")
   (pprint (dsn->objtype="TextGroup") p)
    (fprintf p "\n")
     (fprintf p "Expecting nil, found objtype to be: ")	
   (pprint dsn->objtype p)	
    (fprintf p "\n")
  ) ; defun test_textblockgroup


;; test_layergroup  - test attribute access of Layergroup Attrs
;find all Layergroup Attrs
  ;    print out all attributes of Layergroup Parameter type

  (defun test_layergroup (p)
    (pprint (setq dsn (axlGetParam "paramLayerGroup:PIN")) p)
    (fprintf p "\n")
 ;   (pprint dsn->? p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "Setting NChildren to: ")
     (pprint (putprop dsn "15" 'nChildren) p)
    (fprintf p "\n")
    (fprintf p "Expecting no change, found nChildren to be: ")	
    (pprint dsn->nChildren p)
    (fprintf p "\n")
    (fprintf p "Setting objtype to: ")
   (pprint (dsn->objtype="LayerGroup") p)
    (fprintf p "\n")
   (fprintf p "Expecting nil, found objtype to be: ")	
   (pprint dsn->objtype p)	
    (fprintf p "\n")
 ) ; defun test_layergroup

  (defun test_layergroup1 (p)
    (pprint (setq lg (axlGetParam "paramLayerGroup:via class")) p)
    (fprintf p "\n")
    (fprintf p "Retrieving the same attr twice- objType:\n")
    (pprint lg->objType p)
    (fprintf p "\n")
    (pprint lg->objType p)
    (fprintf p "\n")
   ) ; defun test_layergroup1

(defun test_general (p)
   (let (x y z)
      (setq x (axlGetParam "paramDesign"))
	; test the eval function
	(fprintf p "Eval of x: %s\n", (eval x))
	; test the eq function
	(setq y (axlGetParam "paramDesign"))
	(fprintf p "Eq x y?: ")
	(cond ((equal x y) (fprintf p "t\n")) (t (fprintf p "nil\n")))
        (setq z (axlGetParam "paramDisplay"))
	(fprintf p "Eq x z?: ")
	(cond ((equal x z) (fprintf p "t\n")) (t (fprintf p "nil\n")))
	; test the singlequestion attr retrieval
	(pprint x->? p)
	(fprintf p "\n")
;	(pprint z->activeLayer p)
;	(fprintf p "\n")
	; test illegal attr retrieval
	(fprintf p " retrieving illegal attr, dummy; expecting nil: ")
	(pprint x->dummy p)
;	(fprintf p "\n")
   ) ; let
) ; test_general
  
(defun axlgroup_test ()
 (setq p outfile("bronze.txt", "a"))
 (setq _itemsperline 1)
 (fprintf p "\n\ntest_textblockgroup:\n\n")
 (test_textblockgroup p)
 (fprintf p "\n\ntest_layergroup:\n\n")
 (test_layergroup p)
; (test_layergroup1 p)
 (fprintf p "\n\ntest_general:\n\n")
 (test_general p)
 (close p)
 ) ; defun axlgroup_test

(defun del_file ()
	(deleteFile "bronze.txt")
) ; del_file

(defun my_fail_test1 ()
	(printf "test_design, expecting nil: ")
	(pprint (axlGetParam "design"))
	(printf "\n")
) ; my_fail_test1

(defun my_fail_test2 ()
	(printf "test_layer, expecting nil: ")
	(pprint (axlGetParam "paramtextblock"))
	(printf "\n")
) ; my_fail_test2

(defun my_fail_test3 ()
	(printf "test_layer, expecting nil: ")
	(pprint (axlGetParam "paramLayerGroup:VIA CLASS/paramLayer:VIA"))
	(printf "\n")
) ; my_fail_test3

(defun my_fail_test4 ()
	(printf "test_layer, expecting nil: ")
	(pprint (axlGetParam ""))
	(printf "\n")
) ; my_fail_test4

(defun my_fail_test5 ()
	(printf "test_layer, expecting nil: ")
	(pprint (axlGetParam "paramLayerGroup:VIA_PIN"))
	(printf "\n")
) ; my_fail_test5

(defun my_fail_test6 ()
	(printf "test_layer, expecting nil: ")
	(pprint (axlGetParam "paramLayerGroup:VIA_PIN/paramLayer:TOP"))
	(printf "\n")
) ; my_fail_test6
