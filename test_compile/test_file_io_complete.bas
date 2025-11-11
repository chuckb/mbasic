10 REM Test Complete File I/O Support
20 PRINT "=== File I/O Test Suite ==="
30 PRINT
40 REM Test 1: Create and write a file
50 PRINT "Test 1: Writing to test.txt..."
60 OPEN "O", 1, "test.txt"
70 PRINT #1, "First line of text"
80 PRINT #1, "Second line with number: "; 123
90 PRINT #1, "Third and final line"
100 CLOSE 1
110 PRINT "File written and closed."
120 PRINT
130 REM Test 2: Read file and show position
140 PRINT "Test 2: Reading file with LOC/LOF..."
150 OPEN "I", 1, "test.txt"
160 PRINT "File size (LOF): "; LOF(1); " bytes"
170 WHILE NOT EOF(1)
180   PRINT "Position (LOC): "; LOC(1)
190   LINE INPUT #1, L$
200   PRINT "  Read: "; L$
210 WEND
220 PRINT "Final position: "; LOC(1)
230 CLOSE 1
240 PRINT
250 REM Test 3: WRITE# for structured data
260 PRINT "Test 3: WRITE# to data.txt..."
270 OPEN "O", 2, "data.txt"
280 WRITE #2, "John", 25, 1234.56
290 WRITE #2, "Jane", 30, 2345.67
300 CLOSE 2
310 PRINT "Data written."
320 PRINT
330 REM Test 4: INPUT# to read structured data
340 PRINT "Test 4: INPUT# from data.txt..."
350 OPEN "I", 2, "data.txt"
360 INPUT #2, N$, A%, S
370 PRINT "  Name: "; N$; " Age: "; A%; " Salary: "; S
380 INPUT #2, N$, A%, S
390 PRINT "  Name: "; N$; " Age: "; A%; " Salary: "; S
400 CLOSE 2
410 PRINT
420 REM Test 5: Append mode
430 PRINT "Test 5: Appending to test.txt..."
440 OPEN "A", 1, "test.txt"
450 PRINT #1, "Fourth line (appended)"
460 CLOSE 1
470 PRINT "Line appended."
480 PRINT
490 REM Test 6: KILL to delete file
500 PRINT "Test 6: Deleting data.txt..."
510 KILL "data.txt"
520 PRINT "File deleted."
530 PRINT
540 REM Test 7: Multiple files open
550 PRINT "Test 7: Multiple files..."
560 OPEN "O", 1, "file1.txt"
570 OPEN "O", 2, "file2.txt"
580 PRINT #1, "Data for file 1"
590 PRINT #2, "Data for file 2"
600 CLOSE 1
610 CLOSE 2
620 PRINT "Two files written."
630 PRINT
640 REM Cleanup
650 PRINT "Cleaning up test files..."
660 KILL "test.txt"
670 KILL "file1.txt"
680 KILL "file2.txt"
690 PRINT
700 PRINT "=== All File I/O Tests Complete ==="
710 END