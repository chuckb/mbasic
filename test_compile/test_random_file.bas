10 REM Test random file I/O
20 REM Create a simple database with name and age records
30 OPEN "R", #1, "test.dat"
40 FIELD #1, 20 AS N$, 5 AS A$
50 REM
60 REM Write three records
70 LSET N$ = "Alice"
80 RSET A$ = "25"
90 PUT #1, 1
100 REM
110 LSET N$ = "Bob"
120 RSET A$ = "30"
130 PUT #1, 2
140 REM
150 LSET N$ = "Charlie"
160 RSET A$ = "35"
170 PUT #1, 3
180 REM
190 REM Read back and display
200 PRINT "Reading records:"
210 FOR I = 1 TO 3
220 GET #1, I
230 PRINT "Record"; I; ": Name="; N$; " Age="; A$
240 NEXT I
250 CLOSE #1
260 PRINT "Test complete!"
270 END
