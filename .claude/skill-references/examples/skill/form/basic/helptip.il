;;	
; Demostration of an helptip form capability (see axlFORMBNFDoc)
;	requires helptip.form
;
; In form file:
;      - Fields have HELPTIP keyword
;      - Provide INFO text field with field name of helptip

;----------------------------------------------------------------
;----------------------------------------------------------------
;----------------------------------------------------------------
; 1) Standalone form -- 

; form handle
unless(boundp('_heltip_fw) _heltip_fw = nil)
;
;


procedure( helptip()
    let( (fw)
    fw = axlFormCreate('_heltip_fw "helptip"
		'("msgLines" 0) 'heltip_CB t nil)
    axlFormDisplay(fw)
))

; END PUBLIC FUNCTIONS
;----------------------------------------------------------------
 
;----------------------------------------------------------------
;; Form callback with grid control
procedure( heltip_CB(fw)
    prog(()
     unless((fw->doneState == 0)
	 axlFormClose(fw)
	 return(t)
     )
))
 
