10 REM String test program
20 INPUT "Enter your name: ", NAME$
30 INPUT "Enter your city: ", CITY$
40 GREETING$ = "Hello " + NAME$ + " from " + CITY$
50 PRINT GREETING$
60 FIRST$ = LEFT$(NAME$, 3)
70 PRINT "First 3 chars: "; FIRST$
80 LEN1% = LEN(NAME$)
90 PRINT "Name length:"; LEN1%
100 END