#!/bin/bash
exec 2>mbasic_stderr.log
python3 mbasic --ui curses test_end_stderr.bas
