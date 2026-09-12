(putd '__v2DiagProjectOne nil)
(defun __v2DiagProjectOne (m)
 (let (rawToken refreshed figs figout fraw fref)
  (setq rawToken (sprintf nil "%L" m))
  (setq refreshed (axlDBRefreshId m))
  (setq figout nil)
  (if refreshed then
   (progn
    (setq figs refreshed->violations)
    (foreach f figs
     (setq fraw (sprintf nil "%L" f))
     (setq fref (axlDBRefreshId f))
     (setq figout (cons (list nil 'rawToken fraw 'refreshedToken (sprintf nil "%L" fref) 'refreshNil (if fref then nil else t)) figout)))
    (list nil 'rawToken rawToken 'refreshedToken (sprintf nil "%L" refreshed) 'refreshNil nil 'data (__abProjectDrc refreshed) 'figures (reverse figout) 'waived refreshed->waived 'allegro_generated refreshed->fixed))
   else
    (list nil 'rawToken rawToken 'refreshedToken (sprintf nil "%L" refreshed) 'refreshNil t 'data nil 'figures nil 'waived nil 'allegro_generated nil))))
(putd '__v2DiagItem nil)
(defun __v2DiagItem (kind primary secondary layer objType start end width radius cw center)
 (let (target count markers out)
  (setq target (__abFindDrcItem kind primary secondary layer objType start end width radius cw center))
  (if target then
   (progn
    (setq count (axlDRCItem nil target))
    (setq markers (axlDRCItem t target))
    (foreach m markers (setq out (cons (__v2DiagProjectOne m) out)))
    (list nil 'resolved t 'count count 'markers (reverse out)))
   else (list nil 'resolved nil 'count nil 'markers nil))))
(putd '__v2DiagSnapshot nil)
(defun __v2DiagSnapshot ()
 (let ((design (axlDBRefreshId (axlDBGetDesign))) out)
  (foreach m design->drcs (setq out (cons (__v2DiagProjectOne m) out)))
  (list nil 'count (axlDRCGetCount) 'markers (reverse out))))
