10 REM Test random access file operations
20 PRINT "Testing random access files (partial support)"
30 PRINT
40 REM Open a random access file
50 OPEN "R", 1, "random.dat", 80
60 REM Define field structure
70 FIELD #1, 20 AS NAME$, 10 AS PHONE$, 50 AS ADDR$
80 REM Set field values
90 LSET NAME$ = "John Doe"
100 LSET PHONE$ = "555-1234"
110 LSET ADDR$ = "123 Main Street"
120 REM Write record
130 PUT #1, 1
140 REM Read it back
150 GET #1, 1
160 PRINT "Name: "; NAME$
170 PRINT "Phone: "; PHONE$
180 PRINT "Address: "; ADDR$
190 CLOSE 1
200 END