
; This code demostrates passing arguments from the Allegro command line to a register
;	Skill commad (axlCmdRegister)
;
; Rules: 
;	- args are always passed from Allegro cmd line to Skill as strings
;	- whitespace is used to separate strings on Allegro cmd line into multiple arguments
;
; Method 3 is recommended since user will never see a generic Skill error 

;------------------------------------------
; 1) Simple example zero or 1 arg
;	Examples: 
;		mycmd t
;		mycmd 
procedure( mycmd( @optional (arg nil))
	printf("ARG %L\n" arg)
)

axlCmdRegister("mycmd" 'mycmd ?cmdType "general")

;------------------------------------------
; 2) zero, 1 or 2 args
;	Examples: 
;		mycmd2 foo bar
;		mycmd2 foo 
;		mycmd2 
procedure( mycmd2( @optional (arg nil) (arg2 "2"))
	printf("ARG %L 2= %L\n" arg arg2)
)
	
axlCmdRegister("mycmd2" 'mycmd2 ?cmdType "general")


;------------------------------------------
; 3) Recommended method
;	Examples: 
;		generalargs
;		generalargs 1 2 3 4 5 6
procedure( mycmdRecommended( @rest nameList)
	printf("REST= %L\n" nameList)
)
	
axlCmdRegister("generalargs" 'mycmdRecommended ?cmdType "general")

