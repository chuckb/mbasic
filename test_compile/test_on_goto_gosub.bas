10 REM Test ON...GOTO and ON...GOSUB
20 X% = 2
30 PRINT "Testing ON...GOTO with X% = "; X%
40 ON X% GOTO 100, 200, 300
50 PRINT "This should not print (ON GOTO fell through)"
60 GOTO 400
100 PRINT "Jumped to line 100 (X% was 1)"
110 GOTO 400
200 PRINT "Jumped to line 200 (X% was 2)"
210 GOTO 400
300 PRINT "Jumped to line 300 (X% was 3)"
310 GOTO 400
400 REM Test ON...GOSUB
410 Y% = 3
420 PRINT "Testing ON...GOSUB with Y% = "; Y%
430 ON Y% GOSUB 500, 600, 700
440 PRINT "Returned from subroutine"
450 REM Test out of range
460 Z% = 5
470 PRINT "Testing ON...GOTO with Z% = "; Z%; " (out of range)"
480 ON Z% GOTO 100, 200, 300
490 PRINT "Fell through (Z% was out of range)"
495 END
500 PRINT "In subroutine 500 (Y% was 1)"
510 RETURN
600 PRINT "In subroutine 600 (Y% was 2)"
610 RETURN
700 PRINT "In subroutine 700 (Y% was 3)"
710 RETURN