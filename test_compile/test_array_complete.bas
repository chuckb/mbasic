10 REM Complete array test
20 DIM A%(10), B!(5), C#(3,3), D(2,2,2)
30 REM Test integer array
40 FOR I% = 0 TO 10
50   LET A%(I%) = I% * 2
60 NEXT I%
70 REM Test single precision array
80 FOR I% = 0 TO 5
90   LET B!(I%) = I% * 1.5
100 NEXT I%
110 REM Test double precision 2D array
120 FOR I% = 0 TO 3
130   FOR J% = 0 TO 3
140     LET C#(I%, J%) = I% * 10 + J%
150   NEXT J%
160 NEXT I%
170 REM Test 3D array
180 FOR I% = 0 TO 2
190   FOR J% = 0 TO 2
200     FOR K% = 0 TO 2
210       LET D(I%, J%, K%) = I% * 100 + J% * 10 + K%
220     NEXT K%
230   NEXT J%
240 NEXT I%
250 REM Test array access in expressions
260 LET X% = A%(5) + A%(6)
270 LET Y! = B!(2) * B!(3)
280 LET Z# = C#(1, 2) + C#(2, 1)
290 LET W = D(1, 1, 1) + D(0, 1, 2)
300 END