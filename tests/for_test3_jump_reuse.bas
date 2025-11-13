10 REM Test: Jump out and reuse variable
20 PRINT "Starting FOR I loop..."
30 FOR I=1 TO 10
40 PRINT "I=";I
50 IF I=3 THEN GOTO 100
60 NEXT I
70 PRINT "Never reach here"
80 SYSTEM
100 PRINT "Jumped out at I=";I
110 PRINT "Starting new FOR I loop..."
120 FOR I=1 TO 5
130 PRINT "New I=";I
140 NEXT I
150 PRINT "Success!"
160 SYSTEM
