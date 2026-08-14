
; Example of using callback function (s_handler) in Allegro's parseFile API

(defun ptest ()
   let((fp file result)

   file = "./test.txt"
   fp = outfile(file)
   fprintf(fp "1|2|3|4\n")
   fprintf(fp "a|b|c|d\n")
   fprintf(fp "AA|BB|CC|DD\n")
   close(fp)

   result = parseFile(file 'ptestCB "|")

   ; for efficiency list is built reversed
   result = reverse(result)

   printf("\n\nResult = %L\n" result)

   deleteFile(file)
))

(defun ptestCB (line lineParsed res)
    printf("LINE = %L\n" line)
    printf("CB = %L\n" lineParsed)
    ; just prepend each parsed line to the master list, return 'res' variable
    res = cons(lineParsed res)

    ; just for grins uncomment the following line. The return MUST be a list.
    ;list("foo")
)
