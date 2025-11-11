10 REM Test all remaining compiler features
20 REM File operations
30 RESET
40 NAME "OLD.DAT" AS "NEW.DAT"
50 FILES "*.BAS"
60 REM Display operations
70 WIDTH 80
80 LPRINT "Hello, printer!"
90 REM Memory and system
100 CLEAR
110 A = VARPTR(B)
120 C = USR(16384)
130 CALL 16384
140 REM Interpreter-only features (should warn)
150 CHAIN "MENU.BAS"
160 COMMON X, Y, Z
170 END
