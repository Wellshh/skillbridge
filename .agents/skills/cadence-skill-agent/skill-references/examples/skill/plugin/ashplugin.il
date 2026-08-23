;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 ; Skill File
 ; Author --
 ;	Cadence Design Systems
 ;
 ; Function --
 ;   Demostration of axl Plugin capability
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



unless(boundp('_ashTestDll)
    _ashTestDll = nil 
    _ashEcho = nil
    _ashReturn = nil
    _ashDistance = nil
)

;
; Load plugin, import 3 symbols

procedure( ashPluginLoad()
    prog( (pluginName)

    pluginName = "axlecho_plugin"

    ; load dll
    _ashTestDll = axlDllOpen(pluginName)
    unless(_ashTestDll
	printf("Can't find dll %s\n" pluginName)
	return(nil)
    )

    ; import the 3 symbols in dll
    _ashEcho = axlDllSym(_ashTestDll "ashEcho")
    _ashReturn = axlDllSym(_ashTestDll "ashReturn")
    _ashDistance = axlDllSym(_ashTestDll "ashDistance")

    ; Try
    ; _ashTestDll->??

    return(t)
))


;
; main demostration of plugin functionality

procedure( ashTestDll()
    let( (xy1 xy2)


    ashPluginLoad()

    printf("\nExample of axlDllCall with 1 of each argument\n")
    ret = axlDllCall(_ashEcho 1 2.0 t "is a string" 10.1:20.2)
    printf("Return  %L\n" ret)

    printf("\nExample of axlDllCallList with 1 of each argument\n")
    ret = axlDllCallList(_ashEcho list(-1 -2.0 nil "another string" -10.1:-20.2))
    printf("Return  %L\n" ret)

    printf("\nExample of axlReturn\n")
    ret = axlDllCall(_ashReturn t t t nil nil)
    printf("Return  %L\n" ret)

    xy1 = 10:20
    xy2 = 40:60
    printf("\nCalculate distance between two points %L %L\n" xy1 xy2)
    ret =  ashDistance(10:20 40:60)
    printf("Return  %f\n" ret)

    ; close Dll -- not used
    ; axlDllClose(d)
))

; API wrapper for distance plugin API
;
;	Call  ashDistance(10:0 25.1:0) -> 15.1

procedure( ashDistance( pt1 pt2)
    unless(_ashTestDll
	ashPluginLoad())

    ; call returns list of so take the car of the return
    car( axlDllCall(_ashDistance pt1 pt2) )

    ; Also can do the following
    ; car( axlDllCall( _ashTestDll->functions->ashDistance pt1 pt2) )
)
