10 REM Test CP/M Text File Format (CRLF and ^Z)
20 REM First write a test file with normal PRINT#
30 PRINT "Creating CP/M format text file..."
40 OPEN "O", 1, "cpm_test.txt"
50 PRINT #1, "Line 1 - Testing CP/M format"
60 PRINT #1, "Line 2 - Should have CRLF endings"
70 PRINT #1, "Line 3 - Last line before EOF"
80 CLOSE 1
90 PRINT "File created."
100 REM Now read it back line by line
110 PRINT "Reading file back..."
120 OPEN "I", 1, "cpm_test.txt"
130 C% = 0
140 WHILE NOT EOF(1)
150   LINE INPUT #1, L$
160   C% = C% + 1
170   PRINT "Line "; C%; ": ["; L$; "]"
180 WEND
190 CLOSE 1
200 PRINT "Total lines read: "; C%
210 END