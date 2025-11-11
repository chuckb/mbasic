10 REM Simple error test
20 PRINT "Testing error handling"
30 ON ERROR GOTO 100
40 PRINT "About to trigger error"
50 ERROR 11
60 PRINT "This should not print"
70 END
100 PRINT "Error caught!"
110 PRINT "Error code is"; ERR
120 PRINT "Error line is"; ERL
130 END