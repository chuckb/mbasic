10 REM Test array support
20 DIM A%(10), B%(5,3)
30 REM Test 1D array
40 FOR I% = 0 TO 10
50   LET A%(I%) = I% * 2
60 NEXT I%
70 REM Test array access
80 LET X% = A%(5)
90 REM Test 2D array
100 FOR I% = 0 TO 5
110   FOR J% = 0 TO 3
120     LET B%(I%, J%) = I% + J%
130   NEXT J%
140 NEXT I%
150 REM Test 2D array access
160 LET Y% = B%(2, 1)
170 END