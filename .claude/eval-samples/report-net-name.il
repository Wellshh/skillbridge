; Report the documented database name of a net found by name.
procedure( reportNetName(t_name)
    let((dbid)
        dbid = axlDBFindByName('net t_name)
        when( dbid
            printf("net name: %L\n" axlDbidName(dbid))
        )
        dbid
    )
)
