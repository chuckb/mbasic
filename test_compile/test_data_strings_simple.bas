10 REM Test DATA/READ with strings
20 DATA "Hello", "World", 123, 456.789
30 DATA "Alpha", "Beta", "Gamma"
40 READ A$, B$, N%, X!
50 PRINT "First string: "; A$
60 PRINT "Second string: "; B$
70 PRINT "Number: "; N%
80 PRINT "Float: "; X!
90 READ C$, D$, E$
100 PRINT "Third string: "; C$
110 PRINT "Fourth string: "; D$
120 PRINT "Fifth string: "; E$
130 REM Test RESTORE
140 RESTORE
150 READ F$
160 PRINT "After RESTORE, first value: "; F$
170 END