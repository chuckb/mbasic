10 REM Test JavaScript type coercion
20 DEFINT I-K
30 DEFDBL D
40 REM
50 REM Test INTEGER truncation on assignment
60 I = 3.7
70 PRINT "I = 3.7 -> "; I
80 I = -3.7
90 PRINT "I = -3.7 -> "; I
100 I = 32768
110 PRINT "I = 32768 -> "; I
120 I = -32769
130 PRINT "I = -32769 -> "; I
140 REM
150 REM Test SINGLE precision (via explicit suffix)
160 X! = 1/3
170 PRINT "X! = 1/3 -> "; X!
180 REM
190 REM Test DOUBLE precision (via DEFDBL)
200 D = 1/3
210 PRINT "D = 1/3 -> "; D
220 REM
230 REM Test FOR loop with INTEGER variable
240 PRINT "FOR I = 1 TO 3.5:"
250 FOR I = 1 TO 3.5
260 PRINT "  I = "; I
270 NEXT I
280 PRINT "After loop I = "; I
290 REM
300 REM Test type suffix on variable
310 Y% = 99.9
320 PRINT "Y% = 99.9 -> "; Y%
330 Z# = 1/7
340 PRINT "Z# = 1/7 -> "; Z#
350 REM
360 PRINT "Done!"
370 END
