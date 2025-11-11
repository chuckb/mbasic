10 REM Test FRE() function
20 PRINT "Testing FRE() function"
30 PRINT
40 REM Test FRE(0) - total free memory
50 F = FRE(0)
60 PRINT "FRE(0):"; F
70 PRINT
80 REM Test FRE("") - string pool free space before allocation
90 S = FRE("")
100 PRINT "FRE(\"\") before:"; S
110 PRINT
120 REM Allocate some strings
130 A$ = "Hello World"
140 B$ = "Test String"
150 C$ = "More Data"
160 PRINT "Allocated 3 strings"
170 PRINT
180 REM Check string pool after allocation
190 S2 = FRE("")
200 PRINT "FRE(\"\") after:"; S2
210 PRINT "Used:"; S - S2
220 END
