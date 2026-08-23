
; Normally axlSelectByName returns single net xnets. If you
; desire only multi-net xnets use this function instead of
; axlSelectByName

procedure( ashXnetSelectByName(t_name  @optional (g_wildcard nil))
    let((names xnets)
    names = axlSelectByName("XNET" t_name g_wildcard)
    when(names 
	foreach(item names
	   when(item->type=="XNET"
	   	xnets = cons(item xnets))
	)
    )
    xnets
))

