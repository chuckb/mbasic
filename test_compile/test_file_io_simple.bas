10 REM Test File I/O for Compiler
20 REM Write a file with PRINT#
30 PRINT "Writing to test.txt..."
40 OPEN "O", 1, "test.txt"
50 PRINT #1, "First line"
60 PRINT #1, "Second line"
70 PRINT #1, "Third line with number: "; 42
80 CLOSE 1
90 PRINT "File written"
100 REM Read it back with INPUT#
110 PRINT "Reading from test.txt..."
120 OPEN "I", 1, "test.txt"
130 WHILE NOT EOF(1)
140 LINE INPUT #1, L$
150 PRINT "Read: "; L$
160 WEND
170 CLOSE 1
180 PRINT "Done reading"
190 REM Test WRITE# with comma-delimited data
200 PRINT "Writing data.txt with WRITE#..."
210 OPEN "O", 2, "data.txt"
220 WRITE #2, "Alice", 25, 1234.56
230 WRITE #2, "Bob", 30, 2345.67
240 CLOSE 2
250 PRINT "Data file written"
260 REM Read back with INPUT#
270 PRINT "Reading data.txt with INPUT#..."
280 OPEN "I", 2, "data.txt"
290 INPUT #2, N$, A%, S
300 PRINT "Name: "; N$; " Age: "; A%; " Salary: "; S
310 INPUT #2, N$, A%, S
320 PRINT "Name: "; N$; " Age: "; A%; " Salary: "; S
330 CLOSE 2
340 PRINT "Test complete!"
350 END