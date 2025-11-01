10 REM Test CHAIN Statement
20 PRINT "Testing CHAIN"
30 PRINT "=============="
40 PRINT
50 REM Test 1: CHAIN with ALL to preserve variables
60 PRINT "Test 1: CHAIN with ALL flag (preserves variables)"
70 X = 42
80 Y$ = "Hello"
90 PRINT "Before CHAIN: X ="; X; ", Y$ = "; Y$
100 PRINT
110 CHAIN "/tmp/chain_target.bas", , ALL
120 PRINT "Returned from CHAIN"
130 PRINT "After CHAIN: X ="; X; ", Y$ = "; Y$
140 PRINT
150 PRINT "Test 2: CHAIN without ALL (variables reset)"
160 A = 99
170 B$ = "World"
180 PRINT "Before CHAIN: A ="; A; ", B$ = "; B$
190 PRINT
200 CHAIN "/tmp/chain_target2.bas"
210 PRINT "Returned from CHAIN"
220 PRINT "After CHAIN: A ="; A; ", B$ = "; B$
230 PRINT
240 PRINT "CHAIN tests complete!"
250 END
