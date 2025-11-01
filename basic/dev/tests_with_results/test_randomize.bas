10 REM Test RANDOMIZE statement
20 PRINT "Test 1: RANDOMIZE with specific seed"
30 RANDOMIZE 42
40 PRINT "First random number: "; RND
50 PRINT "Second random number: "; RND
60 PRINT "Third random number: "; RND
70 PRINT
80 PRINT "Test 2: RANDOMIZE with same seed (should give same sequence)"
90 RANDOMIZE 42
100 PRINT "First random number: "; RND; " (should match above)"
110 PRINT "Second random number: "; RND; " (should match above)"
120 PRINT "Third random number: "; RND; " (should match above)"
130 PRINT
140 PRINT "Test 3: RANDOMIZE with different seed"
150 RANDOMIZE 123
160 PRINT "First random number: "; RND; " (should be different)"
170 PRINT "Second random number: "; RND; " (should be different)"
180 PRINT "Third random number: "; RND; " (should be different)"
190 PRINT
200 PRINT "Test 4: RANDOMIZE with expression as seed"
210 X = 99
220 RANDOMIZE X + 1
230 PRINT "First random number: "; RND
240 PRINT "Second random number: "; RND
250 PRINT
260 PRINT "Test 5: RANDOMIZE without seed (uses timer)"
270 RANDOMIZE
280 PRINT "Random number with timer seed: "; RND
290 PRINT "Random number with timer seed: "; RND
300 END
