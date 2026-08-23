; Appends Site specific Skill path(s) to skill path using an
; Allegro or Bourne shell environment variable SITE_SKILLPATH.
; It then optionally loads a site.ilinit file which may load
; the site's Skill package.
; 
; Useage:
;     1) add to start of each users ~/pcbenv/allegro.ilinit file
;     2) Have each user set environment variable, SITE_SKILLPATH either
;	 in Allegro env file or at the OS level.
;     3) Create a site.ilinit file in one of the directories
;	 specified in SITE_SKILLPATH. Have this file load site files
;   
; See also: Building & loading contextes for faster startup
;
(let (siteEnv)
    siteEnv = axlGetVariable("SITE_SKILLPATH")
    when(siteEnv
	setSkillPath(append(parseString(siteEnv) getSkillPath()))
	)
)

errset( load( "site.ilinit"))
