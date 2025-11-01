10 REM Test FileIO in Web UI
20 REM This tests SandboxedFileIO (browser localStorage)
30 REM
40 PRINT "FileIO Test for Web UI"
50 PRINT "======================"
60 PRINT
70 REM
100 PRINT "Test 1: List files (should be empty initially)"
110 FILES
120 PRINT
130 REM
200 PRINT "Test 2: Try to list .BAS files"
210 FILES "*.BAS"
220 PRINT
230 REM
300 PRINT "Test 3: Create some test data in localStorage"
310 PRINT "   (You'll need to use browser console for this)"
320 PRINT "   Run in browser console:"
330 PRINT "   localStorage.setItem('mbasic_file_test1.bas', '10 PRINT \"TEST1\"');"
340 PRINT "   localStorage.setItem('mbasic_file_test2.bas', '10 PRINT \"TEST2\"');"
350 PRINT "   localStorage.setItem('mbasic_file_readme.txt', 'This is a test');"
360 PRINT
370 PRINT "   Then RUN this program again to see the files!"
380 PRINT
390 REM
400 PRINT "Test 4: Check what FILES shows after manual setup"
410 PRINT "   (Run this after adding files via console)"
420 REM FILES
430 PRINT
500 PRINT "Done! Press F12 to open browser console and add test files."
510 END
