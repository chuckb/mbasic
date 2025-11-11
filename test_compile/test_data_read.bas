10 REM Test DATA/READ/RESTORE statements
20 DATA 10, 20, 30, 40, 50
30 DATA 1.5, 2.5, 3.5
40 DATA "Hello", "World"
50 REM Read integer values
60 READ A%, B%, C%
70 PRINT "Integers: "; A%; ", "; B%; ", "; C%
80 REM Read float values
90 READ X!, Y!, Z!
100 PRINT "Floats: "; X!; ", "; Y!; ", "; Z!
110 REM Test RESTORE
120 RESTORE
130 READ D%, E%
140 PRINT "After RESTORE: "; D%; ", "; E%
150 END