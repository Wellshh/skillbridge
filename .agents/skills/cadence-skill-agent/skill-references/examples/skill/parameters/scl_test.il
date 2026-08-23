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




;; test_layer  - test attribute access of Layer Attrs
;find all Layer Attrs
 ;;    print out all attributes of Layer Parameter type


  (defun test_layer (p)
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:top")) p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "Setting color to: ")
     (pprint (putprop dsn 8 'color) p)
    (fprintf p "\n")
    (fprintf p "Found color to be: ")	
    (pprint dsn->color p)
    (fprintf p "\n")
    (fprintf p "Setting visibility to: ")
    (pprint (dsn->visible=t) p)
    (fprintf p "\n")
    (fprintf p "Found visible to be: ")	
    (pprint dsn->visible p)
    (fprintf p "\n")
    (fprintf p "Setting isEtch to: ")
    (pprint (dsn->isEtch=nil) p)
    (fprintf p "\n")
    (fprintf p "Expecting no change, found isEtch to be: ")
    (pprint dsn->isEtch p)
    (fprintf p "\n")
    (fprintf p "Setting Name to: ")
     (pprint (putprop dsn "BETTER" 'name) p)
    (fprintf p "\n")
    (fprintf p "Found name to be: ")	
    (pprint dsn->name p)
    (fprintf p "\n")
    (fprintf p "Setting objtype to: ")
   (pprint (dsn->objtype="Layer") p)
    (fprintf p "\n")
    (fprintf p "Expecting nil, found objtype to be: ")	
   (pprint dsn->objtype p)	
     (fprintf p "\n")
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "\n")
    (fprintf p "Setting layer object, found to be: ")
   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
    (fprintf p "Retrieving layer object, found to be: ")
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:better")) p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
   ) ; defun test_layer

  (defun test_layer1 (p)
    (pprint (setq dsn (axlGetParam "paramLayerGroup:via class/paramLayer:soldermask_top")) p)
    (fprintf p "\n")
 ;   (pprint dsn->? p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "Setting visibility to: ")
    (pprint (dsn->visible=nil) p)
;     (pprint (putprop dsn nil 'visible) p)
    (fprintf p "\n")
    (fprintf p "Found visible to be: ")	
    (pprint dsn->visible p)
    (fprintf p "\n")
    (fprintf p "Setting Name to: ")
     (pprint (putprop dsn "BETTER" 'name) p)
    (fprintf p "\n")
    (fprintf p "Found name to be: ")	
    (pprint dsn->name p)
    (fprintf p "\n")
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "\n")
    (fprintf p "Setting layer object,expecting nil, found to be: ")
   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
   (fprintf p "Returned nil as parentName is not ETCH")
    (fprintf p "\n")
    (fprintf p "Retrieving layer object, found to be: ")
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:better")) p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
   ) ; defun test_layer1


  (defun test_layer2 (p)
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:two")) p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "Setting visibility to: ")
    (pprint (dsn->visible=nil) p)
    (fprintf p "\n")
    (fprintf p "Found visible to be: ")	
    (pprint dsn->visible p)
    (fprintf p "\n")
    (fprintf p "Setting Name to: ")
     (pprint (putprop dsn "WORK" 'name) p)
    (fprintf p "\n")
    (fprintf p "Found name to be: ")	
    (pprint dsn->name p)
    (fprintf p "\n")
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "\n")
    (fprintf p "Setting layer object, found to be: ")
   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
    (fprintf p "Retrieving layer object, found to be: ")
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:work")) p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
   ) ; defun test_layer2


  (defun test_layer3 (p)
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:better")) p)
    (fprintf p "\n")
 ;   (pprint dsn->? p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "Setting color to: ")
;     (pprint (putprop dsn 50 'color) p)
    (pprint (dsn->color=50) p)
    (fprintf p "\n")
    (fprintf p "Found color to be: ")	
    (pprint dsn->color p)
    (fprintf p "\n")
    (fprintf p "Setting Name to: ")
     (pprint (putprop dsn "WORK" 'name) p)
    (fprintf p "\n")
    (fprintf p "Found name to be: ")	
    (pprint dsn->name p)
    (fprintf p "\n")
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "\n")
    (fprintf p "Setting layer object,expecting nil, found to be: ")
   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
   (fprintf p "Returned nil as color index is illegal")
    (fprintf p "\n")
    (fprintf p "Retrieving layer object,expecting nil, found to be: ")
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:work")) p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
   ) ; defun test_layer3

  (defun test_layer4 (p)
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:three")) p)
    (fprintf p "\n")
 ;   (pprint dsn->? p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "Setting Name to: ")
     (pprint (putprop dsn "TWO" 'name) p)
    (fprintf p "\n")
    (fprintf p "Found name to be: ")	
    (pprint dsn->name p)
    (fprintf p "\n")
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "\n")
    (fprintf p "Setting layer object,expecting nil, found to be: ")
   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
    (fprintf p "Retrieving layer object, found to be: ")
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:two")) p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
   ) ; defun test_layer4


  (defun test_layer5 (p)
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:two")) p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "Setting visibility to: ")
;    (pprint (dsn->visible=t) p)
     (pprint (putprop dsn t 'visible) p)
    (fprintf p "\n")
    (fprintf p "Found visible to be: ")	
    (pprint dsn->visible p)
    (fprintf p "\n")
    (fprintf p "Setting Name to: ")
     (pprint (putprop dsn "BETTER" 'name) p)
    (fprintf p "\n")
    (fprintf p "Found name to be: ")	
    (pprint dsn->name p)
    (fprintf p "\n")
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "\n")
    (fprintf p "Setting layer object, found to be: ")
   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
    (fprintf p "Returned nil as sclass name already exists")
    (fprintf p "\n")
    (fprintf p "Retrieving layer object, found to be: ")
    (pprint (setq dsn (axlGetParam "paramLayerGroup:etch/paramLayer:BETTER")) p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
   ) ; defun test_layer5


   
(defun axllayer_test ()
 (setq p outfile("bronze.txt", "a"))
 (setq _itemsperline 1)
 (fprintf p "\n\n*test_layer:********************************************\n\n")
 (test_layer p)
 (fprintf p "\n\n*test_layer1:\n\n")
 (test_layer1 p)	
 (fprintf p "\n\n*test_layer2:\n\n")
 (test_layer2 p) 
 (fprintf p "\n\n*test_layer3:\n\n")
 (test_layer3 p) 
 (fprintf p "\n\n*test_layer4:\n\n")
 (test_layer4 p) 
 (fprintf p "\n\n*test_layer5:\n\n")
 (test_layer5 p) 
 (close p)
 ) ; defun axllayer_test
