10 REM Test FRE() function - both numeric and string forms
20 PRINT "Testing FRE() function"
30 PRINT
40 REM Test FRE(0) - total free memory
50 F = FRE(0)
60 PRINT "FRE(0) - Total free memory:"; F; "bytes"
70 PRINT
80 REM Test FRE("") - string pool free space
90 S = FRE("")
100 PRINT "FRE(\"\") - String pool free:"; S; "bytes"
110 PRINT
120 REM Allocate some strings
130 A$ = "Hello, World!"
140 B$ = "This is a test string."
150 C$ = "More string data here."
160 PRINT "Allocated 3 strings:"
170 PRINT "  A$ = "; A$
180 PRINT "  B$ = "; B$
190 PRINT "  C$ = "; C$
200 PRINT
210 REM Check string pool free space after allocation
220 S2 = FRE("")
230 PRINT "FRE(\"\") after allocation:"; S2; "bytes"
240 PRINT "String space used:"; S - S2; "bytes"
250 PRINT
260 REM Test FRE(numeric expression)
270 X = 5
280 F2 = FRE(X * 2)
290 PRINT "FRE(X*2) where X=5:"; F2; "bytes"
300 END
