
; This demostrates the options of menu editing
;
; See axlUIMenuFind for baseline documentation

procedure( menuTest1()
 let( (q l z)

 ; add a line before add rect 
 q = axlUIMenuFind( nil "add rect")
 z = axlUIMenuInsert(q 'separator )

 ;add a new command at bottom of add menu
 q = axlUIMenuFind(nil 3 'bottom)
 z = axlUIMenuInsert(q "add hello" "echo hello add" )

 ; add a web link at the top of the help menu
 q = axlUIMenuFind( nil -1 'top)
 ;    shows how to embed double quotes in string
 z = axlUIMenuInsert(q "Google" "http \"http://google.com\"")

 ; add a new menubar item -- list method
 q = axlUIMenuFind( nil -1)
 l = '((popup "Drop1") ("hello1" "echo hello1") ("hello2" "echo hello2"))
 z = axlUIMenuInsert(q l)

 ; add a new menubar item -- individual calls
 q = axlUIMenuFind( nil -1)
 z = axlUIMenuInsert(q 'popup "Drop2")
 z = axlUIMenuInsert(nil "hello3"  "echo hello 3")
 z = axlUIMenuInsert(nil "hello4"  "echo hello 4")
 z = axlUIMenuInsert(nil 'popup "Pull1")
 printf("Menu popup id %L\n" z)
 z = axlUIMenuInsert(nil "hello5" "echo hello 5" )
 z = axlUIMenuInsert(nil 'end)
 z = axlUIMenuInsert(nil "hello6" "echo hello 6" )


 ; disable about and add check
 q = axlUIMenuFind( nil "about")
 axlUIMenuChange(q 'enable nil 'check t)

 ; delete first menu item in add menu
 q = axlUIMenuFind(nil 3 'top)
 axlUIMenuDelete(q)

 ; delete edit menu
 q = axlUIMenuFind(nil 1)
 axlUIMenuDelete(q)
))


;--------------------------------------------------------------------------
; the following two examples demostrate adding menu items via the menu trigger
; load this file via the allegro.ilinit file and you should see the menus
; items after allegro starts

; create a menu list
menuList = '(
     (popup "MenuBar")
	("hello" "echo hello")
	(popup "Pull") 
	   ("hello1" "echo hello1") 
	   ("hello2" "echo hello2")
	   (popup "Pull 2") 
	      ("hello3" "echo hello3") 
	   (end)
	end
	(separator)
	("hello4" "echo hello4")
     )

; The following demos additional Allegro script capabilites:
;   - command chaining via the ";" allows multiple commands on 1 line
;   - "scriptmode +i" to make forms invisible; scriptmode value restored at
;	end of command chain
;   - "toggle" value for checkbox form fields will switch the checkbox state
;   - "form_next" for enum fields (or checkboxes) will switch to next enum
;	item (form_prev also availale). Change "FORM" to form_next and
;	remove value 
ml2 = '(
     (popup "QuickKeys")
	   ("EndCaps" "scriptmode +i; prmed; FORM prmedit display_enhance toggle; FORM prmedit done ") 
	   ("Ratsnest" "scriptmode +i; prmed; form_next prmedit ratsnest_display; FORM prmedit done ") 
	)

procedure( menuTrig1()
    ; add to bottom of tool menu
    res = axlUIMenuRegister("reports" menuList 'bottom)

    ; add a new menu item before the help menu
    res = axlUIMenuRegister(-1 ml2)
)

procedure( menuTrig2(t_menufile)
    let( (q)
    printf("MENU FILE= %s\n" t_menufile)
    q = axlUIMenuFind(nil -1)
    res = axlUIMenuInsert(q menuList)
))


;   only 1 line should be uncommented at a time

; To see axlUIMenuRegister uncomment the following line
;menuTrig1()

; Using the trigger function directly
;axlTriggerSet('menu  'menuTrig2)

