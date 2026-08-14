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




;; test_display  - test attribute access of Display Attrs
;find all Display Attrs
  ;    print out all attributes of Display Parameter type

  (defun test_display (p)
    (pprint (setq dsn (axlGetParam "paramDisplay")) p)
    (fprintf p "\n")
;    (pprint dsn->? p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "Setting ActiveLayer to: ")
     (pprint (putprop dsn "PIN/PASTEMASK_TOP" 'activeLayer) p)
    (fprintf p "\n")
    (fprintf p "Found activeLayer to be: ")	
    (pprint dsn->activeLayer p)
    (fprintf p "\n")
    (fprintf p "Setting AltLayer to: ")
     (pprint (putprop dsn "ETCH/THREE" 'altLayer) p)
    (fprintf p "\n")
    (fprintf p "Found AltLayer to be: ")	
    (pprint dsn->altLayer p)
    (fprintf p "\n")
    (fprintf p "Setting snap to: ")
     (pprint (putprop dsn nil 'snap) p)
    (fprintf p "\n")
    (fprintf p "Found snap to be: ")	
    (pprint dsn->snap p)
    (fprintf p "\n")
    (fprintf p "Setting autoFindFilter to: ")
    (pprint (dsn->autoFindFilter=nil) p)
    (fprintf p "\n")
    (fprintf p "Found autoFindFilter to be: ")	
    (pprint dsn->autoFindfilter p)
    (fprintf p "\n")
    (fprintf p "Setting objtype to: ")
   (pprint (dsn->objtype="Display") p)
    (fprintf p "\n")
    (fprintf p "Expecting nil, found objtype to be: ")	
   (pprint dsn->objtype p)	
    (fprintf p "\n")
    (fprintf p "\n")
    (fprintf p "Setting layer object, found to be: ")	
   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
    (fprintf p "Retrieving layer object, found to be: ")	
    (pprint (setq dsn (axlGetParam "paramDisplay")) p)
  (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
   ) ; defun test_display

  
(defun axldisplay_test ()
 (setq p outfile("bronze.txt", "a"))
 (setq _itemsperline 1)
 (fprintf p "\n\n*test_display:******************************************\n\n")
 (test_display p)
 (close p)
 ) ; defun axldisplay_test
