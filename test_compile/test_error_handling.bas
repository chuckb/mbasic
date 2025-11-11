10 REM Test error handling
20 ON ERROR GOTO 1000
30 PRINT "Setting up error handler..."
40 PRINT
50 REM Trigger an error
60 PRINT "Triggering error 50..."
70 ERROR 50
80 PRINT "This should not print!"
90 GOTO 2000
100 REM
1000 REM Error handler
1010 PRINT "Error handler reached!"
1020 PRINT "Error code:"; ERR
1030 PRINT "Error line:"; ERL
1040 PRINT
1050 REM Clear error and resume
1060 RESUME 2000
1070 REM
2000 REM End of program
2010 PRINT "Program completed"
2020 END