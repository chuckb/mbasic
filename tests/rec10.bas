10 PRINT "Testing recursive GOSUB depth 10"
20 D=0:M=10
30 GOSUB 100
40 PRINT "Back to main, depth reached:";D
50 END
100 D=D+1
110 PRINT "Depth:";D
120 IF D>=M THEN RETURN
130 GOSUB 100
140 PRINT "Returned at depth:";D
150 RETURN
