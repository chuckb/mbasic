10 REM Web UI Debugger Verification Test
20 REM This program tests all debugger features
30 REM
40 REM Test 1: Step mode shows NEXT statement
50 FOR I=0 TO 3
60 PRINT "I="; I
70 NEXT I
80 REM
90 REM Test 2: GOSUB/RETURN jumps
100 PRINT "Before GOSUB"
110 GOSUB 200
120 PRINT "After GOSUB"
130 REM
140 REM Test 3: Mid-line GOSUB and RETURN
150 PRINT "A": GOSUB 300: PRINT "B"
160 REM
170 REM Test 4: Multi-statement line
180 PRINT "X": PRINT "Y": PRINT "Z"
190 END
200 REM Subroutine 1
210 PRINT "In subroutine 1"
220 Q=Q+1
230 RETURN
300 REM Subroutine 2
310 J=J+1
320 RETURN
