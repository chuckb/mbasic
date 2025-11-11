10 REM Test reading CP/M format file with CRLF and ^Z
20 PRINT "Reading real_cpm.txt (CP/M format)..."
30 OPEN "I", 1, "real_cpm.txt"
40 C% = 0
50 WHILE NOT EOF(1)
60   LINE INPUT #1, L$
70   C% = C% + 1
80   PRINT "Line "; C%; ": ["; L$; "]"
90 WEND
100 CLOSE 1
110 PRINT "Total lines read: "; C%
120 PRINT "Successfully read CP/M format file!"
130 END