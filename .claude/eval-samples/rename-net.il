; Rename a net and report the outcome in the main window message line.
procedure( renameNet(t_old t_new)
    if( axlRenameNet(t_old t_new)
        then axlUIWPrint(nil "renamed %s to %s" t_old t_new)
        else warn("rename of %s failed\n" t_old)
    )
)
