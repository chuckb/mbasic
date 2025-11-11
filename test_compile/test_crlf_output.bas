10 REM Test CRLF output
20 PRINT "Writing file with CRLF..."
30 OPEN "O", 1, "crlf_test.txt"
40 PRINT #1, "Line 1"
50 PRINT #1, "Line 2"
60 PRINT #1, "Line 3"
70 CLOSE 1
80 PRINT "File written. Check crlf_test.txt"
90 END