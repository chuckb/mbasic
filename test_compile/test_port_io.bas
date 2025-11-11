10 REM Test PEEK, POKE, INP, OUT, WAIT
20 REM Memory operations
30 A = PEEK(100)
40 POKE 100, 42
50 REM Port I/O
60 B = INP(255)
70 OUT 255, 1
80 REM Wait for port condition
90 WAIT 255, 1
100 PRINT "Port I/O test complete"
110 END
