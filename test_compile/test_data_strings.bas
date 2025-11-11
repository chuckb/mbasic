10 REM Test DATA/READ with strings
20 DATA "Hello", "World", 123, 456.789
30 DATA "Alpha", "Beta", "Gamma"
40 DIM A$(3), B$(3)
50 READ A$(1), A$(2), N%, X!
60 PRINT "First string: "; A$(1)
70 PRINT "Second string: "; A$(2)
80 PRINT "Number: "; N%
90 PRINT "Float: "; X!
100 READ A$(3), B$(1), B$(2)
110 PRINT "Third string: "; A$(3)
120 PRINT "Fourth string: "; B$(1)
130 PRINT "Fifth string: "; B$(2)
140 REM Test RESTORE
150 RESTORE
160 READ C$
170 PRINT "After RESTORE, first value: "; C$
180 END