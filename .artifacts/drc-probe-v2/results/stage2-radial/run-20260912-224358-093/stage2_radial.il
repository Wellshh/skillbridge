;;; II-B radial-versus-vertical probe. DBIDs are resolved inside each RPC.
(putd '__v2DrcViaItemCount nil)
(defun __v2DrcViaItemCount (padstack netName x y)
  (letseq ((design (axlDBRefreshId (axlDBGetDesign))) matches via)
    (foreach n design->nets
      (when (equal n->name netName)
        (foreach b n->branches
          (foreach item b->children
            (when (and (equal item->objType "via")
                       (equal (car item->xy) x) (equal (cadr item->xy) y))
               (setq matches (cons item matches)))))))
    (cond ((null matches) (error "DRC_VIA_TARGET_NOT_FOUND"))
          ((cdr matches) (error "DRC_VIA_TARGET_AMBIGUOUS")))
    (setq via (car matches))
    (unless (equal via->name padstack) (error "DRC_VIA_PADSTACK_MISMATCH"))
    (list nil 'resolved t 'count (axlDRCItem nil via)
          'markers (let (out)
                     (foreach m (axlDRCItem t via)
                       (setq out (cons (list nil 'data (__abProjectDrc m)
                                                   'waived m->waived
                                                   'allegro_generated m->fixed) out)))
                     (reverse out)))))
