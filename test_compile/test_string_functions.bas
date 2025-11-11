10 REM Test string functions
20 A$ = "Hello World"
30 B$ = "Test"
40 PRINT "Original string: "; A$
50 PRINT "LEFT$(A$, 5) = "; LEFT$(A$, 5)
60 PRINT "RIGHT$(A$, 5) = "; RIGHT$(A$, 5)
70 PRINT "MID$(A$, 7, 5) = "; MID$(A$, 7, 5)
80 PRINT "MID$(A$, 7) = "; MID$(A$, 7)
90 PRINT "LEN(A$) = "; LEN(A$)
100 PRINT "CHR$(65) = "; CHR$(65)
110 PRINT "ASC(""A"") = "; ASC("A")
120 PRINT "STR$(123) = "; STR$(123)
130 PRINT "VAL(""456"") = "; VAL("456")
140 PRINT "SPACE$(5) = ["; SPACE$(5); "]"
150 PRINT "STRING$(5, 42) = "; STRING$(5, 42)
160 PRINT "STRING$(3, ""X"") = "; STRING$(3, "X")
170 PRINT "HEX$(255) = "; HEX$(255)
180 PRINT "OCT$(64) = "; OCT$(64)
190 PRINT "INSTR(A$, ""World"") = "; INSTR(A$, "World")
200 PRINT "INSTR(7, A$, ""o"") = "; INSTR(7, A$, "o")
210 END