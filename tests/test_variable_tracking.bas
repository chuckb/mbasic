10 REM Test variable tracking with ERR% and ERL%
20 PRINT "Initial ERR%=";ERR%
30 PRINT "Initial ERL%=";ERL%
40 ON ERROR GOTO 100
50 X=1/0
60 PRINT "This should not print"
70 END
100 PRINT "Error handler: ERR%=";ERR%;" ERL%=";ERL%
110 END
