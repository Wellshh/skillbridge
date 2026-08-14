
procedure( XnetSelectByName(t_name  @optional (g_wildcard nil))
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

